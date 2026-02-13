import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

server = os.getenv("SRC_MSSQL_SERVER")
db = os.getenv("SRC_MSSQL_DB")
user = os.getenv("SRC_MSSQL_USER")
pw = os.getenv("SRC_MSSQL_PASSWORD")
driver = os.getenv("SRC_MSSQL_DRIVER", "ODBC Driver 18 for SQL Server")

if not all([server, db, user, pw]):
    raise ValueError("Missing .env values. Please set SRC_MSSQL_SERVER/DB/USER/PASSWORD")

# encode driver for URL
driver_enc = driver.replace(" ", "+")
url = f"mssql+pyodbc://{user}:{pw}@{server}/{db}?driver={driver_enc}&TrustServerCertificate=yes"

print("Connecting to:", f"{server}/{db} with driver={driver}")

engine = create_engine(url)

# 最小讀取：StoreData 前 5 筆
sql = "SELECT TOP (5) * FROM dbo.StoreData;"

with engine.connect() as conn:
    df = pd.read_sql(text(sql), conn)

print(df)
print("✅ SUCCESS: MSSQL connection OK")
