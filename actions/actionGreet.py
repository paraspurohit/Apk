from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_GREET
from constants.buttons import MENU_BUTTONS
from constants.messages import GREET_TEXT, HELP_TEXT


class ActionGreet(Action):

    def name(self) -> Text:
        return ACTION_GREET

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=GREET_TEXT)
        dispatcher.utter_message(text=HELP_TEXT, buttons=MENU_BUTTONS)
        return []
    