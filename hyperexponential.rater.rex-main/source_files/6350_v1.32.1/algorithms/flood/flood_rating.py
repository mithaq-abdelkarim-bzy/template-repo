import hx
import polars as pl
from algorithms.flood.flood_rating_factor import flood_rating_factor, flood_us_total_adjustment, flood_intl_total_adjustment
from algorithms.flood.flood_us_rating import flood_us_base_rate_lookup, flood_us_base_rate
from algorithms.rating_common_functions import (loss_curve_lookup, ground_up_rate, ground_up_uw_rate,
    granularity_option_structure, deductible_option_structure, sublimit_option_structure,
    expected_loss, percent_worth)
from algorithms.intl_rating_common_functions import intl_base_rate_lookup, intl_base_rate, intl_entry_exit_tiv, intl_fire_deductible_fill
from algorithms.us_rating_common_functions import us_entry_exit_tiv
from algorithms.analytical_curves import loss_curve

def flood_us_rating_calc(hxd, df, other_data):
    '''
    Calculates US flood rating
    '''

    df = flood_rating_factor(hxd, df, other_data)
    df = flood_us_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = flood_us_base_rate_lookup(hxd, df, other_data)
    df = loss_curve_lookup(hxd, df, hx.params.fl_loss_curve_selection, "tiv_region", "flood_us_curve_selected")

    for index, layer in enumerate(hxd.layers, start=1):
        df = flood_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl)
        df = ground_up_rate(hxd, df, other_data, layer, index, "flood_us")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "flood_us", "fl")
        df, granularity_pl = granularity_option_structure(hxd, df, other_data, layer, index, "fl", "flood",
                hx.params.fl_granularity_rank)
        df = deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, "fl", "flood",
                pl.col("tiv_region"), pl.col("count_region"))        
        df = sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, "fl", "flood")
        df = us_entry_exit_tiv(hxd, df, other_data, layer, index, "fl", "flood_us", "tiv_region")
        df = loss_curve(hxd, df, index, "flood_us")
        df = percent_worth(hxd, df, other_data, layer, index, "flood_us")
        df = expected_loss(hxd, df, other_data, layer, index, "flood_us")
    
    del base_rate_pl
    return df


def flood_intl_rating_calc(hxd, df, other_data):
    '''
    Calculates international flood rating
    '''

    df = flood_intl_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = intl_base_rate_lookup(hxd, df, other_data, "FL", "flood")
    df = loss_curve_lookup(hxd, df, hx.params.fl_loss_curve_selection, "tiv_region", "flood_intl_curve_selected")

    for index, layer in enumerate(hxd.layers, start=1):
        df = intl_fire_deductible_fill(hxd, df, layer, index, "flood", "flood", short_peril_struct_name="fl")
        df = intl_base_rate(hxd, df, other_data, layer, index, base_rate_pl, "flood", "fl")
        df = ground_up_rate(hxd, df, other_data, layer, index, "flood_intl")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "flood_intl", "fl")
        df = intl_entry_exit_tiv(hxd, df, other_data, layer, index, "fl", "flood_intl", "tiv_region")
        df = loss_curve(hxd, df, index, "flood_intl")
        df = percent_worth(hxd, df, other_data, layer, index, "flood_intl")
        df = expected_loss(hxd, df, other_data, layer, index, "flood_intl")

    return df


def flood_hxd_assignment(hxd, df, other_data):
    '''
    Assign flood data to hxd
    '''
    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_entry_perc_layer{index}"))
                .otherwise(pl.col(f"flood_intl_entry_perc_layer{index}"))
                .alias(f"flood_entry_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_exit_perc_layer{index}"))
                .otherwise(pl.col(f"flood_intl_exit_perc_layer{index}"))
                .alias(f"flood_exit_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_worth_percent_layer{index}"))
                .otherwise(pl.col(f"flood_intl_worth_percent_layer{index}"))
                .alias(f"flood_worth_percent_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_total_expected_loss_pre_uw_layer{index}"))
                .otherwise(pl.col(f"flood_intl_total_expected_loss_pre_uw_layer{index}"))
                .alias(f"flood_total_expected_loss_pre_uw_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_total_expected_loss_post_uw_layer{index}"))
                .otherwise(pl.col(f"flood_intl_total_expected_loss_post_uw_layer{index}"))
                .alias(f"flood_total_expected_loss_post_uw_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_tiv_exposed_layer{index}"))
                .otherwise(pl.col(f"flood_intl_tiv_exposed_layer{index}"))
                .alias(f"flood_tiv_exposed_layer{index}")
        )

        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(
                    (
                        pl.col(f"flood_us_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"flood_us_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"flood_us_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .otherwise(
                    (
                        pl.col(f"flood_intl_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"flood_intl_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"flood_intl_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .fill_nan(0).alias(f"rate_base_total_fl_layer{index}")
        )

        df = df.with_columns(
            (
                (
                    df[f"flood_us_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"flood_us_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"flood_us_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"] +
                    df[f"flood_intl_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"flood_intl_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"flood_intl_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_fl_layer{index}")
        )

    if hxd.policy_information.small_schedule_model:
        fl_katrisk_risk_rating_list = df['fl_katrisk_risk_rating_factor'].to_list()
        fl_construction_rating_list = df['fl_construction_rating_factor'].to_list()
        fl_num_floors_rating_list = df['fl_num_floors_rating_factor'].to_list()
        fl_basement_rating_list = df['fl_basement_rating_factor'].to_list()
        fl_elevation_rating_list = df['fl_elevation_rating_factor'].to_list()
        fl_catnet_score_list = df['fl_catnet_rating_factor'].to_list()
        fl_size_discount_list = df['fl_size_discount_rating_factor'].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_katriskscore_fl = fl_katrisk_risk_rating_list[i]
            row.rfr_construction_fl = fl_construction_rating_list[i]
            row.rfr_nofloors_fl = fl_num_floors_rating_list[i]
            row.rfr_basement_fl = fl_basement_rating_list[i]
            row.rfr_elevation_fl = fl_elevation_rating_list[i]
            row.rfr_hazardscore_fl = fl_catnet_score_list[i]
            row.rfr_sizedisc_fl = fl_size_discount_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            # Assign to schedule table
            flood_entry_perc_list = df[f"flood_entry_perc_layer{index}"].to_list()
            flood_exit_perc_list = df[f"flood_exit_perc_layer{index}"].to_list()
            flood_worth_percent_list = df[f"flood_worth_percent_layer{index}"].to_list()
            flood_el_pre_uw_list = df[f"flood_total_expected_loss_pre_uw_layer{index}"].to_list()
            flood_el_post_uw_list = df[f"flood_total_expected_loss_post_uw_layer{index}"].to_list()
            fl_ded_usd = df[f"fl_deductible_selected_layer{index}"].to_list()
            fl_sublimit_usd = df[f"fl_selected_sublimit_layer{index}"].to_list()
            fl_tiv_exposed_list = df[f"flood_tiv_exposed_layer{index}"].to_list()

            flood_base_rate_list = df[f"rate_base_total_fl_layer{index}"].to_list()

            flood_ground_up_rate_list = df[f"rate_gu_total_fl_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_fl = flood_entry_perc_list[i]
                target_output_by_layer.flc_exit_fl = flood_exit_perc_list[i]
                target_output_by_layer.flc_worth_fl = flood_worth_percent_list[i]
                target_output_by_layer.el_pre_uw_usd_100_fl = flood_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_fl = flood_el_post_uw_list[i]
                target_output_by_layer.deductible_usd_fl = fl_ded_usd[i]
                target_output_by_layer.sublimit_usd_fl = fl_sublimit_usd[i]
                target_output_by_layer.tivexposed_total_usd_fl = fl_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_fl = flood_base_rate_list[i]
                target_output_by_layer.rate_gu_total_fl = flood_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            flood_el_pre_uw_list = df[f"flood_total_expected_loss_pre_uw_layer{index}"].to_list()
            fl_ded_usd = df[f"fl_deductible_selected_layer{index}"].to_list()
            fl_tiv_exposed_list = df[f"flood_tiv_exposed_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_fl = flood_el_pre_uw_list[i]
                target_output_by_layer.deductible_usd_fl = fl_ded_usd[i]
                target_output_by_layer.tivexposed_total_usd_fl = fl_tiv_exposed_list[i]

    return df
