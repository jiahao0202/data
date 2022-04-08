from datetime import datetime

from utils.product_util import CurveTypeEnum, SurfaceTypeEnum


class VolSurfaceParam:
    def __init__(
            self,
            surface_type: SurfaceTypeEnum,
            surface_param: dict
    ):
        self.__surface_type = surface_type
        self.__surface_param = surface_param

    @property
    def surface_type(self):
        return self.__surface_type

    @property
    def surface_param(self):
        return self.__surface_param

    @classmethod
    def create_const_vol_param(cls,
                               valuation_date: datetime,
                               const_vol: float):
        param = dict()
        param['valuation_date'] = valuation_date
        param['const_vol'] = const_vol
        return cls(SurfaceTypeEnum.Const, param)

    @classmethod
    def create_term_vol_param(cls,
                              valuation_date: datetime,
                              terms: list,
                              term_vols: list):
        param = dict()
        param['valuation_date'] = valuation_date
        param['term_vols'] = term_vols
        param['terms'] = terms
        return cls(SurfaceTypeEnum.Term, param)


class CurveParam:
    def __init__(
            self,
            curve_type: CurveTypeEnum,
            curve_param: dict
    ):
        self.__curve_type = curve_type
        self.__curve_param = curve_param

    @property
    def curve_type(self):
        return self.__curve_type

    @property
    def curve_param(self):
        return self.__curve_param

    @classmethod
    def create_const_curve_param(cls,
                                 valuation_date: datetime,
                                 const_rate: float):
        param = dict()
        param['valuation_date'] = valuation_date
        param['const_rate'] = const_rate
        return cls(CurveTypeEnum.Const, param)

    @classmethod
    def create_term_curve_param(cls,
                                valuation_date: datetime,
                                terms: list,
                                rates: list):
        param = dict()
        param['valuation_date'] = valuation_date
        param['rates'] = rates
        param['terms'] = terms
        return cls(CurveTypeEnum.Term, param)
