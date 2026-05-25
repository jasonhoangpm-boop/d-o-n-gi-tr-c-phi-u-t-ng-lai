import pandas as pd
from sqlalchemy import text
from typing import Any

from project.database.db_config import get_db_engine
from project.utils.logger import get_logger


logger = get_logger(__name__)


REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]


def store_stock_data(symbol: str, df: pd.DataFrame, interval: str = "5m") -> None:
    """🔥 Lưu dữ liệu cổ phiếu vào bảng {symbol}_prices"""
    from project.database.db_config import create_stock_table
    
    try:
        if df is None or df.empty:
            raise RuntimeError("Input DataFrame is empty.")

        required = ["date", "open", "high", "low", "close", "volume"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise RuntimeError(f"Missing columns: {missing}")

        # Tạo bảng nếu chưa tồn tại
        create_stock_table(symbol)

        working_df = df[required].copy()
        working_df = working_df.dropna()

        # 🔥 FIX DATE FORMAT
        working_df["date"] = pd.to_datetime(working_df["date"])

        # 🔥 IMPORTANT: add interval column
        working_df["interval"] = interval

        # 🔥 volume safe cast
        working_df["volume"] = working_df["volume"].astype("int64")

        records = working_df.to_dict(orient="records")

        if not records:
            logger.info("No valid rows to insert")
            return

        engine = get_db_engine()
        table_name = f"{symbol.lower()}_prices"

        # 🔥 Dynamic SQL (tùy theo symbol)
        upsert_sql = text(f"""
            INSERT INTO {table_name}
            (date, open, high, low, close, volume, interval)
            VALUES
            (:date, :open, :high, :low, :close, :volume, :interval)
            ON CONFLICT (date, interval) DO UPDATE
            SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume;
        """)

        with engine.begin() as conn:
            conn.execute(upsert_sql, records)

        logger.info(f"✅ Inserted/Updated {len(records)} rows into {table_name}")

    except Exception as exc:
        logger.error(f"Failed to store {symbol} data: {exc}")
        raise RuntimeError(f"Data store failed: {exc}") from exc


def store_vnindex_data(df: pd.DataFrame, interval: str = "5m") -> None:
    try:
        if df is None or df.empty:
            raise RuntimeError("Input DataFrame is empty.")

        required = ["date", "open", "high", "low", "close", "volume"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            raise RuntimeError(f"Missing columns: {missing}")

        working_df = df[required].copy()
        working_df = working_df.dropna()

        # 🔥 FIX DATE FORMAT
        working_df["date"] = pd.to_datetime(working_df["date"])

        # 🔥 IMPORTANT: add interval column
        working_df["interval"] = interval

        # 🔥 volume safe cast
        working_df["volume"] = working_df["volume"].astype("int64")

        records = working_df.to_dict(orient="records")

        if not records:
            logger.info("No valid rows to insert")
            return

        engine = get_db_engine()

        # 🔥 FIX SQL (PHẢI CÓ interval)
        upsert_sql = text("""
            INSERT INTO vnindex_prices
            (date, open, high, low, close, volume, interval)
            VALUES
            (:date, :open, :high, :low, :close, :volume, :interval)
            ON CONFLICT (date, interval) DO UPDATE
            SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume;
        """)

        with engine.begin() as conn:
            conn.execute(upsert_sql, records)

        logger.info("Inserted/Updated %s rows", len(records))

    except Exception as exc:
        logger.error("Failed to store VNINDEX data: %s", exc)
        raise RuntimeError(f"Data store failed: {exc}") from exc