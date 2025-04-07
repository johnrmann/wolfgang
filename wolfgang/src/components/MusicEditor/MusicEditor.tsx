import React, { useState } from 'react';

import { Song } from '@/core/song';
import { ODE_TO_JOY } from '@/core/constants';

import PianoRoll from '@/components/PianoRoll/PianoRoll';
import PlayButton from './PlayButton';

export default function MusicEditor() {
	const [song, setSong] = useState<Song>(ODE_TO_JOY);

	return (
		<div>
			<h1>Music Editor</h1>
			<PlayButton song={song} />
			<PianoRoll song={song} onClickEmpty={undefined} />
		</div>
	);
}
