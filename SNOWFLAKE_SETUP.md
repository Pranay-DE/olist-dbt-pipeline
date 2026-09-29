# Snowflake Setup Guide

This document describes how the Snowflake environment for this project is created and configured. It's intended for anyone who wants to reproduce the pipeline on their own Snowflake account.

> ⚠️ This project was developed on a **Snowflake free trial**. If the trial has expired, the steps below reproduce the full environment in about 10 minutes.

---

## Prerequisites

- A Snowflake account (free trial works)
- `dbt-snowflake` installed locally
- The 9 Olist CSV files placed in `seeds/` (download from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce))

---

## Step 1: Create Database & Schemas

Run these SQL commands in the Snowflake SQL Editor:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS olist_warehouse;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS olist_warehouse.raw;
CREATE SCHEMA IF NOT EXISTS olist_warehouse.silver;
CREATE SCHEMA IF NOT EXISTS olist_warehouse.gold;

-- Verify
SHOW SCHEMAS IN DATABASE olist_warehouse;
```

Expected output — `RAW`, `SILVER`, `GOLD`, plus the default `PUBLIC` and `INFORMATION_SCHEMA`.

---

## Step 2: Create Compute Warehouse

```sql
-- Create compute warehouse (X-Small for cost efficiency)
CREATE WAREHOUSE IF NOT EXISTS compute_wh
  WAREHOUSE_SIZE = XSMALL
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

-- Verify
SHOW WAREHOUSES;
```

The `AUTO_SUSPEND = 60` setting means the warehouse shuts down after 60 seconds of inactivity, which keeps trial credits from draining between runs.

---

## Step 3: Configure dbt Profile

Create or update `~/.dbt/profiles.yml`:

```yaml
olist_dbt_pipeline:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_account_identifier>
      user: <your_username>
      password: <your_password>
      role: ACCOUNTADMIN
      database: olist_warehouse
      warehouse: COMPUTE_WH
      schema: raw
      threads: 4
      client_session_keep_alive: false
```

**Notes:**

- `account` — use the account identifier from your Snowflake URL. Both formats work: `<org>-<account>` (e.g. `abcdxy-12345`) or `<org>.<account>`.
- `user` / `password` — your Snowflake login credentials. These are never committed to the repo.
- `database` — lowercase `olist_warehouse` to match the DDL above.
- `schema` — set to `raw`; the custom `generate_schema_name` macro (see Step 6) routes models to their correct schemas regardless.
- `warehouse` — X-Small is sufficient; the full build takes ~11 minutes.

---

## Step 4: Test Connection

```bash
dbt debug
```

Expected output ends with:

```
Connection test: [OK connection ok]
All checks passed!
```

---

## Step 5: Load Seed Data

```bash
dbt seed
```

This creates 9 tables in `OLIST_WAREHOUSE.RAW`:

| Table | Rows |
|---|---|
| olist_customers_dataset | 99,441 |
| olist_geolocation_dataset | 1,000,163 |
| olist_order_items_dataset | 112,650 |
| olist_order_payments_dataset | 103,886 |
| olist_order_reviews_dataset | 99,224 |
| olist_orders_dataset | 99,441 |
| olist_products_dataset | 32,951 |
| olist_sellers_dataset | 3,095 |
| product_category_name_translation | 71 |

**Total: ~1.55M rows**

---

## Step 6: Build the Pipeline

```bash
dbt build
```

This will:

- Create **9 staging views** in `RAW`
- Create **7 cleaned tables** in `SILVER`
- Create **4 analytical tables** in `GOLD`
- Run **92 data quality tests**

Final output:

```
Done. PASS=121 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=121
```

(The 121 count includes 9 seeds + 9 staging views + 11 tables + 92 tests.)

---

## Schema Layout

```
OLIST_WAREHOUSE
├── RAW
│   ├── [9 seed tables from dbt seed]
│   ├── stg_customers            (view)
│   ├── stg_orders               (view)
│   ├── stg_order_items          (view)
│   ├── stg_order_payments       (view)
│   ├── stg_order_reviews        (view)
│   ├── stg_products             (view)
│   ├── stg_product_translation  (view)
│   ├── stg_sellers              (view)
│   └── stg_geolocation          (view)
│
├── SILVER
│   ├── customers_clean
│   ├── order_items_clean
│   ├── order_payments_clean
│   ├── order_reviews_clean
│   ├── orders_clean
│   ├── products_clean
│   └── sellers_clean
│
└── GOLD
    ├── olist_master_table
    ├── sales_performance
    ├── customer_behaviour
    └── delivery_performance
```

---

## Key Configurations

### 1. Custom Schema Routing — `macros/generate_schema_name.sql`

By default, dbt concatenates `target.schema` with the custom schema, producing names like `RAW_SILVER` and `RAW_GOLD`. This macro overrides that so models land exactly where intended:

```sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
```

### 2. Pre-Hook Backups — `macros/backup_table.sql`

Before each silver/gold table rebuild, a `<table>_backup` copy is created automatically, enabling instant rollback:

```sql
{% macro backup_table() %}
  {% if execute %}
    {% if adapter.get_relation(database=database, schema=schema, identifier=this.name) %}
      {% set sql %}
        DROP TABLE IF EXISTS {{ this.name }}_backup;
        CREATE TABLE {{ this.name }}_backup AS
        SELECT * FROM {{ this.name }};
      {% endset %}
      {% do run_query(sql) %}
    {% endif %}
  {% endif %}
{% endmacro %}
```

### 3. Materialization Strategy — `dbt_project.yml`

```yaml
models:
  olist_dbt_pipeline:
    staging:
      +schema: raw
      +materialized: view        # Lightweight, no storage
    silver:
      +schema: silver
      +materialized: table       # Persisted for performance
    gold:
      +schema: gold
      +materialized: table       # Final business layer
```

---

## Cost Estimation

Approximate Snowflake costs for this project (Standard Edition):

| Item | Value |
|---|---|
| Warehouse size | X-Small (1 credit/hour) |
| Credit price | ~$2–3 USD depending on region |
| Build time | ~11–12 minutes |
| Credits per build | ~0.2 |
| Cost per build | ~$0.40–0.60 |
| Trial credits | $400 (standard) |
| Builds covered by trial | ~700–1,000 |

After the trial, if you schedule the pipeline daily via Airflow, monthly cost is roughly **$12–18** at these rates.

---

## Troubleshooting

### "Account identifier not found"

Use the account identifier exactly as it appears in your Snowflake URL — typically `<org>-<account>` or `<org>.<account>`. Redact this value if you plan to commit the file publicly.

### "Invalid username or password"

- Username is case-sensitive — verify in the Snowflake console.
- Reset the password in Snowflake and update `profiles.yml`.

### "Schema does not exist"

Re-run the DDL from Step 1:

```sql
CREATE SCHEMA IF NOT EXISTS olist_warehouse.silver;
CREATE SCHEMA IF NOT EXISTS olist_warehouse.gold;
```

### Models land in `RAW_SILVER` / `RAW_GOLD`

The `generate_schema_name` macro is missing or not being loaded. Confirm `macros/generate_schema_name.sql` exists and re-run `dbt build`.

### Warehouse not starting

Check the warehouse state:

```sql
SHOW WAREHOUSES;
```

If `state` is `SUSPENDED`, it will resume automatically on the next query (`AUTO_RESUME = TRUE`).

---

## Useful Snowflake Queries

```sql
-- Tables per schema
SELECT TABLE_SCHEMA, TABLE_NAME
FROM OLIST_WAREHOUSE.INFORMATION_SCHEMA.TABLES
ORDER BY TABLE_SCHEMA, TABLE_NAME;

-- Table sizes
SELECT TABLE_NAME, ROW_COUNT, BYTES / 1024 / 1024 AS SIZE_MB
FROM OLIST_WAREHOUSE.INFORMATION_SCHEMA.TABLE_STORAGE_METRICS
WHERE TABLE_SCHEMA = 'SILVER'
ORDER BY BYTES DESC;

-- Recent queries
SELECT QUERY_TEXT, START_TIME, TOTAL_ELAPSED_TIME
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
ORDER BY START_TIME DESC
LIMIT 10;

-- Warehouse credit usage (last 7 days)
SELECT DATE_TRUNC('DAY', START_TIME) AS DAY,
       WAREHOUSE_NAME,
       SUM(CREDITS_USED) AS CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME >= DATEADD('DAY', -7, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY 1 DESC;
```

---

## Next Steps

After confirming all models are built:

1. Capture screenshots of the schemas and gold-layer query results for the portfolio
2. Document row counts per layer
3. Add Airflow + Astronomer Cosmos orchestration on top of this dbt project

---

## Resources

- [Snowflake Documentation](https://docs.snowflake.com)
- [dbt Snowflake Adapter](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup)
- [Snowflake Free Trial](https://signup.snowflake.com/)