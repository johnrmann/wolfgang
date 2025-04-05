export enum MessageType {
	NOTE = 'NOTE',
	CHANGE_TEMPO = 'CHANGE_TEMPO',
	CHANGE_TIME_SIGNATURE = 'CHANGE_TIME_SIGNATURE',
}

export interface Message {
	messageType: MessageType;
}

export interface Note extends Message {
	messageType: MessageType.NOTE;

	/** 60 is Middle C. */
	pitch: number;

	/** In ticks, with 12 being one quarter note. */
	duration: number;
}

export interface ChangeTempo extends Message {
	messageType: MessageType.CHANGE_TEMPO;

	/** In beats per minute. */
	tempo: number;
}

/**
 * Nothing for now. Assume that everything defaults to 4/4.
 */
export interface ChangeTimeSignature extends Message {
	messageType: MessageType.CHANGE_TIME_SIGNATURE;
}

export interface Song {
	[index: number]: Message[];
}
