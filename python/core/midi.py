import mido

def flatten_tracks(
	tracks: list[mido.MidiTrack],
	selected: set[int] = None,
) -> mido.MidiTrack:
	"""
	Flatten a list of MIDI tracks into a single list of MIDI messages.
	"""
	if selected is None:
		selected = set(range(len(tracks)))
	flattened_timed = []
	for i, track in enumerate(tracks):
		t = 0
		if i not in selected:
			continue
		for msg in track:
			if msg.is_meta:
				continue
			t += msg.time
			tuple = (t, msg)
			flattened_timed.append(tuple)
	flattened_sorted = sorted(flattened_timed, key=lambda x: x[0])
	flattened = [tuple[1] for tuple in flattened_sorted]
	track = mido.MidiTrack()
	for msg in flattened:
		track.append(msg)
	return track


def pick_tracks(
	midi: mido.MidiFile,
	selected: set[int] = None,
) -> mido.MidiFile:
	"""
	Pick a list of MIDI tracks from a MIDI file.
	"""
	new_midi = mido.MidiFile(ticks_per_beat=midi.ticks_per_beat)
	if selected is None:
		selected = set(range(len(midi.tracks)))
	track = flatten_tracks(midi.tracks, selected=selected)
	new_midi.tracks.append(track)
	return new_midi
