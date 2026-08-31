import duckdb
conn = duckdb.connect('dev.duckdb')

print("=== Customers Columns ===")
conn.sql("Describe olist_customers_dataset").show()

print("=== Row Count ===")
conn.sql("Select count(*) as total From olist_customers_dataset").show()

print("=== Duplicate Customer ID ===")
conn.sql("""
    Select customer_id, count(*) as count
    From olist_customers_dataset
    Group by customer_id
    Having Count(*) > 1
    Order by Count desc
""").show()

print("=== Duplicate Customer Unique ID")
conn.sql("""
    Select customer_unique_id, count(*) as count
    From olist_customers_dataset
    Group by customer_unique_id
    Having count(*) > 1
    Order By count desc
""").show()

print("=== State Distribution ===")
conn.sql("""
    Select customer_state, count(*) as count
    From olist_customers_dataset
    Group by customer_state
    Order by count desc
""").show()

print("=== Null Check ===")
conn.sql("""
    Select
        SUM(Case when customer_id is null then 1 else 0 end) as null_customer_id,
        SUM(Case when customer_unique_id is null then 1 else 0 end) as null_customer_unique_id,
        SUM(Case when customer_city is null then 1 else 0 end) as null_customer_city,
        SUM(Case when customer_state is null then 1 else 0 end) as null_customer_state
    From olist_customers_dataset
""").show()

conn.close()