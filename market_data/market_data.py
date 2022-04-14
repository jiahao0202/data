from datetime import datetime
from market_data.builder import Builder
from market_data.curve.base_curve import BaseCurve
from market_data.surface.base_surface import BaseVolSurface
from market_data.market_data_params import CurveParam, VolSurfaceParam


class MarketData(object):
    def __init__(self,
                 valuation_date: datetime,
                 spot: float,
                 vol_surface: BaseVolSurface,
                 discounting_curve: BaseCurve,
                 dividend_curve: BaseCurve
                 ):
        self.__valuation_date = valuation_date
        self.__spot = spot
        self.__vol_surface = vol_surface
        self.__discounting_curve = discounting_curve
        self.__dividend_curve = dividend_curve

    @property
    def valuation_date(self) -> datetime:
        return self.__valuation_date

    @property
    def spot(self) -> float:
        return self.__spot

    @property
    def vol_surface(self) -> BaseVolSurface:
        return self.__vol_surface

    @property
    def discounting_curve(self) -> BaseCurve:
        return self.__discounting_curve

    @property
    def dividend_curve(self) -> BaseCurve:
        return self.__dividend_curve

    def get_volatility(self, tau, strike):
        return self.__vol_surface.vol(tau, strike)

    def get_discounting_rate(self, tau):
        return self.__discounting_curve.discount(tau)

    def get_dividend_rate(self, tau):
        return self.__dividend_curve.discount(tau)

    @classmethod
    def create_market_data(cls,
                           spot: float,
                           vol_param: VolSurfaceParam,
                           discounting_curve_param: CurveParam,
                           dividend_curve_param: CurveParam):
        valuation_date = vol_param.surface_param['valuation_date']
        vol_surface = Builder.build_vol_surface(vol_param)
        discounting_curve = Builder.build_curve(discounting_curve_param)
        dividend_curve = Builder.build_curve(dividend_curve_param)
        return cls(valuation_date=valuation_date,
                   spot=spot,
                   vol_surface=vol_surface,
                   discounting_curve=discounting_curve,
                   dividend_curve=dividend_curve)
