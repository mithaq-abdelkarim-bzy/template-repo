import hx
import polars as pl
from algorithms.earthquake.earthquake_rating_factor import earthquake_rating_factor, earthquake_us_total_adjustment, earthquake_intl_total_adjustment
from algorithms.earthquake.earthquake_us_rating import earthquake_us_base_rate_lookup, earthquake_us_base_rate
from algorithms.rating_common_functions import ground_up_rate, ground_up_uw_rate, loss_curve_lookup, \
    granularity_option_structure, deductible_option_structure, sublimit_option_structure, \
    percent_worth, expected_loss
from algorithms.intl_rating_common_functions import intl_base_rate_lookup, intl_base_rate, intl_entry_exit_tiv
from algorithms.us_rating_common_functions import us_entry_exit_tiv
from algorithms.analytical_curves import loss_curve


def earthquake_us_rating_calc(hxd, df, other_data):
    '''
    Calculates US earthquake Rating
    '''

    df = earthquake_rating_factor(hxd, df, other_data)
    df = earthquake_us_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = earthquake_us_base_rate_lookup(hxd, df, other_data)
    df = loss_curve_lookup(hxd, df, hx.params.eq_loss_curve_selection, "tiv_eq_gate", "earthquake_us_curve_selected")
    
    for index, layer in enumerate(hxd.layers, start=1):
        df = earthquake_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl)
        df = ground_up_rate(hxd, df, other_data, layer, index, "earthquake_us")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "earthquake_us", "eq")
        df, granularity_pl = granularity_option_structure(hxd, df, other_data, layer, index, "eq", "quake",
                hx.params.eq_granularity_rank)
        df = deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, "eq", "quake",
                pl.col("tiv_eq_gate"), pl.col("count_eq_gate"))
        df = sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, "eq", "quake")
        df = us_entry_exit_tiv(hxd, df, other_data, layer, index, "eq", "earthquake_us", "tiv_eq_gate")
        df = loss_curve(hxd, df, index, "earthquake_us")
        df = percent_worth(hxd, df, other_data, layer, index, "earthquake_us")
        df = expected_loss(hxd, df, other_data, layer, index, "earthquake_us")
    
    del base_rate_pl

    return df


def earthquake_intl_rating_calc(hxd, df, other_data):
    '''
    Calculates International Earthquake Rating
    '''

    df = earthquake_intl_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = intl_base_rate_lookup(hxd, df, other_data, "EQ", "earthquake")
    df = loss_curve_lookup(hxd, df, hx.params.eq_loss_curve_selection, "tiv_region", "earthquake_intl_curve_selected")
        
    for index, layer in enumerate(hxd.layers, start=1):
        df = intl_base_rate(hxd, df, other_data, layer, index, base_rate_pl, "earthquake", "eq")
        df = ground_up_rate(hxd, df, other_data, layer, index, "earthquake_intl")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "earthquake_intl", "eq")
        df = intl_entry_exit_tiv(hxd, df, other_data, layer, index, "eq", "earthquake_intl", "tiv_region")
        df = loss_curve(hxd, df, index, "earthquake_intl")
        df = percent_worth(hxd, df, other_data, layer, index, "earthquake_intl")
        df = expected_loss(hxd, df, other_data, layer, index, "earthquake_intl")

    del base_rate_pl

    return df


def earthquake_expected_loss_calc(hxd, df, other_data):
    '''
    Calculate expected loss based on (US + CA) or non CA
    '''

    for index, layer in enumerate(hxd.layers, start=1):
        earthquake_pl = df[["country", 
                            f"earthquake_us_total_expected_loss_pre_uw_layer{index}",
                            f"earthquake_intl_total_expected_loss_pre_uw_layer{index}",
                            f"earthquake_us_total_expected_loss_post_uw_layer{index}",
                            f"earthquake_intl_total_expected_loss_post_uw_layer{index}",
                        ]]


        df = df.with_columns(
            earthquake_pl.select(
                [
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"earthquake_us_total_expected_loss_pre_uw_layer{index}"))
                        .when(pl.col("country") == "Canada")
                        .then(pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"))
                        .otherwise(0)
                        .alias(f"earthquake_us_total_expected_loss_pre_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"earthquake_us_total_expected_loss_post_uw_layer{index}"))
                        .when(pl.col("country") == "Canada")
                        .then(pl.col(f"earthquake_intl_total_expected_loss_post_uw_layer{index}"))
                        .otherwise(0)
                        .alias(f"earthquake_us_total_expected_loss_post_uw_layer{index}"),
                    pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                        .then(0)
                        .otherwise(pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"))
                        .alias(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"),
                    pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                        .then(0)
                        .otherwise(pl.col(f"earthquake_intl_total_expected_loss_post_uw_layer{index}"))
                        .alias(f"earthquake_intl_total_expected_loss_post_uw_layer{index}"),
                ]
            )
        )

    return df


def earthquake_hxd_assignment(hxd, df, other_data):
    '''
    Assign earthquake data to hxd
    '''
    for index, layer in enumerate(hxd.layers, start=1):
        # Assign to schedule table
        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"earthquake_us_entry_perc_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_entry_perc_layer{index}"))
                .alias(f"earthquake_entry_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"earthquake_us_exit_perc_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_exit_perc_layer{index}"))
                .alias(f"earthquake_exit_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"earthquake_us_worth_percent_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_worth_percent_layer{index}"))
                .alias(f"earthquake_worth_percent_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"earthquake_us_tiv_exposed_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_tiv_exposed_layer{index}"))
                .alias(f"earthquake_tiv_exposed_layer{index}")
        )

        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(
                    (
                        pl.col(f"earthquake_us_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"earthquake_us_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"earthquake_us_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .otherwise(
                    (
                        pl.col(f"earthquake_intl_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"earthquake_intl_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"earthquake_intl_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .fill_nan(0).alias(f"rate_base_total_eq_layer{index}")
        )

        df = df.with_columns(
            (
                (
                    df[f"earthquake_us_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"earthquake_us_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"earthquake_us_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"] +
                    df[f"earthquake_intl_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"earthquake_intl_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"earthquake_intl_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_eq_layer{index}")
        )

    if hxd.policy_information.small_schedule_model:
        eq_occupancy_list = df['eq_occupancy_factor'].to_list()
        eq_construction_list = df['eq_construction_factor'].to_list()
        eq_year_built_list = df['eq_year_built_factor'].to_list()
        eq_num_floors_list = df['eq_num_floors_factor'].to_list()
        eq_catnet_intl_list = df['eq_catnet_intl_factor'].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_occ_eq = eq_occupancy_list[i]
            row.rfr_construction_eq = eq_construction_list[i]
            row.rfr_yearbuilt_eq = eq_year_built_list[i]
            row.rfr_nofloors_eq = eq_num_floors_list[i]
            row.rfr_hazardscore_eq = eq_catnet_intl_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            # Assign to schedule table
            earthquake_entry_perc_list = df[f"earthquake_entry_perc_layer{index}"].to_list()
            earthquake_exit_perc_list = df[f"earthquake_exit_perc_layer{index}"].to_list()
            earthquake_worth_percent_list = df[f"earthquake_worth_percent_layer{index}"].to_list()
            eq_ded_usd = df[f"eq_deductible_selected_layer{index}"].to_list()
            eq_sublimit_usd = df[f"eq_selected_sublimit_layer{index}"].to_list()
            eq_tiv_exposed_list = df[f"earthquake_tiv_exposed_layer{index}"].to_list()

            earthquake_base_rate_list = df[f"rate_base_total_eq_layer{index}"].to_list()

            earthquake_ground_up_rate_list = df[f"rate_gu_total_eq_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_eq = earthquake_entry_perc_list[i]
                target_output_by_layer.flc_exit_eq = earthquake_exit_perc_list[i]
                target_output_by_layer.flc_worth_eq = earthquake_worth_percent_list[i]
                target_output_by_layer.deductible_usd_eq = eq_ded_usd[i]
                target_output_by_layer.sublimit_usd_eq = eq_sublimit_usd[i]
                target_output_by_layer.tivexposed_total_usd_eq = eq_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_eq = earthquake_base_rate_list[i]
                target_output_by_layer.rate_gu_total_eq = earthquake_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            eq_ded_usd = df[f"eq_deductible_layer{index}"].to_list()
            eq_tiv_exposed_list = df[f"earthquake_tiv_exposed_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.deductible_usd_eq = eq_ded_usd[i]
                target_output_by_layer.tivexposed_total_usd_eq = eq_tiv_exposed_list[i]
    
    return df