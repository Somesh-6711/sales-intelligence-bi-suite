import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

def get_engine():
    host = os.getenv("MYSQL_HOST", "localhost")
    port = os.getenv("MYSQL_PORT", "3306")
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
    db = os.getenv("MYSQL_DB", "sales_bi")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"
    return create_engine(url, pool_pre_ping=True)

if __name__ == "__main__":
    engine = get_engine()
    with engine.connect() as conn:
        conn.exec_driver_sql("SELECT 1;")
    print("✅ MySQL connection successful.")
