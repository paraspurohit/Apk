from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ASK_NAME
from constants.buttons import MENU_BUTTON
from constants.messages import ASK_NAME, BACK_TEXT
from services.buttonService import ButtonService


class ActionAskName(Action):

    def __init__(self) -> None:
        self.__buttonService=ButtonService()

    def name(self) -> Text:
        return ACTION_ASK_NAME

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        menu_buttons = await self.__buttonService.button(MENU_BUTTON)
        dispatcher.utter_message(text=ASK_NAME)
        dispatcher.utter_message(text=BACK_TEXT, buttons=menu_buttons)
        return []
