import sys

from core.midi_tokenizer import read_midi_file

if __name__ == '__main__':
	# Read input file from command line.
	file_path = sys.argv[1]

	# Read output path from the command line. If it isn't there, then just
	# print the output to the console.
	output_path = None
	if len(sys.argv) > 2:
		output_path = sys.argv[2]

	# Read the MIDI file.
	tokens = read_midi_file(file_path)
	if not output_path:
		for token in tokens:
			print(token)
	else:
		with open(output_path, 'w') as f:
			for token in tokens:
				f.write(str(token) + '\n')
			print("Wrote output to", output_path)
