import {NOTES, NOTES_PER_OCTAVE} from './constants';

/**
 * Converts a pitch number to a string representation.
 */
export function pitchString(pitch: number): string {
	const octave = Math.floor(pitch / NOTES_PER_OCTAVE) - 1;
	const noteName = NOTES[pitch % NOTES_PER_OCTAVE];
	return `${noteName}${octave}`;
}

/**
 * Destructs a pitch number into (note, octave).
 */
export function pitchTuple(pitch: number): [string, number] {
	const octave = Math.floor(pitch / NOTES_PER_OCTAVE) - 1;
	const noteName = NOTES[pitch % NOTES_PER_OCTAVE];
	return [noteName, octave];
}

/**
 * Returns true if the pitch is a note in the C-major scale.
 */
export function isPitchMajor(pitch: number): boolean {
	const [note] = pitchTuple(pitch);
	return ['C', 'D', 'E', 'F', 'G', 'A', 'B'].includes(note);
}
