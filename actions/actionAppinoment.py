from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.patient_detail import PatientDetail
from constants.actions import ACTION_APPOINTMENT
from constants.common import APPIONTMENT, AVAILABILITY, BUSY, DOCTOR_DETAIL, NAME, DATE, SLOTS, TEXT
from constants.file import APPOINTMENT_FILE_PATH, DOCTOR_DETAIL_FILE_PATH
from constants.messages import BOOKING_TEXT, FAILED_TEXT
from constants.slot import SLOT_DR_ID, SLOT_NAME, SLOT_PHONE, SLOT_DATE
from helper.json_Helper import JsonHelper


class ActionAppointment(Action):

    def __init__(self) -> None:
        self.__jsonhelper = JsonHelper()

    def name(self) -> Text:
        return ACTION_APPOINTMENT

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        time = tracker.latest_message[TEXT]
        date = tracker.get_slot(SLOT_DATE)
        name = tracker.get_slot(SLOT_NAME)
        id = int(tracker.get_slot(SLOT_DR_ID))
        phone = tracker.get_slot(SLOT_PHONE)
        name = name.title()
        patient_detail = PatientDetail(
                                    Dr_id=id,
                                    Patient=name,
                                    phone=phone,
                                    date=date,
                                    time=time).dict()
        data = self.__jsonhelper.read(DOCTOR_DETAIL_FILE_PATH) 
        detail = data.get(DOCTOR_DETAIL)
        dr_name = detail[id].get(NAME)
        await self.__jsonhelper.add(
                            new_data=patient_detail,
                            user=APPIONTMENT,
                            FILE_Path=APPOINTMENT_FILE_PATH)
        dr_availability = detail[id].get(AVAILABILITY)
        for availability in dr_availability:
            if availability.get(DATE)==date:
                for time_val in availability.get(SLOTS):
                    if time_val == time:
                        index = availability.get(SLOTS).index(time_val)
                        availability[SLOTS][index] = BUSY
                        self.__jsonhelper.write_json(data)
                        dispatcher.utter_message(text=BOOKING_TEXT.format(dr_name,date,time))
                        return []
        dispatcher.utter_message(FAILED_TEXT)  
        return [] 
     