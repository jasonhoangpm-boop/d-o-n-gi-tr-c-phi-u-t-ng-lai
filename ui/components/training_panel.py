from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import torch
from sklearn.preprocessing import MinMaxScaler
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

import stock_prediction_project.config as model_config
from stock_prediction_project.models.lstm_model import StockLSTM


FEATURE_COLUMNS = ["open", "high", "low", "close", "volume"]


def _prepare_training_data(data_frame: pd.DataFrame, sequence_length: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    values = data_frame[FEATURE_COLUMNS].astype(float).dropna().values
    if len(values) <= sequence_length + 20:
        raise ValueError("Not enough rows for training. Please load more historical data.")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)

    features = []
    targets = []
    for index in range(sequence_length, len(scaled)):
        features.append(scaled[index - sequence_length:index])
        targets.append(scaled[index, 3])

    feature_array = np.array(features, dtype=np.float32)
    target_array = np.array(targets, dtype=np.float32)

    split_index = int(len(feature_array) * 0.8)
    split_index = min(max(split_index, 1), len(feature_array) - 1)

    train_x = feature_array[:split_index]
    train_y = target_array[:split_index]
    val_x = feature_array[split_index:]
    val_y = target_array[split_index:]
    return train_x, train_y, val_x, val_y


def _evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module, device: torch.device) -> float:
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for features, targets in loader:
            features = features.to(device)
            targets = targets.to(device)
            predictions = model(features)
            batch_loss = criterion(predictions, targets)
            total_loss += batch_loss.item() * features.size(0)

    return total_loss / len(loader.dataset)


def _train_model(
    data_frame: pd.DataFrame,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    model_path: Path,
    progress_bar,
    status_placeholder,
) -> dict[str, list[float]]:
    train_x, train_y, val_x, val_y = _prepare_training_data(data_frame, model_config.SEQUENCE_LENGTH)

    train_loader = DataLoader(
        TensorDataset(torch.from_numpy(train_x), torch.from_numpy(train_y)),
        batch_size=batch_size,
        shuffle=True,
    )
    val_loader = DataLoader(
        TensorDataset(torch.from_numpy(val_x), torch.from_numpy(val_y)),
        batch_size=batch_size,
        shuffle=False,
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = StockLSTM(
        input_size=5,
        hidden_size=model_config.HIDDEN_SIZE,
        num_layers=model_config.NUM_LAYERS,
        dropout=model_config.DROPOUT,
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    model_path.parent.mkdir(parents=True, exist_ok=True)
    best_val_loss = float("inf")
    history: dict[str, list[float]] = {"train_loss": [], "val_loss": []}

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0

        for features, targets in train_loader:
            features = features.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            predictions = model(features)
            loss = criterion(predictions, targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * features.size(0)

        train_loss = running_loss / len(train_loader.dataset)
        val_loss = _evaluate(model, val_loader, criterion, device)

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), model_path)

        progress_bar.progress(int(epoch / epochs * 100))
        status_placeholder.caption(
            f"Epoch {epoch}/{epochs} | train_loss={train_loss:.6f} | val_loss={val_loss:.6f}"
        )

    return history


def _build_loss_figure(history: dict[str, list[float]]) -> go.Figure:
    epochs = list(range(1, len(history["train_loss"]) + 1))

    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=epochs,
            y=history["train_loss"],
            mode="lines+markers",
            name="Train Loss",
            line=dict(color="#4DA3FF", width=2),
        )
    )
    figure.add_trace(
        go.Scatter(
            x=epochs,
            y=history["val_loss"],
            mode="lines+markers",
            name="Validation Loss",
            line=dict(color="#FF9F43", width=2),
        )
    )

    figure.update_layout(
        template="plotly_dark",
        margin=dict(l=12, r=12, t=32, b=12),
        xaxis_title="Epoch",
        yaxis_title="Loss",
        height=320,
        hovermode="x unified",
    )
    return figure


def render_training_panel(price_data: pd.DataFrame, model_path: Path) -> None:
    st.markdown("### Model Training Panel")
    with st.expander("Model Training", expanded=False):
        cols = st.columns(3, gap="small")
        epochs = int(
            cols[0].number_input(
                "Epochs",
                min_value=1,
                max_value=500,
                value=int(model_config.EPOCHS),
                step=1,
            )
        )
        batch_size = int(
            cols[1].number_input(
                "Batch Size",
                min_value=8,
                max_value=1024,
                value=int(model_config.BATCH_SIZE),
                step=8,
            )
        )
        learning_rate = float(
            cols[2].number_input(
                "Learning Rate",
                min_value=0.00001,
                max_value=1.0,
                value=float(model_config.LEARNING_RATE),
                step=0.0001,
                format="%.5f",
            )
        )

        start_training = st.button("Start Training", type="primary", use_container_width=True)

        if start_training:
            if price_data.empty:
                st.error("Training cannot start because the source data is empty.")
            else:
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                try:
                    history = _train_model(
                        data_frame=price_data,
                        epochs=epochs,
                        batch_size=batch_size,
                        learning_rate=learning_rate,
                        model_path=model_path,
                        progress_bar=progress_bar,
                        status_placeholder=status_placeholder,
                    )
                    st.session_state["training_history"] = history
                    st.session_state["model_updated"] = True
                    st.success("Training completed. Model checkpoint was updated.")
                except Exception as exc:
                    st.error(f"Training failed: {exc}")

        if "training_history" in st.session_state:
            st.plotly_chart(_build_loss_figure(st.session_state["training_history"]), use_container_width=True)
