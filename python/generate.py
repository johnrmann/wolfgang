import torch
import argparse

from core.song import Song

from model.run import get_dataset_and_model, generate
from model.constants import SEQ_LENGTH, DEVICE
from model.seeds import ODE_TO_JOY_SEED

# Configuration
parser = argparse.ArgumentParser(
	description="Generate a sequence of MIDI tokens using a trained Hybrid CNN-Transformer model."
)
parser.add_argument(
	'--model',
	type=str,
	required=True,
	help="Path to save the trained model."
)
parser.add_argument(
	'--out',
	type=str,
	required=False,
	help="Path to save the generated MIDI file."
)
args = parser.parse_args()

dataset, model = get_dataset_and_model(args.model, debug=True)
id2token = dataset.vocab.id_to_token
token2id = dataset.vocab.token_to_id

# Starting seed: TEMPO 0 0 120, NOTE 0 0 1 60
seed_tokens = ODE_TO_JOY_SEED
sequence = seed_tokens[:]

# Pad to SEQ_LENGTH if needed
if len(sequence) < SEQ_LENGTH:
	pad_token = "PAD"  # arbitrary filler token
	sequence = [pad_token] * (SEQ_LENGTH - len(sequence)) + sequence

# Generate tokens
generated = sequence.copy()
num_tokens_to_generate = 2048
print("Generating...")

# Convert back to readable tokens
generated_tokens = generate(dataset, model, seed_tokens, num_tokens_to_generate)
print("\nGenerated token sequence:\n")
print(" ".join(generated_tokens))

# Now, create a song.
if args.out:
	song = Song.from_text(generated_tokens)
	midi = song.to_midi()
	midi.save(args.out)
	print(f"\nSaved generated MIDI file to {args.out}")
