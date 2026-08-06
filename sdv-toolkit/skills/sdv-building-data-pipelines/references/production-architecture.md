# Production Architecture

Design production-grade data pipelines with proper layering, partitioning, file sizing, and lifecycle management. Covers medallion architecture, storage layout, and cost optimization.

## Table of Contents

1. [Medallion Architecture](#medallion-architecture)
2. [Partitioning Strategies](#partitioning-strategies)
3. [File Sizing](#file-sizing)
4. [Dataset Lifecycle](#dataset-lifecycle)
5. [Cost Optimization](#cost-optimization)

---

## Medallion Architecture

### Overview

The medallion architecture organizes data into quality tiers:

```
[Source Systems]
        ↓
   ┌──────────┐
   │  Bronze  │  (raw, immutable, full fidelity)
   └─────┬────┘
         │ cleansing, validation, standardization
         ↓
   ┌──────────┐
   │  Silver  │  (clean, reliable, conformed dimensions)
   └─────┬────┘
         │ aggregation, business logic
         ↓
   ┌──────────┐
   │  Gold    │  (optimized for specific use cases)
   └──────────┘
```

### Bronze Layer (Raw)

**Characteristics**:
- Store as append-only (never update raw data)
- Keep original schema; add ingestion metadata
- Format: Parquet or Delta Lake (if ACID needed)
- Partition by: ingestion date or event date

**Implementation**:

```python
# Polars: Append to Bronze
import polars as pl

bronze_df = pl.DataFrame({
    "raw_data": json_payloads,
    "_ingestion_timestamp": datetime.utcnow(),
    "_source_file": source_path
})

bronze_df.write_parquet(
    "s3://lakehouse/bronze/events/",
    use_pyarrow=True,
    pyarrow_options={"partition_cols": ["_ingestion_date"]}
)
```

**Rules**:
- Never modify or delete Bronze data
- Keep full fidelity (don't drop columns)
- Add metadata columns for lineage

### Silver Layer (Validated)

**Characteristics**:
- Apply data quality checks (nulls, duplicates, referential integrity)
- Standardize data types (normalize dates, currencies)
- Denormalize dimension keys (snowflake → star schema)
- Format: Delta Lake or Iceberg for ACID guarantees

**Implementation**:

```python
import pyarrow.dataset as ds

# Write Silver Parquet with partitioning
ds.write_dataset(
    silver_table,
    "s3://lakehouse/silver/orders/",
    format="parquet",
    partitioning=ds.partitioning(
        ["order_date_year", "order_date_month"],
        flavor="hive"
    )
)
```

**Rules**:
- Validate all records (fail or quarantine invalid)
- Standardize formats (dates, currencies, codes)
- Handle slowly changing dimensions (SCD Type 2 if needed)

### Gold Layer (Curated)

**Characteristics**:
- Pre-aggregated tables (daily sales by region, ML features)
- Optimized for specific queries (materialized views)
- Format: Parquet (read-heavy) or materialized views in DuckDB

**Implementation**:

```python
import duckdb

# Materialized Gold view in DuckDB
con = duckdb.connect("analytics.db")
con.execute("""
    CREATE OR REPLACE VIEW gold_daily_sales AS
    SELECT
        order_date,
        region,
        SUM(amount) AS total_sales,
        COUNT(*) AS order_count
    FROM silver_orders
    GROUP BY 1, 2
""")

# Export to Parquet
con.execute("""
    COPY gold_daily_sales 
    TO 's3://lakehouse/gold/daily_sales.parquet' 
    (FORMAT PARQUET)
""")
```

**Rules**:
- Optimize for query patterns (column selection, sorting)
- Pre-compute common aggregations
- Document business logic clearly

---

## Partitioning Strategies

### Choosing Partition Keys

**Good partition keys**:
- Frequently filtered dimensions (date, region, category)
- Low to moderate cardinality (< 10,000 distinct values)
- Stable values (don't partition by timestamp with milliseconds)

**Avoid**:
- High-cardinality keys (user_id, transaction_id)
- Over-partitioning creating tiny files (< 10MB)
- Columns with high skew (99% of data in one partition)

### Single-Column Partitioning

```python
# Polars: write partitioned data
df.write_parquet(
    "s3://lakehouse/silver/transactions/",
    use_pyarrow=True,
    pyarrow_options={"partition_cols": ["transaction_date"]}
)
```

### Multi-Column Partitioning

Hierarchical directories: `year=2024/month=01/region=US/`

```python
import pyarrow.dataset as ds
import pyarrow as pa

partitioning = ds.partitioning(
    schema=pa.schema([
        ("year", pa.int16()),
        ("month", pa.int8()),
        ("region", pa.string())
    ]),
    flavor="hive"
)

ds.write_dataset(
    table,
    "s3://lakehouse/silver/orders/",
    format="parquet",
    partitioning=partitioning
)
```

### Partition Pruning

Query only needed partitions:

```python
# Polars lazy scan with predicate on partition columns
lazy_df = pl.scan_parquet("s3://lakehouse/silver/orders/")
filtered = (
    lazy_df
    .filter(pl.col("year") == 2024)
    .filter(pl.col("month") == 1)
    .filter(pl.col("region") == "US")
    .collect()
)
# Only reads files under year=2024/month=01/region=US/
```

---

## File Sizing

### Optimal File Size

**Target: 256MB – 1GB per file** (workload-dependent)

| Size | Impact |
|------|--------|
| Too small (< 128MB) | Metadata overhead, slow listing, many file handles |
| Optimal (256MB - 1GB) | Good balance of parallelism and efficiency |
| Too large (> 2GB) | Poor parallelism, memory pressure, skewed processing |

### Calculating Row Count

Estimate rows per GB based on row size:

```
rows_per_gb ≈ 1_000_000_000 bytes / row_size_in_bytes
```

Example with 500 bytes per row:
```python
rows_per_gb = 1_000_000_000 / 500  # ≈ 2,000,000 rows/GB
```

### Controlling File Size

**PyArrow**:
```python
ds.write_dataset(
    table,
    "output/",
    format="parquet",
    max_rows_per_file=1_000_000,  # ~1GB for 500 byte rows
    partitioning=partitioning
)
```

**Polars** (limited control, relies on row groups):
```python
df.write_parquet(
    "output.parquet",
    row_group_size=100_000  # Controls Parquet row group size
)
```

### Compaction

Periodically rewrite small files into larger ones:

```python
def compact_partition(partition_path: str, target_size_mb: int = 256):
    """Rewrite small files in a partition to optimal size."""
    import pyarrow.fs as fs
    
    s3 = fs.S3FileSystem()
    files = s3.get_file_info(fs.FileSelector(partition_path, recursive=True))
    
    # Filter small files
    small_files = [f for f in files if f.size < 10_000_000]  # < 10MB
    
    if len(small_files) > 10:  # Threshold for compaction
        # Read all small files
        tables = [pq.read_table(f.path) for f in small_files]
        combined = pa.concat_tables(tables)
        
        # Delete old files
        for f in small_files:
            s3.delete_file(f.path)
        
        # Write with optimal row count
        rows_per_file = int((target_size_mb * 1_000_000) / estimated_row_size)
        ds.write_dataset(
            combined,
            partition_path,
            format="parquet",
            max_rows_per_file=rows_per_file
        )
```

---

## Dataset Lifecycle

### Stages

| Stage | Description | Retention | Format |
|-------|-------------|-----------|--------|
| **Raw/Staging** | Ingested data, minimal processing | 7-30 days | Parquet/CSV/JSON |
| **Bronze** | Immutable raw data | 30-90 days (then archive) | Parquet/Delta |
| **Silver** | Validated, cleaned | Indefinite (versioned) | Delta/Iceberg |
| **Gold** | Aggregated, business-ready | Indefinite | Parquet/DuckDB views |
| **Archive** | Historical, rarely accessed | Long-term (cold storage) | Parquet (compressed) |

### Metadata Tracking

Maintain a data catalog table:

```sql
CREATE TABLE dataset_catalog (
    dataset_name VARCHAR PRIMARY KEY,
    layer VARCHAR,           -- bronze/silver/gold
    format VARCHAR,          -- parquet/delta/iceberg
    location VARCHAR,
    schema JSON,             -- column names and types
    owner VARCHAR,
    created_at TIMESTAMP,
    last_updated TIMESTAMP,
    retention_days INTEGER,
    pii_level VARCHAR        -- high/medium/low
);
```

### Data Retention Implementation

```python
import boto3
from datetime import datetime, timedelta


def apply_retention_policy(bucket: str, prefix: str, retention_days: int):
    """Move or delete data older than retention period."""
    s3 = boto3.client('s3')
    cutoff = datetime.now() - timedelta(days=retention_days)
    
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get('Contents', []):
            if obj['LastModified'].replace(tzinfo=None) < cutoff:
                # Move to archive or delete
                archive_key = obj['Key'].replace(prefix, f"archive/{prefix}")
                s3.copy_object(
                    Bucket=bucket,
                    CopySource={'Bucket': bucket, 'Key': obj['Key']},
                    Key=archive_key,
                    StorageClass='GLACIER'
                )
                s3.delete_object(Bucket=bucket, Key=obj['Key'])
```

---

## Cost Optimization

### Storage Tiering

| Access Frequency | Storage Class | Use Case |
|------------------|---------------|----------|
| Hot (daily) | S3 Standard / GCS Standard | Bronze, Silver, recent Gold |
| Warm (weekly) | S3 IA / GCS Nearline | Gold older than 1 month |
| Cold (rare) | S3 Glacier / GCS Archive | Bronze archive, compliance |

### Lifecycle Policy (AWS S3)

```json
{
  "Rules": [{
    "ID": "Bronze Archive Policy",
    "Status": "Enabled",
    "Filter": {
      "Prefix": "bronze/"
    },
    "Transitions": [
      {
        "Days": 30,
        "StorageClass": "STANDARD_IA"
      },
      {
        "Days": 90,
        "StorageClass": "GLACIER"
      }
    ],
    "Expiration": {
      "Days": 2555
    }
  }]
}
```

### Query Optimization

- **Predicate pushdown**: Filter on partition columns first
- **Column pruning**: Select only needed columns
- **Caching**: Materialize frequently accessed Gold aggregates
- **Compression**: Zstd level 3 for balance of speed and size

### Avoiding Small Files

Monitor file counts:

```python
import pyarrow.fs as fs


def check_file_sizes(bucket_prefix: str, threshold_bytes: int = 10_000_000):
    """Identify partitions with too many small files."""
    s3 = fs.S3FileSystem()
    infos = s3.get_file_info(fs.FileSelector(bucket_prefix, recursive=True))
    
    total_files = len(infos)
    small_files = sum(1 for info in infos if info.size < threshold_bytes)
    avg_size = sum(info.size for info in infos) / len(infos)
    
    print(f"Total files: {total_files}")
    print(f"Small files (< {threshold_bytes/1e6:.1f}MB): {small_files}")
    print(f"Average size: {avg_size/1e6:.1f}MB")
    
    if small_files > total_files * 0.5:
        print("WARNING: Consider compacting small files")
```

---

## Decision Checklist

Before deploying to production:

1. **Data contract**: Required columns and types defined?
2. **Layer semantics**: Bronze immutable? Silver validated? Gold aggregated?
3. **Write mode**: Append, partition overwrite, or merge?
4. **Layout**: Partition keys + target file size set?
5. **Incremental logic**: Watermark/checkpoint strategy defined?
6. **Evolution policy**: Additive-only by default?
7. **Operational controls**: Tests + observability + retention + backfill process?

---

## Anti-Patterns (Reject in Review)

- Full table overwrite for small incremental changes
- No checkpoint/watermark for recurring pipeline
- Unbounded tiny-file generation
- Partitioning by high-cardinality columns
- No backfill plan / no rollback strategy
- Production credentials in code/config

---

## References

- `pipeline-patterns.md` — ETL patterns and incremental loading
- `crud-operations.md` — Append, overwrite, merge patterns
- `@designing-data-storage` (external skill, not bundled in sdv-toolkit) — Delta Lake, Iceberg, and file formats
- `accessing-cloud-storage` — Cloud storage authentication and access
- [Delta Lake Documentation](https://delta.io/)
- [Apache Iceberg Documentation](https://iceberg.apache.org/)
