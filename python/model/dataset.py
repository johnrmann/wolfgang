import glob
import os
import torch

from torch.utils.data import Dataset

from core.constants import MessageType, TimeSignature, MAX_NOTE_DURATION, MAX_REST_DURATION

from model.constants import SEQ_LENGTH

class MidiTokenDataset(Dataset):
	def __init__(self, data_path = None, seq_length = SEQ_LENGTH):
		self.seq_length = seq_length
		
		self._generate_vocab()
		if data_path is not None:
			self._read_tokens_from_folder(data_path)
			self.encoded = [self.token_to_id[t] for t in self.tokens]
		
	def _generate_vocab(self):
		# Text tokens
		vocab = [v.value for v in MessageType]
		vocab.extend([v.value for v in TimeSignature])
		# Note tokens - beat
		for i in range(MAX_REST_DURATION):
			vocab.append(f"T{i}")
		# Note tokens - duration
		for i in range(1, MAX_NOTE_DURATION):
			vocab.append(f"D{i}")
		# Note tokens - pitch
		for i in range(0, 110):
			vocab.append(f"P{i}")
		# For now, add "120BPM" as the default time signature
		vocab.append("BPM120")
		vocab.append("BPM124")
		self.vocab = sorted(set(vocab))
		self.token_to_id = {t: i for i, t in enumerate(self.vocab)}
		self.id_to_token = {i: t for i, t in enumerate(self.vocab)}

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

	def pad_sequence(self, sequence):
		# Pad to SEQ_LENGTH if needed
		if len(sequence) < self.seq_length:
			pad_token = self.token_to_id["PAD"]
			seq2 = [pad_token] * (self.seq_length - len(sequence)) + sequence
			return seq2
		else:
			return sequence
