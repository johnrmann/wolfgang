def microseconds_per_quarter_to_bpm(microseconds_per_quarter: int) -> float:
	return 60_000_000 / microseconds_per_quarter


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
