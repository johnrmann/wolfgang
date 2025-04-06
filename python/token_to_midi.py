import argparse
import os
import sys

from core.song import Song

parser = argparse.ArgumentParser(
	description="Convert tokens to listenable MIDI files."
)
parser.add_argument(
	'--input',
	type=str,
	required=True,
	help="Path to the token file."
)
parser.add_argument(
	'--out',
	type=str,
	required=True,
	help="Path to save the MIDI file."
)
args = parser.parse_args()
input_file = args.input
output_file = args.out

if not os.path.isfile(input_file):
	print(f"Error: {input_file} is not a file.")
	exit(1)

# Read the token file
with open(input_file, 'r') as f:
	lines = f.readlines()
	tokens = []
	for line in lines:
		tokens.extend(line.strip().split())
	song = Song.from_text(tokens)
	midi = song.to_midi()
	midi.save(output_file)
	print(f"Saved generated MIDI file to {output_file}")

