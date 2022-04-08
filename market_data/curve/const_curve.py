from abc import ABC
from market_data.curve.base_curve import BaseCurve
from datetime import datetime
import math


class ConstCurve(BaseCurve, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 rate: float):
        super().__init__(valuation_date)
        self.__rate = rate

    def rate(self, tau) -> float:
        return self.__rate

    def discount(self, tau) -> float:
        return math.exp(-self.__rate * tau)


