import os
import torch

class ModelHandler:
    def __init__(self, model, model_path="trained_model.pth"):
        self.model = model
        self.model_path = model_path

    def save_model(self):
        torch.save(self.model.state_dict(), self.model_path)
        print(f"Model saved to {self.model_path}")

    def load_model(self):
        """
        Load the model state dictionary from the saved file.
        """
        if os.path.exists(self.model_path):
            try:
                # Ensure the file is not empty
                if os.path.getsize(self.model_path) == 0:
                    raise EOFError(f"The model file at {self.model_path} is empty.")

                self.model.load_state_dict(torch.load(self.model_path))
                self.model.eval()
                print(f"Model loaded from {self.model_path}")
            except EOFError as e:
                raise EOFError(f"Failed to load model from {self.model_path}. The file might be corrupted or incomplete.") from e
            except RuntimeError as e:
                raise RuntimeError(f"Error loading model state_dict: {e}")
        else:
            raise FileNotFoundError(f"Model file not found at path: {self.model_path}")
