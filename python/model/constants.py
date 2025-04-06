import torch

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')
SEQ_LENGTH = 32
BATCH_SIZE = 16
EMBED_SIZE = 256
N_HEADS = 8
TRANSFORMER_LAYERS = 6
CNN_CHANNELS = 32
EPOCHS = 3
