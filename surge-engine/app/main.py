import logging
from fastapi import FastAPI
from .schemas import SurgeRequest, SurgeResponse
from .services import fetch_weather_data
from .engine import calculate_surge_multiplier
from fastapi import HTTPException

logger = logging.getLogger(__name__)

app = FastAPI(tags=["Surge Pricing Engine"])

@app.get("/",tags = ["Feature Check"])
def read_root():
    return {"message": "Surge Pricing Engine is up and running!"}

@app.post("/predict-surge", response_model=SurgeResponse, tags=["Surge Prediction"])
def predict_surge(request: SurgeRequest):
    weather = fetch_weather_data(request.city)

    if weather is None:
        logger.error(f"Failed to fetch weather data for city: {request.city}")
        raise HTTPException(
            status_code=400,
            detail=f"Could not fetch weather data for '{request.city}'. Please check the city name and try again."
        )
    surge_calculation = calculate_surge_multiplier(request, weather)
    final_price = round(request.base_price * surge_calculation.multiplier, 2)
    return SurgeResponse(
        city=request.city,
        original_price=request.base_price,
        final_price=final_price,
        multiplier=surge_calculation.multiplier,
        surge_applied=surge_calculation.multiplier > 1.0,
        reason=surge_calculation.reason
    )