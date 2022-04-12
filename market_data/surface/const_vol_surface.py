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

    def bump(self, bump_size, is_bump_pct=False):
        if is_bump_pct:
            const_vol = self.__const_rate * (1 + bump_size)
        else:
            const_vol = self.__const_rate + bump_size
        return ConstVolSurface(self.valuation_date, const_vol=const_vol)
