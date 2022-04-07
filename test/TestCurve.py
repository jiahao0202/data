from curve.const_curve import ConstCurve
from datetime import datetime
import math
import unittest


class TestCurve(unittest.TestCase):
    def setUp(self) -> None:
        valuation_date = datetime(2020, 1, 1)
        self.const_rate = 0.025
        self.const_curve = ConstCurve(valuation_date=valuation_date,
                                      rate=self.const_rate)

    def test_const_curve(self):
        terms = [0, 0.5, 1, 3]
        for term in terms:
            self.assertEqual(self.const_rate, self.const_curve.rate(tau=term))
        for term in terms:
            self.assertEqual(math.exp(-self.const_rate * term), self.const_curve.discount(term))