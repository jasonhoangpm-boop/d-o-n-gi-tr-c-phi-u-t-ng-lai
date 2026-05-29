from __future__ import annotations

import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ROOT_DIR)

from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st
import torch
from dotenv import load_dotenv
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import text
from streamlit_autorefresh import st_autorefresh

import stock_prediction_project.config as model_config
from project.data_pipeline.fetch_data import fetch_vnindex_data
from project.data_pipeline.preprocess_data import preprocess_vnindex_data
from project.data_pipeline.store_data import store_vnindex_data
from project.database.db_config import get_db_engine, initialize_database

import stock_prediction_project.config as model_config
from project.data_pipeline.fetch_data import fetch_vnindex_data, fetch_stock_data
from project.data_pipeline.preprocess_data import preprocess_vnindex_data
from project.data_pipeline.store_data import store_vnindex_data, store_stock_data
from project.database.db_config import get_db_engine, create_stock_table
from stock_prediction_project.models.lstm_model import StockLSTM
from ui.components.chart import build_price_volume_figure
from ui.components.header import render_header
from ui.components.prediction_panel import render_prediction_panel
from ui.components.timeframe_selector import filter_by_timeframe, render_timeframe_selector
from ui.components.training_panel import render_training_panel
from ui.auth import show_auth_pages

import stock_prediction_project.config as model_config
from project.data_pipeline.fetch_data import fetch_vnindex_data, fetch_stock_data
from project.data_pipeline.preprocess_data import preprocess_vnindex_data
from project.data_pipeline.store_data import store_vnindex_data, store_stock_data
from project.database.db_config import get_db_engine, create_stock_table
from stock_prediction_project.models.lstm_model import StockLSTM
from ui.components.chart import build_price_volume_figure
from ui.components.header import render_header
from ui.components.prediction_panel import render_prediction_panel
from ui.components.timeframe_selector import filter_by_timeframe, render_timeframe_selector
from ui.components.training_panel import render_training_panel
from ui.auth import show_auth_pages

FEATURE_COLUMNS = ["open", "high", "low", "close", "volume"]
ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "stock_prediction_project" / "models" / "best_stock_lstm.pt"
FALLBACK_CSV = ROOT_DIR / "stock_prediction_project" / "data" / "stock_data.csv"


def inject_styles() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0f1c, #05070d);
        color: #e6edf3;
    }

    /* Header */
    .finance-header {
        background: linear-gradient(135deg, #0f172a, #020617);
        border: 1px solid rgba(0,255,255,0.15);
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 0 20px rgba(0,255,255,0.1);
    }

    .finance-header h1 {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.4rem;
        color: #00f5ff;
        text-shadow: 0 0 10px #00f5ff;
    }

    /* Metric card */
    [data-testid="stMetric"] {
        background: linear-gradient(145deg, #020617, #0f172a);
        border: 1px solid rgba(0,255,255,0.1);
        border-radius: 14px;
        padding: 10px;
        box-shadow: 0 0 10px rgba(0,255,255,0.05);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(0,255,255,0.1);
    }

    /* Button */
    .stButton>button {
        background: linear-gradient(90deg, #00f5ff, #00c3ff);
        border: none;
        border-radius: 10px;
        color: black;
        font-weight: bold;
    }

    .stButton>button:hover {
        box-shadow: 0 0 12px #00f5ff;
    }

    /* Chart container */
    .plotly-graph-div {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0,255,255,0.1);
    }

    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=55)
def load_stock_data(symbol: str = "VNINDEX") -> pd.DataFrame:
    engine = get_db_engine()
    table_name = f"{symbol.lower()}_prices"
    query = text(
        f"""
        SELECT date, open, high, low, close, volume
        FROM {table_name}
        ORDER BY date ASC
        """
    )
    data_frame = pd.read_sql(query, engine)

    if data_frame is None or data_frame.empty:
        raise RuntimeError("API returned empty data")

    data_frame["date"] = pd.to_datetime(data_frame["date"])
    for column in FEATURE_COLUMNS:
        data_frame[column] = pd.to_numeric(data_frame[column], errors="coerce")

    data_frame = data_frame.dropna(subset=["date", *FEATURE_COLUMNS]).sort_values("date").reset_index(drop=True)
    return data_frame


@st.cache_data(ttl=15)
def load_live_stock_data(symbol: str = "VNINDEX", interval: str = "5m") -> pd.DataFrame:
    
    # 👉 dùng hàm chung cho tất cả mã
    data_frame = fetch_stock_data(symbol=symbol, interval=interval, fallback_to_daily=False)

    if data_frame is None or data_frame.empty:
        raise RuntimeError(f"No rows returned from live API for {symbol}")

    data_frame = data_frame.copy()

    # chuẩn hóa date
    data_frame["date"] = pd.to_datetime(data_frame["date"], errors="coerce")

    # sort
    data_frame = data_frame.sort_values("date").reset_index(drop=True)

    # bỏ trùng thời gian
    data_frame = data_frame.drop_duplicates(subset=["date"], keep="last")

    # convert numeric
    for col in ["open", "high", "low", "close", "volume"]:
        data_frame[col] = pd.to_numeric(data_frame[col], errors="coerce")

    # fill close
    data_frame["close"] = data_frame["close"].ffill()

    # clean final
    data_frame = (
        data_frame
        .dropna(subset=["date", *FEATURE_COLUMNS])
        .sort_values("date")
        .reset_index(drop=True)
    )

    if data_frame.empty:
        raise RuntimeError(f"Live API returned no usable rows for {symbol}")
    return data_frame.tail(5000)


def load_fallback_data() -> pd.DataFrame:
    if not FALLBACK_CSV.exists():
        return pd.DataFrame(columns=["date", *FEATURE_COLUMNS])

    raw = pd.read_csv(FALLBACK_CSV)
    renamed = raw.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )

    if "date" in renamed.columns:
        renamed["date"] = pd.to_datetime(renamed["date"], errors="coerce")
    else:
        renamed["date"] = pd.bdate_range(end=pd.Timestamp.today(), periods=len(renamed))

    for column in FEATURE_COLUMNS:
        renamed[column] = pd.to_numeric(renamed[column], errors="coerce")

    fallback = renamed.dropna(subset=["date", *FEATURE_COLUMNS]).sort_values("date")
    return fallback[["date", *FEATURE_COLUMNS]].reset_index(drop=True)


def percentage_change(series: pd.Series, periods: int) -> float:
    if len(series) <= periods:
        return float("nan")

    previous = float(series.iloc[-periods - 1])
    current = float(series.iloc[-1])

    if previous == 0:
        return float("nan")

    return (current / previous - 1.0) * 100.0


def render_metrics_panel(price_data: pd.DataFrame) -> None:
    st.markdown("### Metrics Display")

    close_series = price_data["close"].astype(float)
    metrics = [
        ("Daily Change %", percentage_change(close_series, 1)),
        ("Weekly Change %", percentage_change(close_series, 5)),
        ("Monthly Change %", percentage_change(close_series, 21)),
        ("Yearly Change %", percentage_change(close_series, 252)),
    ]

    columns = st.columns(4, gap="small")
    for column, (label, value) in zip(columns, metrics):
        if np.isnan(value):
            column.metric(label, "N/A")
        else:
            sign = "+" if value >= 0 else ""
            column.metric(label, f"{sign}{value:.2f}%")


@st.cache_resource
def load_prediction_model(model_path_str: str) -> StockLSTM | None:
    model_path = Path(model_path_str)
    if not model_path.exists():
        return None

    model = StockLSTM(
        input_size=model_config.INPUT_SIZE,
        hidden_size=model_config.HIDDEN_SIZE,
        num_layers=model_config.NUM_LAYERS,
        dropout=model_config.DROPOUT,
    )

    state_dict = torch.load(model_path, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model



def generate_prediction(price_data: pd.DataFrame, horizon: int, model: StockLSTM | None) -> tuple[pd.DataFrame, str]:
    ordered = price_data.sort_values("date").copy()
    last_date = pd.to_datetime(ordered["date"].iloc[-1])
    next_dates = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=horizon)

    if model is None or len(ordered) <= model_config.SEQUENCE_LENGTH + 1:
        drift = ordered["close"].pct_change().tail(20).mean()
        drift = 0.0 if np.isnan(drift) else float(drift)
        start_price = float(ordered["close"].iloc[-1])
        predictions = [start_price * ((1.0 + drift) ** step) for step in range(1, horizon + 1)]
        return pd.DataFrame({"date": next_dates, "close": predictions}), "Drift baseline"

    values = ordered[FEATURE_COLUMNS].astype(float).values
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_values = scaler.fit_transform(values)

    sequence_length = model_config.SEQUENCE_LENGTH
    sequence = scaled_values[-sequence_length:].copy()
    volume_anchor = float(sequence[-1, 4])

    normalized_predictions: list[float] = []
    with torch.no_grad():
        for _ in range(horizon):
            inputs = torch.tensor(sequence[np.newaxis, :, :], dtype=torch.float32)
            prediction = float(model(inputs).cpu().item())
            prediction = float(np.clip(prediction, 0.0, 1.0))
            normalized_predictions.append(prediction)

            next_row = np.array([prediction, prediction, prediction, prediction, volume_anchor], dtype=np.float32)
            sequence = np.vstack([sequence[1:], next_row])

    close_predictions = []
    for value in normalized_predictions:
        dummy = np.zeros((1, len(FEATURE_COLUMNS)), dtype=np.float32)
        dummy[0, 3] = value
        dummy[0, 4] = volume_anchor
        close_predictions.append(float(scaler.inverse_transform(dummy)[0, 3]))

    prediction_frame = pd.DataFrame({"date": next_dates, "close": close_predictions})
    return prediction_frame, "LSTM model"


def render_symbol_selector() -> str:
    """Selector để chọn mã cổ phiếu từ sidebar"""
    st.sidebar.markdown("## Stock Symbol Selector")
    symbol = st.sidebar.text_input(
        "Enter Stock Code (e.g., VNINDEX, ACB, VNM)",
        value="VNINDEX",
        placeholder="VNINDEX"
    ).upper()
    return symbol if symbol else "VNINDEX"






def render_pipeline_controls(symbol: str = "VNINDEX") -> None:
    st.sidebar.markdown("## Pipeline Controls")

    if st.sidebar.button("Sync Latest Data", use_container_width=True):
        try:
            # Tự động tạo bảng nếu chưa tồn tại
            create_stock_table(symbol)
            # Fetch dữ liệu cho symbol được chọn
            latest_data = fetch_stock_data(symbol=symbol, interval="5m")
            # Lưu vào database
            store_stock_data(symbol=symbol, df=latest_data)
            load_stock_data.clear()
            st.sidebar.success(f"✅ {symbol} data synced to {symbol.lower()}_prices table.")
        except Exception as exc:
            st.sidebar.error(f"❌ Sync failed: {exc}")

    if st.sidebar.button("Run Preprocess Check", use_container_width=True):
        try:
            processed = preprocess_vnindex_data()
            st.sidebar.success(f"Preprocess successful. Rows: {len(processed)}")
        except Exception as exc:
            st.sidebar.error(f"Preprocess failed: {exc}")


def main_app():
    """
    Hàm chứa logic chính của ứng dụng sau khi người dùng đã đăng nhập.
    """
    load_dotenv(ROOT_DIR / ".env")

    st.set_page_config(
        page_title="Stock Financial Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    inject_styles()

    st.sidebar.success(f"Welcome, {st.session_state['username']}!")
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state.pop('username', None)
        # Clear all caches on logout
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

    symbol = render_symbol_selector()

    st.sidebar.markdown("---")
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        if 'username' in st.session_state and st.session_state['username']:
            st.sidebar.markdown(f"👤 **{st.session_state['username']}**")
    with col2:
        st_autorefresh(interval=60_000, key="stock_dashboard_refresh")

    render_pipeline_controls(symbol)

    if st.session_state.pop("model_updated", False):
        load_prediction_model.clear()
        st.session_state["prediction_requested"] = True

    live_exc = None
    db_exc = None
    try:
        price_data = load_live_stock_data(symbol=symbol, interval="5m")
        data_source = f"Live {symbol} API (5m)"
    except Exception as exc:
        live_exc = exc
        try:
            price_data = load_stock_data(symbol=symbol)
            data_source = f"PostgreSQL table: {symbol.lower()}_prices"
            st.warning(f"Live API unavailable ({live_exc}). Switched to database data.")
        except Exception as inner_exc:
            db_exc = inner_exc
            price_data = load_fallback_data()
            data_source = "Fallback CSV"
            st.warning(
                f"Live API unavailable ({live_exc}) and database unavailable ({db_exc}). Switched to fallback CSV dataset."
            )

    if price_data.empty:
        st.error("No usable market data found. Please sync data first.")
        return

    latest_price = float(price_data["close"].iloc[-1])
    day_change = percentage_change(price_data["close"], 1)

    render_header(
        symbol=symbol,
        current_price=latest_price,
        pct_change=0.0 if np.isnan(day_change) else day_change,
        last_updated=pd.to_datetime(price_data["date"].iloc[-1]).to_pydatetime(),
    )

    st.caption(f"Data source: {data_source}")
    st.caption(
        f"Market tick time: {pd.to_datetime(price_data['date'].iloc[-1]).strftime('%Y-%m-%d %H:%M:%S')} | "
        f"App refresh time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    render_metrics_panel(price_data)

    st.markdown("### Timeframe Selector")
    selected_timeframe = render_timeframe_selector(default="6M")
    filtered_data = filter_by_timeframe(price_data, selected_timeframe)

    selected_horizon, should_predict = render_prediction_panel()

    model = load_prediction_model(str(MODEL_PATH))
    prediction_frame = st.session_state.get("prediction_frame", pd.DataFrame())

    if should_predict or prediction_frame.empty:
        prediction_frame, prediction_source = generate_prediction(price_data, selected_horizon, model)
        st.session_state["prediction_frame"] = prediction_frame
        st.session_state["prediction_source"] = prediction_source
    else:
        prediction_source = st.session_state.get("prediction_source", "Unknown")

    if not prediction_frame.empty:
        first_prediction = float(prediction_frame["close"].iloc[0])
        projected_change = (first_prediction / latest_price - 1.0) * 100.0
        sign = "+" if projected_change >= 0 else ""
        st.caption(
            f"Prediction source: {prediction_source} | Next projected close: {first_prediction:,.2f} ({sign}{projected_change:.2f}%)"
        )

    st.markdown("### Main Price Chart + Volume Chart")
    figure = build_price_volume_figure(
        price_data=filtered_data,
        prediction_data=prediction_frame,
        symbol=symbol,
    )
    st.plotly_chart(figure, use_container_width=True)

    render_training_panel(price_data=price_data, model_path=MODEL_PATH)

def run_app():

    # Load CSS toàn app
    inject_styles()

    # Session login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Nếu chưa login
    if not st.session_state['logged_in']:
        show_auth_pages()

    # Nếu đã login
    else:
        main_app()

if __name__ == "__main__":
    # Tải biến môi trường LÀ VIỆC ĐẦU TIÊN
    load_dotenv(ROOT_DIR / ".env")
    
    # Khởi tạo database NGAY SAU KHI có biến môi trường
    # Thao tác này bây giờ sẽ có thông tin đăng nhập chính xác
    initialize_database()
    
    # Chạy ứng dụng
    run_app()
