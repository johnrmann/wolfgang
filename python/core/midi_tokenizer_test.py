from core.midi_tokenizer import MidiTokenizer
from core.token import Note, Step

def test__midi_tokenizer__starts_empty():
	tokenizer = MidiTokenizer()
	assert tokenizer.tokens == []


def test__midi_tokenizer__add_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	assert isinstance(tokenizer.tokens[0], Note)
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60


def test__midi_tokenizer__add_notes():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_on(61, 480)
	tokenizer.note_off(61, 480)
	assert len(tokenizer.tokens) == 4
	assert isinstance(tokenizer.tokens[0], Note)
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert isinstance(tokenizer.tokens[1], Step)
	assert tokenizer.tokens[1].ticks == 24
	assert isinstance(tokenizer.tokens[2], Note)
	assert tokenizer.tokens[2].duration == 12
	assert tokenizer.tokens[2].pitch == 61


def test__midi_tokenizer__add_chord():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_on(64, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(64, 0)
	assert len(tokenizer.tokens) == 3
	assert isinstance(tokenizer.tokens[0], Note)
	assert isinstance(tokenizer.tokens[1], Note)
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[1].duration == 12
	assert tokenizer.tokens[1].pitch == 64


def test__midi_tokenizer__add_broken_chord():
	tokenizer= MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_on(64, 480)
	tokenizer.note_on(67, 480)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(64, 0)
	tokenizer.note_off(67, 0)
	assert len(tokenizer.tokens) == 6
	assert isinstance(tokenizer.tokens[0], Note)
	assert tokenizer.tokens[0].duration == 36
	assert isinstance(tokenizer.tokens[1], Step)
	assert tokenizer.tokens[1].ticks == 12
	assert isinstance(tokenizer.tokens[2], Note)
	assert tokenizer.tokens[2].duration == 24
	assert isinstance(tokenizer.tokens[3], Step)
	assert tokenizer.tokens[3].ticks == 12
	assert isinstance(tokenizer.tokens[4], Note)
	assert tokenizer.tokens[4].duration == 12
	assert isinstance(tokenizer.tokens[5], Step)
	assert tokenizer.tokens[5].ticks == 12


def test__midi_tokenizer__extend_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(60, 480)
	assert tokenizer.tokens[0].duration == 24
	assert tokenizer.tokens[0].pitch == 60


def test__midi_tokenizer__midi_ticks_per_beat():
	tokenizer = MidiTokenizer(midi_ticks_per_beat=100)
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 100)
	tokenizer.note_on(61, 0)
	tokenizer.note_off(61, 100)
	assert len(tokenizer.tokens) == 4
	assert tokenizer.tokens[0].duration == 12
	assert tokenizer.tokens[0].pitch == 60
	assert tokenizer.tokens[2].duration == 12
	assert tokenizer.tokens[2].pitch == 61
