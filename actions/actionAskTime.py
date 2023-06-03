import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.button import Button
from constants.actions import ACTON_ASK_TIME
from constants.common import AVAILABILITY, DOCTOR_DETAIL, DATE, SLOTS,TEXT
from constants.file import DOCTOR_DETAIL_FILE_PATH
from constants.messages import TIME_TEXT
from constants.slot import SLOT_DR_ID
from helper.json_Helper import JsonHelper


class ActionAskTime(Action):

    def __init__(self) -> None:
        self.__jsonhelper = JsonHelper()

    def name(self) -> Text:
        return ACTON_ASK_TIME

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check_date = tracker.latest_message[TEXT]
        time_button = []
        flag = 0
        id = int(tracker.get_slot(SLOT_DR_ID))
        data = self.__jsonhelper.read(DOCTOR_DETAIL_FILE_PATH)
        dr_availability = data[DOCTOR_DETAIL][id][AVAILABILITY]
        for availability in dr_availability:
            if availability.get(DATE)==check_date:
                flag=1 
                for time_val in availability.get(SLOTS):
                    button = Button(time_val,time_val).dict()
                    time_button.append(button)
                break
            if flag == 1:
                break
        dispatcher.utter_message(text=TIME_TEXT, buttons=time_button)
        return []
