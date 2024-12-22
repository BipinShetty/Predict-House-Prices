import torch
from torch.utils.data import Dataset
import pandas as pd

class HousingDataset(Dataset):
    def __init__(self, df):
        # Normalize column names
        df.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in df.columns]

        # Required columns
        required_columns = [
            'lotarea', 'overallqual', 'overallcond', 'centralair',
            'fullbath', 'bedroomabvgr', 'garagecars'
        ]

        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise KeyError(f"Dataset is missing one or more required columns: {missing_columns}")

        # Convert Central Air to numeric (Y -> 1, N -> 0)
        if 'centralair' in df.columns:
            df['centralair'] = df['centralair'].map({'Y': 1, 'N': 0}).fillna(0)

        # Ensure all columns are numeric
        for col in required_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        self.X = df[required_columns].values  # Features
        self.y = df['saleprice'].fillna(0).values if 'saleprice' in df.columns else None

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.X[idx], dtype=torch.float32),
            torch.tensor(self.y[idx], dtype=torch.float32) if self.y is not None else None
        )
