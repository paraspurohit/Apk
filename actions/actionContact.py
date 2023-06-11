from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTON_CONTACT
from constants.buttons import MENU_BUTTON
from constants.messages import CONTACT_TEXT
from services.buttonService import ButtonService


class ActionContact(Action):

    def __init__(self) -> None:
        self.__buttonService = ButtonService()

    def name(self) -> Text:
        return ACTON_CONTACT

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        menu_button= await self.__buttonService.button(MENU_BUTTON)
        dispatcher.utter_message(text=CONTACT_TEXT, buttons=menu_button)
        return []
