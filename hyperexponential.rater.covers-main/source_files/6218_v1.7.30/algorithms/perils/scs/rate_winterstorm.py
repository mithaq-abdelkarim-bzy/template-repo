import hx
import polars as pl
import pandas as pd
import numpy as np
from algorithms.rate_common_rating_functions import worth_lookup, spatial_key_modifier, iso_construction_modifier, num_floors_modifier, size_discount_modifier, base_rates



def winterstorm_rating_calcs(hxd, df):
    

    df = base_rates(hxd, df, "WTS")
    df = size_discount_modifier(hxd, df, "WTS")
    df = worth_lookup(hxd, df, "WTS")


    # calcualte overall modifier (excluding size discount)
    df = df.with_columns((pl.lit(1)).alias("wts_modifier"))

    # calculate overall modifers
    for coverage, size_dis in zip (["buildings", "contents", "bi"], ["buildings", "contents", "buildings"]):
        df = df.with_columns((pl.col(f"wts_base_rate_{coverage}") * pl.col("wts_modifier") * pl.col(f"wts_size_discount_{size_dis}_modifier")).alias(f"wts_{coverage}_modified"))

    # calcualte buildings, contents, and BI net el
    for coverage in ("buildings", "contents", "bi"):
        df = df.with_columns(
            pl.when(pl.col("loc_aop_covered") == "Yes")
            .then(pl.col(f"loc_tiv_{coverage}") * pl.col(f"wts_{coverage}_modified") * pl.col("wts_worth") )
            .otherwise(0)
            .alias(f"wts_{coverage}_market_share_el")
        )

    return df