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
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=False)

    # Ensure all expected weather condition columns are present
    # The model was trained with these specific categories
    expected_condition_columns = [
        'weather_condition_rainy',
        'weather_condition_snowy',
        'weather_condition_sunny',
        'weather_condition_windy'
    ]

    # Add any missing condition columns with default value 0 (False)
    for col in expected_condition_columns:
        if col not in df.columns:
            df[col] = False

    # Reorder columns to put condition columns together (optional, for consistency)
    # This ensures the column order matches what the model expects
    condition_cols_present = [col for col in expected_condition_columns if col in df.columns]
    other_cols = [col for col in df.columns if col not in expected_condition_columns]
    # Reorder: other columns first, then condition columns in expected order
    df = df[other_cols + condition_cols_present]

    return df