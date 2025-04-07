import glob
import os
import torch

from torch.utils.data import Dataset

from core.constants import MessageType, TimeSignature, MAX_NOTE_DURATION, MAX_REST_DURATION

from model.constants import SEQ_LENGTH
from model.vocab import Vocab

class MidiTokenDataset(Dataset):
	def __init__(self, data_path = None, seq_length = SEQ_LENGTH):
		self.seq_length = seq_length
		
		self.vocab = Vocab()
		if data_path is not None:
			self._read_tokens_from_folder(data_path)
			self.encoded = [self.token_to_id[t] for t in self.tokens]

	def _read_tokens_from_folder(self, data_path):
		self.files = sorted(glob.glob(os.path.join(data_path, '*.tok')))
		self.tokens = []
		for f in self.files:
			with open(f, 'r') as file:
				content = file.read()
				lines = content.split('\n')
				for line in lines:
					self.tokens.extend(line.strip().split())

	def __len__(self):
		return len(self.tokens) - self.seq_length

	def __getitem__(self, idx):
		x = torch.tensor(self.encoded[idx:idx+self.seq_length])
		y = torch.tensor(self.encoded[idx+1:idx+self.seq_length+1])
		return x, y

	@property
	def id_to_token(self):
		return self.vocab.id_to_token

	@property
	def token_to_id(self):
		return self.vocab.token_to_id

	def _pad_sequence_int(self, sequence: list[int]) -> list[int]:
		# Pad to SEQ_LENGTH if needed
		if len(sequence) < self.seq_length:
			pad_token = self.token_to_id["PAD"]
			seq2 = [pad_token] * (self.seq_length - len(sequence)) + sequence
			return seq2
		else:
			return sequence

	def _pad_sequence_str(self, sequence: list[str]) -> list[str]:
		# Pad to SEQ_LENGTH if needed
		if len(sequence) < self.seq_length:
			pad_token = "PAD"
			seq2 = [pad_token] * (self.seq_length - len(sequence)) + sequence
			return seq2
		else:
			return sequence

	def pad_sequence(self, sequence: list[str] | list[int]) -> list[int] | list[str]:
		if isinstance(sequence[0], int):
			return self._pad_sequence_int(sequence)
		else:
			return self._pad_sequence_str(sequence)
