from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, ActiveLoop
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import VALIDATE_DOCTOR_FORM
from constants.buttons import MENU_BUTTONS
from constants.common import MENU, REQUESTED_SLOT, TEXT
from constants.messages import CHOOSE_TEXT, HELP_TEXT
from constants.slot import SLOT_DATE, SLOT_DR_ID, SLOT_TIME
from services.buttonService import ButtonService


class ValidateDoctorForm(FormValidationAction):

    def __init__(self) -> None:
        self.__buttonService=ButtonService()

    def name(self) -> Text:
        return VALIDATE_DOCTOR_FORM
    
    async def next_requested_slot(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[EventType]:
        message = tracker.latest_message.get(TEXT)
        print(message)
        if message != MENU:
            required_slots = await self.required_slots(
                self.domain_slots(domain), dispatcher, tracker, domain
            )
            if required_slots == self.domain_slots(domain):
                return None
            missing_slots = (
                slot_name
                for slot_name in required_slots
                if tracker.slots.get(slot_name) is None
            )
            return SlotSet(REQUESTED_SLOT, next(missing_slots, None))
        menu_buttons = await self.__buttonService.button(MENU_BUTTONS)
        dispatcher.utter_message(text=HELP_TEXT, buttons=menu_buttons)
        return ActiveLoop(None)

    async def validate_id(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if slot_value.isnumeric():
            return {SLOT_DR_ID: int(slot_value)}
        else:
            dispatcher.utter_message(CHOOSE_TEXT)
            return {SLOT_DR_ID: None}

    async def validate_date(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return {SLOT_DATE: slot_value}

    async def validate_time(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return {SLOT_TIME: slot_value}
