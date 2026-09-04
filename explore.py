import duckdb
conn = duckdb.connect('dev.duckdb')

# print("=== CLEAN TABLES ===")
# conn.sql("SELECT table_name FROM duckdb_tables() WHERE table_name LIKE '%master%'").show()

# print("=== Order Reviews Columns ===")
# conn.sql("Describe stg_order_reviews").show()

# print("=== Row Counts ===")
# conn.sql("Select count(*) From stg_order_reviews").show()

# print("=== Review Score Distribution ===")
# conn.sql("""
#     Select
#         review_score,
#         count(*) as count
#     From stg_order_reviews
#     Group by review_score
#     Order by count desc
# """).show()

# print("=== Null Columns ===")
# conn.sql("""
#     Select
#         Sum(Case When review_id is null Then 1 Else 0 end) as null_order_id,
#         Sum(Case When order_id is null Then 1 Else 0 end) as null_order_id,
#         Sum(Case When review_score is null Then 1 Else 0 end) as null_review_score,
#         Sum(Case When review_comment_title is null Then 1 Else 0 end) as null_review_comment_title,
#         Sum(Case When review_comment_message is null Then 1 Else 0 end) as null_review_comment_message,
#         Sum(Case When review_creation_date is null Then 1 Else 0 end) as null_review_creation_date,
#         Sum(Case When review_answer_timestamp is null Then 1 Else 0 end) as null_review_answer_timestamp
#     From stg_order_reviews
# """).show()

# print("=== Duplicate Review ID ====")
# conn.sql("""
#     Select
#         review_id,
#         count(*) as count
#     From stg_order_reviews
#     group by review_id
#     having count(*) > 1
#     order by count desc
#     Limit 5
# """).show()

# print("=== Response Time Check ===")
# conn.sql("""
#     Select
#         Min(Datediff('day', review_creation_date, review_answer_timestamp)) as min_days,
#         Max(Datediff('day', review_creation_date, review_answer_timestamp)) as max_days,
#         ROUND(AVG(DATEDIFF('day', review_creation_date, review_answer_timestamp)), 2) as avg_days,
#         SUM(Case When review_creation_date > review_answer_timestamp Then 1 Else 0 end) as incorrect_dates
#     From stg_order_reviews
# """).show()

# print("=== CASE 1: Same review_id, Different order_id ===")
# conn.sql("""
#     SELECT review_id, COUNT(DISTINCT order_id) as distinct_orders
#     FROM olist_order_reviews_dataset
#     GROUP BY review_id
#     HAVING COUNT(DISTINCT order_id) > 1
#     ORDER BY distinct_orders DESC
#     LIMIT 10
# """).show()

# print("=== CASE 2: Same review_id, Same order_id (true duplicates) ===")
# conn.sql("""
#     SELECT review_id, order_id, COUNT(*) as count
#     FROM olist_order_reviews_dataset
#     GROUP BY review_id, order_id
#     HAVING COUNT(*) > 1
#     ORDER BY count DESC
#     LIMIT 10
# """).show()

# print("=== CASE 3: Same order_id, Different review_id ===")
# conn.sql("""
#     SELECT order_id, COUNT(DISTINCT review_id) as distinct_reviews
#     FROM olist_order_reviews_dataset
#     GROUP BY order_id
#     HAVING COUNT(DISTINCT review_id) > 1
#     ORDER BY distinct_reviews DESC
#     LIMIT 10
# """).show()

# print("=== CASE 4: Same order_id, Same review_id (identical rows) ===")
# conn.sql("""
#     SELECT order_id, review_id, COUNT(*) as count
#     FROM olist_order_reviews_dataset
#     GROUP BY order_id, review_id
#     HAVING COUNT(*) > 1
#     ORDER BY count DESC
#     LIMIT 10
# """).show()

# print("=== TOTAL COUNTS SUMMARY ===")
# conn.sql("""
#     SELECT
#         COUNT(*) as total_rows,
#         COUNT(DISTINCT review_id) as distinct_review_ids,
#         COUNT(DISTINCT order_id) as distinct_order_ids
#     FROM olist_order_reviews_dataset
# """).show()

print("=== MASTER TABLE ROW COUNT ===")
conn.sql("SELECT COUNT(*) as total FROM olist_master_table").show()

print("=== MASTER TABLE COLUMNS ===")
conn.sql("DESCRIBE olist_master_table").show()

print("=== SAMPLE DATA ===")
conn.sql("SELECT * FROM olist_master_table LIMIT 3").show()