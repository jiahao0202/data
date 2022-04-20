import optparse
import os

import pandas as pd
import numpy as np
from market_data.surface.base_surface import BaseVolSurface
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface
from temp.caller import AutocallPricer
from temp.meta_data import *
from temp.vanilla_option_data_processor import vol_schemes, vol_terms


def calc_step_vol(tau, vol_surface: BaseVolSurface):
    dt = 1. / 244.
    step_size = round(tau / dt)
    vols = np.zeros(step_size)
    for i in range(step_size):
        vols[i] = vol_surface.vol(tau - i * dt)
    return vols


if __name__ == "__main__":
    if '000905_calc' not in os.listdir("./"):
        os.makedirs("./000905_calc/")
    parser = optparse.OptionParser()
    parser.add_option('-v', dest='vol_scheme', type='string')
    (options, args) = parser.parse_args()
    vol_scheme = options.vol_scheme

    if vol_scheme not in os.listdir("./000905_calc/"):
        os.makedirs(f'./000905_calc/{vol_scheme}')

    test_dict = decode_pickle("./temp/autocall_meta_data.pickle")
    with open(f"./coupon_new/{vol_scheme}.pickle", 'rb') as f:
        data = pickle.load(f)
        coupon_dict = pickle.loads(data)
    for key, value in test_dict.items():
        print("{}:   @{}".format(key, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        frame = pd.read_pickle(f'./000905/{key}.pickle')
        if vol_scheme.startswith('flat'):
            frame['vol_surface'] = frame.apply(lambda x: ConstVolSurface(x.name, x[vol_schemes[vol_scheme]]), axis=1)
        else:
            frame['vol_surface'] = frame.apply(lambda x: TermVolSurface(x.name,
                                                                        [x / 244 for x in vol_terms[vol_scheme]],
                                                                        x[vol_schemes[vol_scheme]]), axis=1)
        exp_dt = datetime.strptime(value['expiration_date'], "%Y-%m-%d")
        frame['tau'] = frame.apply(lambda x: MetaData.year_fraction_trading(x.name, exp_dt), axis=1)
        exp_tau = frame['tau'].values[0]
        initial_price = frame['close'].values[0]
        frame['vols'] = frame.apply(lambda x: calc_step_vol(x['tau'], x['vol_surface']), axis=1)
        coupon_rate = 0.5272264406085014 #coupon_dict[key]
        frame['fixings'] = frame.apply(lambda x: list(frame[frame.index < x.name]['close'].values), axis=1)

        frame['pv'] = frame.apply(lambda x:
                                  AutocallPricer.autocall_pricer(spot=x['close'],
                                                                 initial_price=initial_price,
                                                                 r=0.025,
                                                                 q=0.,
                                                                 vol=x['vols'],
                                                                 tau=x['tau'],
                                                                 exp_tau=exp_tau,
                                                                 dt=1. / 244.,
                                                                 ko_list=value['ko_list'],
                                                                 num_paths=80000,
                                                                 ko_price=value['ko_price'],
                                                                 ki_price=value['ki_price'],
                                                                 coupon_rate=coupon_rate,
                                                                 natural_day_list=value['nat_ko_list'],
                                                                 fixings=x['fixings']
                                                                 ),
                                  axis=1)

        frame['delta'] = frame.apply(lambda x:
                                     AutocallPricer.autocall_delta(spot=x['close'],
                                                                   initial_price=initial_price,
                                                                   r=0.025,
                                                                   q=0.,
                                                                   vol=x['vols'],
                                                                   tau=x['tau'],
                                                                   exp_tau=exp_tau,
                                                                   dt=1. / 244.,
                                                                   ko_list=value['ko_list'],
                                                                   num_paths=80000,
                                                                   ko_price=value['ko_price'],
                                                                   ki_price=value['ki_price'],
                                                                   coupon_rate=coupon_rate,
                                                                   natural_day_list=value['nat_ko_list'],
                                                                   fixings=x['fixings']
                                                                   ),
                                     axis=1)
        frame.to_csv(f"./000905_calc/{vol_scheme}/{key}.csv")
