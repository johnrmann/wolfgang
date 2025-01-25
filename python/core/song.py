import mido

from .token import Token, Note

def song_event_to_mido_message(event):
	delta_time = event[0]
	message_type = event[1]
	if message_type == 'note_on':
		return mido.Message('note_on', note=event[2], velocity=64, time=delta_time)
	elif message_type == 'note_off':
		return mido.Message('note_off', note=event[2], velocity=64, time=delta_time)
	else:
		raise ValueError("Invalid message type")


class Song:
	_tokens: list[Token]

	def __init__(self, tokens: list[Token] = None):
		if tokens is None:
			tokens = []
		self._tokens = tokens[:]

	def _message_tuples(self):
		for token in self._tokens:
			if isinstance(token, Note):
				yield token.start_midi, "note_on", token.pitch
				yield token.end_midi, "note_off", token.pitch
	
	def _sorted_message_tuples(self):
		return sorted(self._message_tuples())
	
	def message_tuples(self):
		time_idxed = self._sorted_message_tuples()
		posts = time_idxed[1:]
		pres = time_idxed[:-1]
		pairs = zip(posts, pres)
		yield time_idxed[0]
		for post, pre in pairs:
			post_time = post[0]
			payload = post[1:]
			pre_time = pre[0]
			delta_time = post_time - pre_time
			yield delta_time, *payload

	def to_midi(self):
		events = self.message_tuples()
		mid = mido.MidiFile()
		track = mido.MidiTrack()
		mid.tracks.append(track)
		for event in events:
			track.append(song_event_to_mido_message(event))
		return mid
