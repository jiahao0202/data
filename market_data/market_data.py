from curve.base_curve import BaseCurve
from curve.const_curve import ConstCurve
from curve.term_curve import TermCurve
from datetime import datetime
from surface.base_surface import BaseVolSurface
from surface.const_vol_surface import ConstVolSurface
from surface.term_vol_surface import TermVolSurface


class MarketData(object):
    def __init__(self,
                 valuation_date: datetime,
                 vol_surface: BaseVolSurface,
                 discounting_curve, BaseCurve,
                 dividend_curve: BaseCurve
                 ):
        self.__valuation_date = valuation_date
        self.__vol_surface = vol_surface
        self.__discounting_curve = discounting_curve
        self.__dividend_curve = dividend_curve

    @property
    def valuation_date(self) -> datetime:
        return self.__valuation_date

    @property
    def vol_surface(self) -> BaseVolSurface:
        return self.__vol_surface

    @property
    def discounting_curve(self) -> BaseCurve:
        return self.__discounting_curve

    @property
    def dividend_curve(self) -> BaseCurve:
        return self.__dividend_curve
