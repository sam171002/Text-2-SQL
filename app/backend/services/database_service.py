"""
db_service.py
--------------
Handles Azure SQL Database connection and query execution.
Includes retry logic and clear logging.
"""

import os
import pyodbc
import time
import logging
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ------------------ AZURE CONNECTION FUNCTION ------------------

def get_azure_connection(max_retries=3, retry_delay=5):
    """
    Establish connection to Azure SQL Database.
    Retries a few times if connection fails (useful for network/firewall delays).
    """
    server = os.getenv("AZURE_SQL_SERVER")       # e.g., text2sqlserver.database.windows.net
    database = os.getenv("AZURE_SQL_DATABASE")   # e.g., cancer_data_db
    username = os.getenv("AZURE_SQL_USER")       # e.g., azureadmin
    password = os.getenv("AZURE_SQL_PASSWORD")   # your password

    if not all([server, database, username, password]):
        logging.error("❌ Missing one or more Azure SQL credentials in .env file.")
        return None

    conn_str = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"UID={username};"
        f"PWD={password};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )

    for attempt in range(1, max_retries + 1):
        try:
            logging.info(f"🔌 Connecting to Azure SQL Database (Attempt {attempt}/{max_retries})...")
            connection = pyodbc.connect(conn_str)
            logging.info("✅ Connected to Azure SQL Database successfully.")
            return connection

        except Exception as e:
            logging.error(f"⚠️ Connection attempt {attempt} failed: {e}")
            if attempt < max_retries:
                logging.info(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logging.error("❌ All connection attempts failed.")
                return None


# ------------------ QUERY EXECUTION FUNCTION ------------------

def execute_sql_query(sql_query: str):
    """
    Executes SQL query on Azure SQL Database and returns results in dict format.
    """
    connection = get_azure_connection()
    if connection is None:
        logging.error("❌ Failed to establish Azure SQL connection. Cannot execute query.")
        return None

    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        connection.close()

        logging.info(f"✅ Query executed successfully — fetched {len(rows)} rows.")
        return {"columns": columns, "rows": rows}

    except Exception as e:
        logging.error(f"❌ Error executing SQL query: {e}")
        return None
