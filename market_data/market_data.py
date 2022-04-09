from builder import Builder
from curve.base_curve import BaseCurve
from datetime import datetime
from params import CurveParam, VolSurfaceParam
from surface.base_surface import BaseVolSurface


class MarketData(object):
    def __init__(self,
                 valuation_date: datetime,
                 vol_surface: BaseVolSurface,
                 discounting_curve: BaseCurve,
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

    def get_vol(self, tau, strike):
        return self.__vol_surface.vol(tau, strike)

    def get_discounting_rate(self, tau):
        return self.__discounting_curve.discount(tau)

    def get_dividend_rate(self, tau):
        return self.__dividend_curve.discount(tau)

    @classmethod
    def create_market_data(cls,
                           vol_param: VolSurfaceParam,
                           discounting_curve_param: CurveParam,
                           dividend_curve_param: CurveParam):
        valuation_date = vol_param.surface_param['valuation_date']
        vol_surface = Builder.build_vol_surface(vol_param)
        discounting_curve = Builder.build_curve(discounting_curve_param)
        dividend_curve = Builder.build_curve(dividend_curve_param)
        return cls(valuation_date=valuation_date,
                   vol_surface=vol_surface,
                   discounting_curve=discounting_curve,
                   dividend_curve=dividend_curve)
