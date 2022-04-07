import unittest
from datetime import datetime
from surface.const_surface import ConstantSurface


class TestSurface(unittest.TestCase):
    def setUp(self) -> None:
        valuation_date = datetime(2020, 1, 1)
        self.const_rate = 0.3
        self.const_surface = ConstantSurface(valuation_date=valuation_date,
                                             const_rate=self.const_rate)

    def test_const_surface(self):
        for term in [0.5, 1, 2]:
            self.assertEqual(self.const_rate, self.const_surface.vol(term))

        for term in [0.5, 1, 2]:
            for strike in [0.5, 1, 1.5]:
                self.assertEqual(self.const_rate, self.const_surface.vol(strike, term))
        