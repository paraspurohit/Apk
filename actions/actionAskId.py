import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ASK_ID
from constants.common import CONSULT, DOCTOR_DETAIL, ID, SPECIALITY,NAME
from constants.file import DOCTOR_DETAIL_FILE_PATH
from services.carouselService import CarouselService


class ActionAskId(Action):

    def __init__(self) -> None:
        self.__carouselService = CarouselService()

    def name(self) -> Text:
        return ACTION_ASK_ID

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        elements = []
        file = open(DOCTOR_DETAIL_FILE_PATH)
        data = json.load(file)
        for doctor in data.get(DOCTOR_DETAIL):
            element = {
                    "title": f"{doctor.get(NAME)}",
                    "subtitle": f"{doctor.get(SPECIALITY)}",
                    "image_url": "https://i.imgur.com/f72nzh0.jpg",
                    "buttons": [{
                        "title": CONSULT,
                        "type": "postback",
                        "payload": f"{doctor.get(ID)}"
                    },
                    ]
                } 
            elements.append(element)
        file.close()
        attachment = self.__carouselService.carousel(elements)
        dispatcher.utter_message(attachment=attachment)
        return []
    