import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import text

from project.config import MA_LONG_WINDOW, MA_SHORT_WINDOW, NORM_MAX, NORM_MIN
from project.database.db_config import get_db_engine
from project.utils.logger import get_logger


logger = get_logger(__name__)


def preprocess_vnindex_data() -> pd.DataFrame:
    try:
        engine = get_db_engine()                
        query = text(
            """
            SELECT date, open, high, low, close, volume
            FROM vnindex_prices
            ORDER BY date ASC
            """
        )

        df = pd.read_sql(query, engine)
        if df.empty:
            raise RuntimeError("No rows found in vnindex_prices.")

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        numeric_cols = ["open", "high", "low", "close", "volume"]
        df = df.dropna(subset=numeric_cols)

        df["MA_10"] = df["close"].rolling(window=MA_SHORT_WINDOW).mean()
        df["MA_20"] = df["close"].rolling(window=MA_LONG_WINDOW).mean()

        df = df.dropna().reset_index(drop=True)

        scale_cols = ["open", "high", "low", "close", "volume", "MA_10", "MA_20"]
        scaler = MinMaxScaler(feature_range=(NORM_MIN, NORM_MAX))
        df[scale_cols] = scaler.fit_transform(df[scale_cols])

        logger.info("Preprocessed %s rows from vnindex_prices", len(df))
        return df
    except Exception as exc:
        logger.error("Failed to preprocess VNINDEX data: %s", exc)
        raise RuntimeError(f"Preprocessing failed: {exc}") from exc
