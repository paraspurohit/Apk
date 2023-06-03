from typing import List

from components.carousel.card import Card
from constants.messageType import GENERIC


class Payload():

    def __init__(self, elements: List[Card]) -> None:
        self.template_type = GENERIC
        self.elements = elements

    def dict(self):
        return self.__dict__
