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
