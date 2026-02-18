這份完整的 README.md 採用中英對照格式，除了展現技術實力外，更特別強調了你對組織異動維護 (Org Maintenance) 與 行級安全性 (RLS) 的專業理解。

企業級自動化報表與 RLS 派發系統 / Enterprise Automated Reporting with RLS
📖 專案概述 / Project Overview
本專案開發了一套針對企業環境設計的數據自動化派發流程。透過 Python 結合 SQL 數據庫，實現根據不同接收者的職權範圍（如品牌、部門、負責人）自動篩選數據（Row-Level Security, RLS），並定時生成客製化 Excel 報表發送至對應人員。

This project implements an automated data distribution workflow tailored for corporate environments. Using Python and SQL, it enforces Row-Level Security (RLS) to filter data based on the recipient's scope (e.g., Brand, SV, or Manager) and dispatches customized Excel reports on a scheduled basis.

🎯 核心目標 / Core Objectives
消除人工耗時 / Eliminate Manual Work: 轉化每日手動篩選、製表、寄信的重複性勞動。

Converts daily manual data filtering, formatting, and emailing into a zero-touch automated task.

數據權限安全 / Data Security & RLS: 確保「正確的人只看到正確的數據」。

Ensures "the right person sees only the right data" through automated logic.

內網資安合規 / Intranet Compliance: 採用地端部署（On-premise），解決企業內網資料庫無法對外連線的限制。

Utilizes on-premise deployment to bypass firewall restrictions for internal databases like MSSQL.

🛠️ 技術特點 / Technical Features
1. 動態 RLS 與 名單維護 / Dynamic RLS & List Maintenance
針對企業頻繁的組織異動（調職、離職、新進），系統設計了高度可維護性：

組織對照表管理 / Org-Mapping Management: 透過維護 report_dispatch_map 檔案，管理人員名單、組織層級與對應電子信箱。

Manages personnel lists, organizational hierarchies, and emails via a centralized report_dispatch_map.

靈活擴充性 / Scalability: 組織調整時，僅需更新對照表即可，無需改動核心程式碼。

Updates distribution logic by simply editing the mapping file without modifying the core source code.

2. 交付穩定性策略 / Delivery Stability
SMTP 驗證 / Authenticated SMTP: 支援企業級發信權限配置。

Supports enterprise-grade SMTP authentication for reliable sending.

白名單建議 / Whitelisting: 配置收件端「安全寄件者」以確保報表不被視為垃圾郵件。

Advocates for "Safe Senders" whitelisting to prevent automated reports from being flagged as spam.

🚀 部署與執行 / Deployment & Execution
設定環境變數 / Setup Environment Variables (.env)
Code snippet
DB_HOST=your_internal_db_ip
MAIL_USER=your_office365_account
MAIL_PASSWORD=your_app_password
設定自動排程 / Setup Cron Job
Bash
# 每天下午 4:30 執行 / Run every day at 16:30
30 16 * * * cd /path/to/project && /path/to/.venv/bin/python main_dispatch.py >> cron_log.log 2>&1
💎 專案價值 / Value Proposition
維護成本低 / Low Maintenance: 將人員名單維護與程式邏輯分離。

Decouples personnel management from programmatic logic.

資安在地化 / Data Residency: 數據生成過程不流經任何第三方雲端，符合資安法規。

Processes stay within the intranet, ensuring data privacy and regulatory compliance.

日誌監控 / Logging: 內建 cron_log.log 機制，實現 7/24 的自動化監控與故障排除。

Built-in logging for 7/24 monitoring and efficient troubleshooting.

📜 授權協議 / License
本專案採用 MIT License。
Distributed under the MIT License.
