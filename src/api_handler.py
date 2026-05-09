from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("Loaded API Key:", API_KEY)

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def get_current_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 401:
        print("[ERROR] Invalid API key. Check your .env file.")
        return None

    if response.status_code != 200:
        print(f"[ERROR] API error: {response.status_code}")
        return None

    return response.json()


def get_forecast(city):
    url = f"{FORECAST_URL}?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    if response.status_code == 401:
        print("[ERROR] Forecast API error: 401")
        return None

    if response.status_code != 200:
        print(f"[ERROR] Forecast API error: {response.status_code}")
        return None

    return response.json()