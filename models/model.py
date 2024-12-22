import torch.nn as nn

class SalePriceModel(nn.Module):
    def __init__(self):
        super(SalePriceModel, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(7, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.fc(x)
