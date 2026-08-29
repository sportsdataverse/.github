---
name: sdv-assuring-data-pipelines
description: "Data quality validation and observability for data pipelines. Combines Great Expectations and Pandera for data validation with OpenTelemetry and Prometheus for monitoring and alerting."
dependsOn: ["@sdv-building-data-pipelines"]
---

# Assuring Data Pipelines

Data quality validation and observability for production data pipelines. Ensure data correctness with validation frameworks and gain visibility into pipeline performance with tracing and metrics.

## Two Pillars of Pipeline Assurance

| Concern | Tools | Purpose |
|---------|-------|---------|
| **Data Quality** | Great Expectations, Pandera | Validate schema, distributions, business rules |
| **Observability** | OpenTelemetry, Prometheus | Trace execution, monitor health, alert on issues |

## Why Both Matter

- **Quality without observability**: You know data is wrong, but can't trace where it broke
- **Observability without quality**: You see pipeline latency, but miss silent data corruption
- **Together**: Complete feedback loop from detection → diagnosis → remediation

## Quick Comparison: Validation Tools

| Feature | Great Expectations | Pandera |
|---------|-------------------|---------|
| **Approach** | Declarative "expectations" | Schema definitions with checks |
| **DataFrame Support** | Pandas, Spark, SQL, BigQuery | Pandas, Polars, PySpark, Dask |
| **Validation Output** | JSON results with detailed diagnostics | Boolean or exception |
| **Best For** | Enterprise data platforms, comprehensive profiling | Python-centric pipelines, lightweight |
| **Learning Curve** | Steeper (DataContext, Checkpoints) | Lower (Python decorators/classes) |

## When to Use Which?

**Great Expectations**: You need comprehensive data documentation, profiling, and validation with rich reporting. Organizations with dedicated data quality teams.

**Pandera**: You're already in Python/Pandas/Polars ecosystem and want simple schema validation with type hints. Quick checks in ETL scripts or API responses.

## Skill Dependencies

- `@sdv-building-data-pipelines` - Polars, DuckDB, Pandas basics
- `@orchestrating-data-pipelines` (external skill, not bundled in sdv-toolkit) - Integrate validation into workflows

---

## Great Expectations (GX)

### Installation
```bash
pip install great_expectations
# For specific backends
pip install "great_expectations[spark]"
```

### Quickstart
```python
import great_expectations as gx
import pandas as pd

# Initialize context (creates gx/ directory if first time)
context = gx.get_context()

# Create expectation suite
context.create_expectation_suite("my_suite")

# Get validator
validator = context.get_validator(
    batch_request={
        "datasource_name": "pandas",
        "data_asset_name": "my_data",
    },
    expectation_suite_name="my_suite"
)

# Define expectations
validator.expect_column_values_to_not_be_null("id")
validator.expect_column_values_to_be_between("value", min_value=0, max_value=1000)
validator.expect_column_values_to_be_in_set("category", value_set=["A", "B", "C"])
validator.expect_column_values_to_match_strftime_format("date", strftime_format="%Y-%m-%d")

# Validate
result = validator.validate()
print(f"Success: {result.success}")
if not result.success:
    print(f"Failed expectations: {result.results}")
```

### Data Sources & Connectors
```yaml
# gx/contexts/<context>/datasources/pandas_datasource.yml
datasources:
  pandas_datasource:
    class_name: Datasource
    module_name: great_expectations.datasource
    execution_engine:
      module_name: great_expectations.execution_engine
      class_name: PandasExecutionEngine
    data_connectors:
      default_runtime_data_connector_name:
        class_name: RuntimeDataConnector
        batch_identifiers:
          - runtime_batch_identifier_name
```

### Checkpoints (Validation Automation)
```python
# Create checkpoint
checkpoint_config = {
    "name": "my_checkpoint",
    "config_version": 1.0,
    "class_name": "SimpleCheckpoint",
    "validations": [
        {
            "batch_request": {
                "datasource_name": "pandas",
                "data_connector_name": "default_runtime_data_connector_name",
                "data_asset_name": "my_data",
            },
            "expectation_suite_name": "my_suite"
        }
    ]
}

context.add_checkpoint(**checkpoint_config)

# Run checkpoint
results = context.run_checkpoint(checkpoint_name="my_checkpoint")
```

### Integration with Orchestrators

**Prefect**:
```python
from prefect import flow, task
import great_expectations as gx

@task
def validate_data(df: pd.DataFrame, suite_name: str) -> bool:
    context = gx.get_context()
    validator = context.get_validator(
        batch_request={
            "datasource_name": "pandas",
            "data_asset_name": "validation_data"
        },
        expectation_suite_name=suite_name
    )
    validator.add_batch(df, batch_identifier="batch_1")
    result = validator.validate()
    return result.success

@flow
def pipeline_with_validation():
    df = extract()
    if validate_data(df, "my_suite"):
        transformed = transform(df)
        load(transformed)
    else:
        raise ValueError("Data validation failed")
```

**Dagster**:
```python
from dagster import asset
import great_expectations as gx

@asset
def validated_asset(df: pd.DataFrame) -> pd.DataFrame:
    context = gx.get_context()
    validator = context.add_or_edit_expectation_suite("asset_suite")
    # ... define expectations

    validator.add_batch(df)
    result = validator.validate()
    if not result.success:
        raise Exception(f"Validation failed: {result}")
    return df
```

---

## Pandera: Lightweight Schema Validation

### Installation
```bash
pip install pandera[pandas]     # For pandas
pip install pandera[polars]     # For Polars
pip install pandera[pyspark]    # For PySpark
```

### Basic Usage
```python
import pandera as pa
import pandas as pd

# Define schema
schema = pa.DataFrameSchema({
    "id": pa.Column(pa.Int, checks=pa.Check.gt(0)),
    "category": pa.Column(pa.String, checks=pa.Check.isin(["A", "B", "C"])),
    "value": pa.Column(pa.Float, checks=[
        pa.Check.gt(0),
        pa.Check.lt(10000)
    ]),
    "date": pa.Column(pa.DateTime)
})

# Validate DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "category": ["A", "B", "A"],
    "value": [100.0, 200.0, 150.0],
    "date": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"])
})

validated = schema.validate(df)  # Raises SchemaError if invalid
print("Validation passed!")

# Decorator pattern
@schema.validate
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category")["value"].sum().reset_index()
```

### Custom Checks
```python
# Custom validation function
def custom_check(series: pd.Series) -> bool:
    return (series > 0).all()

schema = pa.DataFrameSchema({
    "value": pa.Column(pa.Float, checks=custom_check)
})

# Or lambda
schema = pa.DataFrameSchema({
    "value": pa.Column(pa.Float, checks=pa.Check(lambda x: x > 0))
})
```

### Polars Integration
```python
import pandera.polars as pa
import polars as pl

schema = pa.DataFrameSchema({
    "id": pa.Column(pl.Int64, pa.Check.gt(0)),
    "value": pa.Column(pa.Float64, pa.Check.in_range(0, 1000))
})

df = pl.DataFrame({"id": [1, 2], "value": [100.0, 200.0]})
validated = schema.validate(df)
```

---

## OpenTelemetry Integration

OpenTelemetry (OTel) provides a vendor-neutral standard for distributed tracing, metrics, and logs.

### Installation
```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### Basic Tracing
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
import logging

# Setup tracer provider
provider = TracerProvider()
exporter = OTLPSpanExporter(endpoint="http://localhost:4317")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("data_pipeline")

def run_pipeline():
    with tracer.start_as_current_span("extract") as span:
        span.set_attribute("source", "sales.parquet")
        span.set_attribute("format", "parquet")
        df = pl.scan_parquet("data/sales.parquet").collect()
        span.set_attribute("rows_read", len(df))

    with tracer.start_as_current_span("transform") as span:
        span.set_attribute("operation", "aggregation")
        result = df.group_by("category").agg(pl.col("value").sum())

    with tracer.start_as_current_span("load") as span:
        span.set_attribute("target", "duckdb.summary")
        result.to_pandas().to_sql("summary", conn, if_exists="replace")
        span.set_attribute("rows_written", len(result))

if __name__ == "__main__":
    run_pipeline()
```

### Trace Context Propagation

For multi-service pipelines, pass trace context:

```python
from opentelemetry import propagators
from opentelemetry.propagators.b3 import B3Format

# Inject trace context into message headers (Kafka, HTTP)
carrier = {}
propagator = B3Format()
propagator.inject(carrier, context=trace.get_current_span().get_context())

# Send carrier dict with message (e.g., Kafka header)
producer.produce(
    topic="events",
    key=key,
    value=json.dumps(data),
    headers=list(carrier.items())
)

# Consumer extracts context
context = propagator.extract(carrier=carrier)
with tracer.start_as_current_span("process_message", context=context):
    process(data)
```

---

## Prometheus Metrics

Prometheus collects numeric time series data. Push or pull metrics from your application.

### Installation
```bash
pip install prometheus-client
```

### Basic Instrumentation
```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Define metrics
ROWS_PROCESSED = Counter(
    'etl_rows_processed_total',
    'Total rows processed by ETL',
    ['source', 'stage']
)

PROCESSING_TIME = Histogram(
    'etl_processing_seconds',
    'Time spent processing',
    ['operation'],
    buckets=[0.1, 0.5, 1.0, 5.0, 10.0, 30.0, 60.0]
)

PIPELINE_ERRORS = Counter(
    'etl_errors_total',
    'Total preprocessing errors',
    ['stage', 'error_type']
)

MEMORY_USAGE = Gauge(
    'etl_memory_bytes',
    'Process memory usage in bytes'
)

# Start metrics server (Prometheus scrapes this endpoint)
start_http_server(8000)

def process_batch(stage: str, batch_id: int):
    with PROCESSING_TIME.time(operation=f"batch_{batch_id}"):
        try:
            rows = extract_and_process(batch_id)
            ROWS_PROCESSED.labels(source="kafka", stage=stage).inc(rows)
            return rows
        except Exception as e:
            PIPELINE_ERRORS.labels(stage=stage, error_type=type(e).__name__).inc()
            raise

# Periodic gauge update
import psutil
def update_memory():
    process = psutil.Process()
    MEMORY_USAGE.set(process.memory_info().rss)
```

### Custom Collector
```python
from prometheus_client import CollectorRegistry, Gauge

registry = CollectorRegistry()

# Custom gauge that computes on demand
queue_size = Gauge(
    'kafka_queue_size',
    'Number of messages in queue',
    registry=registry
)

def collect_queue_size():
    size = kafka_consumer.metrics()['fetch-metrics']['records-lag-max']
    queue_size.set(size)

# Register with push gateway or scrape
```

---

## Integration with Orchestration

### Prefect Built-in Observability
Prefect automatically records:
- Task run status (success/failure)
- Duration
- Retry counts
- Parameters

Enable Prefect Cloud/Server for UI:

```bash
prefect cloud login  # or prefect server start
prefect agent start -q 'default'
```

### Dagster Observability
Dagster Dagit UI shows:
- Asset materialization history
- Run duration and status
- Asset lineage graph
- Resource usage

Enable metrics:
```python
from dagster import DagsterMetric

@asset
def monitored_asset():
    # Dagster automatically records metrics
    pass
```

---

## Dashboards & Alerting

### Grafana Dashboard Example

Create dashboard with panels:
- **Throughput**: `rate(etl_rows_processed_total[5m])`
- **Latency**: `histogram_quantile(0.95, etl_processing_seconds_bucket)`
- **Error Rate**: `rate(etl_errors_total[5m])`
- **Memory**: `etl_memory_bytes / 1024 / 1024`

### Alert Rules (Prometheus Alertmanager)

```yaml
groups:
  - name: etl-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(etl_errors_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "ETL error rate elevated"
          description: "{{ $labels.stage }} stage error rate: {{ $value }} errors/sec"
```

---

## Best Practices

### Data Quality
1. ✅ **Validate early** - Check data quality immediately after extraction
2. ✅ **Fail fast** - Stop pipeline on validation failure (or route to quarantine)
3. ✅ **Version your schemas** - Store schema definitions in version control
4. ✅ **Use both static and runtime checks** - Static schema + dynamic checks (ranges, uniqueness)
5. ✅ **Integrate with orchestration** - Use Prefect/Dagster task dependencies for validation steps
6. ❌ **Don't** validate only at the end - catch issues early
7. ❌ **Don't** use `try/except` to ignore validation errors (unless intentional quarantine)

### Observability
1. ✅ **Span every pipeline stage** - extract, transform, load, validate
2. ✅ **Add attributes** - dataset names, row counts, file paths
3. ✅ **Propagate context** across async boundaries (threads, processes, network)
4. ✅ **Record errors** in spans with `span.record_exception()`
5. ✅ **Sample judiciously** - 100% in dev, lower in prod (sampling policy)

### Metrics
1. ✅ **Use counters for events** (rows processed, errors)
2. ✅ **Use histograms for durations** (processing time, latency)
3. ✅ **Use gauges for state** (queue size, memory usage)
4. ✅ **Label dimensions** (stage, source, status) but avoid cardinality explosion
5. ✅ **Export endpoint** on separate port (8000) outside app port

### Production
1. ✅ **Centralized logs** - send structured logs to ELK/Datadog
2. ✅ **Correlation IDs** - Include trace IDs in log entries
3. ✅ **Alert on SLA breaches** - latency > threshold, error rate > X%
4. ✅ **Test observability** - Simulate failures, verify traces/metrics
5. ✅ **Document schema** - Define metric names and label values in README

---

## Testing Patterns

### pytest Integration
```python
import pytest
import pandas as pd
import pandera as pa

schema = pa.DataFrameSchema({
    "id": pa.Column(pa.Int, pa.Check.gt(0)),
    "value": pa.Column(pa.Float)
})

def test_transformation_output():
    df = transform_function(source_df)
    schema.validate(df)  # Will raise if invalid

@pytest.fixture
def sample_data():
    return pd.DataFrame({"id": [1, 2], "value": [10.0, 20.0]})

def test_pipeline(sample_data):
    result = pipeline.run(sample_data)
    assert len(result) > 0
```

---

## Integrated Quality Validation Workflow

Combine validation and observability for a complete feedback loop:

```python
from opentelemetry import trace
from prometheus_client import Counter, Histogram
import pandera as pa

# Metrics
VALIDATION_ERRORS = Counter('validation_errors_total', 'Validation failures', ['check_type'])
ROWS_VALIDATED = Counter('rows_validated_total', 'Rows passing validation')

# Tracing
tracer = trace.get_tracer("quality_pipeline")

# Schema
schema = pa.DataFrameSchema({
    "id": pa.Column(pa.Int, pa.Check.gt(0)),
    "value": pa.Column(pa.Float, pa.Check.in_range(0, 1000))
})

def quality_assured_pipeline(df):
    with tracer.start_as_current_span("validate_and_process") as span:
        span.set_attribute("input_rows", len(df))
        
        # Validation
        try:
            validated = schema.validate(df)
            ROWS_VALIDATED.inc(len(validated))
            span.set_attribute("validation_passed", True)
        except pa.errors.SchemaError as e:
            VALIDATION_ERRORS.labels(check_type="schema").inc()
            span.record_exception(e)
            span.set_attribute("validation_passed", False)
            raise
        
        # Processing
        result = validated.groupby("category").agg({"value": "sum"})
        span.set_attribute("output_rows", len(result))
        
        return result
```

---

## References

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Pandera Documentation](https://pandera.pydata.org/)
- [pandera-polars](https://pandera.pydata.org/pandera-polars-docs/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/instrumentation/python/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Grafana Dashboarding](https://grafana.com/docs/grafana/latest/dashboards/)
- `@sdv-building-data-pipelines` - Pipeline patterns with validation
- `@orchestrating-data-pipelines` (external skill, not bundled in sdv-toolkit) - Prefect/Dagster observability features

## Applying this to model inputs, not just published datasets

Everything above validates **published datasets**. The same machinery belongs on
**feature sets and the frame handed to `.fit()`**, which is where the failures
originate: a join that silently matched 60% of rows, a season that read zero rows
and reported success, an id that stringified as `"123.0"`.

`sdv-modeling`'s `references/tracking.md` §6 defines where those contracts attach
(the `contracts:` block of a feature-set definition) and names two SDV-specific
expectations worth writing once: `expect_column_pair_dtypes_to_match` before a
join, and `expect_season_coverage_to_be_complete` so a row count of zero is an
error rather than a state.
