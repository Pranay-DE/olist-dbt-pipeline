import duckdb
conn = duckdb.connect('dev.duckdb')

print("=== CLEAN TABLES ===")
conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%clean%'").show()

# print("=== Zero Installments Payment ===")
# conn.sql("""
#     Select * From
#     stg_order_payments
#     where payment_installments = 0
# """).show()

# print("=== Check True Duplicates===")
# conn.sql("""
#     Select
#         order_id,
#         payment_sequential,
#         count(*) as count
#     From stg_order_payments
#     Group by order_id, payment_sequential
#     Having count(*) > 1
# """).show()

# print("=== Payment Type Wise Distribution ===")
# conn.sql("""
#     Select payment_type, count(*) as count
#     From stg_order_payments
#     Group by payment_type
#     Order by count(*) desc
# """).show()