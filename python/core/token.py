from .constants import MIDI_TICKS_PER_WOLFGANG_TICK, TICKS_PER_BEAT

class Token:
	time: int

	def __init__(self, ticks: int = None, midi_ticks: int = None):
		if ticks is not None and midi_ticks is None:
			self.time = ticks
		elif midi_ticks is not None and ticks is None:
			self.time = midi_ticks / MIDI_TICKS_PER_WOLFGANG_TICK
		else:
			raise ValueError("ticks XOR midi_ticks must be provided")

	def time_index(self):
		beats = self.time // TICKS_PER_BEAT
		ticks = self.time % TICKS_PER_BEAT
		return beats, ticks


class Note(Token):
	pitch: int
	duration: int

	def __init__(
			self,
			pitch: int = 60,
			duration: int = None,
			midi_duration: int = None,
			**kwargs
	):
		super().__init__(**kwargs)
		self.pitch = pitch
		if duration is None and midi_duration is not None:
			self.duration = midi_duration / MIDI_TICKS_PER_WOLFGANG_TICK
		else:
			self.duration = duration

	def __str__(self):
		beats, ticks = self.time_index()
		duration = self.duration
		pitch = self.pitch
		return f"NOTE {beats} {ticks} {duration} {pitch}"
