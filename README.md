# Sales Intelligence BI Suite (Tableau + MySQL + Python)

End-to-end BI reporting project that converts raw transactional data into curated analytics tables and Tableau dashboards.  
Built to demonstrate **data analysis, database management, automation, reporting, and data visualization** skills for roles like **Data Visualization & Database Specialist**.

---

## Why this project

Many teams still rely on manual Excel reporting and inconsistent KPI definitions. This leads to:
- slow reporting cycles
- duplicate / missing records
- mismatched KPI numbers across teams
- dashboards that are hard to maintain

This project builds a repeatable pipeline:
**Raw Excel → Python cleaning/validation → MySQL warehouse tables → curated extracts → Tableau dashboards**.

---

## What this helps with (business + skills)

**Business use-cases**
- Executive KPI tracking (revenue, orders, customers, AOV)
- Product performance benchmarking (top revenue/units products)
- Customer/account review (RFM-style segmentation signals)
- Data quality monitoring (missing IDs, cancellations, returns)

**Skills demonstrated**
- Data cleaning + profiling (Python/pandas)
- Relational modeling + SQL (MySQL)
- Automated reporting extracts (Python → CSV)
- Dashboard design + communication (Tableau Public)
- Documentation and reproducible workflow (GitHub-ready repo)

---

## Tech Stack

- **Python**: pandas, SQLAlchemy, PyMySQL, python-dotenv
- **MySQL**: schema design, ETL staging, KPI queries
- **Tableau Public**: dashboards built from curated extracts
- **Excel** dataset ingestion with openpyxl

---

## Dataset

**Online Retail (Excel)** — transactional sales dataset (InvoiceNo, StockCode, Quantity, UnitPrice, CustomerID, Country).  
Source: UCI “Online Retail” dataset (also available via Kaggle mirrors).

File used: `data/raw/Online Retail.xlsx`

---

## Data Quality Highlights (from `data/outputs/data_quality_report.csv`)

- **Rows processed:** 541,909  
- **Invoices:** 25,900  
- **Customers (non-null):** 4,372  
- **Products:** 3,958  
- **Missing CustomerID:** 135,080 (**24.93%**)  
- **Cancellations (InvoiceNo starts with “C”):** 9,288 (**1.71%**)  
- **Negative quantity rows (returns):** 10,624 (**1.96%**)  
- **Date range:** 2010-12-01 → 2011-12-09  

This project keeps the **raw staging layer** and produces **clean extracts** (excluding cancellations and non-positive sales) for reporting.

---

## Architecture

1) **Extract & Stage**
- Load Excel into MySQL staging table: `retail_raw`

2) **Transform**
- Populate BI tables: `customers`, `products`, `orders`, `order_items`

3) **Validate / Profile**
- Generate data quality and top lists in `data/outputs/`

4) **Publish Extracts**
- Export curated datasets for Tableau Public to `data/processed/`

5) **Visualize**
- Build interactive dashboards in Tableau Public from CSV extracts

> Note: Tableau Public does not support all database connectors in the same way as Tableau Desktop.  
> For portability and reproducibility, this project publishes **curated CSV extracts** generated from MySQL.

---

## Repo Structure

sales-bi-tableau-mysql-python/
│── README.md
│── data/
│   ├── raw/                 # original dataset
│   ├── processed/           # cleaned CSVs
│── sql/
│   ├── schema.sql           # tables
│   ├── views.sql            # KPI views
│   ├── indexes.sql
│── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_clean_validate.ipynb
│── src/
│   ├── extract_load.py
│   ├── transform_clean.py
│   ├── validate_quality.py
│   ├── refresh_pipeline.py
│── dashboards/
│   ├── tableau_dashboard_screenshots/
│   ├── tableau_workbook_link.txt
│── docs/
│   ├── kpi_definitions.md
│   ├── data_dictionary.md
│   ├── user_guide.md
│── requirements.txt
│── .env.example



---

## How to Run (End-to-End)

### 1) Setup environment
Create/activate your environment and install dependencies:
```bash
pip install -r requirements.txt
```

1) Create .env in repo root:

MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD
MYSQL_DB=sales_bi

2) Create MySQL tables

Run sql/schema.sql in MySQL Workbench (or via CLI).

3) Load raw Excel into MySQL
```bash
python -m src.extract_load
```

4) Transform into BI tables
```bash
python -m src.transform_clean
```
5) Generate data quality outputs
```bash
python -m src.validate_quality
```

6) Export curated datasets for Tableau Public
```bash
python -m src.export_for_tableau
```

Outputs:

data/processed/daily_kpis.csv

data/processed/top_products.csv

data/processed/customer_rfm.csv

## Dashboards (Tableau Public)

Built using the curated extracts in data/processed/.

Dashboard 1 — Executive KPI Overview

Revenue, Orders, Customers, AOV

Revenue trend over time

Dashboard 2 — Product Performance

Top products by revenue and units

Product benchmarking table

Dashboard 3 — Customer / Account Review

Frequency vs Monetary scatter

Recency distribution

Customer tier segmentation + Top customers

📌 Add screenshots here:

C:\Users\100me\Projects\sales-intelligence-bi-suite\dashboards\tableau_dashboard_screenshots\01_executive_kpi.png.png

C:\Users\100me\Projects\sales-intelligence-bi-suite\dashboards\tableau_dashboard_screenshots\02_product_performance.png.png

C:\Users\100me\Projects\sales-intelligence-bi-suite\dashboards\tableau_dashboard_screenshots\03_customer_account_review.png.png


📌 Tableau Public link:

(https://public.tableau.com/app/profile/somesh.p8433/viz/Book1_17707052977860/Dashboard2?publish=yes)

##  Key Takeaways / Insights (examples you can include)

KPI reporting becomes consistent after staging + transformation into MySQL tables.

Missing CustomerIDs (~25%) require careful handling (exclude from customer segmentation).

Cancellations and returns are present and must be filtered or handled separately for “net sales” reporting.

Top products typically contribute a large share of revenue (Pareto-style concentration).

Resume-ready bullets

Built an end-to-end BI pipeline using Python + MySQL + Tableau Public to convert raw Excel transactions into curated KPI datasets and interactive dashboards.

Developed SQL-based transformations to populate analytics tables (customers, products, orders, order_items) and exported automated reporting extracts.

Implemented data profiling and quality checks (missing IDs, cancellations, returns) and documented KPI logic for transparent reporting.