import duckdb
conn = duckdb.connect('dev.duckdb')

# print("=== Backup TABLES ===")
# conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%backup%'").show()

# print("=== Customer Behaviour Sample ===")
# conn.sql("""
#     SELECT *
#     FROM customer_behaviour
#     ORDER BY total_orders DESC
#     LIMIT 10
# """).show()

# print("=== ROW COUNT ===")
# conn.sql("SELECT COUNT(*) as total FROM customer_behaviour").show()

print("=== CHECK NULLS ===")
conn.sql("""
    Select
        SUM(CASE WHEN customer_unique_id IS NULL THEN 1 ELSE 0 END) as null_customer_unique_id,
        SUM(CASE WHEN customer_city IS NULL THEN 1 ELSE 0 END) as null_customer_city,
        SUM(CASE WHEN customer_state IS NULL THEN 1 ELSE 0 END) as null_customer_state,
        SUM(CASE WHEN customer_type IS NULL THEN 1 ELSE 0 END) as null_customer_type,
        SUM(CASE WHEN total_spend IS NULL THEN 1 ELSE 0 END) as null_total_spend
    FROM customer_behaviour
""").show()

print("=== CHECK NULLS ===")
conn.sql("""
    Select
        SUM(CASE WHEN total_orders IS NULL THEN 1 ELSE 0 END) as null_total_orders,
        SUM(CASE WHEN avg_review_score IS NULL THEN 1 ELSE 0 END) as null_avg_review_score,
        SUM(CASE WHEN avg_delivery_days IS NULL THEN 1 ELSE 0 END) as null_avg_delivery_days,
        SUM(CASE WHEN preferred_payment_type IS NULL THEN 1 ELSE 0 END) as null_preferred_payment_type,
        SUM(CASE WHEN payment_usage_count IS NULL THEN 1 ELSE 0 END) as null_payment_usage_count
    FROM customer_behaviour
""").show()

# conn.sql("""
#     Select order_id
#     From order_payments_clean
#     Group By order_id
#     Having MIN(payment_sequential) > 1
# """).show()

# conn.sql("Select * From customer_behaviour where preferred_payment_type is null").show()