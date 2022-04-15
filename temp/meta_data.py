import pickle
from datetime import datetime
from patterns.singleton import Singleton


def decode_pickle(file):
    with open(file, 'rb') as f:
        res = pickle.load(f)
    res = pickle.loads(res)
    return res


class MetaData(metaclass=Singleton):
<<<<<<< HEAD
    trading_cal = decode_pickle("./trade_cal.pickle")
    exp_map_1mo = decode_pickle('./exp_1m.pickle')
    exp_map_3mo = decode_pickle('./exp_3m.pickle')
    exp_map_6mo = decode_pickle('./exp_6m.pickle')
    exp_map_12mo = decode_pickle('./exp_12m.pickle')
=======
    trading_cal = decode_pickle("exp_data/trade_cal.pickle")
    exp_map_1mo = decode_pickle('exp_data/exp_1m.pickle')
    exp_map_3mo = decode_pickle('exp_data/exp_3m.pickle')
    exp_map_6mo = decode_pickle('exp_data/exp_6m.pickle')
    exp_map_12mo = decode_pickle('exp_data/exp_12m.pickle')
>>>>>>> c10d40f (Meta Data update)

    @staticmethod
    def year_fraction_trading(valuation_date: datetime, expiration_date: datetime):
        valuation_date = valuation_date.strftime("%Y-%m-%d")
        expiration_date = expiration_date.strftime("%Y-%m-%d")
        date_diff = MetaData.trading_cal.index(expiration_date) - MetaData.trading_cal.index(valuation_date)
        return date_diff / 244.

    @staticmethod
    def year_fraction(valuation_date: datetime, expiration_date: datetime):
        date_diff = (expiration_date.timestamp() - valuation_date.timestamp()) / (3600 * 24)
        return date_diff / 365.

    @staticmethod
    def get_expiration_date_1mo(valuation_date) -> datetime:
        return datetime.strptime(MetaData.exp_map_1mo[valuation_date], "%Y-%m-%d")

    @staticmethod
    def get_expiration_date_3mo(valuation_date) -> datetime:
        return datetime.strptime(MetaData.exp_map_3mo[valuation_date], "%Y-%m-%d")

    @staticmethod
    def get_expiration_date_6mo(valuation_date) -> datetime:
        return datetime.strptime(MetaData.exp_map_6mo[valuation_date], "%Y-%m-%d")

    @staticmethod
    def get_expiration_date_12mo(valuation_date) -> datetime:
        return datetime.strptime(MetaData.exp_map_12mo[valuation_date], "%Y-%m-%d")
