{{ config(
    materialized='table',
    pre_hook=[
        "Drop Table If EXISTS {{ this.name }}_backup",
        "Create TABLE {{ this.name }}_backup as Select * FROM {{ this.name }}"
    ]
)
}}

with orders as(
    select * from{{ref('stg_orders')}}
),

cleaned as(
    Select
        order_id,
        customer_id,
        order_status,
        CASE 
            WHEN order_status = 'delivered' THEN 'Completed'
            WHEN order_status in ('shipped', 'invoiced', 'processing', 'approved', 'created')  THEN 'In Progress'
            WHEN order_status in ('canceled', 'unavailable') THEN 'Canceled'
            ELSE order_status
        END as order_status_category,
        order_purchase_timestamp as ordered_at,
        order_approved_at as approved_at,
        order_delivered_carrier_date as shipped_at,
        order_delivered_customer_date as delivered_at,
        order_estimated_delivery_date as estimated_delivery_at,
        CASE
            WHEN month(order_purchase_timestamp) >= 4
            THEN concat(
                'FY', year(order_purchase_timestamp),
                '-', RIGHT(CAST(year(order_purchase_timestamp) + 1 as VARCHAR),2))
            else concat(
                'FY', year(order_purchase_timestamp) - 1,
                '-', RIGHT(CAST(year(order_purchase_timestamp) as VARCHAR),2))
            end as fiscal_year,
        year(order_purchase_timestamp) as order_year,
        month(order_purchase_timestamp) as order_month,
        dayofweek(order_purchase_timestamp) as order_day_of_week,
        CASE 
            WHEN order_approved_at is NOT NULL
            THEN datediff('hour', order_purchase_timestamp, order_approved_at)  
        END as hours_to_approve,
        CASE 
            WHEN order_delivered_carrier_date is NOT NULL
            THEN datediff('day', order_purchase_timestamp, order_delivered_carrier_date)
        END as days_to_ship,
        CASE 
            WHEN order_delivered_customer_date is NOT NULL
            THEN datediff('day', order_purchase_timestamp, order_delivered_customer_date)
        END as actual_days_to_delivered,
        CASE 
            WHEN order_estimated_delivery_date is NOT NULL
            THEN datediff('day', order_purchase_timestamp, order_estimated_delivery_date)
        END as estimated_days_to_delivered,
        CASE 
            WHEN order_estimated_delivery_date is NOT NULL
            AND order_delivered_customer_date is NOT NULL
            THEN datediff('day', order_estimated_delivery_date, order_delivered_customer_date)
        END as delivery_variance_days,
        CASE 
            WHEN order_delivered_customer_date IS NULL
            THEN 'Not Delivered'
            WHEN order_delivered_customer_date <= order_estimated_delivery_date
            THEN 'Delivered On Time'
            ElSE 'Late'
        END as delivery_category,
        CASE
            WHEN order_approved_at < order_purchase_timestamp
                or order_delivered_carrier_date < order_approved_at
                or order_delivered_customer_date < order_delivered_carrier_date
            THEN 'Invalid Date'
            ELSE 'VALID'
        END as is_date_valid
    FROM orders
)

Select * FROM cleaned