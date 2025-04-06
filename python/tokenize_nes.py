import os
import sys
import argparse
import mido

from core.midi_tokenizer import read_midi
from core.midi import pick_tracks

# Get arguments for the input directory and output directory
parser = argparse.ArgumentParser(
	description="Convert MIDI files to tokenized format."
)
parser.add_argument(
	'--input',
	type=str,
	required=True,
	help="Path to the directory containing MIDI files."
)
parser.add_argument(
	'--out-melody',
	type=str,
	required=True,
	help="Path to the directory to save tokenized melody files."
)
parser.add_argument(
	'--out-full',
	type=str,
	required=True,
	help="Path to the directory to save tokenized full files."
)
args = parser.parse_args()

input_dir = args.input
melody_dir = args.out_melody
full_dir = args.out_full

if not os.path.exists(melody_dir):
	os.makedirs(melody_dir)
if not os.path.exists(full_dir):
	os.makedirs(full_dir)

# Check if the input directory exists
if not os.path.isdir(input_dir):
	print(f"Error: {input_dir} is not a directory.")
	exit(1)

for root, _, files in os.walk(input_dir):
	for file in files:
		if not file.endswith('.mid'):
			continue
		file_path = os.path.join(root, file)
		print(f"Processing {file_path}...")
		# Read the MIDI file
		midi = mido.MidiFile(file_path)
		tracks = midi.tracks
		melody_track = pick_tracks(midi, set([0, 1]))
		full_track = pick_tracks(midi, set([0, 1, 2, 3]))
		melody_msgs = read_midi(melody_track)
		full_msgs = read_midi(full_track)
		
		# Write the tokenized melody to the melody directory
		melody_file = os.path.join(
			melody_dir,
			file.replace('.mid', '.melody.tok')
		)
		with open(melody_file, 'w') as f:
			for msg in melody_msgs:
				f.write(str(msg) + '\n')
		
		# Write the tokenized full to the full directory
		full_file = os.path.join(full_dir, file.replace('.mid', '.full.tok'))
		with open(full_file, 'w') as f:
			for msg in full_msgs:
				f.write(str(msg) + '\n')
