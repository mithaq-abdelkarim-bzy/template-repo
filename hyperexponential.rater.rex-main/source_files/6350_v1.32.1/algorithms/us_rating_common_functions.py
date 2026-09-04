import hx
import polars as pl


def us_entry_exit_tiv(hxd, df, other_data, layer, index, peril_abbr, peril, tiv_base_field, sublimit_peril=None, deductible_peril=None):
    '''
    Calcuate entry and exit tiv
    '''

    if not sublimit_peril:
        sublimit_peril = peril_abbr

    if not deductible_peril:
        deductible_peril = peril

    sublimit_field = f"{sublimit_peril}_selected_sublimit_layer{index}"
    deductible_field = f"{deductible_peril}_deductible_layer{index}"
    policy_limit = other_data[f'policy_limit_usd_layer{index}']


    policy_sublimit = other_data[f"{sublimit_peril}_policy_sublimit_usd_layer{index}"]
    policy_excess = other_data[f'policy_excess_usd_layer{index}']
    df = df.with_columns(
        [
            pl.when(pl.col("country") != "United States")
                .then(0)
                .when((pl.col(sublimit_field) == 0) & (policy_sublimit == 0))
                .then(policy_limit)
                .when(policy_sublimit == 0)
                .then(pl.max(pl.min(policy_limit, pl.col(sublimit_field) - policy_excess), pl.lit(0)))
                .when(pl.col(sublimit_field) == 0)
                .then(pl.max(pl.min(policy_limit, policy_sublimit - policy_excess), pl.lit(0)))
                .otherwise(pl.max(pl.min(policy_limit, policy_sublimit - policy_excess, pl.col(sublimit_field) - policy_excess), pl.lit(0)))
                .alias(f"{deductible_peril}_limit_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col(f"{sublimit_peril}_deductible_layer{index}"))
                .otherwise(0)
                .alias(deductible_field)
        ]
    )

    # Calculate TIV exposed
    df = df.with_columns(
        pl.when(pl.col("country") == "United States")
            .then(
                pl.max([
                    pl.min([
                        pl.col('tiv_total_usd') - other_data[f'policy_excess_usd_layer{index}'],
                        pl.col(f"{deductible_peril}_limit_layer{index}")
                    ]),
                    pl.lit(0)
                ])
            )
            .otherwise(0)
            .alias(f"{deductible_peril}_tiv_exposed_layer{index}")
    )

    # Calculate entry/exit tiv
    df = df.with_columns(
        [
            pl.when(pl.col("country") == "United States")
                .then((other_data[f'policy_excess_usd_layer{index}'] + pl.col(deductible_field)) / pl.col(tiv_base_field))
                .otherwise(0)
                .fill_nan(0)
                .alias(f"{peril}_entry_over_tiv_layer{index}"),
            pl.when(pl.col("country") == "United States")
                .then((other_data[f'policy_excess_usd_layer{index}'] + pl.col(deductible_field) + pl.col(f"{deductible_peril}_limit_layer{index}")) / pl.col(tiv_base_field))
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


    return df