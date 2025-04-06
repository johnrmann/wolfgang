from .constants import (
	TEMPO_MARKING_TO_BPM,
	MIDI_TICKS_PER_BEAT,
	TICKS_PER_BEAT,
	MAX_NOTE_DURATION,
	MessageType
)

from core.utils import (
	find_prefixed_int,
	bpm_to_tempo_marking,
)	


class Message:
	"""
	A Message is formed from a sequence of Tokens.
	"""
	pass


class Step(Message):
	"""
	A Step message indicates the passage of time. Think of it as a tuple of
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

	def __add__(self, other):
		if isinstance(other, Step):
			return Step(ticks=self.ticks + other.ticks)
		raise ValueError("Cannot add Step to non-Step object")

	def __str__(self):
		return f"STEP T{self.ticks}"


def merge_adjacent_steps(msgs: list[Message]):
	"""
	Given a list of tokens, merge adjacent Step tokens into one.
	"""
	new_msgs = []
	for msg in msgs:
		if len(new_msgs) == 0:
			new_msgs.append(msg)
			continue
		prev_msg = new_msgs[-1]
		if isinstance(prev_msg, Step) and isinstance(msg, Step):
			prev_msg.ticks += msg.ticks
		else:
			new_msgs.append(msg)
	return new_msgs


class Note(Message):
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
			self.duration = min(int(TICKS_PER_BEAT * factor), MAX_NOTE_DURATION)
		else:
			self.duration = min(duration, MAX_NOTE_DURATION)

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


class ChangeTempo(Message):
	tempo: int

	def __init__(self, tempo: int | str = 120):
		super().__init__()
		if isinstance(tempo, str):
			self.tempo = TEMPO_MARKING_TO_BPM[tempo.upper()]
		else:
			self.tempo = tempo

	def __str__(self):
		tempo = bpm_to_tempo_marking(self.tempo)
		return f"TEMPO {tempo.value}"


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


class ChangeTimeSignature(Message):
	time_signature: TimeSignature

	def __init__(self, time_signature: TimeSignature = None):
		super().__init__()
		self.time_signature = time_signature

	def __str__(self):
		ts = time_signature_string(self.time_signature)
		return f"TIMESIG {ts}"


class EndOfSong(Message):
	def __str__(self):
		control = MessageType.END.value
		return f"{control}"
