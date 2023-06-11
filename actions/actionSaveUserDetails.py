from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_CONFIRMATION
from constants.common import USER_SHEET
from constants.slot import SLOT_DISEASES, SLOT_EMAIL, SLOT_NAME, SLOT_PHONE
from services.gsheetService import GSheetService


class ActionSaveUserDetails(Action):

    def __init__(self) -> None:
        self.__gsheetservice = GSheetService()

    def name(self) -> Text:
        return ACTION_CONFIRMATION

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot(SLOT_NAME)
        email = tracker.get_slot(SLOT_EMAIL)
        phone = tracker.get_slot(SLOT_PHONE)
        diseases = tracker.get_slot(SLOT_DISEASES)
        user_detail = [name, email, phone, diseases]
        await self.__gsheetservice.add(user_detail, USER_SHEET)
        return []
