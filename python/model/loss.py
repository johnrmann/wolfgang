from core.constants import TOKEN_TYPE_TO_PAYLOAD_LENGTH
from core.utils import read_prefixed_int, count_payload

def consecutive_steps_penalty(target, id2token):
	batch_size, seq_len = target.shape
	penalty = 0.0
	for b in range(batch_size):
		tokens = [id2token[int(i)] for i in target[b]]
		violations = 0
		i = 0
		while i < len(tokens):
			if tokens[i] != 'STEP':
				i += 1
				continue
			while tokens[i] == 'STEP' and i < len(tokens):
				i += 3
				violations += 1
				if i >= len(tokens):
					break
			violations -= 1
		penalty += violations ** 2
	return penalty / batch_size


def zero_length_penalty(target, id2token):
	batch_size, seq_len = target.shape
	penalty = 0.0
	for b in range(batch_size):
		tokens = [id2token[int(i)] for i in target[b]]
		violations = 0
		i = 0
		while i < len(tokens):
			if tokens[i] == 'NOTE' and i + 2 < len(tokens):
				try:
					duration = read_prefixed_int(tokens[i+1], 'D')
					if duration == 0:
						violations += 1
				except ValueError:
					pass
				i += 3
			elif tokens[i] == 'STEP' and i + 2 < len(tokens):
				try:
					beat = read_prefixed_int(tokens[i+1], 'B')
					tick = read_prefixed_int(tokens[i+2], 'T')
					if beat == 0 and tick == 0:
						violations += 1
				except ValueError:
					pass
				i += 3
			else:
				i += 1
		penalty += violations ** 2
	return penalty / batch_size


def malformed_penalty(target, id2token):
	batch_size, seq_len = target.shape
	penalty = 0.0
	for b in range(batch_size):
		tokens = [id2token[int(i)] for i in target[b]]
		violations = 0
		i = 0
		last_control_token = None
		last_payload_count = 0
		while i < len(tokens):
			token = tokens[i]
			if token in TOKEN_TYPE_TO_PAYLOAD_LENGTH:
				if last_control_token is None:
					last_control_token = token
					i += 1
					continue
				if TOKEN_TYPE_TO_PAYLOAD_LENGTH[last_control_token] != last_payload_count:
					violations += 1
				last_control_token = token
				last_payload_count = 0
			else:
				last_payload_count += 1
			i += 1
		if last_control_token is not None and last_payload_count != TOKEN_TYPE_TO_PAYLOAD_LENGTH[last_control_token]:
			violations += 1
		penalty += violations ** 2
	return penalty / batch_size
