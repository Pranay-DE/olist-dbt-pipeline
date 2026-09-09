import duckdb
conn = duckdb.connect('dev.duckdb')

# print("=== Backup TABLES ===")
# conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%backup%'").show()

print("=== Sales Performance Sample ===")
conn.sql("""
    SELECT
        product_category,
        fiscal_year,
        order_month,
        total_orders,
        total_revenue,
        avg_freight_percentage
    FROM sales_performance
    ORDER BY total_revenue DESC
    LIMIT 10
""").show()

print("=== ROW COUNT ===")
conn.sql("SELECT COUNT(*) as total FROM sales_performance").show()