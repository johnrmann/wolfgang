import { TICKS_PER_BEAT } from "@/core/constants";

interface CanvasCoordinatesToSongCoordinates_Options {
	canvasDimensions: {
		width: number;
		height: number;
	};

	clickCoordinates: {
		x: number;
		y: number;
	};

	beatDimensions: {
		width: number;
		height: number;
	};

	highestPitch: number;
}

export function canvasCoordinatesToSongCoordinates({
	canvasDimensions,
	clickCoordinates,
	beatDimensions,
	highestPitch,
}: CanvasCoordinatesToSongCoordinates_Options): {
	pitch: number;
	ticks: number;
} {
	const { x: clickX, y: clickY } = clickCoordinates;
	const { width: beatWidth, height: beatHeight } = beatDimensions;

	const pitch = highestPitch - Math.floor(clickY / beatHeight);
	const ticks = Math.floor((clickX / beatWidth) * TICKS_PER_BEAT);

	return {
		pitch,
		ticks,
	};
}
