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
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS mart;"))

def load_parquet(table: str, file: str):
    df = pd.read_parquet(file)
    with engine.begin() as conn:
        df.to_sql(table, schema="mart", con=conn, if_exists="replace", index=False)
    print(f"✅ Loaded mart.{table}: {len(df):,} rows")

def main():
    ensure_schema()
    load_parquet("dim_store", "dim_store.parquet")
    load_parquet("dim_sv", "dim_sv.parquet")
    load_parquet("fact_sales_daily", "fact_sales_daily.parquet")

    if os.path.exists("mapping_store_alias.parquet"):
        load_parquet("mapping_store_alias", "mapping_store_alias.parquet")

    print("✅ Import complete.")

if __name__ == "__main__":
    main()
