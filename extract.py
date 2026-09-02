import duckdb
import pandas as pd

conn = duckdb.connect('dev.duckdb')

df = conn.execute("SELECT * FROM stg_product_translation").df()
df.to_csv('products_translation_preview.csv', index = False)
print(f"Exported {len(df)} row")

conn.close()