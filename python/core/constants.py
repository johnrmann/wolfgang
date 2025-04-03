"""
Constants used throughout the project.
"""

from enum import Enum

class TokenType(Enum):
	"""
	An enumeration of the different types of tokens that can be found in a
	song.
	"""
	PAD = 'PAD'
	NOTE = 'NOTE'
	TEMPO = 'TEMPO'
	TIMESIG = 'TIMESIG'
	END = 'END'

class TimeSignature(Enum):
	"""
	An enumeration of the different time signatures that can be found in a song.
	"""
	FOUR_FOUR = 'TS.4.4'
	THREE_FOUR = 'TS.3.4'
	SIX_EIGHT = 'TS.6.8'

# Four ticks per beat gives us resolution of sixteenth notes, times three so
# we can represent triplets.
TICKS_PER_BEAT = 12

# MIDI files have 480 ticks per quarter note, whereas Wolfgang has 12.
MIDI_TICKS_PER_WOLFGANG_TICK = 40

# The number of MIDI ticks per quarter note.
MIDI_TICKS_PER_BEAT = 480

# The maximum number of notes in a song.
BEATS_PER_SONG = 1024
