from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ASK_USER_EMAIL
from constants.messages import REACH_TEXT


class ActionAskUserEmail(Action):

    def name(self) -> Text:
        return ACTION_ASK_USER_EMAIL

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text= REACH_TEXT)
        return []
    