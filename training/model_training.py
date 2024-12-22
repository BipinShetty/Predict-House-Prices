from models.model import SalePriceModel
from datasets.dataset import HousingDataset
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn
import torch

def train_and_save_model(data, model_path="trained_model.pth", epochs=10, batch_size=32, lr=0.001):
    dataset = HousingDataset(data)
    train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    model = SalePriceModel()  # Ensure this matches the updated feature count
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    for epoch in range(epochs):
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X).squeeze()
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()

    torch.save(model.state_dict(), model_path)
    print(f"Model retrained and saved to {model_path}")
