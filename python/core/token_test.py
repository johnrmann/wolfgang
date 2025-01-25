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


def test__token__errors_no_time():
	try:
		Token()
		assert False
	except ValueError:
		assert True


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


def test__note__init__midi_ticks_per_beat():
	note = Note(
		pitch=60,
		midi_duration=350,
		midi_ticks_per_beat=100,
		midi_ticks=25,
	)
	assert note.pitch == 60
	assert note.duration == 42
	assert note.time == 3
	assert note.time_index() == (0, 3)


def test__note__comparison__time():
	note1 = Note(
		pitch=60,
		duration=12,
		ticks=0,
	)
	note2 = Note(
		pitch=60,
		duration=12,
		ticks=1,
	)
	assert note1 < note2
	assert note2 > note1


def test__note__comparison__pitch():
	note1 = Note(
		pitch=60,
		duration=12,
		ticks=0,
	)
	note2 = Note(
		pitch=61,
		duration=12,
		ticks=0,
	)
	assert note1 < note2
	assert note2 > note1


def test__note__extends_via_end():
	note = Note(
		pitch=60,
		duration=6,
		ticks=6,
	)
	assert note.end == 12
	note.end = 18
	assert note.duration == 12


def test__note__extends_via_end_midi():
	note = Note(
		pitch=60,
		midi_duration=480,
		ticks=0,
		midi_ticks_per_beat=480,
	)
	assert note.end_midi == 480
	note.end_midi = 960
	assert note.duration == 24
	assert note.end == 24
	assert note.end_midi == 960
