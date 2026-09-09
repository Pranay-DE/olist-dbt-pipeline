{{ config(
    MATERIALIZED = 'table'
)
}}

with master as(
    SELECT * FROM {{ ref('olist_master_table') }}
),

payment_ranked as(
    SELECT
        customer_unique_id,
        primary_payment_type,
        COUNT(*) AS usage_count,
        ROW_NUMBER() OVER (
            PARTITION BY customer_unique_id
            ORDER BY COUNT(*) DESC, primary_payment_type
        ) AS rank
    FROM master
    GROUP BY customer_unique_id, primary_payment_type
),

customer as(
    SELECT
        m.customer_unique_id,
        m.customer_city,
        m.customer_state,
        m.customer_type,
        SUM(m.total_item_value) as total_spend,
        COUNT(DISTINCT m.order_id) as total_orders,
        AVG(m.review_score) as avg_review_score,
        AVG(m.actual_days_to_delivered) as avg_delivery_days,
        p.primary_payment_type as preferred_payment_type,
        MAX(p.usage_count) as payment_usage_count
    FROM master as m
    LEFT JOIN payment_ranked as p
        ON m.customer_unique_id = p.customer_unique_id
        AND p.rank = 1
    GROUP BY
        m.customer_unique_id,
        m.customer_city,
        m.customer_state,
        m.customer_type,
        p.primary_payment_type
)

SELECT * FROM customer