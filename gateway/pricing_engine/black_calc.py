from gateway.params.greeks_params import GreeksParams
from gateway.params.pricing_params import PricingParams
from market_data.market_data import MarketData
from numerics.bs_pricer.vanilla_pricer import VanillaOptionPricer
from product.instrument import Instrument
from product.options.vanilla_option import VanillaOption
from utils.numerics_util import PricingRequest
from utils.time_utils import TimeUtil


class BlackCalculator:
    @staticmethod
    def calc_vanilla_option(
            requests: list,
            instrument: VanillaOption,
            market_data: MarketData,
    ):
        results = []
        spot = market_data.spot
        strike = instrument.strike
        expiration_date = instrument.expiration_date
        valuation_date = market_data.valuation_date
        # TODO: finish the pricer
        tau = TimeUtil.time_diff_natural_day( valuation_date, expiration_date)
        r = market_data.get_discounting_rate(tau)
        vol = market_data.get_volatility(tau, strike)
        q = market_data.get_dividend_rate(tau)
        option_type = instrument.option_type
        pricer = VanillaOptionPricer(spot, strike, vol, r, q, tau, option_type)
        for request in requests:
            if request == PricingRequest.Price:
                results.append(pricer.price())
            elif request == PricingRequest.Delta:
                results.append(pricer.delta())
            elif request == PricingRequest.Gamma:
                results.append(pricer.gamma())
            elif request == PricingRequest.Vega:
                results.append(pricer.vega())
            elif request == PricingRequest.Rho:
                results.append(pricer.rho())
            elif request == PricingRequest.Phi:
                results.append(pricer.phi())
            elif request == PricingRequest.Theta:
                results.append(pricer.theta())
            else:
                raise ValueError
        return results
