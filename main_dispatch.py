import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 匯入產檔核心函式
from generate_reports import generate_timeseries_report

# 1. 載入環境變數 (.env)
load_dotenv()

def send_report_email(target_email, file_path, subject, recipient_name):
    """
    透過 Gmail SMTP 發送附件郵件
    """
    sender_email = os.getenv("MAIL_USER")
    sender_password = os.getenv("MAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("❌ 錯誤：找不到 MAIL_USER 或 MAIL_PASSWORD 環境變數。")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"報表自動化系統 <{sender_email}>"
    msg['To'] = target_email
    
    body = f"{recipient_name} 您好：\n\n附件為您的專屬營運數據報表，請查收。\n(本信件為系統自動發送)"
    msg.set_content(body)

    # 讀取並夾帶 Excel 檔案
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
            msg.add_attachment(
                file_data, 
                maintype='application', 
                subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                filename=file_name
            )
    except Exception as e:
        print(f"❌ 檔案讀取/夾帶失敗: {e}")
        return False

    # 執行發信
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ SMTP 發信失敗: {e}")
        return False

def run_dispatch():
    """
    主循環：讀取對照表 -> 產檔 -> 發信
    """
    # 讀取對照表並自動清洗欄位空格
    csv_file = "report_dispatch_map.csv"
    if not os.path.exists(csv_file):
        print(f"❌ 找不到對照表檔案: {csv_file}")
        return

    df = pd.read_csv(csv_file)
    df.columns = [c.strip() for c in df.columns] # 清洗 Header
    
    # 測試月份設定
    target_month = "2025-08"

    print(f"📊 開始執行自動派發任務，共 {len(df)} 筆...")

    for i, row in df.iterrows():
        # 讀取對照表資訊 (對應你的第四張截圖欄位)
        s_type = str(row['scope_type']).strip().lower() if pd.notna(row.get('scope_type')) else None
        s_value = str(row['scope_value']).strip() if pd.notna(row.get('scope_value')) else None
        recipient = str(row['Recipient']).strip() if pd.notna(row.get('Recipient')) else "相關負責人"
        email = str(row['Email']).strip() if pd.notna(row.get('Email')) else None

        if not s_value or not email:
            print(f"⚠️ 第 {i+1} 筆資料不完整，跳過。")
            continue

        print(f"\n🚀 ({i+1}/{len(df)}) 處理中: {recipient} | 維度: {s_type} | 數值: {s_value}")

        # 1. 呼叫 generate_reports.py 產出報表
        file_path = generate_timeseries_report(s_type, s_value, year_month=target_month)

        if file_path and os.path.exists(file_path):
            # 2. 產檔成功後執行發信
            subject = f"【自動速報】{s_value} 數據報告 - {target_month}"
            if send_report_email(email, file_path, subject, recipient):
                print(f"   ✅ 已成功寄送報表至: {email}")
            else:
                print(f"   ❌ 發信失敗，請檢查 SMTP 設定。")
        else:
            # 如果資料庫查無資料會進入這裡
            print(f"   ⚠️ {s_value} 無可用數據，略過發信。")

if __name__ == "__main__":
    run_dispatch()