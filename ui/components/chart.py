from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from utils.candlestick_scaling import (
    calculate_candlestick_range,
    calculate_tick_interval,
    calculate_volume_range,
)
from ui.components.volume_chart import build_volume_trace


def get_price_unit(symbol: str):
    if symbol == "VNINDEX":
        return "điểm", ""
    return "VND", "₫ "


def build_price_volume_figure(
    price_data: pd.DataFrame,
    prediction_data: pd.DataFrame | None = None,
    symbol: str = "VNINDEX",
) -> go.Figure:

    figure = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.04,
        row_heights=[0.74, 0.26],
        subplot_titles=(f"{symbol} Candlestick", "Volume"),
    )

    if price_data.empty:
        figure.update_layout(template="plotly_dark", height=760)
        return figure

    ordered = (
        price_data.sort_values("date")
        .dropna(subset=["date", "open", "high", "low", "close", "volume"])
        .tail(120)
        .copy()
    )

    if ordered.empty:
        figure.update_layout(template="plotly_dark", height=760)
        return figure

    # ======================
    # DATA PREP (QUAN TRỌNG)
    # ======================
    ordered["ema20"] = ordered["close"].ewm(span=20).mean()

    price_min, price_max = calculate_candlestick_range(ordered)
    price_tick = calculate_tick_interval(price_max - price_min)

    volume_min, volume_max = calculate_volume_range(ordered)

    unit_text, prefix = get_price_unit(symbol)

    # ======================
    # CANDLESTICK
    # ======================
    figure.add_trace(
        go.Candlestick(
            x=ordered["date"],
            open=ordered["open"],
            high=ordered["high"],
            low=ordered["low"],
            close=ordered["close"],
            name="OHLC",
            increasing_line_color="#2ecc71",
            decreasing_line_color="#ff4d4d",
            increasing_fillcolor="rgba(0,255,159,0.5)",
            decreasing_fillcolor="rgba(255,77,77,0.5)",
        ),
        row=1,
        col=1,
    )

    # ======================
    # CURRENT PRICE LINE
    # ======================
    current_price = float(ordered["close"].iloc[-1])

    figure.add_trace(
        go.Scatter(
            x=[ordered["date"].iloc[0], ordered["date"].iloc[-1]],
            y=[current_price, current_price],
            mode="lines",
            line=dict(color="#00f5ff", width=3, dash="dot"),
            name=f"Current: {current_price:,.0f}",
            hoverinfo="skip",
        ),
        row=1,
        col=1,
    )

    # ======================
    # PREDICTION
    # ======================
    if prediction_data is not None and not prediction_data.empty:
        prediction_ordered = prediction_data.sort_values("date").copy()

        figure.add_trace(
            go.Scatter(
                x=prediction_ordered["date"],
                y=prediction_ordered["close"],
                mode="lines",
                line=dict(color="#FF9F43", width=2.5, dash="dash"),
                name="Prediction",
            ),
            row=1,
            col=1,
        )

    # ======================
    # EMA
    # ======================
    figure.add_trace(
        go.Scatter(
            x=ordered["date"],
            y=ordered["ema20"],
            mode="lines",
            name="EMA 20",
            line=dict(color="#ffaa00", width=2),
        ),
        row=1,
        col=1,
    )

    # ======================
    # VOLUME
    # ======================
    figure.add_trace(build_volume_trace(ordered), row=2, col=1)

    # ======================
    # LAYOUT
    # ======================
    figure.update_layout(
        template="plotly_dark",
        height=760,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor="#020617",
        plot_bgcolor="#020617",
        font=dict(color="#e6edf3", family="Inter"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="x unified",
        xaxis_rangeslider_visible=False,
    )

    # ======================
    # AXES X
    # ======================
    figure.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        type="category",
        row=1,
        col=1,
    )

    figure.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        type="category",
        row=2,
        col=1,
    )

    # ======================
    # PRICE AXIS
    # ======================
    figure.update_yaxes(
    row=1,
    col=1,

    range=[price_min, price_max],
    autorange=False,

    # 👉 QUAN TRỌNG: chia mốc theo số lượng ít hơn
    nticks=6,   # 👈 chỉ 5–6 mốc là đẹp cho Streamlit

    showgrid=True,
    gridcolor="rgba(255,255,255,0.06)",

    zeroline=False,

    tickformat=",.0f",
    ticks="outside",
    ticklen=5,

    ticksuffix=f" {unit_text}",

    side="right",

    tickfont=dict(
        size=11,
        color="#cbd5e1"
    ),

    title=f"Giá ({unit_text})",
)

    # ======================
    # VOLUME AXIS
    # ======================
    figure.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        range=[volume_min, volume_max],
        autorange=False,
        rangemode="normal",
        row=2,
        col=1,
        tickformat=",.0f",
    )

    return figure