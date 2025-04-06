import torch
import argparse

from core.song import Song

from model.run import get_dataset_and_model
from model.constants import SEQ_LENGTH, DEVICE
from model.seeds import EMPTY_SEED

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
id2token = dataset.id_to_token
token2id = dataset.token_to_id

# Starting seed: TEMPO 0 0 120, NOTE 0 0 1 60
seed_tokens = EMPTY_SEED
sequence = [token2id[t] for t in seed_tokens]

# Pad to SEQ_LENGTH if needed
if len(sequence) < SEQ_LENGTH:
	pad_token = token2id["PAD"]  # arbitrary filler token
	sequence = [pad_token] * (SEQ_LENGTH - len(sequence)) + sequence

# Generate tokens
generated = sequence.copy()
num_tokens_to_generate = 2048
print("Generating...")

for _ in range(num_tokens_to_generate):
	x = torch.tensor(generated[-SEQ_LENGTH:], dtype=torch.long).unsqueeze(0).to(DEVICE)
	with torch.no_grad():
		logits = model(x)
	probs = torch.softmax(logits[0, -1], dim=0)
	next_token_id = torch.multinomial(probs, num_samples=1).item()
	generated.append(next_token_id)

# Convert back to readable tokens
generated_tokens = [id2token[i] for i in generated]
print("\nGenerated token sequence:\n")
print(" ".join(generated_tokens))

# Now, create a song.
if args.out:
	song = Song.from_text(generated_tokens)
	midi = song.to_midi()
	midi.save(args.out)
	print(f"\nSaved generated MIDI file to {args.out}")
