from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.app.core.mlflow.model_loader import load_model
from src.app.api.v1.routes import predict
    
app = FastAPI(
    title="Surge Prediction API",
    description="API for predicting surge values based on weather conditions and timestamps.",
)


@app.get("/")
async def root():
    return {"message": "Welcome to the Surge Prediction API. Use /api/v1/predict to get predictions."}

app.include_router(predict.router, prefix="/api/v1")