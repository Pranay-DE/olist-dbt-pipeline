{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop TABLE IF EXISTS {{this.name}}_backup",
        "CREATE TABLE {{this.name}}_backup as SELECT * FROM {{this.name}}"
    ]
)
}}

with payments as(
    Select * from {{ref('stg_order_payments')}}
),

cleaned as(
    Select
        order_id,
        payment_sequential,
        Case
            When payment_type = 'not_defined' THEN 'unknown'
            Else payment_type
        End as payment_type,
        payment_installments,
        CASE 
            WHEN payment_installments = 0 THEN 'Not Applicable'
            WHEN payment_installments = 1 THEN 'Full Payment'
            WHEN payment_installments <= 6 THEN 'Short Term'
            ELSE 'Long Term'
        END as payment_installment_type,
        payment_value,
        CASE
            WHEN payment_value < 1   THEN 'Near Zero'
            WHEN payment_value < 50  THEN 'Low'
            WHEN payment_value < 200 THEN 'Medium'
            ELSE 'High'
        END as payment_value_category
    From payments
)

Select * from cleaned