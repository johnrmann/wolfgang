import torch

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
SEQ_LENGTH = 32
BATCH_SIZE = 16
EMBED_SIZE = 256
N_HEADS = 2
TRANSFORMER_LAYERS = 4
CNN_CHANNELS = 32
EPOCHS = 5
