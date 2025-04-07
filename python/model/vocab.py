from core.constants import (
	MessageType,
	TimeSignature,
	TempoMarking,
	MAX_NOTE_DURATION,
	MAX_REST_DURATION
)


class Vocab:
	"""
	Represents the vocabulary of a model, with maps to convert between text
	token and integer token.
	"""
	vocab: list[str]
	token_to_id: dict[str, int]
	id_to_token: dict[int, str]

	CONTROL_TOKEN_IDS: set[int]

	def __init__(self):
		# Control tokens.
		vocab = [v.value for v in MessageType]
		# Time signature tokens.
		vocab.extend([v.value for v in TimeSignature])
		# Note tokens - beat
		for i in range(1, MAX_REST_DURATION + 1):
			vocab.append(f"T{i}")
		# Note tokens - duration
		for i in range(1, MAX_NOTE_DURATION + 1):
			vocab.append(f"D{i}")
		# Note tokens - pitch
		for i in range(0, 110):
			vocab.append(f"P{i}")
		# Tempo marking tokens
		vocab.extend([v.value for v in TempoMarking])
		self.vocab = sorted(set(vocab))
		self.token_to_id = {t: i for i, t in enumerate(self.vocab)}
		self.id_to_token = {i: t for i, t in enumerate(self.vocab)}
		# Create maps.
		self.CONTROL_TOKEN_IDS = set(self.token_to_id[t.value] for t in MessageType)
		self.PITCH_TOKEN_IDS = set(self.token_to_id[f"P{i}"] for i in range(0, 110))
		self.TEMPO_TOKEN_IDS = set(self.token_to_id[t.value] for t in TempoMarking)
		self.DURATION_TOKEN_IDS = set(self.token_to_id[f"D{i}"] for i in range(1, MAX_NOTE_DURATION + 1))
		self.TICK_TOKEN_IDS = set(self.token_to_id[f"T{i}"] for i in range(1, MAX_REST_DURATION + 1))
		self.TIME_SIGNATURE_TOKEN_IDS = set(self.token_to_id[t.value] for t in TimeSignature)
		self.SINGLE_CONTROL_TOKEN_IDS = {self.token_to_id['PAD'], self.token_to_id['END']}

	def __len__(self):
		return len(self.vocab)

	def valid_next_tokens(self, current_ids):
		if len(current_ids) == 0:
			return self.CONTROL_TOKEN_IDS
		last_token = self.id_to_token[current_ids[-1]]
		if last_token == f"T{MAX_REST_DURATION + 1}":
			return self.CONTROL_TOKEN_IDS
		elif last_token.startswith('TS.'):
			return self.CONTROL_TOKEN_IDS
		elif last_token.startswith("T"):
			return self.CONTROL_TOKEN_IDS
		elif last_token.startswith("P"):
			return self.CONTROL_TOKEN_IDS
		elif last_token.startswith("D"):
			return self.PITCH_TOKEN_IDS
		elif last_token in ['PAD', 'END']:
			return self.CONTROL_TOKEN_IDS
		elif last_token == 'NOTE':
			return self.DURATION_TOKEN_IDS
		elif last_token == 'TEMPO':
			return self.TEMPO_TOKEN_IDS
		elif last_token == 'TIMESIG':
			return self.TIME_SIGNATURE_TOKEN_IDS
		elif last_token == 'STEP':
			return self.TICK_TOKEN_IDS
		else:
			return self.CONTROL_TOKEN_IDS