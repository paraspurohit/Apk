from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.button import Button
from constants.actions import ACTION_ASK_DATE
from constants.common import DOCTOR_DETAIL,DATE,ID,TEXT,AVAILABILITY
from constants.file import DOCTOR_DETAIL_FILE_PATH
from constants.messages import DATE_TEXT
from helper.json_Helper import JsonHelper


class ActionAskDate(Action):

    def __init__(self):
        self.__jsonhelper = JsonHelper()

    def name(self) -> Text:
        return ACTION_ASK_DATE 

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check_id = tracker.latest_message[TEXT]
        date_buttons = []
        data = self.__jsonhelper.read(DOCTOR_DETAIL_FILE_PATH)
        for doctor in data.get(DOCTOR_DETAIL):
            if check_id == doctor.get(ID):
                for dates in doctor.get(AVAILABILITY):
                    date = dates.get(DATE)
                    button = Button(date,date).dict()
                    date_buttons.append(button)
                break
        dispatcher.utter_message(text=DATE_TEXT, buttons=date_buttons)
        return []
    