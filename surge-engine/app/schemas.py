from pydantic import BaseModel,Field
import datetime as dt

class WeatherData(BaseModel):
    city: str
    temperature: float
    condition: str
    description: str
    timestamp: dt.datetime

class SurgeRequest(BaseModel):
    city: str
    active_orders: int = Field(..., ge=0, description="Number of active orders in the city") 
    rider_count: int = Field(..., ge=0, description="Number of available riders in the city")
    base_price: float = Field(..., gt=0, description="Base price for the ride")

class SurgeResponse(BaseModel):
    city: str
    original_price: float
    final_price: float
    multiplier: float
    surge_applied: bool
    reason: str

class SurgeCalculation(BaseModel):
    multiplier: float
    reason: str