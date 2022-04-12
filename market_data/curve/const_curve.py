from abc import ABC
from market_data.curve.base_curve import BaseCurve
from datetime import datetime
import math


class ConstCurve(BaseCurve, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 const_rate: float):
        super().__init__(valuation_date)
        self.__const_rate = const_rate

    def rate(self, tau) -> float:
        return self.__const_rate

    def discount(self, tau) -> float:
        return math.exp(-self.__const_rate * tau)

    def bump(self, bump_size, is_bump_pct=False):
        if is_bump_pct:
            const_rate = self.__const_rate * (1 + bump_size)
        else:
            const_rate = self.__const_rate + bump_size
        return ConstCurve(self.valuation_date, const_rate=const_rate)
