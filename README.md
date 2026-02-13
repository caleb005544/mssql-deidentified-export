# MSSQL Export & De-Identification Tool

This project extracts aggregated sales data from a SQL Server (MSSQL) database, performs de-identification, and exports portable Parquet files for offline usage.

## 🎯 Purpose

- Extract daily aggregated sales (2024–2025)
- Remove personally identifiable information
- Generate portable datasets
- Prepare data for offline PostgreSQL import
- Support automated report dispatch system

## 📦 Output Files

Generated under `/export`:

- dim_store.parquet
- dim_sv.parquet
- fact_sales_daily.parquet
- mapping_store_alias.parquet

## 🔐 Security

- `.env` file is required but not included
- No raw transaction-level data exported
- No customer/member information included
- Only aggregated daily store-level data exported

## 🚀 Usage

1. Create `.env` from `.env.example`
2. Install dependencies:

## Version 1.0 - Initial Export Tool

