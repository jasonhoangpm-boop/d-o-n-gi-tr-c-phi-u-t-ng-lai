"""Data preprocessing helpers for stock price prediction."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


FEATURE_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def load_stock_data(csv_path: str | Path) -> pd.DataFrame:
    """Load raw stock data from a CSV file."""
    data_frame = pd.read_csv(csv_path)
    missing_columns = [column for column in FEATURE_COLUMNS if column not in data_frame.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")
    return data_frame.copy()


def prepare_features(data_frame: pd.DataFrame) -> pd.DataFrame:
    """Keep the expected columns and remove empty rows."""
    cleaned_frame = data_frame.loc[:, FEATURE_COLUMNS].copy()
    cleaned_frame = cleaned_frame.dropna().reset_index(drop=True)
    return cleaned_frame


def scale_features(data_frame: pd.DataFrame) -> tuple[np.ndarray, MinMaxScaler]:
    """Scale all input features to the 0-1 range."""
    scaler = MinMaxScaler()
    scaled_values = scaler.fit_transform(data_frame[FEATURE_COLUMNS].values)
    return scaled_values, scaler


def create_sequences(
    scaled_values: np.ndarray,
    sequence_length: int,
) -> Tuple[np.ndarray, np.ndarray]:
    """Create sliding window sequences and next-step targets."""
    features = []
    targets = []

    for index in range(sequence_length, len(scaled_values)):
        features.append(scaled_values[index - sequence_length:index])
        targets.append(scaled_values[index, 3])

    return np.array(features), np.array(targets)


def train_test_split_sequences(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.8,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Split sequences into train and test sets without shuffling."""
    split_index = int(len(features) * train_ratio)
    return (
        features[:split_index],
        features[split_index:],
        targets[:split_index],
        targets[split_index:],
    )