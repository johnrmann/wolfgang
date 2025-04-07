import React, { useRef, useState, useEffect, useCallback } from 'react';

import { Song } from '@/core/song';
import { MIN_PITCH, MAX_PITCH } from '@/core/constants';
import { millisecondsPerTick } from '@/core/utils';

interface Options {
	song: Song;
}

type BufferMap = Record<number, AudioBuffer | null>;

const PlayButton = ({ song }: Options) => {
	const audioContextRef = useRef<AudioContext | null>(null);
	const [buffers, setBuffers] = useState<BufferMap>({});

	const [isPlaying, setIsPlaying] = useState(false);

	const sourcesRef = useRef<AudioBufferSourceNode[]>([]);

	useEffect(() => {
		const ctx = new AudioContext();
		audioContextRef.current = ctx;

		const loadAudio = async () => {
			const loadedBuffers: BufferMap = {};
			for (let i = MIN_PITCH; i <= MAX_PITCH; i++) {
				const response = await fetch(`/mp3/notes/${i}.mp3`);
				const arrayBuffer = await response.arrayBuffer();
				const audioBuffer = await ctx.decodeAudioData(arrayBuffer);
				loadedBuffers[i] = audioBuffer;
			}
			setBuffers(loadedBuffers);
		};

		loadAudio();

		return () => {
			ctx.close();
		};
	}, []);

	const onClickPlay = useCallback(() => {
		if (!audioContextRef.current) return;
	
		if (isPlaying) {
			// Stop all scheduled notes
			sourcesRef.current.forEach((src) => {
			try {
			  src.stop(0);
			} catch (e) {
			  /* no-op if it’s already ended */
			}
		  });
		  sourcesRef.current = [];
		  setIsPlaying(false);
		  return;
		}
	
		// If we have no buffers yet, just return
		if (Object.keys(buffers).length === 0) {
		  return;
		}
	
		// Start scheduling
		const ctx = audioContextRef.current;
		const now = ctx.currentTime;
		const tempoBpm = 120;
		const secondsPerTick = millisecondsPerTick(tempoBpm) / 1000;
	
		// Clear any old sources array
		sourcesRef.current = [];
	
		const allNotes = song.allNotes(); // or however your Song class works
	
		let iteration = allNotes.next();
		while (!iteration.done) {
			const [tick, note] = iteration.value;
			const startTime = now + (tick * secondsPerTick);
			const src = ctx.createBufferSource();
			src.buffer = buffers[note.pitch] || null;
			if (src.buffer) {
				src.connect(ctx.destination);
				// schedule exactly
				src.start(startTime);
				sourcesRef.current.push(src);
			}
			iteration = allNotes.next();
		}
	
		setIsPlaying(true);
	  }, [isPlaying, song, buffers]);

	const playLabel = isPlaying ? 'Stop' : 'Play';

	return (
		<button onClick={onClickPlay}>
			{playLabel}
		</button>
	);
};

export default PlayButton;
