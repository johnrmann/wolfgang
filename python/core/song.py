import mido

from .token import Token, Note, ChangeTimeSignature, ChangeTempo, EndOfSong
from core.constants import TokenType

def song_event_to_mido_message(event):
	delta_time = event[0]
	message_type = event[1]
	if message_type == 'note_on':
		return mido.Message('note_on', note=event[2], velocity=64, time=delta_time)
	elif message_type == 'note_off':
		return mido.Message('note_off', note=event[2], velocity=64, time=delta_time)
	elif message_type == 'time_signature':
		return mido.MetaMessage('time_signature', numerator=event[2], denominator=event[3], time=delta_time)
	elif message_type == 'set_tempo':
		tempo = mido.bpm2tempo(event[2])
		print(tempo)
		return mido.MetaMessage('set_tempo', tempo=tempo, time=delta_time)
	else:
		raise ValueError("Invalid message type")


class Song:
	_tokens: list[Token]

	def __init__(self, tokens: list[Token] = None):
		if tokens is None:
			tokens = []
		self._tokens = tokens[:]

	@staticmethod
	def from_text(texts: list[str]):
		token_list = []
		i = 0
		while i < len(texts):
			text = texts[i]
			if text == TokenType.PAD.value:
				i += 1
			elif text == TokenType.NOTE.value:
				if i + 4 >= len(texts):
					break
				beat = texts[i + 1]
				tick = texts[i + 2]
				duration = texts[i + 3]
				pitch = texts[i + 4]
				note = Note.from_text(beat, tick, duration, pitch)
				if note:
					token_list.append(note)
				i += 5
			elif text == TokenType.TIMESIG.value:
				# For now, just assume everything is 4/4
				token_list.append(ChangeTimeSignature(time_signature=(4, 4), ticks=0))
				i += 4
			elif text == TokenType.TEMPO.value:
				tempo = int(texts[i + 3])
				token_list.append(ChangeTempo(tempo, ticks=0))
				i += 4
			elif text == TokenType.END.value:
				i += 1
				token_list.append(EndOfSong())
				break
		token_list = sorted(token_list)
		return Song(token_list)

	def _message_tuples(self):
		for token in self._tokens:
			if isinstance(token, Note):
				yield token.start_midi, "note_on", token.pitch
				yield token.end_midi, "note_off", token.pitch
			elif isinstance(token, ChangeTimeSignature):
				yield token.start_midi, "time_signature", *token.time_signature
			elif isinstance(token, ChangeTempo):
				yield token.start_midi, "set_tempo", token.tempo
	
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
