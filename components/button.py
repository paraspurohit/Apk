from typing import List


class Button():

    def __init__(self, title: str, payload: str) -> None:
        self.title = title
        self.payload = payload

    def dict(self):
        return self.__dict__