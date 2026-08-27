-- This test PASSES when 0 rows returned (table has data)
-- This test FAILS when 1 row returned (table is empty)

SELECT COUNT(*) as row_count
FROM {{ source('olist', 'olist_orders_dataset') }}
HAVING COUNT(*) = 0