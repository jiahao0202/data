from abc import ABC, abstractmethod
from datetime import datetime


class BaseVolSurface(ABC):
    def __init__(self,
                 valuation_date: datetime
                 ):
        self.__valuation_date = valuation_date

    @property
    def valuation_date(self):
        return self.__valuation_date

    @abstractmethod
    def vol(self, *args):
        raise NotImplemented
