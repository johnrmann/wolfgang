import argparse

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from model.run import get_dataset_and_model, generate
from model.seeds import MIDDLE_C_SEED

model_path = "../model/2025-04-03-e.pth"

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
		print("Generating tokens...")
		print(await request.json())
		body = await request.json()
		print(body)
		length = body.get("length", 2048)
		print("Length ", length)
		seed = body.get("seed", None)
		print(length, seed)

		if seed is None:
			seed = MIDDLE_C_SEED
		else:
			seed = seed.split()
		seed = [dataset.token_to_id[t] for t in seed]

		tokens = generate(dataset, model, seed, length)
		joined = " ".join(tokens)
		
		return {"generated": joined}
	except Exception as e:
		print(e)
		raise HTTPException(status_code=400, detail="Invalid request format")


@app.post("/json/generate")
async def json_generate():
	"""
	Generate a MIDI file using the trained model with a JSON request. We expect
	a JSON request with two fields:

	-	length: The number of tokens to generate.

	-	seed: The seed tokens to use for generation, as an array of objects.
	"""
	pass
