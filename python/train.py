import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import glob
import os
import re
import argparse

from model.constants import BATCH_SIZE, EPOCHS, DEVICE
from model.dataset import MidiTokenDataset
from model.loss import sequence_order_penalty, excessive_gap_penalty
from model.model import HybridModel

# Configuration
parser = argparse.ArgumentParser(
	description="Train a Hybrid CNN-Transformer model on MIDI token data."
)
parser.add_argument(
	'--data_path',
	type=str,
	required=True,
	help="Path to the directory containing tokenized MIDI files."
)
parser.add_argument(
	'--model_out',
	type=str,
	required=True,
	help="Path to save the trained model."
)
args = parser.parse_args()

# Data
print("Loading data...")
dataset = MidiTokenDataset(args.data_path)
vocab_size = len(dataset.vocab)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Model, loss, optimizer
model = HybridModel(vocab_size).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
if __name__ == '__main__':
	print("Training...")
	for epoch in range(EPOCHS):
		total_loss = 0
		i = 0
		print(f"Training {len(dataloader)} batches")
		for x, y in dataloader:
			i += 1
			if i == 1000:
				print("Batch 1000")
				i = 0
			x, y = x.to(DEVICE), y.to(DEVICE)
			optimizer.zero_grad()
			output = model(x)
			cr_loss = criterion(output.view(-1, vocab_size), y.view(-1))
			loss = cr_loss
			if epoch == EPOCHS - 1:
				ord_penalty = sequence_order_penalty(y, dataset.id_to_token)
				gap_penalty = excessive_gap_penalty(y, dataset.id_to_token)
				loss = cr_loss + (1.0 * (ord_penalty + gap_penalty))
			loss.backward()
			optimizer.step()
			total_loss += loss.item()
		avg_loss = total_loss / len(dataloader)
		print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {avg_loss:.4f}")

	print("Training completed.")

	# Save model
	torch.save(model.state_dict(), args.model_out)
	print(f"Model saved to {args.model_out}")
