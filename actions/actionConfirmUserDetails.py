from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_DETAILS
from constants.buttons import CONFIRMATION_BUTTONS, MENU_BUTTON
from constants.common import MENU, TEXT
from constants.messages import CONFIRMATION_TEXT, USER_TEXT
from constants.slot import SLOT_NAME, SLOT_DISEASES, SLOT_EMAIL, SLOT_PHONE
from services.buttonService import ButtonService


class ActionConfirmUserDetails(Action):

    def __init__(self) -> None:
        self.__buttonService=ButtonService()
        
    def name(self) -> Text:
        return ACTION_DETAILS

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message.get(TEXT) == MENU:
            return []
        confirmation_button = await self.__buttonService.button(CONFIRMATION_BUTTONS)
        name = tracker.get_slot(SLOT_NAME)
        email = tracker.get_slot(SLOT_EMAIL)
        phone = tracker.get_slot(SLOT_PHONE)
        diseases = tracker.get_slot(SLOT_DISEASES)
        msg = f"{CONFIRMATION_TEXT} \n {USER_TEXT.format(name,email,phone,diseases)}"
        dispatcher.utter_message(text=msg, buttons=confirmation_button)
        return []
