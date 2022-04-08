from abc import ABC
from datetime import datetime
from market_data.surface.base_surface import BaseVolSurface


class ConstVolSurface(BaseVolSurface, ABC):
    def __init__(self,
                 valuation_date: datetime,
                 const_vol):
        super().__init__(valuation_date)
        self.__const_rate = const_vol

    def vol(self, *args):
        return self.__const_rate
