import pandas as pd
from market_data.surface.term_vol_surface import TermVolSurface
from temp.meta_data import MetaData

vol_schemes = {
    'flat_3m': '3m',
    'flat_6m': '6m',
    'flat_12m': '12m',
    'term_vol_3': ['3m', '6m', '12m'],
    'term_vol_12': ['1m', '2m', '3m', '4m', '5m', '6m', '7m', '8m', '9m', '10m', '11m', '12m']
}


vol_terms = {
    'flat_3m': 63,
    'flat_6m': 126,
    'flat_12m': 252,
    'term_vol_3': [63, 126, 252],
    'term_vol_12': [21, 42, 63, 84, 105, 126, 147, 168, 189, 210, 231, 252]
}


def process_individual_stock(stock: pd.DataFrame, vol_scheme: str):
    stock['r'] = 0.025
    stock['q'] = 0.
    if stock.empty:
        return pd.DataFrame()
    expiration_date = max(stock.index)
    stock['tau'] = stock.apply(lambda x: MetaData.year_fraction_trading(x.name, expiration_date), axis=1)
    if vol_scheme.startswith("flat"):
        stock['vol'] = stock[vol_schemes[vol_scheme]]
    else:
        terms = [x / 252 for x in vol_terms[vol_scheme]]
        stock['vol_surface'] = stock.apply(lambda x:
                                           TermVolSurface(valuation_date=x.name,
                                                          terms=terms,
                                                          term_vols=list(x.loc[vol_schemes[vol_scheme]])),
                                           axis=1)
        stock['vol'] = stock.apply(lambda x: x['vol_surface'].vol(tau=x['tau']), axis=1)
    return stock[['close', 'tau', 'r', 'q', 'vol']]
