import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.optim as optim
from datasets.dataset import HousingDataset

class RealEstateApp:
    def __init__(self, db_handler, model_handler, llm_handler):
        self.db_handler = db_handler
        self.model_handler = model_handler
        self.llm_handler = llm_handler

    def train_model(self, data, epochs=10, batch_size=32, lr=0.001):
        dataset = HousingDataset(data)
        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        criterion = nn.MSELoss()
        optimizer = optim.Adam(self.model_handler.model.parameters(), lr=lr)

        for epoch in range(epochs):
            for batch_X, batch_y in train_loader:
                optimizer.zero_grad()
                predictions = self.model_handler.model(batch_X).squeeze()
                loss = criterion(predictions, batch_y)
                loss.backward()
                optimizer.step()
        self.model_handler.save_model()

    def predict_price(self, *inputs):
        inputs_processed = [
            float(inputs[i]) if i != 3 else 1.0 if inputs[i] == "Y" else 0.0
            for i in range(len(inputs))
        ]
        inputs_tensor = torch.tensor([inputs_processed], dtype=torch.float32)
        price = self.model_handler.model(inputs_tensor).item()
        return f"Estimated Price: ${price:,.2f}"

    def record_price(self, *inputs):
        try:
            self.db_handler.add_verified_price(*inputs)
            return "Sale price recorded successfully!"
        except Exception as e:
            return f"Error recording sale price: {str(e)}"

    def copy_values(self, *args):
        return args

    def query_closest_match(self, *inputs):
        result = self.db_handler.get_closest_match(inputs)
        return f"Closest Match: {result}" if result else "No match found."

    def generate_listing(self, *inputs):
        features, description = inputs[:-1], inputs[-1]
        full_data = self.db_handler.get_full_data_for_features(features)
        listing = self.llm_handler.generate_listing_llm(full_data, description)
        self.db_handler.record_listing(listing)
        return listing

    def record_feedback(self, listing, feedback):
        try:
            self.db_handler.record_feedback(listing, feedback)
            return "Feedback recorded successfully!"
        except Exception as e:
            return f"Error recording feedback: {str(e)}"

    def generate_customer_profiles(self, *inputs):
        full_data = self.db_handler.get_full_data_for_features(inputs)
        profiles = self.llm_handler.generate_listing_llm(full_data,description="")
        return profiles
