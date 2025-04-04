import torch
import argparse

from model.dataset import MidiTokenDataset
from core.song import Song
from model.model import HybridModel
from model.constants import SEQ_LENGTH, DEVICE

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

# Load dataset for vocab
print("Loading dataset and vocab...")
dataset = MidiTokenDataset(seq_length=SEQ_LENGTH)
token2id = dataset.token_to_id
id2token = dataset.id_to_token
vocab_size = len(dataset.vocab)

# Load model
print("Loading model...")
model = HybridModel(vocab_size)
model.load_state_dict(torch.load(args.model, map_location=DEVICE))
model.to(DEVICE)
model.eval()

# Starting seed: TEMPO 0 0 120, NOTE 0 0 1 60
seed_tokens = [
	"TIMESIG", "TS.4.4",
	"TEMPO", "BPM120",
	"NOTE", "D12", "P60",
	"STEP", "B1", "T0",
	"NOTE", "D12", "P62",
	"STEP", "B1", "T0",
	"NOTE", "D12", "P64",
	"STEP", "B1", "T0",
	# "NOTE", "D12", "P64",
	# "STEP", "B1", "T0",
	# "NOTE", "D12", "P64",
	# "STEP", "B1", "T0",
	# "NOTE", "D12", "P65",
	# "STEP", "B1", "T0",
	# "NOTE", "D12", "P67",
	# "STEP", "B1", "T0",
	# "NOTE", "D12", "P67",
	# "STEP", "B1", "T0",
]
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
