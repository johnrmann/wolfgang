import torch
import torch.nn as nn
import torch.optim as optim
import glob
import os
import re
import argparse

from tqdm import tqdm
from torch.utils.data import Dataset, DataLoader

from model.constants import BATCH_SIZE, DEVICE
from model.dataset import MidiTokenDataset
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
parser.add_argument(
	'--epochs',
	type=int,
	default=10,
	help="Number of training epochs."
)
parser.add_argument(
	'--bars',
	type=bool,
	default=False,
	help="Progress bars?"
)
args = parser.parse_args()

# Data
print("Loading data...")
dataset = MidiTokenDataset(args.data_path)
vocab_size = len(dataset.vocab)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
bars = args.bars

# Model, loss, optimizer
model = HybridModel(vocab_size).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
if __name__ == '__main__':
	print("Training...")
	for epoch in tqdm(range(args.epochs), disable=not bars):
		total_loss = 0
		inner_count = tqdm(
			total=len(dataloader),
			desc=f"Epoch {epoch+1}/{args.epochs}",
			disable=not bars,
		)
		for x, y in dataloader:
			x, y = x.to(DEVICE), y.to(DEVICE)
			optimizer.zero_grad()
			output = model(x)
			cr_loss = criterion(output.view(-1, vocab_size), y.view(-1))
			loss = cr_loss
			loss.backward()
			optimizer.step()
			total_loss += loss.item()
			inner_count.update(1)
		inner_count.close()
		avg_loss = total_loss / len(dataloader)
		print(f"Epoch {epoch+1}/{args.epochs}, Loss: {avg_loss:.4f}")

	print("Training completed.")

	# Save model
	torch.save(model.state_dict(), args.model_out)
	print(f"Model saved to {args.model_out}")
