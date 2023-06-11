from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_APPOINTMENT
from constants.buttons import MENU_BUTTON
from constants.common import DOCTOR_SHEET, APPIONTMENT_SHEET, EMAIL, MENU, TEXT
from constants.messages import BOOKING_TEXT
from constants.slot import SLOT_DR_ID, SLOT_NAME, SLOT_PHONE, SLOT_DATE
from services.buttonService import ButtonService
from services.gsheetService import GSheetService


class ActionBookAppointment(Action):

    def __init__(self) -> None:
        self.__gsheetService = GSheetService()
        self.__buttonSerive = ButtonService()

    def name(self) -> Text:
        return ACTION_APPOINTMENT

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if tracker.latest_message.get(TEXT) == MENU:
            return []
        menu_button = await self.__buttonSerive.button(MENU_BUTTON)
        time = tracker.latest_message[TEXT]
        date = tracker.get_slot(SLOT_DATE)
        name = tracker.get_slot(SLOT_NAME)
        id = int(tracker.get_slot(SLOT_DR_ID))
        phone = tracker.get_slot(SLOT_PHONE)
        name = name.title()
        email = tracker.get_slot(EMAIL)
        data = await self.__gsheetService.getdata(DOCTOR_SHEET)
        dr_name = data[id][0]
        data = [id, dr_name, name, phone, date, time, email]
        await self.__gsheetService.add(data, APPIONTMENT_SHEET)
        dispatcher.utter_message(text=BOOKING_TEXT.format(dr_name, date, time),buttons=menu_button)
        return []
