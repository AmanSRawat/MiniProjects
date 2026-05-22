# Surge Prediction MLflow Project

This project predicts surge pricing based on weather conditions using machine learning models tracked with MLflow.

## Overview

The project includes:
- Data loading from MySQL database (or CSV)
- Data preprocessing (cyclical encoding of timestamps, one-hot encoding of weather conditions)
- Model training (Random Forest, XGBoost)
- Model evaluation and tracking with MLflow
- A FastAPI service for serving predictions

## Dataset

**Important**: The dataset used in this project is synthetic/fake and was generated using the [Faker](https://faker.readthedocs.io/) library. The data resides in a MySQL database named `weatherdata` with a table `weather` containing the following columns:
- `id`: Record identifier
- `city`: City name
- `temperature`: Temperature in Celsius
- `condition`: Weather condition (Sunny, Rainy, Cloudy, Snowy, Windy)
- `description`: Textual description of weather (generated sentences)
- `timestamp`: Date and time of the record
- `surge`: Surge multiplier (target variable, range 0-3.0)

The synthetic nature of the data means it's suitable for demonstration and testing purposes but may not reflect real-world weather patterns.

## Project Structure

```
surge_mlflow/
├── .venv/                  # Virtual environment
├── mlflow.db               # MLflow SQLite database
├── mlruns/                 # MLflow artifacts
├── notebook/               # Jupyter notebooks for EDA
├── scripts/                # Pipeline execution scripts
├── src/                    # Source code
│   ├── app/                # FastAPI application
│   ├── data/               # Data loading and preprocessing
│   ├── models/             # Model training and evaluation
│   └── utils/              # Utility functions
├── dockerfile              # Docker configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables (create a `.env` file):
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=weatherdata
   ```

## Usage

### Training Pipeline

To run the complete ML pipeline (data loading, preprocessing, training, evaluation, MLflow logging):

```bash
python scripts\rulpipeline.py
```

Alternatively, you can use the modular pipeline:
```bash
python scripts\runpipeline.py
```

### API Service

To start the FastAPI prediction service:

```bash
python src\app\main.py
```

The API will be available at `http://localhost:8000`.

### MLflow UI

To view experiments and runs:
```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```
Then open `http://localhost:5000` in your browser.

## Model Information

The project experiments with:
- Random Forest Regressor
- XGBoost Regressor

Features used:
- Temperature
- Cyclical encodings of timestamp (hour, day, month sine/cosine)
- One-hot encoded weather conditions

## License

This project is for educational and demonstration purposes.

## Acknowledgments

- MLflow for experiment tracking
- Faker library for generating synthetic dataset
- Scikit-learn, XGBoost for modeling