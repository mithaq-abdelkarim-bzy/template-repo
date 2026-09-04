import hx
import polars as pl
import numpy as np
from scipy import stats
from algorithms.analytical_curves import loss_curve, size_discount
from algorithms.rating_common_functions import loss_curve_lookup, ground_up_uw_rate, ground_up_rate
from algorithms.utilities import pd_df_from_hx_list
from algorithms.intl_rating_common_functions import join_intl_ded_table


def policy_limits_usd(hxd, other_data, layer, index):
    # Move to utilities file later
    # Calculate Limit and Excess in USD
    exchange_rate = hxd.policy_information.exchange_rate
    other_data[f'policy_limit_usd_layer{index}'] = layer.limit / exchange_rate if exchange_rate else 0
    other_data[f'policy_excess_usd_layer{index}'] = layer.excess / exchange_rate if exchange_rate else 0
    other_data[f'policy_wildfire_deductible_usd_layer{index}'] = layer.perils.wildfire.deductible / exchange_rate if exchange_rate and layer.perils.wildfire.deductible else 0
    return other_data


def wildfire_rating_calc(hxd, df, other_data):
    df = wildfire_rating_non_layer(hxd, df, other_data)

    for index, layer in enumerate(hxd.layers, start=1):
        other_data = policy_limits_usd(hxd, other_data, layer, index)
        df = wildfire_expected_losses(hxd, df, other_data, layer, index)

    return df


def wildfire_expected_losses(hxd, df, other_data, layer, index):
    # Base Rate 
    for col in ["wildfire_buildings_base_rate", "wildfire_contents_base_rate", "wildfire_bi_base_rate"]:
        df = df.with_columns(
            (pl.col(col) * pl.col(f"wf_covered_rating_layer{index}")).alias(col + f"_layer{index}")
        )

    df = df.with_columns(
        (pl.col(f"wildfire_buildings_base_rate_layer{index}") + pl.col(f"wildfire_contents_base_rate_layer{index}") + pl.col(f"wildfire_bi_base_rate_layer{index}")).alias(f"wildfire_total_base_rate_layer{index}")
    )

    # Ground Up Rates
    df = ground_up_rate(hxd, df, other_data, layer, index, "wildfire")
    df = ground_up_uw_rate(hxd, df, other_data, layer, index, "wildfire", "wf")

    df = join_intl_ded_table(hxd, df, "wildfire", index, fill_null_ded=other_data[f'policy_wildfire_deductible_usd_layer{index}'] or 0)
    df = df.drop(["country_sublimit", "perc_of_tiv", "fixed_min", "fixed_max"])

    df = df.with_columns(
        pl.lit(other_data[f'policy_limit_usd_layer{index}']).alias(f"limit_usd_layer{index}"),
        pl.lit(other_data[f'policy_excess_usd_layer{index}']).alias(f"excess_usd_layer{index}"),
        (
            pl.when(pl.col("country") == "United States").then(
                pl.lit(other_data[f'policy_wildfire_deductible_usd_layer{index}'])
            ).otherwise(
                pl.when((pl.col(f"wildfire_loc_intl_ded_layer{index}") == 0) | (pl.col(f"wildfire_loc_intl_ded_layer{index}").is_null()))
                .then(pl.lit(other_data[f'policy_wildfire_deductible_usd_layer{index}']))
                .otherwise(pl.col(f"wildfire_loc_intl_ded_layer{index}")))
            ).alias(f"wildfire_deductible_usd_layer{index}")
    )

    # TIV Exposed
    df = df.with_columns(
        pl.max(
            pl.min(
                pl.col('tiv_total_usd') - pl.col(f"excess_usd_layer{index}"),
                pl.col(f"limit_usd_layer{index}")
            ),
            0
        ).fill_null(0).alias(f"wildfire_tiv_exposed_layer{index}")
    )

    # Entry / TIV & Exit / TIV

    df = df.with_columns(
        (
           ( pl.col(f"excess_usd_layer{index}") + pl.col(f"wildfire_deductible_usd_layer{index}")) / pl.col('tiv_region')
        ).fill_nan(0).fill_null(0).alias(f"wildfire_entry_over_tiv_layer{index}"),
        (
            (pl.col(f"limit_usd_layer{index}") + pl.col(f"wildfire_deductible_usd_layer{index}") + pl.col(f"excess_usd_layer{index}"))/ pl.col('tiv_region')
        ).fill_nan(0).fill_null(0).alias(f"wildfire_exit_over_tiv_layer{index}")
    )

    # Replace infinity values
    df = df.with_columns(
        [
            pl.when(pl.col(f"wildfire_entry_over_tiv_layer{index}").is_infinite()).then(0).otherwise(pl.col(f"wildfire_entry_over_tiv_layer{index}")).keep_name(),
            pl.when(pl.col(f"wildfire_exit_over_tiv_layer{index}").is_infinite()).then(0).otherwise(pl.col(f"wildfire_exit_over_tiv_layer{index}")).keep_name()
        ]
    )

    # Entry & Exit
    df = loss_curve(hxd, df, index, "wildfire")

    # Worth
    df = df.with_columns(
        (pl.col(f"wildfire_exit_perc_layer{index}") - pl.col(f"wildfire_entry_perc_layer{index}")).alias(f"wildfire_worth_percent_layer{index}")
    )

    policy_length = hxd.policy_information.policy_length.selected

    # Expected Loss
    df = df.with_columns(
        (
            pl.col('tiv_buildings_usd') * pl.col(f"wildfire_buildings_ground_up_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_buildings_pre_uw_layer{index}"),
        (
            pl.col('tiv_contents_total_usd') * pl.col(f"wildfire_contents_ground_up_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_contents_pre_uw_layer{index}"),
        (
            pl.col('tiv_bi_usd') * pl.col(f"wildfire_bi_ground_up_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_bi_pre_uw_layer{index}"),
        (
            pl.col('tiv_buildings_usd') * pl.col(f"wildfire_buildings_ground_up_uw_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_buildings_post_uw_layer{index}"),
        (
            pl.col('tiv_contents_total_usd') * pl.col(f"wildfire_contents_ground_up_uw_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_contents_post_uw_layer{index}"),
        (
            pl.col('tiv_bi_usd') * pl.col(f"wildfire_bi_ground_up_uw_rate_layer{index}") * pl.col(f"wildfire_worth_percent_layer{index}") * policy_length
        ).alias(f"wildfire_expected_loss_bi_post_uw_layer{index}")
    )

    df = df.with_columns(
        (
            pl.col(f"wildfire_expected_loss_buildings_pre_uw_layer{index}") + \
            pl.col(f"wildfire_expected_loss_contents_pre_uw_layer{index}") + \
            pl.col(f"wildfire_expected_loss_bi_pre_uw_layer{index}")
        ).alias(f"wildfire_total_expected_loss_pre_uw_layer{index}"),
        (
            pl.col(f"wildfire_expected_loss_buildings_post_uw_layer{index}") + \
            pl.col(f"wildfire_expected_loss_contents_post_uw_layer{index}") + \
            pl.col(f"wildfire_expected_loss_bi_post_uw_layer{index}")
        ).alias(f"wildfire_total_expected_loss_post_uw_layer{index}")
    )

    # Split out into US and Intl for later
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col(f"wildfire_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(None)).alias(f"wildfire_us_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") == "United States").then(pl.col(f"wildfire_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(None)).alias(f"wildfire_us_total_expected_loss_post_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"wildfire_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(None)).alias(f"wildfire_intl_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"wildfire_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(None)).alias(f"wildfire_intl_total_expected_loss_post_uw_layer{index}"),
    )

    return df


def wildfire_rating_non_layer(hxd, df, other_data):
    # Inputs:
    # catnet_score_wf (AW)
    # riskmeter_score_wf (AX)

    # Load parameter tables
    wf_tiers_df = hx.params.wf_tiers
    wf_loss_curves_df = hx.params.wf_loss_curve_selection
    default_loss_curves_df = hx.params.default_loss_curve_selection
    wf_us_cat_base_rates_df = hx.params.wf_us_cat_base_rates
    intl_base_rates_df = hx.params.intl_base_rates
    catnet_score_df = hx.params.wf_catnet_score
    riskmeter_score_df = hx.params.wf_riskmeter_score
    non_cat_base_rates_df = hx.params.non_cat_base_rates
    construction_load_df = hx.params.construction_load
    pc_code_df = hx.params.ppc_load

    # Fetch Wildfire State Tier
    wf_tiers_df = wf_tiers_df[["US State Code", "WF Tier"]]
    wf_tiers_pl = pl.from_pandas(wf_tiers_df).rename({"US State Code": "state", "WF Tier": "wildfire_us_tier"})
    df = df.join(wf_tiers_pl, on="state", how="left")

    # Fetch Wildfire Category
    # From Riskmeter
    riskmeter_score_categories_df = riskmeter_score_df[["Score", "Category"]]
    riskmeter_score_categories_pl = pl.from_pandas(riskmeter_score_categories_df).rename({"Score": "riskmeter_score_wf", "Category": "wildfire_riskmeter_category"})
    df = df.join(riskmeter_score_categories_pl, on="riskmeter_score_wf", how="left")
    # From Catnet
    catnet_score_categories_df = catnet_score_df[["Intensity", "Category"]]
    catnet_score_categories_pl = pl.from_pandas(catnet_score_categories_df).rename({"Intensity": "catnet_score_wf", "Category": "wildfire_catnet_category"})
    df = df.join(catnet_score_categories_pl, on="catnet_score_wf", how="left")
    # Reconcile
    df = df.with_columns(
        pl.when(pl.col('riskmeter_score_wf') > 0).then('wildfire_riskmeter_category').otherwise(pl.col('wildfire_catnet_category')).alias('wildfire_category')
    )

    # Fetch Exposure Curve
    df = loss_curve_lookup(hxd, df, wf_loss_curves_df, "tiv_region", "wildfire_curve_selected")

    # US Base Rates
    # Buildings
    us_base_rate_buildings_df = wf_us_cat_base_rates_df[["StateCounty", "WF Buildings"]]
    us_base_rate_buildings_df["WF Buildings"] = us_base_rate_buildings_df["WF Buildings"]*other_data['inflation']  # Adjust for inflation
    us_base_rate_buildings_pl = pl.from_pandas(us_base_rate_buildings_df).rename({"StateCounty": "state_county", "WF Buildings": "us_wildfire_buildings_base_rate"})
    us_base_rate_buildings_pl = us_base_rate_buildings_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_buildings_pl, on="state_county_lowercase", how="left")
    # Contents
    us_base_rate_contents_df = wf_us_cat_base_rates_df[["StateCounty", "WF Contents"]]
    us_base_rate_contents_df["WF Contents"] = us_base_rate_contents_df["WF Contents"]*other_data['inflation']
    us_base_rate_contents_pl = pl.from_pandas(us_base_rate_contents_df).rename({"StateCounty": "state_county", "WF Contents": "us_wildfire_contents_base_rate"})
    us_base_rate_contents_pl = us_base_rate_contents_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_contents_pl, on="state_county_lowercase", how="left")
    # BI
    us_base_rate_bi_df = wf_us_cat_base_rates_df[["StateCounty", "WF BI"]]
    us_base_rate_bi_df["WF BI"] = us_base_rate_bi_df["WF BI"]*other_data['inflation']
    us_base_rate_bi_pl = pl.from_pandas(us_base_rate_bi_df).rename({"StateCounty": "state_county", "WF BI": "us_wildfire_bi_base_rate"})
    us_base_rate_bi_pl = us_base_rate_bi_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_bi_pl, on="state_county_lowercase", how="left")

    # Intl Base Rates
    intl_base_rates_df = intl_base_rates_df[["Country", "WF"]]
    intl_base_rates_df["WF"] = intl_base_rates_df["WF"]*other_data['inflation']
    intl_base_rates_pl = pl.from_pandas(intl_base_rates_df).rename({"Country": "country", "WF": "intl_wildfire_buildings_base_rate"})
    intl_base_rates_pl = intl_base_rates_pl.with_columns(pl.col("country").str.to_lowercase().alias("country_lowercase")).drop("country")
    df = df.join(intl_base_rates_pl, on="country_lowercase", how="left")
    df = df.with_columns(
        pl.col('intl_wildfire_buildings_base_rate').alias('intl_wildfire_contents_base_rate'),
        pl.col('intl_wildfire_buildings_base_rate').alias('intl_wildfire_bi_base_rate')
    )

    # Choose correct country (US/Intr)
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_buildings_base_rate")).otherwise(pl.col("intl_wildfire_buildings_base_rate")).alias("wildfire_buildings_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_contents_base_rate")).otherwise(pl.col("intl_wildfire_contents_base_rate")).alias("wildfire_contents_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_bi_base_rate")).otherwise(pl.col("intl_wildfire_bi_base_rate")).alias("wildfire_bi_base_rate")
        )

    # Calcuate CatNet Score Cap
    catnet_score_cap_df = wf_us_cat_base_rates_df[["StateCounty", "WF CatNet Cap"]]
    catnet_score_cap_pl = pl.from_pandas(catnet_score_cap_df).rename({"StateCounty": "state_county", "WF CatNet Cap": "wildfire_catnet_score_cap"})
    catnet_score_cap_pl = catnet_score_cap_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(catnet_score_cap_pl, on="state_county_lowercase", how="left")

    # Calcuate CatNet Score Load
    df = df.with_columns(
        (
            pl.min(pl.col('catnet_score_wf'), pl.col('wildfire_catnet_score_cap').fill_null(10))
        ).alias("catnet_score_wf_intensity")   
    )
    catnet_score_df = catnet_score_df[["Intensity", "Load"]]
    catnet_score_pl = pl.from_pandas(catnet_score_df).rename({"Intensity": "catnet_score_wf_intensity", "Load": "catnet_score_wf_load_raw"})
    df = df.join(catnet_score_pl, on="catnet_score_wf_intensity", how="left")
    df = df.with_columns(
        (
            1 + pl.when(pl.col('riskmeter_score_wf') > 0).then(0).otherwise(pl.col('catnet_score_wf_load_raw'))
        ).alias("wildfire_catnet_score_load")
    )

    # Calculate RiskMeter Score Load
    riskmeter_score_df = riskmeter_score_df[["Score", "Load"]]
    riskmeter_score_pl = pl.from_pandas(riskmeter_score_df).rename({"Score": "riskmeter_score_wf", "Load":"wildfire_riskmeter_load"})
    df = df.join(riskmeter_score_pl, on="riskmeter_score_wf", how="left")
    df = df.with_columns(
        ((
            (pl.col("wildfire_riskmeter_load").ceil()/10).ceil()      # replicating excel's ROUNDUP(riskmeter_score_wf,-1)/10
        ).fill_null(0) + 1).alias("wildfire_riskmeter_load")
    )

    # Calcuate Occupancy Load
    # changed this to use Key instead of just Occupancy as different loads for the "Vacant" occupancy by Industry was causing duplication of schedule locations
    occupancy_load_df = non_cat_base_rates_df[["Key", "Wildfire Load"]]
    occupancy_load_pl = pl.from_pandas(occupancy_load_df).rename({"Key": "industry_occupancy", "Wildfire Load": "wildfire_occupancy_load"})
    df = df.join(occupancy_load_pl, on="industry_occupancy", how="left")
    df = df.with_columns(
            (
                1 + pl.col("wildfire_occupancy_load").fill_null(0)
            ).alias("wildfire_occupancy_load")
    )

    # Calcuate Construction Load
    construction_load_df = construction_load_df[["ISO", "Wildfire", "Construction"]]
    construction_load_pl = pl.from_pandas(construction_load_df).rename({"ISO": "constr_code", "Wildfire": "wildfire_construction_load"})
    df = df.join(construction_load_pl, on="constr_code", how="left")
    df = df.with_columns(
            (
                1 + pl.col("wildfire_construction_load").fill_null(0)
            ).alias("wildfire_construction_load")
    )

    # PC Code Rating Factor
    pc_code_df = pc_code_df[["PPC", "Wildfire"]]
    pc_code_pl = pl.from_pandas(pc_code_df).rename({"PPC": "pc_code", "Wildfire": "wildfire_pc_code_load"})
    df = df.join(pc_code_pl, on="pc_code", how="left")
    df = df.with_columns(
            (
                1 + pl.col("wildfire_pc_code_load").fill_null(0)
            ).alias("wildfire_pc_code_load")
    )

    # Size Discount Rating Factor

    # Load parameter tables
    loc_discount_df = hx.params.location_level_tiv
    acc_discount_df = hx.params.account_level_tiv
    # assign Discount Factors 
    total_acc_tiv = other_data["total_tiv_total_usd"]
    total_loc_tiv_df = df["tiv_total_usd"]

    wildfire_size_discount_load = size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, "wildfire")

    df = df.with_columns(pl.Series(name="wildfire_size_discount_load", values = wildfire_size_discount_load))


    # Total Rating Factor Adjustment
    df = df.with_columns(
        (
            pl.col('wildfire_catnet_score_load') * \
            pl.col('wildfire_riskmeter_load') * \
            pl.col('wildfire_occupancy_load') * \
            pl.col('wildfire_construction_load') * \
            pl.col('wildfire_pc_code_load') * \
            pl.col('wildfire_size_discount_load')    
        ).alias('us_wildfire_buildings_total_adjustment')
    )

    df = df.with_columns(
        pl.col('us_wildfire_buildings_total_adjustment').alias('us_wildfire_contents_total_adjustment')
    )
    
    df = df.with_columns(
        (((pl.col("tiv_bi")/pl.col("tiv_total")) * pl.col("bi_waiting_period_factor")) + (1 - (pl.col("tiv_bi")/pl.col("tiv_total")))).fill_nan(1).fill_null(1).alias("wildfire_bi_waiting_period_factor")
    )
    
    df = df.with_columns(
        (
            pl.col('us_wildfire_buildings_total_adjustment') * \
            pl.col('wildfire_bi_waiting_period_factor') * \
            other_data['bi_indemnity_period_factor'] * \
            other_data['cbi_load']
        ).alias('us_wildfire_bi_total_adjustment')
    )

    # US & Intl are separated out in the sheet but have identical values
    df = df.with_columns(
        pl.col('us_wildfire_buildings_total_adjustment').alias('intl_wildfire_buildings_total_adjustment'),
        pl.col('us_wildfire_contents_total_adjustment').alias('intl_wildfire_contents_total_adjustment'),
        pl.col('us_wildfire_bi_total_adjustment').alias('intl_wildfire_bi_total_adjustment')
    )

    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_buildings_total_adjustment")).otherwise(pl.col("intl_wildfire_buildings_total_adjustment")).alias("wildfire_buildings_total_adjustment"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_contents_total_adjustment")).otherwise(pl.col("intl_wildfire_contents_total_adjustment")).alias("wildfire_contents_total_adjustment"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_wildfire_bi_total_adjustment")).otherwise(pl.col("intl_wildfire_bi_total_adjustment")).alias("wildfire_bi_total_adjustment")
        )

    # Total Modifier Impact
    # Note same as BI above for both fire and wildfire. TODO: is this correct?
    df = df.with_columns(
        pl.col("wildfire_bi_total_adjustment").alias("wildfire_total_modifier_impact")
        )

    return df


def wildfire_hxd_assignment(hxd, df, other_data):
    '''
    Assign wildfire data to hxd
    '''
    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            ((df[f"wildfire_buildings_base_rate_layer{index}"] * df["tiv_buildings_usd"] +
                df[f"wildfire_contents_base_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                df[f"wildfire_bi_base_rate_layer{index}"] * df["tiv_bi_usd"]) / df["tiv_total_usd"])
                .fill_nan(0).alias(f"rate_base_total_wf_layer{index}")
        )

        df = df.with_columns(
            (
                (
                    df[f"wildfire_buildings_ground_up_uw_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"wildfire_contents_ground_up_uw_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"wildfire_bi_ground_up_uw_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_wf_layer{index}")
        )

    if hxd.policy_information.small_schedule_model:
        wf_catnet_score_list = df['wildfire_catnet_score_load'].to_list()
        wf_riskmeter_list = df['wildfire_riskmeter_load'].to_list()
        wf_occupancy_list = df['wildfire_occupancy_load'].to_list()
        wf_construction_list = df['wildfire_construction_load'].to_list()
        wf_pc_code_list = df['wildfire_pc_code_load'].to_list()
        wf_size_discount_list = df['wildfire_size_discount_load'].to_list()
        
        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_hazardscore_wf = wf_catnet_score_list[i]
            row.rfr_hazardscoreriskmeter_wf = wf_riskmeter_list[i]
            row.rfr_occ_wf = wf_occupancy_list[i]
            row.rfr_construction_wf = wf_construction_list[i]
            row.rfr_ppc_wf = wf_pc_code_list[i]
            row.rfr_sizedisc_wf = wf_size_discount_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            # Assign to schedule table
            wildfire_entry_perc_list = df[f"wildfire_entry_perc_layer{index}"].to_list()
            wildfire_exit_perc_list = df[f"wildfire_exit_perc_layer{index}"].to_list()
            wildfire_worth_percent_list = df[f"wildfire_worth_percent_layer{index}"].to_list()
            wf_el_pre_uw_list = df[f"wildfire_total_expected_loss_pre_uw_layer{index}"].to_list()
            wf_el_post_uw_list = df[f"wildfire_total_expected_loss_post_uw_layer{index}"].to_list()
            wf_tiv_exposed_list = df[f'wildfire_tiv_exposed_layer{index}'].to_list()

            wildfire_base_rate_list = df[f"rate_base_total_wf_layer{index}"].to_list()

            wildfire_ground_up_rate_list = df[f"rate_gu_total_wf_layer{index}"].to_list()


            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_wf = wildfire_entry_perc_list[i]
                target_output_by_layer.flc_exit_wf = wildfire_exit_perc_list[i]
                target_output_by_layer.flc_worth_wf = wildfire_worth_percent_list[i]
                target_output_by_layer.el_pre_uw_usd_100_wf = wf_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_wf = wf_el_post_uw_list[i]
                target_output_by_layer.tivexposed_total_usd_wf = wf_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_wf = wildfire_base_rate_list[i]
                target_output_by_layer.rate_gu_total_wf = wildfire_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            wf_el_pre_uw_list = df[f"wildfire_total_expected_loss_pre_uw_layer{index}"].to_list()
            wf_tiv_exposed_list = df[f'wildfire_tiv_exposed_layer{index}'].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_wf = wf_el_pre_uw_list[i]
                target_output_by_layer.tivexposed_total_usd_wf = wf_tiv_exposed_list[i]

    return df
