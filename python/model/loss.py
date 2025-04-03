from core.constants import TICKS_PER_BEAT
from core.utils import read_prefixed_int

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
