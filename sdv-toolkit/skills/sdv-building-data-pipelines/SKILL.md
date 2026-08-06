---
name: sdv-building-data-pipelines
description: "Build production batch data pipelines with Polars, DuckDB, and PyArrow. Covers ETL patterns, medallion architecture, partitioning, and CRUD operations. Use when designing or implementing data ingestion, transformation, and loading workflows in Python."
---

# Building Data Pipelines

Build robust, efficient batch data pipelines in Python. This skill covers the complete pipeline lifecycle: extracting data from sources, transforming with DataFrames or SQL, loading to destinations, and operating with production standards.

## When to use this skill

Use this skill when:
- Building ETL/ELT pipelines in Python
- Choosing between Polars, DuckDB, PyArrow, or SQL for data processing
- Designing data layer architecture (Bronze/Silver/Gold)
- Implementing incremental loading with watermarks or CDC
- Deciding on append vs overwrite vs merge semantics
- Setting up partitioning and file sizing strategies
- Validating data quality at pipeline boundaries

## When not to use this skill

Use other skills for:
- **Cloud storage authentication and access** → `accessing-cloud-storage`
- **Lakehouse table formats (Delta/Iceberg)** → `@designing-data-storage` (external skill, not bundled in sdv-toolkit)
- **Workflow orchestration (Prefect/Dagster)** → `orchestrating-data-pipelines`
- **Streaming data (Kafka/MQTT)** → `building-streaming-pipelines`
- **Data quality frameworks** → `sdv-assuring-data-pipelines`
- **AI/ML pipelines (embeddings/vectors)** → `engineering-ai-pipelines`

---

## Quick tool selection

| Task | Default choice | When to consider alternatives |
|------|---------------|------------------------------|
| DataFrame transformations | **Polars** | Use DuckDB for heavy SQL/windowing; PyArrow for interchange only |
| SQL analytics over files | **DuckDB** | Use Polars for complex expression chains; PostgreSQL for OLTP sources |
| Data interchange between systems | **PyArrow** | Use Parquet files for persistence; Arrow IPC for streaming |
| Incremental/upsert operations | **DuckDB MERGE** | Use Delta Lake for ACID guarantees; Iceberg for catalog integration |
| Production ETL structure | **Polars + DuckDB** | Add orchestrator (Prefect/Dagster) for scheduling and retries |

**Decision rule**: Start with Polars lazy for transformations. Use DuckDB when SQL is clearer or when joining multiple sources. Keep boundaries in Arrow/Parquet format.

---

## Core workflow

### 1. Design the pipeline

Answer these questions before writing code:

1. **Data contract**: What columns and types are required? What are the key constraints?
2. **Layer semantics**: Bronze (raw/immutable), Silver (validated), or Gold (aggregated)?
3. **Write mode**: Append, partition overwrite, or merge/upsert?
4. **Partitioning**: Which columns will be filtered most often? (typically date + low-cardinality dimensions)
5. **Incremental logic**: Watermark column? CDC source? Full reload capability?
6. **Schema evolution**: Additive-only policy? Type widening allowed?

### 2. Implement with lazy evaluation

```python
import polars as pl
import duckdb
from datetime import datetime

def run_pipeline(source_path: str, target_table: str):
    # Extract: lazy scan with predicate pushdown
    lazy_df = (
        pl.scan_parquet(source_path)
        .filter(pl.col("event_date") >= datetime(2024, 1, 1))
        .select(["id", "event_date", "category", "amount"])
    )
    
    # Transform: chain operations, still lazy
    transformed = (
        lazy_df
        .with_columns(pl.col("category").str.to_lowercase())
        .filter(pl.col("amount").is_not_null())
    )
    
    # Load: materialize and write
    df = transformed.collect()
    
    with duckdb.connect("analytics.db") as con:
        con.sql(f"CREATE OR REPLACE TABLE staging AS SELECT * FROM df")
        con.sql(f"""
            MERGE INTO {target_table} AS target
            USING staging AS source
            ON target.id = source.id
            WHEN MATCHED THEN UPDATE SET *
            WHEN NOT MATCHED THEN INSERT *
        """)
    
    return {"rows_processed": len(df), "target": target_table}
```

### 3. Validate and operate

- **Schema validation**: Check required columns and types before loading
- **Row count logging**: Track rows in/out at each stage
- **Checkpoint persistence**: Store watermark timestamps for incremental runs
- **Idempotency**: Ensure re-runs produce the same result (no duplicates)

---

## Production standards

### File sizing
- Target **256MB–1GB** per Parquet file
- Too small → metadata overhead, slow listing
- Too large → poor parallelism, memory pressure

### Partitioning
- **Good keys**: date, region, category (low-moderate cardinality, frequently filtered)
- **Avoid**: user_id, transaction_id (high cardinality), timestamps with milliseconds

### Write semantics

| Operation | Use when | Implementation |
|-----------|----------|----------------|
| **Append** | Strictly new immutable events | `INSERT INTO` or `write_delta(mode="append")` |
| **Partition overwrite** | Reprocessing a date slice deterministically | `write_delta(mode="overwrite", partition_filters=...)` |
| **Merge/Upsert** | Corrections, late updates, de-duplication | `MERGE INTO` (DuckDB) or `write_delta(mode="merge")` |

### Schema evolution policy
- **Default**: Additive changes only (new nullable columns)
- **Caution**: Type widening only when compatibility is clear
- **Never**: Destructive rename/drop in-place for shared production tables

---

## Progressive disclosure

Start here based on your need:

- **Building a complete ETL pipeline** → `references/pipeline-patterns.md`
- **Designing production architecture** → `references/production-architecture.md`
- **Implementing CRUD operations** → `references/crud-operations.md`
- **Production template with logging** → `templates/complete_etl_pipeline.py`

---

## Related skills

- `accessing-cloud-storage` — Cloud storage authentication and remote file access
- `@designing-data-storage` (external skill, not bundled in sdv-toolkit) — Lakehouse formats (Delta Lake, Iceberg), file formats, storage design
- `orchestrating-data-pipelines` — Prefect, Dagster, dbt for workflow scheduling
- `sdv-assuring-data-pipelines` — Data quality testing and observability
- `building-streaming-pipelines` — Kafka, MQTT, NATS for real-time data
- `engineering-ai-pipelines` — Embeddings, vector databases, RAG patterns

---

## Migration notes

This skill replaces and consolidates:
- `data-engineering-core` — Core library patterns and ETL workflows
- `data-engineering-best-practices` — Production architecture and standards

Content has been reorganized into workflow-focused references with direct file paths.
