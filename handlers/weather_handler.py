# handlers/weather_handler.py

import requests
from config import OPENWEATHER_API_KEY, OPENWEATHER_API_URL, OPENWEATHER_GEO_URL


def get_lat_lon(city):
    """Fetch latitude and longitude for a given city name."""
    try:
        response = requests.get(OPENWEATHER_GEO_URL, params={
            "q": city,
            "limit": 1,
            "appid": OPENWEATHER_API_KEY
        })
        data = response.json()
        if not data:
            return None, None
        return data[0]["lat"], data[0]["lon"]
    except Exception as e:
        print(f"[Geo lookup error] {e}")
        return None, None

def get_weather_summary(city, mode="current"):
    """
    Get weather summary for a given city and mode:
    mode = 'current' | 'hourly' | 'daily'
    """
    if not OPENWEATHER_API_KEY:
        return "Weather API key is missing."

    lat, lon = get_lat_lon(city)
    if lat is None or lon is None:
        return f"I couldn’t find the location: {city}."

    # Decide what to exclude based on mode
    if mode == "current":
        exclude = "minutely,hourly,daily,alerts"
    elif mode == "hourly":
        exclude = "current,minutely,daily,alerts"
    elif mode == "daily":
        exclude = "current,minutely,hourly,alerts"
    else:
        return "I didn't understand the forecast type you wanted."

    try:
        response = requests.get(OPENWEATHER_API_URL, params={
            "lat": lat,
            "lon": lon,
            "exclude": exclude,
            "appid": OPENWEATHER_API_KEY,
            "units": "imperial"
        })

        if response.status_code != 200:
            return f"Weather API returned an error: {response.status_code}"

        data = response.json()

        if mode == "current":
            return _format_current(data, city)
        elif mode == "hourly":
            return _format_hourly(data, city)
        elif mode == "daily":
            return _format_daily(data, city)

    except Exception as e:
        return f"Error getting weather: {e}"

def _format_current(data, city):
    temp = int(data["current"]["temp"])
    desc = data["current"]["weather"][0]["description"]
    feels = int(data["current"]["feels_like"])
    return f"It's currently {temp} degrees in {city}, with {desc}. It feels like {feels}."

def _format_hourly(data, city):
    forecasts = data.get("hourly", [])[:3]
    if not forecasts:
        return "I couldn't get the hourly forecast."
    
    summary = f"The next few hours in {city} look like this:"
    for i, hour in enumerate(forecasts):
        temp = int(hour["temp"])
        desc = hour["weather"][0]["description"]
        summary += f" Hour {i+1}: {temp} degrees with {desc}."
    return summary

def _format_daily(data, city):
    forecasts = data.get("daily", [])[:3]
    if not forecasts:
        return "I couldn't get the daily forecast."
    
    summary = f"The forecast for the next few days in {city}:"
    for i, day in enumerate(forecasts):
        temp_max = int(day["temp"]["max"])
        temp_min = int(day["temp"]["min"])
        desc = day["weather"][0]["description"]
        summary += f" Day {i+1}: High of {temp_max}, low of {temp_min}, with {desc}."
    return summary
