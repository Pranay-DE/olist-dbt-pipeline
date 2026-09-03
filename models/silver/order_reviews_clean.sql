{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If Exists {{ this.name }}_backup",
        "Create Table {{ this.name }}_backup as Select * From {{ this.name }}"
    ]
)
}}

with review as(
    Select * From {{ref('stg_order_reviews')}}
),

review_flags as(
    SELECT
        review_id,
        order_id,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            Order By review_creation_date DESC
        ) as order_row_num,
        COUNT(*) OVER (
            PARTITION BY review_id
        ) as review_id_count
    From review
),

cleaned as(
    SELECT
        r.review_id,
        r.order_id,
        r.review_score,
        CASE 
            WHEN r.review_score <= 2 THEN 'Negative'
            WHEN r.review_score = 3 THEN 'Neutral'
            ELSE 'Positive'
        END as review_score_category,
        CASE 
            WHEN r.review_comment_title is null Then 'No Comment'
            ELSE r.review_comment_title
            END as review_title,
        CASE 
            WHEN r.review_comment_message is null Then 'No Comment'
            ELSE r.review_comment_message
            END as review_message,
        r.review_creation_date as reviewed_at,
        r.review_answer_timestamp as answered_at,
        Datediff('days', r.review_creation_date, r.review_answer_timestamp) as days_to_answer,
        CASE
            WHEN DATEDIFF('day', r.review_creation_date, r.review_answer_timestamp) > 30
                THEN 'Late Response'
            ELSE 'On Time'
        END AS is_late_response,
        CASE 
            WHEN f.review_id_count = 1 THEN true  
            ELSE false
        END as is_review_id_unique
    From review as r
    inner join review_flags as f
        on r.review_id = f.review_id
        and r.order_id = f.order_id
    where f.order_row_num = 1
)

Select * From cleaned