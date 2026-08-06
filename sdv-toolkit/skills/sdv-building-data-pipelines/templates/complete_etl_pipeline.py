"""
Complete ETL Pipeline Template

A production-ready template for building ETL pipelines with Polars, DuckDB, and PyArrow.
Features:
- Lazy evaluation for memory efficiency
- Context manager for resource cleanup
- Incremental loading support
- Structured logging with exc_info
- Configuration via JSON
- Watermark tracking
- Type hints and docstrings

Usage:
    with DataPipeline("config.json") as pipeline:
        result = pipeline.run("data/input.parquet")
        print(pipeline.get_summary(7))
"""

import polars as pl
import duckdb
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PipelineError(Exception):
    """Custom exception for pipeline errors."""
    pass


class DataPipeline:
    """
    Production-grade ETL pipeline template.
    
    Args:
        config_path: Path to JSON configuration file
        
    Example config.json:
        {
            "duckdb_path": "analytics.db",
            "raw_path": "data/raw",
            "processed_path": "data/processed"
        }
    """
    
    def __init__(self, config_path: str = "pipeline_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)
        
        self.duckdb_path = self.config["duckdb_path"]
        self._connection: Optional[duckdb.DuckDBPyConnection] = None
        
    def __enter__(self):
        """Context manager entry - opens connection."""
        self._connection = duckdb.connect(self.duckdb_path)
        self._init_duckdb_tables()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection cleanup."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    @property
    def con(self) -> duckdb.DuckDBPyConnection:
        """Get current DuckDB connection (raises if not in context)."""
        if self._connection is None:
            raise PipelineError("Not in context manager. Use 'with DataPipeline() as pipeline:'")
        return self._connection
    
    def _init_duckdb_tables(self):
        """Initialize DuckDB schema if not exists."""
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS raw_events (
                id VARCHAR,
                event_type VARCHAR,
                value DOUBLE,
                timestamp TIMESTAMP,
                metadata VARCHAR
            )
        """)
        
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS daily_summary (
                date DATE,
                event_type VARCHAR,
                total_value DOUBLE,
                event_count BIGINT,
                processed_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS pipeline_checkpoints (
                pipeline_name VARCHAR PRIMARY KEY,
                last_timestamp TIMESTAMP,
                row_count BIGINT
            )
        """)
    
    def extract(self, source: str) -> pl.LazyFrame:
        """
        Extract data from source as LazyFrame.
        
        Supports:
        - Local Parquet files
        - S3 paths (requires credentials configuration)
        - Local CSV files
        
        Args:
            source: Path to data file (.parquet or .csv)
            
        Returns:
            LazyFrame for efficient processing
            
        Raises:
            PipelineError: If source format unsupported
        """
        logger.info(f"Extracting from {source}")
        
        if source.endswith(".csv"):
            return pl.scan_csv(source)
        elif source.endswith(".parquet") or source.startswith("s3://"):
            return pl.scan_parquet(source)
        else:
            raise PipelineError(f"Unsupported source format: {source}")
    
    def transform(self, df: pl.LazyFrame) -> pl.LazyFrame:
        """
        Apply transformations to raw data.
        
        Override this method to customize transformations.
        
        Args:
            df: LazyFrame from extract stage
            
        Returns:
            Transformed LazyFrame
        """
        return (
            df
            .with_columns([
                pl.col("timestamp").str.to_datetime(),
                pl.col("value").fill_null(0)
            ])
            .filter(pl.col("value") > 0)
            .filter(pl.col("timestamp") >= datetime(2024, 1, 1))
        )
    
    def load(self, df: pl.DataFrame) -> Dict[str, Any]:
        """
        Load transformed data to destination.
        
        Args:
            df: Materialized DataFrame to load
            
        Returns:
            Dict with load statistics
        """
        # Insert raw events
        self.con.execute("INSERT INTO raw_events SELECT * FROM df")
        
        # Create daily summary
        summary = (
            df.group_by(
                pl.col("timestamp").dt.date().alias("date"),
                "event_type"
            )
            .agg([
                pl.col("value").sum().alias("total_value"),
                pl.col("id").count().alias("event_count")
            ])
            .sort("date")
        )
        
        self.con.execute("INSERT INTO daily_summary SELECT * FROM summary")
        
        return {
            "events_loaded": len(df),
            "summary_rows": len(summary),
            "timestamp": datetime.now().isoformat()
        }
    
    def run(self, source_path: str) -> Dict[str, Any]:
        """
        Execute full ETL pipeline.
        
        Args:
            source_path: Path to source data file
            
        Returns:
            Dict with pipeline execution results
            
        Raises:
            PipelineError: If pipeline execution fails
        """
        logger.info(f"Starting pipeline from {source_path}")
        
        try:
            # Extract (lazy - no data loaded yet)
            raw = self.extract(source_path)
            
            # Transform (still lazy)
            transformed = self.transform(raw)
            
            # Collect and load (materialize here)
            result_df = transformed.collect()
            logger.info(f"Transformed {len(result_df)} rows")
            
            load_result = self.load(result_df)
            logger.info(f"Pipeline completed: {load_result}")
            
            return load_result
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}", exc_info=True)
            raise PipelineError(f"Pipeline execution failed: {e}") from e
    
    def run_incremental(self, source_path: str, watermark_col: str = "timestamp") -> Dict[str, Any]:
        """
        Execute incremental ETL pipeline using watermark.
        
        Args:
            source_path: Path to source data file
            watermark_col: Column name for watermark tracking
            
        Returns:
            Dict with pipeline execution results
        """
        logger.info(f"Starting incremental pipeline from {source_path}")
        
        # Get last watermark
        result = self.con.execute("""
            SELECT MAX(last_timestamp) FROM pipeline_checkpoints
            WHERE pipeline_name = 'raw_events'
        """).fetchone()
        last_watermark = result[0] if result[0] else datetime(1900, 1, 1)
        
        logger.info(f"Last watermark: {last_watermark}")
        
        try:
            # Extract with filter
            raw = self.extract(source_path)
            filtered = raw.filter(pl.col(watermark_col) > last_watermark)
            
            # Transform and load
            transformed = self.transform(filtered)
            result_df = transformed.collect()
            
            if len(result_df) == 0:
                logger.info("No new data to process")
                return {"events_loaded": 0, "message": "No new data"}
            
            load_result = self.load(result_df)
            
            # Update watermark
            new_watermark = result_df[watermark_col].max()
            self.con.execute("""
                INSERT OR REPLACE INTO pipeline_checkpoints
                VALUES ('raw_events', ?, ?)
            """, [new_watermark, len(result_df)])
            
            logger.info(f"Incremental pipeline completed: {load_result}")
            return load_result
            
        except Exception as e:
            logger.error(f"Incremental pipeline failed: {e}", exc_info=True)
            raise PipelineError(f"Incremental pipeline execution failed: {e}") from e
    
    def get_summary(self, days: int = 7) -> pl.DataFrame:
        """
        Query recent summary statistics.
        
        Args:
            days: Number of days to look back
            
        Returns:
            DataFrame with summary data
        """
        result = self.con.execute(f"""
            SELECT date, event_type, total_value, event_count
            FROM daily_summary
            WHERE date >= CURRENT_DATE - INTERVAL '{days} days'
            ORDER BY date DESC
        """)
        return result.pl()
    
    def get_watermark(self, pipeline_name: str = "raw_events") -> Optional[datetime]:
        """
        Get last processed timestamp for incremental loading.
        
        Args:
            pipeline_name: Name of pipeline to check
            
        Returns:
            Last timestamp or None
        """
        result = self.con.execute("""
            SELECT last_timestamp FROM pipeline_checkpoints
            WHERE pipeline_name = ?
        """, [pipeline_name]).fetchone()
        return result[0] if result and result[0] else None
    
    def validate_schema(self, df: pl.DataFrame, required_cols: Dict[str, pl.DataType]) -> bool:
        """
        Validate DataFrame has required columns with correct types.
        
        Args:
            df: DataFrame to validate
            required_cols: Dict of column name to expected Polars type
            
        Returns:
            True if valid
            
        Raises:
            PipelineError: If validation fails
        """
        for col, dtype in required_cols.items():
            if col not in df.columns:
                raise PipelineError(f"Missing required column: {col}")
            if df[col].dtype != dtype:
                raise PipelineError(
                    f"Column '{col}' has wrong type: {df[col].dtype} != {dtype}"
                )
        return True


# Example usage
if __name__ == "__main__":
    # Create example config
    config = {
        "duckdb_path": "analytics.db",
        "raw_path": "data/raw",
        "processed_path": "data/processed"
    }
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Using context manager for automatic cleanup
    with DataPipeline("config.json") as pipeline:
        # Run single batch
        result = pipeline.run("data/events_2024.parquet")
        print(f"Loaded {result['events_loaded']} events")
        
        # Or run incremental
        # result = pipeline.run_incremental("data/events_2024.parquet")
        
        # Query results
        summary = pipeline.get_summary(30)
        print("\nLast 30 days summary:")
        print(summary)
        
        # Check watermark
        watermark = pipeline.get_watermark()
        print(f"\nLast processed: {watermark}")
