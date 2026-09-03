# Olist E-Commerce dbt Pipeline

## Overview
End-to-end ELT pipeline transforming raw Brazilian e-commerce data 
from Olist through Bronze → Silver → Gold layers using dbt and DuckDB.

## Architecture
- **Staging (Bronze):** Raw source tables declared and lightly cleaned
- **Silver:** Cleaned, joined, and enriched business models  
- **Gold:** Final business-ready models for reporting and analysis

## Dataset
[Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- 100,000 orders from 2016 to 2018
- 9 source tables covering orders, customers, products, sellers, reviews

## Tech Stack
- **dbt Core** — transformation and modelling
- **DuckDB** — local analytical database
- **Python** — data loading from CSV sources

## Project Structure
models/
- staging/ ← views, one per source table
- silver/ ← cleaned and joined tables
- gold/ ← business ready final models

## Silver Layer Models

| Model | Source | Key Transformations |
|-------|--------|---------------------|
| orders_clean | stg_orders | Delivery metrics, fiscal year, date validation |
| customers_clean | stg_customers | City standardisation, repeat customer flag |
| order_items_clean | stg_order_items | Deduplication, price categories, freight analysis |
| products_clean | stg_products + translation | English category names, volume calculation |
| order_payments_clean | stg_order_payments | Payment type standardisation, installment categories |
| sellers_clean | stg_sellers | Column renaming, city normalisation |
| order_reviews_clean | stg_order_reviews | Sentiment analysis, response time, deduplication |

## Data Quality
- **67 tests** across staging and silver layers — all passing
- Source freshness checks on all 9 raw tables
- Custom tests for business logic validation
- Pre-hook backup on every silver model for recovery

## How to Run
1. Install dependencies: `pip install dbt-duckdb`
2. Download Olist dataset from Kaggle and place CSVs in `raw_data/`
3. Load source data: `python load_data.py`
4. Run all models: `dbt build`
5. View documentation: `dbt docs generate && dbt docs serve`

## Status
🟡 In Progress — Staging and Silver layers complete, Gold layer in development

### Completed
- ✅ Staging layer — 9 models
- ✅ Silver layer — 7 models, 67 tests
- ✅ Pre-hook backup strategy on all silver models
- ✅ Source validation tests

### In Progress
- 🚧 Gold layer — sales performance, customer behaviour, delivery analysis
