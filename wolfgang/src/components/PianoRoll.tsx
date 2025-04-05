import React, {useEffect, useRef, useState} from 'react';

import { Song } from '../core/message';
import { isPitchMajor } from '@/core/utils';
import { MAX_PITCH } from '@/core/constants';

const NOTE_HEIGHT = 20;
const BEAT_WIDTH = 60;

const MAJOR_ROW_COLOR = '#f0f0f0';
const MINOR_ROW_COLOR = '#e0e0e0';

interface Options {
}

interface DrawPianoRollGridRowOptions {
	ctx: CanvasRenderingContext2D;
	pitch: number;
	y: number;
	width: number;
}

function drawPianoRollGridRow({
	ctx,
	pitch,
	y,
	width,
}: DrawPianoRollGridRowOptions) {
	ctx.fillStyle = isPitchMajor(pitch) ? MAJOR_ROW_COLOR : MINOR_ROW_COLOR;
	ctx.fillRect(0, y, width, NOTE_HEIGHT);
	ctx.strokeStyle = '#ccc';
	ctx.beginPath();
	ctx.moveTo(0, y);
	ctx.lineTo(width, y);
	ctx.stroke();
}

function drawPianoRollGrid(ctx: CanvasRenderingContext2D, width: number, height: number) {
	let pitch = MAX_PITCH;
	for (let i = 0; i < height; i += NOTE_HEIGHT) {
		const y = i;
		drawPianoRollGridRow({
			ctx, pitch, y, width,
		});
		pitch -= 1;
	}
}

const PianoRoll = (options: Options) => {
	const canvasRef = useRef<HTMLCanvasElement | null>(null);
	const [canvasSize, setCanvasSize] = useState({
		width: 800,
		height: 600,
	});

	useEffect(() => {
		const canvas = canvasRef.current;
		const ctx = canvas?.getContext('2d');
		if (!canvas || !ctx) {
			console.error('Failed to get canvas context');
			return;
		}

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawPianoRollGrid(ctx, canvasSize.width, canvasSize.height);
	}, []);

	return (
		<div className="piano-roll">
			<canvas
				ref={canvasRef}
				width={canvasSize.width}
				height={canvasSize.height}
				style={{border: '1px solid black', display: 'block'}}
			/>
		</div>
	);
};

export default PianoRoll;
