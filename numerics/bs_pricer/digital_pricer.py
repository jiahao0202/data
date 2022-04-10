from math import exp, sqrt
from scipy.special import ndtr
from scipy.stats import norm
from utils.product_util import OptionTypeEnum


class DigitalOptionPricer:
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

    def price(self):
        if self.option_type == OptionTypeEnum.Call:
            return exp(-self.r * self.tau) * ndtr(self.d2)
        elif self.option_type == OptionTypeEnum.Put:
            return exp(-self.r * self.tau) * (1 - ndtr(self.d2))

    def delta(self):
        delta = exp(-self.r * self.tau) * norm.pdf(self.d2) / (self.vol * self.spot * sqrt(self.tau))
        if self.option_type == OptionTypeEnum.Call:
            return delta
        elif self.option_type == OptionTypeEnum.Put:
            return -1 * delta

    def gamma(self):
        gamma = exp(-self.r * self.tau) * self.d1 * norm.pdf(self.d2) / (self.vol**2 * self.spot**2 * sqrt(self.tau))
        if self.option_type == OptionTypeEnum.Call:
            return -gamma
        elif self.option_type == OptionTypeEnum.Put:
            return gamma

    def theta(self):
        value_decay = exp(-self.r * self.tau) * norm.pdf(self.d2) * \
                      (.5 * self.d1 / self.tau - (self.r - self.q) / self.vol * sqrt(self.tau))
        return self.r * self.price() - value_decay

    def vega(self):
        return -exp(-self.r * self.tau) * norm.pdf(self.d2) * (sqrt(self.tau) + self.d2 / self.vol)
