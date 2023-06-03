from typing import List


class PatientDetail():

    def __init__(self, Dr_id: str, Patient: str, phone: str , date: str , time:str) -> None:
        self.Dr_id = Dr_id
        self.Patient = Patient
        self.phone = phone
        self.date = date
        self.time = time
    def dict(self):
        return self.__dict__