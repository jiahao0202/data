from abc import ABC
from datetime import datetime
from product.instrument import Instrument
from utils.pricer_util import PricerEnum
from utils.product_util import OptionTypeEnum


class VanillaOption(Instrument, ABC):

    PricingTypes = [PricerEnum.Analytical, PricerEnum.MonteCarlo]

    def __init__(self,
                 expiration_date: datetime,
                 strike: float,
                 option_type: OptionTypeEnum,
                 ):
        super().__init__(expiration_date)
        self.__strike = strike
        self.__option_type = option_type

    @property
    def strike(self) -> float:
        return self.__strike

    @property
    def option_type(self) -> OptionTypeEnum:
        return self.__option_type

    def payoff(self, spot):
        return max(spot - self.__strike, 0.) if self.__option_type == OptionTypeEnum.Call \
            else max(self.__strike - spot, 0.)
