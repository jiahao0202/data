from gateway.params.greeks_params import GreeksParams
from gateway.params.pricing_params import PricingParams
from gateway.pricing_engine.black_calc import BlackCalculator
from market_data.market_data import MarketData
from product.instrument import Instrument
from product.options.vanilla_option import VanillaOption
from utils.pricer_util import PricerEnum


class PricingGateway:
    @staticmethod
    def single_asset_option_pricer(
            requests: list,
            instrument: Instrument,
            market_data: MarketData,
            pricing_params: PricingParams,
            greeks_params: GreeksParams
    ):
        if pricing_params.pricing_type == PricerEnum.Analytical:
            if isinstance(instrument, VanillaOption):
                assert pricing_params.pricing_type in VanillaOption.PricingTypes, \
                    "Vanilla Option does not apply to {} pricer".format(pricing_params.pricing_type.value)
                return BlackCalculator.calc_vanilla_option(requests, instrument, market_data)
