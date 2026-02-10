from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.config import get_engine

OUT_DIR = Path("data/outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def q(conn, sql: str):
    return conn.execute(text(sql)).fetchone()

def main():
    engine = get_engine()

    with engine.connect() as conn:
        conn.execute(text("USE sales_bi;"))

        total_rows = q(conn, "SELECT COUNT(*) FROM retail_raw;")[0]
        distinct_invoices = q(conn, "SELECT COUNT(DISTINCT InvoiceNo) FROM retail_raw;")[0]
        distinct_customers = q(conn, "SELECT COUNT(DISTINCT CustomerID) FROM retail_raw WHERE CustomerID IS NOT NULL;")[0]
        distinct_products = q(conn, "SELECT COUNT(DISTINCT StockCode) FROM retail_raw;")[0]
        missing_customer = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE CustomerID IS NULL;")[0]
        cancellations = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE InvoiceNo LIKE 'C%';")[0]
        negative_qty = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE Quantity < 0;")[0]
        zero_qty = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE Quantity = 0;")[0]
        negative_price = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE UnitPrice < 0;")[0]
        null_dates = q(conn, "SELECT COUNT(*) FROM retail_raw WHERE InvoiceDate IS NULL;")[0]

        min_date = q(conn, "SELECT MIN(InvoiceDate) FROM retail_raw;")[0]
        max_date = q(conn, "SELECT MAX(InvoiceDate) FROM retail_raw;")[0]

        # Top countries
        top_countries = conn.execute(text("""
            SELECT Country, COUNT(*) AS rows_cnt
            FROM retail_raw
            GROUP BY Country
            ORDER BY rows_cnt DESC
            LIMIT 10;
        """)).fetchall()

        # Top products by revenue
        top_products = conn.execute(text("""
            SELECT StockCode, MAX(Description) AS Description, ROUND(SUM(LineSales), 2) AS Revenue
            FROM retail_raw
            GROUP BY StockCode
            ORDER BY Revenue DESC
            LIMIT 10;
        """)).fetchall()

    # Build report rows
    report = [
        ("total_rows", total_rows),
        ("distinct_invoices", distinct_invoices),
        ("distinct_customers_non_null", distinct_customers),
        ("distinct_products", distinct_products),
        ("missing_customer_rows", missing_customer),
        ("missing_customer_pct", round(missing_customer * 100 / total_rows, 2)),
        ("cancellation_rows", cancellations),
        ("cancellation_pct", round(cancellations * 100 / total_rows, 2)),
        ("negative_quantity_rows", negative_qty),
        ("negative_quantity_pct", round(negative_qty * 100 / total_rows, 2)),
        ("zero_quantity_rows", zero_qty),
        ("negative_price_rows", negative_price),
        ("null_invoice_date_rows", null_dates),
        ("date_range_start", str(min_date)),
        ("date_range_end", str(max_date)),
    ]

    df = pd.DataFrame(report, columns=["metric", "value"])
    out_path = OUT_DIR / "data_quality_report.csv"
    df.to_csv(out_path, index=False)

    # Save top lists too (nice for GitHub)
    pd.DataFrame(top_countries, columns=["country", "rows"]).to_csv(OUT_DIR / "top_countries.csv", index=False)
    pd.DataFrame(top_products, columns=["stock_code", "description", "revenue"]).to_csv(OUT_DIR / "top_products.csv", index=False)

    print(f"✅ Saved: {out_path}")
    print("✅ Saved: data/outputs/top_countries.csv")
    print("✅ Saved: data/outputs/top_products.csv")

if __name__ == "__main__":
    main()
