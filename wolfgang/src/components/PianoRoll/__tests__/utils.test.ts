import {canvasCoordinatesToSongCoordinates} from "../utils";

describe('canvasCoordinatesToSongCoordinates', () => {
	const BEAT_DIMS = {
		width: 48,
		height: 20,
	};

	const CANVAS_DIMS = {
		width: 800,
		height: 600,
	};

	const HIGHEST_PITCH = 108;

	it('can recognize the first tick at the highest pitch', () => {
		const {pitch, ticks} = canvasCoordinatesToSongCoordinates({
			canvasDimensions: CANVAS_DIMS,
			clickCoordinates: {
				x: 0,
				y: 0,
			},
			beatDimensions: BEAT_DIMS,
			highestPitch: HIGHEST_PITCH,
		});
		expect(pitch).toBe(HIGHEST_PITCH);
		expect(ticks).toBe(0);
	});

	it('can recognize the first tick at the highest pitch with padding', () => {
		const {pitch, ticks} = canvasCoordinatesToSongCoordinates({
			canvasDimensions: CANVAS_DIMS,
			clickCoordinates: {
				x: 1,
				y: 19,
			},
			beatDimensions: BEAT_DIMS,
			highestPitch: HIGHEST_PITCH,
		});
		expect(pitch).toBe(HIGHEST_PITCH);
		expect(ticks).toBe(0);
	});

	it('can recognize the second tick at the highest pitch', () => {
		const {pitch, ticks} = canvasCoordinatesToSongCoordinates({
			canvasDimensions: CANVAS_DIMS,
			clickCoordinates: {
				x: 4,
				y: 19,
			},
			beatDimensions: BEAT_DIMS,
			highestPitch: HIGHEST_PITCH,
		});
		expect(pitch).toBe(HIGHEST_PITCH);
		expect(ticks).toBe(1);
	});
});
