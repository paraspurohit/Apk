import re
from typing import Any, Text, Dict, List

from rasa_sdk import  Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import VALIDATE_EMAIL_FORM
from constants.slot import SLOT_USER_EMAIL
from constants.regex import  EMAIL_REGEX
from constants.messages import INVALID_INPUT


class ValidateEmailForm(FormValidationAction):
    
    def name(self) -> Text:
        return VALIDATE_EMAIL_FORM
    
    async def validate_user_email(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if (re.fullmatch(EMAIL_REGEX, slot_value)):
            return {SLOT_USER_EMAIL: slot_value}
        dispatcher.utter_message(text=INVALID_INPUT)
        return {SLOT_USER_EMAIL: None}
