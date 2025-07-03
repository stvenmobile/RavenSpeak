import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default location (used if not extracted from voice input)
DEFAULT_CITY = "Matthews"
DEFAULT_STATE = "North Carolina"
DEFAULT_COUNTRY = "US"

# OpenWeather settings
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_API_URL = "https://api.openweathermap.org/data/3.0/onecall"
OPENWEATHER_GEO_URL = "http://api.openweathermap.org/geo/1.0/direct"

# Piper voice model
PIPER_MODEL_PATH = "piper/en_US-amy-medium.onnx"

# Optional: voice settings
VOICE_RATE = 1.0  # Future use if supporting speaking speed, etc.

# Optional: fallback AI settings (Ollama or OpenAI)
USE_AI_BACKEND = False
AI_ENDPOINT = os.getenv("AI_ENDPOINT", "http://192.168.1.60:11435/api/generate")
