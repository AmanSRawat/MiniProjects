from src.data.preprocess import preprocess_data
import pandas as pd

def preprocess_input_data(input_data):
    """Preprocesses the input data for prediction."""
    # Convert input data to DataFrame
    df = pd.DataFrame([input_data])
    
    # Preprocess the data using the same steps as training
    processed_df = preprocess_data(df)
    
    return processed_df