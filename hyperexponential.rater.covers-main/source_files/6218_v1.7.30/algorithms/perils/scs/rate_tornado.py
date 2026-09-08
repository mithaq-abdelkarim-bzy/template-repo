import hx
import polars as pl
import pandas as pd
import numpy as np
from algorithms.rate_common_rating_functions import worth_lookup, spatial_key_modifier, iso_construction_modifier, bhi_modifier, base_rates, year_built_modifier, size_discount_modifier, occupancy_modifier



def tornado_rating_calcs(hxd, df):
    

    df = base_rates(hxd, df, "TN")
    df = spatial_key_modifier(hxd, df, "TN") 
    df = iso_construction_modifier(hxd, df, "TN")
    df = year_built_modifier(hxd, df, "TN")
    df = bhi_modifier(hxd, df, "TN")
    df = size_discount_modifier(hxd, df, "TN")
    df = occupancy_modifier(hxd, df, "TN")
    df = worth_lookup(hxd, df, "TN")


    # calcualte overall modifier (excluding size discount)
    df = df.with_columns(
        (pl.col("tn_spatial_key_modifier") * pl.col("tn_year_built_modifier") * pl.col("tn_bhi_modifier") * pl.col("tn_occupancy_modifier") * pl.col("tn_construction_modifier")).alias("tn_modifier")
    )

    # calculate overall modifers
    for coverage, size_dis in zip (["buildings", "contents", "bi"], ["buildings", "contents", "buildings"]):
        df = df.with_columns((pl.col(f"tn_base_rate_{coverage}") * pl.col("tn_modifier") * pl.col(f"tn_size_discount_{size_dis}_modifier")).alias(f"tn_{coverage}_modified"))

    # calcualte buildings, contents, and BI net el
    for coverage in ("buildings", "contents", "bi"):
        df = df.with_columns(
            pl.when((pl.col("loc_aop_covered") == "Yes") | ((hxd.cds.layers[0].standard_non_standard == "Yes") & (pl.col("loc_scs_covered") == "Yes")))
            .then(pl.col(f"loc_tiv_{coverage}") * pl.col(f"tn_{coverage}_modified") * pl.col("tn_worth") )
            .otherwise(0)
            .alias(f"tn_{coverage}_market_share_el")
        )

    return df