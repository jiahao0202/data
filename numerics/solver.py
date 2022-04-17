import numpy as np
from numerics.bs_pricer.vanilla_pricer import VanillaOptionPricer
from scipy.optimize import brentq
from utils.product_util import OptionTypeEnum


class Solver:
    @staticmethod
    def implied_vol_solver(mkt_price,
                           spot,
                           strike,
                           r,
                           q,
                           tau,
                           option_type:
                           OptionTypeEnum,
                           precision=1e-6,
                           max_iter=100):
        lower_bdd = 1e-4
        upper_bdd = 1000

        def func(vol_):
            return VanillaOptionPricer.price(spot, strike, vol_, r, q, tau, option_type) - mkt_price

        if func(lower_bdd) * func(upper_bdd) > 0:
            return np.nan

        else:
            solved_vol = brentq(func, lower_bdd, upper_bdd, xtol=precision, maxiter=max_iter)
            return solved_vol
