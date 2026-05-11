import mlflow
import mlflow.pyfunc
from functools import lru_cache
from src.app.exceptions import ModelLoadingError

@lru_cache(maxsize=1)
def load_model(model_name: str,stage: str = "Production"):
    """
    Load the trained model from the specified path.

    Args:
        model_name (str): The name of the model to load.
        stage (str): The stage from which to load the model (e.g., "Production", "Staging").
    Returns:
        The loaded model object.
    """
    
    try:
        model_uri = f"models:/{model_name}/{stage}"
        model = mlflow.pyfunc.load_model(model_uri)
        return model
    except Exception as e:
        raise ModelLoadingError(f"Error loading model from {model_uri}: {e}")