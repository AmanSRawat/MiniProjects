from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal

class PredictRequest(BaseModel):
    temperature: float = Field(...,ge=-50, le=50, description="Temperature in Celsius")
    condition: Literal['Sunny','Cloudy','Rainy', 'Windy', 'Snowy'] = Field(..., description="Weather condition")
    timestamp: datetime = Field(..., description="Timestamp of the prediction request")
    
    @field_validator('condition')
    def validate_condition(cls, value):
        allowed_conditions = ['Sunny', 'Cloudy', 'Rainy', 'Windy', 'Snowy']
        if value not in allowed_conditions:
            raise ValueError(f"Condition must be one of {allowed_conditions}")
        return value

class PredictResponse(BaseModel):
    surge: float = Field(..., description="Predicted surge value")
    timestamp: datetime = Field(..., description="Timestamp of the prediction response")