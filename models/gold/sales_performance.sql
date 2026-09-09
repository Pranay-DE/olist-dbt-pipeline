{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If Exists {{ this.name }}_backup",
        "Create Table {{ this.name }}_backup as Select * From {{ this.name }}"
    ]
)
}}

with master as(
    SELECT * FROM{{ ref('olist_master_table') }}
    WHERE product_id IS NOT NULL
),

sales as(
    SELECT
        product_category,
        fiscal_year,
        MONTH(ordered_at) as order_month,
        COUNT(DISTINCT order_id) as total_orders,
        COUNT(DISTINCT product_id) as total_products_sold,
        SUM(price) as total_revenue,
        SUM(freight_value) as total_freight,
        SUM(total_item_value) as total_value,
        ROUND(AVG(price), 2) as avg_item_price,
        ROUND(AVG(freight_value), 2) as avg_item_freight_value,
        ROUND(
                SUM(freight_value) / 
                NULLIF(SUM(total_item_value), 0) * 100
        , 2) as avg_freight_percentage
    FROM master
    GROUP BY
        product_category,
        fiscal_year,
        MONTH(ordered_at)
)

SELECT * FROM sales