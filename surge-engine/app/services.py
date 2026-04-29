import os
import logging
import requests
import datetime as dt
from dotenv import load_dotenv
from .schemas import WeatherData

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("api_key")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def fetch_weather_data(city: str) -> WeatherData | None:
    """Fetch weather data for a given city.

    Args:
        city: City name to fetch weather for

    Returns:
        WeatherData object if successful, None if failed
    """
    if not API_KEY:
        logger.error("OpenWeatherMap API key not configured")
        return None

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
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

    except requests.exceptions.Timeout:
        logger.error(f"Weather API timeout for city: {city}")
        return None
    except requests.exceptions.HTTPError as err:
        status = err.response.status_code
        if status == 404:
            logger.error(f"City not found: {city}")
        elif status == 401:
            logger.error("Invalid OpenWeatherMap API key")
        else:
            logger.error(f"Weather API HTTP error for {city}: {status}")
        return None
    except requests.exceptions.RequestException as err:
        logger.error(f"Weather API request failed for {city}: {err}")
        return None
    except KeyError as err:
        logger.error(f"Unexpected weather API response format: {err}")
        return None
    except Exception as err:
        logger.error(f"Unexpected error fetching weather for {city}: {err}")
        return None