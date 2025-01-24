from .token import Token, Note

class MidiTokenizer:
	_tokens = list[Token]

	# Maps the pitch number (60 being middle C) to the time index that the
	# note was turned on.
	_open_pitches = dict[int, int]

	def __init__(self):
		self._tokens = []
		self._open_pitches = {}

	def note_on(self, pitch: int, ticks: int):
		if pitch in self._open_pitches:
			raise ValueError(f"Note {pitch} is already on")
		self._open_pitches[pitch] = ticks

	def note_off(self, pitch: int, ticks: int):
		if pitch not in self._open_pitches:
			raise ValueError(f"Note {pitch} is not on")
		on_ticks = self._open_pitches[pitch]
		duration = ticks - on_ticks
		self._tokens.append(Note(
			pitch=pitch,
			midi_duration=duration,
			midi_ticks=on_ticks
		))
		del self._open_pitches[pitch]

	@property
	def tokens(self):
		return self._tokens
