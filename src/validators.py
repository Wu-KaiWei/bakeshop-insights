from __future__ import annotations

import pandas as pd


class ValidationError(ValueError):
    pass


REQUIRED_PRODUCTS_COLS = {"product_id", "product_name", "category", "unit_cost", "unit_price"}
REQUIRED_SALES_COLS = {"date", "order_id", "product_id", "quantity", "channel", "discount_rate"}


def _require_columns(df: pd.DataFrame, required: set[str], name: str) -> None:
    missing = required - set(df.columns)
    if missing:
        raise ValidationError(f"{name} missing columns: {sorted(missing)}")


def validate_products(products: pd.DataFrame) -> pd.DataFrame:
    _require_columns(products, REQUIRED_PRODUCTS_COLS, "products")

    df = products.copy()

    # types
    for col in ["unit_cost", "unit_price"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df["product_id"].isna().any():
        raise ValidationError("products has missing product_id")

    if df["unit_cost"].isna().any() or df["unit_price"].isna().any():
        raise ValidationError("products has non-numeric unit_cost/unit_price")

    if (df["unit_cost"] < 0).any() or (df["unit_price"] < 0).any():
        raise ValidationError("products has negative unit_cost/unit_price")

    # unique product_id
    if df["product_id"].duplicated().any():
        dups = df.loc[df["product_id"].duplicated(), "product_id"].tolist()
        raise ValidationError(f"products has duplicated product_id: {dups}")

    return df


def validate_sales(sales: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    _require_columns(sales, REQUIRED_SALES_COLS, "sales")

    df = sales.copy()

    # parse date
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    if df["date"].isna().any():
        raise ValidationError("sales has invalid date format; expected YYYY-MM-DD")

    # numeric
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["discount_rate"] = pd.to_numeric(df["discount_rate"], errors="coerce")

    if df["quantity"].isna().any():
        raise ValidationError("sales has non-numeric quantity")
    if df["discount_rate"].isna().any():
        raise ValidationError("sales has non-numeric discount_rate")

    if (df["quantity"] < 0).any():
        raise ValidationError("sales has negative quantity")

    if (df["discount_rate"] < 0).any() or (df["discount_rate"] > 1).any():
        raise ValidationError("sales discount_rate must be between 0 and 1")

    # product_id existence
    product_ids = set(products["product_id"].astype(str).tolist())
    missing = sorted(set(df["product_id"].astype(str).tolist()) - product_ids)
    if missing:
        raise ValidationError(f"sales has unknown product_id(s): {missing}")

    # basic string cols
    if df["order_id"].isna().any():
        raise ValidationError("sales has missing order_id")
    if df["channel"].isna().any():
        raise ValidationError("sales has missing channel")

    return df