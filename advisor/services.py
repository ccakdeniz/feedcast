import requests
from datetime import datetime

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @staticmethod
    def get_forecast(lat, lon, days=10):
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": ["temperature_2m_max", "precipitation_probability_max"],
            "timezone": "auto",
            "forecast_days": days,
            "temperature_unit": "fahrenheit"
        }

        response = requests.get(WeatherService.BASE_URL, params=params)
        response.raise_for_status() # Catching if anything goes wrong with the API call
        return response.json()