export enum MessageType {
	NOTE = 'NOTE',
	TEMPO = 'TEMPO',
	TIME_SIGNATURE = 'TIME_SIGNATURE',
}

export interface Message {
	type: MessageType;
}

export interface Note extends Message {
	type: MessageType.NOTE;

	/** 60 is Middle C. */
	pitch: number;

	/** In ticks, with 12 being one quarter note. */
	duration: number;
}

export function makeNote(pitch: number, duration: number): Note {
	return {
		type: MessageType.NOTE,
		pitch,
		duration,
	};
}

export interface ChangeTempo extends Message {
	type: MessageType.TEMPO;

	/** In beats per minute. */
	tempo: number;
}

export function makeTempo(tempo: number): ChangeTempo {
	return {
		type: MessageType.TEMPO,
		tempo,
	};
}

/**
 * Nothing for now. Assume that everything defaults to 4/4.
 */
export interface ChangeTimeSignature extends Message {
	type: MessageType.TIME_SIGNATURE;

	numerator: number;
	denominator: number;
}

export function makeTimeSignature(numerator: number, denominator: number): ChangeTimeSignature {
	return {
		type: MessageType.TIME_SIGNATURE,
		numerator,
		denominator,
	};
}
