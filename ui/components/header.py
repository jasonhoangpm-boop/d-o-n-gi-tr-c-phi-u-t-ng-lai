from __future__ import annotations

from datetime import datetime

import streamlit as st


def render_header(symbol: str, current_price: float, pct_change: float, last_updated: datetime | None = None) -> None:
    color = "#2ecc71" if pct_change >= 0 else "#e74c3c"
    change_prefix = "+" if pct_change >= 0 else ""
    update_text = last_updated.strftime("%Y-%m-%d %H:%M") if last_updated else "N/A"

    st.markdown(
        f"""
        <div class=\"finance-header\"> 
            <div>
                <p class=\"symbol\">Stock Symbol</p>
                <h1>{symbol}</h1>
            </div>
            <div>
                <p class=\"label\">Current Price</p>
                <h2>{current_price:,.2f}</h2>
            </div>
            <div>
                <p class=\"label\">Daily Change</p>
                <h2 style=\"color:{color};\">{change_prefix}{pct_change:.2f}%</h2>
                <span class=\"updated\">Updated: {update_text}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
