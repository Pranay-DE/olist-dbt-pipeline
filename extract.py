import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM orders_clean").df()
df.to_csv('orders_clean_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()