import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from components.user_detail import UserDetail
from constants.actions import ACTION_CONFIRMATION
from constants.common import USER_DETAIL
from constants.file import USER_DETAIL_FILE_Path
from constants.slot import SLOT_DISEASES, SLOT_EMAIL, SLOT_NAME, SLOT_PHONE
from helper.json_Helper import JsonHelper
from services.gsheetService import GSheetService


class ActionConfirmation(Action):

    def __init__(self) -> None:
        self.__jasonHelper = JsonHelper()
        self.__gsheetservice = GSheetService()

    def name(self) -> Text:
        return ACTION_CONFIRMATION

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot(SLOT_NAME)
        email = tracker.get_slot(SLOT_EMAIL)
        phone = tracker.get_slot(SLOT_PHONE)
        diseases = tracker.get_slot(SLOT_DISEASES)
        # user_detail = UserDetail(
        #                         name=name,
        #                         email=email,
        #                         phone=phone,
        #                         disease=diseases).dict()
        # await self.__jasonHelper.add(
        #                        new_data=user_detail,
        #                        user=USER_DETAIL,
        #                        FILE_Path=USER_DETAIL_FILE_Path)
        user_detail = [name,email,phone,diseases]
        self.__gsheetservice.add(user_detail)
        return []
