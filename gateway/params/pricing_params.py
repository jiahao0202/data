from gateway.params.greeks_params import GreeksParams
from utils.pricer_util import PricerEnum


class PricingParams:
    def __init__(
            self,
            pricing_type: PricerEnum
    ):
        self.__pricing_type = pricing_type

    @property
    def pricing_type(self):
        return self.__pricing_type


class AnalyticPricingParam(PricingParams):
    def __init__(self):
        super().__init__(pricing_type=PricerEnum.Analytical)


class MCPricingParam(PricingParams):
    def __init__(self, num_paths, step_size, is_antithetic):
        super().__init__(PricerEnum.MonteCarlo)
        self.__num_paths = num_paths
        self.__step_size = step_size
        self.__is_antithetic = is_antithetic
