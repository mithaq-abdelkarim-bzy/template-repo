import hx
import polars as pl
from algorithms.perils.scs.rate_tornado import tornado_rating_calcs
from algorithms.perils.scs.rate_hail import hail_rating_calcs
from algorithms.perils.scs.rate_winterstorm import winterstorm_rating_calcs


def scs_rating_calcs(hxd, df):
    df = tornado_rating_calcs(hxd, df)
    df = hail_rating_calcs(hxd, df)
    df = winterstorm_rating_calcs(hxd, df)


    return df






   