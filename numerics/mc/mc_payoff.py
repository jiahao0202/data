from numba import jit
from product.options.vanilla_option import VanillaOption


class MCPayoffs:
    @staticmethod
    def vanilla_option_payoff(instrument: VanillaOption, paths):
        pass

    @staticmethod
    @jit(nopython=True)
    def digital_option_payoff(paths):
        pass
