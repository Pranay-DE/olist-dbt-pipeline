import duckdb
conn = duckdb.connect('dev.duckdb')

print("=== CLEAN TABLES ===")
conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%clean%'").show()

# print("=== Sellers Columns ===")
# conn.sql("Describe stg_sellers").show()

# print("=== Row Count ===")
# conn.sql("Select count(*) as total_rows From stg_sellers").show()

# print("=== Duplicate Seller ID ===")
# conn.sql("""
#     Select
#         seller_id,
#         count(*) as count
#     From stg_sellers
#     Group By seller_id
#     Having count(*) > 1
# """).show()

# print("=== Null Check ===")
# conn.sql("""
#     Select
#         SUM(CASE WHEN seller_id is null THEN 1 ELSE 0 END) as null_seller_id,
#         SUM(CASE WHEN seller_zip_code_prefix is null THEN 1 ELSE 0 END) as null_seller_zip_code_prefix,
#         SUM(CASE WHEN seller_city is null THEN 1 ELSE 0 END) as null_seller_city,
#         SUM(CASE WHEN seller_state is null THEN 1 ELSE 0 END) as null_seller_state
#     From stg_sellers
# """).show()

# print("=== State Distribution ===")
# conn.sql("""
#     Select
#         seller_state,
#         count(*) as count
#     From stg_sellers
#     Group by seller_state
#     Order BY count desc
# """).show()