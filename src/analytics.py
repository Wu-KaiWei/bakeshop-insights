from __future__ import annotations

import pandas as pd


def enrich_sales(sales: pd.DataFrame, products: pd.DataFrame) -> pd.DataFrame:
    """
    Merge sales with product info and compute revenue/cost/profit.
    """
    df = sales.merge(products, on="product_id", how="left")

    # compute metrics
    df["gross_revenue"] = df["quantity"] * df["unit_price"]
    df["revenue"] = df["gross_revenue"] * (1 - df["discount_rate"])
    df["cost"] = df["quantity"] * df["unit_cost"]
    df["profit"] = df["revenue"] - df["cost"]

    return df


def kpi_summary(enriched: pd.DataFrame) -> pd.DataFrame:
    total_revenue = float(enriched["revenue"].sum())
    total_cost = float(enriched["cost"].sum())
    total_profit = float(enriched["profit"].sum())
    margin = (total_profit / total_revenue) if total_revenue else 0.0

    total_orders = int(enriched["order_id"].nunique())
    total_items = float(enriched["quantity"].sum())

    return pd.DataFrame(
        [{
            "total_revenue": round(total_revenue, 2),
            "total_cost": round(total_cost, 2),
            "total_profit": round(total_profit, 2),
            "profit_margin": round(margin, 4),
            "total_orders": total_orders,
            "total_items_sold": round(total_items, 0),
        }]
    )


def daily_summary(enriched: pd.DataFrame) -> pd.DataFrame:
    grp = enriched.groupby("date", as_index=False).agg(
        orders=("order_id", "nunique"),
        items_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        cost=("cost", "sum"),
        profit=("profit", "sum"),
    )
    grp["profit_margin"] = grp.apply(lambda r: (r["profit"] / r["revenue"]) if r["revenue"] else 0.0, axis=1)
    for col in ["revenue", "cost", "profit"]:
        grp[col] = grp[col].round(2)
    grp["profit_margin"] = grp["profit_margin"].round(4)
    grp["items_sold"] = grp["items_sold"].round(0)
    return grp.sort_values("date")


def top_products(enriched: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    grp = enriched.groupby(["product_id", "product_name", "category"], as_index=False).agg(
        items_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    grp["revenue"] = grp["revenue"].round(2)
    grp["profit"] = grp["profit"].round(2)
    grp["items_sold"] = grp["items_sold"].round(0)

    by_profit = grp.sort_values(["profit", "revenue"], ascending=False).head(n).copy()
    by_profit.insert(0, "rank_type", "top_profit")

    by_sold = grp.sort_values(["items_sold", "revenue"], ascending=False).head(n).copy()
    by_sold.insert(0, "rank_type", "top_sold")

    return pd.concat([by_profit, by_sold], ignore_index=True)


def channel_summary(enriched: pd.DataFrame) -> pd.DataFrame:
    grp = enriched.groupby("channel", as_index=False).agg(
        orders=("order_id", "nunique"),
        items_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
    )
    grp["revenue"] = grp["revenue"].round(2)
    grp["profit"] = grp["profit"].round(2)
    grp["items_sold"] = grp["items_sold"].round(0)
    return grp.sort_values("revenue", ascending=False)