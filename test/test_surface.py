import unittest
from datetime import datetime
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface


class TestSurface(unittest.TestCase):
    def setUp(self) -> None:
        valuation_date = datetime(2020, 1, 1)
        self.const_rate = 0.3
        self.const_surface = ConstVolSurface(valuation_date=valuation_date,
                                             const_rate=self.const_rate
                                             )
        self.term_vol_surface = TermVolSurface(valuation_date=valuation_date,
                                               terms=[0.5, 1, 2],
                                               vols=[0.5, 0.6, 0.65]
                                               )

    def test_const_surface(self):
        for term in [0.5, 1, 2]:
            self.assertEqual(self.const_rate, self.const_surface.vol(term))

        for term in [0.5, 1, 2]:
            for strike in [0.5, 1, 1.5]:
                self.assertEqual(self.const_rate, self.const_surface.vol(strike, term))

    def test_term_vol_surface(self):
        terms = [0.25, 0.5, 0.75, 1, 1.5, 1.8, 2, 2.5]
        variances = [0.0625, 0.125, 0.2425, 0.36, 0.6025, 0.748, 0.845, 1.05625]
        for i in range(len(terms)):
            term = terms[i]
            step_vol = self.term_vol_surface.vol(tau=term)
            self.assertAlmostEqual(step_vol**2 * term, variances[i])
