{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If Exists {{ this.name }}_backup",
        "Create Table {{ this.name }}_backup as Select * From {{ this.name }}"
    ]
)
}}

with orders as(SELECT * FROM {{ref ('orders_clean')}}),
customers as(Select * From {{ref ('customers_clean')}}),
items as(Select * From {{ref ('order_items_clean')}}),
products as(Select * From {{ref ('products_clean')}}),
sellers as(Select * From {{ref ('sellers_clean')}}),
reviews as(Select * From {{ref ('order_reviews_clean')}}),

-- agg payment to order level
payment_agg as(
    SELECT
        order_id,
        MAX(CASE WHEN payment_sequential = 1
            THEN payment_type END) as primary_payment_type,
        SUM(payment_value) as total_payment_value,
        CASE WHEN COUNT(*) > 1
            THEN TRUE ELSE FALSE
        END as has_multiple_payment
    FROM {{ref ('order_payments_clean')}}
    GROUP BY order_id
),

master as(
    SELECT
        o.order_id,
        o.ordered_at,
        o.delivered_at,
        o.estimated_delivery_at,
        o.order_status_category,
        o.actual_days_to_delivered,
        o.estimated_days_to_delivered,
        o.delivery_variance_days,
        o.delivery_category,
        i.order_item_id,
        i.product_id,
        p.product_category,
        p.product_weight_g,
        p.product_volume_cm3,
        i.seller_id,
        s.city as seller_city,
        s.state as seller_state,
        i.price,
        i.freight_value,
        i.total_item_value,
        i.price_category,
        pay.primary_payment_type,
        pay.total_payment_value,
        pay.has_multiple_payment,
        c.customer_id,
        c.customer_unique_id,
        c.customer_city,
        c.customer_state,
        c.customer_type,
        r.review_score,
        r.review_score_category,
        r.days_to_answer,
        r.is_late_response
    FROM orders as o
    LEFT JOIN customers as c
        ON o.customer_id = c.customer_id
    LEFT JOIN items as i
        ON o.order_id = i.order_id
    LEFT JOIN products as p
        ON i.product_id = p.product_id
    LEFT JOIN sellers as s
        ON i.seller_id = s.seller_id
    LEFT JOIN payment_agg as pay
        ON o.order_id = pay.order_id
    LEFT JOIN reviews as r
        ON o.order_id = r.order_id
    WHERE o.is_date_valid = 'VALID'
)

Select * From master