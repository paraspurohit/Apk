import re
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.events import SlotSet, EventType, ActiveLoop
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import VALIDATE_BOOKING_FORM
from constants.buttons import MENU_BUTTONS
from constants.common import MENU, TEXT, REQUESTED_SLOT
from constants.messages import HELP_TEXT, INVALID_INPUT
from constants.regex import DISEASE_REGEX, EMAIL_REGEX, NAME_REGEX
from constants.slot import SLOT_NAME, SLOT_EMAIL, SLOT_PHONE, SLOT_DISEASES
from services.buttonService import ButtonService


class ValidateBookingForm(FormValidationAction):

    def __init__(self) -> None:
        self.__buttonService=ButtonService()

    def name(self) -> Text:
        return VALIDATE_BOOKING_FORM
    
    async def next_requested_slot(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> Optional[EventType]:
        message = tracker.latest_message.get(TEXT)
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


    async def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print(slot_value)
        if re.fullmatch(NAME_REGEX, slot_value):
            return {SLOT_NAME: slot_value}
        dispatcher.utter_message(text=INVALID_INPUT)
        return {SLOT_NAME: None}

    async def validate_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if (re.fullmatch(EMAIL_REGEX, slot_value)):
            return {SLOT_EMAIL: slot_value}
        dispatcher.utter_message(text=INVALID_INPUT)
        return {SLOT_EMAIL: None}

    async def validate_phone(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if len(slot_value) == 10 and slot_value.isnumeric():
            return {SLOT_PHONE: slot_value}
        dispatcher.utter_message(text=INVALID_INPUT)
        return {SLOT_PHONE: None}

    async def validate_diseases(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if re.fullmatch(DISEASE_REGEX, slot_value):
            return {SLOT_DISEASES: slot_value}
        dispatcher.utter_message(text=INVALID_INPUT)
        return {SLOT_DISEASES: None}
