from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


GREEN = "#2ecc71"
RED = "#e74c3c"


def build_volume_trace(data_frame: pd.DataFrame) -> go.Bar:
    if data_frame.empty:
        return go.Bar(x=[], y=[], name="Volume")

    close_change = data_frame["close"].diff().fillna(0)
    colors = [GREEN if value >= 0 else RED for value in close_change]

    return go.Bar(
        x=data_frame["date"],
        y=data_frame["volume"],
        marker_color=colors,
        name="Volume",
        opacity=0.85,
    )
