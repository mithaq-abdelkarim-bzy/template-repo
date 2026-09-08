import hx
import polars as pl
import pandas as pd
from algorithms.rate_common_rating_functions import worth_lookup, spatial_key_modifier,iso_construction_modifier, occupancy_modifier, ppc_modifer, size_discount_modifier, base_rates



def wf_rating_calcs(hxd, df):
    

    df = base_rates(hxd, df, "WF")
    df = spatial_key_modifier(hxd, df, "WF")
    df = iso_construction_modifier(hxd, df, "WF")
    df = occupancy_modifier(hxd, df, "WF")
    df = ppc_modifer(hxd, df, "WF")
    df = size_discount_modifier(hxd, df, "WF")
    df = worth_lookup(hxd, df, "WF")

    # calcualte overall modifier (excluding size discount)
    df = df.with_columns(
        (pl.col("wf_spatial_key_modifier") * pl.col("wf_construction_modifier") * pl.col("wf_occupancy_modifier") * pl.col("wf_ppc_modifier")).alias("wf_modifier")
    )

    # calculate overall modifers
    for coverage, size_dis in zip (["buildings", "contents", "bi"], ["buildings", "contents", "buildings"]):
        df = df.with_columns((pl.col(f"wf_base_rate_{coverage}") * pl.col("wf_modifier") * pl.col(f"wf_size_discount_{size_dis}_modifier")).alias(f"wf_{coverage}_modified"))

    # calcualte buildings, contents, and BI net el
    for coverage in ("buildings", "contents", "bi"):
        df = df.with_columns(
            pl.when(pl.col("loc_aop_covered") == "Yes")
            .then(pl.col(f"loc_tiv_{coverage}") * pl.col(f"wf_{coverage}_modified") * pl.col("wf_worth") )
            .otherwise(0)
            .alias(f"wf_{coverage}_market_share_el")
        )

    return df