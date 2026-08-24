with source as(

    select * from {{ source('olist', 'olist_geolocation_dataset')}}

),

geolocation as(
    SELECT
        geolocation_zip_code_prefix,
        geolocation_lat,
        geolocation_lng,
        geolocation_city,
        geolocation_state
    from source
)

select * from geolocation