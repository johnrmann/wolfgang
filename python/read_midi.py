import os
import sys
import argparse

from core.midi_tokenizer import read_midi_file
from core.message import Note, Step, merge_adjacent_steps
from core.song import Song

parser = argparse.ArgumentParser(
	description="Convert MIDI files to tokenized format."
)
parser.add_argument(
	'--input',
	type=str,
	required=True,
	help="Path to the MIDI file or directory."
)
parser.add_argument(
	'--out',
	type=str,
	required=False,
	help="Path to save the tokenized file."
)
parser.add_argument(
	'--transpose_range',
	type=int,
	required=False,
	help="Generate copies of the MIDI file transposed by this range.",
	default=0
)

args = parser.parse_args()
in_arg = args.input
out_arg = args.out
transpose_range = args.transpose_range

def write_song(song: Song, to_path: str):
	"""Write a song to a file."""
	with open(to_path, 'w') as f:
		tokens = song.to_message_strings()
		for token in tokens:
			f.write(str(token) + '\n')
	print("Wrote output to", to_path)

def transform_midi_file(in_path: str, out_path: str | None = None):
	messages = read_midi_file(in_path)
	messages = [
		msg for msg in messages
		if not isinstance(msg, Note) or msg.duration > 0
	]
	messages = [
		msg for msg in messages
		if not isinstance(msg, Step) or msg.ticks > 0
	]
	messages = merge_adjacent_steps(messages)
	song = Song(messages)
	if out_path is None:
		for token in messages:
			print(token)
	else:
		write_song(song, out_path)
		for delta in range(1, transpose_range + 1):
			transposed_up = song.transposed(delta)
			transposed_down = song.transposed(-delta)
			up_path = out_path.replace('.tok', f'_up_{delta}.tok')
			down_path = out_path.replace('.tok', f'_down_{delta}.tok')
			write_song(transposed_up, up_path)
			write_song(transposed_down, down_path)


if __name__ == '__main__':
	# Determine if the in_path is a file or a directory. If it's a directory,
	# assume the contents are all .mid files and read them all.
	if os.path.isdir(in_arg):
		for root, _, files in os.walk(in_arg):
			for file in files:
				if file.endswith('.mid') and not file.endswith('.ignore.mid'):
					new_file = file.replace('.mid', '.tok')
					new_out_path = os.path.join(out_arg, new_file)
					try:
						transform_midi_file(os.path.join(root, file), new_out_path)
					except Exception as e:
						print(f"Error processing {file}: {e}")
	else:
		transform_midi_file(in_arg, out_arg)
