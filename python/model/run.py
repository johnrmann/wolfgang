import torch

from model.dataset import MidiTokenDataset
from model.model import HybridModel
from model.constants import SEQ_LENGTH, DEVICE

def get_dataset_and_model(model_path: str, debug: bool = False):
	# Load dataset for vocab
	if debug:
		print("Loading dataset and vocab...")
	dataset = MidiTokenDataset(seq_length=SEQ_LENGTH)
	vocab_size = len(dataset.vocab)

	# Load model
	if debug:
		print("Loading model...")
	model = HybridModel(vocab_size)
	model.load_state_dict(torch.load(model_path, map_location=DEVICE))
	model.to(DEVICE)
	model.eval()
	return dataset, model


def generate(dataset: MidiTokenDataset, model, seed: list[str], length: int):
	"""
	Generate a sequence of tokens using the trained model.
	"""
	
	padded = dataset.pad_sequence(seed)

	# Generate tokens
	generated = padded.copy()
	for _ in range(length):
		x = torch.tensor(generated[-dataset.seq_length:], dtype=torch.long).unsqueeze(0).to(DEVICE)
		with torch.no_grad():
			y = model(x)
			next_token = torch.argmax(y[:, -1, :], dim=-1).item()
			generated.append(next_token)

	return [dataset.id_to_token[i] for i in generated]
