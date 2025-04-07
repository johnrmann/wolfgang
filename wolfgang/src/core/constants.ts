import {Note, MessageType, makeNote} from './message';
import {Song} from './song';

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

export const ODE_TO_JOY: Song = new Song();
ODE_TO_JOY.addNote(0, 12, 64);
ODE_TO_JOY.addNote(12, 12, 64);
ODE_TO_JOY.addNote(24, 12, 65);
ODE_TO_JOY.addNote(36, 12, 67);
ODE_TO_JOY.addNote(48, 12, 67);
ODE_TO_JOY.addNote(60, 12, 65);
ODE_TO_JOY.addNote(72, 12, 64);
ODE_TO_JOY.addNote(84, 12, 62);
ODE_TO_JOY.addNote(96, 12, 60);
ODE_TO_JOY.addNote(108, 12, 60);
ODE_TO_JOY.addNote(120, 12, 62);
ODE_TO_JOY.addNote(132, 12, 64);
ODE_TO_JOY.addNote(144, 18, 64);
ODE_TO_JOY.addNote(162, 6, 62);
ODE_TO_JOY.addNote(168, 24, 62);
