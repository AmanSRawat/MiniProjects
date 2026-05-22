from src.data.preprocess import preprocess_data
import pandas as pd

def preprocess_input_data(input_data):
    """Preprocesses the input data for prediction."""
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])
    
    # RENAME 'condition' TO 'weather_condition' IF NEEDED
    if 'condition' in df.columns and 'weather_condition' not in df.columns:
        df = df.rename(columns={'condition': 'weather_condition'})
    
    # Preprocess the data using the same steps as training
    processed_df = preprocess_data(df)
    
    return processed_df