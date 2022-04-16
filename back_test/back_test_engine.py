import pandas as pd
from numerics.bs_pricer.vanilla_pricer import VanillaOptionPricer
from temp.meta_data import MetaData
from utils.product_util import OptionTypeEnum


class BackTestEngine:
    @staticmethod
    def run(frame: pd.DataFrame):
        """

        :param frame: dataframe return from temp.vanilla_option_data_processor
        :return: $PV and $Delta
        """
        notional = 1000000
        strike = frame['close'].values[0]
        initial_price = strike
        frame['pv'] = frame.apply(lambda x:
                                  VanillaOptionPricer.price(
                                      spot=x['close'],
                                      strike=strike,
                                      r=x['r'],
                                      q=x['q'],
                                      tau=x['tau'],
                                      vol=x['vol'],
                                      option_type=OptionTypeEnum.Call
                                  ) / initial_price * notional, axis=1)

        frame['qty'] = frame.apply(lambda x:
                                   VanillaOptionPricer.delta(
                                       spot=x['close'],
                                       strike=strike,
                                       r=x['r'],
                                       q=x['q'],
                                       tau=x['tau'],
                                       vol=x['vol'],
                                       option_type=OptionTypeEnum.Call
                                   ) * notional / x['close'], axis=1)
        frame['cash'] = 0.
        for i in range(len(frame.index)):
            today = frame.index[i]
            if i == 0:
                frame.loc[today, 'cash'] = frame.loc[today, 'pv'] - frame.loc[today, 'qty'] * frame.loc[today, 'close']
            else:
                yesterday = frame.index[i - 1]
                dt = MetaData.year_fraction(yesterday, today)
                if i < len(frame.index) - 1:
                    frame.loc[today, 'cash'] = \
                        frame.loc[yesterday, 'cash'] * (1 + dt * frame.loc[today, 'r']) - \
                        (frame.loc[today, 'qty'] - frame.loc[yesterday, 'qty']) * frame.loc[today, 'close']
                else:
                    frame.loc[today, 'cash'] = \
                        frame.loc[yesterday, 'cash'] * (1 + dt * frame.loc[today, 'r']) + \
                        frame.loc[yesterday, 'qty'] * frame.loc[today, 'close'] - frame.loc[today, 'pv']
        return frame
