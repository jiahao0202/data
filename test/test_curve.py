from market_data.curve.const_curve import ConstCurve
from market_data.curve.term_curve import TermCurve
from datetime import datetime
import math
import unittest


class TestCurve(unittest.TestCase):
    def setUp(self) -> None:
        valuation_date = datetime(2020, 1, 1)
        self.const_rate = 0.025
        self.const_curve = ConstCurve(valuation_date=valuation_date,
                                      const_rate=self.const_rate)
        self.term_curve = TermCurve(valuation_date=valuation_date,
                                    terms=[1, 2, 3],
                                    rates=[0.02, 0.025, 0.028])
        self.bump_size = 0.01
        self.const_curve_bump = self.const_curve.bump(self.bump_size, False)
        self.term_curve_bump = self.term_curve.bump(self.bump_size, True)

    def test_const_curve(self):
        terms = [0, 0.5, 1, 3]

        # Test const curve
        for term in terms:
            self.assertEqual(self.const_rate, self.const_curve.rate(tau=term))
        for term in terms:
            self.assertEqual(math.exp(-self.const_rate * term), self.const_curve.discount(tau=term))

        # Test const vol surface bump
        for term in terms:
            self.assertAlmostEqual(self.const_rate + self.bump_size, self.const_curve_bump.rate(tau=term))

    def test_term_curve(self):
        rates = [0.02, 0.02, 0.021, 0.025, 0.0274, 0.028, 0.028]
        terms = [0.5, 1, 1.2, 2, 2.8, 3, 3.5]
        for i in range(len(terms)):
            term = terms[i]
            self.assertEqual(self.term_curve.rate(tau=term), rates[i])
        for i in range(len(terms)):
            self.assertEqual(math.exp(-rates[i] * terms[i]), self.term_curve.discount(tau=terms[i]))

        # Test term vol surface bump
        for i in range(len(terms)):
            term = terms[i]
            self.assertAlmostEqual(self.term_curve_bump.rate(tau=term), rates[i] * (1 + self.bump_size))
