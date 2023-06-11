from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.button import Button
from constants.actions import ACTION_ASK_DATE
from constants.common import ID, PAYLOAD, DOCTOR_SHEET, TITLE
from constants.messages import DATE_TEXT
from services.buttonService import ButtonService
from services.gsheetService import GSheetService


class ActionAskDate(Action):

    def __init__(self):
        self.__gsheetservice = GSheetService()
        self.__buttonService = ButtonService()

    def name(self) -> Text:
        return ACTION_ASK_DATE

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check_id = tracker.get_slot(ID)
        data = await self.__gsheetservice.getdata(DOCTOR_SHEET)
        date_buttons = []
        date = data[check_id][3]
        date = date.split("\n")
        for date in date:
            button = {
               TITLE : date,
               PAYLOAD : date,
            }
            date_buttons.append(button)
        date_buttons = await self.__buttonService.button(date_buttons)
        dispatcher.utter_message(text=DATE_TEXT, buttons=date_buttons)
        return []
