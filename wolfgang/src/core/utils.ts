export function pitchString(pitch: number): string {
	const noteNames = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
	const octave = Math.floor(pitch / 12) - 1;
	const noteName = noteNames[pitch % 12];
	return `${noteName}${octave}`;
}
