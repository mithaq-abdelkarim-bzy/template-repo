import hx
import polars as pl
import numpy as np

def peril_rating_summary(hxd, df, other_data, peril):
    '''
    Calculates direct and indirect expenses, gross net premium
    '''
    assumption_1_in_250_pricing_df = hx.params.assumption_1_in_250_pricing
    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team

    non_cat_capital_alloc_init = assumption_1_in_250_pricing_df['fire_aop_init_capital_allocation'][0]  # Does look like they all use this allocation? TODO Check
    roc = assumption_1_in_250_pricing_df['roc'][0]

    capital = assumption_1_in_250_pricing_df["held_capital"][0]
    group_cat_risk = assumption_1_in_250_pricing_df["gross_group_cat_risk"][0]
    add_group_cat_risk = assumption_1_in_250_pricing_df["additional_group_cat_risk"][0]

    if hxd.policy_information.team:
        team = hxd.policy_information.team
        add_capital_req = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Corresponding Capital Required"].iloc[0])[team]
        if team == "Renewables":
            non_cat_capital_alloc = add_capital_req
        else:
            non_cat_capital_alloc = non_cat_capital_alloc_init
    else:
        add_capital_req = 0
        non_cat_capital_alloc = 0


    for index, layer in enumerate(hxd.layers, start=1):
        # Calculate cost of capital

        if (peril == "windstorm_us" or peril == "earthquake_us") and team != "Renewables" and other_data[f"cat_method_{peril}_layer{index}"] != "Proxy":
            df = df.with_columns(
                (
                    (pl.col(f"{peril}_marginal_impact_pre_uw_layer{index}") * capital / group_cat_risk * add_capital_req *
                         add_group_cat_risk * 100 * roc * hxd.policy_information.policy_length.selected)
                ).alias(f"{peril}_cost_of_capital_pre_uw_layer{index}"),
                (
                    (pl.col(f"{peril}_marginal_impact_post_uw_layer{index}") * capital / group_cat_risk * add_capital_req *
                         add_group_cat_risk * 100 * roc * hxd.policy_information.policy_length.selected)
                ).alias(f"{peril}_cost_of_capital_post_uw_layer{index}"),
            )
        else:
            df = df.with_columns(
                (
                    pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") * non_cat_capital_alloc * roc
                ).alias(f"{peril}_cost_of_capital_pre_uw_layer{index}"),
                (
                    pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") * non_cat_capital_alloc * roc
                ).alias(f"{peril}_cost_of_capital_post_uw_layer{index}")
            )

        # Calcuate percentage of expected loss for given peril
        df = df.with_columns(
            [
                (pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") / other_data[f"sum_total_expected_loss_pre_uw_layer{index}"])
                    .fill_nan(pl.lit(0))
                    .alias(f"{peril}_percent_expected_loss_pre_uw_layer{index}"),
                (pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") / other_data[f"sum_total_expected_loss_post_uw_layer{index}"])
                    .fill_nan(pl.lit(0))
                    .alias(f"{peril}_percent_expected_loss_post_uw_layer{index}"),                    
            ]

        )

        # Calculate indrect expenses per location
        if hxd.policy_information.team:
            team = hxd.policy_information.team
            indirect_expense = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Indirect Expenses Per Policy"].iloc[0])[team]
        else:
            indirect_expense = 0
        
        df = df.with_columns(
            [
                (indirect_expense * pl.col(f"{peril}_percent_expected_loss_pre_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .alias(f"{peril}_indirect_expenses_pre_uw_layer{index}"),
                (indirect_expense * pl.col(f"{peril}_percent_expected_loss_post_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .alias(f"{peril}_indirect_expenses_post_uw_layer{index}"),
            ]
        )

        # Calculate Gross Net Technical Premium
        if hxd.policy_information.team:
            direct_expense_perc = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Direct Expenses Per Premium"].iloc[0])[team]
            investment_income_perc = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Investment Income Per Premium"].iloc[0])[team]
            max_lr = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Max Loss Ratio"].iloc[0])[team]
        else:
            direct_expense_perc = 0
            investment_income_perc = 0
            max_lr = 1

        if peril == "windstorm_us" or peril == "earthquake_us":
            df = df.with_columns(
                [
                    ((pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_cost_of_capital_pre_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_pre_uw_layer{index}") + 
                        pl.col(f"{peril}_ri_cost_pre_uw_layer{index}") + pl.col(f"{peril}_lae_pre_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_1_pre_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_pre_uw_layer{index}") + pl.col(f"{peril}_lae_pre_uw_layer{index}") + pl.col(f"{peril}_sd_pre_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_2_pre_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_lae_pre_uw_layer{index}")) / max_lr)
                        .alias(f"{peril}_gn_technical_prem_3_pre_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_cost_of_capital_post_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_post_uw_layer{index}") + 
                        pl.col(f"{peril}_ri_cost_post_uw_layer{index}") + pl.col(f"{peril}_lae_post_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_1_post_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_post_uw_layer{index}") + pl.col(f"{peril}_lae_post_uw_layer{index}") + pl.col(f"{peril}_sd_post_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_2_post_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_lae_post_uw_layer{index}")) / max_lr)
                        .alias(f"{peril}_gn_technical_prem_3_post_uw_layer{index}"),
                ]
            )
        else:
            df = df.with_columns(
                [
                    ((pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_cost_of_capital_pre_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_pre_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_1_pre_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_pre_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_2_pre_uw_layer{index}"),
                    (pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") / max_lr)
                        .alias(f"{peril}_gn_technical_prem_3_pre_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_cost_of_capital_post_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_post_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_1_post_uw_layer{index}"),
                    ((pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") + pl.col(f"{peril}_indirect_expenses_post_uw_layer{index}"))
                        / (1 - direct_expense_perc + investment_income_perc))
                        .alias(f"{peril}_gn_technical_prem_2_post_uw_layer{index}"),
                    (pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") / max_lr)
                        .alias(f"{peril}_gn_technical_prem_3_post_uw_layer{index}"),
                ]
            )
            
    return df


def peril_rating_assignment(hxd, df, other_data):
    cb_countries = pl.from_pandas(hx.params.intl_base_rates)
    cb_countries = set(cb_countries.filter(pl.col("Continent") == "Caribbean").select("Country").to_series().to_list())

    for status in ['pre', 'post']:
        for index, layer in enumerate(hxd.layers, start=1):
            df = df.with_columns(
                pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                    .then(pl.col(f"earthquake_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"earthquake_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"earthquake_cost_of_capital_{status}_uw_layer{index}"),
                pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"flood_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"flood_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"flood_cost_of_capital_{status}_uw_layer{index}"),
                pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"hail_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"hail_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"hail_cost_of_capital_{status}_uw_layer{index}"),
                pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"tornado_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"tornado_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"tornado_cost_of_capital_{status}_uw_layer{index}"),
                pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"wildfire_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"wildfire_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"wildfire_cost_of_capital_{status}_uw_layer{index}"),
                pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                    .then(pl.col(f"windstorm_us_cost_of_capital_{status}_uw_layer{index}"))
                    .otherwise(pl.col(f"windstorm_intl_cost_of_capital_{status}_uw_layer{index}"))
                    .alias(f"windstorm_cost_of_capital_{status}_uw_layer{index}"),
            )

    if hxd.policy_information.small_schedule_model:
        for status in ['pre', 'post']:
            for index, layer in enumerate(hxd.layers, start=1):
                eq_coc_list = df[f"earthquake_cost_of_capital_{status}_uw_layer{index}"].to_list()
                fl_coc_list = df[f"flood_cost_of_capital_{status}_uw_layer{index}"].to_list()
                ha_coc_list = df[f"hail_cost_of_capital_{status}_uw_layer{index}"].to_list()
                tn_coc_list = df[f"tornado_cost_of_capital_{status}_uw_layer{index}"].to_list()
                wf_coc_list = df[f"wildfire_cost_of_capital_{status}_uw_layer{index}"].to_list()
                ws_coc_list = df[f"windstorm_cost_of_capital_{status}_uw_layer{index}"].to_list()

                for i, row in enumerate(hxd.schedule.schedule_table):
                    target_output_by_layer = row.output_by_layer[index-1]

                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_eq", eq_coc_list[i])
                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_fl", fl_coc_list[i])
                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_ha", ha_coc_list[i])
                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_tn", tn_coc_list[i])
                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_wf", wf_coc_list[i])
                    setattr(target_output_by_layer, f"coc_{status}_uw_usd_100_ws", ws_coc_list[i])

    elif other_data["large_model_assign"]:
        for index, layer in enumerate(hxd.layers, start=1):
            eq_coc_list = df[f"earthquake_cost_of_capital_pre_uw_layer{index}"].to_list()
            fl_coc_list = df[f"flood_cost_of_capital_pre_uw_layer{index}"].to_list()
            ha_coc_list = df[f"hail_cost_of_capital_pre_uw_layer{index}"].to_list()
            tn_coc_list = df[f"tornado_cost_of_capital_pre_uw_layer{index}"].to_list()
            wf_coc_list = df[f"wildfire_cost_of_capital_pre_uw_layer{index}"].to_list()
            ws_coc_list = df[f"windstorm_cost_of_capital_pre_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.coc_pre_uw_usd_100_eq = eq_coc_list[i]
                target_output_by_layer.coc_pre_uw_usd_100_fl = fl_coc_list[i]
                target_output_by_layer.coc_pre_uw_usd_100_ha = ha_coc_list[i]
                target_output_by_layer.coc_pre_uw_usd_100_tn = tn_coc_list[i]
                target_output_by_layer.coc_pre_uw_usd_100_wf = wf_coc_list[i]
                target_output_by_layer.coc_pre_uw_usd_100_ws = ws_coc_list[i]

    return df
