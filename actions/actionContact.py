from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTON_CONTACT
from constants.messages import CONTACT_TEXT

class ActionContact(Action):

    def name(self) -> Text:
        return ACTON_CONTACT
    
    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=CONTACT_TEXT)
        return []
    