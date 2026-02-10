from sqlalchemy import text
from src.config import get_engine

def run(engine):
    with engine.begin() as conn:
        conn.execute(text("USE sales_bi;"))

        # rerun-safe reset
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
        conn.execute(text("TRUNCATE TABLE order_items;"))
        conn.execute(text("TRUNCATE TABLE orders;"))
        conn.execute(text("TRUNCATE TABLE products;"))
        conn.execute(text("TRUNCATE TABLE customers;"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

        # 1) Customers: ONE row per CustomerID
        # - created_at: first purchase date
        # - country: most frequent country for that customer (fallback to any)
        conn.execute(text("""
            INSERT INTO customers (customer_id, customer_name, segment, city, state, country, created_at)
            SELECT
                r.CustomerID AS customer_id,
                NULL AS customer_name,
                NULL AS segment,
                NULL AS city,
                NULL AS state,
                c.country AS country,
                r.first_date AS created_at
            FROM
                (SELECT CustomerID, MIN(DATE(InvoiceDate)) AS first_date
                 FROM retail_raw
                 WHERE CustomerID IS NOT NULL
                 GROUP BY CustomerID) r
            LEFT JOIN
                (SELECT CustomerID, Country AS country
                 FROM (
                     SELECT CustomerID, Country,
                            ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY COUNT(*) DESC) AS rn
                     FROM retail_raw
                     WHERE CustomerID IS NOT NULL
                     GROUP BY CustomerID, Country
                 ) t
                 WHERE rn = 1) c
            ON r.CustomerID = c.CustomerID;
        """))

        # 2) Products
        conn.execute(text("""
            INSERT INTO products (product_id, product_name, category, sub_category)
            SELECT
                StockCode AS product_id,
                MAX(NULLIF(Description, 'nan')) AS product_name,
                NULL AS category,
                NULL AS sub_category
            FROM retail_raw
            WHERE StockCode IS NOT NULL
            GROUP BY StockCode;
        """))

        # 3) Orders
        conn.execute(text("""
            INSERT INTO orders (order_id, order_date, ship_date, ship_mode, customer_id, region, sales, discount, profit)
            SELECT
                InvoiceNo AS order_id,
                DATE(MIN(InvoiceDate)) AS order_date,
                NULL AS ship_date,
                NULL AS ship_mode,
                MAX(CustomerID) AS customer_id,
                Country AS region,
                ROUND(SUM(LineSales), 2) AS sales,
                0.000 AS discount,
                NULL AS profit
            FROM retail_raw
            GROUP BY InvoiceNo, Country;
        """))

        # 4) Order Items
        conn.execute(text("""
            INSERT INTO order_items (order_id, product_id, quantity, sales, discount, profit)
            SELECT
                InvoiceNo AS order_id,
                StockCode AS product_id,
                CAST(Quantity AS SIGNED) AS quantity,
                ROUND(LineSales, 2) AS sales,
                0.000 AS discount,
                NULL AS profit
            FROM retail_raw;
        """))

    print("✅ Transformed retail_raw into customers/products/orders/order_items")

def main():
    engine = get_engine()
    run(engine)

if __name__ == "__main__":
    main()
