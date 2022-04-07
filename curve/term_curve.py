from abc import ABC
from curve.base_curve import BaseCurve
from datetime import datetime
from numerics.interp.linear_interp import LinearInterp1d
import math


class TermCurve(BaseCurve, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 rates: list,
                 terms: list):
        super().__init__(valuation_date)
        self.__interp = LinearInterp1d(x=terms, y=rates, mode='flat')

    def rate(self, tau) -> float:
        return self.__interp.interp(tau)

    def discount(self, tau) -> float:
        return math.exp(-self.rate(tau) * tau)
