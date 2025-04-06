import os
import argparse

parser = argparse.ArgumentParser(
	description="Clean tokenized MIDI files by removing empty lines and comments."
)
parser.add_argument(
	'--directory',
	type=str,
	required=True,
	help="Path to the directory containing tokenized MIDI files."
)

args = parser.parse_args()

directory = args.directory
if not os.path.isdir(directory):
	print(f"Error: {directory} is not a directory.")
	exit(1)

EMPTY_STEP = "STEP T0"

def clean_file(filepath):
	with open(filepath, 'r') as f:
		lines = f.readlines()

	new_lines = [line for line in lines if line.strip() != EMPTY_STEP]

	if len(new_lines) < len(lines):
		with open(filepath, 'w') as f:
			f.writelines(new_lines)
		print(f"Cleaned {filepath}: removed {len(lines) - len(new_lines)} lines.")
	else:
		print(f"No changes made to {filepath}.")

def clean_directory(dirpath):
	for root, _, files in os.walk(dirpath):
		for file in files:
			if file.endswith('.tok'):
				filepath = os.path.join(root, file)
				clean_file(filepath)

if __name__ == '__main__':
	clean_directory(directory)
	print("Cleaning complete.")
