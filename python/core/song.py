import mido

from .message import Message, Note, Step, ChangeTimeSignature, ChangeTempo, EndOfSong, merge_adjacent_steps
from core.constants import MessageType, TICKS_PER_BEAT
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
	_tokens: list[Message]
	_midi_ticks_per_beat: int

	def __init__(
		self,
		tokens: list[Message] = None,
		midi_ticks_per_beat: int = 480
	):
		if tokens is None:
			tokens = []
		self._tokens = tokens[:]
		self._midi_ticks_per_beat = midi_ticks_per_beat

	def __len__(self):
		return len(self._tokens)

	@staticmethod
	def from_text(texts: list[str]):
		token_list = []
		i = 0
		while i < len(texts):
			text = texts[i]
			if text == MessageType.PAD.value:
				i += 1
			elif text == MessageType.STEP.value:
				if i + 1 >= len(texts):
					break
				ticks = read_prefixed_int(texts[i+1], 'T')
				if ticks is None:
					break
				token_list.append(Step(ticks=(ticks)))
				i += 2
			elif text == MessageType.NOTE.value:
				if i + 3 >= len(texts):
					break
				note = Note.from_text(texts[i+1 : i+3])
				if note:
					token_list.append(note)
				i += 3
			elif text == MessageType.TIMESIG.value:
				# For now, just assume everything is 4/4
				token_list.append(ChangeTimeSignature(time_signature=(4, 4)))
				i += 2
			elif text == MessageType.TEMPO.value:
				tempo = texts[i+1]
				token_list.append(ChangeTempo(tempo))
				i += 2
			elif text == MessageType.END.value:
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

	def to_message_strings(self) -> list[str]:
		messages = []
		for message in self._tokens:
			messages.append(str(message))
		return messages

	def to_tokens(self) -> list[str]:
		big_str = ''
		for token in self._tokens:
			big_str += str(token) + ' '
		return big_str.strip().split(' ')

	def to_midi(self):
		events = self.message_tuples()
		mid = mido.MidiFile()
		track = mido.MidiTrack()
		mid.tracks.append(track)
		for event in events:
			track.append(song_event_to_mido_message(event))
		return mid

	def to_json(self):
		time = 0
		json = {}
		for message in self._tokens:
			if isinstance(message, Step):
				time += message.ticks
			else:
				if time not in json:
					json[time] = []
				json[time].append(message.to_json())
		return json

	def transposed(self, delta_pitch: int):
		"""
		Create a copy of this song transposed to a new pitch.
		"""
		new_messages = []
		for message in self._tokens:
			if isinstance(message, Note):
				new_messages.append(message.transposed(delta_pitch))
			else:
				new_messages.append(message)
		return Song(new_messages, midi_ticks_per_beat=self._midi_ticks_per_beat)


class SongBuilder:
	_messages: list[Message]
	_last_time: int = 0

	def __init__(self):
		self._messages = []

	def _advance_time(self, new_time: int):
		if new_time < self._last_time:
			raise ValueError("Time must be greater than last time")
		if new_time == self._last_time:
			return
		delta = new_time - self._last_time
		self._last_time = new_time
		self._messages.append(Step(ticks=delta))

	def note(self, time: int, duration: int, pitch: int):
		self._advance_time(time)
		self._messages.append(Note(pitch=pitch, duration=duration))

	def tempo(self, time: int, tempo: int):
		self._advance_time(time)
		self._messages.append(ChangeTempo(tempo=tempo))

	def time_signature(self, time: int, time_signature: tuple[int, int]):
		self._advance_time(time)
		self._messages.append(ChangeTimeSignature(time_signature=time_signature))

	def end(self, time: int):
		self._advance_time(time)
		self._messages.append(EndOfSong())

	def build(self) -> Song:
		return Song(self._messages)
