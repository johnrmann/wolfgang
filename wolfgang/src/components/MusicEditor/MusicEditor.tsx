import React, { useState, useCallback, useEffect, useRef } from 'react';

import { Note } from '@/core/message';
import { Song } from '@/core/song';
import { MIN_PITCH, MAX_PITCH, ODE_TO_JOY } from '@/core/constants';
import { millisecondsPerTick } from '@/core/utils';

import PianoRoll from '@/components/PianoRoll/PianoRoll';

export default function MusicEditor() {
	const tickRef = useRef(0);
	const intervalRef = useRef<NodeJS.Timer | null>(null);
	const audioCache = useRef<Record<number, HTMLAudioElement>>({});

	const [song, setSong] = useState<Song>(ODE_TO_JOY);
	const [isPlaying, setIsPlaying] = useState(false);

	useEffect(() => {
		const cache: Record<number, HTMLAudioElement> = {};
		for (let pitch = MIN_PITCH; pitch <= MAX_PITCH; pitch++) {
			const audio = new Audio(`/mp3/notes/${pitch}.mp3`);
			audio.preload = 'auto';
			audio.load();
			cache[pitch] = audio;
		}
		audioCache.current = cache;
	}, []);

	const onClickPlay = useCallback(() => {
		if (isPlaying) {
			if (intervalRef.current) {
				//clearInterval(intervalRef.current);
				intervalRef.current = null;
			}
			tickRef.current = 0;
			setIsPlaying(false);
		}
		else {
			const interval = setInterval(() => {
				console.log('interval');
				const notes = song.getNotes(tickRef.current);
				if (notes) {
					notes.forEach((message) => {
						if (message.messageType !== 'NOTE') {
							return;
						}
						const note = message as Note;
						const audio = audioCache.current[note.pitch];
						if (audio) {
							audio.currentTime = 0;
							audio.play();
						}
					});
				}
				tickRef.current += 1;
			}, millisecondsPerTick(120));
			intervalRef.current = interval;
			setIsPlaying(true);
		}
	}, []);

	const playLabel = isPlaying ? 'Stop' : 'Play';

	return (
		<div>
			<h1>Music Editor</h1>
			<button onClick={onClickPlay}>{playLabel}</button>
			<PianoRoll song={song} onClickEmpty={undefined} />
		</div>
	);
}
