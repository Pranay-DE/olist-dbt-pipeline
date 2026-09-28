{{ config(
    MATERIALIZED = 'table',
    pre_hook = ["{{ backup_table() }}"]
)
}}

with sellers as(
    Select * From {{ ref('stg_sellers') }}
),

cleaned as(
    SELECT
        seller_id,
        seller_zip_code_prefix as zip_code_prefix,
        lower(seller_city) as city,
        seller_state as state
    From sellers
)

Select * From cleaned