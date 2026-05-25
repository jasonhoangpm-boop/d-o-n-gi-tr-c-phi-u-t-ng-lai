import pandas as pd
from datetime import date, timedelta
from vnstock import Vnstock
import os

CSV_DIR = "stock_prediction_project/data"
SYMBOL = "VNINDEX"   


def fetch_history(symbol: str, years: int = 11) -> pd.DataFrame:
    """
    Fetch lịch sử OHLCV cho bất kỳ mã cổ phiếu hoặc index nào
    """

    end_date = date.today()
    start_date = end_date - timedelta(days=365 * years)

    client = Vnstock().stock(symbol=symbol, source="VCI")

    df = client.quote.history(
        start=start_date.isoformat(),
        end=end_date.isoformat(),
        interval="1D"
    )

    if df is None or df.empty:
        raise RuntimeError(f"Không lấy được dữ liệu: {symbol}")

    # chuẩn hóa tên cột
    df.columns = df.columns.str.lower()

    df = df.rename(columns={
        "time": "date",
        "datetime": "date"
    })

    required = ["date", "open", "high", "low", "close", "volume"]
    missing = [c for c in required if c not in df.columns]

    if missing:
        raise RuntimeError(f"{symbol} thiếu cột: {missing}")

    df = df[required].copy()

    # convert datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # CLEAN DATA (QUAN TRỌNG)
    df = df.dropna(subset=["date", "open", "high", "low", "close"])
    df = df[df["volume"] > 0]

    # sort + remove duplicate
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")

    df = df.reset_index(drop=True)

    return df


def save_to_csv(symbol: str = SYMBOL, years: int = 11):
    """
    Lưu dữ liệu theo từng mã riêng biệt
    """

    os.makedirs(CSV_DIR, exist_ok=True)

    df = fetch_history(symbol, years)

    file_path = os.path.join(CSV_DIR, "stock_data.csv")

    df.to_csv(file_path, index=False)

    print(f"✔ Đã lưu: {symbol}")
    print(f"✔ Path: {file_path}")
    print(df.head())


def batch_download(symbols: list, years: int = 11):
    """
    Tải nhiều mã cùng lúc (VN30, stock basket...)
    """

    for symbol in symbols:
        try:
            save_to_csv(symbol, years)
        except Exception as e:
            print(f"❌ Lỗi {symbol}: {e}")


if __name__ == "__main__":
    # 1 mã
    save_to_csv(SYMBOL)

    