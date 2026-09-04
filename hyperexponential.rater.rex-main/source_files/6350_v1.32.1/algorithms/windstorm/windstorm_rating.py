import hx
import polars as pl
from algorithms.windstorm.windstorm_rating_factor import windstorm_rating_factor, windstorm_us_total_adjustment, windstorm_intl_total_adjustment
from algorithms.windstorm.windstorm_us_rating import windstorm_us_base_rate_lookup, windstorm_us_base_rate
from algorithms.rating_common_functions import ground_up_rate, ground_up_uw_rate, loss_curve_lookup, \
        granularity_option_structure, deductible_option_structure, sublimit_option_structure, \
        expected_loss, percent_worth
from algorithms.intl_rating_common_functions import intl_base_rate_lookup, intl_base_rate, intl_entry_exit_tiv
from algorithms.us_rating_common_functions import us_entry_exit_tiv
from algorithms.analytical_curves import loss_curve


def windstorm_us_rating_calc(hxd, df, other_data):
    '''
    Calculates US Windstorm Rating
    '''

    df = windstorm_rating_factor(hxd, df, other_data)
    df = windstorm_us_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = windstorm_us_base_rate_lookup(hxd, df, other_data)
    df = loss_curve_lookup(hxd, df, hx.params.ws_loss_curve_selection, "tiv_ws_gate", "windstorm_us_curve_selected")

    for index, layer in enumerate(hxd.layers, start=1):
        df = windstorm_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl)
        df = ground_up_rate(hxd, df, other_data, layer, index, "windstorm_us")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "windstorm_us", "ws")
        df, granularity_pl = granularity_option_structure(hxd, df, other_data, layer, index, "ws", "named_windstorm",
                hx.params.ws_granularity_rank)
        df = deductible_option_structure(hxd, df, other_data, layer, index, granularity_pl, "ws", "named_windstorm",
                pl.col("tiv_ws_gate"), pl.col("count_ws_gate"))
        df = sublimit_option_structure(hxd, df, other_data, layer, index, granularity_pl, "ws", "named_windstorm")
        df = us_entry_exit_tiv(hxd, df, other_data, layer, index, "ws", "windstorm_us", "tiv_ws_gate")
        df = loss_curve(hxd, df, index, "windstorm_us")
        df = percent_worth(hxd, df, other_data, layer, index, "windstorm_us")
        df = expected_loss(hxd, df, other_data, layer, index, "windstorm_us")

    del base_rate_pl
    return df


def windstorm_intl_rating_calc(hxd, df, other_data):
    '''
    Calculates International Windstorm Rating
    '''

    df = windstorm_intl_total_adjustment(hxd, df, other_data)
    df, base_rate_pl = intl_base_rate_lookup(hxd, df, other_data, "WS", "windstorm")
    df = loss_curve_lookup(hxd, df, hx.params.ws_loss_curve_selection, "tiv_region", "windstorm_intl_curve_selected")

    for index, layer in enumerate(hxd.layers, start=1):
        df = intl_base_rate(hxd, df, other_data, layer, index, base_rate_pl, "windstorm", "ws")
        df = ground_up_rate(hxd, df, other_data, layer, index, "windstorm_intl")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "windstorm_intl", "ws")
        df = intl_entry_exit_tiv(hxd, df, other_data, layer, index, "ws", "windstorm_intl", "tiv_region")
        df = loss_curve(hxd, df, index, "windstorm_intl")
        df = percent_worth(hxd, df, other_data, layer, index, "windstorm_intl")
        df = expected_loss(hxd, df, other_data, layer, index, "windstorm_intl")

    del base_rate_pl
    return df



def windstorm_expected_loss_calc(hxd, df, other_data):
    '''
    Calculate expected loss based on US + Carribbean WS
    '''

    cb_countries = pl.from_pandas(hx.params.intl_base_rates)
    cb_countries = set(cb_countries.filter(pl.col("Continent") == "Caribbean").select("Country").to_series().to_list())
    
    for index, layer in enumerate(hxd.layers, start=1):
        windstorm_pl = df[["country", 
                            f"windstorm_us_total_expected_loss_pre_uw_layer{index}",
                            f"windstorm_intl_total_expected_loss_pre_uw_layer{index}",
                            f"windstorm_us_total_expected_loss_post_uw_layer{index}",
                            f"windstorm_intl_total_expected_loss_post_uw_layer{index}",
                        ]]


        df = df.with_columns(
            windstorm_pl.select(
                [
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"windstorm_us_total_expected_loss_pre_uw_layer{index}"))
                        .when(pl.col("country").is_in(cb_countries))
                        .then(pl.col(f"windstorm_intl_total_expected_loss_pre_uw_layer{index}"))
                        .otherwise(0)
                        .alias(f"windstorm_us_total_expected_loss_pre_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"windstorm_us_total_expected_loss_post_uw_layer{index}"))
                        .when(pl.col("country").is_in(cb_countries))
                        .then(pl.col(f"windstorm_intl_total_expected_loss_post_uw_layer{index}"))
                        .otherwise(0)
                        .alias(f"windstorm_us_total_expected_loss_post_uw_layer{index}"),
                    pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                        .then(0)
                        .otherwise(pl.col(f"windstorm_intl_total_expected_loss_pre_uw_layer{index}"))
                        .alias(f"windstorm_intl_total_expected_loss_pre_uw_layer{index}"),
                    pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                        .then(0)
                        .otherwise(pl.col(f"windstorm_intl_total_expected_loss_post_uw_layer{index}"))
                        .alias(f"windstorm_intl_total_expected_loss_post_uw_layer{index}"),
                ]
            )
        )

    return df




def windstorm_hxd_assignment(hxd, df, other_data):
    '''
    Assign windstorm data to hxd
    '''
    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"windstorm_us_entry_perc_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_entry_perc_layer{index}"))
                .alias(f"windstorm_entry_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"windstorm_us_exit_perc_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_exit_perc_layer{index}"))
                .alias(f"windstorm_exit_perc_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"windstorm_us_worth_percent_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_worth_percent_layer{index}"))
                .alias(f"windstorm_worth_percent_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"windstorm_us_tiv_exposed_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_tiv_exposed_layer{index}"))
                .alias(f"windstorm_tiv_exposed_layer{index}")
        )

        df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(
                    (
                        pl.col(f"windstorm_us_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"windstorm_us_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"windstorm_us_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .otherwise(
                    (
                        pl.col(f"windstorm_intl_buildings_base_rate_layer{index}") * pl.col("tiv_buildings_usd") +
                        pl.col(f"windstorm_intl_contents_base_rate_layer{index}") * pl.col("tiv_contents_usd") +
                        pl.col(f"windstorm_intl_bi_base_rate_layer{index}") * pl.col("tiv_bi_usd") 
                    ) / pl.col("tiv_total_usd")
                )
                .fill_nan(0).alias(f"rate_base_total_ws_layer{index}")
        )

        df = df.with_columns(
            (
                (
                    df[f"windstorm_us_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"windstorm_us_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"windstorm_us_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"] +
                    df[f"windstorm_intl_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"windstorm_intl_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] + 
                    df[f"windstorm_intl_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_ws_layer{index}")
        )

    if hxd.policy_information.small_schedule_model:
        ws_occupancy_list = df['ws_occupancy_factor'].to_list()
        ws_construction_list = df['ws_construction_factor'].to_list()
        ws_year_built_list = df['ws_year_built_factor'].to_list()
        ws_floor_area_list = df['ws_floor_area_factor'].to_list()
        ws_num_floors_list = df['ws_num_floors_factor'].to_list()
        ws_roof_age_list = df['ws_roof_age_factor'].to_list()
        ws_roof_covering_list = df['ws_roof_covering_factor'].to_list()
        ws_roof_geometry_list = df['ws_roof_geometry_factor'].to_list()
        ws_storm_surge_list = df['ws_storm_surge_factor'].to_list()
        ws_catnet_intl_list = df['ws_catnet_intl_factor'].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_occ_ws = ws_occupancy_list[i]
            row.rfr_construction_ws = ws_construction_list[i]
            row.rfr_yearbuilt_ws = ws_year_built_list[i]
            row.rfr_floorarea_ws = ws_floor_area_list[i]
            row.rfr_nofloors_ws = ws_num_floors_list[i]
            row.rfr_roofage_ws = ws_roof_age_list[i]
            row.rfr_roofcovering_ws = ws_roof_covering_list[i]
            row.rfr_roofgeometry_ws = ws_roof_geometry_list[i]
            row.rfr_ss_ws = ws_storm_surge_list[i]
            row.rfr_hazardscore_ws = ws_catnet_intl_list[i]

        for index, layer in enumerate(hxd.layers, start=1):
            # Assign to schedule table

            windstorm_entry_perc_list = df[f"windstorm_entry_perc_layer{index}"].to_list()
            windstorm_exit_perc_list = df[f"windstorm_exit_perc_layer{index}"].to_list()
            windstorm_worth_percent_list = df[f"windstorm_worth_percent_layer{index}"].to_list()
            ws_ded_usd = df[f"ws_deductible_selected_layer{index}"].to_list()
            ws_sublimit_usd = df[f"ws_selected_sublimit_layer{index}"].to_list()
            ws_tiv_exposed_list = df[f"windstorm_tiv_exposed_layer{index}"].to_list()

            windstorm_base_rate_list = df[f"rate_base_total_ws_layer{index}"].to_list()

            windstorm_ground_up_rate_list = df[f"rate_gu_total_ws_layer{index}"].to_list()
            
            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_ws = windstorm_entry_perc_list[i]
                target_output_by_layer.flc_exit_ws = windstorm_exit_perc_list[i]
                target_output_by_layer.flc_worth_ws = windstorm_worth_percent_list[i]
                target_output_by_layer.deductible_usd_ws = ws_ded_usd[i]
                target_output_by_layer.sublimit_usd_ws = ws_sublimit_usd[i]
                target_output_by_layer.tivexposed_total_usd_ws = ws_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_ws = windstorm_base_rate_list[i]
                target_output_by_layer.rate_gu_total_ws = windstorm_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:
        for index, layer in enumerate(hxd.layers, start=1):

            ws_ded_usd = df[f"ws_deductible_selected_layer{index}"].to_list()
            ws_tiv_exposed_list = df[f"windstorm_tiv_exposed_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.deductible_usd_ws = ws_ded_usd[i]
                target_output_by_layer.tivexposed_total_usd_ws = ws_tiv_exposed_list[i]
    
    return df
