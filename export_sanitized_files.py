"""
export_sanitized_files.py

Company network/VPN only:
- Extract minimal, de-identified datasets from MSSQL (PowerBI DB)
- Output portable Parquet files under ./export
- No local DB needed at company side

Outputs (based on your latest scope):
- export/dim_store.parquet
- export/dim_sv.parquet
- export/mapping_store_alias.parquet
- export/fact_sales_daily.parquet   (daily aggregated already; safest & smallest)

Notes:
- Holiday: not exported (you said you will build it yourself)
- Budget: not exported
- POSHeader: exported as DAILY AGGREGATE (no OrderId/OrderNo/MembershipNo -> very low risk)
"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

# ---- MSSQL conn (from .env) ----
server = os.getenv("SRC_MSSQL_SERVER")
db = os.getenv("SRC_MSSQL_DB")
user = os.getenv("SRC_MSSQL_USER")
pw = os.getenv("SRC_MSSQL_PASSWORD")
driver = os.getenv("SRC_MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")

# Export date range (inclusive start, exclusive end)
START_DATE = "2024-01-01"
END_DATE_EXCL = "2026-01-01"  # covers 2025-12-31

if not all([server, db, user, pw]):
    raise ValueError("Missing .env values. Please set SRC_MSSQL_SERVER/DB/USER/PASSWORD")

driver_enc = driver.replace(" ", "+")
SRC_URL = f"mssql+pyodbc://{user}:{pw}@{server}/{db}?driver={driver_enc}&TrustServerCertificate=yes"
engine = create_engine(SRC_URL, fast_executemany=True)

os.makedirs("export", exist_ok=True)


def export_dim_store():
    """
    StoreData columns you provided:
      Brand, StoreNo, StoreName, StoreAddress, StoreTelephone, OpenDate, CloseDate, Category, Type, Area, SeatCount

    We keep only:
      Brand, StoreNo, StoreName (anonymized), Category, Type, Area
    We drop:
      Address, Telephone, SeatCount, dates, etc.
    """
    q = """
    SELECT
        Brand,
        StoreNo,
        StoreName,
        Category,
        Type,
        Area
    FROM dbo.StoreData;
    """
    df = pd.read_sql(text(q), engine)

    # Normalize keys
    df["StoreNo"] = df["StoreNo"].astype(str)

    # StoreName anonymization: deterministic alias by StoreNo ordering
    uniq = sorted(df["StoreNo"].unique())
    mapping = {s: f"Store-{i+1:04d}" for i, s in enumerate(uniq)}
    df["StoreName"] = df["StoreNo"].map(mapping)

    # Save mapping for debugging/trace (optional)
    pd.DataFrame(
        {"storeno": uniq, "store_alias": [mapping[s] for s in uniq]}
    ).to_parquet("export/mapping_store_alias.parquet", index=False)

    # Rename to target dim columns
    df = df.rename(
        columns={
            "Brand": "brand",
            "StoreNo": "storeno",
            "StoreName": "store_name",
            "Category": "category",
            "Type": "type",
            "Area": "area",
        }
    )

    df.to_parquet("export/dim_store.parquet", index=False)
    print(f"✅ Exported dim_store: {len(df):,} rows")


def export_dim_sv():
    """
    SVData columns you provided:
      StoreNo, SVName, SVStartDate, SVEndDate

    For reporting dispatch, we need StoreNo -> SVName mapping.
    Keep only:
      StoreNo, SVName
    """
    q = """
    SELECT
        StoreNo,
        SVName
    FROM dbo.SVData;
    """
    df = pd.read_sql(text(q), engine)

    df["StoreNo"] = df["StoreNo"].astype(str)

    df = df.rename(columns={"StoreNo": "storeno", "SVName": "sv_name"})

    # Optional: if multiple records per StoreNo exist, keep one deterministically
    # (e.g., latest by sorting sv_name; or you can implement date logic later if needed)
    df = df.drop_duplicates(subset=["storeno"], keep="last")

    df.to_parquet("export/dim_sv.parquet", index=False)
    print(f"✅ Exported dim_sv: {len(df):,} rows")


def export_fact_sales_daily():
    """
    POSHeader columns you provided include:
      OrderDate, StoreNo, CustomerCount, NetAmount, (plus many sensitive fields)

    We export DAILY AGGREGATE ONLY (de-identified):
      date, storeno, revenue, customer_count

    No OrderId/OrderNo/MembershipNo exported.
    """
    q = f"""
    SELECT
        OrderDate AS [date],
        StoreNo,
        SUM(NetAmount) AS revenue,
        SUM(CustomerCount) AS customer_count
    FROM dbo.POSHeader
    WHERE OrderDate >= '{START_DATE}'
      AND OrderDate <  '{END_DATE_EXCL}'
    GROUP BY OrderDate, StoreNo
    ORDER BY OrderDate, StoreNo;
    """
    df = pd.read_sql(text(q), engine)

    # Types
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["StoreNo"] = df["StoreNo"].astype(str)

    df = df.rename(columns={"StoreNo": "storeno"})

    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce").fillna(0).round(2)
    df["customer_count"] = pd.to_numeric(df["customer_count"], errors="coerce").fillna(0).astype(int)

    df.to_parquet("export/fact_sales_daily.parquet", index=False)
    print(f"✅ Exported fact_sales_daily: {len(df):,} rows")


def main():
    export_dim_store()
    export_dim_sv()
    export_fact_sales_daily()
    print("✅ Export complete. Files saved under ./export")
    print("   Files:")
    print("   - export/dim_store.parquet")
    print("   - export/dim_sv.parquet")
    print("   - export/mapping_store_alias.parquet")
    print("   - export/fact_sales_daily.parquet")


if __name__ == "__main__":
    main()
