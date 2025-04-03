import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import glob
import os
import re
import argparse

from model.constants import (
	EMBED_SIZE,
	CNN_CHANNELS,
	SEQ_LENGTH,
	N_HEADS,
	TRANSFORMER_LAYERS
)

class HybridModel(nn.Module):
	def __init__(
			self,
			vocab_size,
			embed_size = EMBED_SIZE,
			cnn_channels = CNN_CHANNELS,
			seq_length = SEQ_LENGTH,
			n_heads = N_HEADS,
			n_layers = TRANSFORMER_LAYERS
	):
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
