"""Transformer model for stock price prediction."""

from __future__ import annotations

import torch
from torch import nn
import math

import stock_prediction_project.config as config


class PositionalEncoding(nn.Module):
    """Positional encoding for Transformer."""

    pe: torch.Tensor

    def __init__(self, d_model: int, max_len: int = 5000) -> None:
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        if d_model % 2 == 1:
            # When d_model is odd, use div_term[:-1] for odd indices to match shape
            pe[:, 1::2] = torch.cos(position * div_term[:-1])
        else:
            # When d_model is even, use full div_term for odd indices
            pe[:, 1::2] = torch.cos(position * div_term)
        # Register as buffer so it moves to device with model
        self.register_buffer("pe", pe.unsqueeze(0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional encoding to input tensor."""
        return x + self.pe[:, : x.size(1), :]


class StockTransformer(nn.Module):
    """Transformer model for stock price prediction."""

    def __init__(
        self,
        input_size: int = config.INPUT_SIZE,
        d_model: int = 64,
        nhead: int = 4,
        num_layers: int = config.NUM_LAYERS,
        dropout: float = config.DROPOUT,
        dim_feedforward: int = 256,
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.d_model = d_model

        self.input_projection = nn.Linear(input_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model)
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True,
            activation="relu",
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        self.dropout = nn.Dropout(dropout)
        self.regressor = nn.Linear(d_model, 1)

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """Predict the next day closing price for a batch of sequences."""
        # Project input to d_model dimension
        x = self.input_projection(inputs)
        
        # Add positional encoding
        x = self.positional_encoding(x)
        
        # Apply transformer encoder
        transformer_output = self.transformer_encoder(x)
        
        # Use the last token's output
        last_step = transformer_output[:, -1, :]
        
        # Apply dropout
        dropped = self.dropout(last_step)
        
        # Regression head
        return self.regressor(dropped).squeeze(-1)
