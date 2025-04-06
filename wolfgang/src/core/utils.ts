import {NOTES, NOTES_PER_OCTAVE, TICKS_PER_BEAT} from './constants';

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

export function millisecondsPerBeat(tempo: number): number {
	// 60 seconds in a minute / beats per minute * 1000 milliseconds in a second
	return (60 / tempo) * 1000;
}

export function millisecondsPerTick(tempo: number): number {
	return millisecondsPerBeat(tempo) / TICKS_PER_BEAT;
}