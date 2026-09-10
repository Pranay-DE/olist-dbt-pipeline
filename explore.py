import duckdb
conn = duckdb.connect('dev.duckdb')

# print("=== Backup TABLES ===")
# conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%backup%'").show()

# print("=== Delivery Performance Sample ===")
# conn.sql("""
#     SELECT * FROM delivery_performance
#     LIMIT 10
# """).show()

# print("=== ROW COUNT ===")
# conn.sql("Select count(*) as total_rows FROM delivery_performance").show()

print("=== DESCRIBE DELIVERY PERFORMANCE ===")
conn.sql("DESCRIBE delivery_performance").show()

print("=== CHECK NULLS ===")
conn.sql("""
    SELECT
        SUM(CASE WHEN seller_id IS NULL THEN 1 ELSE 0 END) as null_seller_id,
        SUM(CASE WHEN seller_city IS NULL THEN 1 ELSE 0 END) as null_seller_city,
        SUM(CASE WHEN seller_state IS NULL THEN 1 ELSE 0 END) as null_seller_state,
        SUM(CASE WHEN total_orders IS NULL THEN 1 ELSE 0 END) as null_total_orders,
        SUM(CASE WHEN delivered_orders IS NULL THEN 1 ELSE 0 END) as null_delivered_orders
    FROM delivery_performance
""").show()

print("=== CHECK NULLS ===")
conn.sql("""
    SELECT
        SUM(CASE WHEN on_time_orders IS NULL THEN 1 ELSE 0 END) as null_on_time_orders,
        SUM(CASE WHEN late_orders IS NULL THEN 1 ELSE 0 END) as null_late_orders,
        SUM(CASE WHEN not_delivered_orders IS NULL THEN 1 ELSE 0 END) as null_not_delivered_orders,
        SUM(CASE WHEN on_time_delivery_rate IS NULL THEN 1 ELSE 0 END) as null_on_time_delivery_rate,
        SUM(CASE WHEN late_delivery_rate IS NULL THEN 1 ELSE 0 END) as null_late_delivery_rate
    FROM delivery_performance
""").show()

print("=== CHECK NULLS ===")
conn.sql("""
    SELECT
        SUM(CASE WHEN not_delivered_rate IS NULL THEN 1 ELSE 0 END) as null_not_delivered_rate,
        SUM(CASE WHEN avg_actual_days_to_delievered IS NULL THEN 1 ELSE 0 END) as null_avg_actual_days_to_delievered,
        SUM(CASE WHEN avg_delivery_variance_days IS NULL THEN 1 ELSE 0 END) as null_avg_delivery_variance_days,
        SUM(CASE WHEN avg_review_score IS NULL THEN 1 ELSE 0 END) as null_avg_review_score,
        SUM(CASE WHEN total_review_count IS NULL THEN 1 ELSE 0 END) as null_total_review_count
    FROM delivery_performance
""").show()

# conn.sql("Select seller_id FROM delivery_performance where avg_review_score is NULL").show()

# print("=== UNIQUE SELLER ID ===")
# conn.sql("""
#     SELECT
#         seller_id,
#         count(*) as count
#     FROM delivery_performance
#     GROUP BY seller_id
#     HAVING COUNT(*) > 1
# """).show()