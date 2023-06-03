from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_DENY
from constants.messages import REENTER_TEXT


class ActionDeny(Action):

    def name(self) -> Text:
        return ACTION_DENY

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=REENTER_TEXT)
        return [AllSlotsReset()]
