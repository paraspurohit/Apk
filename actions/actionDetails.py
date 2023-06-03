from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_DETAILS
from constants.slot import SLOT_NAME, SLOT_DISEASES, SLOT_EMAIL, SLOT_PHONE
from constants.buttons import CONFIRMATION_BUTTONS
from constants.messages import CONFIRMATION_TEXT, USER_TEXT


class ActionDetails(Action):

    def name(self) -> Text:
        return ACTION_DETAILS

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot(SLOT_NAME)
        email = tracker.get_slot(SLOT_EMAIL)
        phone = tracker.get_slot(SLOT_PHONE)
        diseases = tracker.get_slot(SLOT_DISEASES)
        msg = f"{CONFIRMATION_TEXT} \n {USER_TEXT.format(name,email,phone,diseases)}"
        dispatcher.utter_message(text=msg,buttons=CONFIRMATION_BUTTONS)
        return []
    