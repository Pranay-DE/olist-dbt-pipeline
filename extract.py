import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM olist_master_table").df()
df.to_csv('olist_master_table_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()