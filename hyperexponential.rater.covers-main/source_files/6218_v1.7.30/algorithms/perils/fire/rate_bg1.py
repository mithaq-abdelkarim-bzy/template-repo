import hx
import polars as pl
from algorithms.rate_common_rating_functions import base_rates, bg_scl_prop_covered, size_discount_modifier, ppc_modifer


def bg1_rating_calcs(hxd, df):

    df = base_rates(hxd, df, "BG1")
    df = bg_scl_prop_covered(hxd, df, "BG1")
    df = size_discount_modifier(hxd, df, "BG1")
    df = ppc_modifer(hxd, df, "BG1")

  

    # calcualte buildings and contents modifier
    df = df.with_columns(
        (pl.col("bg1_base_rate_buildings") * pl.col("bg1_buildings_prop_covered") * pl.col("bg1_size_discount_buildings_modifier") * pl.col("bg1_ppc_modifier")).alias("bg1_buildings_modifier"),
        (pl.col("bg1_base_rate_contents") * pl.col("bg1_contents_prop_covered") * pl.col("bg1_size_discount_contents_modifier") * pl.col("bg1_ppc_modifier")).alias("bg1_contents_modifier")
    )

    return df



