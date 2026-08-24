with source as(

    select * from{{source('olist', 'olist_order_reviews_dataset')}}

),

order_reviews as(
    SELECT
        review_id,
        order_id,
        review_score,
        review_comment_title,
        review_comment_message,
        review_creation_date,
        review_answer_timestamp
    from source
)

Select * From order_reviews