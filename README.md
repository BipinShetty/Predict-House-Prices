# Real Estate Application 🏡

## Overview
This is a scalable real estate application designed for property agents and brokers to predict property prices, create property listings, and profile potential customers. The application combines machine learning, large language models (LLMs), and a user-friendly interface to deliver a seamless real estate experience.

---

## Features
### 1. Sale Price Estimation and Recording
- Predict the sale price of a property based on selected features using a trained PyTorch model.
- Record verified sale prices to the database for further refinement and future training.

### 2. Sales Listing and Customer Profiling
- Query the closest matching property from the database based on selected features.
- Generate a salesy property listing using GPT-2, leveraging property features and user descriptions.
- Create 5 customer profile
s tailored to the property, including occupation, income, family size, and lifestyle.
- Record user feedback (Thumbs Up/Down) for future reinforcement learning.

---

![Screen Shot 2024-12-29 at 9 28 52 PM](https://github.com/user-attachments/assets/567d611e-6826-4a4d-8b89-a92db85ff103)
![Screen Shot 2024-12-29 at 9 29 05 PM](https://github.com/user-attachments/assets/f21ee4c7-878d-469e-9bfd-6ed29bb5653d)


## Technical Stack
### Backend
- **PyTorch**: For training and inference of sale price prediction models.
- **SQLite**: As the database to store property data, verified sale prices, listings, and user feedback.

### Local LLM
- **GPT-2**: Used for generating sales listings and customer profiles.
- **Hugging Face Transformers**: For loading and interacting with GPT-2.

### User Interface
- **Gradio**: Provides a lightweight and interactive web UI for application functionalities.

### Logging
- Comprehensive logging for debugging and monitoring using Python's `logging` module.

---


## Installation and Setup

### Prerequisites
Ensure the following are installed:
- Python 3.8+
- Hugging Face Transformers library
- PyTorch
- Gradio

### Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/real-estate-app.git
   cd real-estate-app

2. python -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

3. pip install -r requirements.txt

4. python main.py

Usage
### Sale Price Estimation and Recording:

Input property features (e.g., Lot Area, Bedrooms).
Click "Predict" to estimate the sale price.
Record the verified sale price for future reference and model retraining.
Sales Listing and Customer Profiling:

Select property features and find the closest matching property.
Generate a property listing based on features and a description.
View customer profiles and record user feedback for refinement.
UI Modes:

Switch between Light and Dark modes using the toggle button.
Architecture
Components
Database Layer:

SQLite database for storing properties, listings, and feedback.
Data normalization and schema management for efficient storage and queries.
Model Layer:

### PyTorch-based SalePriceModel for price prediction.
Supports retraining and evaluation with new data.
LLM Integration:

### GPT-2 model to generate property listings and customer profiles.
Hugging Face Transformers pipeline for interaction with the LLM.
Frontend Layer:

### Gradio interface with multiple tabs for price prediction, listings, and profiling.
Scalability and Future Improvements
Current Design:
Local SQLite database and GPT-2 model for simplicity and ease of deployment.
V2 Improvements:
Database:

### Migrate to a cloud database (e.g., PostgreSQL or MongoDB) for higher scalability.
Add caching (e.g., Redis) for faster queries.
Model:

### Enhance the price prediction model with additional features.
Support online learning to dynamically adapt to new data.
LLM:

### Upgrade to larger models or fine-tuned LLMs for better listings and profiles.
Implement reinforcement learning using user feedback.
UI:

Improve responsiveness and add more customization options.
Support multi-user workflows with authentication.
Deployment:

### Deploy using containerization (e.g., Docker) and orchestration (e.g., Kubernetes).
Enable API-based interactions for integration with other systems.
Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request. Ensure code adheres to the best practices and includes necessary tests.


