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
        self.__term_vols = term_vols
    
    def vol(self, tau):
        if tau <= min(self.__terms):
            return self.__term_vols[0]
        elif tau >= max(self.__terms):
            return self.__term_vols[-1]
        else:
            variance = self.__interp.interp(tau)
            return math.sqrt(variance / tau)

    def bump(self, bump_size, is_bump_pct=False):

        # TODO: to fix the bump of term vol surface

        if is_bump_pct:
            term_vols = [x * (1 + bump_size) for x in self.__term_vols]
        else:
            term_vols = [x + bump_size for x in self.__term_vols]
        return TermVolSurface(self.valuation_date, terms=self.__terms, term_vols=term_vols)
