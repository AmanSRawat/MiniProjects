import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def preprocess_data(df) -> pd.DataFrame:
    """Preprocesses the weather data."""
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract hour and apply cyclical encoding
    hour = df['timestamp'].dt.hour
    df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * hour / 24)
    
    # Drop original timestamp and hour columns
    df.drop(columns=['timestamp'], inplace=True)
    
    # One-hot encode categorical features
    categorical_cols = ['weather_condition']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    
    return df