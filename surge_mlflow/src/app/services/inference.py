from src.app.utils.preprocessing import preprocess_input_data
from src.app.core.mlflow.model_loader import load_model
from src.app.exceptions import ModelLoadingError, PredictionError
import pandas as pd

def make_prediction(input_data: dict) -> float:
    """_summary_

    Args:
        input_data (dict): _description_

    Returns:
        float: The prediction result.
    """
    try:
        # Preprocess input data
        preprocessed_data = preprocess_input_data(input_data)
        
        # Get the model 
        model = load_model(model_name="surge_prediction_model", stage="Production")
        
        # Predict
        prediction = model.predict(preprocessed_data)
        return float(prediction[0])
    except Exception as e:
        raise PredictionError(f"Error during prediction: {e}")