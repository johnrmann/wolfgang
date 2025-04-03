import torch

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
SEQ_LENGTH = 32
BATCH_SIZE = 16
EMBED_SIZE = 96
N_HEADS = 2
TRANSFORMER_LAYERS = 2
CNN_CHANNELS = 32
EPOCHS = 5
