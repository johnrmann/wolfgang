from .midi_tokenizer import MidiTokenizer

def test__midi_tokenizer__starts_empty():
	tokenizer = MidiTokenizer()
	assert tokenizer.tokens == []


def test__midi_tokenizer__add_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	assert len(tokenizer.tokens) == 1
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[0].time == 0


def test__midi_tokenizer__extend_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, delta_ticks=0)
	tokenizer.note_off(60, delta_ticks=480)
	tokenizer.note_off(60, delta_ticks=480)
	assert len(tokenizer.tokens) == 1
	assert tokenizer.tokens[0].duration == 24
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[0].time == 0


def test__midi_tokenizer__add_note__delta_ticks():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, delta_ticks=0)
	tokenizer.note_off(60, delta_ticks=480)
	tokenizer.note_on(61, delta_ticks=0)
	tokenizer.note_off(61, delta_ticks=480)
	assert len(tokenizer.tokens) == 2
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[0].time == 0
	assert tokenizer.tokens[1].duration == 12
	assert tokenizer.tokens[1].pitch == 61
	assert tokenizer.tokens[1].time == 12


def test__midi_tokenizer__midi_ticks_per_beat():
	tokenizer = MidiTokenizer(midi_ticks_per_beat=100)
	tokenizer.note_on(60, delta_ticks=0)
	tokenizer.note_off(60, delta_ticks=100)
	tokenizer.note_on(61, delta_ticks=0)
	tokenizer.note_off(61, delta_ticks=100)
	assert len(tokenizer.tokens) == 2
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[0].time == 0
	assert tokenizer.tokens[1].duration == 12
	assert tokenizer.tokens[1].pitch == 61
	assert tokenizer.tokens[1].time == 12
