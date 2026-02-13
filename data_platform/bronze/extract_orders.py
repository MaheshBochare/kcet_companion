import os
import json
import pandas as pd
from sqlalchemy import create_engine, inspect
from datetime import datetime, timezone
import logging

# -------------------------------------------------
# Logging (production-safe)
# -------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# -------------------------------------------------
# Database connection
# -------------------------------------------------
DB_URL = "postgresql://postgres:postgres@localhost:5432/kcet_companion"
engine = create_engine(DB_URL)
inspector = inspect(engine)

# -------------------------------------------------
# Bronze base path
# -------------------------------------------------
BRONZE_BASE_PATH = "data_platform/bronze"
os.makedirs(BRONZE_BASE_PATH, exist_ok=True)

# -------------------------------------------------
# Schema name
# -------------------------------------------------
DB_SCHEMA = "public"

# -------------------------------------------------
# Tables to ingest
# -------------------------------------------------
tables = [
    "category",
    "college_branch",
    "core_college",
    "core_branch",
    "core_cutoff",
    "round",
    "seat_matrix",
    "year_dim",
]

# -------------------------------------------------
# Ingestion loop
# -------------------------------------------------
for table in tables:
    try:
        logging.info(f"Starting ingestion for table: {DB_SCHEMA}.{table}")

        table_path = os.path.join(BRONZE_BASE_PATH, table)
        os.makedirs(table_path, exist_ok=True)

        # -----------------------------
        # Read table from Postgres
        # -----------------------------
        query = f"SELECT * FROM {DB_SCHEMA}.{table}"
        df = pd.read_sql(query, engine)

        # -----------------------------
        # Audit columns (Bronze rules)
        # -----------------------------
        ingestion_time = datetime.now(timezone.utc)

        df["ingestion_ts"] = ingestion_time
        df["source_schema"] = DB_SCHEMA
        df["source_table"] = table

        # -----------------------------
        # Write Parquet
        # -----------------------------
        parquet_file = f"{table}_{ingestion_time.strftime('%Y-%m-%d')}.parquet"
        parquet_path = os.path.join(table_path, parquet_file)

        df.to_parquet(
            parquet_path,
            index=False,
            engine="pyarrow"
        )

        # -----------------------------
        # Schema metadata
        # -----------------------------
        columns = inspector.get_columns(table, schema=DB_SCHEMA)

        schema_metadata = {
            "table": table,
            "schema": DB_SCHEMA,
            "row_count": len(df),
            "extracted_at": ingestion_time.isoformat(),
            "columns": [
                {
                    "name": col["name"],
                    "type": str(col["type"]),
                    "nullable": col["nullable"]
                }
                for col in columns
            ]
        }

        schema_file = os.path.join(table_path, "_schema.json")
        with open(schema_file, "w") as f:
            json.dump(schema_metadata, f, indent=2)

        logging.info(f"Bronze Parquet written: {parquet_path}")
        logging.info(f"Schema metadata written: {schema_file}")

    except Exception as e:
        logging.error(f"Failed to ingest table {table}", exc_info=True)

logging.info("Bronze ingestion completed successfully")
