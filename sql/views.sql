USE sales_bi;

CREATE OR REPLACE VIEW v_daily_kpis AS
SELECT
  order_date,
  COUNT(DISTINCT order_id) AS orders,
  COUNT(DISTINCT customer_id) AS customers,
  ROUND(SUM(sales), 2) AS revenue,
  ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS aov
FROM orders
GROUP BY order_date;

CREATE OR REPLACE VIEW v_top_products AS
SELECT
  oi.product_id,
  p.product_name,
  SUM(oi.quantity) AS units,
  ROUND(SUM(oi.sales), 2) AS revenue
FROM order_items oi
LEFT JOIN products p ON p.product_id = oi.product_id
GROUP BY oi.product_id, p.product_name;

CREATE OR REPLACE VIEW v_customer_rfm AS
SELECT
  o.customer_id,
  MAX(o.order_date) AS last_order_date,
  DATEDIFF((SELECT MAX(order_date) FROM orders), MAX(o.order_date)) AS recency_days,
  COUNT(DISTINCT o.order_id) AS frequency_orders,
  ROUND(SUM(o.sales), 2) AS monetary_revenue
FROM orders o
WHERE o.customer_id IS NOT NULL
GROUP BY o.customer_id;
