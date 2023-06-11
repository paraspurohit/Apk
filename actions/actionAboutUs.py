from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ABOUT_US
from constants.buttons import MENU_BUTTON
from constants.messages import ABOUT_TEXT
from services.buttonService import ButtonService


class ActionAboutUs(Action):

    def __init__(self) -> None:
        self.__buttonService = ButtonService()

    def name(self) -> Text:
        return ACTION_ABOUT_US

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        menu_button= await self.__buttonService.button(MENU_BUTTON)
        dispatcher.utter_message(text=ABOUT_TEXT, buttons=menu_button)
        return []
