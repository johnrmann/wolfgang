import sys
import os
import shutil

# Map note names to semitone offsets
NOTE_TO_SEMITONE = {
	'C': 0,
	'C#': 1, 'Db': 1,
	'D': 2,
	'D#': 3, 'Eb': 3,
	'E': 4,
	'F': 5,
	'F#': 6, 'Gb': 6,
	'G': 7,
	'G#': 8, 'Ab': 8,
	'A': 9,
	'A#': 10, 'Bb': 10,
	'B': 11
}

def octave(note_name: str) -> int:
	if note_name[-1].isdigit():
		return int(note_name[-1])
	else:
		return 0

def note(note_name: str) -> str:
	return note_name[:-1]

def pitch_to_midi(note_name: str) -> int:
	semitone = NOTE_TO_SEMITONE.get(note(note_name))
	oct = octave(note_name)
	return semitone + (oct + 1) * 12 if semitone is not None else None

def rename_mp3_files():
	for filename in os.listdir(sys.argv[1]):
		if filename.endswith('.mp3'):
			print(repr(filename))
			note_name = filename[:-4]  # Strip off '.mp3'
			try:
				midi_number = pitch_to_midi(note_name)
				old_filename = os.path.join(sys.argv[1], filename)
				new_filename = os.path.join(sys.argv[1], f"{midi_number}.mp3")
				shutil.move(old_filename, new_filename)
				print(f"Renamed: {filename} → {new_filename}")
			except ValueError as e:
				print(f"Skipped: {filename} ({e})")

if __name__ == '__main__':
	rename_mp3_files()
