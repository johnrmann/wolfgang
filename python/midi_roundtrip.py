import sys

from core.midi_tokenizer import read_midi_file
from core.song import Song

if __name__ == '__main__':
	# Read input file from command line.
	file_path = sys.argv[1]

	# Read output path from the command line. If it isn't there, then just
	# print the output to the console.
	output_path = sys.argv[2]

	# Read the MIDI file.
	tokens = read_midi_file(file_path)
	song = Song(tokens)
	midi = song.to_midi()
	midi.save(output_path)
