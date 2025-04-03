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
