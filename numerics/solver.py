import numpy as np
from numerics.bs_pricer.vanilla_pricer import VanillaOptionPricer
from scipy.optimize import bisect
from temp.autocall_evaluate import autocall_mc_pricer, rng
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
            solved_vol = bisect(func, lower_bdd, upper_bdd, xtol=precision, maxiter=max_iter)
            return solved_vol

    @staticmethod
    def autocall_coupon_solver(spot,
                               r,
                               q,
                               vol,
                               tau,
                               ko_price,
                               ki_price,
                               ko_list,
                               natural_day_list,
                               initial_price,
                               exp_tau,
                               num_paths=100000,
                               dt=1. / 244.,
                               precision=1e-6,
                               max_iter=100
                               ):
        lower_bdd = 0.
        upper_bdd = 1.

        def func(coupon_rate_to_solve):
            normal_dist_ = rng(num_paths, tau, dt, np.array([]))
            return autocall_mc_pricer(normal_dist=normal_dist_,
                                                initial_price=initial_price,
                                                  spot=spot,
                                                  r=r,
                                                  q=q,
                                                  vol=vol,
                                                  tau=tau,
                                                  exp_tau=exp_tau,
                                                  dt=1./244.,
                                                  ko_list=np.array(ko_list),
                                                  num_paths=num_paths,
                                                  ko_price=ko_price,
                                                  ki_price=ki_price,
                                                  coupon_rate=coupon_rate_to_solve,
                                                  natural_day_list=np.array(natural_day_list)
                                      )

        solved_coupon = bisect(func, lower_bdd, upper_bdd, xtol=precision, maxiter=max_iter)
        return solved_coupon
