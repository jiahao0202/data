from math import exp, log, sqrt
from scipy.special import ndtr
from scipy.stats import norm
from utils.product_util import OptionTypeEnum


class BarrierOptionPricer:
    @staticmethod
    def calc_mu(q, vol):
        return (q - vol ** 2 / 2) / (vol ** 2)

    @staticmethod
    def calc_lambda(r, q, vol):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return sqrt(mu ** 2 + 2 * r / (vol ** 2))

    @staticmethod
    def calc_z(spot, barrier, r, q, vol, tau):
        lambda_ = BarrierOptionPricer.calc_lambda(r, q, vol)
        return log(barrier / spot) / (vol * sqrt(tau)) + lambda_ * vol * sqrt(tau)

    @staticmethod
    def calc_x1(spot, strike, q, vol, tau):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return log(spot / strike) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_x2(spot, barrier, q, vol, tau):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return log(spot / barrier) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_y1(spot, strike, barrier, q, vol, tau):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return log(barrier**2 / (spot*strike)) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_y2(spot, barrier, q, vol, tau):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return log(barrier / spot) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_a(spot, strike, r, q, vol, tau, phi):
        x1 = BarrierOptionPricer.calc_x1(spot, strike, q, vol, tau)
        return phi * spot * exp((q-r) * tau) * ndtr(phi * x1) - \
               phi * strike * exp(-r * tau) * ndtr(phi * x1 - phi * vol * sqrt(tau))

    @staticmethod
    def calc_b(spot, strike, barrier, r, q, vol, tau, phi):
        x2 = BarrierOptionPricer.calc_x2(spot, barrier, q, vol, tau)
        return phi * spot * exp((q - r) * tau) * ndtr(phi * x2) - \
               phi * strike * exp(-r * tau) * ndtr(phi * x2 - phi * vol * sqrt(tau))

    @staticmethod
    def calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita):
        y1 = BarrierOptionPricer.calc_y1(spot, strike, barrier, q, vol, tau)
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return phi * spot * exp((q-r) * tau) * (barrier / spot) ** (2 * (1 + mu)) * ndtr(ita * y1) - \
               phi * strike * exp(-r * tau) * (barrier / spot) ** (2 * mu) * ndtr(ita * y1 - ita * vol * sqrt(tau))

    @staticmethod
    def calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita):
        y2 = BarrierOptionPricer.calc_y2(spot, barrier, q, vol, tau)
        mu = BarrierOptionPricer.calc_mu(q, vol)
        return phi * spot * exp((q - r) * tau) * (barrier / spot) ** (2 * (1 + mu)) * ndtr(ita * y2) - \
               phi * strike * exp(-r * tau) * (barrier / spot) ** (2 * mu) * ndtr(ita * y2 - ita * vol * sqrt(tau))

    @staticmethod
    def calc_e(spot, barrier, r, q, vol, tau, rebate, ita):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        x2 = BarrierOptionPricer.calc_x2(spot, barrier, q, vol, tau)
        y2 = BarrierOptionPricer.calc_y2(spot, barrier, q, vol, tau)
        return rebate * exp(-r * tau) * (ndtr(ita * x2 - ita * vol * sqrt(tau)) -
                                         (barrier / spot) ** (2 * mu) * ndtr(ita * y2 - ita * vol * sqrt(tau)))

    @staticmethod
    def calc_f(spot, barrier, r, q, vol, tau, rebate, ita):
        mu = BarrierOptionPricer.calc_mu(q, vol)
        lambda_ = BarrierOptionPricer.calc_lambda(r, q, vol)
        z = BarrierOptionPricer.calc_z(spot, barrier, r, q, vol, tau)
        return rebate * ((barrier / spot) ** (mu + lambda_) * ndtr(ita * z) +
                         (barrier / spot) ** (mu - lambda_) * ndtr(ita * z - 2 * ita * lambda_ * vol * sqrt(tau)))

    @staticmethod
    def price_down_and_in_option(spot, strike, barrier, r, q, vol, tau, rabte):
        ita = 1
        phi = 1
        return 0.
