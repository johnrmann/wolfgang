import argparse

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from core.song import Song, SongBuilder

from model.run import get_dataset_and_model, generate
from model.seeds import MIDDLE_C_SEED

model_path = "../model/2025-04-06-pilot.pth"

app = FastAPI()
dataset, model = get_dataset_and_model(model_path, debug=False)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/hello")
async def hello():
	return {"message": "Hello, World!"}


@app.post("/tok/generate")
async def tok_generate(request: Request):
	"""
	Generate tokens using the trained model with tokens as an input. We expect
	a JSON request with two fields:

	-	length: The number of tokens to generate.

	-	seed: The seed tokens to use for generation, as a string. If left
		blank, default to 4/4 time at 120BPM with quarter-note middle C as the
		initial note.
	"""
	
	try:
		body = await request.json()
		length = body.get("length", 2048)
		seed = body.get("seed", None)

		if seed is None:
			seed = MIDDLE_C_SEED
		else:
			seed = seed.split()
		seed = [dataset.token_to_id[t] for t in seed]

		tokens = generate(dataset, model, seed, length)
		joined = " ".join(tokens)
		
		return {"generated": joined}
	except Exception as e:
		raise HTTPException(status_code=400, detail="Invalid request format")


@app.post("/json/generate")
async def json_generate(request: Request):
	"""
	Generate a MIDI file using the trained model with a JSON request. We expect
	a JSON request with two fields:

	-	length: The number of tokens to generate.

	-	seed: The seed tokens to use for generation, as an array-like object.
		The tick index of the event is the index, pointing to an array of
		notes that have a duration and pitch.
	"""
	try:
		body = await request.json()
		length = body.get("length", 2048)
		json_seed = body.get("seed", None)
		song_builder = SongBuilder()
		for time_index_str, messages in json_seed.items():
			time_index = int(time_index_str)
			for message in messages:
				if message.get('type') == 'NOTE':
					duration = message.get('duration', 0)
					pitch = message.get('pitch', 0)
					song_builder.note(time_index, duration, pitch)
				elif message.get('type') == 'TEMPO':
					tempo = message.get('tempo', 120)
					song_builder.tempo(time_index, tempo)
				elif message.get('type') == 'TIME_SIGNATURE':
					numerator = message.get('numerator', 4)
					denominator = message.get('denominator', 4)
					timesig = (numerator, denominator)
					song_builder.time_signature(time_index, timesig)
		song = song_builder.build()
		token_seed = song.to_tokens()
		tokens = generate(dataset, model, token_seed, length)
		new_song = Song.from_text(tokens)
		return {"generated": new_song.to_json()}
	except Exception as e:
		print(e)
		raise HTTPException(status_code=400, detail="Invalid request format")
