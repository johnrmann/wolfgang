from core.constants import TICKS_PER_BEAT

# Custom loss function with order constraint (augmenting default CE loss)
def sequence_order_penalty(target, id2token):
	batch_size, seq_len = target.shape
	penalty = 0.0
	for b in range(batch_size):
		tokens = [id2token[int(i)] for i in target[b]]
		note_times = []
		i = 0
		while i < len(tokens):
			if tokens[i] == 'NOTE' and i + 4 < len(tokens):
				try:
					beat = int(tokens[i+1])
					tick = int(tokens[i+2])
					time = beat * TICKS_PER_BEAT + tick
					note_times.append(time)
				except ValueError:
					pass
				i += 5
			else:
				i += 1
		for j in range(1, len(note_times)):
			if note_times[j] < note_times[j-1]:
				penalty += (note_times[j-1] - note_times[j]) ** 2 

	return penalty / batch_size  # average over batch

def excessive_gap_penalty(target, id2token, penalty_beats=6):
	batch_size, seq_len = target.shape
	penalty = 0.0
	penalty_ticks = penalty_beats * TICKS_PER_BEAT
	for b in range(batch_size):
		tokens = [id2token[int(i)] for i in target[b]]
		note_times = []
		i = 0
		while i < len(tokens):
			if tokens[i] == 'NOTE' and i + 4 < len(tokens):
				try:
					beat = int(tokens[i+1])
					tick = int(tokens[i+2])
					time = beat * TICKS_PER_BEAT + tick
					note_times.append(time)
				except ValueError:
					pass
				i += 5
			else:
				i += 1
		for j in range(1, len(note_times)):
			gap = note_times[j] - note_times[j-1]
			if gap > penalty_ticks:
				penalty += (gap - penalty_ticks) ** 2
	return penalty / batch_size
