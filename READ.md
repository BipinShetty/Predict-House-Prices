# Real Estate Application 🏡

## Overview
This project demonstrates a scalable real estate application with features for:
- Sale price prediction and recording
- Sales listing and customer profiling

The application uses:
- **PyTorch** for sale price prediction
- **SQLite** for database storage
- **GPT-2** (local LLM) for generating property listings and customer profiles
- **Gradio** for an interactive user interface

---

## Features
1. **Sale Price Estimation and Recording**
   - Predict sale price based on property features.
   - Record verified sale prices in the database.

2. **Sales Listing and Customer Profiling**
   - Query properties that closely match selected features.
   - Generate property listings using GPT-2.
   - Generate 5 customer profiles for target properties.

3. **Light/Dark Mode Toggle**
   - Customize UI theme based on user preference.

---

## Installation and Setup

### Prerequisites
- Python 3.8+
- Hugging Face Transformers library
- PyTorch

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/real-estate-app.git
   cd real-estate-app
