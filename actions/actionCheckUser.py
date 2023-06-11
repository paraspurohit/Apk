from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_CHECK_USER
from constants.buttons import APPOINTMENT_BUTTON, MENU_BUTTON
from constants.common import  APPIONTMENT_SHEET, MENU, TEXT, USER_EMAIL
from constants.messages import BOOKING_TEXT, NOT_VISITED_TEXT, VISITED_TEXT
from services.buttonService import ButtonService
from services.gsheetService import GSheetService


class ActionCheckUser(Action):

    def __init__(self) -> None:
        self.__buttonServie = ButtonService()
        self.__gsheetService = GSheetService()

    def name(self) -> Text:
        return ACTION_CHECK_USER

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message.get(TEXT) == MENU:
            return []
        user_email = tracker.get_slot(USER_EMAIL)
        data = await self.__gsheetService.getdata(APPIONTMENT_SHEET)
        button = await self.__buttonServie.button(APPOINTMENT_BUTTON)
        data.pop(0)
        paitent_detail = []
        for data in data:
            if data[6] == user_email:
                paitent_detail.append(data)
                dispatcher.utter_message(text=VISITED_TEXT)
                dr_name = paitent_detail[0][1]
                date = paitent_detail[0][4]
                time = paitent_detail[0][5]
                menu_button = await self.__buttonServie.button(MENU_BUTTON)
                dispatcher.utter_message(text=BOOKING_TEXT.format(dr_name, date, time), buttons=menu_button)
                return []
        dispatcher.utter_message(text=NOT_VISITED_TEXT, buttons=button)
        return []
