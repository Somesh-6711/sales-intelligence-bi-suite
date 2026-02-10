from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.config import get_engine


RAW_DIR = Path("data/raw")

def find_xlsx() -> Path:
    xlsx_files = sorted(RAW_DIR.glob("*.xlsx"))
    if not xlsx_files:
        raise FileNotFoundError("No .xlsx found in data/raw/. Put the dataset there first.")
    return xlsx_files[0]  # take first xlsx

def load_excel_to_mysql(engine, xlsx_path: Path):
    print(f"Reading: {xlsx_path}")
    df = pd.read_excel(xlsx_path, engine="openpyxl")

    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    expected = {"InvoiceNo","StockCode","Description","Quantity","InvoiceDate","UnitPrice","CustomerID","Country"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in Excel: {missing}")

    # Basic cleaning
    df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
    df["StockCode"] = df["StockCode"].astype(str).str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()
    df["Country"] = df["Country"].astype(str).str.strip()

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

    # CustomerID has missing values in this dataset; keep nullable integer
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce").astype("Int64")

    # Helpful computed fields
    df["LineSales"] = (df["Quantity"] * df["UnitPrice"]).round(2)
    df["IsCancellation"] = df["InvoiceNo"].str.startswith("C")

    # Drop rows with critical nulls
    df = df.dropna(subset=["InvoiceDate", "InvoiceNo", "StockCode", "Quantity", "UnitPrice", "Country"])

    # Load to MySQL staging table
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS retail_raw;"))

    df.to_sql("retail_raw", engine, if_exists="replace", index=False, chunksize=20000)
    print(f"✅ Loaded {len(df):,} rows into sales_bi.retail_raw")

def main():
    engine = get_engine()
    xlsx_path = find_xlsx()
    load_excel_to_mysql(engine, xlsx_path)

if __name__ == "__main__":
    main()
