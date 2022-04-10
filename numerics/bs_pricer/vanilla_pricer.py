from math import exp, sqrt
from scipy.stats import norm
from scipy.special import ndtr
from utils.product_util import OptionTypeEnum


class VanillaOptionPricer:
    def __init__(self, spot, strike, vol, r, q, tau, option_type: OptionTypeEnum):
        self.spot = spot
        self.strike = strike
        self.vol = vol
        self.r = r
        self.q = q
        self.tau = tau
        self.option_type = option_type
        self.d1 = self.__d1()
        self.d2 = self.d1 - self.vol * sqrt(tau)

    def __d1(self):
        return (self.spot / self.strike + (self.r - self.q + .5 * self.vol ** 2) * self.tau) / \
               (self.vol * sqrt(self.tau))

    def price(self) -> float:
        if self.option_type == OptionTypeEnum.Call:
            return self.spot * exp(-self.q * self.tau) * ndtr(self.d1) - \
                self.strike * exp(-self.r * self.tau) * ndtr(self.d2)
        elif self.option_type == OptionTypeEnum.Put:
            return -self.spot * exp(-self.q * self.tau) * ndtr(-self.d1) + \
                self.strike * exp(-self.r * self.tau) * ndtr(-self.d2)

    def delta(self) -> float:
        if self.option_type == OptionTypeEnum.Call:
            return exp(-self.q * self.tau) * ndtr(self.d1)
        elif self.option_type == OptionTypeEnum.Put:
            return exp(-self.q * self.tau) * (ndtr(self.d1) - 1)

    def gamma(self) -> float:
        return exp(-self.q * self.tau) * norm.pdf(self.d1)

    def theta(self) -> float:
        if self.option_type == OptionTypeEnum.Call:
            return -self.vol * self.spot * exp(-self.q * self.tau) * norm.pdf(self.d1) / (2 * sqrt(self.tau)) + \
                   self.q * self.spot * ndtr(self.d1) * exp(-self.q * self.tau) - \
                   self.r * self.strike * exp(-self.r * self.tau) * ndtr(self.d2)
        elif self.option_type == OptionTypeEnum.Put:
            return -self.vol * self.spot * exp(-self.q * self.tau) * norm.pdf(-self.d1) / (2 * sqrt(self.tau)) - \
                   self.q * self.spot * ndtr(-self.d1) * exp(-self.q * self.tau) + \
                   self.r * self.strike * exp(-self.r * self.tau) * ndtr(self.d2)

    def vega(self) -> float:
        return self.spot * sqrt(self.tau) * exp(-self.q * self.tau) * norm.pdf(self.d1)

    def rho(self) -> float:
        if self.option_type == OptionTypeEnum.Call:
            return self.strike * self.tau * exp(-self.r * self.tau) * ndtr(self.d2)
        elif self.option_type == OptionTypeEnum.Put:
            return -self.strike * self.tau * exp(-self.r * self.tau) * ndtr(-self.d2)

    def phi(self) -> float:
        if self.option_type == OptionTypeEnum.Call:
            return -self.tau * self.spot * exp(-self.q * self.tau) * ndtr(self.d1)
        elif self.option_type == OptionTypeEnum.Put:
            return self.tau * self.spot * exp(-self.q * self.tau) * ndtr(-self.d1)
