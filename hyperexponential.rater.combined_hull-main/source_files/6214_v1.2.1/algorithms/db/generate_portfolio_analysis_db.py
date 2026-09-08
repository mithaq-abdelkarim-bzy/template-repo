import os
import sqlite3
import pandas as pd

csv_tables = [
    "Vessel.csv",
    "Application.csv",
    "CoreMasterList.csv",
    "CoreUpdateList.csv",
    "RaterKVData.csv",
]

# Specify the path where the SQLite database file will be created
db_file_path = os.path.join(os.path.dirname(__file__), "portfolio_analysis.db")
# Create a connection to the disk-based SQLite database
conn = sqlite3.connect(db_file_path)

for table_name in csv_tables:
    table_path = os.path.join(os.path.dirname(__file__), table_name)
    df = pd.read_csv(table_path)
    df.to_sql(table_name.split(".")[0], conn, index=False, if_exists="replace")

conn.close()
