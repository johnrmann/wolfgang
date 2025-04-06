import {Song, Note, MessageType, makeNote} from './message';

/**
 * The twelve notes of the chromatic scale.
 */
export const NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];

/**
 * The number of notes in an octave.
 */
export const NOTES_PER_OCTAVE = 12;

/**
 * The number of ticks in a quarter note.
 */
export const TICKS_PER_BEAT = 12;

// A piano will typically support pitches between A0 (21) and C8 (108).
export const MAX_PITCH = 108;
export const MIN_PITCH = 21;

export const ODE_TO_JOY: Song = {
	0: [
		makeNote(64, 12),
	],
	12: [
		makeNote(64, 12),
	],
	24: [
		makeNote(65, 12),
	],
	36: [
		makeNote(67, 12),
	],
	48: [
		makeNote(67, 12),
	],
	60: [
		makeNote(65, 12),
	],
	72: [
		makeNote(64, 12),
	],
	84: [
		makeNote(62, 12),
	],
	96: [
		makeNote(60, 12),
	],
	108: [
		makeNote(60, 12),
	],
	120: [
		makeNote(62, 12),
	],
	132: [
		makeNote(64, 12),
	],
	144: [	
		makeNote(64, 12),
	],
	156: [
		makeNote(62, 12),
	],
	168: [
		makeNote(62, 12),
	],
}