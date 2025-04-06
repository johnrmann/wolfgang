import mido

def flatten_tracks(
	tracks: list[mido.MidiTrack],
	selected: set[int] = None,
):
	"""
	Flatten a list of MIDI tracks into a single list of MIDI messages.
	"""
	if selected is None:
		selected = set(range(len(tracks)))
	flattened_timed = []
	for i, track in enumerate(tracks):
		if i not in selected:
			continue
		for msg in track:
			if msg.is_meta:
				continue
			time = msg.time
			tuple = (time, msg)
			flattened_timed.append(tuple)
	flattened_sorted = sorted(flattened_timed, key=lambda x: x[0])
	flattened = [tuple[1] for tuple in flattened_sorted]
	return flattened
