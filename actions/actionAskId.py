from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from constants.actions import ACTION_ASK_ID
from constants.common import CONSULT, DOCTOR_SHEET
from services.carouselService import CarouselService
from services.gsheetService import GSheetService


class ActionAskId(Action):

    def __init__(self) -> None:
        self.__carouselService = CarouselService()
        self.__gsheetService = GSheetService()

    def name(self) -> Text:
        return ACTION_ASK_ID

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        elements = []
        doc_detail = await self.__gsheetService.getdata(DOCTOR_SHEET)
        doc_detail.pop(0)
        for count,detail in enumerate(doc_detail,1):
            element = {
                "title": f"{detail[0]}",
                "subtitle": f"{detail[1]}",
                "image_url": detail[2],
                "buttons": [{
                    "title": CONSULT,
                    "type": "postback",
                    "payload": f"{count}"
                },
                ]
            }
            elements.append(element)
        attachment = self.__carouselService.carousel(elements)
        dispatcher.utter_message(attachment=attachment)
        return []
