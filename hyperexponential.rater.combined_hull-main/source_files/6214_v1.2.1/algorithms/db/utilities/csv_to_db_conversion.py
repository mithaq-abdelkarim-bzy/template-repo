import os
import sqlite3
import pandas as pd

# Load your data into a DataFrame
table_name = "../../../parameter_tables/combined_hull.csv"  # Your CSV file name
table_path = os.path.join(os.path.dirname(__file__), table_name)  # Path to the CSV file
vessels_df = pd.read_csv(table_path)  # Load data into a DataFrame
vessels_df_lite = vessels_df.sample(frac=0.05, random_state=None)

# Specify the path where the SQLite database file will be created
db_file_path = os.path.join(os.path.dirname(__file__), "../combined_hull.db")

# Create a connection to the disk-based SQLite database
conn = sqlite3.connect(db_file_path)

# Load the DataFrame into a SQL table within the database file
vessels_df.to_sql("vessels", conn, index=False, if_exists="replace")

# Close the connection when done
conn.close()
