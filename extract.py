import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM customer_behaviour").df()
df.to_csv('customer_behaviour_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()