from gateway.params.greeks_params import GreeksParams
from market_data.curve.const_curve import ConstCurve
from market_data.curve.term_curve import TermCurve
from market_data.params import CurveParam, VolSurfaceParam
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface
from utils.product_util import CurveTypeEnum, SurfaceTypeEnum


class Builder:
    @staticmethod
    def build_vol_surface(vol_param: VolSurfaceParam):
        param = vol_param.surface_param
        if vol_param.surface_type == SurfaceTypeEnum.Const:
            return ConstVolSurface(valuation_date=param['valuation_date'],
                                   const_vol=param['const_vol'])
        elif vol_param.surface_type == SurfaceTypeEnum.Term:
            return TermVolSurface(valuation_date=param['valuation_date'],
                                  term_vols=param['term_vols'],
                                  terms=param['terms'])
        else:
            raise NotImplemented

    @staticmethod
    def build_curve(curve_param: CurveParam):
        param = curve_param.curve_param
        if curve_param.curve_type == CurveTypeEnum.Const:
            return ConstCurve(valuation_date=param['valuation_date'],
                              const_rate=param['const_rate'])
        elif curve_param.curve_type == CurveTypeEnum.Term:
            return TermCurve(valuation_date=param['valuation_date'],
                             terms=param['terms'],
                             rates=param['rates'])

    @staticmethod
    def get_default_greeks_params():
        return GreeksParams(1e-2, 1e-2, 1e-4, 1e-4)
