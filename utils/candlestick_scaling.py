from __future__ import annotations

from typing import Tuple

import pandas as pd


def _positive_padding(value_range: float, ratio: float) -> float:
    padding = value_range * ratio
    return padding if padding > 0 else ratio


def calculate_candlestick_range(df: pd.DataFrame) -> Tuple[float, float]:
    """Return padded y-axis limits for candlestick prices using LOW/HIGH percentiles."""
    if df.empty:
        return 0.0, 1.0

    lows = pd.to_numeric(df["low"], errors="coerce").dropna()
    highs = pd.to_numeric(df["high"], errors="coerce").dropna()
    if lows.empty or highs.empty:
        return 0.0, 1.0

    low_percentile = float(lows.quantile(0.02))
    high_percentile = float(highs.quantile(0.98))

    if high_percentile <= low_percentile:
        min_val = float(lows.min())
        max_val = float(highs.max())
    else:
        min_val = low_percentile
        max_val = high_percentile

    price_range = max_val - min_val
    padding = _positive_padding(price_range, 0.05)

    y_min = min_val - padding
    y_max = max_val + padding
    return y_min, y_max


def calculate_volume_range(df: pd.DataFrame) -> Tuple[float, float]:
    """Return percentile-based y-axis limits for volume without forced zero baseline."""
    if df.empty:
        return 0.0, 1.0

    volumes = pd.to_numeric(df["volume"], errors="coerce").dropna()
    if volumes.empty:
        return 0.0, 1.0

    min_val = float(volumes.quantile(0.05))
    max_val = float(volumes.quantile(0.98))

    if max_val <= min_val:
        min_val = float(volumes.min())
        max_val = float(volumes.max())

    volume_range = max_val - min_val
    padding = _positive_padding(volume_range, 0.10)

    y_min = min_val - padding
    y_max = max_val + padding

    if float(volumes.min()) <= 0:
        y_min = min(y_min, 0.0)

    return y_min, y_max


def calculate_tick_interval(range_value: float) -> float:
    if range_value < 50:
        return 5.0
    if range_value < 200:
        return 10.0
    if range_value < 1000:
        return 50.0
    return 100.0
