import requests
import os
from dotenv import load_dotenv

load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_coordinates(location_str):
    """
    Given a location string (e.g., "London, England"), returns a tuple of (lat, lon, name).
    If the location cannot be resolved, returns (None, None, None).
    """
    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY not set in environment")

    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": location_str,
        "limit": 1,
        "appid": OPENWEATHER_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data:
            return None, None, None

        result = data[0]
        name_parts = [result.get("name")]
        if result.get("state"):
            name_parts.append(result.get("state"))
        if result.get("country"):
            name_parts.append(result.get("country"))

        name = ", ".join(name_parts)
        return result["lat"], result["lon"], name

    except Exception as e:
        print(f"[GeoUtils] Error fetching coordinates: {e}")
        return None, None, None
