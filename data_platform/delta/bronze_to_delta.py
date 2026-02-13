import os
from pyspark.sql import SparkSession
from datetime import datetime, timezone
import logging

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------------------------
# Spark Session with Delta Lake
# -------------------------------------------------
spark = (
    SparkSession.builder
    .appName("KCET-Bronze-Parquet-to-Delta")
    .config(
        "spark.sql.extensions",
        "io.delta.sql.DeltaSparkSessionExtension"
    )
    .config(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog"
    )
    .getOrCreate()
)

# -------------------------------------------------
# Paths (ALIGNED WITH YOUR BRONZE OUTPUT)
# -------------------------------------------------
PARQUET_BRONZE_BASE = "data_platform/bronze"
DELTA_BRONZE_BASE = "data_lake/bronze_delta"

os.makedirs(DELTA_BRONZE_BASE, exist_ok=True)

# -------------------------------------------------
# Convert one table
# -------------------------------------------------
def convert_table(table_name):
    logging.info(f"Converting Bronze Parquet → Delta for table: {table_name}")

    parquet_path = os.path.join(
        PARQUET_BRONZE_BASE,
        table_name,
        "*.parquet"
    )

    delta_path = os.path.join(
        DELTA_BRONZE_BASE,
        table_name
    )

    # Read ALL parquet files for the table
    df = spark.read.parquet(parquet_path)

    # Write as Delta (append-only, Bronze rule)
    (
        df.write
        .format("delta")
        .mode("append")
        .save(delta_path)
    )

    logging.info(f"Delta Bronze written: {delta_path}")

# -------------------------------------------------
# Main Execution
# -------------------------------------------------
def main():
    tables = [
        d for d in os.listdir(PARQUET_BRONZE_BASE)
        if os.path.isdir(os.path.join(PARQUET_BRONZE_BASE, d))
    ]

    for table in tables:
        convert_table(table)

    logging.info("PHASE 2 completed: Bronze Parquet → Delta conversion")

if __name__ == "__main__":
    main()
