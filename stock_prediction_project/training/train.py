"""Training loop for the stock prediction model."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from stock_prediction_project import config
from stock_prediction_project.models.lstm_model import StockLSTM


def _build_loader(features: np.ndarray, targets: np.ndarray, batch_size: int, shuffle: bool) -> DataLoader:
    feature_tensor = torch.tensor(features, dtype=torch.float32)
    target_tensor = torch.tensor(targets, dtype=torch.float32)
    dataset = TensorDataset(feature_tensor, target_tensor)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def evaluate_model(model: StockLSTM, data_loader: DataLoader, criterion: nn.Module, device: torch.device) -> float:
    """Compute average loss on the validation/test set."""
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for batch_features, batch_targets in data_loader:
            batch_features = batch_features.to(device)
            batch_targets = batch_targets.to(device)
            predictions = model(batch_features)
            loss = criterion(predictions, batch_targets)
            total_loss += loss.item() * batch_features.size(0)

    return total_loss / len(data_loader.dataset)


def train_model(
    train_features: np.ndarray,
    train_targets: np.ndarray,
    test_features: np.ndarray,
    test_targets: np.ndarray,
    model_path: str | Path = "models/best_stock_lstm.pt",
) -> StockLSTM:
    """Train the model and save the best checkpoint."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    train_loader = _build_loader(train_features, train_targets, config.BATCH_SIZE, shuffle=True)
    test_loader = _build_loader(test_features, test_targets, config.BATCH_SIZE, shuffle=False)

    model = StockLSTM(
        input_size=config.INPUT_SIZE,
        hidden_size=config.HIDDEN_SIZE,
        num_layers=config.NUM_LAYERS,
        dropout=config.DROPOUT,
    ).to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    best_loss = float("inf")
    epochs_without_improvement = 0
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, config.EPOCHS + 1):
        model.train()
        running_loss = 0.0

        for batch_features, batch_targets in train_loader:
            batch_features = batch_features.to(device)
            batch_targets = batch_targets.to(device)

            optimizer.zero_grad()
            predictions = model(batch_features)
            loss = criterion(predictions, batch_targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_features.size(0)

        train_loss = running_loss / len(train_loader.dataset)
        validation_loss = evaluate_model(model, test_loader, criterion, device)
        print(f"Epoch {epoch}/{config.EPOCHS} - train_loss: {train_loss:.6f} - val_loss: {validation_loss:.6f}")

        if validation_loss < best_loss:
            best_loss = validation_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), model_path)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.EARLY_STOPPING_PATIENCE:
                print(
                    f"Early stopping triggered at epoch {epoch} after "
                    f"{config.EARLY_STOPPING_PATIENCE} epochs without improvement."
                )
                break

    model.load_state_dict(torch.load(model_path, map_location=device))

    return model


def train_generic_model(
    model: nn.Module,
    train_features: np.ndarray,
    train_targets: np.ndarray,
    test_features: np.ndarray,
    test_targets: np.ndarray,
    model_path: str | Path = "models/best_stock_model.pt",
) -> nn.Module:
    """Train any PyTorch model and save the best checkpoint."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    train_loader = _build_loader(train_features, train_targets, config.BATCH_SIZE, shuffle=True)
    test_loader = _build_loader(test_features, test_targets, config.BATCH_SIZE, shuffle=False)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=config.LEARNING_RATE)

    best_loss = float("inf")
    epochs_without_improvement = 0
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, config.EPOCHS + 1):
        model.train()
        running_loss = 0.0

        for batch_features, batch_targets in train_loader:
            batch_features = batch_features.to(device)
            batch_targets = batch_targets.to(device)

            optimizer.zero_grad()
            predictions = model(batch_features)
            loss = criterion(predictions, batch_targets)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * batch_features.size(0)

        train_loss = running_loss / len(train_loader.dataset)
        validation_loss = evaluate_model(model, test_loader, criterion, device)
        print(f"Epoch {epoch}/{config.EPOCHS} - train_loss: {train_loss:.6f} - val_loss: {validation_loss:.6f}")

        if validation_loss < best_loss:
            best_loss = validation_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), model_path)
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.EARLY_STOPPING_PATIENCE:
                print(
                    f"Early stopping triggered at epoch {epoch} after "
                    f"{config.EARLY_STOPPING_PATIENCE} epochs without improvement."
                )
                break

    model.load_state_dict(torch.load(model_path, map_location=device))
    return model