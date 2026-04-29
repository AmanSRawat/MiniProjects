# Surge Pricing Engine

A FastAPI-based dynamic pricing system that calculates ride surge multipliers based on real-time weather conditions and demand/supply ratios.

## Features

- **Weather-based pricing**: Integrates with OpenWeatherMap API to adjust prices based on current weather
- **Demand analysis**: Calculates surge based on active orders vs. available riders
- **Dynamic multipliers**: Applies up to 3.0x multiplier with detailed reason codes
- **Pydantic validation**: Full request/response validation

## Installation

```bash
cd surge-engine
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your OpenWeatherMap API key:

```
api_key=your_openweathermap_api_key
```

## Usage

Start the server:

```bash
uvicorn app.main:app --reload
```

API endpoint: `POST /predict-surge`

### Request Example

```bash
curl -X POST http://localhost:8000/predict-surge \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Dehradun",
    "active_orders": 50,
    "rider_count": 30,
    "base_price": 100.0
  }'
```

### Response Example

```json
{
  "city": "Dehradun",
  "original_price": 100.0,
  "final_price": 170.0,
  "multiplier": 1.7,
  "surge_applied": true,
  "reason": "High demand: active orders exceed available riders. & Adverse weather: Rain conditions."
}
```

## Pricing Logic

| Factor | Condition | Multiplier Increase |
|--------|-----------|---------------------|
| High demand | orders > 1.5x riders | +0.5x |
| Moderate demand | orders > 1.0x riders | +0.2x |
| No riders | rider_count = 0 | +0.8x |
| Adverse weather | Rain, Snow, Thunderstorm, Drizzle | +0.3x |
| Cold weather | Temperature < 5°C | +0.2x |
| Hot weather | Temperature > 30°C | +0.2x |


## API Documentation

Interactive docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
surge-engine/
├── app/
│   ├── main.py         # FastAPI application & endpoints
│   ├── engine.py       # Surge calculation logic
│   ├── schemas.py      # Pydantic models
│   └── services.py     # Weather API integration
├── .env                # Environment variables (API keys)
├── requirements.txt    # Python dependencies
└── README.md
```

## License

MIT
