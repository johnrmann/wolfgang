"""
Constants used throughout the project.
"""

from enum import Enum

class MessageType(Enum):
	"""
	An enumeration of the different types of tokens that can be found in a
	song.
	"""
	PAD = 'PAD'
	STEP = 'STEP'
	NOTE = 'NOTE'
	TEMPO = 'TEMPO'
	TIMESIG = 'TIMESIG'
	END = 'END'

TOKEN_TYPE_TO_PAYLOAD_LENGTH = {
	MessageType.PAD: 0,
	MessageType.STEP: 1,
	MessageType.NOTE: 2,
	MessageType.TEMPO: 1,
	MessageType.TIMESIG: 1,
	MessageType.END: 0,

	MessageType.PAD.value: 0,
	MessageType.STEP.value: 2,
	MessageType.NOTE.value: 2,
	MessageType.TEMPO.value: 1,
	MessageType.TIMESIG.value: 1,
	MessageType.END.value: 0,
}

class TimeSignature(Enum):
	"""
	An enumeration of the different time signatures that can be found in a song.
	"""
	FOUR_FOUR = 'TS.4.4'
	THREE_FOUR = 'TS.3.4'
	SIX_EIGHT = 'TS.6.8'

class TempoMarking(Enum):
	""""
	An enumeration of the different tempo markings that can be found in a
	song.
	"""
	LARGO = 'LARGO'
	ADAGIO = 'ADAGIO'
	ADANTE = 'ADANTE'
	ALLEGRO = 'ALLEGRO'
	VIVACE = 'VIVACE'
	PRESTO = 'PRESTO'
	PRESTISSIMO = 'PRESTISSIMO'

TEMPO_MARKING_TO_BPM = {
	TempoMarking.LARGO: 40,
	TempoMarking.ADAGIO: 60,
	TempoMarking.ADANTE: 80,
	TempoMarking.ALLEGRO: 120,
	TempoMarking.VIVACE: 140,
	TempoMarking.PRESTO: 160,
	TempoMarking.PRESTISSIMO: 200,

	TempoMarking.LARGO.value: 40,
	TempoMarking.ADAGIO.value: 60,
	TempoMarking.ADANTE.value: 80,
	TempoMarking.ALLEGRO.value: 120,
	TempoMarking.VIVACE.value: 140,
	TempoMarking.PRESTO.value: 160,
	TempoMarking.PRESTISSIMO.value: 200,
}

# Four ticks per beat gives us resolution of sixteenth notes, times three so
# we can represent triplets.
TICKS_PER_BEAT = 12

# MIDI files have 480 ticks per quarter note, whereas Wolfgang has 12.
MIDI_TICKS_PER_WOLFGANG_TICK = 40

# The number of MIDI ticks per quarter note.
MIDI_TICKS_PER_BEAT = 480

# The maximum number of notes in a song.
BEATS_PER_SONG = 1024

# We don't expect rests to be longer than 24 beats (six notes).
MAX_REST_DURATION = 24 * TICKS_PER_BEAT

# We don't expect notes to be longer than 16 beats (eight notes).
MAX_NOTE_DURATION = 16 * TICKS_PER_BEAT
