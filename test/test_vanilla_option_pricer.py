import unittest
from datetime import datetime

from gateway.pricing_gateway import PricingGateway
from market_data.builder import Builder
from market_data.curve.const_curve import ConstCurve
from market_data.market_data import MarketData
from market_data.surface.const_vol_surface import ConstVolSurface
from numerics.bs_pricer.vanilla_pricer import VanillaOptionPricer
from product.options.vanilla_option import VanillaOption
from utils.numerics_util import PricingRequest
from utils.product_util import OptionTypeEnum


class TestVanillaOptionPricer(unittest.TestCase):
    def setUp(self) -> None:
        spot = 100
        r = 0.025
        q = 0.
        vol = 0.3
        option_type = OptionTypeEnum.Call
        strike = 100
        valuation_date = datetime(2021, 4, 6)
        expiration_date = datetime(2022, 4, 6)
        self.vol_surface = ConstVolSurface(valuation_date, vol)
        self.discounting_curve = ConstCurve(valuation_date, r)
        self.dividend_curve = ConstCurve(valuation_date, q)
        self.market_data = MarketData(valuation_date, spot,
                                      self.vol_surface, self.discounting_curve, self.dividend_curve)
        self.vanilla_option = VanillaOption(expiration_date=expiration_date,
                                            strike=strike,
                                            option_type=option_type)

    def test_gateway_price(self):
        pricer = VanillaOptionPricer(
            spot=self.market_data.spot,
            strike=self.vanilla_option.strike,
            vol=self.market_data.get_volatility(tau=1, strike=1),
            r=self.market_data.get_discounting_rate(tau=1),
            q=self.market_data.get_dividend_rate(tau=1),
            tau=1,
            option_type=self.vanilla_option.option_type
        )
        benchmark = [
            pricer.price(),
            pricer.delta(),
            pricer.gamma(),
            pricer.vega(),
            pricer.rho(),
            pricer.phi(),
            pricer.theta()
        ]
        requests = [
            PricingRequest.Price,
            PricingRequest.Delta,
            PricingRequest.Gamma,
            PricingRequest.Vega,
            PricingRequest.Rho,
            PricingRequest.Phi,
            PricingRequest.Theta
        ]
        pricing_params = Builder.get_analytical_pricer()
        greeks_params = Builder.get_default_greeks_params()
        results = PricingGateway.single_asset_option_pricer(
            requests=requests,
            instrument=self.vanilla_option,
            market_data=self.market_data,
            pricing_params=pricing_params,
            greeks_params=greeks_params
        )
        for i in range(len(requests)):
            self.assertAlmostEqual(results[i], benchmark[i])
