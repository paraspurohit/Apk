import re
from typing import Any, Text, Dict, List

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import VALIDATE_BOOKING_FORM
from constants.slot import SLOT_NAME, SLOT_EMAIL, SLOT_PHONE, SLOT_DISEASES
from constants.regex import DISEASE_REGEX, EMAIL_REGEX, NAME_REGEX
from constants.messages import INVALID_INPUT


class ValidateBookingForm(FormValidationAction):

    def name(self) -> Text:
        return VALIDATE_BOOKING_FORM
        
    async def validate_name(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
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
    