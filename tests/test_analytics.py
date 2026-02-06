import pandas as pd

from src.validators import validate_products, validate_sales, ValidationError
from src.analytics import enrich_sales, kpi_summary


def _products_df():
    return pd.DataFrame([
        {"product_id": "B001", "product_name": "Croissant", "category": "Pastry", "unit_cost": 0.5, "unit_price": 2.0},
        {"product_id": "B002", "product_name": "Latte", "category": "Coffee", "unit_cost": 0.4, "unit_price": 3.0},
    ])


def test_profit_calculation():
    products = validate_products(_products_df())

    sales_raw = pd.DataFrame([
        {"date": "2026-01-01", "order_id": "O1", "product_id": "B001", "quantity": 2, "channel": "in_store", "discount_rate": 0.10},
    ])
    sales = validate_sales(sales_raw, products)
    enriched = enrich_sales(sales, products)

    # revenue = 2 * 2.0 * 0.9 = 3.6
    # cost = 2 * 0.5 = 1.0
    # profit = 2.6
    profit = float(enriched.loc[0, "profit"])
    assert round(profit, 2) == 2.60


def test_unknown_product_id_raises():
    products = validate_products(_products_df())

    sales_raw = pd.DataFrame([
        {"date": "2026-01-01", "order_id": "O1", "product_id": "X999", "quantity": 1, "channel": "in_store", "discount_rate": 0.0},
    ])

    try:
        validate_sales(sales_raw, products)
        assert False, "Expected ValidationError"
    except ValidationError:
        assert True


def test_kpi_summary_totals():
    products = validate_products(_products_df())

    sales_raw = pd.DataFrame([
        {"date": "2026-01-01", "order_id": "O1", "product_id": "B001", "quantity": 1, "channel": "in_store", "discount_rate": 0.0},
        {"date": "2026-01-01", "order_id": "O2", "product_id": "B002", "quantity": 1, "channel": "delivery", "discount_rate": 0.0},
    ])
    sales = validate_sales(sales_raw, products)
    enriched = enrich_sales(sales, products)

    kpi = kpi_summary(enriched).iloc[0].to_dict()
    # revenue = 2.0 + 3.0 = 5.0
    assert float(kpi["total_revenue"]) == 5.00
    assert int(kpi["total_orders"]) == 2