import optparse

import numpy as np
import pandas as pd
import pickle
from autocall_calc import calc_step_vol
from datetime import datetime
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface
from numerics.solver import Solver
from temp.caller import AutocallPricer
from temp.meta_data import decode_pickle, MetaData
from temp.vanilla_option_data_processor import vol_schemes, vol_terms

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-v', dest='vol_scheme', type='string')
    (options, args) = parser.parse_args()
    vol_scheme = options.vol_scheme

    test_dict = decode_pickle("./temp/autocall_meta_data.pickle")
    coupon_dict = {}
    for key, value in test_dict.items():
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

        vols = frame['vols'].values[0]
        coupon_ = Solver.autocall_coupon_solver(spot=initial_price,
                                                initial_price=initial_price,
                                                exp_tau=exp_tau,
                                                r=0.025,
                                                q=0.,
                                                vol=vols,
                                                tau=exp_tau,
                                                ko_price=value['ko_price'],
                                                ki_price=value['ki_price'],
                                                ko_list=value['ko_list'],
                                                natural_day_list=value['nat_ko_list'],
                                                num_paths=100000,
                                                precision=1e-3
                                                )
        pv = AutocallPricer.autocall_pricer(spot=initial_price,
                                            initial_price=initial_price,
                                            r=0.025,
                                            q=0.,
                                            vol=vols,
                                            tau=exp_tau,
                                            dt=1./244.,
                                            exp_tau=exp_tau,
                                            ko_price=value['ko_price'],
                                            ki_price=value['ki_price'],
                                            ko_list=value['ko_list'],
                                            natural_day_list=value['nat_ko_list'],
                                            coupon_rate=coupon_,
                                            fixings=np.array([]),
                                            num_paths=100000
                                            )
        print("{} cpr: {}   pv:   {}".format(key, round(coupon_, 8), round(pv, 8)))
        coupon_dict[key] = {}
        coupon_dict[key]['cpr'] = coupon_
        coupon_dict[key]['pv'] = pv
    with open(f"./coupon_new/{vol_scheme}.pickle", 'wb') as f:
        data = pickle.dumps(coupon_dict)
        pickle.dump(data, f)
