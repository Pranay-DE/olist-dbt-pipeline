{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If EXISTS {{ this.name }}_backup",
        "Create TABLE {{ this.name }}_backup as Select * FROM {{ this.name }}"
    ]
)
}}

with order_items as(
    select * from {{ref('stg_order_items')}}
),

removed_duplicates as(
    Select *,
        ROW_NUMBER() Over(
            Partition BY order_id, product_id
            Order BY order_item_id
        ) as row_num
    from order_items
),

cleaned as(
    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        shipping_limit_date,
        price,
        Case
            When price <= 500 Then 'Low Price Product'
            When price <= 2000 Then 'Mid Price Product'
            When price <= 5000 Then 'High Price Product'
            Else 'Premium'
        End as price_category,
        freight_value,
        ROUND(freight_value / Nullif(price + freight_value, 0) * 100, 2)
        as freight_percentage,
        price + freight_value as total_item_value
    From removed_duplicates
    WHERE row_num = 1
)

Select * From cleaned