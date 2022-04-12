from gateway.params.greeks_params import GreeksParams
from gateway.params.pricing_params import PricingParams
from market_data.market_data import MarketData
from product.instrument import Instrument
from product.options.vanilla_option import VanillaOption


class BlackCalculator:
    def __init__(
            self,
            instrument: Instrument,
            market_data: MarketData,
            greeks_params: GreeksParams
    ):
        self.__instrument = instrument
        self.__market_data = market_data
        self.__greeks_params = greeks_params

    @classmethod
    def calc_vanilla_option(
            cls,
            requests: list,
            instrument: VanillaOption,
            market_data: MarketData,
            greeks_params: GreeksParams
    ):
        calculator = cls(instrument, market_data, greeks_params)
        results = []
        spot = market_data.spot
        strike = instrument.strike
        expiration_date = instrument.expiration_date
        valuation_date = market_data.valuation_date
        # TODO: finish the pricer
