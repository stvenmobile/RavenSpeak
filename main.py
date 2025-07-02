# main.py

import os
import ctypes
from contextlib import contextmanager

\# Suppress ALSA lib warnings
def suppress_alsa_warnings():
    try:
        asound = ctypes.cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(ctypes.CFUNCTYPE(None, ctypes.c_char_p)(lambda x: None))
    except Exception as e:
        print(f"[INFO] Could not suppress ALSA warnings: {e}")

suppress_alsa_warnings()

from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
from handlers.weather_handler import get_weather_summary

# Load env variables
load_dotenv()

DEFAULT_CITY = "Matthews"
WAKE_WORD = "raven"

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 165)

def speak(text):
    print(f"[🗣️ RavenSpeak] {text}")
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"[🎧 Heard] {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print(f"[STT Error] {e}")
        return ""

def extract_city(text):
    words = text.split()
    for i, word in enumerate(words):
        if word in ["in", "at", "for"] and i + 1 < len(words):
            return words[i + 1].capitalize()
    return DEFAULT_CITY

def main_loop():
    speak("Raven is listening.")
    while True:
        text = recognize_speech()
        if WAKE_WORD in text:
            if "weather" in text or "forecast" in text:
                city = extract_city(text)
                mode = "current"
                if "hourly" in text:
                    mode = "hourly"
                elif "daily" in text or "forecast" in text:
                    mode = "daily"

                summary = get_weather_summary(city, mode)
                speak(summary)
            else:
                speak("Sorry, I only handle weather right now.")

if __name__ == "__main__":
    main_loop()
