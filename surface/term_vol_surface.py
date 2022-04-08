from abc import ABC
from datetime import datetime
from numerics.interp.linear_interp import LinearInterp1d
from surface.base_surface import BaseVolSurface


class TermVolSurface(BaseVolSurface, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 terms: list,
                 vols: list):
        super().__init__(valuation_date)
        assert len(terms) == len(vols), "the lengths of terms and vols must match"
        vars = [terms[i] * vols[i] ** 2 for i in range(len(terms))]
        self.__interp = LinearInterp1d(x=terms, y=vars,)
