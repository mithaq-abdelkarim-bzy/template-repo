import hx
import polars as pl
import numpy as np
from scipy import stats
from algorithms.analytical_curves import loss_curve, mbbefdg_pl, size_discount
from algorithms.rating_common_functions import ground_up_rate, ground_up_uw_rate, loss_curve_lookup, \
    granularity_option_structure, deductible_option_structure, sublimit_option_structure, \
    percent_worth, expected_loss
from algorithms.us_rating_common_functions import us_entry_exit_tiv
from algorithms.intl_rating_common_functions import intl_base_rate_lookup, intl_base_rate, intl_entry_exit_tiv, intl_fire_deductible_fill


def tornado_rating_calc(hxd, df, other_data):
    df = loss_curve_lookup(hxd, df, hx.params.tn_loss_curve_selection, "tiv_region", "tornado_curve_selected")
    df = tornado_rating_non_layer(hxd, df, other_data)

    for index, layer in enumerate(hxd.layers, start=1):
        df = tornado_rating_layer(hxd, df, other_data, layer, index)

        df = ground_up_rate(hxd, df, other_data, layer, index, "tornado")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "tornado", "scs")

        df, granularity_pl = granularity_option_structure(hxd, df, other_data, layer, index, "scs", "scs", hx.params.scs_granularity_rank)
        df = deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, "scs", "scs", pl.col("tiv_region"), pl.col("count_region"))
        df = intl_fire_deductible_fill(hxd, df, layer, index, "tornado", "scs")
        df = sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, "scs", "scs")

        # US Entry/Exit
        df = us_entry_exit_tiv(hxd, df, other_data, layer, index, "tn", "tornado", "tiv_region", sublimit_peril="scs", deductible_peril="scs_us")
        df = df.rename({f"tornado_entry_over_tiv_layer{index}": f"us_tornado_entry_over_tiv_layer{index}", f"tornado_exit_over_tiv_layer{index}": f"us_tornado_exit_over_tiv_layer{index}"})
        
        # Intl Entry/Exit
        df = intl_entry_exit_tiv(hxd, df, other_data, layer, index, "scs", "tornado", "tiv_region")
        df = df.with_columns(
            (pl.col(f"tornado_entry_over_tiv_layer{index}") + pl.col(f"us_tornado_entry_over_tiv_layer{index}")).alias(f"tornado_entry_over_tiv_layer{index}"), 
            (pl.col(f"tornado_exit_over_tiv_layer{index}") + pl.col(f"us_tornado_exit_over_tiv_layer{index}")).alias(f"tornado_exit_over_tiv_layer{index}")
        )
        df = df.drop(f"us_tornado_entry_over_tiv_layer{index}", f"us_tornado_exit_over_tiv_layer{index}")
        
        df = loss_curve(hxd, df, index, "tornado")
        df = percent_worth(hxd, df, other_data, layer, index, "tornado")
        df = expected_loss(hxd, df, other_data, layer, index, "tornado")

        df = split_us_and_intl(hxd, df, other_data, layer, index)
    
    return df


def split_us_and_intl(hxd, df, other_data, layer, index):
    # Split out into US and Intl for later
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col(f"tornado_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"tornado_us_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") == "United States").then(pl.col(f"tornado_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"tornado_us_total_expected_loss_post_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"tornado_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"tornado_intl_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"tornado_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"tornado_intl_total_expected_loss_post_uw_layer{index}"),
    )
    return df


def tornado_rating_layer(hxd, df, other_data, layer, index):
    flc_df = hx.params.flc
    exposure_curve_parameters_df = hx.params.exposure_curve_parameters
    assumption_1_in_250_pricing_df = hx.params.assumption_1_in_250_pricing
    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team


    for col in ["tornado_buildings_base_rate", "tornado_contents_base_rate", "tornado_bi_base_rate"]:
        df = df.with_columns(
            (pl.col(col) * pl.col(f"scs_covered_rating_layer{index}")).alias(col + f"_layer{index}")
        )

    df = df.with_columns(
        (pl.col(f"tornado_buildings_base_rate_layer{index}") + pl.col(f"tornado_contents_base_rate_layer{index}") + pl.col(f"tornado_bi_base_rate_layer{index}")).alias(f"tornado_total_base_rate_layer{index}")
    )

    return df

    
def tiv_country_table(hxd):

    # Load parameter tables
    intl_country_tiv_string = hx.params.intl_country_tiv_list['country_tiv_list'].iloc[0]
    intl_country_tiv_list = intl_country_tiv_string.replace(", ", ",").split(",")
    intl_country_tiv_list = [x.split("%") for x in intl_country_tiv_list]
    intl_country_tiv_list = [x for x in intl_country_tiv_list if x != ['']]

    intl_country_tiv_pl = pl.DataFrame(intl_country_tiv_list, orient="row").rename(
        {
            "column_1": "country",
            "column_2": "tiv_country"
        }
    ).drop("column_0")

    intl_country_tiv_pl = intl_country_tiv_pl.with_columns(pl.col("tiv_country").str.strip().cast(pl.Float64).alias("tiv_country"))
    intl_country_tiv_pl = intl_country_tiv_pl.with_columns(pl.col("country").str.to_lowercase().alias("country_lowercase")).drop("country")
    return intl_country_tiv_pl

def tornado_rating_non_layer(hxd, df, other_data):
    tn_us_cat_base_rates = hx.params.tn_us_cat_base_rates
    tn_catnet_score = hx.params.tn_catnet_score
    intl_base_rates = hx.params.intl_base_rates
    tn_us_occupancy_score = hx.params.tn_us_occupancy_score
    intl_occupancy_rating_factor = hx.params.intl_occupancy_rating_factor
    tn_loss_curve_selection = hx.params.tn_loss_curve_selection
    tn_us_construction_score = hx.params.tn_us_construction_score
    tn_us_year_built = hx.params.tn_us_year_built
    intl_year_built_rating_factor = hx.params.intl_year_built_rating_factor
    non_cat_base_rates = hx.params.non_cat_base_rates
    loc_discount_df = hx.params.location_level_tiv
    acc_discount_df = hx.params.account_level_tiv



    # US Base Rates
    # Buildings
    us_base_rates_buildings_df = tn_us_cat_base_rates[["StateCounty", "TN Buildings"]]
    us_base_rates_buildings_df["TN Buildings"] = us_base_rates_buildings_df.loc[:, "TN Buildings"]*other_data['inflation']  # Adjust for inflation
    us_base_rates_buildings_pl = pl.from_pandas(us_base_rates_buildings_df).rename({"StateCounty": "state_county", "TN Buildings": "us_base_rate_tn_buildings"})
    us_base_rates_buildings_pl = us_base_rates_buildings_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rates_buildings_pl, on="state_county_lowercase", how="left")
    # Contents
    us_base_rate_contents_df = tn_us_cat_base_rates[["StateCounty", "TN Contents"]]
    us_base_rate_contents_df["TN Contents"] = us_base_rate_contents_df.loc[:, "TN Contents"]*other_data['inflation']
    us_base_rate_contents_pl = pl.from_pandas(us_base_rate_contents_df).rename({"StateCounty": "state_county", "TN Contents": "us_base_rate_tn_contents"})
    us_base_rate_contents_pl = us_base_rate_contents_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_contents_pl, on="state_county_lowercase", how="left")
    # BI
    us_base_rate_bi_df = tn_us_cat_base_rates[["StateCounty", "TN BI"]]
    us_base_rate_bi_df["TN BI"] = us_base_rate_bi_df.loc[:, "TN BI"]*other_data['inflation']
    us_base_rate_bi_pl = pl.from_pandas(us_base_rate_bi_df).rename({"StateCounty": "state_county", "TN BI": "us_base_rate_tn_bi"})
    us_base_rate_bi_pl = us_base_rate_bi_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_bi_pl, on="state_county_lowercase", how="left")

    # Intl Base Rates
    intl_base_rates_df = intl_base_rates[["Country", "TN"]]
    intl_base_rates_df["TN"] = intl_base_rates_df.loc[: ,"TN"]*other_data['inflation']
    intl_base_rates_pl = pl.from_pandas(intl_base_rates_df).rename({"Country": "country", "TN": "intl_base_rate_tn_buildings"})
    intl_base_rates_pl = intl_base_rates_pl.with_columns(pl.col("country").str.to_lowercase().alias("country_lowercase")).drop("country")
    df = df.join(intl_base_rates_pl, on="country_lowercase", how="left")
    df = df.with_columns(
        pl.col('intl_base_rate_tn_buildings').alias('intl_base_rate_tn_contents'),
        pl.col('intl_base_rate_tn_buildings').alias('intl_base_rate_tn_bi')
    )

    # Choose correct country (US/Intl)
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_tn_buildings")).otherwise(pl.col("intl_base_rate_tn_buildings")).alias("tornado_buildings_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_tn_contents")).otherwise(pl.col("intl_base_rate_tn_contents")).alias("tornado_contents_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_tn_bi")).otherwise(pl.col("intl_base_rate_tn_bi")).alias("tornado_bi_base_rate")
        )

    
    ### Rating Factors
    ## Occupancy
    # atc code already populated in hail

    # US
    tn_us_occupancy_score = tn_us_occupancy_score[[x for x in tn_us_occupancy_score.columns if x not in ["Country", "State", "County"]]]
    tn_us_occupancy_score = tn_us_occupancy_score.melt(id_vars=["StateCounty"])
    tn_us_occupancy_pl = pl.from_pandas(tn_us_occupancy_score).rename({"StateCounty": "state_county_lowercase", "variable": "atc_code", "value": "tornado_occupancy_load_us"})
    tn_us_occupancy_pl = tn_us_occupancy_pl.with_columns(
        pl.col("state_county_lowercase").str.to_lowercase().alias("state_county_lowercase"),
        pl.col("atc_code").cast(pl.Int64).alias("atc_code")
    )
    df = df.join(tn_us_occupancy_pl, on=["state_county_lowercase", "atc_code"], how="left")

    # Intl
    tn_intl_occupancy = intl_occupancy_rating_factor[["Occupancy", "Tornado"]]
    tn_intl_occupancy_pl = pl.from_pandas(tn_intl_occupancy).rename({"Occupancy": "atc_code", "Tornado": "tornado_occupancy_load_intl"})
    df = df.join(tn_intl_occupancy_pl, on="atc_code", how="left")

    df = df.with_columns(
        (1 + pl.when(pl.col("country") == "United States").then(pl.col("tornado_occupancy_load_us")).otherwise(pl.col("tornado_occupancy_load_intl"))).fill_null(1).fill_nan(1).alias("tornado_occupancy_load"),
    )

    ## Construction
    # US
    tn_us_construction_score = tn_us_construction_score[[x for x in tn_us_construction_score.columns if x not in ["Country", "State", "County"]]]
    tn_us_construction_score = tn_us_construction_score.melt(id_vars=["StateCounty"])
    tn_us_construction_score_pl = pl.from_pandas(tn_us_construction_score).rename({"StateCounty": "state_county_lowercase", "variable": "constr_code", "value": "tornado_us_construction_load"})
    tn_us_construction_score_pl = tn_us_construction_score_pl.with_columns(
        pl.col("state_county_lowercase").str.to_lowercase().alias("state_county_lowercase"),
        pl.col("constr_code").cast(pl.Int64).alias("constr_code")
    )
    df = df.join(tn_us_construction_score_pl, on=["state_county_lowercase", "constr_code"], how="left")

    # Intl - use WS construction load
    df = df.with_columns(
        (pl.when(pl.col("country") == "United States").then(1 + pl.col("tornado_us_construction_load")
        ).otherwise(pl.col("ws_construction_factor"))).fill_null(1).fill_nan(1).alias("tornado_construction_load")
    )

    ## Year Built
    # US
    tn_us_year_built = tn_us_year_built[[x for x in tn_us_year_built.columns if x not in ["Country", "State", "County"]]]
    tn_us_year_built_pl = pl.from_pandas(tn_us_year_built).rename({"StateCounty": "state_county"})
    tn_us_year_built_pl = tn_us_year_built_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")
    df = df.join(tn_us_year_built_pl, on="state_county_lowercase", how="left")
    df = df.with_columns(
        pl.lit(0).alias("tornado_us_year_built_load")
    )
    for cutoff in sorted([int(x) for x in list(tn_us_year_built.columns) if x != "StateCounty"]):
        df = df.with_columns(
            pl.when(pl.col("year_built") >= cutoff).then(pl.col(str(cutoff))).otherwise(pl.col("tornado_us_year_built_load")).alias("tornado_us_year_built_load")
        )
        df.drop(str(cutoff))

    # Intl
    intl_year_built_rating_factor = intl_year_built_rating_factor[["Year", "Tornado"]]
    intl_year_built_rating_factor_pl = pl.from_pandas(intl_year_built_rating_factor).rename({"Year": "year_built", "Tornado": "tornado_intl_year_built_load"})
    df = df.sort("year_built")
    df = df.join_asof(intl_year_built_rating_factor_pl, on="year_built")
    df = df.sort("row_nr")
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col("tornado_us_year_built_load")).otherwise(pl.col("tornado_intl_year_built_load")).fill_null(0).alias("tornado_year_built_load"),
    )
    df = df.with_columns(
        (1 + pl.when(pl.col("year_built") == 9999).then(0).otherwise(pl.col("tornado_year_built_load"))).alias("tornado_year_built_load")
    )

    
    ## Intl Catnet Score
    tn_catnet_score = tn_catnet_score[["Score Band", "Load"]]
    tn_catnet_score_pl = pl.from_pandas(tn_catnet_score).rename({"Score Band": "catnet_score_tn", "Load": "tornado_catnet_score_load"})
    df = df.join(tn_catnet_score_pl, on="catnet_score_tn", how="left")
    df = df.with_columns(
        (1 + pl.when(pl.col("country") == "United States").then(pl.lit(0)).otherwise(pl.col("tornado_catnet_score_load"))).fill_null(1).fill_nan(1).alias("tornado_catnet_score_load"),
    )

    ## Size discount
    total_acc_tiv = other_data["total_tiv_total_usd"]
    total_loc_tiv_df = df["tiv_total_usd"]
    
    tornado_size_discount = size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, "tornado")
    df =  df.with_columns(pl.Series(name="tornado_size_discount_load", values = tornado_size_discount))

    ## Total Rating Factor Adjustments
    df = df.with_columns(
        (
            pl.col('tornado_occupancy_load') * \
            pl.col('tornado_construction_load') * \
            pl.col('tornado_year_built_load') * \
            pl.col('tornado_catnet_score_load') * \
            pl.col('tornado_size_discount_load')
        ).alias('tornado_buildings_total_adjustment')
    )

    df = df.with_columns(
        pl.col('tornado_buildings_total_adjustment').alias('tornado_contents_total_adjustment')
    )
    
    df = df.with_columns(
        (
            pl.col('tornado_contents_total_adjustment') * \
            pl.col('bi_waiting_period_factor') * \
            other_data['bi_indemnity_period_factor'] * \
            other_data['cbi_load']
        ).alias('tornado_bi_total_adjustment')
    )

    return df


def tornado_hxd_assignment(hxd, df, other_data):
    '''
    Assign tornado data to hxd
    '''
    if hxd.policy_information.small_schedule_model:
        tornado_occupancy_list = df['tornado_occupancy_load'].to_list()
        tornado_construction_list = df['tornado_construction_load'].to_list()
        tornado_year_built_list = df['tornado_year_built_load'].to_list()
        tornado_catnet_score_list = df['tornado_catnet_score_load'].to_list()
        tornado_size_discount_list = df['tornado_size_discount_load'].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_occ_tn = tornado_occupancy_list[i]
            row.rfr_construction_tn = tornado_construction_list[i]
            row.rfr_yearbuilt_tn = tornado_year_built_list[i]
            row.rfr_hazardscore_tn = tornado_catnet_score_list[i]
            row.rfr_sizedisc_tn = tornado_size_discount_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            # Assign to schedule table
            tornado_entry_perc_list = df[f"tornado_entry_perc_layer{index}"].to_list()
            tornado_exit_perc_list = df[f"tornado_exit_perc_layer{index}"].to_list()
            tornado_worth_percent_list = df[f"tornado_worth_percent_layer{index}"].to_list()
            tornado_el_pre_uw_list = df[f"tornado_total_expected_loss_pre_uw_layer{index}"].to_list()
            tornado_el_post_uw_list = df[f"tornado_total_expected_loss_post_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_tn =  tornado_entry_perc_list[i]
                target_output_by_layer.flc_exit_tn =  tornado_exit_perc_list[i]
                target_output_by_layer.flc_worth_tn =  tornado_worth_percent_list[i]
                target_output_by_layer.el_pre_uw_usd_100_tn =  tornado_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_tn =  tornado_el_post_uw_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            tornado_el_pre_uw_list = df[f"tornado_total_expected_loss_pre_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_tn = tornado_el_pre_uw_list[i]
                
    return df