from math import exp, log, sqrt
from scipy.special import ndtr


class BarrierOptionPricer:
    @staticmethod
    def calc_mu(b, vol):
        return (b - vol * vol / 2) / (vol * vol)

    @staticmethod
    def calc_lambda(r, b, vol):
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return sqrt(mu ** 2 + 2 * r / (vol ** 2))

    @staticmethod
    def calc_z(spot, barrier, r, b, vol, tau):
        lambda_ = BarrierOptionPricer.calc_lambda(r, b, vol)
        return log(barrier / spot) / (vol * sqrt(tau)) + lambda_ * vol * sqrt(tau)

    @staticmethod
    def calc_x1(spot, strike, b, vol, tau):
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return log(spot / strike) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_x2(spot, barrier, b, vol, tau):
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return log(spot / barrier) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_y1(spot, strike, barrier, b, vol, tau):
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return log(barrier ** 2 / (spot * strike)) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_y2(spot, barrier, b, vol, tau):
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return log(barrier / spot) / (vol * sqrt(tau)) + (1 + mu) * vol * sqrt(tau)

    @staticmethod
    def calc_a(spot, strike, r, q, vol, tau, phi):
        b = r - q
        x1 = BarrierOptionPricer.calc_x1(spot, strike, b, vol, tau)
        return phi * spot * exp((b - r) * tau) * ndtr(phi * x1) - \
               phi * strike * exp(-r * tau) * ndtr(phi * x1 - phi * vol * sqrt(tau))

    @staticmethod
    def calc_b(spot, strike, barrier, r, q, vol, tau, phi):
        b = r - q
        x2 = BarrierOptionPricer.calc_x2(spot, barrier, b, vol, tau)
        return phi * spot * exp((b - r) * tau) * ndtr(phi * x2) - \
               phi * strike * exp(-r * tau) * ndtr(phi * x2 - phi * vol * sqrt(tau))

    @staticmethod
    def calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita):
        b = r - q
        y1 = BarrierOptionPricer.calc_y1(spot, strike, barrier, b, vol, tau)
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return phi * spot * exp((b - r) * tau) * (barrier / spot) ** (2 * (1 + mu)) * ndtr(ita * y1) - \
               phi * strike * exp(-r * tau) * (barrier / spot) ** (2 * mu) * ndtr(ita * y1 - ita * vol * sqrt(tau))

    @staticmethod
    def calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita):
        b = r - q
        y2 = BarrierOptionPricer.calc_y2(spot, barrier, b, vol, tau)
        mu = BarrierOptionPricer.calc_mu(b, vol)
        return phi * spot * exp((b - r) * tau) * (barrier / spot) ** (2 * (1 + mu)) * ndtr(ita * y2) - \
               phi * strike * exp(-r * tau) * (barrier / spot) ** (2 * mu) * ndtr(ita * y2 - ita * vol * sqrt(tau))

    @staticmethod
    def calc_e(spot, barrier, r, q, vol, tau, rebate, ita):
        b = r - q
        mu = BarrierOptionPricer.calc_mu(b, vol)
        x2 = BarrierOptionPricer.calc_x2(spot, barrier, b, vol, tau)
        y2 = BarrierOptionPricer.calc_y2(spot, barrier, b, vol, tau)
        return rebate * exp(-r * tau) * (ndtr(ita * x2 - ita * vol * sqrt(tau)) -
                                         (barrier / spot) ** (2 * mu) * ndtr(ita * y2 - ita * vol * sqrt(tau)))

    @staticmethod
    def calc_f(spot, barrier, r, q, vol, tau, rebate, ita):
        b = r - q
        mu = BarrierOptionPricer.calc_mu(b, vol)
        lambda_ = BarrierOptionPricer.calc_lambda(r, b, vol)
        z = BarrierOptionPricer.calc_z(spot, barrier, r, b, vol, tau)
        return rebate * ((barrier / spot) ** (mu + lambda_) * ndtr(ita * z) +
                         (barrier / spot) ** (mu - lambda_) * ndtr(ita * z - 2 * ita * lambda_ * vol * sqrt(tau)) )

    @staticmethod
    def price_down_and_in_call_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = 1
        phi = 1
        e = BarrierOptionPricer.calc_e(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return c + e
        else:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - b + d + e

    @staticmethod
    def price_up_and_in_call_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = -1
        phi = 1
        e = BarrierOptionPricer.calc_e(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            return a + e
        else:
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return b - c + d + e

    @staticmethod
    def price_down_and_in_put_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = 1
        phi = -1
        e = BarrierOptionPricer.calc_e(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return b - c + d + e
        else:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            return a + e

    @staticmethod
    def price_up_and_in_put_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = -1
        phi = -1
        e = BarrierOptionPricer.calc_e(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - b + d + e
        else:
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return c + e

    @staticmethod
    def price_down_and_out_call_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = 1
        phi = 1
        f = BarrierOptionPricer.calc_f(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - c + f
        else:
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return b - d + f

    @staticmethod
    def price_up_and_out_call_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = -1
        phi = 1
        f = BarrierOptionPricer.calc_f(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            return f
        else:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - b + c - d + f

    @staticmethod
    def price_down_and_out_put_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = 1
        phi = -1
        f = BarrierOptionPricer.calc_f(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - b + c - d + f
        else:
            return f

    @staticmethod
    def price_up_and_out_put_option(spot, strike, barrier, r, q, vol, tau, rebate):
        ita = -1
        phi = -1
        f = BarrierOptionPricer.calc_f(spot, barrier, r, q, vol, tau, rebate, ita)
        if strike > barrier:
            b = BarrierOptionPricer.calc_b(spot, strike, barrier, r, q, vol, tau, phi)
            d = BarrierOptionPricer.calc_d(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return b - d + f
        else:
            a = BarrierOptionPricer.calc_a(spot, strike, r, q, vol, tau, phi)
            c = BarrierOptionPricer.calc_c(spot, strike, barrier, r, q, vol, tau, phi, ita)
            return a - c + f
