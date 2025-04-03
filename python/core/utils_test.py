from core.utils import (
	microseconds_per_quarter_to_bpm,
	read_prefixed_int,
	find_prefixed_int,
	count_payload,
)

def test__microseconds_per_quarter_to_bpm():
	assert microseconds_per_quarter_to_bpm(500_000) == 120.0
	assert microseconds_per_quarter_to_bpm(1_000_000) == 60.0
	assert microseconds_per_quarter_to_bpm(2_000_000) == 30.0
	assert microseconds_per_quarter_to_bpm(1_200_000) == 50.0


def test__read_prefixed_int():
	assert read_prefixed_int("BPM120", "BPM") == 120
	assert read_prefixed_int("BPM60", "BPM") == 60
	assert read_prefixed_int("BPM30", "BPM") == 30
	assert read_prefixed_int("BPM50", "BPM") == 50
	assert read_prefixed_int("X", "X") is None
	assert read_prefixed_int("120", "BPM") is None
	assert read_prefixed_int("", "BPM") is None


def test__find_prefixed_int():
	tokens = ["A4", "B8", "C15", "D16"]
	assert find_prefixed_int(tokens, "A") == 4
	assert find_prefixed_int(tokens, "B") == 8
	assert find_prefixed_int(tokens, "C") == 15
	assert find_prefixed_int(tokens, "D") == 16


def test__count_payload__partial():
	tokens = ["A4", "B8", "C15", "D16", "PAD", "E23", "F42"]
	assert count_payload(tokens) == 4


def test__count_payload__empty():
	tokens = ["PAD", "PAD", "PAD"]
	assert count_payload(tokens) == 0


def test__count_payload__full():
	tokens = ["A4", "B8", "C15", "D16"]
	assert count_payload(tokens) == 4
