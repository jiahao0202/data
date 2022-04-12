from market_data.market_data import MarketData
from product.instrument import Instrument
from product.options.vanilla_option import VanillaOption


class PricingGateway:
    @staticmethod
    def single_asset_option_pricer(
            requests: list,
            instrument: Instrument,
            market_data: MarketData,
            pricing_params
    ):
        if isinstance(instrument, VanillaOption):
            return
