from typing import List


class Button():

    def __init__(self, type: str, title: str, payload: str = None, url: str = None) -> None:
        self.type=type
        self.title = title
        self.payload = payload
        self.url = url

    def dict(self):
        return self.__dict__
