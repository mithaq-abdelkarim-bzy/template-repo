import hx
import polars as pl
from algorithms.rate_common_rating_functions import join_param_table
from algorithms.perils.fire.rate_bg1 import bg1_rating_calcs
from algorithms.perils.fire.rate_bg2 import bg2_rating_calcs
from algorithms.perils.fire.rate_scl import scl_rating_calcs


def fire_rating_calcs(hxd, df):
    df = bg1_rating_calcs(hxd, df)
    df = bg2_rating_calcs(hxd, df)
    df = scl_rating_calcs(hxd, df)
    df = bg_bi_rate_calcs(hxd, df)
    df = ded_credit_calcs(hxd, df)
    df = expected_loss_calcs(hxd, df)


    return df

def bg_bi_rate_calcs(hxd, df):

    bg_bi_multiplier_table = pl.from_pandas(hx.params.table_bg_bi_multiplier)
 
    if hxd.cds.layers[0].extra_expense_coverage == "Yes":
        bg_bi_multiplier_table = bg_bi_multiplier_table.select("BI Occupancy", "Business Income and Extra Expense").rename({"Business Income and Extra Expense": "bg_bi_multiplier"})
    else:
        bg_bi_multiplier_table = bg_bi_multiplier_table.select("BI Occupancy", "Business Income Without Extra Expense").rename({"Business Income Without Extra Expense": "bg_bi_multiplier"})

    df = df.with_columns(df.join(bg_bi_multiplier_table, left_on="bi_risk_type", right_on="BI Occupancy", how="left"))
    df = join_param_table(df, hx.params.table_bg_bi_rates, "Average", "bg_bi_rate", "StateName", "bg1_state", upper=True, drop=False)
    df = df.with_columns((pl.col("bg_bi_multiplier") * pl.col("bg_bi_rate") * (pl.col("bg1_buildings_modifier") + pl.col("bg2_buildings_modifier"))).alias("bg_bi_rate"))
    df = df.drop("bg_bi_multiplier")

    return df




def ded_credit_calcs (hxd, df):

    ded_credit_table = pl.from_pandas(hx.params.table_ded_credit)
    ded_credit_melted = ded_credit_table.melt(id_vars=["Deductible Bands", "Peril"], variable_name="tiv_bands", value_name="credit")
    ded_credit_melted = ded_credit_melted.with_columns((pl.col("tiv_bands").cast(pl.Float64)).alias("tiv_bands"))
    ded_credit_melted = ded_credit_melted.sort([pl.col("Deductible Bands").reverse(), pl.col("tiv_bands").reverse()])

    #sets loc_aop_ded  and tiv to a min of the lowest band in the premas table 
    df = df.with_columns(
        pl.when(pl.col("loc_tiv_total") < ded_credit_melted.select("tiv_bands").max().item() - 1)
        .then(pl.col("loc_tiv_total"))
        .otherwise(ded_credit_melted.select("tiv_bands").max().item())
        .alias("temp_loc_tiv_total"),
    
        pl.when(pl.col("loc_aop_ded") > ded_credit_melted.select("Deductible Bands").min().item())
        .then(pl.col("loc_aop_ded"))
        .otherwise(ded_credit_melted.select("Deductible Bands").min().item())
        .alias("temp_acc_aop_ded")

    )

    # this needs to be rounded since values will not line up in the join_asof
    df = df.with_columns(pl.col("temp_acc_aop_ded").round(2))       
    df = df.sort("temp_acc_aop_ded")
    df = df.join_asof(
        ded_credit_melted.select("Deductible Bands").sort("Deductible Bands").unique(),
        left_on=pl.col("temp_acc_aop_ded"), right_on=pl.col("Deductible Bands"), strategy="backward"
    )
    
    
    # the forward strategy will promot vales when they are equal. The code below accounts for that
    df = df.with_columns(
        pl.when(pl.col("temp_acc_aop_ded").is_in(ded_credit_melted.select("Deductible Bands").unique()["Deductible Bands"].to_list()))
        .then(pl.col("temp_acc_aop_ded"))
        .otherwise(pl.col("Deductible Bands"))
        .alias("Deductible Bands")
    )
    
    # Original code
    df = df.sort("temp_loc_tiv_total")
    df = df.join_asof(
        ded_credit_melted.select("tiv_bands").sort("tiv_bands").unique(),
        left_on=pl.col("temp_loc_tiv_total"), right_on=pl.col("tiv_bands"), strategy="forward"
    )

    peril_list = ded_credit_melted["Peril"].unique().to_list()

    for peril in peril_list:
        df = df.join(
            ded_credit_melted.filter(pl.col("Peril") == peril).select("Deductible Bands", "tiv_bands", "credit").rename({"credit": peril}),       
            on=("Deductible Bands", "tiv_bands"), how = "left"
        )

    df = df.drop("temp_loc_tiv_total", "temp_acc_aop_ded") 


    # long line of code. I have a feeling Seb won't like it! 
    df = df.with_columns(
        pl.when(pl.col("bg2_region") == "Southeast")
        .then((((pl.col("bg1_base_rate_buildings") + pl.col("bg1_base_rate_contents")) * pl.col("BG1")) + ((pl.col("bg2_base_rate_buildings") + pl.col("bg2_base_rate_contents")) * pl.col("BG2 SE")) + ((pl.col("scl_base_rate_buildings") + pl.col("scl_base_rate_contents")) * pl.col("BG2 NON SE AND SCL"))) \
            / (pl.col("bg1_base_rate_buildings") + pl.col("bg1_base_rate_contents") + pl.col("bg2_base_rate_buildings") + pl.col("bg2_base_rate_contents") + pl.col("scl_base_rate_buildings") + pl.col("scl_base_rate_contents")))
        .otherwise((((pl.col("bg1_base_rate_buildings") + pl.col("bg1_base_rate_contents")) * pl.col("BG1")) + ((pl.col("bg2_base_rate_buildings") + pl.col("bg2_base_rate_contents")) * pl.col("BG2 NON SE AND SCL")) + ((pl.col("scl_base_rate_buildings") + pl.col("scl_base_rate_contents")) * pl.col("BG2 NON SE AND SCL"))) \
            / (pl.col("bg1_base_rate_buildings") + pl.col("bg1_base_rate_contents") + pl.col("bg2_base_rate_buildings") + pl.col("bg2_base_rate_contents") + pl.col("scl_base_rate_buildings") + pl.col("scl_base_rate_contents")))
        .alias("ded_credit")
    )
    df = df.drop("Deductible Bands", "tiv_bands", "BG1", "BG2 SE", "BG2 NON SE AND SCL")
    
    return df

def expected_loss_calcs(hxd, df):

    for coverage in ("buildings", "contents"):
        for peril in ("bg1", "bg2", "scl"):
            df = df.with_columns(
                pl.when(pl.col("loc_aop_covered") == "Yes")
                .then((pl.col(f"{peril}_{coverage}_modifier") * pl.col(f"loc_tiv_{coverage}") * pl.col("ded_credit"))/100)
                .when((hxd.cds.layers[0].standard_non_standard == "Yes") & (pl.col("loc_scs_covered") == "Yes"))
                .then(((pl.col(f"{peril}_{coverage}_modifier") * pl.col(f"loc_tiv_{coverage}") * pl.col("ded_credit")) * (pl.col("limit_factor") - pl.col("excess_factor")))/100)
                .otherwise(pl.lit(0))
                .alias(f"{peril}_{coverage}_market_share_el")
            )
            
    # in the CMT we are checking if SCS is covered. 
    df = df.with_columns(
        pl.when(pl.col("loc_aop_covered") == "Yes")
        .then(((pl.col("bg_bi_rate") + pl.col("scl_bi_rate")) * pl.col("loc_tiv_bi"))/100)
        .when((hxd.cds.layers[0].standard_non_standard == "Yes") & (pl.col("loc_scs_covered") == "Yes"))
        .then((((pl.col("bg_bi_rate") + pl.col("scl_bi_rate")) * pl.col("loc_tiv_bi")) * (pl.col("limit_factor") - pl.col("excess_factor")))/100)
        .otherwise(0)
        .alias("fire_bi_market_share_el")
    )

    return df


   