import pandas as pd
from database.init_db import DatabaseHandler
from models.model import SalePriceModel
from models.model_handler import ModelHandler
from app.real_state_app import RealEstateApp
from front_end.gradio_ui import RealEstateAppUI
from models.llm_handler import LLMHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_database(db_handler, data_path):
    """Initialize the database with Ames Housing dataset."""
    try:
        db_handler.initialize_database(data_path)
        logging.info("Database initialized successfully.")
    except KeyError as e:
        logging.error(f"Error initializing database: {e}")
        exit(1)

def initialize_model(model_handler, data, db_handler):
    """Initialize or train the sale price prediction model."""
    try:
        model_handler.load_model()
        logging.info("Model loaded successfully.")
    except (FileNotFoundError, EOFError):
        logging.warning("Model not found or invalid. Training a new model.")
        app = RealEstateApp(db_handler, model_handler, None)
        app.train_model(data)

def initialize_llm_handler(hf_token):
    """Initialize the LLM handler."""
    try:
        llm_handler = LLMHandler(model_name="gpt2", token=hf_token)
        logging.info("LLM Handler initialized successfully.")
        return llm_handler
    except Exception as e:
        logging.error(f"Failed to initialize LLM Handler: {e}")
        exit(1)

if __name__ == "__main__":
    # Data path
    data_path = "data/ames_housing.csv"

    # Load the data
    try:
        data = pd.read_csv(data_path)
        data.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in data.columns]
        logging.info("Dataset loaded and normalized successfully.")
    except Exception as e:
        logging.error(f"Error loading dataset: {e}")
        exit(1)

    # Initialize database
    db_handler = DatabaseHandler()
    initialize_database(db_handler, data_path)

    # Initialize model and handler
    model = SalePriceModel()
    model_handler = ModelHandler(model, model_path="trained_model.pth")
    initialize_model(model_handler, data, db_handler)

    # Hugging Face token (replace with your token)
    hf_token = "your_huggingface_token"

    # Initialize LLM Handler
    llm_handler = initialize_llm_handler(hf_token)

    # Initialize app and UI
    app = RealEstateApp(db_handler, model_handler, llm_handler)
    ui = RealEstateAppUI(app)

    # Launch UI
    ui.create_ui()
