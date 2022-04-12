from abc import ABC
from market_data.curve.base_curve import BaseCurve
from datetime import datetime
from numerics.interp.linear_interp import LinearInterp1d
import math


class TermCurve(BaseCurve, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 rates: list,
                 terms: list):
        super().__init__(valuation_date)
        self.__terms = terms
        self.__rates = rates
        self.__interp = LinearInterp1d(x=terms, y=rates, mode='flat')

    def rate(self, tau) -> float:
        return self.__interp.interp(tau)

    def discount(self, tau) -> float:
        return math.exp(-self.rate(tau) * tau)

    def bump(self, bump_size, is_bump_pct=False):
        if is_bump_pct:
            rates = [x * (1 + bump_size) for x in self.__rates]
        else:
            rates = [x + bump_size for x in self.__rates]
        return TermCurve(self.valuation_date, rates=rates, terms=self.__terms)
