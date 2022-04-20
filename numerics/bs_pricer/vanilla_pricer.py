import numpy as np
from math import exp, log, sqrt
from scipy.stats import norm
from scipy.special import ndtr
from utils.product_util import OptionTypeEnum


class VanillaOptionPricer:
    @staticmethod
    def __d1(spot, strike, vol, r, q, tau):
        return (log(spot / strike) + (r - q + .5 * vol ** 2) * tau) / (sqrt(tau) * vol)
    
    @staticmethod
    def price(spot, strike, vol, r, q, tau, option_type) -> float:
        if vol == 0.:
            return np.nan
        if tau < 1. / 244.:
            return max(0, spot-strike) if option_type == OptionTypeEnum.Call else max(0, strike-spot)
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        d2 = d1 - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return spot * exp(-q * tau) * ndtr(d1) - strike * exp(-r * tau) * ndtr(d2)
        elif option_type == OptionTypeEnum.Put:
            return -spot * exp(-q * tau) * ndtr(-d1) + strike * exp(-r * tau) * ndtr(-d2)

    @staticmethod
    def delta(spot, strike, vol, r, q, tau, option_type) -> float:
        if vol == 0.:
            return np.nan
        if tau < 1. / 244.:
            return max(0, spot-strike) if option_type == OptionTypeEnum.Call else max(0, strike-spot)
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        if option_type == OptionTypeEnum.Call:
            return exp(-q * tau) * ndtr(d1)
        elif option_type == OptionTypeEnum.Put:
            return exp(-q * tau) * (ndtr(d1) - 1)

    @staticmethod
    def gamma(spot, strike, vol, r, q, tau, option_type) -> float:
        if tau < 1. / 244.:
            return 0.
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        return exp(-q * tau) * norm.pdf(d1)

    @staticmethod
    def theta(spot, strike, vol, r, q, tau, option_type) -> float:
        if tau < 1. / 244.:
            return 0.
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        d2 = d1 - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return -vol * spot * exp(-q * tau) * norm.pdf(d1) / (2 * sqrt(tau)) + \
                   q * spot * ndtr(d1) * exp(-q * tau) - r * strike * exp(-r * tau) * ndtr(d2)
        elif option_type == OptionTypeEnum.Put:
            return -vol * spot * exp(-q * tau) * norm.pdf(-d1) / (2 * sqrt(tau)) - \
                   q * spot * ndtr(-d1) * exp(-q * tau) + r * strike * exp(-r * tau) * ndtr(d2)

    @staticmethod
    def vega(spot, strike, vol, r, q, tau, option_type) -> float:
        if tau < 1. / 244.:
            return 0.
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        return spot * sqrt(tau) * exp(-q * tau) * norm.pdf(d1)

    @staticmethod
    def rho(spot, strike, vol, r, q, tau, option_type) -> float:
        if tau < 1. / 244.:
            return 0.
        d2 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau) - vol * sqrt(tau)
        if option_type == OptionTypeEnum.Call:
            return strike * tau * exp(-r * tau) * ndtr(d2)
        elif option_type == OptionTypeEnum.Put:
            return -strike * tau * exp(-r * tau) * ndtr(-d2)

    @staticmethod
    def phi(spot, strike, vol, r, q, tau, option_type) -> float:
        if tau < 1. / 244.:
            return 0.
        d1 = VanillaOptionPricer.__d1(spot, strike, vol, r, q, tau)
        if option_type == OptionTypeEnum.Call:
            return -tau * spot * exp(-q * tau) * ndtr(d1)
        elif option_type == OptionTypeEnum.Put:
            return tau * spot * exp(-q * tau) * ndtr(-d1)
