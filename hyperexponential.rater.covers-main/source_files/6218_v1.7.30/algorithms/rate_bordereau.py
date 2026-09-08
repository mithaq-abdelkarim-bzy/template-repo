import hx
import polars as pl
import pandas as pd
import numpy as np
from datetime import datetime
from algorithms.rate_common_rating_functions import join_param_table


def read_bordereau_table(hxd):

    df = read_sov(hxd)
    df = clean_join_data(hxd, df)
    df = excess_calcs(df)
    
    return  df


def read_sov(hxd):
    columns = [
        "last_updated", "loc_id", "acc_name", "acc_number", "inception_date", "expiry_date", "ceded_share", "acc_beazley_received_gg_prem", "acc_all_perils_gg_sd", "loc_1_in_250_oep", "loc_1_in_10_aep", "loc_ws_beazley_share_gg_aal", "loc_eq_beazley_share_gg_aal", "zip", 
        "latitude", "longitude", "loc_tiv_buildings", "loc_tiv_contents", "loc_tiv_bi", "loc_tiv_total", "iso_constr", "ppc_code", "sprinkler", "occupancy_description", 
        "num_stories", "year_built", "floor_area", "distance_to_coast", "beazley_gate","loc_aop_covered", "loc_aop_ded", "loc_aop_excess", "loc_aop_limit",
        "loc_scs_covered", "loc_scs_ded", "loc_scs_excess", "loc_scs_limit", "loc_ws_covered", "loc_ws_ded", "loc_ws_excess", "loc_ws_limit", 
        "loc_eq_covered", "loc_eq_ded", "loc_eq_excess", "loc_eq_limit"
        ]

    df = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.cds.exposure.granular.schedule_table])

    df["industry"] = [row.industry_occupancy_dropdown.industry for row in hxd.cds.exposure.granular.schedule_table]
    df["occupancy"] = [row.industry_occupancy_dropdown.occupancy for row in hxd.cds.exposure.granular.schedule_table]
    df["country"] = [row.address_dropdown.country for row in hxd.cds.exposure.granular.schedule_table]
    df["state"] = [row.address_dropdown.state for row in hxd.cds.exposure.granular.schedule_table]
    df["city"] = [row.address_dropdown.city for row in hxd.cds.exposure.granular.schedule_table]
    df["county"] = [row.address_dropdown.county for row in hxd.cds.exposure.granular.schedule_table]

    df = pl.from_pandas(df)

    df = df.with_columns(
        pl.col("last_updated").cast(pl.Date),
        pl.col("loc_id").cast(pl.Int64),
        pl.col("acc_name").cast(pl.Utf8),
        pl.col("acc_number").cast(pl.Utf8),
        pl.col("inception_date").cast(pl.Date),
        pl.col("expiry_date").cast(pl.Date),
        pl.col("ceded_share").cast(pl.Float64),
        pl.col("acc_beazley_received_gg_prem").cast(pl.Float64),
        pl.col("loc_1_in_250_oep").cast(pl.Float64),
        pl.col("loc_1_in_10_aep").cast(pl.Float64),
        pl.col("loc_eq_beazley_share_gg_aal").cast(pl.Float64),
        pl.col("loc_ws_beazley_share_gg_aal").cast(pl.Float64),
        pl.col("zip").cast(pl.Utf8),
        pl.col("latitude").cast(pl.Float64),
        pl.col("longitude").cast(pl.Float64),
        pl.col("loc_tiv_buildings").cast(pl.Float64),
        pl.col("loc_tiv_contents").cast(pl.Float64),
        pl.col("loc_tiv_bi").cast(pl.Float64),
        pl.col("loc_tiv_total").cast(pl.Float64),
        pl.col("iso_constr").cast(pl.Utf8),
        pl.col("ppc_code").cast(pl.Utf8), # needs to be a str because prarms table (table_fire_ppc) that we map to this is a str. Hence, I'm assuming that this column could have non-numbers  
        pl.col("sprinkler").cast(pl.Utf8),
        pl.col("occupancy_description").cast(pl.Utf8),
        pl.col("num_stories").cast(pl.Int64),
        pl.col("year_built").cast(pl.Int64),
        pl.col("floor_area").cast(pl.Int64), 
        pl.col("distance_to_coast").cast(pl.Float64),
        pl.col("beazley_gate").cast(pl.Utf8),
        pl.col("loc_aop_covered").cast(pl.Utf8),
        pl.col("loc_aop_ded").cast(pl.Float64),
        pl.col("loc_aop_excess").cast(pl.Float64),
        pl.col("loc_aop_limit").cast(pl.Float64),
        pl.col("loc_scs_covered").cast(pl.Utf8),
        pl.col("loc_scs_ded").cast(pl.Float64),
        pl.col("loc_scs_excess").cast(pl.Float64),
        pl.col("loc_scs_limit").cast(pl.Float64),
        pl.col("loc_ws_covered").cast(pl.Utf8),
        pl.col("loc_ws_ded").cast(pl.Float64),
        pl.col("loc_ws_excess").cast(pl.Float64),
        pl.col("loc_ws_limit").cast(pl.Float64),
        pl.col("loc_eq_covered").cast(pl.Utf8),
        pl.col("loc_eq_ded").cast(pl.Float64),
        pl.col("loc_eq_excess").cast(pl.Float64),
        pl.col("loc_eq_limit").cast(pl.Float64),
        pl.concat_str(pl.col("state"), pl.col("county")).alias("state_county")
    )

    return df


def clean_join_data(hxd, df):
    
    inception_date = datetime(hxd.cds.standard_fields.inception_date.year, hxd.cds.standard_fields.inception_date.month, hxd.cds.standard_fields.inception_date.day)

    ############### These calcs need to be done after the excess calcs 
    rms_ws_uplift = pl.from_pandas(hx.params.table_uplift)["rms_ws_uplift"].item()
    rms_eq_uplift = pl.from_pandas(hx.params.table_uplift)["rms_eq_uplift"].item()

    df = df.with_columns(
        (pl.col("loc_ws_beazley_share_gg_aal") * pl.lit(rms_ws_uplift)).alias("loc_ws_beazley_share_aal"),
        (pl.col("loc_eq_beazley_share_gg_aal") * pl.lit(rms_eq_uplift)).alias("loc_eq_beazley_share_aal")
    )


    df = df.with_columns(
        (pl.col("loc_ws_beazley_share_aal") / pl.col("ceded_share")).alias("loc_ws_market_share_aal"),
        (pl.col("loc_eq_beazley_share_aal") / pl.col("ceded_share")).alias("loc_eq_market_share_aal")
    )


    df = df.with_columns(pl.col("loc_1_in_250_oep").sum().over("acc_number").alias("acc_1_in_250_oep"))

    # assign weights to eq and ws (we need two weights). One with the avg weight for locations that have 0 aal and another without the avg.
    # This is because the NMP will need to be applied to ws and eq (cases where weight is using avg) and it will also be needed for capital allocation (cases where we have 0 weights) where we don't want to assign a cat cost of cap when there is no AAL
    # for more details see how they are used in the rate_premium.py tab
    df = df.with_columns(
        (pl.col("loc_ws_beazley_share_aal") / pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal")).fill_null(0).fill_nan(0).alias("ws_weight_temp"),
        (pl.col("loc_eq_beazley_share_aal") / pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal")).fill_null(0).fill_nan(0).alias("eq_weight_temp")
    )

    ws_average = df.select(pl.col("ws_weight_temp")).mean().item()
    eq_average = df.select(pl.col("eq_weight_temp")).mean().item()
    total = ws_average + eq_average
    ws_average_weight = ws_average / total if total != 0 else ws_average
    eq_average_weight = eq_average / total if total != 0 else eq_average

    df = df.with_columns(
        pl.when(pl.sum_horizontal("ws_weight_temp", "eq_weight_temp") == 0)
        .then(pl.lit(ws_average_weight))
        .otherwise(pl.col("ws_weight_temp"))
        .alias("ws_weight_with_avg")
    )

    df = df.with_columns(
        pl.when(pl.sum_horizontal("ws_weight_temp", "eq_weight_temp") == 0)
        .then(pl.lit(eq_average_weight))
        .otherwise(pl.col("eq_weight_temp"))
        .alias("eq_weight_with_avg")
    )

    df = df.drop("ws_weight_temp", "eq_weight_temp")
    
    # setting ws and eq to zero or 1 depending on if they are covered
    df = df.with_columns(
        pl.when((pl.col("loc_ws_covered") == "No") & (pl.col("loc_eq_covered") == "No"))
        .then(pl.lit(0))
        .when((pl.col("loc_ws_covered") == "Yes") & (pl.col("loc_eq_covered") == "No"))
        .then(pl.lit(1))
        .otherwise(pl.col("ws_weight_with_avg"))
        .alias("ws_weight_without_avg")
    )

    df = df.with_columns(
        pl.when((pl.col("loc_ws_covered") == "No") & (pl.col("loc_eq_covered") == "No"))
        .then(pl.lit(0))
        .when((pl.col("loc_ws_covered") == "No") & (pl.col("loc_eq_covered") == "Yes"))
        .then(pl.lit(1))
        .otherwise(pl.col("eq_weight_with_avg"))
        .alias("eq_weight_without_avg")
    )

    df = df.with_columns(
        (pl.col("ws_weight_with_avg") * pl.col("loc_1_in_250_oep")).alias("loc_ws_1_in_250_oep"),
        (pl.col("eq_weight_with_avg") * pl.col("loc_1_in_250_oep")).alias("loc_eq_1_in_250_oep")
    )   


    # add account level deductible 
    df = df.with_columns(pl.col("loc_aop_ded").sum().over("acc_number").alias("acc_aop_deductible").round(5))
   
    # get BG1 state. We use three different ways of mapping it to ensure that all zips are mapped
    if hxd.cds.currencies.source_currency == "USD":
        
        df = join_param_table(df, hx.params.table_bg_mapping, "State Name", "bg1_state", "Zip Code", "zip", drop=False)
        df = join_param_table(df, hx.params.table_secondary_mapping, "State", "bg1_state_method_2", "Zip Code", "zip", drop=False)
        df = join_param_table(df, hx.params.table_bg_mapping, "State Name", "bg1_state_method_3", "State Abbreviation", "state", drop=False)
 

        df = df.with_columns(pl.col("bg1_state").fill_null(pl.col("bg1_state_method_2")).alias("bg1_state"))
        df = df.with_columns(pl.col("bg1_state").fill_null(pl.col("bg1_state_method_3")).alias("bg1_state"))
        df = df.drop("bg1_state_method_2", "bg1_state_method_3")
    else:
        df = df.with_columns(
            pl.col("state").alias("bg1_state")
        )

    # Get BG1 Territory
    df = join_param_table(df, hx.params.table_bg_mapping, "BG1 Terr", "bg1_territory", "Zip Code", "zip", drop=False)
    # we need to fill this with NA since we use it to lookup from a param table with NA entries
    df = df.with_columns(pl.col("bg1_territory").fill_null(pl.lit("NA")))
    
    # set blank or null values in iso_constr to ISO.1
    df = df.with_columns(
        pl.when(pl.col("iso_constr").is_in(["ISO.1", "ISO.2", "ISO.3", "ISO.4", "ISO.5", "ISO.6"]))
        .then(pl.col("iso_constr"))
        .otherwise(pl.lit("ISO.1"))
        .alias("iso_constr")
    )

    # excess calcs (this is used for BG1 calcs)
    df = df.with_columns(
        pl.when(pl.col("loc_scs_ded") > 0).then(pl.col("loc_scs_ded"))
        .when(pl.col("loc_scs_excess") > 0).then(pl.col("loc_scs_excess"))
        .when(pl.col("loc_ws_ded") > 0).then(pl.col("loc_ws_ded"))
        .when(pl.col("loc_ws_excess") > 0).then(pl.col("loc_ws_excess"))
        .when(pl.col("loc_eq_ded") > 0).then(pl.col("loc_eq_ded"))
        .when(pl.col("loc_eq_excess") > 0).then(pl.col("loc_eq_excess"))
        .otherwise(0).alias("bg_excess")        
    )

    df = df.with_columns(
        pl.when(pl.col("loc_scs_ded") > 0).then(pl.col("loc_scs_ded") + pl.col("loc_scs_limit"))
        .when(pl.col("loc_scs_excess") > 0).then(pl.col("loc_scs_excess") + pl.col("loc_scs_limit"))
        .when(pl.col("loc_ws_ded") > 0).then(pl.col("loc_ws_ded") + pl.col("loc_ws_limit"))
        .when(pl.col("loc_ws_excess") > 0).then(pl.col("loc_ws_excess") + pl.col("loc_ws_limit"))
        .when(pl.col("loc_eq_ded") > 0).then(pl.col("loc_eq_ded") + pl.col("loc_eq_limit"))
        .when(pl.col("loc_eq_excess") > 0).then(pl.col("loc_eq_excess") + pl.col("loc_eq_limit"))
        .otherwise(0).alias("loc_aop_limit")        
    )

    # calcualte BG2 and SCL Region 
    if hxd.cds.currencies.source_currency == "USD":
        df = join_param_table(df, hx.params.table_bg2_scl_regions, "BG2 Region", "bg2_region", "State", "bg1_state", drop=False)
        df = join_param_table(df, hx.params.table_bg2_scl_regions, "SCL Region", "scl_region", "State", "bg1_state", drop=False)

    else:
        df = df.with_columns(pl.lit("Entire State").alias("bg2_region"))
        df = df.with_columns(pl.lit("SEW").alias("scl_region"))

    # calculate BG2 Territory
    df = join_param_table(df, hx.params.table_bg_mapping, "BG2 Terr", "bg2_territory", "Zip Code", "zip", drop=False)
    df = df.with_columns(pl.col("bg2_territory").fill_null("Unknown"))

    # calculate SCL occupancy
    scl_occupancy_table = pl.from_pandas(hx.params.table_atc_mapping).sort(pl.col("SCL Occupancy") == "Unknown", descending=True).unique(subset=["Mapped ATC"]).select("SCL Occupancy", "Mapped ATC").rename({"SCL Occupancy": "scl_occupancy", "Mapped ATC": "occupancy"})
    df = df.join(scl_occupancy_table, on="occupancy", how="left")
    df = df.with_columns(pl.col("scl_occupancy").fill_null("Unknown"))

    #BI Construction
    df = df.with_columns(
        pl.when(pl.col("iso_constr").is_in(["ISO.5", "ISO.6"]))
        .then(pl.col("iso_constr"))
        .otherwise(pl.lit("All Other"))
        .alias("bi_construction")
    )

    #BI Occupancy
    df = df.with_columns(
        pl.when(pl.col("occupancy") == "Permanent Dwelling (multi family housing)")
        .then(pl.col("occupancy"))
        .otherwise(pl.lit("All Other"))
        .alias("bi_occupancy")
    )

    # Type of BI Risk
    df = join_param_table(df, hx.params.table_atc_mapping, "BI Group", "bi_risk_type", "Original Description", "occupancy", drop=False)

    #ATC Code
    df = join_param_table(df, hx.params.table_atc_occupancy_modifier, "ATC_Code", "atc_occupancy_code", "Row Labels", "occupancy", drop=False)

    df = df.with_row_count()
    
    return df


def excess_calcs(df):

    # in the CMT we are dividing by buildings tiv. Should this be overall tiv?
    df = df.with_columns(
        (pl.col("bg_excess") / pl.col("loc_tiv_buildings")).alias("excess_perc_of_tiv")
    )

    # replace all inf, nan, and blansk with 1
    df = df.with_columns(
        pl.when(pl.col("excess_perc_of_tiv").cast(pl.Float64, strict=False).is_null() | pl.col("excess_perc_of_tiv").is_nan() | (pl.col("excess_perc_of_tiv").is_in([float("inf"), -float("inf")])))
        .then(pl.lit(1))
        .otherwise(pl.col("excess_perc_of_tiv"))
        .alias("excess_perc_of_tiv")
    )

    df = df.with_columns(
        (pl.col("loc_aop_limit") / pl.col("loc_tiv_total")).alias("limit_perc_of_tiv")
    )

    df = df.sort("limit_perc_of_tiv")
    limit_factors_table = pl.from_pandas(hx.params.table_limit_factors)
    limit_factors_melted = limit_factors_table.melt(id_vars="Limit as proportion of TIV", variable_name="peril", value_name="limit_factor")

    df = df.join_asof(limit_factors_table.select("Limit as proportion of TIV").sort("Limit as proportion of TIV"), left_on="limit_perc_of_tiv", right_on="Limit as proportion of TIV", strategy="backward")

    # calculate limit factor 
    df = df.with_columns(
        pl.when((pl.col("loc_scs_covered") == "Yes") | (pl.col("loc_ws_covered") == "Yes"))
        .then(pl.lit("WS1"))
        .otherwise(pl.lit("EQ1"))
        .alias("peril")        
    )

    df = df.join(limit_factors_melted, on=["Limit as proportion of TIV", "peril"], how="left")

    df = df.with_columns(
        pl.when(pl.col("limit_factor") <= 0)
        .then(pl.lit(limit_factors_table["WS1"][1]))
        .otherwise(pl.col("limit_factor"))
        .alias("limit_factor")
    )

    df = df.drop("Limit as proportion of TIV")

    # calculate excess factor
    df = df.sort("excess_perc_of_tiv")
    
    df = df.join_asof(limit_factors_table.select("Limit as proportion of TIV").sort("Limit as proportion of TIV"), left_on="excess_perc_of_tiv", right_on="Limit as proportion of TIV", strategy="backward")
    df = df.join(limit_factors_melted, left_on=["Limit as proportion of TIV", "peril"], right_on=["Limit as proportion of TIV", "peril"], how="left")
    df = df.rename({"limit_factor_right": "excess_factor_backward"})
    df = df.drop("Limit as proportion of TIV")

    #this is for the greater than join. Used in .otherwise part of when statment below 
    df = df.join_asof(limit_factors_table.select("Limit as proportion of TIV").sort("Limit as proportion of TIV"), left_on="excess_perc_of_tiv", right_on="Limit as proportion of TIV", strategy="forward")
    df = df.join(limit_factors_melted, left_on=["Limit as proportion of TIV", "peril"], right_on=["Limit as proportion of TIV", "peril"], how="left")
    df = df.rename({"limit_factor_right": "excess_factor_forward"})
    df = df.drop("Limit as proportion of TIV")

    
    df = df.with_columns(
        pl.when((pl.col("excess_factor_backward") == pl.col("limit_factor")))
        .then(pl.col("excess_factor_forward"))
        .otherwise("excess_factor_backward")
        .alias("excess_factor")
    )

    df = df.drop("peril", "excess_factor_backward", "excess_factor_forward")

    return df
