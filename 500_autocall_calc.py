import optparse
import pandas as pd
import numpy as np
from market_data.surface.base_surface import BaseVolSurface
from market_data.surface.const_vol_surface import ConstVolSurface
from market_data.surface.term_vol_surface import TermVolSurface
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
    vol_scheme = 'flat_3m'
    test_dict = decode_pickle("./temp/autocall_meta_data.pickle")
    for key, value in test_dict.items():
        print(key)
        frame = pd.read_pickle(f'./000905/{key}.pickle')
        if vol_scheme.startswith('flat'):
            frame['vol_surface'] = frame.apply(lambda x: ConstVolSurface(x.name, vol_schemes[vol_scheme]), axis=1)
        else:
            frame['vol_surface'] = frame.apply(lambda x: TermVolSurface(x.name,
                                                                        [x / 244 for x in vol_terms[vol_scheme]],
                                                                        x[vol_schemes[vol_scheme]]), axis=1)
        exp_dt = datetime.strptime(value['expiration_date'], "%Y-%m-%d")
        frame['tau'] = frame.apply(lambda x: MetaData.year_fraction_trading(x.name, exp_dt), axis=1)
        frame['vols'] = frame.apply(lambda x: calc_step_vol(x['tau'], x['vol_surface']), axis=1)

