# stt/mic_listener.py

import speech_recognition as sr

def listen_for_command(timeout=None, phrase_time_limit=10):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            print(f"🗣️ Heard: {text}")
            return text
        except sr.UnknownValueError:
            print("🤷 Could not understand audio.")
        except sr.RequestError as e:
            print(f"❌ API Error: {e}")
    
    return None
