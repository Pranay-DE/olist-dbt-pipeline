import duckdb
conn = duckdb.connect('dev.duckdb')

# print("=== Products Columns ===")
# conn.sql("Describe stg_products").show()

# print("=== Row Count ===")
# conn.sql("Select Count(*) as total From stg_products").show()

# print("=== Null Check ===")
# conn.sql("""
#     Select
#         Sum(Case when product_id is null then 1 else 0 end) as null_product_id,
#         Sum(Case when product_category_name is null then 1 else 0 end) as null_product_category_name,
#         Sum(Case when product_name_lenght is null then 1 else 0 end) as null_product_name_lenght,
#         Sum(Case when product_description_lenght is null then 1 else 0 end) as null_product_description_lenght,
#         Sum(Case when product_photos_qty is null then 1 else 0 end) as null_product_photos_qty,
#         Sum(Case when product_weight_g is null then 1 else 0 end) as null_product_weight_g,
#         Sum(Case when product_length_cm  is null then 1 else 0 end) as null_product_length_cm ,
#         Sum(Case when product_height_cm is null then 1 else 0 end) as null_product_height_cm,
#         Sum(Case when product_width_cm is null then 1 else 0 end) as null_product_width_cm
#     From stg_products
# """).show()

# print("=== Translation Table ===")
# conn.sql("Describe stg_product_translation").show()

# print("=== Categories not in translation ===")
# conn.sql("""
#     Select p.product_category_name, count(*) as product_count
#     From stg_products as p
#     Left Join stg_product_translation as t
#     on p.product_category_name = t.product_category_name
#     Where t.product_category_name is null
#     Group by p.product_category_name
#     order by product_count Desc
# """).show()

conn.sql("Select table_name From duckdb_tables() where table_name LIKE '%clean%'").show()