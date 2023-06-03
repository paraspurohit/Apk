from typing import List


class Card():

    def __init__(self, title: str, image: str, subtitle: str = None, buttons: List[dict] = None) -> None:
        self.title = title
        self.image_url = image
        if subtitle:
            self.subtitle = subtitle
        if buttons:
            self.buttons = buttons

    def dict(self):
        return self.__dict__