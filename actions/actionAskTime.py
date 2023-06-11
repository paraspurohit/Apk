from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.button import Button
from constants.actions import ACTON_ASK_TIME
from constants.common import ID, PAYLOAD, DOCTOR_SHEET, TITLE
from constants.messages import TIME_TEXT
from services.buttonService import ButtonService
from services.gsheetService import GSheetService


class ActionAskTime(Action):

    def __init__(self) -> None:
        self.__gsheetservice = GSheetService()
        self.__buttonService = ButtonService()

    def name(self) -> Text:
        return ACTON_ASK_TIME

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check_id = int(tracker.get_slot(ID))
        data = await self.__gsheetservice.getdata(DOCTOR_SHEET)
        time_button = []
        time = data[check_id][4]
        time = time.split("\n")
        for time in time:
            button = {
               TITLE : time,
               PAYLOAD : time,
            }
            time_button.append(button)
        time_button = await self.__buttonService.button(time_button)
        dispatcher.utter_message(text=TIME_TEXT, buttons=time_button)
        return []
