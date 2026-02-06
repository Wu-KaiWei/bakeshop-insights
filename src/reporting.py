from __future__ import annotations

import pandas as pd


def _fmt_money(x: float) -> str:
    return f"£{x:,.2f}"


def build_text_report(
    kpi: pd.DataFrame,
    daily: pd.DataFrame,
    channel: pd.DataFrame,
    top: pd.DataFrame,
) -> str:
    k = kpi.iloc[0].to_dict()

    lines: list[str] = []
    lines.append("BakeShop Insights — Sales & Profit Report")
    lines.append("=" * 44)
    lines.append("")
    lines.append("Overall KPI")
    lines.append("-" * 11)
    lines.append(f"Total revenue:   {_fmt_money(float(k['total_revenue']))}")
    lines.append(f"Total cost:      {_fmt_money(float(k['total_cost']))}")
    lines.append(f"Total profit:    {_fmt_money(float(k['total_profit']))}")
    lines.append(f"Profit margin:   {float(k['profit_margin'])*100:.2f}%")
    lines.append(f"Total orders:    {int(k['total_orders'])}")
    lines.append(f"Items sold:      {int(k['total_items_sold'])}")
    lines.append("")
    lines.append("Channel summary (revenue desc)")
    lines.append("-" * 29)
    for _, r in channel.iterrows():
        lines.append(
            f"{r['channel']:<10} | orders={int(r['orders']):>3} | items={int(r['items_sold']):>3} | "
            f"revenue={_fmt_money(float(r['revenue']))} | profit={_fmt_money(float(r['profit']))}"
        )

    lines.append("")
    lines.append("Top products by profit")
    lines.append("-" * 22)
    top_profit = top[top["rank_type"] == "top_profit"].head(5)
    for _, r in top_profit.iterrows():
        lines.append(
            f"{r['product_name']:<18} | {r['category']:<7} | sold={int(r['items_sold']):>3} | "
            f"profit={_fmt_money(float(r['profit']))}"
        )

    lines.append("")
    lines.append("Daily summary (first 5 rows)")
    lines.append("-" * 28)
    for _, r in daily.head(5).iterrows():
        lines.append(
            f"{r['date']} | orders={int(r['orders']):>3} | revenue={_fmt_money(float(r['revenue']))} | "
            f"profit={_fmt_money(float(r['profit']))} | margin={float(r['profit_margin'])*100:.2f}%"
        )

    lines.append("")
    return "\n".join(lines)