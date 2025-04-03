from .constants import MIDI_TICKS_PER_BEAT, TICKS_PER_BEAT, TokenType

from core.utils import (
	find_prefixed_int,
	read_prefixed_int,
)


class Token:
	"""
	All Tokens inherit from this class.
	"""
	pass


class Step(Token):
	"""
	A Step token indicates the passage of time. Think of it as a tuple of
	(beat, tick).
	"""

	def __init__(
			self,
			ticks: int = None,
			midi_ticks: int = None,
			midi_ticks_per_beat: int = MIDI_TICKS_PER_BEAT
	):
		self._midi_ticks_per_beat = midi_ticks_per_beat
		if ticks is not None and midi_ticks is None:
			self.ticks = ticks
		elif midi_ticks is not None and ticks is None:
			self.ticks = int(TICKS_PER_BEAT * (midi_ticks / midi_ticks_per_beat))
		else:
			raise ValueError("ticks XOR midi_ticks must be provided")

	def __str__(self):
		beats, ticks = self.time_index()
		return f"STEP B{beats} T{ticks}"

	def time_index(self):
		beats = self.ticks // TICKS_PER_BEAT
		ticks = self.ticks % TICKS_PER_BEAT
		return beats, ticks


class Note(Token):
	pitch: int
	duration: int

	def __init__(
			self,
			pitch: int = 60,
			duration: int = None,
			midi_duration: int = None,
	):
		super().__init__()
		self.pitch = pitch
		if duration is None and midi_duration is not None:
			factor = (midi_duration / midi_ticks_per_beat)
			self.duration = int(TICKS_PER_BEAT * factor)
		else:
			self.duration = duration

	@staticmethod
	def from_text(tokens: list[str]):
		if len(tokens) < 2:
			return None
		subseq = tokens[:2]
		duration = find_prefixed_int(subseq, 'D')
		pitch = find_prefixed_int(subseq, 'P')
		# If one of them is not found, return None
		if duration is None or pitch is None:
			return None
		return Note(
			pitch=pitch,
			duration=duration,
		)

	def __str__(self):
		duration = min(self.duration, 120)
		pitch = self.pitch
		return f"NOTE D{duration} P{pitch}"


class ChangeTempo(Token):
	tempo: int

	def __init__(self, tempo: int = 120):
		super().__init__()
		self.tempo = tempo

	def __str__(self):
		tempo = self.tempo
		return f"TEMPO BPM{tempo}"


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

	def __init__(self, time_signature: TimeSignature = None):
		super().__init__()
		self.time_signature = time_signature

	def __str__(self):
		ts = time_signature_string(self.time_signature)
		return f"TIMESIG {ts}"


class EndOfSong(Token):
	def __str__(self):
		control = TokenType.END.value
		return f"{control}"
