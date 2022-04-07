from abc import ABC
from datetime import datetime
from surface.base_surface import BaseSurface


class ConstantSurface(BaseSurface, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 const_rate):
        super().__init__(valuation_date)
        self.__const_rate = const_rate

    def vol(self, *args):
        return self.__const_rate
