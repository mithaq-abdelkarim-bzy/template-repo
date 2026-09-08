import hx
import polars as pl
import pandas as pd
import numpy as np
from algorithms.rate_common_rating_functions import worth_lookup, base_rates, spatial_key_modifier, iso_construction_modifier, num_floors_modifier, size_discount_modifier



def fl_rating_calcs(hxd, df):
    

    df = base_rates(hxd, df, "FL")
    df = spatial_key_modifier(hxd, df, "FL")
    df = iso_construction_modifier(hxd, df, "FL")
    df = num_floors_modifier(hxd, df, "FL")
    df = size_discount_modifier(hxd, df, "FL")
    df = worth_lookup(hxd, df, "FL")


    # calcualte overall modifier (excluding size discount)
    df = df.with_columns(
        (pl.col("fl_spatial_key_modifier") * pl.col("fl_construction_modifier") * pl.col("fl_num_floors_modifier")).alias("fl_modifier")
    )

    
    # calculate overall modifers
    for coverage, size_dis in zip (["buildings", "contents", "bi"], ["buildings", "contents", "buildings"]):
        df = df.with_columns((pl.col(f"fl_base_rate_{coverage}") * pl.col("fl_modifier") * pl.col(f"fl_size_discount_{size_dis}_modifier")).alias(f"fl_{coverage}_modified"))

    # calcualte buildings, contents, and BI net el
    for coverage in ("buildings", "contents", "bi"):
        df = df.with_columns(
            pl.when(pl.col("loc_aop_covered") == "Yes")
            .then(pl.col(f"loc_tiv_{coverage}") * pl.col(f"fl_{coverage}_modified") * pl.col("fl_worth") )
            .otherwise(0)
            .alias(f"fl_{coverage}_market_share_el")
        )

    return df