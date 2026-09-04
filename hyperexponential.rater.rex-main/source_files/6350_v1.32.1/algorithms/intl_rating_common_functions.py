import hx
import polars as pl
import numpy as np
from algorithms.utilities import pd_df_from_hx_list


def intl_base_rate_lookup(hxd, df, other_data, row_name, peril):

    # Load parameter table
    intl_base_rates_df = hx.params.intl_base_rates
    intl_base_rates_pl = pl.from_pandas(intl_base_rates_df[["Country", row_name]]).rename(
                            {"Country": "country_lowercase", row_name: f"{peril}_intl_buildings_base_rate"})

    intl_base_rates_pl = intl_base_rates_pl.with_columns(
        pl.col("country_lowercase").str.to_lowercase().alias("country_lowercase")
    )           
    
    base_rate_pl = df[["row_nr", "country", "country_lowercase"]].join(intl_base_rates_pl, on="country_lowercase", how="left")[["row_nr", "country", f"{peril}_intl_buildings_base_rate"]]

    return df, base_rate_pl


def intl_base_rate(hxd, df, other_data, layer, index, base_rate_pl, peril, peril_abbr):

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"{peril_abbr}_covered_rating_layer{index}")))

    df = df.with_columns(
        base_rate_pl.select(
            (pl.col(f"{peril}_intl_buildings_base_rate") * pl.col(f"{peril_abbr}_covered_rating_layer{index}") * other_data['inflation'])
                .alias(f"{peril}_intl_buildings_base_rate_layer{index}")
        )
    )

    # Zero any nulls caused by US territories
    df = df.with_columns(
        pl.when(pl.col("country") == "United States").then(pl.lit(0)).otherwise(pl.col(f"{peril}_intl_buildings_base_rate_layer{index}")
            ).alias(f"{peril}_intl_buildings_base_rate_layer{index}")
    )

    df = df.with_columns(
        [
            pl.col(f"{peril}_intl_buildings_base_rate_layer{index}").alias(f"{peril}_intl_contents_base_rate_layer{index}"),
            pl.col(f"{peril}_intl_buildings_base_rate_layer{index}").alias(f"{peril}_intl_bi_base_rate_layer{index}")
        ]
    )

    return df


def intl_entry_exit_tiv(hxd, df, other_data, layer, index, peril_abbr, peril, tiv_base_field):
    '''
    Calcuate entry and exit tiv
    '''
    data_schema_peril = {
        # "fire": "fire",  # Not used
        "ws": "named_windstorm", 
        "scs": "scs", 
        "fl": "flood", 
        "eq": "quake", 
        # "wf": "wildfire"  # Not used
    }
    
    if peril_abbr == "scs":
        tiv_exposed_layer_field = f"scs_intl_tiv_exposed_layer{index}"
    else:
        tiv_exposed_layer_field = f"{peril}_tiv_exposed_layer{index}"

    policy_limit = other_data[f'policy_limit_usd_layer{index}']
    policy_sublimit = other_data[f"{peril_abbr}_policy_sublimit_usd_layer{index}"]

    df = join_intl_ded_table(hxd, df, data_schema_peril[peril_abbr], index, fill_null_ded=0)

    # Assign sublimit and perc, min and max deductibles
    df = df.with_columns(pl.col("country_sublimit").alias(f"{peril_abbr}_country_sublimit"))
    df = df.with_columns((pl.col("perc_of_tiv") * pl.col("tiv_total_usd")).alias(f"{peril_abbr}_intl_perc_loc_deductible"))
    df = df.with_columns(pl.col("fixed_min").alias(f"{peril_abbr}_intl_min_loc_deductible"))
    df = df.with_columns(pl.col("fixed_max").alias(f"{peril_abbr}_intl_max_loc_deductible"))
    
    # Limit / sublimit / country sublimit
    df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(0)
                .when(policy_sublimit == 0)
                .then(policy_limit)
                .otherwise(
                    pl.max(
                        pl.min(policy_limit, policy_sublimit - other_data[f'policy_excess_usd_layer{index}']), 
                        pl.lit(0)
                    )
                )
                .fill_null(policy_limit)
                .alias(f"{peril}_limit_layer{index}"),
    )

    df = df.with_columns(
            pl.when(pl.col("country") == "United States")
                .then(0)
                .when((pl.col("country_sublimit") == 0) | pl.col("country_sublimit").is_null())
                .then(pl.col(f"{peril}_limit_layer{index}"))
                .otherwise(
                    pl.min(
                        pl.col(f"{peril}_limit_layer{index}"), 
                        pl.max(pl.col("country_sublimit") - other_data[f'policy_excess_usd_layer{index}'], pl.lit(0))
                    )
                )
                .alias(f"{peril}_combined_sublimit_layer{index}")
    )  
    
    df = df.with_columns(
        pl.when(pl.col("country") == "United States")
            .then(0)
            .otherwise( 
                pl.when((pl.col(f"{data_schema_peril[peril_abbr]}_loc_intl_ded_layer{index}").is_null()) | (pl.col(f"{data_schema_peril[peril_abbr]}_loc_intl_ded_layer{index}") == 0))               
                .then(pl.col(f"{peril_abbr}_deductible_layer{index}"))
                .otherwise(pl.col(f"{data_schema_peril[peril_abbr]}_loc_intl_ded_layer{index}"))                    
                )
            .alias(f"{peril}_combined_ded_layer{index}")
    )

    # Calculate TIV exposed
    df = df.with_columns(
        pl.when(pl.col("country") != "United States")
            .then(
                pl.max([
                    pl.min([
                        pl.col('tiv_total_usd') - other_data[f'policy_excess_usd_layer{index}'],
                        pl.col(f"{peril}_combined_sublimit_layer{index}")
                    ]),
                    pl.lit(0)
                ])
            )
            .otherwise(0)
            .alias(tiv_exposed_layer_field)
    )

    # Calculate entry/exit tiv
    df = df.with_columns(
        [
            pl.when(pl.col("country") != "United States")
                .then((other_data[f'policy_excess_usd_layer{index}'] + pl.col(f"{peril}_combined_ded_layer{index}")) / pl.col(tiv_base_field))
                .otherwise(0)
                .fill_nan(0)
                .alias(f"{peril}_entry_over_tiv_layer{index}"),
            pl.when(pl.col("country") != "United States")
                .then((other_data[f'policy_excess_usd_layer{index}'] + pl.col(f"{peril}_combined_ded_layer{index}") + pl.col(f"{peril}_combined_sublimit_layer{index}")) / pl.col(tiv_base_field))
                .otherwise(0)
                .fill_nan(0)
                .alias(f"{peril}_exit_over_tiv_layer{index}"),                
        ]
    )

    
    # Replace inf for the edge case
    df = df.with_columns(
                            pl.when(pl.col(f"{peril}_entry_over_tiv_layer{index}") == float('inf'))
                                .then(0)
                                .otherwise(pl.col(f"{peril}_entry_over_tiv_layer{index}"))
                                .alias(f"{peril}_entry_over_tiv_layer{index}"),
                            pl.when(pl.col(f"{peril}_exit_over_tiv_layer{index}") == float('inf'))
                                .then(0)
                                .otherwise(pl.col(f"{peril}_exit_over_tiv_layer{index}"))
                                .alias(f"{peril}_exit_over_tiv_layer{index}")
                            )

    df = df.drop([
        "perc_of_tiv",
        "fixed_min",
        "fixed_max",
        "country_sublimit"
    ])
    return df


def intl_fire_deductible_fill(hxd, df, layer, index, peril, peril_struct_name, short_peril_struct_name=None):
    """
    For Hail, Tornado and Flood, if use hasn't specified Region="All" we want to use the fire deductible
    """
    if peril != "flood":
        region_1 = getattr(layer.perils, peril_struct_name).location_ded.option_1.region_dropdown.region
    else:
        region_1 = getattr(layer.perils, peril_struct_name).location_ded.option_1.region_dropdown.fema_zone

    num_options = getattr(hxd.non_layer_perils, peril_struct_name).num_options
    if not short_peril_struct_name:
        short_peril_struct_name = peril_struct_name
    
    if f"{short_peril_struct_name}_deductible_layer{index}_option1" in df.columns:
        lookup_value = pl.col(f"{short_peril_struct_name}_deductible_layer{index}_option1")
    else:
        lookup_value = pl.lit(0)

    df = df.with_columns(
        pl.when(pl.col("country") == "United States")
            .then(pl.col(f"{short_peril_struct_name}_deductible_layer{index}"))
            .when(((num_options or 0) > 0) & (region_1 == "All"))
            .then(lookup_value)
            .otherwise(pl.col(f"fire_deductible_usd_layer{index}"))
            .alias(f"{short_peril_struct_name}_deductible_layer{index}")
    )

    return df
    

def join_intl_ded_table(hxd, df, peril, index, fill_null_ded=None):
    exchange_rate = hxd.policy_information.exchange_rate or 1

    intl_deductibles = pl.from_pandas(pd_df_from_hx_list(getattr(hxd.non_layer_perils, peril).intl_ded))
    intl_deductibles = intl_deductibles.drop("tiv")
    intl_deductibles = intl_deductibles.with_columns([
        ((pl.col("country_sublimit").fill_null(0).cast(pl.Float64) / exchange_rate)).alias("country_sublimit"),
        (pl.col("perc_of_tiv").fill_null(0).cast(pl.Float64)).alias("perc_of_tiv"),
        ((pl.col("fixed_min").fill_null(0).cast(pl.Float64) / exchange_rate)).alias("fixed_min"),
        ((pl.col("fixed_max").fill_null(np.inf).cast(pl.Float64) / exchange_rate)).alias("fixed_max")
        ])

    df = df.join(intl_deductibles, on="country", how="left")

    df = df.with_columns(
        pl.when(pl.col("country") == "United States")
            .then(0)
            .otherwise(
                pl.min(pl.max(pl.col("tiv_total_usd")*pl.col("perc_of_tiv"), pl.col("fixed_min")), pl.col("fixed_max")).fill_null(fill_null_ded)
            )
            .alias(f"{peril}_loc_intl_ded_layer{index}")
    )

    return df