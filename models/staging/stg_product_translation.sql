with source as(

    select * from{{source('olist', 'product_category_name_translation')}}

),

product_translation as(
    SELECT
        product_category_name,
        product_category_name_english
    from source
)

Select * From product_translation