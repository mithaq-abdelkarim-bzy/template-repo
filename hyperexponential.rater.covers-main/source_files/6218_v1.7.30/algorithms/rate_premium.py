import hx
import polars as pl
from datetime import datetime
from algorithms.rate_common_rating_functions import join_param_table




def premium_calcs(hxd, df):
    
    inception_date = datetime(hxd.cds.standard_fields.inception_date.year, hxd.cds.standard_fields.inception_date.month, hxd.cds.standard_fields.inception_date.day)
    expiry_date = datetime(hxd.cds.standard_fields.expiry_date.year, hxd.cds.standard_fields.expiry_date.month, hxd.cds.standard_fields.expiry_date.day)
    
    # cacluate location AFB gross and net prem. 
    df = df.with_columns((pl.col("acc_beazley_received_gg_prem") * (pl.col("loc_all_perils_beazley_share_aal_and_el") / pl.col("acc_all_perils_beazley_share_aal_and_el"))).fill_nan(0).alias("loc_beazley_share_received_gg_prem"))
    df = df.with_columns((pl.col("loc_beazley_share_received_gg_prem") * (1 - hxd.cds.layers[0].total_deductions)).alias("loc_beazley_share_received_gn_prem"))

    # Calcuate the location GG received prem by peril
    for peril, loss_type in zip (("fire", "fl", "tn", "ha", "wf", "wts", "ws", "eq"), ("el", "el", "el", "el", "el", "el", "aal", "aal")):
        df = df.with_columns(
            pl.when(pl.col("acc_all_perils_beazley_share_aal_and_el") != 0)
            .then(pl.col("acc_beazley_received_gg_prem") * (pl.col(f"loc_{peril}_beazley_share_{loss_type}") / pl.col("acc_all_perils_beazley_share_aal_and_el"))) 
            .otherwise(0)
            .alias(f"loc_{peril}_beazley_share_received_gg_prem")
        )

    tp_assumptions_table = pl.from_pandas(hx.params.table_tp_assumptions)

    # name tp assumption variables for clarity
    return_on_cap = tp_assumptions_table["Return on Capital"].item() 
    gross_group_cat_risk = tp_assumptions_table["Gross Group Cat Risk"].item()
    held_cap = tp_assumptions_table["Held Capital"].item()
    additional_group_cat_risk = tp_assumptions_table["Additional Group Cat Risk"].item()
    cap_req = tp_assumptions_table["Corresponding Capital Required"].item()
    fire_int_cap_allocation = tp_assumptions_table["Fire + AOP + Int Capital Allocation"].item()
    indirect_expense_follow= tp_assumptions_table["Indirect Expenses Per Binder Follow"].item()
    indirect_expense_lead= tp_assumptions_table["Indirect Expenses Per Binder"].item()
    sd = tp_assumptions_table["Standard Deviation"].item()
    lae_perc = tp_assumptions_table["LAE %"].item()
    direct_expenses_per_premium = tp_assumptions_table["Direct Expenses Per Premium"].item()
    investment_income_load = tp_assumptions_table["Investment Income Load"].item()
    max_loss_ratio = tp_assumptions_table["Max Loss Ratio"].item()

    # convert group cat risk and held capital from account level to location level
    df = df.with_columns(
        ((pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal") / pl.col("acc_all_perils_beazley_share_aal")) * pl.lit(gross_group_cat_risk)).fill_null(0).fill_nan(0).alias("loc_gross_group_cat_risk"),
        ((pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal") / pl.col("acc_all_perils_beazley_share_aal")) * pl.lit(held_cap)).fill_null(0).fill_nan(0).alias("loc_held_cap")
    )

    # Calculate the cost of capital
    # 1 in 250 oep is split by location based on aal (loc_aal/acc_aal)
    for peril in ("ws", "eq"):
        df = df.with_columns(
            pl.when(pl.col("acc_1_in_250_oep") == 0)
            .then((pl.col(f"loc_{peril}_beazley_share_aal") + (pl.col(f"{peril}_weight_without_avg") * pl.col("loc_nmp_beazley_share_el"))) * fire_int_cap_allocation)
            .otherwise((pl.col(f"loc_{peril}_1_in_250_oep") / pl.col("loc_gross_group_cat_risk")) * (pl.col("loc_held_cap") * cap_req * additional_group_cat_risk * 100))
            .fill_nan(0)
            .alias(f"loc_{peril}_cat_cap_allocation")
        )

        df = df.with_columns((pl.col(f"loc_{peril}_cat_cap_allocation") * return_on_cap).alias(f"loc_{peril}_cost_of_cap"))
        df = df.drop(f"loc_{peril}_cat_cap_allocation")

    for peril in ("fire", "fl", "tn", "ha", "wf", "wts"):
        df = df.with_columns((pl.col(f"loc_{peril}_beazley_share_el") * fire_int_cap_allocation * return_on_cap).alias(f"loc_{peril}_cost_of_cap"))

    # calculate indirect expense 
    if hxd.cds.layers[0].follow_lead == "Lead":
        indirect_expense = indirect_expense_lead
    else:
        indirect_expense = indirect_expense_follow

    date_time_delta = min((df["inception_date"].max() - df["inception_date"].min()).days, 365) / (expiry_date - inception_date).days

    for peril in ("fire", "ws", "eq", "fl", "tn", "ha", "wf", "wts"):
        df = df.with_columns(
            (indirect_expense * ((pl.col(f"loc_{peril}_beazley_share_received_gg_prem") / pl.col(f"loc_beazley_share_received_gg_prem").sum()) / date_time_delta))
            .alias(f"loc_{peril}_indirect_expense")
        )
    
    #calculate the SD and LAE for WS and EQ
    for peril in ("ws", "eq"):

        df = df.with_columns((pl.col("acc_all_perils_gg_sd") * (pl.col(f"loc_{peril}_beazley_share_aal") / (pl.col("acc_all_perils_beazley_share_aal")))).fill_nan(0).fill_null(0).alias(f"loc_{peril}_gg_sd"))

        df = df.with_columns(
            pl.when(pl.col("acc_1_in_250_oep") is not None)
            .then(pl.col(f"loc_{peril}_gg_sd") * sd)
            .otherwise(0)
            .alias(f"loc_{peril}_sd")
        )

        df = df.with_columns(((pl.col(f"loc_{peril}_beazley_share_aal") + ((pl.col("loc_nmp_beazley_share_el") * pl.col(f"{peril}_weight_with_avg")))) * lae_perc).fill_nan(0).fill_null(0).alias(f"loc_{peril}_lae"))

    # join on account profit per dollar of AAL which will be used to calculate RI costs     
    if hxd.cds.currencies.source_currency == "USD":
        zip_lookup = pl.from_pandas(hx.params.table_secondary_mapping).select("RI Name", "Zip Code")
        zip_lookup = zip_lookup.with_columns(pl.col("Zip Code").str.zfill(5).alias("Zip Code"))
        df = df.with_columns(pl.col("zip").str.zfill(5).alias("padded_zip"))
        df = df.with_columns(df.join(zip_lookup, left_on="padded_zip", right_on="Zip Code", how="left"))
        df = join_param_table(df, hx.params.table_profit_ceded_aal, "Profit ceded per $ AAL", "profit_ceded_per_dollar_of_aal", "Region", "RI Name", drop=True)
        df = df.drop("padded_zip")
    else:
        acc_profit_ceded_aal_non_usd = pl.from_pandas(hx.params.table_profit_ceded_aal).filter(pl.col("Region") == "Pacific NW EQ")["Profit ceded per $ AAL"].item()
        df = df.with_columns(pl.lit(acc_profit_ceded_aal_non_usd).alias("profit_ceded_per_dollar_of_aal"))  
              
    df = df.with_columns(pl.col("profit_ceded_per_dollar_of_aal").fill_nan(0).fill_null(0).alias("profit_ceded_per_dollar_of_aal"))

    # calculate RI costs for WS and EQ
    for peril in ("ws", "eq"):
        df = df.with_columns(
            (pl.col("profit_ceded_per_dollar_of_aal") * ((pl.col("loc_nmp_beazley_share_el") * pl.col(f"{peril}_weight_with_avg")) + pl.col(f"loc_{peril}_beazley_share_aal")))
            .fill_nan(0)
            .alias(f"loc_{peril}_ri_cost")
        )

    #### TP calculations ####
    for peril in ("ws", "eq"):
        df = df.with_columns(
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_aal", f"loc_{peril}_cost_of_cap", f"loc_{peril}_indirect_expense", f"loc_{peril}_lae", f"loc_{peril}_ri_cost", f"loc_{peril}_nmp_beazley_share_el") / (1 - direct_expenses_per_premium + investment_income_load))
            .alias(f"loc_{peril}_calc_1_beazley_share_gn_tp"),
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_aal", f"loc_{peril}_indirect_expense", f"loc_{peril}_sd", f"loc_{peril}_lae", f"loc_{peril}_nmp_beazley_share_el") / (1 - direct_expenses_per_premium))
            .alias(f"loc_{peril}_calc_2_beazley_share_gn_tp"),
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_aal", f"loc_{peril}_lae", f"loc_{peril}_nmp_beazley_share_el") / (max_loss_ratio))
            .alias(f"loc_{peril}_calc_3_beazley_share_gn_tp")
        )

    for peril in ("fire", "fl", "tn", "ha", "wf", "wts"):
        df = df.with_columns(
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_el", f"loc_{peril}_cost_of_cap", f"loc_{peril}_indirect_expense", f"loc_{peril}_nmp_beazley_share_el") / (1 - direct_expenses_per_premium + investment_income_load))
            .alias(f"loc_{peril}_calc_1_beazley_share_gn_tp"),
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_el", f"loc_{peril}_indirect_expense", f"loc_{peril}_nmp_beazley_share_el") / (1 - direct_expenses_per_premium))
            .alias(f"loc_{peril}_calc_2_beazley_share_gn_tp"),
            (pl.sum_horizontal(f"loc_{peril}_beazley_share_el", f"loc_{peril}_nmp_beazley_share_el") / (max_loss_ratio))
            .alias(f"loc_{peril}_calc_3_beazley_share_gn_tp")
        )
    # sum the 3 TP methods 
    df = df.with_columns(pl.sum_horizontal(*(f"loc_{peril}_calc_{tp_calc_num}_beazley_share_gn_tp" for peril in ("fire", "fl", "tn", "ha", "wf", "wts", "ws", "eq"))).alias(f"loc_calc_{tp_calc_num}_beazley_share_gn_tp") for tp_calc_num in (1, 2, 3))

    # calculating the tp on account level to calc the max prem to use for each account 
    df = df.with_columns(pl.col(f"loc_calc_{tp_calc_num}_beazley_share_gn_tp").sum().over("acc_number").alias(f"acc_calc_{tp_calc_num}_beazley_share_gn_tp") for tp_calc_num in (1, 2, 3))

    df = df.with_columns(pl.max_horizontal("acc_calc_1_beazley_share_gn_tp", "acc_calc_2_beazley_share_gn_tp", "acc_calc_3_beazley_share_gn_tp").alias("acc_selected_beazley_share_gn_tp"))

    df = df.with_columns(
        pl.when(pl.col("acc_calc_1_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
        .then(pl.col("loc_calc_1_beazley_share_gn_tp"))
        .when(pl.col("acc_calc_2_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
        .then(pl.col("loc_calc_2_beazley_share_gn_tp"))
        .when(pl.col("acc_calc_3_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
        .then(pl.col("loc_calc_3_beazley_share_gn_tp"))
        .alias("loc_selected_beazley_share_gn_tp")
    )

    for peril in ("fire", "fl", "tn", "ha", "wf", "wts", "ws", "eq"): 
        df = df.with_columns(
            pl.when(pl.col("acc_calc_1_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
            .then(pl.col(f"loc_{peril}_calc_1_beazley_share_gn_tp"))
            .when(pl.col("acc_calc_2_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
            .then(pl.col(f"loc_{peril}_calc_2_beazley_share_gn_tp"))
            .when(pl.col("acc_calc_3_beazley_share_gn_tp") == pl.col("acc_selected_beazley_share_gn_tp"))
            .then(pl.col(f"loc_{peril}_calc_3_beazley_share_gn_tp"))
            .alias(f"loc_{peril}_selected_beazley_share_gn_tp")
        )

    return df

    