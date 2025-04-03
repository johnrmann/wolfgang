import mido

from .token import Token, Note, Step, ChangeTimeSignature, ChangeTempo, EndOfSong, merge_adjacent_steps
from core.constants import TokenType, TICKS_PER_BEAT
from core.utils import read_prefixed_int

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
		print(f"Tempo... {tempo}")
		return mido.MetaMessage('set_tempo', tempo=tempo, time=delta_time)
	else:
		raise ValueError("Invalid message type")


class Song:
	_tokens: list[Token]
	_midi_ticks_per_beat: int

	def __init__(
		self,
		tokens: list[Token] = None,
		midi_ticks_per_beat: int = 480
	):
		if tokens is None:
			tokens = []
		self._tokens = tokens[:]
		self._midi_ticks_per_beat = midi_ticks_per_beat

	@staticmethod
	def from_text(texts: list[str]):
		token_list = []
		i = 0
		while i < len(texts):
			text = texts[i]
			if text == TokenType.PAD.value:
				i += 1
			elif text == TokenType.STEP.value:
				if i + 2 >= len(texts):
					break
				steps = read_prefixed_int(texts[i+1], 'B')
				ticks = read_prefixed_int(texts[i+2], 'T')
				if steps is None or ticks is None:
					break
				token_list.append(Step(ticks=(steps * 12 + ticks)))
				i += 3
			elif text == TokenType.NOTE.value:
				if i + 3 >= len(texts):
					break
				note = Note.from_text(texts[i+1 : i+3])
				if note:
					token_list.append(note)
				i += 3
			elif text == TokenType.TIMESIG.value:
				# For now, just assume everything is 4/4
				token_list.append(ChangeTimeSignature(time_signature=(4, 4)))
				i += 2
			elif text == TokenType.TEMPO.value:
				tempo = read_prefixed_int(texts[i+1], 'BPM')
				if tempo is None:
					tempo = 120
				token_list.append(ChangeTempo(tempo))
				i += 2
			elif text == TokenType.END.value:
				i += 1
				token_list.append(EndOfSong())
				break
			else:
				i += 1
		return Song(merge_adjacent_steps(token_list))

	def _message_tuples(self):
		time = 0
		for token in self._tokens:
			start_midi = int(time * self._midi_ticks_per_beat / TICKS_PER_BEAT)
			if isinstance(token, Step):
				time += token.ticks
			elif isinstance(token, Note):
				end = time + token.duration
				end_midi = int(end * self._midi_ticks_per_beat / TICKS_PER_BEAT)
				yield start_midi, "note_on", token.pitch
				yield end_midi, "note_off", token.pitch
			elif isinstance(token, ChangeTimeSignature):
				yield start_midi, "time_signature", *token.time_signature
			elif isinstance(token, ChangeTempo):
				yield start_midi, "set_tempo", token.tempo
	
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
