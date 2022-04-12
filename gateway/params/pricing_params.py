from gateway.params.greeks_params import GreeksParams
from utils.pricer_util import PricerEnum


class PricingParams:
    def __init__(self,
                 pricing_type: PricerEnum,
                 greeks_param: GreeksParams
                 ):
        self.__pricing_type = pricing_type
        self.__greeks_params = greeks_param

    @property
    def pricing_type(self):
        return self.__pricing_type

    @property
    def greeks_params(self):
        return self.__greeks_params
