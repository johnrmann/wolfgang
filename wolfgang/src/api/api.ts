import { Song } from '../core/song';

const API_URL = 'http://localhost:8000';

function endpoint(route: string) {
	return `${API_URL}/${route}`;
}

export async function getHello() {
	const response = await fetch(endpoint('hello'), {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
		},
	});
	const data = await response.json();
	return data;
}

export async function postJsonGenerate(seed: Song) {
	const parameters = {
		seed: seed.messages,
		length: 1024,
	};
	const response = await fetch(endpoint('json/generate'), {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(parameters),
	});
	const data = await response.json();
	return data;
}
