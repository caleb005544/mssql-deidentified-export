import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
dst_url = os.getenv("DST_DB_URL")
if not dst_url:
    raise ValueError("Missing DST_DB_URL in .env")

engine = create_engine(dst_url)

def ensure_schema():
    sql = """
    CREATE SCHEMA IF NOT EXISTS mart;
    """
    with engine.begin() as conn:
        conn.execute(text(sql))

def load_parquet(table: str, file: str):
    df = pd.read_parquet(file)
    with engine.begin() as conn:
        df.to_sql(table, schema="mart", con=conn, if_exists="replace", index=False)

def main():
    ensure_schema()
    load_parquet("dim_store", "export/dim_store.parquet")
    load_parquet("dim_sv", "export/dim_sv.parquet")
    load_parquet("dim_holiday", "export/dim_holiday.parquet")
    load_parquet("fact_posheader", "export/fact_posheader.parquet")
    load_parquet("fact_sales_daily", "export/fact_sales_daily.parquet")
    print("✅ Import complete: mart tables created")

if __name__ == "__main__":
    main()
