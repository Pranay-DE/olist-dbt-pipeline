import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM stg_customers").df()
df.to_csv('customers_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()