import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM stg_order_items").df()
df.to_csv('order_items_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()