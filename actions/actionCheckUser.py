import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_CHECK_USER
from constants.common import EMAIL, USER_DETAILS, USER_EMAIL
from constants.file import USER_DETAIL_FILE_Path
from constants.messages import NOT_VISITED_TEXT, VISITED_TEXT
from helper.json_Helper import JsonHelper


class ActionCheckUser(Action):

    def __init__(self) -> None:
        self.__jsonhelper = JsonHelper()

    def name(self) -> Text:
        return ACTION_CHECK_USER

    async def run(self, dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_email = tracker.get_slot(USER_EMAIL)
        data = self.__jsonhelper.read(USER_DETAIL_FILE_Path)
        user_detail = data.get(USER_DETAILS)
        for detail in user_detail:
            if user_email == detail.get(EMAIL):
                dispatcher.utter_message(text=VISITED_TEXT)
                return []
        dispatcher.utter_message(text=NOT_VISITED_TEXT)
        return []
    