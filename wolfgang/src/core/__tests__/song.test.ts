import {Song} from '../song';

describe('Song', () => {
	describe('initialization', () => {
		it('defaults to 4/4', () => {
			const song = new Song();
			expect(song.timeSignatureAt(0)).toEqual([4, 4]);
		});
	});

	describe('(has|add|get)Note', () => {
		it('doesnt have notes by default', () => {
			const song = new Song();
			expect(song.hasNote(0, 60)).toEqual(false);
		});

		it('adds notes', () => {
			const song = new Song();
			song.addNote(0, 12, 60);
			expect(song.hasNote(0, 60)).toEqual(true);
		});

		it('knows about note length', () => {
			const song = new Song();
			song.addNote(0, 12, 60);
			for (let i = 0; i < 12; i++) {
				expect(song.hasNote(i, 60)).toEqual(true);
			}
			expect(song.hasNote(12, 60)).toEqual(false);
		});

		it('can get notes', () => {
			const song = new Song();
			song.addNote(0, 12, 60);
			expect(song.getNote(0, 60)).toEqual({
				messageType: 'NOTE',
				pitch: 60,
				duration: 12,
			});
			song.addNote(12, 6, 62);
			expect(song.getNote(15, 62)).toEqual({
				messageType: 'NOTE',
				pitch: 62,
				duration: 6,
			});
		});
	});

	describe('deleteNote', () => {
		it('returns false if the note is not found', () => {
			const song = new Song();
			expect(song.deleteNote(0, 60)).toEqual(false);
		});

		it('returns true if the note is found', () => {
			const song = new Song();
			song.addNote(0, 12, 60);
			expect(song.deleteNote(0, 60)).toEqual(true);
			expect(song.hasNote(0, 60)).toEqual(false);
		});
	});
});
