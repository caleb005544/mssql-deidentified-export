import os
import pandas as pd
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

from generate_reports import generate_timeseries_report

# 1. load (.env)
load_dotenv()

def send_report_email(target_email, file_path, subject, recipient_name):
    """
    Gmail SMTP 
    """
    sender_email = os.getenv("MAIL_USER")
    sender_password = os.getenv("MAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("❌Can't find MAIL_USER or MAIL_PASSWORD")
        return False

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = f"Automated Report Delivery System <{sender_email}>"
    msg['To'] = target_email
    
    body = f"{recipient_name} Hello：\n\nAttached is your daily report\n(This is automated email.)"
    msg.set_content(body)

    # read excel
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
        print(f"❌ file read failure {e}")
        return False

    # send
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ SMTP error {e}")
        return False

def run_dispatch():

    csv_file = "report_dispatch_map.csv"
    if not os.path.exists(csv_file):
        print(f"❌ Can't locate file: {csv_file}")
        return

    df = pd.read_csv(csv_file)
    df.columns = [c.strip() for c in df.columns]
    
    target_month = "2025-08"

    print(f"📊 Start sending reports {len(df)} ")

    for i, row in df.iterrows():

        s_type = str(row['scope_type']).strip().lower() if pd.notna(row.get('scope_type')) else None
        s_value = str(row['scope_value']).strip() if pd.notna(row.get('scope_value')) else None
        recipient = str(row['Recipient']).strip() if pd.notna(row.get('Recipient')) else "other"
        email = str(row['Email']).strip() if pd.notna(row.get('Email')) else None

        if not s_value or not email:
            print(f"⚠️  {i+1} incorrect files")
            continue

        print(f"\n🚀 ({i+1}/{len(df)}) processing {recipient} | dimension: {s_type} | number: {s_value}")

        # 1. generate_reports.py 
        file_path = generate_timeseries_report(s_type, s_value, year_month=target_month)

        if file_path and os.path.exists(file_path):
 
            subject = f"【auto report】{s_value} report - {target_month}"
            if send_report_email(email, file_path, subject, recipient):
                print(f"   ✅ Successfully send to {email}")
            else:
                print(f"   ❌ Send email failed for {email}")
        else:
            print(f"   ⚠️ {s_value} report generation failed or file not found.")

if __name__ == "__main__":
    run_dispatch()