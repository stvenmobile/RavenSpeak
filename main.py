import re
from config import DEFAULT_CITY, DEFAULT_STATE, DEFAULT_COUNTRY
from handlers.weather_handler import get_weather_summary
from tts.piper_interface import speak
from stt.mic_listener import listen_for_command

def extract_structured_location(text):
    text = text.lower().replace(",", "")
    words = text.split()

    city = None
    state = None
    country = "US"  # fallback

    if "city" in words:
        try:
            city_index = words.index("city") + 1
            city = words[city_index]
            if city_index + 1 < len(words) and words[city_index + 1] not in ["state", "country"]:
                city += " " + words[city_index + 1]
        except IndexError:
            pass

    if "state" in words:
        try:
            state_index = words.index("state") + 1
            state = words[state_index]
            if state_index + 1 < len(words) and words[state_index + 1] != "country":
                state += " " + words[state_index + 1]
        except IndexError:
            pass

    if "country" in words:
        try:
            country_index = words.index("country") + 1
            country = words[country_index]
            if country_index + 1 < len(words) and words[country_index + 1] not in ["city", "state"]:
                country += " " + words[country_index + 1]
        except IndexError:
            pass

    # If user just says "weather", return default location
    if "weather" in words and not city:
        city = "Matthews"
        state = "North Carolina"
        country = "US"

    location_parts = [part for part in [city, state, country] if part]
    return ", ".join(location_parts).title() if city else None

if __name__ == "__main__":
    print("[RavenSpeak] Ready. ")

    exit_commands = {"goodbye", "bye", "so long", "end", "shutdown", "exit", "that's all"}

    while True:
        input_text = listen_for_command()
        if not input_text:
            continue

        print(f"[🧠 STT Input] {input_text}")

        # Exit check
        lowered = input_text.lower()
        if any(cmd in lowered for cmd in exit_commands):
            speak("Goodbye. Raven signing off.")
            break

        # Strip wake word
        if lowered.startswith("raven"):
            input_text = input_text[len("raven"):].strip()
        else:
            continue  # ignore unrelated input

        city = extract_structured_location(input_text)
        if city:
            print(f"[RavenSpeak] Looking up weather for: {city}")
            try:
                summary = get_weather_summary(city)

                # Remove country from TTS speech output
                spoken_location = ", ".join(city.split(",")[:-1]) if "," in city else city
                summary = summary.replace(city, spoken_location)

                speak(summary)
            except Exception as e:
                speak("There was a problem retrieving the weather.")
                print(f"[ERROR] {e}")
        else:
            speak("Sorry, I couldn't understand the location. Please say something like 'Weather, city Charlotte, state North Carolina'.")

        print("[RavenSpeak] Listening again...\n")
