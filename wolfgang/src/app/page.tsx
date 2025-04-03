'use client';

import {useState, useCallback} from 'react';

import {getHello} from '../api/api';

export default function Home() {
	const [message, setMessage] = useState('');

	const onButtonClick = useCallback(async () => {
		const data = await getHello();
		console.log(data);
		setMessage(data.message);
	}, []);

	return (
		<main>
			<h1>Home</h1>
			<p>{message}</p>
			<button onClick={onButtonClick}>Get Hello</button>
		</main>
	);
}
