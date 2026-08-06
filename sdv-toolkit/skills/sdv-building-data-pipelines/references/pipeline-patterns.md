# Pipeline Patterns

Common patterns for building ETL pipelines with Polars, DuckDB, and PyArrow. Covers basic ETL structure, incremental loading strategies, and resilience patterns.

## Table of Contents

1. [Basic ETL Structure](#basic-etl-structure)
2. [Incremental Loading](#incremental-loading)
3. [Resilience Patterns](#resilience-patterns)
4. [Testing Patterns](#testing-patterns)

---

## Basic ETL Structure

### Reusable ETL Framework

```python
import polars as pl
import duckdb
from pathlib import Path
from datetime import datetime
from typing import Protocol
import logging

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Reusable ETL framework with lazy evaluation."""

    def __init__(self, config: dict):
        self.config = config
        self.raw_path = Path(config["raw_path"])
        self.processed_path = Path(config["processed_path"])

    def extract(self, source: str) -> pl.LazyFrame:
        """Read source data as LazyFrame for efficient processing."""
        if source.endswith(".csv"):
            return pl.scan_csv(source)
        elif source.endswith(".parquet"):
            return pl.scan_parquet(source)
        else:
            raise ValueError(f"Unsupported format: {source}")

    def transform(self, df: pl.LazyFrame) -> pl.LazyFrame:
        """Apply transformations (lazy - not executed yet)."""
        return (
            df
            .filter(pl.col("value").is_not_null())
            .with_columns([
                pl.col("date").str.to_date(),
                pl.col("amount").cast(pl.Float64),
                pl.col("category").str.to_lowercase()
            ])
            .group_by(["category", "date"])
            .agg([
                pl.col("amount").sum().alias("total_amount"),
                pl.col("id").count().alias("count")
            ])
        )

    def load(self, df: pl.DataFrame) -> dict:
        """Materialize and store results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = self.processed_path / f"output_{timestamp}.parquet"
        df.write_parquet(output_path)

        with duckdb.connect(self.config.get("duckdb_path", "analytics.db")) as con:
            con.sql("CREATE OR REPLACE TABLE daily_summary AS SELECT * FROM df")

        return {"output": str(output_path), "rows": len(df)}

    def run(self, source_path: str) -> dict:
        """Execute full pipeline with error handling."""
        logger.info(f"Starting ETL: {source_path}")

        try:
            # Extract (lazy)
            raw = self.extract(source_path)
            # Transform (lazy)
            transformed = self.transform(raw)
            # Collect and load
            result_df = transformed.collect()
            return self.load(result_df)
        except Exception as e:
            logger.error(f"ETL failed: {e}", exc_info=True)
            raise


# Usage
pipeline = ETLPipeline({
    "raw_path": "data/raw",
    "processed_path": "data/processed",
    "duckdb_path": "analytics.db"
})
pipeline.run("data/input.parquet")
```

### Key Principles

1. **Lazy evaluation**: Use `scan_*` and chain operations before `collect()`
2. **Context managers**: Manage DuckDB connections with `with` statements
3. **Type hints**: Document function signatures for clarity
4. **Structured logging**: Include contextual information (source, row counts)
5. **Error handling**: Catch exceptions at pipeline boundary, log with `exc_info=True`

---

## Incremental Loading

### Why Incremental?

- **Efficiency**: Process only changed data, not full dataset
- **Latency**: Faster pipeline runs (hours → minutes)
- **Cost**: Less compute and storage I/O
- **Scalability**: Handle growing datasets without linear time growth

### Pattern 1: Timestamp Watermark

Track the last processed timestamp and fetch only newer records.

```python
from datetime import datetime
from contextlib import contextmanager


@contextmanager
def get_connection(db_path: str = "etl.db"):
    """Context manager for DuckDB connections."""
    con = duckdb.connect(db_path)
    try:
        yield con
    finally:
        con.close()


def get_last_watermark(con, table_name: str, timestamp_col: str = "updated_at") -> datetime:
    """Get max timestamp from target table."""
    result = con.sql(f"SELECT MAX({timestamp_col}) FROM {table_name}").fetchone()
    return result[0] if result[0] else datetime(1900, 1, 1)


def incremental_load(source_path: str, target_table: str):
    """Incremental load from Parquet file using timestamp watermark."""
    with get_connection() as con:
        watermark = get_last_watermark(con, target_table)

        # Parameterized query prevents SQL injection
        query = """
            SELECT * FROM read_parquet(?)
            WHERE updated_at > ?
        """
        new_data = con.sql(query, [source_path, watermark]).pl()

        if len(new_data) > 0:
            # Append to target
            con.sql(f"INSERT INTO {target_table} SELECT * FROM new_data")
            
            # Update watermark
            new_max = new_data["updated_at"].max()
            con.sql("""
                INSERT OR REPLACE INTO pipeline_checkpoints 
                VALUES (?, ?)
            """, [target_table, new_max])
            
            return len(new_data)
        return 0
```

**Pros**: Simple, works for append-only data
**Cons**: Misses updates to old records; relies on accurate timestamps

### Pattern 2: Version/Sequence Number

For databases with version columns or incrementing IDs:

```python
def incremental_by_version(con, source_table: str, target_table: str, version_col: str = "version"):
    """Track last processed version number."""
    last_version = con.sql(f"""
        SELECT MAX({version_col}) FROM {target_table}
    """).fetchone()[0] or 0

    con.sql(f"""
        INSERT INTO {target_table}
        SELECT * FROM {source_table}
        WHERE {version_col} > {last_version}
    """)
```

**Pros**: Guarantees no gaps; handles updates if versions increase on update
**Cons**: Requires monotonic version column

### Pattern 3: Merge/Upsert Pattern

Combine new data with existing using key matching:

```python
def upsert_data(con, source_df, target_table: str, key_columns: list):
    """
    Merge source data into target table using MERGE semantics.
    Requires DuckDB v0.8+ or Spark Delta.
    """
    # Materialize source to staging
    con.sql("CREATE OR REPLACE TABLE staging AS SELECT * FROM source_df")

    # Build merge condition from key columns
    merge_cond = " AND ".join(f"target.{k} = source.{k}" for k in key_columns)

    con.sql(f"""
        MERGE INTO {target_table} AS target
        USING staging AS source
        ON {merge_cond}
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
```

**Pros**: Handles updates and inserts; idempotent
**Cons**: Requires database/engine that supports MERGE

### Idempotent Design

Ensure pipeline can be safely re-run:

```python
def idempotent_incremental(con, source_path: str, target_table: str, merge_keys: list):
    """
    Idempotent incremental: re-running processes same data without duplicates.
    """
    # Read source, deduplicate by merge keys keeping latest
    key_str = ", ".join(merge_keys)
    source = con.sql(f"""
        SELECT DISTINCT ON ({key_str}) *
        FROM read_parquet(?)
        ORDER BY {key_str}, updated_at DESC
    """, [source_path])

    # Use staging and MERGE for idempotency
    con.sql("CREATE OR REPLACE TABLE staging AS SELECT * FROM source")
    
    merge_cond = " AND ".join(f"target.{k} = source.{k}" for k in merge_keys)
    con.sql(f"""
        MERGE INTO {target_table} AS target
        USING staging AS source
        ON {merge_cond}
        WHEN MATCHED THEN UPDATE SET *
        WHEN NOT MATCHED THEN INSERT *
    """)
```

### Anti-Patterns

- **Using row count as watermark** — Counts change non-monotonically
- **No deduplication** — Duplicate processing on retries leads to data duplication
- **Missing transaction boundaries** — Partial loads on failure cause data loss
- **No backfill capability** — Can't re-process specific date range
- **Relying on file modification times** — Not reliable across systems

---

## Resilience Patterns

### Retry Pattern

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import requests.exceptions


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((IOError, requests.exceptions.ConnectionError))
)
def reliable_extract(source: str) -> pl.DataFrame:
    """Extract with automatic retry for transient errors."""
    logger.info(f"Extracting from {source}")
    return pl.read_parquet(source)
```

### Circuit Breaker

```python
import time
from enum import Enum


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Prevent cascading failures with circuit breaker pattern."""
    
    def __init__(self, threshold: int = 5, timeout: int = 60):
        self.threshold = threshold
        self.timeout = timeout
        self.failures = 0
        self.last_failure_time = 0
        self.state = CircuitState.CLOSED

    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError("Circuit breaker is OPEN - fast failing")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failures = max(0, self.failures - 1)
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()
        if self.failures >= self.threshold:
            self.state = CircuitState.OPEN
```

### Schema Validation

```python
def validate_schema(df: pl.DataFrame, expected_schema: dict[str, pl.DataType]) -> bool:
    """
    Validate DataFrame matches expected schema.
    
    Args:
        df: Polars DataFrame
        expected_schema: Mapping of column name to Polars data type
        
    Raises:
        ValueError: If column missing
        TypeError: If column has wrong type
    """
    for col, dtype in expected_schema.items():
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
        if df[col].dtype != dtype:
            raise TypeError(
                f"Column '{col}' has wrong type: {df[col].dtype} != {dtype}"
            )
    return True
```

---

## Testing Patterns

### Unit Tests for Transformations

```python
import pytest


def test_transform_filters_by_date():
    """Test that transformation filters old data."""
    from datetime import date
    
    input_df = pl.DataFrame({
        "date": [date(2023, 12, 1), date(2024, 1, 1), date(2024, 2, 1)],
        "value": [100, 200, 300]
    })
    
    # Apply transformation
    result = transform(input_df.lazy()).collect()
    
    assert len(result) == 2  # Only 2024+ dates
    assert result["value"].sum() == 500
```

### Integration Tests with Temporary Storage

```python
import tempfile
import shutil


def test_full_pipeline():
    """Test end-to-end pipeline with temporary storage."""
    tmpdir = tempfile.mkdtemp()
    try:
        # Write test data
        test_data = pl.DataFrame({
            "id": [1, 2, 3],
            "value": [100, 200, 300]
        })
        test_path = f"{tmpdir}/input.parquet"
        test_data.write_parquet(test_path)
        
        # Run pipeline
        result = run_pipeline(test_path, "test_output")
        
        # Validate
        assert result["rows_processed"] == 3
    finally:
        shutil.rmtree(tmpdir)
```

---

## References

- `production-architecture.md` — Medallion architecture, partitioning, lifecycle management
- `crud-operations.md` — Append, overwrite, merge patterns across tools
- `../templates/complete_etl_pipeline.py` — Production-ready template with logging
- [Polars Documentation](https://pola.rs/)
- [DuckDB Documentation](https://duckdb.org/docs/)
- [Tenacity Retry Library](https://tenacity.readthedocs.io/)
