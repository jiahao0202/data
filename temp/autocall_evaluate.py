import numpy as np
from numba import jit


def rng(num_paths, tau, dt, fixings):
    # np.random.seed(1234)
    step_size = round(tau / dt)
    paths = np.random.normal(size=(num_paths, step_size))
    if len(fixings) != 0:
        fixings = np.repeat([fixings], num_paths, axis=0)
        paths = np.hstack([fixings, paths])
    return paths


@jit(nopython=True)
def autocall_mc_pricer(normal_dist, spot, initial_price, r, q, vol, tau, exp_tau, dt, ko_list, num_paths,
                       ko_price, ki_price, coupon_rate, natural_day_list, notional=1000000):
    step_size = round(exp_tau / dt)
    z_size = round(tau / dt)
    diff_size = step_size - z_size
    paths = np.zeros((num_paths, step_size + 1))
    for i in range(diff_size):
        paths[:, i] = normal_dist[:, i]
    paths[:, diff_size] = spot
    for i in range(diff_size + 1, step_size + 1):
        paths[:, i] = paths[:, i - 1] * np.exp((r - q - .5 * vol[i - diff_size - 1] ** 2) *
                                               dt + vol[i - diff_size - 1] * np.sqrt(dt) * normal_dist[:, i - 1])
    payoffs = np.zeros(num_paths)
    flag_ko = np.zeros(num_paths)
    flag_ki = np.zeros(num_paths)

    for i in range(num_paths):
        for j in range(len(ko_list)):
            if paths[i, ko_list[j]] >= ko_price:
                nat_day = natural_day_list[j]
                payoffs[i] = (notional * coupon_rate * nat_day / 365) * np.exp(-r * nat_day / 365)
                flag_ko[i] = 1
                break

    for i in range(num_paths):
        if flag_ko[i] == 0:
            for j in range(1, step_size + 1):
                if paths[i, j] < ki_price:
                    payoffs[i] = notional * np.minimum(paths[i, -1] / initial_price - 1, 0.) * \
                                 np.exp(-r * natural_day_list[-1] / 365)
                    flag_ki[i] = 1
                    break
    payoffs = np.where(flag_ko + flag_ki == 0,
                       notional * coupon_rate * np.exp(-r * natural_day_list[-1] / 365), payoffs)
    return np.mean(payoffs) / notional
