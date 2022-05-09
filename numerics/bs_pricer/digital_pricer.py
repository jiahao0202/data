from math import exp, sqrt, log
from scipy.special import ndtr
from scipy.stats import norm
from utils.product_util import OptionTypeEnum


class DigitalOptionPricer:
    @staticmethod
    def __d1(spot, strike, vol, r, q, tau):
        return (log(spot / strike) + (r - q + .5 * vol ** 2) * tau) / (sqrt(tau) * vol)

    @staticmethod
    def price(spot, strike, r, q, vol, tau, option_type: OptionTypeEnum):
        if tau <= 1./244.:
            return 1. if spot > strike else 0 if option_type == OptionTypeEnum.Call else 1. if spot < strike else 0
        d2 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau) - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return exp(-r * tau) * ndtr(d2)
        elif option_type == OptionTypeEnum.Put:
            return exp(-r * tau) * (1 - ndtr(d2))

    @staticmethod
    def delta(spot, strike, r, q, vol, tau, option_type: OptionTypeEnum):
        if tau <= 1./244.:
            return 1. if spot > strike else 0 if option_type == OptionTypeEnum.Call else 1. if spot < strike else 0
        d2 = DigitalOptionPricer.__d1(spot, strike, r, q, vol, tau) - vol * sqrt(tau)
        delta = exp(-r * tau) * norm.pdf(d2) / (vol * spot * sqrt(tau))
        return delta if option_type == OptionTypeEnum.Call else -delta

    @staticmethod
    def gamma(spot, strike, r, q, vol, tau, option_type):
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


if __name__ == "__main__":
    pv = DigitalOptionPricer.price(spot=90, strike=100, r=0.025, q=0,
                                   vol=0.2, tau=5./244., option_type=OptionTypeEnum.Call)
