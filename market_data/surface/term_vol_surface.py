from abc import ABC
from datetime import datetime
from numerics.interp.linear_interp import LinearInterp1d
from market_data.surface.base_surface import BaseVolSurface
import math


class TermVolSurface(BaseVolSurface, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 terms: list,
                 term_vols: list):
        super().__init__(valuation_date)
        assert len(terms) == len(term_vols), "the lengths of terms and vols must match"
        variances = [terms[i] * term_vols[i] ** 2 for i in range(len(terms))]
        self.__interp = LinearInterp1d(x=terms, y=variances, mode='flat')
        self.__terms = terms
        self.__vols = term_vols
    
    def vol(self, tau):
        if tau <= min(self.__terms):
            return self.__vols[0]
        elif tau >= max(self.__terms):
            return self.__vols[-1]
        else:
            variance = self.__interp.interp(tau)
            return math.sqrt(variance / tau)
