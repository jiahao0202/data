from abc import ABC, abstractmethod
from datetime import datetime


class BaseCurve(ABC):
    def __init__(
            self,
            valuation_date: datetime
    ):
        self.__valuation_date = valuation_date

    @property
    def valuation_date(self) -> datetime:
        return self.__valuation_date

    @abstractmethod
    def discount(self, tau) -> float:
        raise NotImplemented

    @abstractmethod
    def rate(self, tau) -> float:
        raise NotImplemented
