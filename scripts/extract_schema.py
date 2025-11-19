"""
extract_schema.py
-----------------
Extracts database schema information (table names, columns, and data types)
and saves it as a JSON file for LLM prompt usage.
"""

import os
import json
import logging
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_database_engine():
    """Create SQLAlchemy engine from DATABASE_URL"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env")
    return create_engine(database_url)

def extract_schema(engine):
    """Extracts schema details using SQLAlchemy inspector."""
    inspector = inspect(engine)
    schema_info = {}

    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        schema_info[table_name] = [
            {
                "name": col["name"],
                "type": str(col["type"]),
                "nullable": col["nullable"],
                "default": str(col["default"]),
            }
            for col in columns
        ]
    return schema_info

def save_schema_to_file(schema, output_path="data/schema_info.json"):
    """Save schema dictionary as JSON"""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=4)
    logging.info(f"✅ Schema saved to {output_path}")

def main():
    logging.info("🔍 Extracting database schema...")
    engine = get_database_engine()
    schema = extract_schema(engine)
    save_schema_to_file(schema)
    logging.info("📘 Schema extraction complete!")

if __name__ == "__main__":
    main()
