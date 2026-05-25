from __future__ import annotations

import pandas as pd
import streamlit as st


TIMEFRAME_OPTIONS = ["1D", "1W", "1M", "3M", "6M", "1Y", "5Y", "MAX"]
TIMEFRAME_TO_DAYS = {
    "1D": 1,
    "1W": 7,
    "1M": 30,
    "3M": 90,
    "6M": 180,
    "1Y": 365,
    "5Y": 365 * 5,
}


def render_timeframe_selector(default: str = "6M") -> str:
    if "selected_timeframe" not in st.session_state:
        st.session_state["selected_timeframe"] = default

    columns = st.columns(len(TIMEFRAME_OPTIONS), gap="small")
    for column, option in zip(columns, TIMEFRAME_OPTIONS):
        button_type = "primary" if st.session_state["selected_timeframe"] == option else "secondary"
        if column.button(option, key=f"timeframe_{option}", use_container_width=True, type=button_type):
            st.session_state["selected_timeframe"] = option

    return st.session_state["selected_timeframe"]


def filter_by_timeframe(data_frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    if data_frame.empty or timeframe == "MAX":
        return data_frame.copy()

    ordered = data_frame.sort_values("date").copy()

    if timeframe == "1D":
        return ordered.tail(1).reset_index(drop=True)

    days = TIMEFRAME_TO_DAYS.get(timeframe)
    if days is None:
        return ordered.reset_index(drop=True)

    max_date = ordered["date"].max()
    cutoff = max_date - pd.Timedelta(days=days)
    filtered = ordered[ordered["date"] >= cutoff].copy()
    return filtered.reset_index(drop=True)
