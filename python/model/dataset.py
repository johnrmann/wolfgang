import glob
import os
import torch

from torch.utils.data import Dataset

from core.constants import TokenType, TimeSignature, TICKS_PER_BEAT, BEATS_PER_SONG

from model.constants import SEQ_LENGTH

class MidiTokenDataset(Dataset):
	def __init__(self, data_path, seq_length = SEQ_LENGTH):
		self.seq_length = seq_length
		
		self._generate_vocab()
		self._read_tokens_from_folder(data_path)
		
		self.encoded = [self.token_to_id[t] for t in self.tokens]

	def _generate_vocab(self):
		# Text tokens
		vocab = [v.value for v in TokenType]
		vocab.extend([v.value for v in TimeSignature])
		# Note tokens - beat
		for i in range(BEATS_PER_SONG + 1):
			vocab.append(f"B{i}")
		# Note tokens - tick
		for i in range(TICKS_PER_BEAT):
			vocab.append(f"T{i}")
		# Note tokens - duration
		for i in range(1, TICKS_PER_BEAT * 12):
			vocab.append(f"D{i}")
		# Note tokens - pitch
		for i in range(0, 110):
			vocab.append(f"P{i}")
		# For now, add "120BPM" as the default time signature
		vocab.append("120BPM")
		vocab.append("124BPM")
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
