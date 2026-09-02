import duckdb
conn = duckdb.connect('dev.duckdb')

print("=== CLEAN TABLES ===")
conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%clean%'").show()