import os

import pandas as pd

from back_test.back_test_engine import BackTestEngine
from optparse import OptionParser
from temp.meta_data import MetaData
from temp.utils.sqlite_helper import SqliteHelper
from temp.vanilla_option_data_processor import process_individual_stock, vol_schemes


exp_schemes = {
    '1m': MetaData.exp_map_1mo,
    '3m': MetaData.exp_map_3mo,
    '6m': MetaData.exp_map_6mo,
    '12m': MetaData.exp_map_12mo
}


if __name__ == "__main__":
    notional = 1000000
    parser = OptionParser()
    parser.add_option('-t', dest='exp', type='string')
    (options, args) = parser.parse_args()
    exp = options.exp
    if exp not in os.listdir('./back_test_result'):
        os.makedirs(f'./back_test_result/{exp}')
    exp_term = exp_schemes[exp]
    for start, end in exp_term.items():
        print('---------------------> Backtest date: {}'.format(start))
        if start not in os.listdir(f'./back_test_result/{exp}'):
            os.makedirs(f'./back_test_result/{exp}/{start}')
        for vol_scheme in vol_schemes.keys():
            result_frame = dict()
            print("---------------> Backtest Vol Scheme: {}".format(vol_scheme))
            if vol_scheme not in os.listdir(f'./back_test_result/{exp}/{start}'):
                os.makedirs(f'./back_test_result/{exp}/{start}/{vol_scheme}')
            for stock in MetaData.stocks:
                frame = SqliteHelper.load_data_from_db(stock, '2011-02-01', '2011-03-03')
                frame = process_individual_stock(frame, vol_scheme)
                result = BackTestEngine.run(frame)
                result_frame[stock] = float(result['cash'].values[-1])
            result_frame = pd.DataFrame([result_frame]).T / notional
            # print(result_frame)
            result_frame.to_csv(f'./back_test_result/{exp}/{start}/{vol_scheme}/result.csv')
