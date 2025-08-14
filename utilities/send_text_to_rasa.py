import requests
import logging

RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

logger = logging.getLogger("RavenSpeak")


def send_text_to_rasa(message: str, sender: str = "raven"):
    """
    Send a text message to the Rasa REST API and return the response.
    """
    try:
        payload = {"sender": sender, "message": message}
        response = requests.post(RASA_API_URL, json=payload)
        response.raise_for_status()

        data = response.json()
        for item in data:
            if 'text' in item:
                logger.info(f"[Rasa] Response: {item['text']}")
            if 'custom' in item:
                logger.info(f"[Rasa] Custom payload: {item['custom']}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error(f"[Rasa] Error sending message: {e}")
        return None
