# BakeShop Insights — Sales & Profit Analyzer (Python + Pandas)

A command-line tool that analyses a bakery’s sales data from CSV files and generates KPI summaries,
daily performance tables, channel comparisons, and top-product rankings.
This project was built as a practical portfolio project to demonstrate entry-level IT and data analysis skills.

## Features
- Reads `sales.csv` and `products.csv`
- Validates data quality (dates, numeric fields, product_id matching, etc.)
- Calculates revenue, cost, profit, and profit margin
- Outputs:
  - `outputs/kpi_summary.csv`
  - `outputs/daily_summary.csv`
  - `outputs/top_products.csv`
  - `outputs/channel_summary.csv`
  - `outputs/report.txt`

## Data format

### products.csv
Columns:
- product_id, product_name, category, unit_cost, unit_price

### sales.csv
Columns:
- date (YYYY-MM-DD), order_id, product_id, quantity, channel, discount_rate (0–1)

See examples in `data/`.

## How to run

### 1) Install dependencies

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
```
### 2) Run the analysis

```bash
python -m src.main --sales data/sample_sales.csv --products data/sample_products.csv
```
