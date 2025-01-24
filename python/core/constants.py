"""
Constants used throughout the project.
"""

# Four ticks per beat gives us resolution of sixteenth notes, times three so
# we can represent triplets.
TICKS_PER_BEAT = 12

# MIDI files have 480 ticks per quarter note, whereas Wolfgang has 12.
MIDI_TICKS_PER_WOLFGANG_TICK = 40
