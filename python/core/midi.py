import mido

MessageTuple = tuple[int, mido.Message]


def sort_messages(mido_msgs: list[MessageTuple]) -> list[mido.Message]:
	"""
	Sort a list of MIDI messages by time.
	"""
	sorted_msgs = sorted(mido_msgs, key=lambda x: x[0])
	# Loop through the messages and set the time to the difference from the
	# previous message.
	retimed = [sorted_msgs[0][1]]
	for i in range(1, len(sorted_msgs)):
		last_time, _ = sorted_msgs[i - 1]
		this_time, this_msg = sorted_msgs[i]
		this_msg.time = this_time - last_time
		retimed.append(this_msg)
	return [msg for _, msg in sorted_msgs]


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
				is_tempo = msg.type == "set_tempo"
				is_time_signature = msg.type == "time_signature"
				if not is_tempo and not is_time_signature:
					continue
			t += msg.time
			tuple = (t, msg)
			flattened_timed.append(tuple)
	flattened = sort_messages(flattened_timed)
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
