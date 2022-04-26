from market_data.market_data import MarketData


class MCEngine(object):
    def __init__(self,
                 market_data: MarketData,
                 tau: float,
                 step_size,
                 num_paths,
                 is_antithetic):
        self.market_data = market_data
        self.tau = tau
        self.step_size = step_size
        self.num_paths = num_paths
        self.is_antithetic = is_antithetic
        step_size = round(self.tau / self.step_size)
        initial_spot = market_data.spot


    @classmethod
    def __generate_path(cls):
        pass
