import duckdb
conn = duckdb.connect('dev.duckdb')

# Check for duplicate ids
print("===Duplicate Order ID's===")
conn.sql("""
    Select order_id, Count(*) as orders_count
    From olist_orders_dataset
    Group By order_id
    Having Count(*) > 1
""").show()

# Order status distribution
print("===Order Status===")
conn.sql("""
    Select order_status, Count(*) as status_count
    From olist_orders_dataset
    Group By order_status
    Order By status_count Desc
""").show()

# Check date sequence violations
print("===Date Violations===")
conn.sql("""
    Select count(*) as date_violations
    From olist_orders_dataset
    where
        (order_approved_at is not null
        and order_approved_at < order_purchase_timestamp)
    or
        (order_delivered_carrier_date is not null
        and order_approved_at is not null
        and order_delivered_carrier_date < order_approved_at)
    or
        (order_delivered_customer_date is not null
        and order_delivered_carrier_date is not null
        and order_delivered_customer_date < order_delivered_carrier_date)
""").show()

# Check nulls in date
print("===Null Dates===")
conn.sql("""
    Select
        count(*) as total_order,
        SUM(case when order_approved_at is null then 1 else 0 end) as null_approved_date,
        SUM(case when order_delivered_carrier_date is null then 1 else 0 end) as null_shipped_date,
        SUM(case when order_delivered_customer_date IS NULL THEN 1 ELSE 0 END) as null_delivered_date
    From olist_orders_dataset 
""").show()

# Check fiscal year distribution
print("===Fiscal Year Dsitribution===")
conn.sql("""
    Select
        case
            when month(order_purchase_timestamp) >= 4
            then concat('FY', Year(order_purchase_timestamp), '-',
                cast(Year(order_purchase_timestamp) + 1 as VARCHAR))
            else CONCAT('FY ', YEAR(order_purchase_timestamp) - 1, '-',
                CAST(YEAR(order_purchase_timestamp) AS VARCHAR))
        end as fiscal_year,
        count(*) as order_count
    from olist_orders_dataset
    group by fiscal_year
    order by fiscal_year
""").show()

conn.close()