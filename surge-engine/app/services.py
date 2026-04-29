import os
import requests
import datetime as dt
from dotenv import load_dotenv
from .schemas import WeatherData

load_dotenv()

API_KEY = os.getenv("api_key")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        response.raise_for_status() 
        
        data = response.json()
        weather_dict = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "condition": data["weather"][0]["main"], 
            "description": data["weather"][0]["description"],
            "timestamp": dt.datetime.fromtimestamp(data["dt"])
        }

        return WeatherData(**weather_dict)
        
    except requests.exceptions.HTTPError as err:
        return {"error": f"HTTP Error: {err.response.status_code}", "msg": err.response.text}
    except Exception as e:
        return {"error": str(e)}

weather = fetch_weather_data("Dehradun")
print(weather)