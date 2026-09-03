{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If EXISTS {{ this.name }}_backup",
        "Create Table {{ this.name }}_backup as Select * From {{ this.name }}"
    ]
)
}}

with sellers as(
    Select * From {{ref('stg_sellers')}}
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