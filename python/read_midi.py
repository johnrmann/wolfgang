import os
import sys

from core.midi_tokenizer import read_midi_file
from core.token import Note, merge_adjacent_steps

def transform_midi_file(in_path: str, out_path: str | None = None):
	tokens = read_midi_file(in_path)
	if out_path is None:
		for token in tokens:
			print(token)
	else:
		with open(out_path, 'w') as f:
			for token in tokens:
				if isinstance(token, Note) and token.duration == 0:
					continue
				f.write(str(token) + '\n')
			print("Wrote output to", out_path)


if __name__ == '__main__':
	in_path = sys.argv[1]
	out_path = sys.argv[2] if len(sys.argv) > 2 else None

	# Determine if the in_path is a file or a directory. If it's a directory,
	# assume the contents are all .mid files and read them all.
	if os.path.isdir(in_path):
		for root, _, files in os.walk(in_path):
			for file in files:
				if file.endswith('.mid'):
					new_file = file.replace('.mid', '.tok')
					new_out_path = os.path.join(out_path, new_file)
					try:
						transform_midi_file(os.path.join(root, file), new_out_path)
					except Exception as e:
						print(f"Error processing {file}: {e}")
	else:
		transform_midi_file(in_path, out_path)
