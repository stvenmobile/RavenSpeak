import re
import logging
import requests
from config import DEFAULT_CITY, DEFAULT_STATE, DEFAULT_COUNTRY
from handlers.weather_handler import get_weather_summary
from tts.piper_interface import speak
from stt.mic_listener import listen_for_command
from utilities.rasa_client import send_text_to_rasa

# Setup logging to match rscontrol
logging.basicConfig(
    filename="/tmp/ravenspeak.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("RavenSpeak")

TWO_WORD_CITIES = [
    "los gatos",
    "los angeles",
    "new york",
    "virginia beach",
    "st. croix",
    "san diego",
    "new orleans",
    "st. pauls",
    "winston salem"
]

TWO_WORD_STATES = [
    "north carolina",
    "south carolina",
    "west virginia",
    "north dakota",
    "south dakota",
    "new mexico",
    "new hampshire",
    "rhode island",
    "new jersey",
    "district of columbia",
    "washington dc",
    "washington, dc"
]

def extract_structured_location(text):
    text = text.lower().replace(",", "")
    words = text.split()

    for i in range(len(words) - 1):
        city_candidate = f"{words[i]} {words[i+1]}"
        if city_candidate in TWO_WORD_CITIES:
            return city_candidate.title()

    for i in range(len(words) - 1):
        state_candidate = f"{words[i]} {words[i+1]}"
        if state_candidate in TWO_WORD_STATES and i >= 1:
            city = words[i - 1]
            return f"{city.title()}, {state_candidate.title()}"

    if "in" in words:
        idx = words.index("in")
        city = " ".join(words[idx + 1:])
        return city.title() if city else None

    if "weather" in words:
        return f"{DEFAULT_CITY}, {DEFAULT_STATE}, {DEFAULT_COUNTRY}"

    return None

def contains_english_word(text):
    return any(re.match(r"^[a-zA-Z]+$", word) for word in text.strip().split())

def main():
    print("[RavenSpeak] Ready. Listening for microphone input.")
    logger.info("Raven is listening...")

    exit_commands = {"goodbye", "bye", "so long", "end", "shutdown", "exit", "that's all"}
    asleep = False

    while True:
        input_text = listen_for_command()
        if not input_text:
            continue

        logger.info(f"User said: {input_text}")
        print(f"[🧠 STT Input]  {input_text}")

        lowered = input_text.lower().strip(".,!? ")

        if any(cmd in lowered for cmd in exit_commands):
            speak("Goodbye. Raven signing off.")
            logger.info("Exit command received. Shutting down.")
            break

        if asleep:
            if "wake up" in lowered:
                asleep = False
                speak("I'm awake now. How can I help?")
                logger.info("Raven woke up.")
            else:
                logger.info("Ignored input while asleep.")
                continue
        else:
            if not contains_english_word(lowered):
                logger.info("Ignoring input with no valid English words.")
                continue

            if "go to sleep" in lowered or "sleep" in lowered:
                asleep = True
                speak("I'm going to sleep now. Say 'wake up' if you need me.")
                logger.info("Raven is now asleep.")
                continue

            if lowered.startswith("raven"):
                lowered = lowered[len("raven"):].strip(" ,.:;!?")

            if "weather" in lowered:
                city = extract_structured_location(lowered)
                if city:
                    print(f"[RavenSpeak] Looking up weather for: {city}")
                    logger.info(f"Fetching weather for: {city}")
                    try:
                        summary = get_weather_summary(city)
                        spoken_location = ", ".join(city.split(",")[:-1]) if "," in city else city
                        summary = summary.replace(city, spoken_location)
                        speak(summary)
                        logger.info(f"Spoken weather summary: {summary}")
                    except Exception as e:
                        speak("There was a problem retrieving the weather.")
                        logger.error(f"Weather retrieval failed: {e}")
                else:
                    speak("Sorry, I couldn't understand the location. Please try again.")
                    logger.warning("Failed to extract location from input.")
            else:
                try:
                    response = send_text_to_rasa(input_text)
                    speak(response)
                except Exception as e:
                    speak("There was a problem communicating with Rasa.")
                    logger.error(f"Rasa communication failed: {e}")

        print("[RavenSpeak] Listening again...\n")
        logger.info("Raven is listening again...")

if __name__ == "__main__":
    main()
