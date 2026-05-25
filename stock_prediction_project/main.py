"""Project entrypoint for stock price prediction."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from stock_prediction_project import config
from stock_prediction_project.models.lstm_model import StockLSTM
from stock_prediction_project.models.transformer_model import StockTransformer
from stock_prediction_project.data.fetch_and_save_vnindex import save_to_csv
from stock_prediction_project.training.train import evaluate_model, train_model, train_generic_model
from stock_prediction_project.utils.preprocessing import (
	create_sequences,
	load_stock_data,
	prepare_features,
	scale_features,
	train_test_split_sequences,
)


def _build_loader(features: np.ndarray, targets: np.ndarray) -> DataLoader:
	feature_tensor = torch.tensor(features, dtype=torch.float32)
	target_tensor = torch.tensor(targets, dtype=torch.float32)
	dataset = TensorDataset(feature_tensor, target_tensor)
	return DataLoader(dataset, batch_size=config.BATCH_SIZE, shuffle=False)


def evaluate_results(model: torch.nn.Module, test_features: np.ndarray, test_targets: np.ndarray) -> float:
	"""Evaluate the trained model on the test split and print the final loss."""
	device = next(model.parameters()).device
	test_loader = _build_loader(test_features, test_targets)
	criterion = nn.MSELoss()
	test_loss = evaluate_model(model, test_loader, criterion, device)
	print(f"Final test loss: {test_loss:.6f}")
	return test_loss


def run_pipeline(csv_path: str | Path, model_type: str = "lstm") -> None:
	"""Run the full preprocessing and training workflow.
	
	Args:
		csv_path: Path to the CSV file with stock data.
		model_type: Type of model to train ("lstm" or "transformer"). Defaults to "lstm".
	"""
	raw_data = load_stock_data(csv_path)
	cleaned_data = prepare_features(raw_data)
	scaled_values, _ = scale_features(cleaned_data)
	features, targets = create_sequences(scaled_values, config.SEQUENCE_LENGTH)
	train_features, test_features, train_targets, test_targets = train_test_split_sequences(features, targets)

	if len(train_features) == 0 or len(test_features) == 0:
		raise ValueError("Not enough data to build train and test splits.")

	if model_type.lower() == "lstm":
		model = train_model(train_features, train_targets, test_features, test_targets)
	elif model_type.lower() == "transformer":
		model = StockTransformer(
			input_size=config.INPUT_SIZE,
			d_model=64,
			nhead=4,
			num_layers=config.NUM_LAYERS,
			dropout=config.DROPOUT,
		)
		model = train_generic_model(
			model,
			train_features,
			train_targets,
			test_features,
			test_targets,
			model_path="models/best_stock_transformer.pt",
		)
	else:
		raise ValueError(f"Unknown model type: {model_type}. Choose 'lstm' or 'transformer'.")
	
	evaluate_results(model, test_features, test_targets)


if __name__ == "__main__":
	save_to_csv("VNINDEX", years=11)
	# Train LSTM model (default)
	run_pipeline(Path("stock_prediction_project/data/stock_data.csv"), model_type="lstm")
	
	# Uncomment to train Transformer model instead:
	# run_pipeline(default_data_path, model_type="transformer")
