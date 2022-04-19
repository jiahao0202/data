import numpy as np
from temp.autocall_evaluate import autocall_mc_pricer, rng


class AutocallPricer:
    @staticmethod
    def autocall_pricer(spot, initial_price, r, q, vol, tau, exp_tau, dt, ko_list, num_paths, ko_price, ki_price,
                        coupon_rate, natural_day_list, fixings):
        normal_dist = rng(num_paths, tau, dt, np.array(fixings))
        return autocall_mc_pricer(normal_dist, spot, initial_price, r, q, vol, tau, exp_tau, dt, np.array(ko_list),
                                  num_paths, ko_price, ki_price, coupon_rate, np.array(natural_day_list))

    @staticmethod
    def autocall_delta(spot, initial_price, r, q, vol, tau, exp_tau, dt, ko_list, num_paths, ko_price, ki_price,
                       coupon_rate, natural_day_list, fixings):
        spot_up = spot * 1.01
        spot_down = spot * 0.99
        pv_up = AutocallPricer.autocall_pricer(spot_up, initial_price, r, q, vol, tau, exp_tau, dt, ko_list, num_paths,
                                               ko_price, ki_price, coupon_rate, natural_day_list, fixings)
        pv_down = AutocallPricer.autocall_pricer(spot_down, initial_price, r, q, vol, tau, exp_tau, dt, ko_list,
                                                 num_paths, ko_price, ki_price, coupon_rate, natural_day_list, fixings)
        return (pv_up - pv_down) / (spot * 0.02)
