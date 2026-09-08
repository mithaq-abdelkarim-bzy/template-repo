import hx
import polars as pl
import pandas as pd
import numpy as np
from algorithms.rate_common_rating_functions import worth_lookup, spatial_key_modifier, iso_construction_modifier, floor_area_modifier, bhi_modifier, base_rates, year_built_modifier, size_discount_modifier, occupancy_modifier



def hail_rating_calcs(hxd, df):
    

    df = base_rates(hxd, df, "HA")
    df = spatial_key_modifier(hxd, df, "HA") 
    df = iso_construction_modifier(hxd, df, "HA")
    df = year_built_modifier(hxd, df, "HA")
    df = floor_area_modifier(hxd, df, "HA")
    df = bhi_modifier(hxd, df, "HA")
    df = occupancy_modifier(hxd, df, "HA")
    df = size_discount_modifier(hxd, df, "HA")
    df = worth_lookup(hxd, df, "HA")


    # calcualte overall modifier (excluding size discount)
    df = df.with_columns(
        (pl.col("ha_spatial_key_modifier") * pl.col("ha_construction_modifier") * pl.col("ha_year_built_modifier") * pl.col("ha_floor_area_modifier") * pl.col("ha_bhi_modifier") * pl.col("ha_occupancy_modifier")).alias("ha_modifier")
    )

    # calculate overall modifers
    for coverage, size_dis in zip (["buildings", "contents", "bi"], ["buildings", "contents", "buildings"]):
        df = df.with_columns((pl.col(f"ha_base_rate_{coverage}") * pl.col("ha_modifier") * pl.col(f"ha_size_discount_{size_dis}_modifier")).alias(f"ha_{coverage}_modified"))

    # calcualte buildings, contents, and BI net el
    for coverage in ("buildings", "contents", "bi"):
        df = df.with_columns(
            pl.when((pl.col("loc_aop_covered") == "Yes") | ((hxd.cds.layers[0].standard_non_standard == "Yes") & (pl.col("loc_scs_covered") == "Yes")))
            .then(pl.col(f"loc_tiv_{coverage}") * pl.col(f"ha_{coverage}_modified") * pl.col("ha_worth") )
            .otherwise(0)
            .alias(f"ha_{coverage}_market_share_el")
        )
        
    return df