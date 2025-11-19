"""
db_setup.py
------------
Handles database creation and schema ingestion from CSV files.
This script is intended to be run once to set up the local SQLite database.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from the .env file in the project root
load_dotenv()

def get_database_engine():
    """Creates and returns a SQLAlchemy engine based on the DATABASE_URL."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        logging.error("DATABASE_URL is not set in the .env file.")
        raise ValueError("DATABASE_URL environment variable not found.")
    
    logging.info("Connecting to the database...")
    try:
        engine = create_engine(database_url)
        # Test the connection
        with engine.connect() as connection:
            logging.info("Database connection successful.")
        return engine
    except Exception as e:
        logging.error(f"Failed to create database engine: {e}")
        raise

def clean_column_name(col: str) -> str:
    """Sanitizes column names to be valid in SQL."""
    return ''.join(e for e in col.strip().replace(' ', '_') if e.isalnum() or e == '_')

def load_csv_to_sql(engine, csv_path: str, table_name: str):
    """Loads a CSV file into a specified SQL table."""
    if not os.path.exists(csv_path):
        logging.error(f"CSV file not found at: {csv_path}")
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    logging.info(f"Processing {csv_path} for table '{table_name}'...")
    
    df = pd.read_csv(csv_path)
    df.columns = [clean_column_name(c) for c in df.columns]
    
    logging.info(f"Writing {len(df)} rows to table '{table_name}'...")
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)
    logging.info(f"✅ Table '{table_name}' created successfully.")

def main():
    """Main function to set up the database and load data."""
    logging.info("Starting database setup...")
    try:
        engine = get_database_engine()
        
        # Define the mapping of table names to CSV file paths
        csv_files = {
            "social_data": "data/social-listening.csv",
            "cancer_data": "data/data_Cancer_v2_Merged Data 2.csv"
        }

        for table, path in csv_files.items():
            load_csv_to_sql(engine, path, table)

        logging.info("\n📘 Database setup complete. All tables have been loaded.")

    except Exception as e:
        logging.error(f"An error occurred during database setup: {e}")

if __name__ == "__main__":
    main()