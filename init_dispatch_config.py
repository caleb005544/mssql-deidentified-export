import pandas as pd
import os

def generate_dispatch_csv():
    # 定義派發清單內容
    # scope_type: 報表維度 (brand/sv/storeno)
    # scope_value: 對應名稱 (必須與資料庫內名稱完全一致)
    # Recipient: 收件者姓名 (顯示於信件內文)
    # Email: 接收信箱
    data = [
        # Brand 維度
        ["brand", "brand 1", "Debbie總部", "debbierepo3@gmail.com"],
        ["brand", "brand 2", "Debbie總部", "debbierepo3@gmail.com"],
        
        # SV 維度
        ["sv", "王小明", "王小明督導", "debbierepo3@gmail.com"],
        ["sv", "李大同", "李大同督導", "debbierepo3@gmail.com"],
        
        # StoreNo 維度 (單店)
        ["storeno", "B1001", "B1001店長", "debbierepo3@gmail.com"],
        ["storeno", "B1002", "B1002店長", "debbierepo3@gmail.com"],
    ]

    # 建立 DataFrame
    df = pd.DataFrame(data, columns=["scope_type", "scope_value", "Recipient", "Email"])

    # 產出路徑 (確保存在於你的專案根目錄)
    file_path = "report_dispatch_map.csv"

    # 儲存為 CSV (使用 UTF-8 編碼確保中文不亂碼)
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    
    print(f"✅ 已成功生成對照表：{os.path.abspath(file_path)}")
    print(f"📊 目前共有 {len(df)} 筆派發任務。")

if __name__ == "__main__":
    generate_dispatch_csv()