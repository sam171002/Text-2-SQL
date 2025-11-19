import pandas as pd
import pyodbc
from app.backend.services.database_service import get_azure_connection

# Path to your local CSV
csv_path = r"C:\Users\Asus\Downloads\Capstone-text2SQL\data\data_Cancer_v2_Merged Data 2.csv"

# Read CSV
df = pd.read_csv(csv_path)

# Clean column names (SQL-safe)
df.columns = [c.replace(" ", "_").replace("-", "_") for c in df.columns]

# Connect to Azure SQL
conn = get_azure_connection()
cursor = conn.cursor()

# Drop old table if it exists (optional)
cursor.execute("IF OBJECT_ID('cancer_data', 'U') IS NOT NULL DROP TABLE cancer_data;")

# Create table dynamically based on dataframe
columns = ", ".join([f"[{col}] NVARCHAR(MAX)" for col in df.columns])
create_table_query = f"CREATE TABLE cancer_data ({columns});"
cursor.execute(create_table_query)
conn.commit()

# Insert data row by row
for _, row in df.iterrows():
    values = "', '".join(str(x).replace("'", "''") for x in row)
    insert_query = f"INSERT INTO cancer_data VALUES ('{values}');"
    cursor.execute(insert_query)

conn.commit()
conn.close()

print("✅ CSV successfully uploaded to Azure SQL Database as 'cancer_data'.")
