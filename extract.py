import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM stg_sellers").df()
df.to_csv('sellers_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()