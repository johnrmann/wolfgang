from core.constants import MessageType, TempoMarking, TEMPO_MARKING_TO_BPM

def microseconds_per_quarter_to_bpm(microseconds_per_quarter: int) -> float:
	return 60_000_000 / microseconds_per_quarter


def bpm_to_tempo_marking(bpm: float) -> TempoMarking:
	"""
	Given a BPM value, return the corresponding tempo marking.
	"""
	choice = None
	closest_dist = float('inf')
	for marking, marking_bpm in TEMPO_MARKING_TO_BPM.items():
		dist = abs(marking_bpm - bpm)
		if dist < closest_dist:
			closest_dist = dist
			choice = marking
	return choice


def read_prefixed_int(token: str, prefix: str):
	"""
	Given a token, find the first token that starts with the given prefix
	and return the integer value after the prefix. If not found, return None.
	"""
	if len(token) <= len(prefix):
		return None
	if token.startswith(prefix):
		return int(token[len(prefix):])
	return None


def find_prefixed_int(tokens: list[str], prefix: str):
	"""
	Given a list of tokens, find the first token that starts with the given prefix
	and return the integer value after the prefix. If not found, return None.
	"""
	for token in tokens:
		if token.startswith(prefix):
			return read_prefixed_int(token, prefix)
	return None


def count_payload(tokens: list[str]):
	"""
	Given a list of tokens, count the number of consecutive tokens that are not
	a token type.
	"""
	count = 0
	tok_types = [v.value for v in MessageType]
	while count < len(tokens):
		if tokens[count] in tok_types:
			break
		count += 1
	return count
