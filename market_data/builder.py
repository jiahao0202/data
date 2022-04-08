from market_data.curve.const_curve import ConstCurve
from market_data.curve.term_curve import TermCurve
from market_data.params import VolSurfaceParam
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface
from utils.product_util import SurfaceTypeEnum


class Builder:
    # TODO builder
    @staticmethod
    def build_vol_surface(vol_param: VolSurfaceParam):
        param = vol_param.surface_param
        if vol_param.surface_type == SurfaceTypeEnum.Const:
            return ConstVolSurface(valuation_date=param['valuation_date'],
                                   const_vol=param['const_vol'])
