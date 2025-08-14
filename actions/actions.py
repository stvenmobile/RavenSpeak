from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from typing import Any, Dict, List, Text

# Global sleep flag
sleep_mode = False

def is_sleeping() -> bool:
    global sleep_mode
    return sleep_mode

def set_sleep_mode(state: bool) -> None:
    global sleep_mode
    sleep_mode = state

class ActionWeather(Action):
    def name(self) -> str:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        city = next(tracker.get_latest_entity_values("city"), None)
        if not city:
            dispatcher.utter_message(text="Please tell me which city you're interested in.")
            return []

        dispatcher.utter_message(text=f"The weather in {city} is sunny with 25°C.")
        return []

class ActionHandleAIRequest(Action):
    def name(self) -> str:
        return "action_handle_ai_request"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:

        model = tracker.get_slot("model") or "default"
        role = tracker.get_slot("role") or "assistant"
        temperature = tracker.get_slot("temperature") or 0.7

        dispatcher.utter_message(text=f"AI request received using model '{model}' as role '{role}' with temperature {temperature}.")
        return []

class ActionGoToSleep(Action):
    def name(self) -> str:
        return "action_go_to_sleep"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        set_sleep_mode(True)
        dispatcher.utter_message(text="Okay, I'm going to sleep now.")
        return []

class ActionWake(Action):
    def name(self) -> str:
        return "action_wake"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: DomainDict) -> List[Dict[Text, Any]]:
        set_sleep_mode(False)
        dispatcher.utter_message(text="I'm awake, how can I assist you.")
        return []
