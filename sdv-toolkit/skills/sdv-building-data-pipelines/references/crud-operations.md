# CRUD Operations

Create, read, update, and delete operations across Polars, DuckDB, PyArrow, and lakehouse formats. Covers append, overwrite, merge/upsert, and schema evolution patterns.

## Table of Contents

1. [Write Semantics Overview](#write-semantics-overview)
2. [Append Operations](#append-operations)
3. [Overwrite Operations](#overwrite-operations)
4. [Merge/Upsert Operations](#mergeupsert-operations)
5. [Schema Evolution](#schema-evolution)
6. [Time Travel and Recovery](#time-travel-and-recovery)

---

## Write Semantics Overview

| Operation | Use When | Guarantees | Tools Supported |
|-----------|----------|------------|-----------------|
| **Append** | Strictly new immutable events | At-least-once delivery | All |
| **Partition Overwrite** | Deterministic reprocessing for date/key slice | Idempotent per partition | Polars, PyArrow, Delta, Iceberg |
| **Merge/Upsert** | Corrections, late updates, de-duplication | Exactly-once per key | DuckDB, Delta, Iceberg |

---

## Append Operations

### Polars to Parquet

```python
import polars as pl

# Read existing, concat, rewrite (Parquet has no native append)
existing = pl.read_parquet("s3://bucket/table/")
combined = pl.concat([existing, new_df])
combined.write_parquet("s3://bucket/table/")
```

### Polars to Delta Lake

```python
# Native append support
df.write_delta("s3://bucket/table", mode="append")
```

### PyArrow to Parquet

```python
import pyarrow.dataset as ds

# No direct append; read existing, concat, rewrite
existing = ds.dataset("s3://bucket/table/").to_table()
combined = pa.concat_tables([existing, new_table])
ds.write_dataset(combined, "s3://bucket/table/", format="parquet")
```

### DuckDB to Parquet/Delta

```python
import duckdb

# Append to Parquet
con.sql("""
    COPY (SELECT * FROM new_data) 
    TO 's3://bucket/table.parquet' 
    (FORMAT PARQUET, APPEND true)
""")

# Append to Delta
con.sql("INSTALL delta; LOAD delta;")
con.sql("INSERT INTO delta_table SELECT * FROM new_data")
```

### PyIceberg Append

```python
from pyiceberg.table import Table

table = catalog.load_table("database.table")
table.append(new_arrow_table)
```

---

## Overwrite Operations

### Full Table Overwrite

#### Polars

```python
# Delta Lake
import polars as pl

df.write_delta("s3://bucket/table", mode="overwrite")

# Parquet (delete directory first)
import shutil
shutil.rmtree("s3://bucket/table")
df.write_parquet("s3://bucket/table/")
```

#### PyArrow

```python
import pyarrow.dataset as ds
import shutil

# Delete and rewrite
shutil.rmtree("s3://bucket/table")
ds.write_dataset(table, "s3://bucket/table/", format="parquet")
```

#### DuckDB

```python
# Overwrite Parquet
con.sql("""
    COPY table 
    TO 's3://bucket/table.parquet' 
    (FORMAT PARQUET, OVERWRITE_OR_IGNORE true)
""")

# Overwrite Delta
con.sql("""
    INSTALL delta; LOAD delta;
    COPY (SELECT * FROM df) 
    TO 's3://bucket/delta_table' 
    (FORMAT DELTA, OVERWRITE_OR_IGNORE true)
""")
```

#### PyIceberg

```python
table.overwrite(new_arrow_table)
```

### Partition Overwrite

Replace specific partitions only:

#### Polars/Delta

```python
df.write_delta(
    "s3://bucket/table",
    mode="overwrite",
    partition_filters=[("year", "=", "2024")]
)
```

#### PyArrow

```python
import pyarrow.fs as fs

# Identify partition paths, replace files in those partitions
partition_path = "s3://bucket/table/year=2024/"
s3 = fs.S3FileSystem()
s3.delete_dir_contents(partition_path)

ds.write_dataset(
    table_filtered,
    partition_path,
    format="parquet"
)
```

#### DuckDB

```python
# Delete specific partition, then insert
con.sql("""
    DELETE FROM target_table 
    WHERE year = 2024
""")
con.sql("""
    INSERT INTO target_table 
    SELECT * FROM source_data 
    WHERE year = 2024
""")
```

---

## Merge/Upsert Operations

### DuckDB MERGE

DuckDB supports SQL MERGE syntax:

```python
import duckdb

con = duckdb.connect()

# Create staging table
con.sql("CREATE OR REPLACE TABLE staging AS SELECT * FROM source_df")

# Execute merge
con.sql("""
    MERGE INTO target_table AS target
    USING staging AS source
    ON target.id = source.id
    WHEN MATCHED THEN UPDATE SET 
        col1 = source.col1,
        col2 = source.col2,
        updated_at = CURRENT_TIMESTAMP
    WHEN NOT MATCHED THEN INSERT (id, col1, col2, updated_at)
        VALUES (source.id, source.col1, source.col2, CURRENT_TIMESTAMP)
""")
```

### Delta Lake Merge

```python
import polars as pl
from deltalake import DeltaTable

# Using Polars
df.write_delta(
    "s3://bucket/table",
    mode="merge",
    delta_merge_options={
        "predicate": "source.id = target.id",
        "source_alias": "source",
        "target_alias": "target"
    }
).when_matched_update_all() \
 .when_not_matched_insert_all() \
 .execute()

# Using deltalake directly
dt = DeltaTable("s3://bucket/table")
dt.merge(
    source=new_df.to_arrow(),
    predicate="target.id = source.id",
    source_alias="source",
    target_alias="target"
).when_matched_update_all() \
 .when_not_matched_insert_all() \
 .execute()
```

### PyIceberg Merge

```python
from pyiceberg.table import Table

table.merge(
    source_table,
    predicate="target.id = source.id"
).when_matched_update_all() \
 .when_not_matched_insert_all() \
 .execute()
```

### Merge with Delete

Handle CDC deletes in the merge:

```python
# For Delta Lake
dt.merge(
    source=cdc_df.to_arrow(),
    predicate="target.id = source.id",
    source_alias="source",
    target_alias="target"
).when_matched_delete(
    predicate="source.op = 'D'"
).when_matched_update_all(
    predicate="source.op = 'U'"
).when_not_matched_insert_all(
    predicate="source.op = 'C'"
).execute()
```

---

## Schema Evolution

### Adding Columns

#### Delta Lake

```python
# Option 1: mergeSchema during write
df.write_delta(
    table_uri,
    mode="append",
    delta_write_options={"schema_mode": "merge"}  # Adds new columns
)

# Option 2: explicit ALTER TABLE
from deltalake import DeltaTable

dt = DeltaTable(table_uri)
dt.alter.add_columns(
    {"new_column": "string", "another_new": "int"}
)
```

#### Iceberg

```python
from pyiceberg.schema import Schema
from pyiceberg.types import StringType, IntegerType

# Add column
table.update_schema() \
    .add_column("new_column", StringType()) \
    .commit()

# Or via Spark SQL:
# ALTER TABLE my_table ADD COLUMN new_column STRING;
```

#### DuckDB (Parquet)

DuckDB reads Parquet with extra columns gracefully (missing values become NULL):

```sql
-- Create view that adds new column
CREATE OR REPLACE VIEW my_view AS
SELECT *, NULL::VARCHAR AS new_column 
FROM read_parquet('data.parquet');
```

### Changing Column Types

#### Delta Lake

```python
# Type widening (int → long, decimal precision increase)
dt.alter.change_column(
    column_name="old_col",
    new_type="long"
)
```

#### Iceberg

```python
# Update type (requires compatible widening)
table.update_schema() \
    .update_column("existing_col", new_type=LongType()) \
    .commit()
```

**Best Practice**: Only widen (int → long, decimal → higher precision). Never narrow without creating new column.

### Dropping Columns

#### Delta Lake

```python
dt.alter.drop_column("obsolete_column")
```

#### Iceberg

```python
table.update_schema() \
    .delete_column("obsolete_column") \
    .commit()
```

**Impact**: Old data still contains column but queries fail if accessed. Use time travel to recover if needed.

### Schema Compatibility Rules

| Change | Delta Lake | Iceberg | DuckDB (Parquet) |
|--------|------------|---------|------------------|
| Add column | ✅ (mergeSchema) | ✅ | ✅ (NULL on read) |
| Drop column | ✅ | ✅ | ❌ (breaks if query uses) |
| Rename column | ✅ | ✅ | ❌ (treats as new) |
| Type widen | ✅ | ✅ | ✅ (if Parquet matches) |
| Type narrow | ❌ | ❌ | ❌ |

**Recommendation**: Never drop/rename columns in production tables. Add new columns instead, deprecate old ones in application code.

---

## Time Travel and Recovery

### Delta Lake Time Travel

```python
from deltalake import DeltaTable

dt = DeltaTable("s3://bucket/table")

# List versions
history = dt.history()  # DataFrame with version, timestamp, operation

# Time travel query
df_v5 = pl.read_delta("s3://bucket/table@v5")  # Version 5
df_time = pl.read_delta("s3://bucket/table@2024-01-01T00:00:00Z")  # By timestamp

# Restore previous version
dt.restore(version=10)
```

### Iceberg Time Travel

```python
# Snapshot history
snapshots = table.snapshots()

# Read previous snapshot
prev_snapshot = snapshots[-2]
table.scan(snapshot_id=prev_snapshot.snapshot_id).to_arrow()

# Spark SQL:
# SELECT * FROM my_table VERSION AS OF 10;
# SELECT * FROM my_table TIMESTAMP AS OF '2024-01-01 00:00:00';
```

### DuckDB (Application-Level)

DuckDB doesn't track versions natively. Implement versioning:

```sql
-- Store each batch with batch_id
CREATE TABLE my_data AS 
SELECT *, 1 AS batch_id 
FROM read_parquet('batch1.parquet');

-- Query specific batch
SELECT * FROM my_data WHERE batch_id = 1;

-- Track batches
CREATE TABLE batch_metadata (
    batch_id INT PRIMARY KEY,
    loaded_at TIMESTAMP,
    source_file VARCHAR,
    row_count INT
);
```

---

## Tool-Specific Quick Reference

### Polars

| Operation | Method |
|-----------|--------|
| Append to Delta | `df.write_delta(path, mode="append")` |
| Overwrite Delta | `df.write_delta(path, mode="overwrite")` |
| Merge Delta | `df.write_delta(path, mode="merge", delta_merge_options=...)` |
| Append Parquet | Read + concat + rewrite |

### DuckDB

| Operation | SQL |
|-----------|-----|
| Append | `INSERT INTO target SELECT * FROM source` |
| Overwrite | `CREATE OR REPLACE TABLE target AS SELECT ...` |
| Merge | `MERGE INTO target USING source ON ...` |
| Export Parquet | `COPY (SELECT ...) TO 'file.parquet'` |

### PyArrow

| Operation | Method |
|-----------|--------|
| Append | Read + concat + rewrite |
| Overwrite | `ds.write_dataset(table, path, format="parquet")` |
| Partitioned write | `ds.write_dataset(table, path, partitioning=...)` |

---

## References

- `pipeline-patterns.md` — ETL and incremental loading patterns
- `production-architecture.md` — Medallion architecture and partitioning
- `@designing-data-storage` (external skill, not bundled in sdv-toolkit) — Delta Lake, Iceberg deep dive
- [Delta Lake Schema Evolution](https://delta.io/blog/2023-02-08-delta-lake-schema-evolution/)
- [Apache Iceberg Evolution](https://iceberg.apache.org/docs/latest/evolution/)
- [DuckDB MERGE INTO](https://duckdb.org/docs/stable/sql/statements/merge_into.html)
- [PyArrow Dataset API](https://arrow.apache.org/docs/python/generated/pyarrow.dataset.Dataset.html)
