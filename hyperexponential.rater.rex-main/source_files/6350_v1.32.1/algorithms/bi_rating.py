import hx
import polars as pl

def bi_rating_calc(hxd, df, other_data):
    '''
    Calcuates business interruption related rating value
    '''

    # Load parameter tables
    non_cat_base_rates_df = hx.params.non_cat_base_rates
    bi_waiting_period_load_df = hx.params.bi_waiting_period_load
    cbi_load_df = hx.params.cbi
    bi_indemnity_period_df = hx.params.bi_indemnity_period_load

    # Get the BI occupancy mapping and base period days
    team_column_name = "Waiting Period Base (Days) - NACP" if hxd.policy_information.team == "NACP" else "Waiting Period Base (Days) - OM"

    non_cat_base_rates_df = non_cat_base_rates_df[["Key", team_column_name]]

    non_cat_base_rates_pl = pl.from_pandas(non_cat_base_rates_df).rename({
                                "Key": "industry_occupancy", 
                                team_column_name: "waiting_period_base",
                                })

    df = df.with_columns(
        (pl.col("industry") + pl.col("occupancy")).alias("industry_occupancy")
    )

    df = df.join(non_cat_base_rates_pl, on="industry_occupancy", how="left")

    # Calculate BI waiting days adjustment factor
    policy_bi_waiting_period = hxd.policy_information.bi_waiting_period.selected
    if policy_bi_waiting_period == None or policy_bi_waiting_period < 0 or policy_bi_waiting_period > 720:
        df = df.with_columns(pl.lit(1).alias("bi_waiting_period_adjustment"))
    else:
        bi_waiting_period_load_pl = pl.from_pandas(bi_waiting_period_load_df).melt(
            id_vars="Days", value_vars=["2", "3", "30"], variable_name="waiting_period_base", value_name="load")

        bi_waiting_period_load_pl.replace("waiting_period_base", bi_waiting_period_load_pl.select("waiting_period_base").to_series().cast(pl.Int64))
        bi_waiting_period_load_pl = bi_waiting_period_load_pl.rename({"Days": "days_lookup"})

        bi_waiting_period_load_pl_joined = df[["row_nr", "waiting_period_base"]].join(bi_waiting_period_load_pl, on="waiting_period_base", how="left")

        # Upper bound for interpolation
        bi_waiting_upper = bi_waiting_period_load_pl_joined.filter(pl.col("days_lookup") >= policy_bi_waiting_period)
        bi_waiting_upper = bi_waiting_upper.groupby("row_nr", maintain_order=True).first()
        bi_waiting_upper = bi_waiting_upper[["row_nr", "load", "days_lookup"]]
        bi_waiting_upper = bi_waiting_upper.rename({"load": "load_upper", "days_lookup": "days_lookup_upper"})

        # Lower bound for interpolation
        bi_waiting_lower = bi_waiting_period_load_pl_joined.filter(pl.col("days_lookup") <= policy_bi_waiting_period)
        bi_waiting_lower = bi_waiting_lower.groupby("row_nr", maintain_order=True).last()
        bi_waiting_lower = bi_waiting_lower[["row_nr", "load", "days_lookup"]]
        bi_waiting_lower = bi_waiting_lower.rename({"load": "load_lower", "days_lookup": "days_lookup_lower"})

        bi_waiting_pl_filtered = df[["row_nr"]].join(bi_waiting_upper, on="row_nr", how="left")
        bi_waiting_pl_filtered = bi_waiting_pl_filtered.join(bi_waiting_lower, on="row_nr", how="left")

        df = df.with_columns(
            bi_waiting_pl_filtered.select(
                pl.when(pl.col("days_lookup_upper") == pl.col("days_lookup_lower"))
                    .then(1 + pl.col("load_lower"))
                    .otherwise(
                        1 + pl.col("load_lower") + ((pl.col("load_upper") - pl.col("load_lower")) * (policy_bi_waiting_period - pl.col("days_lookup_lower"))) / (pl.col("days_lookup_upper") - pl.col("days_lookup_lower"))
                    )
                    .alias("bi_waiting_period_factor")
            )
        )
    
    # Calculate BI Indemnity Period adjustment factor
    if hxd.policy_information.team == "Open Market":
        team_column_name = "OM"
    elif hxd.policy_information.team == "European Commercial Property":
        team_column_name = "European Commercial Property"
    elif hxd.policy_information.team == "NACP":
        team_column_name = "NACP"
    else:
        team_column_name = "Renewables"
    policy_bi_indemnity_period = hxd.policy_information.bi_indemnity_period.selected
    bi_indemnity_period_df = bi_indemnity_period_df[["Period", team_column_name]]
    if policy_bi_indemnity_period == None or policy_bi_indemnity_period < 0 or policy_bi_indemnity_period > 1440:
        bi_indemnity_period_factor = 1
    else:
        bi_indemnity_upper = bi_indemnity_period_df[bi_indemnity_period_df["Period"] >= policy_bi_indemnity_period].iloc[0]
        bi_indemnity_lower = bi_indemnity_period_df[bi_indemnity_period_df["Period"] <= policy_bi_indemnity_period].iloc[-1]
        period_lookup_upper, load_upper = bi_indemnity_upper['Period'], bi_indemnity_upper[team_column_name]
        period_lookup_lower, load_lower = bi_indemnity_lower['Period'], bi_indemnity_lower[team_column_name]
        if period_lookup_upper == period_lookup_lower:
            bi_indemnity_period_factor = 1 + load_lower
        else:
            bi_indemnity_period_factor = 1 + load_lower + ((load_upper - load_lower) * (policy_bi_indemnity_period - period_lookup_lower)) / (period_lookup_upper - period_lookup_lower)

    # Calculte CBI adjustment factor
    cbi_load_row = cbi_load_df[cbi_load_df["CBI"] == hxd.policy_information.cbi]
    if len(cbi_load_row):
        cbi_load = 1 + cbi_load_row["Load"].iloc[0]
    else:
        cbi_load = 1

    other_data["bi_indemnity_period_factor"] = bi_indemnity_period_factor
    other_data["cbi_load"] = cbi_load
    
    if hxd.policy_information.small_schedule_model:
        bi_waiting_period_factor_list = df["bi_waiting_period_factor"].to_list()

        for i, row in enumerate(hxd.schedule.schedule_table):
            row.rfr_bi_cbi = other_data["cbi_load"]
            row.rfr_bi_indemnityperiod = other_data["bi_indemnity_period_factor"]
            row.rfr_bi_waitingperiod = bi_waiting_period_factor_list[i]

    return df