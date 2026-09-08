import hx
import polars as pl
from algorithms.rate_common_rating_functions import base_rates, bg_scl_prop_covered, size_discount_modifier


def bg2_rating_calcs(hxd, df):

    
    df = base_rates(hxd, df, "BG2")
    df = bg_scl_prop_covered(hxd, df, "BG2")
    df = size_discount_modifier(hxd, df, "BG2")

    df = df.with_columns(
        (pl.col("bg2_base_rate_buildings") * pl.col("bg2_buildings_prop_covered") * pl.col("bg2_size_discount_buildings_modifier")).alias("bg2_buildings_modifier"),
        (pl.col("bg2_base_rate_contents") * pl.col("bg2_contents_prop_covered") * pl.col("bg2_size_discount_contents_modifier")).alias("bg2_contents_modifier")
    )


    return df