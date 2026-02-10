from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.config import get_engine

def export_query(conn, sql: str, out_path: Path):
    df = pd.read_sql_query(text(sql), conn)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"✅ Wrote: {out_path.resolve()}")
    print(f"   Rows: {len(df):,}")

def main():
    root = Path(__file__).resolve().parents[1]  # repo root
    out_dir = root / "data" / "processed"
    print(f"Repo root detected as: {root}")
    print(f"Output folder: {out_dir.resolve()}")

    engine = get_engine()

    with engine.connect() as conn:
        conn.execute(text("USE sales_bi;"))

        export_query(conn, """
            SELECT
              order_date,
              COUNT(DISTINCT order_id) AS orders,
              COUNT(DISTINCT customer_id) AS customers,
              ROUND(SUM(sales), 2) AS revenue,
              ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
            FROM orders
            WHERE order_id NOT LIKE 'C%'
              AND sales > 0
            GROUP BY order_date
            ORDER BY order_date;
        """, out_dir / "daily_kpis.csv")

        export_query(conn, """
            SELECT
              oi.product_id,
              COALESCE(p.product_name, '') AS product_name,
              SUM(oi.quantity) AS units,
              ROUND(SUM(oi.sales), 2) AS revenue
            FROM order_items oi
            LEFT JOIN products p ON p.product_id = oi.product_id
            WHERE oi.order_id NOT LIKE 'C%'
              AND oi.quantity > 0
              AND oi.sales > 0
            GROUP BY oi.product_id, p.product_name
            ORDER BY revenue DESC;
        """, out_dir / "top_products.csv")

        export_query(conn, """
            SELECT
              customer_id,
              MAX(order_date) AS last_order_date,
              DATEDIFF(
                (SELECT MAX(order_date)
                 FROM orders
                 WHERE order_id NOT LIKE 'C%'
                   AND sales > 0),
                MAX(order_date)
              ) AS recency_days,
              COUNT(DISTINCT order_id) AS frequency_orders,
              ROUND(SUM(sales), 2) AS monetary_revenue
            FROM orders
            WHERE order_id NOT LIKE 'C%'
              AND sales > 0
              AND customer_id IS NOT NULL
            GROUP BY customer_id
            ORDER BY monetary_revenue DESC;
        """, out_dir / "customer_rfm.csv")

if __name__ == "__main__":
    main()
