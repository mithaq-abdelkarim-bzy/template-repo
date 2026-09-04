import hx
import polars as pl
import numpy as np
from scipy import stats
from algorithms.analytical_curves import mbbefdg_pl
from algorithms.rating_common_functions import ground_up_rate, ground_up_uw_rate, loss_curve_lookup, \
    granularity_option_structure, deductible_option_structure, sublimit_option_structure, \
    percent_worth, expected_loss
from algorithms.analytical_curves import loss_curve, size_discount
from algorithms.us_rating_common_functions import us_entry_exit_tiv
from algorithms.intl_rating_common_functions import intl_base_rate_lookup, intl_base_rate, intl_entry_exit_tiv, intl_fire_deductible_fill


def hail_rating_calc(hxd, df, other_data):
    df = loss_curve_lookup(hxd, df, hx.params.ha_loss_curve_selection, "tiv_region", "hail_curve_selected")
    df = hail_rating_non_layer(hxd, df, other_data)

    for index, layer in enumerate(hxd.layers, start=1):
        df = hail_rating_layer(hxd, df, other_data, layer, index)

        df = ground_up_rate(hxd, df, other_data, layer, index, "hail")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "hail", "scs")

        df, granularity_pl = granularity_option_structure(hxd, df, other_data, layer, index, "scs", "scs", hx.params.scs_granularity_rank)
        df = deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, "scs", "scs", pl.col("tiv_region"), pl.col("count_region"))
        df = intl_fire_deductible_fill(hxd, df, layer, index, "hail", "scs")
        df = sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, "scs", "scs")
         
        # US Entry/Exit
        df = us_entry_exit_tiv(hxd, df, other_data, layer, index, "ha", "hail", "tiv_region", sublimit_peril="scs", deductible_peril="scs_us")
        df = df.rename({f"hail_entry_over_tiv_layer{index}": f"us_hail_entry_over_tiv_layer{index}", f"hail_exit_over_tiv_layer{index}": f"us_hail_exit_over_tiv_layer{index}"})

        # Intl Entry/Exit
        df = intl_entry_exit_tiv(hxd, df, other_data, layer, index, "scs", "hail", "tiv_region")
        df = df.with_columns(
            (pl.col(f"hail_entry_over_tiv_layer{index}") + pl.col(f"us_hail_entry_over_tiv_layer{index}")).alias(f"hail_entry_over_tiv_layer{index}"), 
            (pl.col(f"hail_exit_over_tiv_layer{index}") + pl.col(f"us_hail_exit_over_tiv_layer{index}")).alias(f"hail_exit_over_tiv_layer{index}")
        )
        df = df.drop(f"us_hail_entry_over_tiv_layer{index}", f"us_hail_exit_over_tiv_layer{index}")
       
       
        df = loss_curve(hxd, df, index, "hail")
        df = percent_worth(hxd, df, other_data, layer, index, "hail")
        df = expected_loss(hxd, df, other_data, layer, index, "hail")

        df = split_us_and_intl(hxd, df, other_data, layer, index)
    return df


def split_us_and_intl(hxd, df, other_data, layer, index):
    # Split out into US and Intl for later
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col(f"hail_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"hail_us_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") == "United States").then(pl.col(f"hail_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"hail_us_total_expected_loss_post_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"hail_total_expected_loss_pre_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"hail_intl_total_expected_loss_pre_uw_layer{index}"),
        pl.when(pl.col("country") != "United States").then(pl.col(f"hail_total_expected_loss_post_uw_layer{index}")).otherwise(pl.lit(0)).alias(f"hail_intl_total_expected_loss_post_uw_layer{index}"),
    )
    return df


def hail_rating_layer(hxd, df, other_data, layer, index):

    for col in ["hail_buildings_base_rate", "hail_contents_base_rate", "hail_bi_base_rate"]:
        df = df.with_columns(
            (pl.col(col) * pl.col(f"scs_covered_rating_layer{index}")).alias(col + f"_layer{index}")
        )

    df = df.with_columns(
        (pl.col(f"hail_buildings_base_rate_layer{index}") + pl.col(f"hail_contents_base_rate_layer{index}") + pl.col(f"hail_bi_base_rate_layer{index}")).alias(f"hail_total_base_rate_layer{index}")
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



def hail_rating_non_layer(hxd, df, other_data):
    ha_us_base_rates = hx.params.ha_us_base_rates
    ha_intl_base_rates = hx.params.intl_base_rates
    ha_us_occupancy = hx.params.ha_us_occupancy
    ha_intl_occupancy = hx.params.intl_occupancy_rating_factor
    non_cat_base_rates = hx.params.non_cat_base_rates
    ha_construction_load = hx.params.ha_construction_load
    ha_year_built = hx.params.ha_year_built
    hail_floor_area_us = hx.params.ha_floor_area_us
    hail_floor_area_intl = hx.params.ha_floor_area_intl
    ha_roof_age_conversion = hx.params.ha_roof_age_conversion
    roof_age = hx.params.roof_age
    roof_covering = hx.params.roof_covering
    roof_geometry = hx.params.roof_geometry
    ha_intl_catnet_score = hx.params.ha_catnet_score
    loc_discount_df = hx.params.location_level_tiv
    acc_discount_df = hx.params.account_level_tiv


    # US Base Rates
    # Buildings
    us_base_rate_buildings_df = ha_us_base_rates[["StateCounty", "HA Buildings"]]
    us_base_rate_buildings_df["HA Buildings"] = us_base_rate_buildings_df.loc[:, "HA Buildings"]*other_data['inflation']  # Adjust for inflation
    us_base_rate_buildings_pl = pl.from_pandas(us_base_rate_buildings_df).rename({"StateCounty": "state_county", "HA Buildings": "us_base_rate_ha_buildings"})
    us_base_rate_buildings_pl = us_base_rate_buildings_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_buildings_pl, on="state_county_lowercase", how="left")
    # Contents
    us_base_rate_contents_df = ha_us_base_rates[["StateCounty", "HA Contents"]]
    us_base_rate_contents_df["HA Contents"] = us_base_rate_contents_df.loc[:, "HA Contents"]*other_data['inflation']
    us_base_rate_contents_pl = pl.from_pandas(us_base_rate_contents_df).rename({"StateCounty": "state_county", "HA Contents": "us_base_rate_ha_contents"})
    us_base_rate_contents_pl = us_base_rate_contents_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_contents_pl, on="state_county_lowercase", how="left")
    # BI
    us_base_rate_bi_df = ha_us_base_rates[["StateCounty", "HA BI"]]
    us_base_rate_bi_df["HA BI"] = us_base_rate_bi_df.loc[:, "HA BI"]*other_data['inflation']
    us_base_rate_bi_pl = pl.from_pandas(us_base_rate_bi_df).rename({"StateCounty": "state_county", "HA BI": "us_base_rate_ha_bi"})
    us_base_rate_bi_pl = us_base_rate_bi_pl.with_columns(pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")).drop("state_county")
    df = df.join(us_base_rate_bi_pl, on="state_county_lowercase", how="left")

    # Intl Base Rates
    intl_base_rates_df = ha_intl_base_rates[["Country", "HA"]]
    intl_base_rates_df["HA"] = intl_base_rates_df.loc[:, "HA"]*other_data['inflation']
    intl_base_rates_pl = pl.from_pandas(intl_base_rates_df).rename({"Country": "country", "HA": "intl_base_rate_ha_buildings"})
    intl_base_rates_pl = intl_base_rates_pl.with_columns(pl.col("country").str.to_lowercase().alias("country_lowercase")).drop("country")
    df = df.join(intl_base_rates_pl, on="country_lowercase", how="left")
    df = df.with_columns(
        pl.col('intl_base_rate_ha_buildings').alias('intl_base_rate_ha_contents'),
        pl.col('intl_base_rate_ha_buildings').alias('intl_base_rate_ha_bi')
    )

    # Choose correct country (US/Intl)
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_ha_buildings")).otherwise(pl.col("intl_base_rate_ha_buildings")).alias("hail_buildings_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_ha_contents")).otherwise(pl.col("intl_base_rate_ha_contents")).alias("hail_contents_base_rate"),
        pl.when(pl.col("country") == "United States").then(pl.col("us_base_rate_ha_bi")).otherwise(pl.col("intl_base_rate_ha_bi")).alias("hail_bi_base_rate")
        )

    ### Rating Factors
    ## Occupancy
    # atc code
    non_cat_base_rates = non_cat_base_rates[["Key", "ATC Code"]]
    non_cat_base_rates_pl = pl.from_pandas(non_cat_base_rates).rename({"Key": "industry_occupancy", "ATC Code":"atc_code"})
    df = df.join(non_cat_base_rates_pl, on="industry_occupancy", how="left")

    # US
    ha_us_occupancy = ha_us_occupancy.melt(id_vars=["Country", "State Code"])
    ha_us_occupancy_pl = pl.from_pandas(ha_us_occupancy).rename({"Country": "country", "State Code": "state", "variable": "atc_code", "value": "hail_occupancy_load_us"})
    ha_us_occupancy_pl = ha_us_occupancy_pl.with_columns(
        pl.col("atc_code").cast(pl.Int64).alias("atc_code")
    )
    df = df.join(ha_us_occupancy_pl, on=["state", "atc_code"], how="left")

    # Intl
    ha_intl_occupancy = ha_intl_occupancy[["Occupancy", "Hail"]]
    ha_intl_occupancy_pl = pl.from_pandas(ha_intl_occupancy).rename({"Occupancy": "atc_code", "Hail": "hail_occupancy_load_intl"})
    df = df.join(ha_intl_occupancy_pl, on="atc_code", how="left")

    df = df.with_columns(
        (1 + pl.when(pl.col("country") == "United States").then(pl.col("hail_occupancy_load_us")).otherwise(pl.col("hail_occupancy_load_intl"))).fill_null(1).fill_nan(1).alias("hail_occupancy_load"),
    )

    ## Construction
    ha_construction_load = ha_construction_load[["ISO", "Hail"]]
    ha_construction_load_pl = pl.from_pandas(ha_construction_load).rename({"ISO": "constr_code", "Hail": "hail_construction_load"})
    df = df.join(ha_construction_load_pl, on="constr_code", how="left")
    df = df.with_columns(
        (1 + pl.col("hail_construction_load")).fill_null(1).fill_nan(1).alias("hail_construction_load")
    )

    ## Year Built
    ha_year_built_pl = pl.from_pandas(ha_year_built).rename({"Year Built": "year_built", "Hail": "hail_year_built_load"})
    df = df.with_columns(pl.col("year_built").fill_null(9999))
    df = df.sort("year_built")
    df = df.join_asof(ha_year_built_pl, on="year_built")
    df = df.with_columns(
        (1 + pl.when(pl.col("year_built") == 9999).then(0).otherwise(pl.col("hail_year_built_load"))).fill_null(1).fill_nan(1).alias("hail_year_built_load")
    )

    ## Floor Area
    df = df.with_columns(
        pl.when(pl.col("num_stories") == 0).then(0).otherwise(
            (pl.col("floor_area")/pl.col("num_stories")).fill_null(0)
        ).alias("avg_floor_area")
    )

    # US
    hail_floor_area_us_pl = pl.from_pandas(hail_floor_area_us).rename({"State Code": "state"})
    df = df.join(hail_floor_area_us_pl, on="state", how="left")
    df = df.with_columns(
        pl.lit(0).alias("hail_floor_area_load_us")
    )
    for cutoff in sorted([int(x) for x in list(hail_floor_area_us.columns) if x != "State Code"]):
        df = df.with_columns(
            pl.when(pl.col("avg_floor_area") >= cutoff).then(pl.col(str(cutoff))).otherwise(pl.col("hail_floor_area_load_us")).alias("hail_floor_area_load_us")
        )
        df.drop(str(cutoff))

    # Intl
    hail_floor_area_intl_pl = pl.from_pandas(hail_floor_area_intl).rename({"Area": "avg_floor_area", "Hail": "hail_floor_area_load_intl"})
    if not (df.shape[0] == 1 and df["avg_floor_area"].null_count() == 1):  # Default setting error catching
        df = df.sort("avg_floor_area")
        df = df.join_asof(hail_floor_area_intl_pl, on="avg_floor_area")

    df = df.with_columns(
        (1 + pl.when(pl.col("country") == "United States").then(pl.col("hail_floor_area_load_us")).otherwise(pl.col("hail_floor_area_load_intl"))).fill_null(1).fill_nan(1).alias("hail_floor_area_load"),
    )

    
    ## Roof Age
    # Roof Age is usually manually specified using "roof_age" input column in schedule data
    # If this column is blank, need to use the calculated roof age as below

    # For the calculated roof age:
    inception_year = hxd.hx_core.inception_date.year
    df = df.with_columns(pl.col("year_updated").cast(pl.Float64).fill_null(0).alias("year_updated"))
    df = df.with_columns(
        (
            inception_year - 
            pl.when(
                pl.col("year_updated") == 9999
            ).then(
                pl.col("year_built")
            ).when(
                pl.col("year_updated") > 0
            ).then(
                pl.col("year_updated")
            ).otherwise(
                pl.col("year_built")
            )
        ).alias("calculated_roof_age")
    )

    ha_roof_age_conversion_pl = pl.from_pandas(ha_roof_age_conversion).rename({"Lower Bound": "calculated_roof_age", "Age": "calculated_roof_age_category"})
    ha_roof_age_conversion_pl = ha_roof_age_conversion_pl.with_columns(pl.col("calculated_roof_age").cast(pl.Float64))
    if not (df.shape[0] == 1 and df["calculated_roof_age"].null_count() == 1):  # Default setting error catching
        df = df.sort("calculated_roof_age")
        df = df.join_asof(ha_roof_age_conversion_pl, on="calculated_roof_age")
    
    # Then determine which to use, calculated or input
    df = df.with_columns(
        pl.col("roof_age").fill_null(pl.col("calculated_roof_age_category")).alias("roof_age_category")
    )

    # Finally join on loads
    roof_age_pl = pl.from_pandas(roof_age).rename({"Age": "roof_age_category", "Load": "hail_roof_age_load"})
    df = df.join(roof_age_pl, on="roof_age_category", how="left")
    df = df.with_columns(
        (1 + pl.col("hail_roof_age_load")).fill_null(1).fill_nan(1).alias("hail_roof_age_load")
    )

    ## Roof Covering
    roof_covering_pl = pl.from_pandas(roof_covering).rename({"Covering": "roof_covering", "Load": "hail_roof_covering_load"})
    df = df.join(roof_covering_pl, on="roof_covering", how="left")
    df = df.with_columns(
        (1 + pl.col("hail_roof_covering_load")).fill_null(1).fill_nan(1).alias("hail_roof_covering_load")
    )

    ## Roof Geometry
    roof_geometry_pl = pl.from_pandas(roof_geometry).rename({"Geometry": "roof_geometry", "Load": "hail_roof_geometry_load"})
    df = df.join(roof_geometry_pl, on="roof_geometry", how="left")
    df = df.with_columns(
        (1 + pl.col("hail_roof_geometry_load")).fill_null(1).fill_nan(1).alias("hail_roof_geometry_load")
    )

    ## Intl Catnet Score
    ha_intl_catnet_score = ha_intl_catnet_score[["Score Band", "Load"]]
    ha_intl_catnet_score_pl = pl.from_pandas(ha_intl_catnet_score).rename({"Score Band": "catnet_score_ha", "Load": "hail_catnet_score_load"})
    df = df.join(ha_intl_catnet_score_pl, on="catnet_score_ha", how="left")
    df = df.with_columns(
        (1 + pl.when(pl.col("country") == "United States").then(pl.lit(0)).otherwise(pl.col("hail_catnet_score_load"))).fill_null(1).fill_nan(1).alias("hail_catnet_score_load"),
    )

    ## Size Discount
    total_acc_tiv = other_data["total_tiv_total_usd"]
    total_loc_tiv_df = df["tiv_total_usd"]
    
    hail_size_discount = size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, "hail")
    df =  df.with_columns(pl.Series(name="hail_size_discount_load", values = hail_size_discount))

    ## Total Rating Factor Adjustments
    df = df.with_columns(
        (
            pl.col('hail_occupancy_load') * \
            pl.col('hail_construction_load') * \
            pl.col('hail_year_built_load') * \
            pl.col('hail_floor_area_load') * \
            pl.col('hail_roof_age_load') * \
            pl.col('hail_roof_covering_load') * \
            pl.col('hail_roof_geometry_load') * \
            pl.col('hail_catnet_score_load') * \
            pl.col('hail_size_discount_load')
        ).alias('hail_buildings_total_adjustment')
    )

    df = df.with_columns(
        pl.col('hail_buildings_total_adjustment').alias('hail_contents_total_adjustment')
    )
    
    df = df.with_columns(
        (
            pl.col('hail_contents_total_adjustment') * \
            pl.col('bi_waiting_period_factor') * \
            other_data['bi_indemnity_period_factor'] * \
            other_data['cbi_load']
        ).alias('hail_bi_total_adjustment')
    )

    return df


def hail_hxd_assignment(hxd, df, other_data):
    '''
    Assign hail data to hxd
    '''
    if hxd.policy_information.small_schedule_model:
        hail_occupancy_list = df['hail_occupancy_load'].to_list()
        hail_construction_list = df['hail_construction_load'].to_list()
        hail_year_built_list = df['hail_year_built_load'].to_list()
        hail_floor_area_list = df['hail_floor_area_load'].to_list()
        hail_roof_age_list = df['hail_roof_age_load'].to_list()
        hail_roof_covering_list = df['hail_roof_covering_load'].to_list()
        hail_roof_geometry_list = df['hail_roof_geometry_load'].to_list()
        hail_catnet_score_list = df['hail_catnet_score_load'].to_list()
        hail_size_discount_list=df['hail_size_discount_load'].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_occ_ha = hail_occupancy_list[i]
            row.rfr_construction_ha = hail_construction_list[i]
            row.rfr_yearbuilt_ha = hail_year_built_list[i]
            row.rfr_floorarea_ha = hail_floor_area_list[i]
            row.rfr_roofage_ha = hail_roof_age_list[i]
            row.rfr_roofcovering_ha = hail_roof_covering_list[i]
            row.rfr_roofgeometry_ha = hail_roof_geometry_list[i]
            row.rfr_hazardscore_ha = hail_catnet_score_list[i]
            row.rfr_sizedisc_ha = hail_size_discount_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            hail_entry_perc_list = df[f"hail_entry_perc_layer{index}"].to_list()
            hail_exit_perc_list = df[f"hail_exit_perc_layer{index}"].to_list()
            hail_worth_percent_list = df[f"hail_worth_percent_layer{index}"].to_list()
            hail_el_pre_uw_list = df[f"hail_total_expected_loss_pre_uw_layer{index}"].to_list()
            hail_el_post_uw_list = df[f"hail_total_expected_loss_post_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_ha = hail_entry_perc_list[i]
                target_output_by_layer.flc_exit_ha = hail_exit_perc_list[i]
                target_output_by_layer.flc_worth_ha = hail_worth_percent_list[i]
                target_output_by_layer.el_pre_uw_usd_100_ha = hail_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_ha = hail_el_post_uw_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            hail_el_pre_uw_list = df[f"hail_total_expected_loss_pre_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]
                target_output_by_layer.el_pre_uw_usd_100_ha = hail_el_pre_uw_list[i]

    return df
