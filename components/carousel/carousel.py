from typing import Any, Dict

from components.carousel.payload import Payload
from constants.messageType import TEMPLATE


class Carousel():
    def __init__(self, payload: Dict[Payload, Any]) -> None:
        self.type = TEMPLATE
        self.payload = payload

    def dict(self):
        return self.__dict__