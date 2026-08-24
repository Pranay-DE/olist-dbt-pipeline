with source as(

    select * from{{source('olist', 'olist_order_payments_dataset')}}

),

order_payments as(
    select
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value
    from source
)

Select * From order_payments