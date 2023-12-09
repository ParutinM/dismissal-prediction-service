import torch
import torch.nn as nn


class DismissalPredictionModel(nn.Module):
    def __init__(self):
        super(DismissalPredictionModel).__init__()