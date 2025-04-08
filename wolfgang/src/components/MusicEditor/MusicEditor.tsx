import React, { useState, useCallback } from 'react';

import { postJsonGenerate } from '@/api/api';

import { Song } from '@/core/song';
import { EMPTY_SONG } from '@/core/constants';

import PianoRoll from '@/components/PianoRoll/PianoRoll';
import PlayButton from './PlayButton';

export default function MusicEditor() {
	const [song, setSong] = useState<Song>(EMPTY_SONG);

	const onClickSubmit = useCallback(async () => {
		const generatedSong = await postJsonGenerate(song);
		const newSong = new Song();
		newSong.messages = generatedSong.generated;
		setSong(newSong);
	}, []);

	return (
		<div>
			<h1>Music Editor</h1>
			<PlayButton song={song} />
			<button onClick={onClickSubmit}>Generate</button>
			<PianoRoll song={song} onClickEmpty={undefined} />
		</div>
	);
}
