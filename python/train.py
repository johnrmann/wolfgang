import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import glob
import os
import re
import argparse

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

DATA_PATH = args.data_path
DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
SEQ_LENGTH = 128
BATCH_SIZE = 16
EMBED_SIZE = 128
N_HEADS = 4
TRANSFORMER_LAYERS = 4
CNN_CHANNELS = 64
EPOCHS = 5

# Simple Tokenizer and Dataset class
class MidiTokenDataset(Dataset):
	def __init__(self, data_path):
		self.files = sorted(glob.glob(os.path.join(data_path, '*.tok')))
		self.tokens = []
		for f in self.files:
			with open(f, 'r') as file:
				content = file.read()
				lines = content.split('\n')
				for line in lines:
					self.tokens.extend(line.strip().split())
		
		self.vocab = sorted(set(self.tokens))
		self.token_to_id = {t: i for i, t in enumerate(self.vocab)}
		self.id_to_token = {i: t for i, t in enumerate(self.vocab)}
		
		self.encoded = [self.token_to_id[t] for t in self.tokens]

	def __len__(self):
		return len(self.tokens) - SEQ_LENGTH

	def __getitem__(self, idx):
		x = torch.tensor(self.encoded[idx:idx+SEQ_LENGTH])
		y = torch.tensor(self.encoded[idx+1:idx+SEQ_LENGTH+1])
		return x, y

# Hybrid CNN-Transformer Model
class HybridModel(nn.Module):
	def __init__(self, vocab_size, embed_size, cnn_channels, seq_length, n_heads, n_layers):
		super().__init__()
		self.embedding = nn.Embedding(vocab_size, embed_size)
		self.conv = nn.Sequential(
			nn.Conv1d(embed_size, cnn_channels, kernel_size=3, padding=1),
			nn.ReLU(),
			nn.Conv1d(cnn_channels, embed_size, kernel_size=3, padding=1)
		)
		encoder_layer = nn.TransformerEncoderLayer(d_model=embed_size, nhead=n_heads)
		self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
		self.fc_out = nn.Linear(embed_size, vocab_size)

	def forward(self, x):
		x = self.embedding(x).permute(0, 2, 1)
		x = self.conv(x).permute(2, 0, 1)
		x = self.transformer(x)
		return self.fc_out(x.permute(1, 0, 2))

# Data
print("Loading data...")
dataset = MidiTokenDataset(DATA_PATH)
vocab_size = len(dataset.vocab)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Model, loss, optimizer
model = HybridModel(vocab_size, EMBED_SIZE, CNN_CHANNELS, SEQ_LENGTH, N_HEADS, TRANSFORMER_LAYERS).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training Loop
if __name__ == '__main__':
	print("Training...")
	for epoch in range(EPOCHS):
		total_loss = 0
		for x, y in dataloader:
			x, y = x.to(DEVICE), y.to(DEVICE)
			optimizer.zero_grad()
			output = model(x)
			loss = criterion(output.view(-1, vocab_size), y.view(-1))
			loss.backward()
			optimizer.step()
			total_loss += loss.item()
		avg_loss = total_loss / len(dataloader)
		print(f"Epoch {epoch+1}/{EPOCHS}, Loss: {avg_loss:.4f}")

	print("Training completed.")

	# Save model
	torch.save(model.state_dict(), args.model_out)
	print(f"Model saved to {args.model_out}")
