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
├── staging/ ← views, one per source table
├── silver/ ← cleaned and joined tables
└── gold/ ← business ready final models

## How to Run
1. Install dependencies: `pip install dbt-duckdb`
2. Load source data: `python load_data.py`
3. Run all models: `dbt run`
4. Run tests: `dbt test`

## Status
🚧 In Progress — Staging layer complete, Silver layer in development
