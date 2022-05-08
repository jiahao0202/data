from math import exp, sqrt
from scipy.special import ndtr
from scipy.stats import norm
from utils.product_util import OptionTypeEnum


class DigitalOptionPricer:
    @staticmethod
    def __d1(spot, strike, r, q, vol, tau):
        return (spot / strike + (r - q + .5 * vol ** 2) * tau) / \
               (vol * sqrt(tau))

    @staticmethod
    def price(spot, strike, r, q, vol, tau, option_type: OptionTypeEnum):
        d2 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau) - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return exp(-r * tau) * ndtr(d2)
        elif option_type == OptionTypeEnum.Put:
            return exp(-r * tau) * (1 - ndtr(d2))

    @staticmethod
    def delta(spot, strike, r, q, vol, tau, option_type: OptionTypeEnum):
        d2 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau) - vol * sqrt(tau)
        delta = exp(-r * tau) * norm.pdf(d2) / (vol * spot * sqrt(tau))
        return delta if option_type == OptionTypeEnum.Call else -delta

    @staticmethod
    def gamma(spot ,strike, r, q, vol, tau, option_type):
        d1 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau)
        d2 = d1 - vol * sqrt(tau)
        gamma = exp(-r * tau) * d1 * norm.pdf(d2) / ((spot * vol) ** 2 * tau)
        return -gamma if option_type == OptionTypeEnum.Call else gamma

    @staticmethod
    def theta(spot, strike, r, q, vol ,tau, option_type):
        d1 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau)
        d2 = d1 - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return r * exp(-r * tau) * ndtr(d2) + \
                   exp(-r * tau) * norm.pdf(d2) * (d1 / (2 * tau) - (r - q) / (vol * sqrt(tau)))
        elif option_type == OptionTypeEnum.Put:
            return r * exp(-r * tau) * (1 - ndtr(d2)) + \
                   exp(-r * tau) * norm.pdf(d2) * (d1 / (2 * tau) - (r - q) / (vol * sqrt(tau)))

    @staticmethod
    def vega(spot, strike, r, q, vol, tau, option_type: OptionTypeEnum):
        d1 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau)
        d2 = d1 - vol * sqrt(tau)
        vega = exp(-r * tau) * norm.pdf(d2) * d1 / vol
        return -vega if option_type == OptionTypeEnum.Call else vega

