import mido

from collections import defaultdict

from .token import Token, Note, Step, time_signature_string, is_accepted_time_signature, ChangeTempo, ChangeTimeSignature, EndOfSong
from .utils import microseconds_per_quarter_to_bpm

from core.constants import TICKS_PER_BEAT

class MidiTokenizer:
	_ticks: int = 0
	_midi_ticks_per_beat: int = 480

	_tokens = list[Token]

	# Is the pitch number (60 being middle C) currently "open"?
	_open_pitches = dict[int, bool]

	# For overlapping notes, we take the union of them by storing the last
	# note of that pitch. If we two "note off" events for that pitch, we
	# extend the last note to the new time.
	_last_notes: dict[int, Note]
	_last_note_starts: dict[int, int]

	def __init__(self, midi_ticks_per_beat: int = 480):
		self._tokens = []
		self._open_pitches = defaultdict(lambda: False)
		self._last_notes = {}
		self._last_note_starts = {}
		self._midi_ticks_per_beat = midi_ticks_per_beat

	def advance_time(self, delta_midi: int):
		if delta_midi == 0 or delta_midi is None:
			return self._ticks
		delta_ticks = int(TICKS_PER_BEAT * delta_midi / self._midi_ticks_per_beat)
		self._ticks += delta_ticks
		if len(self._tokens) != 0 and isinstance(self._tokens[-1], Step):
			self._tokens[-1].ticks += delta_ticks
		else:
			self._tokens.append(Step(ticks=delta_ticks))
		return self._ticks

	def note_on(self, pitch: int, delta_midi: int = None):
		self.advance_time(delta_midi)
		if self._open_pitches[pitch]:
			return
		self._open_pitches[pitch] = True
		self._last_note_starts[pitch] = self._ticks		
		new_note = Note(pitch=pitch, duration=0)
		self._tokens.append(new_note)
		self._last_notes[pitch] = new_note

	def note_off(self, pitch: int, delta_midi: int = None):
		self.advance_time(delta_midi)
		if pitch not in self._last_notes:
			raise ValueError("Cannot turn off a note that's never been hit.")
		start = self._last_note_starts[pitch]
		self._last_notes[pitch].duration = self._ticks - start
		self._open_pitches[pitch] = False
	
	def time_signature(self, time_signature: tuple[int, int], delta_midi: int = None):
		self.advance_time(delta_midi)
		self._tokens.append(ChangeTimeSignature(
			time_signature=time_signature
		))

	def tempo(self, tempo: int = 120, delta_midi: int = None):
		self.advance_time(delta_midi)
		self._tokens.append(ChangeTempo(tempo=tempo))

	def end(self, delta_midi: int = None):
		self.advance_time(delta_midi)
		self._tokens.append(EndOfSong())

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
					tokenizer.note_off(msg.note, msg.time)
				else:
					tokenizer.note_on(msg.note, msg.time)
			elif msg.type == 'note_off':
				tokenizer.note_off(msg.note, msg.time)
			elif msg.type == 'time_signature':
				timesig = msg.numerator, msg.denominator
				if is_accepted_time_signature(timesig):
					tokenizer.time_signature(time_signature=timesig, delta_midi=msg.time)
				else:
					return None
			elif msg.type == 'set_tempo':
				tempo = int(mido.tempo2bpm(msg.tempo))
				tokenizer.tempo(tempo=tempo, delta_midi=msg.time)
	
	tokenizer.end(delta_midi=0)

	return tokenizer.tokens
