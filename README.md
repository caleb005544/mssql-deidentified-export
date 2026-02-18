# 企業級自動化報表與 RLS 派發系統 / Enterprise Automated Reporting with RLS

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Database](https://img.shields.io/badge/Database-Postgres%20%7C%20MSSQL-orange.svg)

## 📖 專案概述 / Project Overview
本專案開發了一套針對企業環境設計的數據自動化派發流程。透過 Python 結合 SQL 數據庫，實現根據不同接收者的職權範圍（如品牌、部門、負責人）自動篩選數據（Row-Level Security, RLS），並定時生成客製化 Excel 報表發送至對應人員。

This project implements an automated data distribution workflow tailored for corporate environments. Using Python and SQL, it enforces Row-Level Security (RLS) to filter data based on the recipient's scope and dispatches customized Excel reports on a scheduled basis.

---

## 🎯 核心目標 / Core Objectives
* **消除人工耗時 / Eliminate Manual Work**: 轉化每日手動篩選、製表、寄信的重複性勞動。
* **數據權限安全 / Data Security & RLS**: 確保「正確的人只看到正確的數據」。
* **內網資安合規 / Intranet Compliance**: 採用地端部署（On-premise），解決企業內網資料庫無法對外連線的限制。

---

## 🛠️ 技術特點 / Technical Features

### 1. 動態 RLS 與 名單維護 / Dynamic RLS & List Maintenance
針對企業頻繁的組織異動（調職、離職、新進），系統設計了高度可維護性：
* **組織對照表管理 / Org-Mapping Management**: 透過維護 `report_dispatch_map` 檔案，管理人員名單、組織層級與對應電子信箱。
* **靈活擴充性 / Scalability**: 組織調整時，僅需更新對照表即可，無需改動核心程式碼。

### 2. 交付穩定性策略 / Delivery Stability
* **SMTP 驗證 / Authenticated SMTP**: 支援企業級發信權限配置。
* **白名單建議 / Whitelisting**: 配置收件端「安全寄件者」以確保報表不被視為垃圾郵件。

---

## 🚀 部署與執行 / Deployment & Execution

### 設定環境變數 / Setup Environment Variables (`.env`)
```env
DB_HOST=your_internal_db_ip
MAIL_USER=your_office365_account
MAIL_PASSWORD=your_app_password

## 設定自動排程 / Setup Cron Job

# 每天下午 4:30 執行 / Run every day at 16:30
30 16 * * * cd /path/to/project && /path/to/.venv/bin/python main_dispatch.py >> cron_log.log 2>&1

## 專案價值 / Value Proposition
維護成本低 / Low Maintenance: 將人員名單維護與程式邏輯分離，降低管理複雜度。
資安在地化 / Data Residency: 數據生成過程不流經任何第三方雲端，減少管理成本。
日誌監控 / Logging: 內建 cron_log.log 機制，實現 7/24 的自動化監控與故障排除。
