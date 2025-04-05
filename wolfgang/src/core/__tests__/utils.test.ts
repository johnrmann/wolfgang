import {pitchString} from '../utils';

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
});