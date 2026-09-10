{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "DROP TABLE IF EXISTS {{ this.name }}_backup",
        "CREATE TABLE {{ this.name }}_backup as SELECT * FROM {{ this.name }}"
    ]
)
}}

with master as(
    Select * FROM {{ ref('olist_master_table') }}
    WHERE seller_id IS NOT NULL),

sellers as(
    SELECT
        seller_id,
        seller_city,
        seller_state,
        COUNT(DISTINCT order_id) as total_orders,

        -- orders count based on delivery category
        COUNT(DISTINCT
                CASE
                    WHEN delivery_category IN ('Delivered On Time', 'Late')
                    THEN order_id
                END) as delivered_orders,
        COUNT(DISTINCT
                CASE
                    WHEN delivery_category = 'Delivered On Time'
                    THEN order_id
                END) as on_time_orders,
        COUNT(DISTINCT
                CASE
                    WHEN delivery_category = 'Late'
                    THEN order_id
                END) as late_orders,
        COUNT(DISTINCT
                CASE
                    WHEN delivery_category = 'Not Delivered'
                    THEN order_id
                END) as not_delivered_orders,

        -- Delivery Rate Metrics
        ROUND(
            1.0 * COUNT(DISTINCT CASE WHEN delivery_category = 'Delivered On Time' THEN order_id END)
            / NULLIF(COUNT(DISTINCT order_id),0),
        2) as on_time_delivery_rate,
        ROUND(
            1.0 * COUNT(DISTINCT CASE WHEN delivery_category = 'Late' THEN order_id END)
            / NULLIF(COUNT(DISTINCT order_id),0),
        2) as late_delivery_rate,
        ROUND(
            1.0 * COUNT(DISTINCT CASE WHEN delivery_category = 'Not Delivered' THEN order_id END)
            / NULLIF(COUNT(DISTINCT order_id),0),
        2) as not_delivered_rate,

        ROUND(
            AVG(CASE
                    WHEN delivery_category IN ('Delivered On Time', 'Late')
                    THEN actual_days_to_delivered
                END),
        2) as avg_actual_days_to_delievered,
        ROUND(
            AVG(CASE
                    WHEN delivery_category IN ('Delivered On Time', 'Late')
                    THEN delivery_variance_days
                END),
        2) as avg_delivery_variance_days,
        ROUND(
            AVG(review_score),
        2) as avg_review_score,
        COUNT(review_score) as total_review_count
    FROM master
    GROUP BY
        seller_id,
        seller_city,
        seller_state
)

SELECT * FROM sellers