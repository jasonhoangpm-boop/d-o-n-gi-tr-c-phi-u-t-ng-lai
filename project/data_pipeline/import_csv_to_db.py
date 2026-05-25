"""
Script để import dữ liệu từ CSV vào bảng vnindex_prices (PostgreSQL)
"""

from pathlib import Path
import os

from dotenv import load_dotenv
import pandas as pd

from project.data_pipeline.store_data import store_vnindex_data



# 📌 ROOT project
BASE_DIR = Path(__file__).resolve().parents[2]

# 📌 Load .env
load_dotenv(BASE_DIR / ".env", override=True)

# 📌 CSV path (absolute để tránh lỗi)
CSV_PATH = BASE_DIR / "stock_prediction_project" / "data" / "stock_data.csv"


def main():
    
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {CSV_PATH}")

    
    df = pd.read_csv(CSV_PATH)

    
    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    
    required_cols = ["date", "open", "high", "low", "close", "volume"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise RuntimeError(f"Thiếu cột: {missing}")

    
    df = df[required_cols].copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)

    # 🔥 tạo table nếu chưa có
    create_table_if_needed()

    print(f"Import {len(df)} rows vào database...")

    
    store_vnindex_data(df, interval="1D")

    print("Đã import xong vào database!")


if __name__ == "__main__":
    main()