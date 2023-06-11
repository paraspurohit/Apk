from components.carousel.carousel import Carousel
from components.carousel.payload import Payload
from components.carousel.card import Card


class CarouselService():

    def carousel(self, carousel_data):
        elements = []
        for card_data in carousel_data:
            card = Card(
                card_data.get("title", None),
                card_data.get("image_url", None),
                card_data.get("subtitle", None),
                card_data.get("buttons", None)
            ).dict()
            elements.append(card)
        payload = Payload(elements).dict()
        carousel = Carousel(payload).dict()
        return carousel
