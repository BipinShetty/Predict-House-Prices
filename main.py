import pandas as pd
from database.init_db import DatabaseHandler
from models.model import SalePriceModel
from models.model_handler import ModelHandler
from app.real_state_app import RealEstateApp
from front_end.gradio_ui import RealEstateAppUI
from models.llm_handler import LLMHandler

if __name__ == "__main__":
    data_path = "data/ames_housing.csv"

    # Load the data and normalize column names
    data = pd.read_csv(data_path)
    data.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in data.columns]

    # Initialize database
    db_handler = DatabaseHandler()
    try:
        db_handler.initialize_database(data_path)
    except KeyError as e:
        print(f"Error initializing database: {e}")
        exit(1)

    # Initialize model and handler
    model = SalePriceModel()
    model_handler = ModelHandler(model, model_path="trained_model.pth")

    try:
        model_handler.load_model()
    except (FileNotFoundError, EOFError):
        print("Model not found or invalid. Training a new model.")
        app = RealEstateApp(db_handler, model_handler)
        app.train_model(data)

    hf_token = "your_huggingface_token"  # Replace with your Hugging Face token if needed

    # Initialize LLMHandler
    try:
        llm_handler = LLMHandler(model_name="gpt2", token=hf_token)
        print("LLM Handler initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize LLM Handler: {e}")
        exit(1)

    # Initialize app and UI
    app = RealEstateApp(db_handler, model_handler, llm_handler)
    ui = RealEstateAppUI(app)
    ui.create_ui()
import pandas as pd
from database.init_db import DatabaseHandler
from models.model import SalePriceModel
from models.model_handler import ModelHandler
from app.real_state_app import RealEstateApp
from front_end.gradio_ui import RealEstateAppUI
from models.llm_handler import LLMHandler

if __name__ == "__main__":
    data_path = "data/ames_housing.csv"

    # Load the data and normalize column names
    data = pd.read_csv(data_path)
    data.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in data.columns]

    # Initialize database
    db_handler = DatabaseHandler()
    try:
        db_handler.initialize_database(data_path)
    except KeyError as e:
        print(f"Error initializing database: {e}")
        exit(1)

    # Initialize model and handler
    model = SalePriceModel()
    model_handler = ModelHandler(model, model_path="trained_model.pth")

    try:
        model_handler.load_model()
    except (FileNotFoundError, EOFError):
        print("Model not found or invalid. Training a new model.")
        app = RealEstateApp(db_handler, model_handler)
        app.train_model(data)

    hf_token = "your_huggingface_token"  # Replace with your Hugging Face token if needed

    # Initialize LLMHandler
    try:
        llm_handler = LLMHandler(model_name="gpt2", token=hf_token)
        print("LLM Handler initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize LLM Handler: {e}")
        exit(1)

    # Initialize app and UI
    app = RealEstateApp(db_handler, model_handler, llm_handler)
    ui = RealEstateAppUI(app)
    ui.create_ui()
