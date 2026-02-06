from __future__ import annotations

import argparse
from pathlib import Path

from src.io_utils import read_csv, write_csv, write_text, ensure_dir
from src.validators import validate_products, validate_sales, ValidationError
from src.analytics import enrich_sales, kpi_summary, daily_summary, top_products, channel_summary
from src.reporting import build_text_report


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="BakeShop Insights — analyse bakery sales from CSV files.")
    p.add_argument("--sales", required=True, help="Path to sales CSV (e.g. data/sample_sales.csv)")
    p.add_argument("--products", required=True, help="Path to products CSV (e.g. data/sample_products.csv)")
    p.add_argument("--outdir", default="outputs", help="Output directory (default: outputs)")
    p.add_argument("--topn", type=int, default=10, help="Top N products for rankings (default: 10)")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    outdir = ensure_dir(args.outdir)

    try:
        products_raw = read_csv(args.products)
        sales_raw = read_csv(args.sales)

        products = validate_products(products_raw)
        sales = validate_sales(sales_raw, products)

        enriched = enrich_sales(sales, products)

        kpi = kpi_summary(enriched)
        daily = daily_summary(enriched)
        top = top_products(enriched, n=args.topn)
        channel = channel_summary(enriched)

        write_csv(kpi, outdir / "kpi_summary.csv")
        write_csv(daily, outdir / "daily_summary.csv")
        write_csv(top, outdir / "top_products.csv")
        write_csv(channel, outdir / "channel_summary.csv")

        report_text = build_text_report(kpi, daily, channel, top)
        write_text(report_text, outdir / "report.txt")

        print(f"✅ Done. Outputs written to: {Path(outdir).resolve()}")
        return 0

    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        return 2
    except ValidationError as e:
        print(f"❌ Data validation error: {e}")
        return 3
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())