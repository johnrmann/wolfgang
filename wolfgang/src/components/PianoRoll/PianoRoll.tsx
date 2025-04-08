import React, {useEffect, useRef, useState, useCallback} from 'react';

import { Note } from '../../core/message';
import { Song } from '@/core/song';
import { isPitchMajor } from '@/core/utils';
import { MAX_PITCH, TICKS_PER_BEAT } from '@/core/constants';

import {canvasCoordinatesToSongCoordinates} from './utils';

const NOTE_HEIGHT = 20;
const BEAT_WIDTH = 60;

const MAJOR_ROW_COLOR = '#f0f0f0';
const MINOR_ROW_COLOR = '#e0e0e0';

interface Options {
	song: Song;
	onClickEmpty?: ({ pitch, ticks }: { pitch: number; ticks: number }) => void;
	onClickNote?: ({ pitch, ticks }: { pitch: number; ticks: number }) => void;
}

interface CanvasInfo {
	ctx: CanvasRenderingContext2D;
	width: number;
	height: number;
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

interface DrawPianoRollNote_Options {
	canvasInfo: CanvasInfo;
	pitch: number;
	ticks: number;
	duration: number;
}

function drawPianoRollNote({ canvasInfo, pitch, ticks, duration }: DrawPianoRollNote_Options) {
	const { ctx, width, height } = canvasInfo;

	const nRow = MAX_PITCH - pitch;
	const y = nRow * NOTE_HEIGHT;
	const x = ticks * (BEAT_WIDTH / TICKS_PER_BEAT);
	const pDuration = duration / TICKS_PER_BEAT;

	ctx.fillStyle = 'rgba(255, 0, 0, 0.5)';
	ctx.fillRect(x, y, pDuration * BEAT_WIDTH, NOTE_HEIGHT);
	ctx.strokeStyle = '#000';
	ctx.strokeRect(x, y, pDuration * BEAT_WIDTH, NOTE_HEIGHT);
	ctx.fillStyle = '#000';
}

const PianoRoll = (options: Options) => {
	const {
		song,
		onClickEmpty,
		onClickNote,
	} = options;

	const canvasRef = useRef<HTMLCanvasElement | null>(null);
	const [canvasSize, setCanvasSize] = useState({
		width: 1200,
		height: 1200,
	});

	useEffect(() => {
		const canvas = canvasRef.current;
		const ctx = canvas?.getContext('2d');
		if (!canvas || !ctx) {
			console.error('Failed to get canvas context');
			return;
		}

		const canvasInfo = {
			ctx,
			width: canvas.width,
			height: canvas.height,
		};

		ctx.clearRect(0, 0, canvas.width, canvas.height);
		drawPianoRollGrid(ctx, canvasSize.width, canvasSize.height);

		const messages = song.loopMessages();
		let result = messages.next();
		while (!result.done) {
			const [ticks, message] = result.value;
			if (message.type === 'NOTE') {
				const { pitch, duration } = message as Note;
				drawPianoRollNote({
					canvasInfo,
					pitch,
					ticks: ticks,
					duration: duration,
				});
			}
			result = messages.next();
		}
	}, [song]);

	const handleClick = useCallback((event: React.MouseEvent<HTMLCanvasElement>) => {
		const canvas = canvasRef.current;
		if (!canvas) {
			console.error('Canvas not found');
			return;
		}

		const rect = canvas.getBoundingClientRect();
		const x = event.clientX - rect.left;
		const y = event.clientY - rect.top;

		const {pitch, ticks} = canvasCoordinatesToSongCoordinates({
			canvasDimensions: canvasSize,
			clickCoordinates: {x, y},
			beatDimensions: {width: BEAT_WIDTH, height: NOTE_HEIGHT},
			highestPitch: MAX_PITCH,
		});

		// onClickEmpty({pitch, ticks});
	}, [canvasSize, onClickEmpty]);

	return (
		<div className="piano-roll">
			<canvas
				ref={canvasRef}
				width={canvasSize.width}
				height={canvasSize.height}
				style={{border: '1px solid black', display: 'block'}}
				onClick={handleClick}
			/>
		</div>
	);
};

export default PianoRoll;
