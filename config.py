#!/usr/bin/env python3

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# RavenSpeak Configuration

# Default LLM model to use
DEFAULT_MODEL = "llama3"

# Default role/persona for AI responses
DEFAULT_ROLE = "helpful assistant"

# Default temperature for generation randomness (0 = deterministic, 1 = creative)
DEFAULT_TEMP = 0.7

# Optional max tokens to limit length of response
MAX_TOKENS = 500

# Ollama backend URL
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Predefined roles and their system prompts
ROLE_PRESETS = {
    "Personal Assistant": "You are a reliable and efficient personal assistant. Be concise, helpful, and task-focused.",
    "Project Manager": "You are a detail-oriented project manager. Help organize tasks, timelines, and responsibilities clearly.",
    "Network Specialist": "You are a knowledgeable network technician. Provide accurate, jargon-aware support for networking issues.",
    "Software Specialist": "You are an expert software engineer. Help debug code, explain architecture, and offer best practices.",
    "Philosophy Scholar": "You are a classical philosophy scholar. Speak with insight and reflection, using examples from great thinkers.",
    "Financial Analyst": "You are a financial analyst. Offer insights into budgeting, investments, and market trends."
}


# Default location 
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
