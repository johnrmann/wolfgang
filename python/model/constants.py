import torch

DEVICE = torch.device('cpu')
if torch.cuda.is_available():
	DEVICE = torch.device('cuda')
elif torch.backends.mps.is_available():
	DEVICE = torch.device('mps')

SEQ_LENGTH = 64
BATCH_SIZE = 8
EMBED_SIZE = 256
N_HEADS = 8
TRANSFORMER_LAYERS = 6
CNN_CHANNELS = 32
EPOCHS = 3
