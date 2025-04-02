import mido

from .token import Token, Note, time_signature_string, is_accepted_time_signature, ChangeTempo, ChangeTimeSignature
from .utils import microseconds_per_quarter_to_bpm

class MidiTokenizer:
	_ticks: int = 0
	_midi_ticks_per_beat: int = 480

	_tokens = list[Token]

	# Maps the pitch number (60 being middle C) to the time index that the
	# note was turned on.
	_open_pitches = dict[int, int]

	# For overlapping notes, we take the union of them by storing the last
	# note of that pitch. If we two "note off" events for that pitch, we
	# extend the last note to the new time.
	_last_notes: dict[int, Note]

	def __init__(self, midi_ticks_per_beat: int = 480):
		self._tokens = []
		self._open_pitches = {}
		self._last_notes = {}
		self._midi_ticks_per_beat = midi_ticks_per_beat

	def advance_time(self, ticks: int, delta_ticks: int):
		if ticks is not None:
			self._ticks = ticks
		elif delta_ticks is not None:
			self._ticks += delta_ticks
		else:
			raise ValueError("ticks or delta_ticks must be provided")
		return self._ticks

	def note_on(self, pitch: int, ticks: int = None, delta_ticks: int = None):
		ticks = self.advance_time(ticks, delta_ticks)
		if pitch in self._open_pitches:
			return
		self._open_pitches[pitch] = ticks
		if pitch in self._last_notes:
			del self._last_notes[pitch]

	def note_off(self, pitch: int, ticks: int = None, delta_ticks: int = None):
		ticks = self.advance_time(ticks, delta_ticks)

		if pitch not in self._open_pitches and pitch not in self._last_notes:
			raise ValueError("Cannot turn off a note that's never been hit.")
		if pitch in self._last_notes:
			self._last_notes[pitch].end_midi = ticks
			return

		# At this point, we know that the pitch is in the open pitches.
		on_ticks = self._open_pitches[pitch]
		duration = ticks - on_ticks
		new_note = Note(
			pitch=pitch,
			midi_duration=duration,
			midi_ticks=on_ticks,
			midi_ticks_per_beat=self._midi_ticks_per_beat
		)
		if duration != 0:
			self._last_notes[pitch] = new_note
			self._tokens.append(new_note)
		del self._open_pitches[pitch]
	
	def time_signature(self, time_signature: tuple[int, int], ticks: int = None, delta_ticks: int = None):
		ticks = self.advance_time(ticks, delta_ticks)
		self._tokens.append(ChangeTimeSignature(
			time_signature=time_signature,
			midi_ticks=ticks,
			midi_ticks_per_beat=self._midi_ticks_per_beat
		))

	def tempo(self, tempo: int = 120, ticks: int = None, delta_ticks: int = None):
		ticks = self.advance_time(ticks, delta_ticks)
		self._tokens.append(ChangeTempo(
			tempo=tempo,
			midi_ticks=ticks,
			midi_ticks_per_beat=self._midi_ticks_per_beat
		))

	@property
	def tokens(self):
		return self._tokens


def read_midi_file(file_path: str) -> list[Token]:
	midi = mido.MidiFile(file_path)
	tpb = midi.ticks_per_beat
	tokenizer = MidiTokenizer(midi_ticks_per_beat=tpb)

	num_tracks = len(midi.tracks)
	if num_tracks == 0:
		raise ValueError("No tracks in MIDI file")
	
	for idx, track in enumerate(midi.tracks):
		for msg in track:
			if msg.type == 'note_on':
				# Check the velocity of the note. If it's 0, then it's a
				# note off.
				if msg.velocity == 0:
					tokenizer.note_off(msg.note, delta_ticks=msg.time)
				else:
					tokenizer.note_on(msg.note, delta_ticks=msg.time)
			elif msg.type == 'note_off':
				tokenizer.note_off(msg.note, delta_ticks=msg.time)
			elif msg.type == 'time_signature':
				timesig = msg.numerator, msg.denominator
				if is_accepted_time_signature(timesig):
					tokenizer.time_signature(
						time_signature=timesig,
						delta_ticks=msg.time,
					)
				else:
					return None
			elif msg.type == 'set_tempo':
				tempo = int(mido.tempo2bpm(msg.tempo))
				tokenizer.tempo(
					tempo=tempo,
					delta_ticks=msg.time,
				)

	return tokenizer.tokens
