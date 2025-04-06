import mido

from core.midi import flatten_tracks

def test__flatten_tracks():
	# Create a test MIDI file with two tracks.
	midi = mido.MidiFile()
	track1 = mido.MidiTrack()
	track2 = mido.MidiTrack()
	midi.tracks.append(track1)
	midi.tracks.append(track2)

	# Add some messages to the tracks.
	track1.append(mido.Message('note_on', note=60, time=0))
	track1.append(mido.Message('note_off', note=60, time=480))
	track2.append(mido.Message('note_on', note=62, time=480))
	track2.append(mido.Message('note_off', note=62, time=960))

	# Flatten the tracks.
	flattened = flatten_tracks(midi.tracks)

	# Check that the flattened list has the correct number of messages.
	assert len(flattened) == 4
	# Check that the messages are in the correct order.
	assert flattened[0].type == 'note_on'
	assert flattened[0].note == 60
	assert flattened[0].time == 0
	assert flattened[1].type == 'note_off'
	assert flattened[1].note == 60
	assert flattened[1].time == 480
	assert flattened[2].type == 'note_on'
	assert flattened[2].note == 62
	assert flattened[2].time == 480
	assert flattened[3].type == 'note_off'
	assert flattened[3].note == 62
	assert flattened[3].time == 960


def test__flatten_tracks__selected():
	# Create a test MIDI file with two tracks.
	midi = mido.MidiFile()
	track1 = mido.MidiTrack()
	track2 = mido.MidiTrack()
	midi.tracks.append(track1)
	midi.tracks.append(track2)

	# Add some messages to the tracks.
	track1.append(mido.Message('note_on', note=60, time=0))
	track1.append(mido.Message('note_off', note=60, time=480))
	track2.append(mido.Message('note_on', note=62, time=0))
	track2.append(mido.Message('note_off', note=62, time=480))

	# Flatten the tracks.
	flattened = flatten_tracks(midi.tracks, selected={1})

	# Check that the flattened list has the correct number of messages.
	assert len(flattened) == 2
	# Check that the messages are in the correct order.
	assert flattened[0].type == 'note_on'
	assert flattened[0].note == 62
	assert flattened[0].time == 0
	assert flattened[1].type == 'note_off'
	assert flattened[1].note == 62
	assert flattened[1].time == 480
