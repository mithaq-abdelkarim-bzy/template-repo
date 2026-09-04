import hx
import polars as pl
import pandas as pd
import numpy as np
from scipy import stats
from algorithms.rating_common_functions import ground_up_rate, ground_up_uw_rate, loss_curve_lookup
from algorithms.analytical_curves import loss_curve, size_discount
from algorithms.intl_rating_common_functions import join_intl_ded_table


def fire_rating_calc(hxd, df, other_data):
    '''
    Calculates fire rating value
    '''

    df = fire_rating_factor(hxd, df, other_data)
    inflation(hxd, df, other_data)
    df, non_cat_base_rates_pl_joined = fire_base_rate_lookup(hxd, df, other_data)
    df = loss_curve_lookup(hxd, df, hx.params.fire_loss_curve_selection, "tiv_total_usd", "fire_curve_selected")
    
    for index, layer in enumerate(hxd.layers, start=1):
        df = fire_base_rate(hxd, df, other_data, layer, index, non_cat_base_rates_pl_joined)
        df = ground_up_rate(hxd, df, other_data, layer, index, "fire")
        df = ground_up_uw_rate(hxd, df, other_data, layer, index, "fire", "fire")
        df = fire_mb_ground_up_rates(hxd, df, other_data, layer, index)
        df = fire_loss_curve(hxd, df, other_data, layer, index)
        df = fire_expected_loss(hxd, df, other_data, layer, index)
    
    del non_cat_base_rates_pl_joined
    return df


def fire_rating_factor(hxd, df, other_data):

    # Load parameter tables
    non_cat_base_rates_df = hx.params.non_cat_base_rates
    construction_load_df = hx.params.construction_load
    sprinklers_df = hx.params.sprinklers
    pc_code_df = hx.params.ppc_load
    size_discount_df = hx.params.size_discount

    # Join Machinery Breakdown proportion 
    columns = ["industry", "fire_mb_proportion"]
    mb_pl = pl.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.non_layer_perils.fire.machinery_breakdown])
    df = df.join(mb_pl, on="industry", how="left")
    df = df.with_columns(pl.col("fire_mb_proportion").fill_null(0))

    # Apply construction name
    construction_name_df = construction_load_df[["ISO", "Construction"]]
    construction_name_pl = pl.from_pandas(construction_name_df).rename({"ISO": "constr_code", "Construction":"constr_name"})
    df = df.join(construction_name_pl, on="constr_code", how="left")

    # Bring in base rating factors for each location based on industry/occupancy
    base_rating_factor_pl = (
        pl.from_pandas(non_cat_base_rates_df[["Industry", "Occupancy", "BaseTIV", "BaseConstruction", "BaseSprinkler", "BasePCCode"]])
        .rename({"Industry": "industry", "Occupancy": "occupancy", "BaseTIV": "base_tiv", "BaseConstruction": "base_constr_code", "BaseSprinkler": "base_sprinkler", "BasePCCode": "base_pc_code"})
    )
    df = df.join(base_rating_factor_pl, on=["industry", "occupancy"], how="left")

    # Calculate Construction Rating Factor
    construction_load_df = construction_load_df[["ISO", "Fire"]]
    construction_load_pl = pl.from_pandas(construction_load_df).rename({"ISO": "constr_code", "Fire": "fire_construction_load"})
    fire_rating_pl = df[["base_constr_code", "constr_code", "base_sprinkler", "sprinkler", "base_pc_code", "pc_code", "country"]].join(construction_load_pl, on="constr_code", how="left")
    fire_rating_pl = fire_rating_pl.join(construction_load_pl.rename({"fire_construction_load": "base_construction_load"}), left_on="base_constr_code", right_on="constr_code", how="left")

    # Sprinkler Rating Factor
    sprinklers_df = sprinklers_df[["Sprinklers", "Load"]]
    sprinklers_pl = pl.from_pandas(sprinklers_df).rename({"Sprinklers": "sprinkler", "Load": "fire_sprinkler_load"})
    fire_rating_pl = fire_rating_pl.join(sprinklers_pl, on="sprinkler", how="left")
    fire_rating_pl = fire_rating_pl.join(sprinklers_pl.rename({"fire_sprinkler_load": "base_sprinkler_load"}), left_on="base_sprinkler", right_on="sprinkler", how="left")

    # PC Code Rating Factor
    pc_code_df = pc_code_df[["PPC", "Fire"]]
    pc_code_pl = pl.from_pandas(pc_code_df).rename({"PPC": "pc_code", "Fire": "fire_pc_code_load"})
    fire_rating_pl = fire_rating_pl.join(pc_code_pl, on="pc_code", how="left")
    fire_rating_pl = fire_rating_pl.join(pc_code_pl.rename({"fire_pc_code_load": "base_pc_code_load"}), left_on="base_pc_code", right_on="pc_code", how="left")

    # Mexican Fonden Rating Factor NOTE: mexican_fonden was removed from model so setting load to 1. 
    mexican_fonden_load = 1

    # Assign to df columns
    df = df.with_columns(fire_rating_pl.select(
        [
            pl.when((pl.col("constr_code") == None) | (pl.col("constr_code") == 0))
                .then(1)
                .otherwise((1 + pl.col("fire_construction_load")) / (1 + pl.col("base_construction_load")))
                .alias("fire_construction_factor"),
            pl.when((pl.col("sprinkler") == None) | (pl.col("sprinkler") == "Unknown"))
                .then(1)
                .otherwise((1 + pl.col("fire_sprinkler_load")) / (1 + pl.col("base_sprinkler_load")))
                .alias("fire_sprinkler_factor"),
            pl.when(pl.col("pc_code") == None)
                .then(1)
                .otherwise((1 + pl.col("fire_pc_code_load")) / (1 + pl.col("base_pc_code_load")))
                .alias("fire_pc_code_factor"),
            pl.when(pl.col('country') != 'Mexico')
                .then(1)
                .otherwise(1)
                .alias("fire_mexican_fonden_factor"),
            pl.when(pl.col('country') != 'Mexico')
                .then("no")
                .otherwise("yes")
                .alias("is_mexican_fonden")
        ]
    ))

    del fire_rating_pl


    # Fire Size Discount Factor
    loc_discount_df = hx.params.location_level_tiv
    acc_discount_df = hx.params.account_level_tiv
    # assign Discount Factors 
    total_loc_tiv_df = df["tiv_total_usd"]
    total_acc_tiv = other_data["total_tiv_total_usd"]
    total_loc_base_tiv_df = df["base_tiv"]
    
    fire_size_discount_pl = pl.DataFrame({
        # Actual size discount factor = location size discount * account size discount. 
        "fire_actual_size_discount_factor": size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, "fire"),
        # Base size discount factor = location size discount only, based on base TIVs for each location.
        "fire_base_size_discount_factor": size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_base_tiv_df, "fire", exclude_account_size_discount=True)
    })
    # For Fire rating, the size discount factor is based on how location TIVs compare to their base TIVs (by occupancy). 
    # To calculate the SDC adjustment, we require: actual location SDF / base location SDF * actual account SDF
    fire_size_discount_pl = fire_size_discount_pl.with_columns(
        [(pl.col("fire_actual_size_discount_factor") / pl.col("fire_base_size_discount_factor")).alias('fire_size_discount_factor')]
    )
    fire_size_discount_factor = fire_size_discount_pl["fire_size_discount_factor"]

    fire_risk_quality_factor = 1
    other_data['fire_risk_quality_factor'] = fire_risk_quality_factor

    df = df.with_columns(pl.Series(name="fire_size_discount_factor", values = fire_size_discount_factor))

    # Total Rating Factor Adjustment
    df = df.with_columns(
        [
            (
                pl.col('fire_construction_factor') * pl.col('fire_sprinkler_factor') * \
                    pl.col('fire_pc_code_factor') * pl.col('fire_mexican_fonden_factor') * \
                        pl.col('fire_size_discount_factor') * fire_risk_quality_factor
            ).alias('fire_buildings_total_adjustment')
        ]
    )
    
    df = df.with_columns(
        [
            pl.col('fire_buildings_total_adjustment')
                .alias('fire_contents_total_adjustment'),
            (pl.col('fire_buildings_total_adjustment') * pl.col('bi_waiting_period_factor') * \
                other_data['bi_indemnity_period_factor'] * other_data['cbi_load'])
                .alias('fire_bi_total_adjustment')
        ]
    )

    df = df.with_columns(
        (pl.col("fire_construction_factor") * pl.col('fire_size_discount_factor') * pl.col("fire_sprinkler_factor") * pl.col("fire_pc_code_factor") *
            pl.col("fire_mexican_fonden_factor") * fire_risk_quality_factor * pl.col("bi_waiting_period_factor") * other_data["bi_indemnity_period_factor"] *
            other_data["cbi_load"])
            .alias("fire_total_modifier_impact")
    )

    return df


def inflation(hxd, df, other_data):

    # Load parameter tables
    inflation_df = hx.params.inflation

    # Calculate Inflation
    year_month = f"{hxd.hx_core.inception_date.year}{hxd.hx_core.inception_date.month}"
    if year_month not in set(inflation_df['Month']) or not hxd.policy_information.team:
        other_data['inflation'] = 1
    else:
        other_data['inflation'] = 1 + inflation_df[inflation_df['Month'] == year_month][hxd.policy_information.team].iloc[0]
    

def fire_base_rate_lookup(hxd, df, other_data):

    # Load parameter tables
    non_cat_base_rates_df = hx.params.non_cat_base_rates

    # Fire Base Rates (From lookup, before inflation and layer included check)
    non_cat_base_rates_df = non_cat_base_rates_df[["Key", "Buildings", "Contents", "MB", "BI"]]

    non_cat_base_rates_pl = pl.from_pandas(non_cat_base_rates_df).rename({
                                "Key": "industry_occupancy"
                                })

    non_cat_base_rates_pl_joined = df[["row_nr", "industry_occupancy"]].join(non_cat_base_rates_pl, on="industry_occupancy", how="left")   

    return df, non_cat_base_rates_pl_joined


def fire_base_rate(hxd, df, other_data, layer, index, non_cat_base_rates_pl_joined):

    non_cat_base_rates_pl_joined = non_cat_base_rates_pl_joined.with_columns(df.select(pl.col(f"fire_covered_rating_layer{index}")))

    # Fire Base Rates
    df = df.with_columns(
        non_cat_base_rates_pl_joined.select(
            (pl.col('Buildings') * pl.col(f"fire_covered_rating_layer{index}") * other_data['inflation'])
                .alias(f"fire_buildings_base_rate_layer{index}")
        )
    )
    
    df = df.with_columns(
        non_cat_base_rates_pl_joined.select(
            (pl.col('Contents') * pl.col(f"fire_covered_rating_layer{index}") * other_data['inflation'])
                .alias(f"fire_contents_base_rate_layer{index}")
        )
    )

    df = df.with_columns(
        non_cat_base_rates_pl_joined.select(
            (pl.col('MB') * pl.col(f"fire_covered_rating_layer{index}") * other_data['inflation'])
            .alias(f"fire_mb_base_rate_layer{index}")
        )
    )

    df = df.with_columns(
        non_cat_base_rates_pl_joined.select(
            (pl.col('BI') * pl.col(f"fire_covered_rating_layer{index}") * other_data['inflation'])
                .alias(f"fire_bi_base_rate_layer{index}")
        )            
    )

    return df

def fire_mb_ground_up_rates(hxd, df, other_data, layer, index):
    df = df.with_columns(
        [(pl.col(f"fire_mb_base_rate_layer{index}") * pl.col("fire_contents_total_adjustment"))
            .alias(f"fire_mb_ground_up_rate_layer{index}")]
    )
    df = df.with_columns(
        [(pl.col(f"fire_mb_ground_up_rate_layer{index}") * (1 + other_data['fire_uw_adjustments'] + other_data[f'fire_experience_rating_adj_layer{index}']))
            .alias(f"fire_mb_ground_up_uw_rate_layer{index}")]
    )    
    return df

def fire_loss_curve(hxd, df, other_data, layer, index):

    loss_curve_lookup_df = hx.params.loss_curve_lookup
    exchange_rate = hxd.policy_information.exchange_rate or 1 
    fire_deductible = layer.perils.fire.deductible or 0
    fire_deductible_usd = fire_deductible / exchange_rate # Global exchange rate
    mb_sublimit = hxd.non_layer_perils.fire.machinery_breakdown_sublimit or 0
    mb_sublimit_usd = mb_sublimit / exchange_rate

    # Get the intl fire deductibles
    df = join_intl_ded_table(hxd, df, "fire", index, fill_null_ded=fire_deductible_usd)
    df = df.drop(["country_sublimit", "perc_of_tiv", "fixed_min", "fixed_max"])

    # Get the deductible for loss curve calculation
    df = df.with_columns(
        pl.when(pl.col('fire_deductible') == None)
            .then(
                pl.when(pl.col("country") == "United States").then(
                    pl.lit(fire_deductible_usd)
                ).otherwise(
                    pl.when((pl.col(f"fire_loc_intl_ded_layer{index}") == 0) | (pl.col(f"fire_loc_intl_ded_layer{index}").is_null()))
                    .then(pl.lit(fire_deductible_usd))
                    .otherwise(pl.col(f"fire_loc_intl_ded_layer{index}")))# DB Edit - 08.04.2025, the fire_loc_intl_ded_layer has already been converted to USD, convert other deductibles to be in USD. 
                )
        .otherwise(pl.col('fire_deductible') / pl.col('exchange_rate')) # Schedule exchange rate 
        .fill_null(0)
        .alias(f'fire_deductible_layer{index}')
    )

    if hxd.policy_information.exchange_rate:
        expr = pl.col(f'fire_deductible_layer{index}') 
    else:
        expr = pl.lit(0)

    df = df.with_columns(
            expr.alias(f'fire_deductible_usd_layer{index}')
    )

    # Calculate TIV Exposed, Entry / TIV and Exit / TIV
    df = df.with_columns(
        [
            pl.max([
                pl.min([
                    pl.col('tiv_total_usd') - other_data[f'policy_excess_usd_layer{index}'],
                    other_data[f'policy_limit_usd_layer{index}']
                ]), 
                pl.lit(0)
            ]).alias(f'fire_tiv_exposed_layer{index}'),
            pl.when(pl.col('tiv_total_usd') == 0)
                .then(0)
                .otherwise((other_data[f'policy_excess_usd_layer{index}'] + pl.col(f'fire_deductible_usd_layer{index}')) / pl.col('tiv_total_usd'))
                .alias(f'fire_entry_over_tiv_layer{index}'),
            pl.when(pl.col('tiv_total_usd') == 0)
                .then(0)
                .otherwise((other_data[f'policy_limit_usd_layer{index}'] + other_data[f'policy_excess_usd_layer{index}'] + pl.col(f'fire_deductible_usd_layer{index}')) / pl.col('tiv_total_usd'))
                .alias(f'fire_exit_over_tiv_layer{index}'),
        ]
    )    

    df = loss_curve(hxd, df, index, "fire")

    df = df.with_columns(
        (pl.col(f"fire_exit_perc_layer{index}") - pl.col(f"fire_entry_perc_layer{index}")).alias(f"fire_worth_percent_layer{index}")
    )

    df = fire_mb_loss_curve(hxd, df, other_data, layer, index, mb_sublimit_usd)
    
    other_data[f"policy_fire_deductible_usd_layer{index}"] = fire_deductible_usd

    return df


def fire_expected_loss(hxd, df, other_data, layer, index):
    # Buildings, Contents, BI
    df = df.with_columns(
        [
            # Calculate the expected loss pre UW adjustment
            (pl.col("tiv_buildings_usd") * pl.col(f"fire_buildings_ground_up_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_buildings_expected_loss_pre_uw_layer{index}"),    # Buildings
            (pl.col("tiv_contents_total_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_contents_ground_up_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_contents_expected_loss_pre_uw_layer{index}"),     # Contents
            (pl.col("tiv_bi_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_bi_ground_up_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_bi_expected_loss_pre_uw_layer{index}"),           # BI

            # Calculate the expected loss post UW adjustment
            (pl.col("tiv_buildings_usd") * pl.col(f"fire_buildings_ground_up_uw_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_buildings_expected_loss_post_uw_layer{index}"),   # Buildings
            (pl.col("tiv_contents_total_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_contents_ground_up_uw_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_contents_expected_loss_post_uw_layer{index}"),    # Contents                
            (pl.col("tiv_bi_usd") * (1 - pl.col("fire_mb_proportion")) * pl.col(f"fire_bi_ground_up_uw_rate_layer{index}") * pl.col(f"fire_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_bi_expected_loss_post_uw_layer{index}")           # BI
        ]
    )
    # Machinery Breakdown
    df = df.with_columns(
        [
            # Calculate the expected loss pre UW adjustment
            (pl.col("tiv_contents_total_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_ground_up_rate_layer{index}") *\
                pl.col(f"fire_mb_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .fill_null(0).alias(f"fire_mb_contents_expected_loss_pre_uw_layer{index}"),
            (pl.col("tiv_bi_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_ground_up_rate_layer{index}") *\
                (pl.when(pl.col(f"fire_contents_ground_up_rate_layer{index}") == 0)
                    .then(0)
                    .otherwise(pl.col(f"fire_bi_ground_up_rate_layer{index}") / pl.col(f"fire_contents_ground_up_rate_layer{index}"))) *\
                pl.col(f"fire_mb_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_mb_bi_expected_loss_pre_uw_layer{index}"),

            # Calculate the expected loss post UW adjustment
            (pl.col("tiv_contents_total_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_ground_up_uw_rate_layer{index}") *\
                pl.col(f"fire_mb_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .fill_null(0).alias(f"fire_mb_contents_expected_loss_post_uw_layer{index}"),
            (pl.col("tiv_bi_usd") * pl.col("fire_mb_proportion") * pl.col(f"fire_mb_ground_up_uw_rate_layer{index}") *\
                (pl.when(pl.col(f"fire_contents_ground_up_uw_rate_layer{index}") == 0)
                    .then(0)
                    .otherwise(pl.col(f"fire_bi_ground_up_uw_rate_layer{index}") / pl.col(f"fire_contents_ground_up_uw_rate_layer{index}"))) *\
                pl.col(f"fire_mb_worth_percent_layer{index}") * hxd.policy_information.policy_length.selected)
                .alias(f"fire_mb_bi_expected_loss_post_uw_layer{index}")
        ]
    )
    df = df.with_columns(
        [
            (pl.col(f"fire_mb_contents_expected_loss_pre_uw_layer{index}") + pl.col(f"fire_mb_bi_expected_loss_pre_uw_layer{index}"))
                .alias(f"fire_mb_expected_loss_pre_uw_layer{index}"), 
            (pl.col(f"fire_mb_contents_expected_loss_post_uw_layer{index}") + pl.col(f"fire_mb_bi_expected_loss_post_uw_layer{index}"))
                .alias(f"fire_mb_expected_loss_post_uw_layer{index}")            
        ]
    )

    # Total expected loss
    df = df.with_columns(
        [
            (pl.col(f"fire_buildings_expected_loss_pre_uw_layer{index}") + pl.col(f"fire_contents_expected_loss_pre_uw_layer{index}") + pl.col(f"fire_mb_expected_loss_pre_uw_layer{index}") + pl.col(f"fire_bi_expected_loss_pre_uw_layer{index}"))
                .alias(f"fire_total_expected_loss_pre_uw_layer{index}"),
            (pl.col(f"fire_buildings_expected_loss_post_uw_layer{index}") + pl.col(f"fire_contents_expected_loss_post_uw_layer{index}") + pl.col(f"fire_mb_expected_loss_post_uw_layer{index}") + pl.col(f"fire_bi_expected_loss_post_uw_layer{index}"))
                .alias(f"fire_total_expected_loss_post_uw_layer{index}")
        ]
    )

    return df


def fire_hxd_assignment(hxd, df, other_data):
    '''
    Assign fire data to hxd
    '''
    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
        ((df[f"fire_buildings_base_rate_layer{index}"] * df["tiv_buildings_usd"] + 
            df[f"fire_contents_base_rate_layer{index}"] * df["tiv_contents_total_usd"] * (1 - df["fire_mb_proportion"]) + 
            df[f"fire_mb_base_rate_layer{index}"] * df["tiv_contents_total_usd"] * df["fire_mb_proportion"] + 
            df[f"fire_bi_base_rate_layer{index}"] * df["tiv_bi_usd"]) / df["tiv_total_usd"])
            .fill_nan(0).alias(f"rate_base_total_fire_layer{index}")
        )

        df = df.with_columns(
            (
                (
                    df[f"fire_buildings_ground_up_rate_layer{index}"] * df["tiv_buildings_usd"] +
                    df[f"fire_contents_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] * (1 - df["fire_mb_proportion"]) + 
                    df[f"fire_mb_ground_up_rate_layer{index}"] * df["tiv_contents_total_usd"] * df["fire_mb_proportion"] + 
                    df[f"fire_bi_ground_up_rate_layer{index}"] * df["tiv_bi_usd"]
                ) / df["tiv_total_usd"]
            ).fill_nan(0).alias(f"rate_gu_total_fire_layer{index}")
        )

    if hxd.policy_information.small_schedule_model:
        fire_construction_factor_list = df["fire_construction_factor"].to_list()
        fire_sprinkler_factor_list = df["fire_sprinkler_factor"].to_list()
        fire_pc_code_factor_list = df["fire_pc_code_factor"].to_list()
        fire_mexican_fonden_list = df["fire_mexican_fonden_factor"].to_list()
        fire_size_discount_list = df["fire_size_discount_factor"].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_construction_fire = fire_construction_factor_list[i]
            row.rfr_sprinkler_fire = fire_sprinkler_factor_list[i]
            row.rfr_ppc_fire = fire_pc_code_factor_list[i]
            row.rfr_mexicanfonden_fire = fire_mexican_fonden_list[i]
            row.rfr_sizedisc_fire = fire_size_discount_list[i]
            row.rfr_riskquality_fire = other_data['fire_risk_quality_factor']

        for index, layer in enumerate(hxd.layers, start=1):
            fire_entry_perc_list = df[f"fire_entry_perc_layer{index}"].to_list()
            fire_exit_perc_list = df[f"fire_exit_perc_layer{index}"].to_list()
            fire_worth_percent_list = df[f"fire_worth_percent_layer{index}"].to_list()
            fire_el_pre_uw_list = df[f"fire_total_expected_loss_pre_uw_layer{index}"].to_list()
            fire_el_post_uw_list = df[f"fire_total_expected_loss_post_uw_layer{index}"].to_list()
            fire_deductible_list = df[f'fire_deductible_usd_layer{index}'].to_list()
            fire_tiv_exposed_list = df[f'fire_tiv_exposed_layer{index}'].to_list()

            fire_base_rate_list = df[f"rate_base_total_fire_layer{index}"].to_list()
            fire_ground_up_rate_list = df[f"rate_gu_total_fire_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.flc_entry_fire = fire_entry_perc_list[i]
                target_output_by_layer.flc_exit_fire = fire_exit_perc_list[i]
                target_output_by_layer.flc_worth_fire = fire_worth_percent_list[i]
                target_output_by_layer.el_pre_uw_usd_100_fire_total = fire_el_pre_uw_list[i]
                target_output_by_layer.el_post_uw_usd_100_fire_total = fire_el_post_uw_list[i]
                target_output_by_layer.deductible_usd_fire = fire_deductible_list[i]
                target_output_by_layer.tivexposed_total_usd_fire = fire_tiv_exposed_list[i]
                target_output_by_layer.rate_base_total_fire = fire_base_rate_list[i]
                target_output_by_layer.rate_gu_total_fire = fire_ground_up_rate_list[i]

    elif other_data["large_model_assign"]:

        for index, layer in enumerate(hxd.layers, start=1):
            fire_el_pre_uw_list = df[f"fire_total_expected_loss_pre_uw_layer{index}"].to_list()
            fire_deductible_list = df[f'fire_deductible_layer{index}'].to_list()
            fire_tiv_exposed_list = df[f'fire_tiv_exposed_layer{index}'].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_fire_total = fire_el_pre_uw_list[i]
                target_output_by_layer.deductible_usd_fire = fire_deductible_list[i]
                target_output_by_layer.tivexposed_total_usd_fire = fire_tiv_exposed_list[i]

    return df


def fire_occupancy_guide(hxd):
    '''
    For the selected industry-occupancy, this function will return the outputs for the Occupancy Guide
    '''
    # Load parameter tables and inputs 
    industry = hxd.non_layer_perils.fire.occupancy_guide.industry_occupancy_dropdown.industry or None
    occupancy = hxd.non_layer_perils.fire.occupancy_guide.industry_occupancy_dropdown.occupancy or None
    if (industry and occupancy): 
        industry_occupancy = (industry + occupancy)

        non_cat_base_rates_df = hx.params.non_cat_base_rates
        const_dict = hx.params.construction_load.set_index('ISO')['Construction'].to_dict()

        # Determine outputs for the industry-occupancy pair
        base_dict = non_cat_base_rates_df[non_cat_base_rates_df['Key'] == industry_occupancy].iloc[0].to_dict()

        eb_note = "(referral)" if base_dict['EB Code'] == 'D' else ''

        url = r'https://beazley.sharepoint.com/:x:/r/sites/ActuarialPricing/Shared%20Documents/Property/Property%20User%20Guides/1.%20Commercial%20Property/Occupancy%20Guide/Rex%20-%20Live%20Occupancy%20Guide.xlsx?d=w31b58746a48e4840a0164825560a348b&csf=1&web=1&e=eEDFqH'
        
    if not occupancy:
        occupancy_description_text = "Please select an occupancy."
    else:   
        occupancy_description_text = f""" **Assumed Default Rating Factors**
         - Construction: {const_dict[base_dict['BaseConstruction']]}
         - Sprinkler: {base_dict['BaseSprinkler']}
         - PC Code: {base_dict['BasePCCode']}
         - TIV: ${round(base_dict['BaseTIV']):,}
        
        **ATC Occupancy:** {base_dict['ATC Occupancy Group']}

        **Equipment Breakdown Code:** {base_dict['EB Code']} {eb_note}

        *See full guide [here]({url}).*

        """

    ## NOTE: removed occupancy description as not set up yet
    # **Occupancy Description** 
        # {base_dict['OccupancyDescription']}

    occ_guide_outputs = hxd.non_layer_perils.fire.occupancy_guide
    occ_guide_outputs.occupancy_description = occupancy_description_text


def fire_mb_loss_curve(hxd, df, other_data, layer, index, mb_sublimit_usd):
    
    ## Apply sublimit to MB loss curve calculation
    mb_pl = df.clone().drop([f'fire_entry_over_tiv_layer{index}', f'fire_exit_over_tiv_layer{index}', f"fire_entry_perc_layer{index}", f"fire_exit_perc_layer{index}", f"fire_worth_percent_layer{index}"])
    mb_pl = mb_pl.with_columns([
        (pl.col("tiv_contents_total_usd") * pl.col("fire_mb_proportion")).alias("tiv_mb_usd"),
        
        pl.when(mb_sublimit_usd == 0)
        .then(np.inf)
        .otherwise(pl.lit(mb_sublimit_usd))
        .alias("mb_sublimit_usd"),
        
        (other_data[f'policy_limit_usd_layer{index}'] + other_data[f'policy_excess_usd_layer{index}'] + pl.col(f'fire_deductible_usd_layer{index}')).alias("limit_gu_usd")
    ])
    # sublimit it GU. Select sublimit as min of entered sublimit + loc deductible or limit + excess + loc deductible
    mb_pl = mb_pl.with_columns(
        pl.when((pl.col("mb_sublimit_usd") + pl.col(f'fire_deductible_usd_layer{index}')) <= pl.col("limit_gu_usd"))
        .then(pl.col("mb_sublimit_usd") + pl.col(f'fire_deductible_usd_layer{index}'))
        .otherwise(pl.col("limit_gu_usd"))
        .alias("mb_sublimit_usd")
    ).drop("limit_gu_usd")

    mb_pl = mb_pl.with_columns(
        [
            pl.when(pl.col("tiv_mb_usd") == 0)
            .then(0)
            .otherwise((other_data[f'policy_excess_usd_layer{index}'] + pl.col(f'fire_deductible_usd_layer{index}')) / pl.col('tiv_mb_usd'))
            .alias(f'fire_entry_over_tiv_layer{index}'),
            pl.when(pl.col("tiv_mb_usd") == 0)
            .then(0)
            .otherwise(pl.col("mb_sublimit_usd") / pl.col('tiv_mb_usd'))
            .alias(f'fire_exit_over_tiv_layer{index}')
        ]
    )

    mb_pl = loss_curve(hxd, mb_pl, index, "fire")

    mb_pl = mb_pl.rename({
        f"fire_entry_over_tiv_layer{index}": f"fire_mb_entry_over_tiv_layer{index}",
        f"fire_exit_over_tiv_layer{index}": f"fire_mb_exit_over_tiv_layer{index}",
        f"fire_entry_perc_layer{index}": f"fire_mb_entry_perc_layer{index}",
        f"fire_exit_perc_layer{index}": f"fire_mb_exit_perc_layer{index}",
        })

    mb_pl = mb_pl.with_columns(
        # if sublimit GU > excess + deductible, then exit point < entry point and so ensured that these cases are set to 0 on the worth curve
        ((pl.col(f"fire_mb_exit_perc_layer{index}") - pl.col(f"fire_mb_entry_perc_layer{index}")).clip_min(0)).alias(f"fire_mb_worth_percent_layer{index}")  
    )

    mb_pl = mb_pl[["row_nr", f"fire_mb_entry_over_tiv_layer{index}", f"fire_mb_exit_over_tiv_layer{index}", f"fire_mb_entry_perc_layer{index}", f"fire_mb_exit_perc_layer{index}", f"fire_mb_worth_percent_layer{index}"]]

    df = df.join(mb_pl, on = "row_nr", how = "left")

    return df

