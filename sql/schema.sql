CREATE DATABASE IF NOT EXISTS sales_bi;
USE sales_bi;

-- Customers
CREATE TABLE IF NOT EXISTS customers (
  customer_id INT PRIMARY KEY,
  customer_name VARCHAR(255),
  segment VARCHAR(100),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  created_at DATE
);

-- Products
CREATE TABLE IF NOT EXISTS products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(255),
  category VARCHAR(100),
  sub_category VARCHAR(100)
);

-- Orders (header)
CREATE TABLE IF NOT EXISTS orders (
  order_id VARCHAR(50) PRIMARY KEY,
  order_date DATE,
  ship_date DATE,
  ship_mode VARCHAR(100),
  customer_id INT,
  region VARCHAR(100),
  sales DECIMAL(12,2),
  discount DECIMAL(6,3),
  profit DECIMAL(12,2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Order line items (optional but useful for detailed analytics)
CREATE TABLE IF NOT EXISTS order_items (
  order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id VARCHAR(50),
  product_id INT,
  quantity INT,
  sales DECIMAL(12,2),
  discount DECIMAL(6,3),
  profit DECIMAL(12,2),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Helpful indexes
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_items_product ON order_items(product_id);
