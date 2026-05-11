from fastapi import APIRouter, HTTPException
from src.app.schema.predict import PredictRequest, PredictResponse
from src.app.services.inference import make_prediction
from datetime import datetime
from src.app.exceptions import ModelLoadingError, PredictionError,InvalidInputDataError

router = APIRouter()

@router.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest)-> PredictResponse:
    """
    Endpoint to make predictions using the trained model.

    Args:
        request (PredictRequest): The input data for prediction.

    Returns:
        PredictResponse: The predicted surge value and timestamp.
    """
    try:
        prediction_value = make_prediction(request.dict())
        response = PredictResponse(surge=prediction_value, timestamp=datetime.now())
        return response
    except InvalidInputDataError as e:
      raise HTTPException(status_code=400, detail=str(e))
    except ModelLoadingError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except PredictionError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")