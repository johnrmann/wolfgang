from .token import Token, Note

def test__token__sets_ticks():
	token = Token(ticks=1)
	assert token.time == 1


def test__token__sets_midi_ticks():
	token = Token(midi_ticks=480)
	assert token.time == 12


def test__token__time_index_1():
	token = Token(0)
	assert token.time_index() == (0, 0)


def test__token__time_index_2():
	token = Token(13)
	assert token.time_index() == (1, 1)


def test__note__init():
	note = Note(
		pitch=60,
		duration=12,
		ticks=0,
	)
	assert note.pitch == 60
	assert note.duration == 12
	assert note.time == 0


def test__note__str():
	note = Note(
		pitch=60,
		duration=12,
		ticks=0,
	)
	assert str(note) == "NOTE 0 0 12 60"


def test__note__init__midi_duration():
	note = Note(
		pitch=60,
		midi_duration=480,
		ticks=0,
	)
	assert note.pitch == 60
	assert note.duration == 12
	assert note.time == 0
