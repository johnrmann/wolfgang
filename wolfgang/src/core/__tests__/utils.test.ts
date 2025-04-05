import {pitchString, pitchTuple, isPitchMajor} from '../utils';

describe('utils', () => {
	describe('pitchString', () => {
		it('recognizes C4', () => {
			expect(pitchString(60)).toEqual('C4');
		});

		it('recognizes C#4', () => {
			expect(pitchString(61)).toEqual('C#4');
		});

		it('recognizes D4', () => {
			expect(pitchString(62)).toEqual('D4');
		});

		it('recognizes C5', () => {
			expect(pitchString(72)).toEqual('C5');
		});
	});

	describe('pitchTuple', () => {
		it('recognizes C4', () => {
			expect(pitchTuple(60)).toEqual(['C', 4]);
		});

		it('recognizes C#4', () => {
			expect(pitchTuple(61)).toEqual(['C#', 4]);
		});

		it('recognizes D4', () => {
			expect(pitchTuple(62)).toEqual(['D', 4]);
		});

		it('recognizes C5', () => {
			expect(pitchTuple(72)).toEqual(['C', 5]);
		});
	});

	describe('isPitchMajor', () => {
		it('recognizes C4 as major', () => {
			expect(isPitchMajor(60)).toEqual(true);
		});

		it('recognizes C#4 as minor', () => {
			expect(isPitchMajor(61)).toEqual(false);
		});

		it('recognizes D4 as major', () => {
			expect(isPitchMajor(62)).toEqual(true);
		});

		it('recognizes C5 as major', () => {
			expect(isPitchMajor(72)).toEqual(true);
		});
	});
});
