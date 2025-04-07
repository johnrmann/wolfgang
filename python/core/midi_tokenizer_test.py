from core.midi_tokenizer import MidiTokenizer
from core.message import Note, Step

def test__midi_tokenizer__starts_empty():
	tokenizer = MidiTokenizer()
	assert tokenizer.messages == []


def test__midi_tokenizer__add_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	assert isinstance(tokenizer.messages[0], Note)
	assert tokenizer.messages[0].duration == 12
	assert tokenizer.messages[0].pitch == 60


def test__midi_tokenizer__add_notes():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_on(61, 480)
	tokenizer.note_off(61, 480)
	assert len(tokenizer.messages) == 4
	assert isinstance(tokenizer.messages[0], Note)
	assert tokenizer.messages[0].duration == 12
	assert tokenizer.messages[0].pitch == 60
	assert isinstance(tokenizer.messages[1], Step)
	assert tokenizer.messages[1].ticks == 24
	assert isinstance(tokenizer.messages[2], Note)
	assert tokenizer.messages[2].duration == 12
	assert tokenizer.messages[2].pitch == 61


def test__midi_tokenizer__add_chord():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_on(64, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(64, 0)
	assert len(tokenizer.messages) == 3
	assert isinstance(tokenizer.messages[0], Note)
	assert isinstance(tokenizer.messages[1], Note)
	assert tokenizer.messages[0].duration == 12
	assert tokenizer.messages[0].pitch == 60
	assert tokenizer.messages[1].duration == 12
	assert tokenizer.messages[1].pitch == 64


def test__midi_tokenizer__add_broken_chord():
	tokenizer= MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_on(64, 480)
	tokenizer.note_on(67, 480)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(64, 0)
	tokenizer.note_off(67, 0)
	assert len(tokenizer.messages) == 6
	assert isinstance(tokenizer.messages[0], Note)
	assert tokenizer.messages[0].duration == 36
	assert isinstance(tokenizer.messages[1], Step)
	assert tokenizer.messages[1].ticks == 12
	assert isinstance(tokenizer.messages[2], Note)
	assert tokenizer.messages[2].duration == 24
	assert isinstance(tokenizer.messages[3], Step)
	assert tokenizer.messages[3].ticks == 12
	assert isinstance(tokenizer.messages[4], Note)
	assert tokenizer.messages[4].duration == 12
	assert isinstance(tokenizer.messages[5], Step)
	assert tokenizer.messages[5].ticks == 12


def test__midi_tokenizer__extend_note():
	tokenizer = MidiTokenizer()
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 480)
	tokenizer.note_off(60, 480)
	assert tokenizer.messages[0].duration == 24
	assert tokenizer.messages[0].pitch == 60


def test__midi_tokenizer__midi_ticks_per_beat():
	tokenizer = MidiTokenizer(midi_ticks_per_beat=100)
	tokenizer.note_on(60, 0)
	tokenizer.note_off(60, 100)
	tokenizer.note_on(61, 0)
	tokenizer.note_off(61, 100)
	assert len(tokenizer.messages) == 4
	assert tokenizer.messages[0].duration == 12
	assert tokenizer.messages[0].pitch == 60
	assert tokenizer.messages[2].duration == 12
	assert tokenizer.messages[2].pitch == 61


def test__midi_tokenizer__advance_time():
	tokenizer = MidiTokenizer()
	tokenizer.advance_time(480)
	assert len(tokenizer.messages) == 1
	assert isinstance(tokenizer.messages[0], Step)
	assert tokenizer.messages[0].ticks == 12
	tokenizer.advance_time(480)
	assert len(tokenizer.messages) == 1
	assert isinstance(tokenizer.messages[0], Step)
	assert tokenizer.messages[0].ticks == 24
