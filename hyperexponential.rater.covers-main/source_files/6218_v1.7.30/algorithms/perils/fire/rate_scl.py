import hx
import polars as pl
from algorithms.rate_common_rating_functions import base_rates, bg_scl_prop_covered, size_discount_modifier


def scl_rating_calcs(hxd, df):
    
    df = base_rates(hxd, df, "SCL")
    df = bg_scl_prop_covered (hxd, df, "SCL")
    df = size_discount_modifier(hxd, df, "SCL")
    df = scl_bi_rate_calcs(hxd, df)

    df = df.with_columns(
        (pl.col("scl_base_rate_buildings") * pl.col("scl_buildings_prop_covered") * pl.col("scl_size_discount_buildings_modifier")).alias("scl_buildings_modifier"),
        (pl.col("scl_base_rate_contents") * pl.col("scl_contents_prop_covered") * pl.col("scl_size_discount_contents_modifier")).alias("scl_contents_modifier")
    )
   

    return df


def scl_bi_rate_calcs(hxd, df):

    scl_bi_rate_table = pl.from_pandas(hx.params.table_scl_bi_rates)
 
    if hxd.cds.layers[0].extra_expense_coverage == "Yes":
        scl_bi_rate_table = scl_bi_rate_table.select("Index", "Business Income and Extra Expense").rename({"Business Income and Extra Expense": "scl_bi_rate"})
    else:
        scl_bi_rate_table = scl_bi_rate_table.select("Index", "Business Income Without Extra Expense").rename({"Business Income Without Extra Expense": "scl_bi_rate"})

    df = df.with_columns(df.join(scl_bi_rate_table, left_on=pl.concat_str(pl.col("bi_occupancy"),pl.col("bi_construction")), right_on="Index", how="left"))

    return df