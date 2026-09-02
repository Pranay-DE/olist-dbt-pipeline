{{ config(
    MATERIALIZED = 'table',
    pre_hook = [
        "Drop Table If EXISTS {{ this.name }}_backup",
        "Create TABLE {{ this.name }}_backup as Select * FROM {{ this.name }}"
    ]
)
}}

with product as(
    Select * from{{ref ('stg_products')}}
),

product_translation as(
    Select * From{{ref ('stg_product_translation')}}
),

cleaned as(
    SELECT
        p.product_id,
        COALESCE(t.product_category_name_english, p.product_category_name, 'Unknown') as product_category,
        product_name_lenght as product_name_length,
        product_description_lenght as product_description_length,
        product_photos_qty,
        product_weight_g,
        product_length_cm ,
        product_height_cm,
        product_width_cm,
        ROUND(product_length_cm * product_height_cm * product_width_cm, 2) as product_volume_cm3
        from product as p
        Left join product_translation as t
            on p.product_category_name = t.product_category_name
)

Select * From cleaned