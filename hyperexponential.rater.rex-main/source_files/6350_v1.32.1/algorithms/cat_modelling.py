import hx
import polars as pl
import pandas as pd

def cat_method_calc(hxd, df, other_data):
    '''
    Function runs in rater to decide the cat method used and adjusted value
    '''

    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team
    exchange_rate = hxd.policy_information.exchange_rate or 1
    
    ## AT Edit:
    us_cat_uplift = 1 + (assumption_1_in_250_team_df.loc[assumption_1_in_250_team_df["Field"] == "CAT Uplift",f"{hxd.policy_information.team}"].iloc[0] if hxd.policy_information.team else 0)

    for index, layer in enumerate(hxd.layers, start=1):
        # Decide to use proxy/simulation/rms
        if (not sum((layer.quake_aal or 0, layer.intl_quake_aal or 0, layer.simulated_result.us_quake_aal or 0, layer.simulated_result.intl_quake_aal or 0)) or
            (not layer.sim_used and not layer.quake_aal and not layer.intl_quake_aal)):
            other_data[f"cat_method_earthquake_us_layer{index}"] = "Proxy"
            other_data[f"cat_method_earthquake_intl_layer{index}"] = "Proxy"
        elif layer.sim_used:
            other_data[f"cat_method_earthquake_us_layer{index}"] = "Sim"
            other_data[f"cat_method_earthquake_intl_layer{index}"] = "Sim"
        else:
            other_data[f"cat_method_earthquake_us_layer{index}"] = "RMS"
            other_data[f"cat_method_earthquake_intl_layer{index}"] = "RMS"
        
        if (not sum((layer.wind_aal or 0, layer.intl_wind_aal or 0, layer.simulated_result.us_wind_aal or 0, layer.simulated_result.intl_wind_aal or 0)) or
            (not layer.sim_used and not layer.wind_aal and not layer.intl_wind_aal)):
            other_data[f"cat_method_windstorm_us_layer{index}"] = "Proxy"
            other_data[f"cat_method_windstorm_intl_layer{index}"] = "Proxy"
        elif layer.sim_used:
            other_data[f"cat_method_windstorm_us_layer{index}"] = "Sim"
            other_data[f"cat_method_windstorm_intl_layer{index}"] = "Sim"
        else: 
            other_data[f"cat_method_windstorm_us_layer{index}"] = "RMS"
            other_data[f"cat_method_windstorm_intl_layer{index}"] = "RMS"

        # Loads the correct AAL/SD to risk appetite and summary table
        # layer.simulated_result AALs are in policy ccy. They are converted to USD and temporarily stored in USD in other_data for future functions, but the layer.risk_appetite_summary output is converted back to pol ccy
        ## US
        other_data[f"earthquake_us_aal_adjusted_layer{index}"] = ((layer.simulated_result.us_quake_aal if layer.sim_used else layer.quake_aal) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"windstorm_us_aal_adjusted_layer{index}"] = ((layer.simulated_result.us_wind_aal if layer.sim_used else layer.wind_aal) or 0) * other_data["inflation"] * us_cat_uplift / exchange_rate

        other_data[f"earthquake_us_sd_adjusted_layer{index}"] = ((layer.simulated_result.us_quake_sd if layer.sim_used else layer.quake_sd) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"windstorm_us_sd_adjusted_layer{index}"] = ((layer.simulated_result.us_wind_sd if layer.sim_used else layer.wind_sd) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"all_perils_sd_adjusted_layer{index}"] = ((layer.simulated_result.us_all_perils_sd if layer.sim_used else layer.all_perils_sd) or 0) * other_data["inflation"] / exchange_rate

        perc_of_aal_denominator = other_data[f"earthquake_us_aal_adjusted_layer{index}"] + other_data[f"windstorm_us_aal_adjusted_layer{index}"]
        earthquake_us_perc_of_aal = other_data[f"earthquake_us_aal_adjusted_layer{index}"] / perc_of_aal_denominator if perc_of_aal_denominator else 0
        windstorm_us_perc_of_aal = other_data[f"windstorm_us_aal_adjusted_layer{index}"] / perc_of_aal_denominator if perc_of_aal_denominator else 0

        earthquake_us_allocation_1_in_250 = ((layer.simulated_result.oep_impact_1_in_250 if layer.sim_used else layer.mi_1_in_250_oep_pt) or 0) * earthquake_us_perc_of_aal / exchange_rate
        windstorm_us_allocation_1_in_250 = ((layer.simulated_result.oep_impact_1_in_250 if layer.sim_used else layer.mi_1_in_250_oep_pt) or 0) * windstorm_us_perc_of_aal / exchange_rate

        other_data[f"earthquake_us_1_in_250_adjusted_layer{index}"] = earthquake_us_allocation_1_in_250 * other_data["inflation"]
        other_data[f"windstorm_us_1_in_250_adjusted_layer{index}"] = windstorm_us_allocation_1_in_250 * other_data["inflation"]

        other_data[f"earthquake_us_ri_cost_layer{index}"] = layer.ri_cost.quake_us_ri_cost or 0
        other_data[f"windstorm_us_ri_cost_layer{index}"] = layer.ri_cost.wind_us_ri_cost or 0

        layer.risk_appetite_summary.us_wind_aal = other_data[f"windstorm_us_aal_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.us_quake_aal = other_data[f"earthquake_us_aal_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.us_all_perils_aal = layer.risk_appetite_summary.us_wind_aal + layer.risk_appetite_summary.us_quake_aal

        layer.risk_appetite_summary.us_wind_sd = other_data[f"windstorm_us_sd_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.us_quake_sd = other_data[f"earthquake_us_sd_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.us_all_perils_sd = other_data[f"all_perils_sd_adjusted_layer{index}"] * exchange_rate

        layer.risk_appetite_summary.aep_impact_1_in_10 = ((layer.simulated_result.aep_impact_1_in_10 if layer.sim_used else layer.mi_1_in_10_aep_pt) or 0) * other_data["inflation"]
        layer.risk_appetite_summary.oep_impact_1_in_250 = ((layer.simulated_result.oep_impact_1_in_250 if layer.sim_used else layer.mi_1_in_250_oep_pt) or 0) * other_data["inflation"]

        line = (layer.written_line_perc if layer.status in {'Bound', 'MTA', 'Cancellation'} else layer.quoted_line_perc) or 1
        layer.risk_appetite_summary.aep_impact_1_in_10_wrt_line = ((layer.simulated_result.aep_impact_1_in_10_wrt_line if layer.sim_used else (layer.mi_1_in_10_aep_pt or 0) * line) or 0) * other_data["inflation"]
        layer.risk_appetite_summary.oep_impact_1_in_250_wrt_line = ((layer.simulated_result.oep_impact_1_in_250_wrt_line if layer.sim_used else (layer.mi_1_in_250_oep_pt or 0) * line) or 0) * other_data["inflation"]


        other_data[f'aep_impact_layer{index}'] = layer.risk_appetite_summary.aep_impact_1_in_10 / exchange_rate
        other_data[f'oep_impact_layer{index}'] = layer.risk_appetite_summary.oep_impact_1_in_250 / exchange_rate

        ## Intl
        other_data[f"earthquake_intl_aal_adjusted_layer{index}"] = ((layer.simulated_result.intl_quake_aal if layer.sim_used else layer.intl_quake_aal) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"windstorm_intl_aal_adjusted_layer{index}"] = ((layer.simulated_result.intl_wind_aal if layer.sim_used else layer.intl_wind_aal) or 0) * other_data["inflation"] / exchange_rate

        other_data[f"earthquake_intl_sd_adjusted_layer{index}"] = ((layer.simulated_result.intl_quake_sd if layer.sim_used else layer.intl_quake_sd) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"windstorm_intl_sd_adjusted_layer{index}"] = ((layer.simulated_result.intl_wind_sd if layer.sim_used else layer.intl_wind_sd) or 0) * other_data["inflation"] / exchange_rate
        other_data[f"all_perils_intl_sd_adjusted_layer{index}"] = ((layer.simulated_result.intl_all_perils_sd if layer.sim_used else layer.intl_all_perils_sd) or 0) * other_data["inflation"] / exchange_rate

        layer.risk_appetite_summary.intl_wind_aal = other_data[f"windstorm_intl_aal_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.intl_quake_aal = other_data[f"earthquake_intl_aal_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.intl_all_perils_aal = layer.risk_appetite_summary.intl_wind_aal + layer.risk_appetite_summary.intl_quake_aal

        layer.risk_appetite_summary.intl_wind_sd = other_data[f"windstorm_intl_sd_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.intl_quake_sd = other_data[f"earthquake_intl_sd_adjusted_layer{index}"] * exchange_rate
        layer.risk_appetite_summary.intl_all_perils_sd = other_data[f"all_perils_intl_sd_adjusted_layer{index}"] * exchange_rate

        # International country AALs, apply inflation adjustment by country
        if len(layer.simulated_result_intl_country) > 0:
            cols = ['country', 'aal_ws', 'aal_eq']
            intl_country_aals = pl.DataFrame([{column: getattr(row, column) for column in cols} for row in layer.simulated_result_intl_country])
            intl_country_aals = intl_country_aals.with_columns(pl.col(cols).fill_null(0))      # for None/nulls
            intl_country_aals = intl_country_aals.with_columns([
                (pl.col('aal_ws') > 0).alias('show_ws'),
                (pl.col('aal_eq') > 0).alias('show_eq'),
                (pl.col("aal_ws") * other_data["inflation"]).alias("aal_ws"),
                (pl.col("aal_eq") * other_data["inflation"]).alias("aal_eq"),
            ])
            layer.risk_appetite_summary_intl_country = intl_country_aals.to_pandas().to_dict("records")
    
    return df


def cat_method_expected_loss(hxd, df, other_data, cat_peril):
    '''
    Calculate expected loss for cat method
    '''
    
    cache = {}

    intl_cat_model_coverage = hx.params.intl_cat_model_coverage
    intl_cat_model_coverage["WS"] = intl_cat_model_coverage["WS"].astype(bool)
    intl_cat_model_coverage["EQ"] = intl_cat_model_coverage["EQ"].astype(bool)
    intl_cat_model_coverage_pl = pl.from_pandas(intl_cat_model_coverage).rename({"Country": "country", "WS": "windstorm_intl_include_in_proportion_calc", "EQ": "earthquake_intl_include_in_proportion_calc"})

    # map intl perils to uw adjustment names:
    adj_map = {
        "windstorm_intl": "ws",
        "earthquake_intl": "eq"
    }

    for index, layer in enumerate(hxd.layers, start=1):
        for peril in cat_peril:
            ## Replace location-level cat expected loss with simulated / RMS expected loss, allocated to location 
            
            # Assign which countries to include in proportion calculation
            if peril in ["windstorm_intl", "earthquake_intl"]:
                df = df.join(intl_cat_model_coverage_pl[["country", f"{peril}_include_in_proportion_calc"]], on = "country", how="left")
                df = df.rename({f"{peril}_include_in_proportion_calc": f"{peril}_include_in_proportion_calc_layer{index}"})
            else: 
                df = df.with_columns([pl.lit(True).alias(f"{peril}_include_in_proportion_calc_layer{index}")])

            # calculate total peril proxy-method expected loss for locations which are covered by simulation / RMS 
            cache[f"{peril}_sum_el_pre_uw_layer{index}"] = df.filter(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))[f"{peril}_total_expected_loss_pre_uw_layer{index}"].sum()
            cache[f"{peril}_sum_el_post_uw_layer{index}"] = df.filter(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))[f"{peril}_total_expected_loss_post_uw_layer{index}"].sum()
            
            # calculate the location contribution to the total peril proxy expected loss for locations which are modelled by simulation / RMS
            df = df.with_columns([
                        (
                        pl.when(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))
                            .then(pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") / cache[f"{peril}_sum_el_pre_uw_layer{index}"])
                            .otherwise(0)
                            .fill_nan(0)
                            .alias(f"{peril}_percent_expected_loss_pre_uw_layer{index}")
                        ),
                        (
                        pl.when(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))
                            .then(pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") / cache[f"{peril}_sum_el_post_uw_layer{index}"])
                            .otherwise(0)
                            .fill_nan(0)
                            .alias(f"{peril}_percent_expected_loss_post_uw_layer{index}")
                        )
                    ])

            # for locations modelled by simulation / RMS, allocate the selected AAL to those locations, else keep the same expected loss
            if other_data[f"cat_method_{peril}_layer{index}"] in {"Sim", "RMS"}:
                
                pre_uw_expr = (
                    pl.when(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))
                            .then(other_data[f"{peril}_aal_adjusted_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_pre_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                            .otherwise(pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}"))
                            .alias(f"{peril}_total_expected_loss_pre_uw_layer{index}")
                )

                # Apply intl UW adjustments 
                post_uw_expr_base = (
                    other_data[f"{peril}_aal_adjusted_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_post_uw_layer{index}") * hxd.policy_information.policy_length.selected
                )

                if peril in adj_map:
                    adj_name = adj_map[peril]
                    post_uw_expr_base = post_uw_expr_base * (1 + other_data[f"{adj_name}_uw_adjustments"])

                post_uw_expr = (
                    pl.when(pl.col(f"{peril}_include_in_proportion_calc_layer{index}"))
                            .then(post_uw_expr_base)
                            .otherwise(pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}"))
                            .alias(f"{peril}_total_expected_loss_post_uw_layer{index}")
                )

                df = df.with_columns([pre_uw_expr, post_uw_expr])
    
    return df 

def cat_method_us_mi_tp_components(hxd, df, other_data, cat_peril):
    '''
    Calculate peril level marginal impacts and allocate MIs and technical premium assumptions at location level 
    '''

    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team

    for index, layer in enumerate(hxd.layers, start=1):
        for peril in cat_peril:
            # Calculate marginal impact
            df = df.with_columns(
                        (pl.col(f"{peril}_percent_expected_loss_pre_uw_layer{index}") * other_data[f"{peril}_1_in_250_adjusted_layer{index}"])
                            .alias(f"{peril}_marginal_impact_pre_uw_layer{index}"),
                        (pl.col(f"{peril}_percent_expected_loss_post_uw_layer{index}") * other_data[f"{peril}_1_in_250_adjusted_layer{index}"])
                            .alias(f"{peril}_marginal_impact_post_uw_layer{index}")
                    )

            # Calculate LAE, 10 percent SD and RI Cost
            team = hxd.policy_information.team
            lae_perc = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "LAE %"].iloc[0])[team] if hxd.policy_information.team else 0
            cov = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "CoV"].iloc[0])[team] if hxd.policy_information.team else 0
            sd = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Standard Deviation"].iloc[0])[team] if hxd.policy_information.team else 0

            df = df.with_columns(
                (pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") * lae_perc).alias(f"{peril}_lae_pre_uw_layer{index}"),
                pl.when(pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") == 0)
                    .then(0)
                    .when(other_data[f"cat_method_{peril}_layer{index}"] == "Proxy")
                    .then(sd * cov * pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}"))
                    .otherwise(sd * other_data[f"{peril}_sd_adjusted_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_pre_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .alias(f"{peril}_sd_pre_uw_layer{index}"),
                pl.when(bool(other_data[f"{peril}_ri_cost_layer{index}"]) & (other_data[f"cat_method_{peril}_layer{index}"] != "Proxy"))
                    .then(other_data[f"{peril}_ri_cost_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_pre_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .otherwise(pl.col(f"{peril}_total_expected_loss_pre_uw_layer{index}") * pl.col(f"{peril}_profit_ceded_ratio"))
                    .alias(f"{peril}_ri_cost_pre_uw_layer{index}"),
                (pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") * lae_perc).alias(f"{peril}_lae_post_uw_layer{index}"),
                pl.when(pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") == 0)
                    .then(0)
                    .when(other_data[f"cat_method_{peril}_layer{index}"] == "Proxy")
                    .then(sd * cov * pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}"))
                    .otherwise(sd * other_data[f"{peril}_sd_adjusted_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_post_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .alias(f"{peril}_sd_post_uw_layer{index}"),
                pl.when(bool(other_data[f"{peril}_ri_cost_layer{index}"]) & (other_data[f"cat_method_{peril}_layer{index}"] != "Proxy"))
                    .then(other_data[f"{peril}_ri_cost_layer{index}"] * pl.col(f"{peril}_percent_expected_loss_post_uw_layer{index}") * hxd.policy_information.policy_length.selected)
                    .otherwise(pl.col(f"{peril}_total_expected_loss_post_uw_layer{index}") * pl.col(f"{peril}_profit_ceded_ratio"))
                    .alias(f"{peril}_ri_cost_post_uw_layer{index}"),
            )

    return df


def cat_method_hxd_assignment(hxd, df, other_data):
    cb_countries = pl.from_pandas(hx.params.intl_base_rates)
    cb_countries = set(cb_countries.filter(pl.col("Continent") == "Caribbean").select("Country").to_series().to_list())
    
    for index, layer in enumerate(hxd.layers, start=1):
        df = df.with_columns(
            pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                .then(pl.col(f"windstorm_us_total_expected_loss_pre_uw_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_total_expected_loss_pre_uw_layer{index}"))
                .alias(f"windstorm_total_expected_loss_pre_uw_layer{index}"),
            pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                .then(pl.col(f"windstorm_us_total_expected_loss_post_uw_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_total_expected_loss_post_uw_layer{index}"))
                .alias(f"windstorm_total_expected_loss_post_uw_layer{index}"),
            pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                .then(pl.col(f"earthquake_us_total_expected_loss_pre_uw_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"))
                .alias(f"earthquake_total_expected_loss_pre_uw_layer{index}"),
            pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                .then(pl.col(f"earthquake_us_total_expected_loss_post_uw_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_total_expected_loss_post_uw_layer{index}"))
                .alias(f"earthquake_total_expected_loss_post_uw_layer{index}"),       
        )

    if hxd.policy_information.small_schedule_model:
        for status in ['pre', 'post']:
            for index, layer in enumerate(hxd.layers, start=1):
                ri_cost_eq_list = df[f"earthquake_us_ri_cost_{status}_uw_layer{index}"].to_list()
                ri_cost_ws_list = df[f"windstorm_us_ri_cost_{status}_uw_layer{index}"].to_list()
                sd_eq_list = df[f"earthquake_us_sd_{status}_uw_layer{index}"].to_list()
                sd_ws_list = df[f"windstorm_us_sd_{status}_uw_layer{index}"].to_list()
                lae_eq_list = df[f"earthquake_us_lae_{status}_uw_layer{index}"]
                lae_ws_list = df[f"windstorm_us_lae_{status}_uw_layer{index}"]
                aal_eq_us_list = df[f"earthquake_us_total_expected_loss_{status}_uw_layer{index}"]
                aal_ws_us_list = df[f"windstorm_us_total_expected_loss_{status}_uw_layer{index}"]
                aal_eq_intl_list = (
                    df.select(
                        pl.when(pl.col(f"earthquake_intl_include_in_proportion_calc_layer{index}"))
                        .then(pl.col(f"earthquake_intl_total_expected_loss_{status}_uw_layer{index}"))
                        .otherwise(0)
                        .alias("aal_eq_intl")
                    )
                    .to_series().to_list()
                )
                aal_ws_intl_list = (
                    df.select(
                        pl.when(pl.col(f"windstorm_intl_include_in_proportion_calc_layer{index}"))
                        .then(pl.col(f"windstorm_intl_total_expected_loss_{status}_uw_layer{index}"))
                        .otherwise(0)
                        .alias("aal_ws_intl")
                    )
                    .to_series().to_list()
                )
                windstorm_el_uw_list = df[f"windstorm_total_expected_loss_{status}_uw_layer{index}"].to_list()
                earthquake_el_uw_list = df[f"earthquake_total_expected_loss_{status}_uw_layer{index}"].to_list()

                for i, row in enumerate(hxd.schedule.schedule_table):
                    target_output_by_layer = row.output_by_layer[index-1]

                    setattr(target_output_by_layer, f"ri_cost_{status}_uw_eq_usd100", ri_cost_eq_list[i])
                    setattr(target_output_by_layer, f"ri_cost_{status}_uw_ws_usd100", ri_cost_ws_list[i])
                    setattr(target_output_by_layer, f"sd_{status}_uw_eq_usd100", sd_eq_list[i])
                    setattr(target_output_by_layer, f"sd_{status}_uw_ws_usd100", sd_ws_list[i])
                    setattr(target_output_by_layer, f"lae_{status}_uw_eq_usd100", lae_eq_list[i])
                    setattr(target_output_by_layer, f"lae_{status}_uw_ws_usd100", lae_ws_list[i])
                    setattr(target_output_by_layer, f"aal_{status}_uw_eq_us_usd_100", (aal_eq_us_list[i] if other_data[f"cat_method_earthquake_us_layer{index}"] != "Proxy" else 0))
                    setattr(target_output_by_layer, f"aal_{status}_uw_ws_us_usd_100", (aal_ws_us_list[i] if other_data[f"cat_method_windstorm_us_layer{index}"] != "Proxy" else 0))
                    setattr(target_output_by_layer, f"aal_{status}_uw_eq_intl_usd_100", (aal_eq_intl_list[i] if other_data[f"cat_method_earthquake_intl_layer{index}"] != "Proxy" else 0))
                    setattr(target_output_by_layer, f"aal_{status}_uw_ws_intl_usd_100", (aal_ws_intl_list[i] if other_data[f"cat_method_windstorm_intl_layer{index}"] != "Proxy" else 0))
                    setattr(target_output_by_layer, f"el_{status}_uw_usd_100_ws", windstorm_el_uw_list[i])
                    setattr(target_output_by_layer, f"el_{status}_uw_usd_100_eq", earthquake_el_uw_list[i])
    
    elif other_data["large_model_assign"]:
        for index, layer in enumerate(hxd.layers, start=1):
            ri_cost_eq_list = df[f"earthquake_us_ri_cost_pre_uw_layer{index}"].to_list()
            ri_cost_ws_list = df[f"windstorm_us_ri_cost_pre_uw_layer{index}"].to_list()
            lae_eq_list = df[f"earthquake_us_lae_pre_uw_layer{index}"]
            lae_ws_list = df[f"windstorm_us_lae_pre_uw_layer{index}"]
            aal_eq_us_list = df[f"earthquake_us_total_expected_loss_pre_uw_layer{index}"]
            aal_ws_us_list = df[f"windstorm_us_total_expected_loss_pre_uw_layer{index}"]
            aal_eq_intl_list = (
                    df.select(
                        pl.when(pl.col(f"earthquake_intl_include_in_proportion_calc_layer{index}"))
                        .then(pl.col(f"earthquake_intl_total_expected_loss_pre_uw_layer{index}"))
                        .otherwise(0)
                        .alias("aal_eq_intl")
                    )
                    .to_series().to_list()
                )
            aal_ws_intl_list = (
                    df.select(
                        pl.when(pl.col(f"windstorm_intl_include_in_proportion_calc_layer{index}"))
                        .then(pl.col(f"windstorm_intl_total_expected_loss_pre_uw_layer{index}"))
                        .otherwise(0)
                        .alias("aal_ws_intl")
                    )
                    .to_series().to_list()
                )           
            windstorm_el_uw_list = df[f"windstorm_total_expected_loss_pre_uw_layer{index}"].to_list()
            earthquake_el_uw_list = df[f"earthquake_total_expected_loss_pre_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.large_schedule_output):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.ri_cost_pre_uw_eq_usd100 = ri_cost_eq_list[i]
                target_output_by_layer.ri_cost_pre_uw_ws_usd100 = ri_cost_ws_list[i]
                target_output_by_layer.lae_pre_uw_eq_usd100 = lae_eq_list[i]
                target_output_by_layer.lae_pre_uw_ws_usd100 = lae_ws_list[i]
                target_output_by_layer.aal_pre_uw_eq_us_usd_100 = aal_eq_us_list[i]
                target_output_by_layer.aal_pre_uw_ws_us_usd_100 = aal_ws_us_list[i]
                target_output_by_layer.aal_pre_uw_eq_intl_usd_100 = aal_eq_intl_list[i]
                target_output_by_layer.aal_pre_uw_ws_intl_usd_100 = aal_ws_intl_list[i]
                target_output_by_layer.el_pre_uw_usd_100_ws = windstorm_el_uw_list[i]
                target_output_by_layer.el_pre_uw_usd_100_eq = earthquake_el_uw_list[i]

    return df

def drop_cat_method_columns(hxd, df, other_data):
    df = df.drop(["earthquake_us_profit_ceded_ratio", "windstorm_us_profit_ceded_ratio"])
    return df
