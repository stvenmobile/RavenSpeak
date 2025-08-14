import requests

RASA_API_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

def send_text_to_rasa(text):
    response = requests.post(
        RASA_API_ENDPOINT,
        json={"sender": "user", "message": text},
        timeout=5
    )
    if response.status_code == 200:
        messages = response.json()
        return " ".join(m.get("text", "") for m in messages if "text" in m)
    else:
        raise Exception(f"Rasa HTTP {response.status_code}: {response.text}")
