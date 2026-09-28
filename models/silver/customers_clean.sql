{{ config(
    MATERIALIZED = 'table',
    pre_hook = ["{{ backup_table() }}"]
)
}}

with customers as(
    select * from {{ ref('stg_customers') }}
),

cleaned as(
    Select
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix as zip_code_prefix,
        Lower(customer_city) as customer_city,
        customer_state,
        CASE 
            WHEN Count(*) OVER (PARTITION BY customer_unique_id) > 1
            THEN 'Repeat Customer'
            ELSE 'New Customer'
        END as customer_type
    From customers
)

Select * From cleaned