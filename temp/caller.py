import numpy as np
from temp.autocall_evaluate import autocall_mc_pricer, rng


class AutocallPricer:
    @staticmethod
    def autocall_pricer(spot, r, q, vol, tau, dt, ko_list, num_paths, ko_price, ki_price, coupon_rate,
                        natural_day_list):
        normal_dist = rng(num_paths, tau, dt)
        return autocall_mc_pricer(normal_dist, spot, r, q, vol, tau, dt, np.array(ko_list), num_paths, ko_price,
                                  ki_price, coupon_rate, np.array(natural_day_list))

    @staticmethod
    def autocall_delta(spot, r, q, vol, tau, dt, ko_list, num_paths, ko_price, ki_price, coupon_rate,
                       natural_day_list):
        spot_up = spot * 1.01
        spot_down = spot * 0.99
        pv_up = AutocallPricer.autocall_pricer(spot_up, r, q, vol, tau, dt, ko_list, num_paths, ko_price, ki_price,
                                               coupon_rate, natural_day_list)
        pv_down = AutocallPricer.autocall_pricer(spot_down, r, q, vol, tau, dt, ko_list, num_paths, ko_price, ki_price,
                                                 coupon_rate, natural_day_list)
        return (pv_up - pv_down) / spot * 0.02
