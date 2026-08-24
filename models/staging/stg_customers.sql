with source AS(

    select * from {{source('olist', 'olist_customers_dataset')}}

),

customers as (

    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    from source
)

Select * From customers