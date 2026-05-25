from __future__ import annotations

import streamlit as st


HORIZON_OPTIONS = [1, 7, 30]


def render_prediction_panel() -> tuple[int, bool]:
    st.markdown("### Prediction Panel")

    if "prediction_horizon" not in st.session_state:
        st.session_state["prediction_horizon"] = 7
    if "prediction_requested" not in st.session_state:
        st.session_state["prediction_requested"] = True

    columns = st.columns(len(HORIZON_OPTIONS), gap="small")
    for column, days in zip(columns, HORIZON_OPTIONS):
        label = "1 day" if days == 1 else f"{days} days"
        button_type = "primary" if st.session_state["prediction_horizon"] == days else "secondary"
        if column.button(label, key=f"horizon_{days}", use_container_width=True, type=button_type):
            st.session_state["prediction_horizon"] = days
            st.session_state["prediction_requested"] = True

    selected_horizon = int(st.session_state["prediction_horizon"])
    run_prediction = bool(st.session_state.get("prediction_requested", False))
    st.session_state["prediction_requested"] = False

    st.caption(f"Selected horizon: {selected_horizon} trading day(s)")
    return selected_horizon, run_prediction
