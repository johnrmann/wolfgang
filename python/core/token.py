from .constants import MIDI_TICKS_PER_BEAT, TICKS_PER_BEAT

class Token:
	time: int

	def __init__(
			self,
			ticks: int = None,
			midi_ticks: int = None,
			midi_ticks_per_beat: int = MIDI_TICKS_PER_BEAT
	):
		self._midi_ticks_per_beat = midi_ticks_per_beat
		if ticks is not None and midi_ticks is None:
			self.time = ticks
		elif midi_ticks is not None and ticks is None:
			self.time = int(TICKS_PER_BEAT * (midi_ticks / midi_ticks_per_beat))
		else:
			raise ValueError("ticks XOR midi_ticks must be provided")

	def __lt__(self, other):
		return self.time < other.time

	def __gt__(self, other):
		return self.time > other.time
	
	@property
	def start(self):
		return self.time
	
	@start.setter
	def start(self, value):
		self.time = value
	
	@property
	def start_midi(self):
		return int(self._midi_ticks_per_beat * (self.time / TICKS_PER_BEAT))
	
	@start_midi.setter
	def start_midi(self, val):
		self.time = int(TICKS_PER_BEAT * (val / self._midi_ticks_per_beat))

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
			midi_ticks_per_beat: int = MIDI_TICKS_PER_BEAT,
			**kwargs
	):
		super().__init__(midi_ticks_per_beat=midi_ticks_per_beat, **kwargs)
		self.pitch = pitch
		if duration is None and midi_duration is not None:
			factor = (midi_duration / midi_ticks_per_beat)
			self.duration = int(TICKS_PER_BEAT * factor)
		else:
			self.duration = duration

	def __lt__(self, other):
		if self.time == other.time:
			if isinstance(other, Note):
				return self.pitch < other.pitch
			return False
		return self.time < other.time

	def __gt__(self, other):
		if self.time == other.time:
			if isinstance(other, Note):
				return self.pitch > other.pitch
			return True
		return self.time > other.time

	def __str__(self):
		beats, ticks = self.time_index()
		duration = self.duration
		pitch = self.pitch
		return f"NOTE {beats} {ticks} {duration} {pitch}"

	@property
	def end(self):
		return self.time + self.duration

	@end.setter
	def end(self, value):
		self.duration = value - self.time

	@property
	def end_midi(self):
		return int(self._midi_ticks_per_beat * (self.end / TICKS_PER_BEAT))

	@end_midi.setter
	def end_midi(self, val):
		self.duration = int(TICKS_PER_BEAT * (val / self._midi_ticks_per_beat))


class ChangeTempo(Token):
	tempo: int

	def __init__(self, tempo: int, **kwargs):
		super().__init__(**kwargs)
		self.tempo = tempo

	def __str__(self):
		beats, ticks = self.time_index()
		tempo = self.tempo
		return f"TEMPO {beats} {ticks} {tempo}"


TimeSignature = tuple[int, int]


def is_accepted_time_signature(time_signature: TimeSignature):
	num, den = time_signature
	if num == den == 4:
		return True
	if num == 3 and den == 4:
		return True
	if num == 6 and den == 8:
		return True
	return False


def time_signature_string(time_signature: TimeSignature):
	num, den = time_signature
	if num == den == 4:
		return "TS.4.4"
	if num == 3 and den == 4:
		return "TS.3.4"
	if num == 6 and den == 8:
		return "TS.6.8"
	raise ValueError("Invalid time signature")


class ChangeTimeSignature(Token):
	time_signature: TimeSignature

	def __init__(self, time_signature: TimeSignature = None, **kwargs):
		super().__init__(**kwargs)
		self.time_signature = time_signature

	def __str__(self):
		beats, ticks = self.time_index()
		ts = time_signature_string(self.time_signature)
		return f"TIMESIG {beats} {ticks} {ts}"


class EndOfSong(Token):
	def __str__(self):
		beats, ticks = self.time_index()
		return f"EOS {beats} {ticks}"
