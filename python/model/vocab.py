from core.constants import (
	MessageType,
	TimeSignature,
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

	def __init__(self):
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
		