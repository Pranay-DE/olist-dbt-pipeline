import duckdb
import os

# Connect with duckdb database
conn = duckdb.connect('dev.duckdb')

# Path of raw data folder
raw_data_path = 'raw_data'

# Loop through every csv file and load it in duckdb
for file in os.listdir(raw_data_path):
    if file.endswith('.csv'):
        table_name = file.replace('.csv','')
        file_path = os.path.join(raw_data_path, file)
        conn.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{file_path}')
            """)

# Verify all tables loaded
print("\nTables in DuckDB:")
print(conn.execute("Show Tables").fetchall())

conn.close()
print("\nDone!")