from abc import ABC, abstractmethod
from datetime import datetime


class Instrument(ABC):
    def __init__(self, expiration_date: datetime):
        self.__expiration_date = expiration_date

    @property
    def expiration_date(self):
        return self.__expiration_date
