import { Message, Note, ChangeTimeSignature, makeNote, makeTimeSignature, makeTempo } from './message';

interface SongOptions {
	tempo?: number;
}

export class Song {
	private messages: Record<number, Message[]> = {};

	constructor(params?: SongOptions) {
		let startTempo = 120;
		if (params && params.tempo) {
			startTempo = params.tempo;
		}

		this.addMessage(0, makeTimeSignature(4, 4));
		this.addMessage(0, makeTempo(startTempo));
	}

	public *loopMessages(): Generator<[number, Message]> {
		for (const loopTick of Object.keys(this.messages)) {
			const atThisTick = this.messages[Number(loopTick)];
			for (const message of atThisTick) {
				yield [Number(loopTick), message];
			}
		}
	}

	public timeSignatureAt(tick: number): [number, number] {
		let num = -1;
		let denom = -1;

		for (const loopTickStr of Object.keys(this.messages)) {
			const loopTick = Number(loopTickStr);
			const atThisTick = this.messages[loopTick];
			if (loopTick > tick) {
				break;
			}
			for (const message of atThisTick) {
				if (message.messageType === 'CHANGE_TIME_SIGNATURE') {
					const timeSignature = message as ChangeTimeSignature;
					num = timeSignature.numerator;
					denom = timeSignature.denominator;
					break;
				}
			}
		}

		return [num, denom];
	}

	public addMessage(tick: number, message: Message): void {
		if (!this.messages[tick]) {
			this.messages[tick] = [];
		}
		this.messages[tick].push(message);
	}

	public deleteMessage(message: Message): boolean {
		for (const loopTick of Object.keys(this.messages)) {
			const atThisTick = this.messages[Number(loopTick)];
			const index = atThisTick.indexOf(message);
			if (index !== -1) {
				atThisTick.splice(index, 1);
				if (atThisTick.length === 0) {
					delete this.messages[Number(loopTick)];
				}
				return true;
			}
		}
		return false;
	}

	public addNote(tick: number, duration: number, pitch: number): void {
		const note = makeNote(pitch, duration);
		this.addMessage(tick, note);
	}

	public getNote(tick: number, pitch: number): Note | undefined {
		for (const loopTick of Object.keys(this.messages)) {
			const atThisTick = this.messages[Number(loopTick)];
			for (const message of atThisTick) {
				if (message.messageType === 'NOTE') {
					const note = message as Note;
					const noteStart = Number(loopTick);
					const noteEnd = noteStart + note.duration;
					if (note.pitch !== pitch) {
						continue;
					}
					if (noteStart <= tick && tick < noteEnd) {
						return note;
					}
				}
			}
		}
		return undefined;
	}

	public getNotes(tick: number): Note[] {
		const atThisTick = this.messages[tick];
		if (!atThisTick) {
			return [];
		}
		const notes: Note[] = [];
		for (const message of atThisTick) {
			if (message.messageType === 'NOTE') {
				notes.push(message as Note);
			}
		}
		return notes;
	}

	public hasNote(tick: number, pitch: number): boolean {
		return this.getNote(tick, pitch) !== undefined;
	}

	/**
	 * Remove whatever note is at the given (tick, pitch) pair. Return true
	 * if it was removed, false if it was not found.
	 */
	public deleteNote(tick: number, pitch: number): boolean {
		const toRemove = this.getNote(tick, pitch);
		if (!toRemove) {
			return false;
		}
		return this.deleteMessage(toRemove);
	}
}
