import numpy as np
from numba import jit


def rng(num_paths, tau, dt):
    np.random.seed(1234)
    step_size = round(tau / dt)
    return np.random.normal(size=(num_paths, step_size))


@jit(nopython=True)
def mc_pricer(normal_dist, spot, r, q, vol, tau, dt, ko_list, num_paths, ko_price, ki_price, coupon_rate,
              natural_day_list, notional):
    step_size = round(tau / dt)
    paths = np.zeros((num_paths, step_size + 1))
    paths[:, 0] = spot
    for i in range(1, step_size + 1):
        paths[:, i] = paths[:, i - 1] * np.exp((r - q - .5 * vol ** 2) * dt + vol * np.sqrt(dt) * normal_dist[:, i - 1])
    payoffs = np.zeros(num_paths)
    flag_ko = np.zeros(num_paths)
    flag_ki = np.zeros(num_paths)

    for i in range(num_paths):
        for j in range(len(ko_list)):
            if paths[i, ko_list[j]] >= ko_price:
                nat_day = natural_day_list[j]
                payoffs[i] = (notional * coupon_rate * nat_day / 244) * np.exp(-r * nat_day / 244)
                flag_ko[i] = 1
                break

    for i in range(num_paths):
        if flag_ko[i] == 0:
            if np.min(paths[i]) < ki_price:
                payoffs[i] = notional * np.minimum(paths[i, -1] / paths[i, 0] - 1, 0) * \
                             np.exp(-r * natural_day_list[-1])
                flag_ki[i] = 1
    payoffs = np.where(flag_ko + flag_ki == 0, notional * coupon_rate * np.exp(-r * natural_day_list[-1]), payoffs)
    return np.mean(payoffs) / notional
