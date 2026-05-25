"""LSTM model for stock price prediction."""

from __future__ import annotations

import torch
from torch import nn

from stock_prediction_project import config


class StockLSTM(nn.Module):
    """Sequence model that predicts the next closing price."""

    def __init__(
        self,
        input_size: int = config.INPUT_SIZE,
        hidden_size: int = config.HIDDEN_SIZE,
        num_layers: int = config.NUM_LAYERS,
        dropout: float = config.DROPOUT,
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.dropout_rate = dropout

        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0.0,
            batch_first=True,
        )
        self.dropout = nn.Dropout(dropout)
        self.regressor = nn.Linear(hidden_size, 1)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Predict the next day closing price for a batch of sequences."""
        lstm_output, _ = self.lstm(inputs)
        last_step = lstm_output[:, -1, :]
        dropped = self.dropout(last_step)
        return self.regressor(dropped).squeeze(-1)
