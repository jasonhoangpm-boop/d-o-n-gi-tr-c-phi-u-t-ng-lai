from datetime import date
from time import sleep

import pandas as pd
from vnstock import Vnstock

from project.config import START_DATE, SYMBOL
from project.data_pipeline.store_data import store_vnindex_data
from project.utils.logger import get_logger

logger = get_logger(__name__)

SUPPORTED_INTERVALS = {"1D", "1H", "15m", "5m", "1m"}
DEFAULT_INTERVAL = "5m"

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {
        "time": "date",
        "datetime": "date",
    }
    df = df.rename(columns=rename_map)

    required = ["date", "open", "high", "low", "close", "volume"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise RuntimeError(f"Missing required columns from API response: {missing}")

    return df[required].copy()

def _fetch_with_interval(interval: str) -> pd.DataFrame:
    end_date = date.today().isoformat()
    stock_client = Vnstock().stock(symbol=SYMBOL, source="VCI")
    raw_df = stock_client.quote.history(start=START_DATE, end=end_date, interval=interval)

    if raw_df is None or raw_df.empty:
        logger.warning(f"No data returned from vnstock API for VNINDEX at interval={interval}.")
        return pd.DataFrame()

    logger.info("Raw data from API (head):\n%s", raw_df.head())
    logger.info("Raw data from API (tail):\n%s", raw_df.tail())

    df = _normalize_columns(raw_df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    # Xử lý timezone nếu có
    if hasattr(df["date"].iloc[0], 'tzinfo') and df["date"].iloc[0].tzinfo is not None:
        df["date"] = df["date"].dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)
    else:
        df["date"] = df["date"].dt.tz_localize(None)
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")

    # Chỉ resample nếu interval là intraday (khác 1D)
    if interval == "1m":
        df = df.set_index("date")
        df = df.between_time("09:00", "15:00")
        df = df.resample("5min").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })
        df = df.dropna().reset_index()
    elif interval in ["5m", "15m", "1H"]:
        df = df.sort_values("date").reset_index(drop=True)
    elif interval == "1D":
        df = df.reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    latest_timestamp = df["date"].max() if not df.empty else None
    today = pd.Timestamp.today().normalize()
    if latest_timestamp is not None and (today - latest_timestamp) > pd.Timedelta(days=1):
        logger.warning("Dữ liệu mới nhất cho VNINDEX chỉ đến ngày %s, hôm nay là %s", latest_timestamp, today)

    logger.info(
        "Fetched %s rows for VNINDEX at interval=%s. Latest timestamp: %s",
        len(df),
        interval,
        latest_timestamp,
    )
    return df


def _fetch_with_interval_generic(symbol: str, interval: str) -> pd.DataFrame:
    """🔥 Fetch dữ liệu cổ phiếu tùy ý từ vnstock"""
    end_date = date.today().isoformat()
    stock_client = Vnstock().stock(symbol=symbol, source="VCI")
    raw_df = stock_client.quote.history(start=START_DATE, end=end_date, interval=interval)

    if raw_df is None or raw_df.empty:
        raise RuntimeError(f"No data returned from vnstock API for {symbol} at interval={interval}.")

    logger.info("Raw data from API for %s (head):\n%s", symbol, raw_df.head())
    logger.info("Raw data from API for %s (tail):\n%s", symbol, raw_df.tail())

    df = _normalize_columns(raw_df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    # Xử lý timezone nếu có
    if hasattr(df["date"].iloc[0], 'tzinfo') and df["date"].iloc[0].tzinfo is not None:
        df["date"] = df["date"].dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)
    else:
        df["date"] = df["date"].dt.tz_localize(None)
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")

    # Chỉ resample nếu interval là intraday (khác 1D)
    if interval == "1m":
        df = df.set_index("date")
        df = df.between_time("09:00", "15:00")
        df = df.resample("5min").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })
        df = df.dropna().reset_index()
    elif interval in ["5m", "15m", "1H"]:
        df = df.sort_values("date").reset_index(drop=True)
    elif interval == "1D":
        df = df.reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)

    latest_timestamp = df["date"].max() if not df.empty else None
    today = pd.Timestamp.today().normalize()
    if latest_timestamp is not None and (today - latest_timestamp) > pd.Timedelta(days=1):
        logger.warning("Dữ liệu mới nhất cho %s chỉ đến ngày %s, hôm nay là %s", symbol, latest_timestamp, today)

    logger.info(
        "Fetched %s rows for %s at interval=%s. Latest timestamp: %s",
        len(df),
        symbol,
        interval,
        latest_timestamp,
    )
    return df

    if raw_df is None or raw_df.empty:
        raise RuntimeError(f"No data returned from vnstock API for interval={interval}.")

    logger.info("Raw data from API (head):\n%s", raw_df.head())
    logger.info("Raw data from API (tail):\n%s", raw_df.tail())

    df = _normalize_columns(raw_df)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")
    # Xử lý timezone nếu có
    if hasattr(df["date"].iloc[0], 'tzinfo') and df["date"].iloc[0].tzinfo is not None:
        df["date"] = df["date"].dt.tz_convert("Asia/Ho_Chi_Minh").dt.tz_localize(None)
    else:
        df["date"] = df["date"].dt.tz_localize(None)
    df = df.sort_values("date").drop_duplicates(subset=["date"], keep="last")

    # Chỉ resample nếu interval là intraday (khác 1D)
    if interval == "1m":
        # Chỉ resample từ 1m -> 5m
        df = df.set_index("date")
        df = df.between_time("09:00", "15:00")

        df = df.resample("5min").agg({
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum"
        })

        df = df.dropna().reset_index()

    elif interval in ["5m", "15m", "1H"]:
        # 👉 KHÔNG resample nữa
        df = df.sort_values("date").reset_index(drop=True)

    elif interval == "1D":
        df = df.reset_index(drop=True)
    else:
        # Nếu là daily thì giữ nguyên
        df = df.reset_index(drop=True)

    # Cảnh báo nếu thiếu ngày mới nhất
    latest_timestamp = df["date"].max() if not df.empty else None
    today = pd.Timestamp.today().normalize()
    if latest_timestamp is not None and (today - latest_timestamp) > pd.Timedelta(days=1):
        logger.warning("Dữ liệu mới nhất chỉ đến ngày %s, hôm nay là %s", latest_timestamp, today)

    logger.info(
        "Fetched %s rows for %s at interval=%s. Latest timestamp fetched: %s",
        len(df),
        SYMBOL,
        interval,
        latest_timestamp,
    )
    return df

def fetch_vnindex_data(interval: str = DEFAULT_INTERVAL, fallback_to_daily: bool = True) -> pd.DataFrame:
    selected_interval = interval.strip() if isinstance(interval, str) else DEFAULT_INTERVAL

    if selected_interval not in SUPPORTED_INTERVALS:
        raise RuntimeError(f"Unsupported interval '{selected_interval}'. Supported: {sorted(SUPPORTED_INTERVALS)}")

    def safe_fetch(i: str) -> pd.DataFrame:
        try:
            df = _fetch_with_interval(i)

            
            if df is None:
                return pd.DataFrame()

            return df

        except Exception as e:
            logger.warning("Fetch failed for interval=%s: %s", i, e)
            return pd.DataFrame()

    
    df = safe_fetch(selected_interval)

    
    if df.empty and fallback_to_daily and selected_interval != "1D":
        logger.warning("Fallback to 1D interval")
        df = safe_fetch("1D")

    # 3. nếu vẫn rỗng → return empty DF an toàn
    if df.empty:
        logger.error("All fetch attempts failed")
        return pd.DataFrame()

    return df


def fetch_stock_data(symbol: str, interval: str = DEFAULT_INTERVAL, fallback_to_daily: bool = True) -> pd.DataFrame:
    """🔥 Fetch dữ liệu cổ phiếu tùy ý - hỗ trợ mọi mã chứng chỉ"""
    selected_interval = interval.strip() if isinstance(interval, str) else DEFAULT_INTERVAL
    if selected_interval not in SUPPORTED_INTERVALS:
        raise RuntimeError(f"Unsupported interval '{selected_interval}'. Supported: {sorted(SUPPORTED_INTERVALS)}")

    try:
        return _fetch_with_interval_generic(symbol, selected_interval)
    except Exception as exc:
        if fallback_to_daily and selected_interval != "1D":
            logger.warning(
                "Intraday fetch failed for %s at interval=%s. Fallback to 1D. Error: %s",
                symbol,
                selected_interval,
                exc,
            )
            return _fetch_with_interval_generic(symbol, "1D")

        logger.error(f"Failed to fetch {symbol} data: {exc}")
        raise RuntimeError(f"Data fetch failed for {symbol}: {exc}") from exc

def run_realtime_ingestion(interval: str = DEFAULT_INTERVAL, refresh_seconds: int = 300) -> None:
    logger.info(
        "Starting realtime ingestion for %s with interval=%s and refresh=%s seconds",
        SYMBOL,
        interval,
        refresh_seconds,
    )

    try:
        while True:
            try:
                df = fetch_vnindex_data(interval=interval, fallback_to_daily=True)
                store_vnindex_data(df)

                latest_timestamp = df["date"].max() if not df.empty else None
                logger.info("Last updated time after ingestion: %s", latest_timestamp)
            except Exception as exc:
                logger.error("Realtime ingestion cycle failed: %s", exc)

            sleep(refresh_seconds)
    except KeyboardInterrupt:
        logger.info("Realtime ingestion stopped by user.")

