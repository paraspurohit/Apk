from typing import List


class UserDetail():

    def __init__(self, name: str, email: str, phone: str , disease: str) -> None:
        self.name = name
        self.email = email
        self.phone = phone
        self.disease = disease

    def dict(self):
        return self.__dict__