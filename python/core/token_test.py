from .token import Step, Note, EndOfSong, ChangeTempo, ChangeTimeSignature, merge_adjacent_steps

def test__step__sets_ticks():
	token = Step(ticks=1)
	assert token.ticks == 1


def test__step__sets_midi_ticks():
	token = Step(midi_ticks=480)
	assert token.ticks == 12


def test__step__time_index_1():
	token = Step(0)
	assert token.time_index() == (0, 0)


def test__step__time_index_2():
	token = Step(13)
	assert token.time_index() == (1, 1)


def test__step__string():
	token = Step(0)
	assert str(token) == "STEP B0 T0"


def test__step__string_2():
	token = Step(13)
	assert str(token) == "STEP B1 T1"


def test__step__errors_no_time():
	try:
		Step()
		assert False
	except ValueError:
		assert True


def test__note__init():
	note = Note(
		pitch=60,
		duration=12,
	)
	assert note.pitch == 60
	assert note.duration == 12


def test__note__str():
	note = Note(
		pitch=60,
		duration=12,
	)
	assert str(note) == "NOTE D12 P60"


def test__tempo__init():
	tempo = ChangeTempo(144)
	assert tempo.tempo == 144


def test__tempo__str():
	tempo = ChangeTempo(144)
	assert str(tempo) == "TEMPO BPM144"


def test__time_signature__init():
	time_signature = ChangeTimeSignature((4, 4))
	assert time_signature.time_signature == (4, 4)


def test__time_signature__str():
	time_signature = ChangeTimeSignature((6, 8))
	assert str(time_signature) == "TIMESIG TS.6.8"


def test__end_of_song__str():
	end = EndOfSong()
	assert str(end) == "END"


def test__merge_adjacent_steps():
	token_list = [
		Step(0),
		Step(12),
		Step(24),
	]
	assert len(token_list) == 3
	assert token_list[0].ticks == 0
	assert token_list[1].ticks == 12
	assert token_list[2].ticks == 24
	merged = merge_adjacent_steps(token_list)
	assert len(merged) == 1
	assert merged[0].ticks == 36
