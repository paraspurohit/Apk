from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ABOUT_US
from constants.messages import ABOUT_TEXT


class ActionAboutUs(Action):

    def name(self) -> Text:
        return ACTION_ABOUT_US

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=ABOUT_TEXT)
        return []
    