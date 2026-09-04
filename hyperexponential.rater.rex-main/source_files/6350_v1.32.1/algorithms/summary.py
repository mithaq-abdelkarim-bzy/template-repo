import hx
import polars as pl
from operator import attrgetter
import math
from itertools import chain
import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap, MiniMap, Search, Geocoder, DualMap
from algorithms.account_segmentation import millify, generate_street_view_href, read_geojson
# from data_schema.dropdown_list import climate_protection_measures_response, climate_awareness_response

def total_expected_loss_summary(hxd, df, other_data, perils):
    for index, layer in enumerate(hxd.layers, start=1):
        # Calculates total expected loss, aggregated from all perils
        df = df.with_columns(
            df.select([f"{peril}_total_expected_loss_pre_uw_layer{index}" for peril in perils]).sum(axis=1)\
                .alias(f"all_total_expected_loss_pre_uw_layer{index}"),
            df.select([f"{peril}_total_expected_loss_post_uw_layer{index}" for peril in perils]).sum(axis=1)\
                .alias(f"all_total_expected_loss_post_uw_layer{index}")
            )

        other_data[f"sum_total_expected_loss_pre_uw_layer{index}"] = df[f"all_total_expected_loss_pre_uw_layer{index}"].sum()
        other_data[f"sum_total_expected_loss_post_uw_layer{index}"] = df[f"all_total_expected_loss_post_uw_layer{index}"].sum()

        # Assign to backend nodes
        if hxd.policy_information.small_schedule_model:
            el_pre_uw_total_list = df[f"all_total_expected_loss_pre_uw_layer{index}"].to_list()
            el_post_uw_total_list = df[f"all_total_expected_loss_post_uw_layer{index}"].to_list()

            for i, row in enumerate(hxd.schedule.schedule_table):
                target_output_by_layer = row.output_by_layer[index-1]

                target_output_by_layer.el_pre_uw_usd_100_total = el_pre_uw_total_list[i]
                target_output_by_layer.el_post_uw_usd_100_total = el_post_uw_total_list[i]

    return df, other_data


def premium_summary(hxd, df, other_data, peril_node_names):
    '''
    Select which premium calculation method for gross net premium and calculates the GG premium
    '''

    assumption_1_in_250_team_df = hx.params.assumption_1_in_250_team

    if hxd.policy_information.team:
        team = hxd.policy_information.team
        direct_expense_perc = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Direct Expenses Per Premium"].iloc[0])[team]
        investment_income_perc = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Investment Income Per Premium"].iloc[0])[team]
        target_loss_ratio = (assumption_1_in_250_team_df[assumption_1_in_250_team_df['Field'] == "Target Loss Ratio"].iloc[0])[team]
    else:
        direct_expense_perc = 0
        investment_income_perc = 0
        target_loss_ratio = 0.7

    # Pre UW Adjustment
    for index, layer in enumerate(hxd.layers, start=1):
        other_data[f'achieved_premium_100_gg_usd_layer{index}'] = (layer.achieved_premium_100_gg or 0) / hxd.policy_information.exchange_rate if hxd.policy_information.exchange_rate else 0
        
        
        MAX_CALC_METHOD=3
        df = df.with_columns(
            [
                df.select(
                        [f"{peril}_gn_technical_prem_{method}_pre_uw_layer{index}" for peril in peril_node_names]
                    ).sum(axis=1).alias(f"total_gn_technical_prem_{method}_pre_uw_layer{index}")
                for method in range(1, MAX_CALC_METHOD+1)
            ] + \
            [
                df.select(
                        [f"{peril}_gn_technical_prem_{method}_post_uw_layer{index}" for peril in peril_node_names]
                    ).sum(axis=1).alias(f"total_gn_technical_prem_{method}_post_uw_layer{index}")
                for method in range(1, MAX_CALC_METHOD+1)
            ]
        )

        values = [(df[f"total_gn_technical_prem_{method}_pre_uw_layer{index}"].sum() or 0) for method in range(1, MAX_CALC_METHOD+1)]
        pre_uw_selected_method = values.index(max(values)) + 1

        values = [(df[f"total_gn_technical_prem_{method}_post_uw_layer{index}"].sum() or 0) for method in range(1, MAX_CALC_METHOD+1)]
        post_uw_selected_method = values.index(max(values)) + 1

        other_data[f'pre_uw_selected_method_layer{index}'] = pre_uw_selected_method
        other_data[f'post_uw_selected_method_layer{index}'] = post_uw_selected_method
        
        for peril in peril_node_names:
            # Calculates GG Technical premium (pre UW adjustment)
            gn_technical_prem_final_pre_uw = (df[f"{peril}_gn_technical_prem_{pre_uw_selected_method}_pre_uw_layer{index}"].sum() or 0)
            other_data[f'{peril}_gn_technical_premium_pre_uw_layer{index}'] = gn_technical_prem_final_pre_uw
            other_data[f'{peril}_gg_technical_premium_pre_uw_layer{index}'] = gn_technical_prem_final_pre_uw / (1 - layer.brokerage) if layer.brokerage != 1 else 0
            
            # Calculates GG Technical premium (post UW adjustment)
            gn_technical_prem_final_post_uw = (df[f"{peril}_gn_technical_prem_{post_uw_selected_method}_post_uw_layer{index}"].sum() or 0)
            other_data[f'{peril}_gn_technical_premium_post_uw_layer{index}'] = gn_technical_prem_final_post_uw
            other_data[f'{peril}_gg_technical_premium_post_uw_layer{index}'] = gn_technical_prem_final_post_uw / (1 - layer.brokerage) if layer.brokerage != 1 else 0

            # Calculates Expected Loss (pre UW adjustment)
            expected_loss_final_pre_uw = (df[f"{peril}_total_expected_loss_pre_uw_layer{index}"].sum() or 0)
            other_data[f'{peril}_expected_loss_pre_uw_layer{index}'] = expected_loss_final_pre_uw

            # Calculates Expected Loss (post UW adjustment)
            expected_loss_final_post_uw = (df[f"{peril}_total_expected_loss_post_uw_layer{index}"].sum() or 0)
            other_data[f'{peril}_expected_loss_post_uw_layer{index}'] = expected_loss_final_post_uw

        # Splits fire between US and international
        gn_technical_prem_final_post_uw = (sum(df.filter(pl.col("country") == "United States")[f"fire_gn_technical_prem_{post_uw_selected_method}_post_uw_layer{index}"]) or 0)
        other_data[f'fire_us_gg_technical_premium_post_uw_layer{index}'] = gn_technical_prem_final_post_uw / (1 - layer.brokerage) if layer.brokerage != 1 else 0

        gn_technical_prem_final_post_uw = (sum(df.filter(pl.col("country") != "United States")[f"fire_gn_technical_prem_{post_uw_selected_method}_post_uw_layer{index}"]) or 0)
        other_data[f'fire_intl_gg_technical_premium_post_uw_layer{index}'] = gn_technical_prem_final_post_uw / (1 - layer.brokerage) if layer.brokerage != 1 else 0

        # TP components
        other_data[f'total_coc_pre_uw_layer{index}'] = sum([df[f"{peril}_cost_of_capital_pre_uw_layer{index}"].sum() or 0 for peril in peril_node_names])
        other_data[f'total_indirect_expenses_pre_uw_layer{index}'] = sum([df[f"{peril}_indirect_expenses_pre_uw_layer{index}"].sum() or 0 for peril in peril_node_names])
        other_data[f'total_lae_pre_uw_layer{index}'] = sum([df[f"{peril}_lae_pre_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])
        other_data[f'total_ri_pre_uw_layer{index}'] = sum([df[f"{peril}_ri_cost_pre_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])
        other_data[f'total_sd_pre_uw_layer{index}'] = sum([df[f"{peril}_sd_pre_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])

        other_data[f'total_coc_post_uw_layer{index}'] = sum([df[f"{peril}_cost_of_capital_post_uw_layer{index}"].sum() or 0 for peril in peril_node_names])
        other_data[f'total_indirect_expenses_post_uw_layer{index}'] = sum([df[f"{peril}_indirect_expenses_post_uw_layer{index}"].sum() or 0 for peril in peril_node_names])
        other_data[f'total_lae_post_uw_layer{index}'] = sum([df[f"{peril}_lae_post_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])
        other_data[f'total_ri_post_uw_layer{index}'] = sum([df[f"{peril}_ri_cost_post_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])
        other_data[f'total_sd_post_uw_layer{index}'] = sum([df[f"{peril}_sd_post_uw_layer{index}"].sum() or 0 for peril in ["windstorm_us", "earthquake_us"]])

        # TP components - calculate direct expenses and investment income (format investment income as negative)
        gn_technical_prem_pre_uw = (df[f"total_gn_technical_prem_{pre_uw_selected_method}_pre_uw_layer{index}"].sum() or 0)
        gn_technical_prem_post_uw = (df[f"total_gn_technical_prem_{post_uw_selected_method}_post_uw_layer{index}"].sum() or 0)

        other_data[f'total_direct_expenses_pre_uw_layer{index}'] = gn_technical_prem_pre_uw * direct_expense_perc
        other_data[f'total_direct_expenses_post_uw_layer{index}'] = gn_technical_prem_post_uw * direct_expense_perc

        other_data[f'total_investment_income_pre_uw_layer{index}'] = gn_technical_prem_pre_uw * -investment_income_perc
        other_data[f'total_investment_income_post_uw_layer{index}'] = gn_technical_prem_post_uw * -investment_income_perc

        # KPIs
        other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] = sum((other_data[f'{peril}_gg_technical_premium_pre_uw_layer{index}'] for peril in peril_node_names))
        other_data[f'total_gg_technical_premium_post_uw_layer{index}'] = sum((other_data[f'{peril}_gg_technical_premium_post_uw_layer{index}'] for peril in peril_node_names))

        other_data[f'total_expected_loss_pre_uw_layer{index}'] = sum((other_data[f'{peril}_expected_loss_pre_uw_layer{index}'] for peril in peril_node_names))
        other_data[f'total_expected_loss_post_uw_layer{index}'] = sum((other_data[f'{peril}_expected_loss_post_uw_layer{index}'] for peril in peril_node_names))

        other_data[f'total_gn_technical_premium_pre_uw_layer{index}'] = sum((other_data[f'{peril}_gn_technical_premium_pre_uw_layer{index}'] for peril in peril_node_names))
        other_data[f'total_gn_technical_premium_post_uw_layer{index}'] = sum((other_data[f'{peril}_gn_technical_premium_post_uw_layer{index}'] for peril in peril_node_names))

        other_data[f'total_gg_benchmark_premium_pre_uw_layer{index}'] = other_data[f"sum_total_expected_loss_pre_uw_layer{index}"] / target_loss_ratio / (1 - layer.brokerage) if layer.brokerage != 1 else 0
        other_data[f'total_gg_benchmark_premium_post_uw_layer{index}'] = other_data[f"sum_total_expected_loss_post_uw_layer{index}"] / target_loss_ratio / (1 - layer.brokerage) if layer.brokerage != 1 else 0

        # Shows the data in the UI
        other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_gg_technical_premium_pre_uw_layer{index}']) else 0 
                for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem.us_cat 
                if peril_name in peril_node_names}
        
        other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_gg_technical_premium_pre_uw_layer{index}']) else 0 
                for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem.intl_cat 
                if peril_name in peril_node_names}

        other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_gg_technical_premium_post_uw_layer{index}']) else 0 
                for peril_name, _ in layer.post_uw_adjustment.gross_tech_prem.us_cat 
                if peril_name in peril_node_names}
        
        other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_gg_technical_premium_post_uw_layer{index}']) else 0 
                for peril_name, _ in layer.post_uw_adjustment.gross_tech_prem.intl_cat 
                if peril_name in peril_node_names}

        other_data[f"pre_uw_adjustment_gross_tech_prem_fire_layer{index}"] = other_data[f'fire_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'fire_gg_technical_premium_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_gross_tech_prem_fire_layer{index}"] = other_data[f'fire_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'fire_gg_technical_premium_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_cyber_layer{index}"] = other_data[f'cyber_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'cyber_gg_technical_premium_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_gross_tech_prem_cyber_layer{index}"] = other_data[f'cyber_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'cyber_gg_technical_premium_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_nmp_layer{index}"] = other_data[f'nmp_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'nmp_gg_technical_premium_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_gross_tech_prem_nmp_layer{index}"] = other_data[f'nmp_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'nmp_gg_technical_premium_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] = other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] = other_data[f'total_gg_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'total_gg_technical_premium_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] = other_data[f'total_gn_technical_premium_pre_uw_layer{index}'] if not math.isnan(other_data[f'total_gn_technical_premium_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] = other_data[f'total_gn_technical_premium_post_uw_layer{index}'] if not math.isnan(other_data[f'total_gn_technical_premium_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"].values())
        other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"].values())

        other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"].values())
        other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"].values())
        
        # Shows the data in the UI - Expected Loss
        other_data[f"pre_uw_adjustment_expected_loss_us_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_expected_loss_pre_uw_layer{index}']) else 0 
                for peril_name, _ in layer.pre_uw_adjustment.expected_loss.us_cat 
                if peril_name in peril_node_names}
        
        other_data[f"pre_uw_adjustment_expected_loss_intl_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_expected_loss_pre_uw_layer{index}']) else 0 
                for peril_name, _ in layer.pre_uw_adjustment.expected_loss.intl_cat 
                if peril_name in peril_node_names}

        other_data[f"post_uw_adjustment_expected_loss_us_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_expected_loss_post_uw_layer{index}']) else 0 
                for peril_name, _ in layer.post_uw_adjustment.expected_loss.us_cat 
                if peril_name in peril_node_names}
        
        other_data[f"post_uw_adjustment_expected_loss_intl_cat_layer{index}"] = \
            {peril_name:other_data[f'{peril_name}_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'{peril_name}_expected_loss_post_uw_layer{index}']) else 0 
                for peril_name, _ in layer.post_uw_adjustment.expected_loss.intl_cat 
                if peril_name in peril_node_names}

        other_data[f"pre_uw_adjustment_expected_loss_fire_layer{index}"] = other_data[f'fire_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'fire_expected_loss_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_expected_loss_fire_layer{index}"] = other_data[f'fire_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'fire_expected_loss_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_expected_loss_cyber_layer{index}"] = other_data[f'cyber_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'cyber_expected_loss_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_expected_loss_cyber_layer{index}"] = other_data[f'cyber_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'cyber_expected_loss_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_expected_loss_nmp_layer{index}"] = other_data[f'nmp_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'nmp_expected_loss_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_expected_loss_nmp_layer{index}"] = other_data[f'nmp_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'nmp_expected_loss_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_expected_loss_expected_loss_total_layer{index}"] = other_data[f'total_expected_loss_pre_uw_layer{index}'] if not math.isnan(other_data[f'total_expected_loss_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_expected_loss_expected_loss_total_layer{index}"] = other_data[f'total_expected_loss_post_uw_layer{index}'] if not math.isnan(other_data[f'total_expected_loss_post_uw_layer{index}']) else 0

        other_data[f"pre_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_expected_loss_us_cat_layer{index}"].values())
        other_data[f"pre_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_expected_loss_intl_cat_layer{index}"].values())

        other_data[f"post_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_expected_loss_us_cat_layer{index}"].values())
        other_data[f"post_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_expected_loss_intl_cat_layer{index}"].values())
           
        # Calculates GG Technical Rate
        pre_us_cat_dict, post_us_cat_dict = {}, {}
        for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem_rate.us_cat:
            if peril_name in peril_node_names:
                pre_us_cat_dict[peril_name] = other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"][peril_name] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                                                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0
                post_us_cat_dict[peril_name] = other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"][peril_name] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                                                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"] = pre_us_cat_dict
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"] = post_us_cat_dict

        pre_intl_cat_dict, post_intl_cat_dict = {}, {}
        for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem_rate.intl_cat:
            if peril_name in peril_node_names:
                pre_intl_cat_dict[peril_name] = other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"][peril_name] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                                                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0
                post_intl_cat_dict[peril_name] = other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"][peril_name] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                                                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"] = pre_intl_cat_dict
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"] = post_intl_cat_dict

        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_fire_layer{index}"] = \
            other_data[f"pre_uw_adjustment_gross_tech_prem_fire_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_cyber_layer{index}"] = \
            other_data[f"pre_uw_adjustment_gross_tech_prem_cyber_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"post_uw_adjustment_gross_tech_prem_rate_fire_layer{index}"] = \
            other_data[f"post_uw_adjustment_gross_tech_prem_fire_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"post_uw_adjustment_gross_tech_prem_rate_cyber_layer{index}"] = \
            other_data[f"post_uw_adjustment_gross_tech_prem_cyber_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0
        
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_gross_tech_prem_rate_total_layer{index}"] = \
            other_data[f"pre_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"post_uw_adjustment_gross_tech_prem_rate_gross_tech_prem_rate_total_layer{index}"] = \
            other_data[f"post_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] / (other_data['sum_tiv_total_usd'] * hxd.policy_information.policy_length.selected)  \
                if (other_data['sum_tiv_total_usd'] and hxd.policy_information.policy_length.selected) else 0

        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"].values())
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"].values())

        other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"].values())
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"] = sum(other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"].values())

        # Calcuates percent of tech premium
        for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem_rate.us_cat:
            if peril_name in peril_node_names:
                other_data[f'{peril_name}_perc_tech_premium_pre_uw_layer{index}'] = \
                    (other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"][peril_name] / other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) \
                        if other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] else 0

                other_data[f'{peril_name}_perc_tech_premium_post_uw_layer{index}'] = \
                    (other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"][peril_name] / other_data[f'total_gg_technical_premium_post_uw_layer{index}']) \
                        if other_data[f'total_gg_technical_premium_post_uw_layer{index}'] else 0
        
        for peril_name, _ in layer.pre_uw_adjustment.gross_tech_prem_rate.intl_cat:
            if peril_name in peril_node_names:
                other_data[f'{peril_name}_perc_tech_premium_pre_uw_layer{index}'] = \
                    (other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"][peril_name] / other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) \
                        if other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] else 0

                other_data[f'{peril_name}_perc_tech_premium_post_uw_layer{index}'] = \
                    (other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"][peril_name] / other_data[f'total_gg_technical_premium_post_uw_layer{index}']) \
                        if other_data[f'total_gg_technical_premium_post_uw_layer{index}'] else 0        

        other_data[f'fire_perc_tech_premium_pre_uw_layer{index}'] = (other_data[f"pre_uw_adjustment_gross_tech_prem_fire_layer{index}"] / other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] else 0
        other_data[f'fire_perc_tech_premium_post_uw_layer{index}'] = (other_data[f"post_uw_adjustment_gross_tech_prem_fire_layer{index}"] / other_data[f'total_gg_technical_premium_post_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_post_uw_layer{index}'] else 0

        other_data[f'cyber_perc_tech_premium_pre_uw_layer{index}'] = (other_data[f"pre_uw_adjustment_gross_tech_prem_cyber_layer{index}"] / other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] else 0
        other_data[f'cyber_perc_tech_premium_post_uw_layer{index}'] = (other_data[f"post_uw_adjustment_gross_tech_prem_cyber_layer{index}"] / other_data[f'total_gg_technical_premium_post_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_post_uw_layer{index}'] else 0
                            
        other_data[f'nmp_perc_tech_premium_pre_uw_layer{index}'] = (other_data[f"pre_uw_adjustment_gross_tech_prem_nmp_layer{index}"] / other_data[f'total_gg_technical_premium_pre_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_pre_uw_layer{index}'] else 0
        other_data[f'nmp_perc_tech_premium_post_uw_layer{index}'] = (other_data[f"post_uw_adjustment_gross_tech_prem_nmp_layer{index}"] / other_data[f'total_gg_technical_premium_post_uw_layer{index}']) \
                                                                        if other_data[f'total_gg_technical_premium_post_uw_layer{index}'] else 0
        
        # # Calculates achieved GG premium
        for peril in peril_node_names:
            other_data[f'{peril}_achieved_gg_prem_pre_uw_layer{index}'] = (layer.achieved_premium_100_gg or 0) * other_data[f'{peril}_perc_tech_premium_pre_uw_layer{index}']
            other_data[f'{peril}_achieved_gg_prem_post_uw_layer{index}'] = (layer.achieved_premium_100_gg or 0) * other_data[f'{peril}_perc_tech_premium_post_uw_layer{index}']


        other_data[f'total_achieved_gg_prem_pre_uw_layer{index}'] = sum(other_data[f'{peril}_achieved_gg_prem_pre_uw_layer{index}'] for peril in peril_node_names)
        other_data[f'total_achieved_gg_prem_post_uw_layer{index}'] = sum(other_data[f'{peril}_achieved_gg_prem_post_uw_layer{index}'] for peril in peril_node_names)

        other_data[f'total_achieved_gg_prem_pre_uw_layer{index}'] = other_data[f'total_achieved_gg_prem_pre_uw_layer{index}'] if other_data[f'total_achieved_gg_prem_pre_uw_layer{index}'] > 0 else (layer.achieved_premium_100_gg or 0)
        other_data[f'total_achieved_gg_prem_post_uw_layer{index}'] = other_data[f'total_achieved_gg_prem_post_uw_layer{index}'] if other_data[f'total_achieved_gg_prem_post_uw_layer{index}'] > 0 else (layer.achieved_premium_100_gg or 0)

        other_data[f"pre_uw_adjustment_achieved_premium_layer{index}"] = other_data[f'total_achieved_gg_prem_pre_uw_layer{index}'] if not math.isnan(other_data[f'total_achieved_gg_prem_pre_uw_layer{index}']) else 0
        other_data[f"post_uw_adjustment_achieved_premium_layer{index}"] = other_data[f'total_achieved_gg_prem_post_uw_layer{index}'] if not math.isnan(other_data[f'total_achieved_gg_prem_post_uw_layer{index}']) else 0

        # Calculate achieved GG premium rate
        other_data[f'total_achieved_gg_rate_pre_uw_layer{index}'] = other_data[f"pre_uw_adjustment_achieved_premium_layer{index}"] / (other_data['total_tiv_total'] * hxd.policy_information.policy_length.selected)  \
                                                            if (other_data['total_tiv_total'] and hxd.policy_information.policy_length.selected) else 0
        
        other_data[f"pre_uw_adjustment_achieved_rate_layer{index}"] = other_data[f'total_achieved_gg_rate_pre_uw_layer{index}']

        other_data[f'total_achieved_gg_rate_post_uw_layer{index}'] = other_data[f"post_uw_adjustment_achieved_premium_layer{index}"] / (other_data['total_tiv_total'] * hxd.policy_information.policy_length.selected)  \
                                                            if (other_data['total_tiv_total'] and hxd.policy_information.policy_length.selected) else 0
        
        other_data[f"post_uw_adjustment_achieved_rate_layer{index}"] = other_data[f'total_achieved_gg_rate_post_uw_layer{index}']
    
        df = df.with_columns(
            pl.min(pl.max(df["tiv_total_usd"] - df[f"excess_usd_layer{index}"] - df[f"fire_deductible_usd_layer{index}"], 0), df[f"limit_usd_layer{index}"] - df[f"fire_deductible_usd_layer{index}"])\
                .alias(f"trapped_exposure_usd_layer{index}")
        )
        
        other_data[f"sum_total_trapped_exposure_usd_layer{index}"] = df[f"trapped_exposure_usd_layer{index}"].sum()

    return df


def underwriter_adjustments(hxd, df, other_data):
    risk_man_struct = hxd.non_layer_perils.uw_adjustments.risk_man
    experience_struct = hxd.non_layer_perils.uw_adjustments.experience
    valuation_struct = hxd.non_layer_perils.uw_adjustments.valuation
    other_struct = hxd.non_layer_perils.uw_adjustments.other

    for peril, peril_name in zip(['fire', 'named_windstorm', 'scs', 'flood', 'quake', 'wildfire', 
                                    # 'hail', 'tornado'
                                    ],
                                    ['fire', 'ws', 'scs', 'fl', 'eq', 'wf', 
                                    # 'ha', 'tn'
                                    ]):

        other_data[f'{peril_name}_uw_adjustments'] = getattr(risk_man_struct, peril) + getattr(experience_struct, peril) + getattr(valuation_struct, peril) + getattr(other_struct, peril)

        #added by CB 26/03/24 to incorporate calculated experience rating adjustment
        for index, layer in enumerate(hxd.layers, start=1):
            try:
                other_data[f'{peril_name}_experience_rating_adj_layer{index}'] = getattr(layer.perils, peril).experience_rating_adj or 0
            except AttributeError:
                other_data[f'{peril_name}_experience_rating_adj_layer{index}'] = 0


def climate_metrics_calc(hxd, df, other_data):

    # Load parameter tables
    cgear_score_df = hx.params.cgear_score
    cgear_message_df = hx.params.cgear_message

    cgear_score_pl = pl.from_pandas(cgear_score_df).rename({"Zip": "zip", "C-GEAR Score": "cgear_score"})

    climate_pl = df[["country", "zip", "tiv_buildings_usd", "tiv_contents_total_usd", "tiv_bi_usd", "windstorm_us_buildings_ground_up_uw_rate_layer1",
                        "windstorm_us_contents_ground_up_uw_rate_layer1", "windstorm_us_bi_ground_up_uw_rate_layer1", "loc_id", "street_name", "latitude", "longitude",
                        "occupancy", "ws_gate",
                        "total_gn_technical_prem_1_pre_uw_layer1", "total_gn_technical_prem_2_pre_uw_layer1", "total_gn_technical_prem_3_pre_uw_layer1",
                        "windstorm_us_gn_technical_prem_1_pre_uw_layer1", "windstorm_us_gn_technical_prem_2_pre_uw_layer1", "windstorm_us_gn_technical_prem_3_pre_uw_layer1",
                        "distance_from_coast", "constr_code"
                        ]]
    
    climate_pl = climate_pl.with_columns(
                    (
                        pl.col("tiv_buildings_usd") * pl.col("windstorm_us_buildings_ground_up_uw_rate_layer1") +
                        pl.col("tiv_contents_total_usd") * pl.col("windstorm_us_contents_ground_up_uw_rate_layer1") +
                        pl.col("tiv_bi_usd") * pl.col("windstorm_us_bi_ground_up_uw_rate_layer1")
                    ).alias("aal_cgear")
                )

    climate_pl = climate_pl.join(cgear_score_pl, on="zip", how="left")
    
    climate_pl = climate_pl.with_columns(
                    pl.when((pl.col("country") == "United States") & (pl.col("aal_cgear") > 0))
                        .then(pl.col("cgear_score"))
                        .otherwise(0)
                        .fill_null(0)
                        .alias("cgear_score")
                )

    df = df.with_columns(
        climate_pl.select(
            pl.col("cgear_score").alias("cgear_score_total")
        )
    )

    # DL SET THIS TO WINDSTORM TECH PREMIUM NOT TOTAL
    climate_pl = climate_pl.with_columns(
        pl.max(pl.col("windstorm_us_gn_technical_prem_1_pre_uw_layer1"), 
               pl.col("windstorm_us_gn_technical_prem_2_pre_uw_layer1"), 
               pl.col("windstorm_us_gn_technical_prem_3_pre_uw_layer1")).alias("gn_tech_pre_uw_layer")
    )
    
    if hxd.policy_information.small_schedule_model:
        cgear_score_list = climate_pl['cgear_score'].to_list()
        for index, row in enumerate(hxd.schedule.schedule_table):
            row.cgear_score_total = cgear_score_list[index]
    
    climate_pl = climate_pl.with_columns(
                    pl.when(pl.col("cgear_score") == 0)
                        .then(0)
                        .otherwise(pl.col("aal_cgear"))
                        .alias("aal_cgear_masked"),
                    (pl.col("cgear_score") * pl.col("aal_cgear"))
                        .fill_null(0)
                        .alias("aal_weighted_cgear")
                )
    
    count_pl = climate_pl.groupby("cgear_score", maintain_order=True).agg(pl.count())
    count_pl = count_pl.with_columns((pl.col("count") / pl.sum("count")).alias("loc_prop"))

    climate_pl = climate_pl.with_columns((pl.col("tiv_contents_total_usd") + pl.col("tiv_buildings_usd") + pl.col("tiv_bi_usd")).alias("tiv_total_usd"))
    score_summary = climate_pl.groupby("cgear_score", maintain_order = True).agg(pl.sum("tiv_total_usd"), pl.sum("gn_tech_pre_uw_layer"), pl.sum("aal_cgear_masked"), pl.sum("aal_weighted_cgear"))
    
    count_pl = count_pl.join(score_summary, on = "cgear_score", how = "left")

    score_locations = {}
    for index in range(6):
        score_locations[f"score_{index}"] = {"score": f"{index}", "loc_count": 0}

    for row in count_pl.rows(named=True):
        score_locations = score_locations | {f"score_{row['cgear_score']}": {
            # data_schema_node : df_column
            "score": row["cgear_score"], 
            "loc_count": row["count"], 
            "loc_prop": row["loc_prop"], 
            "total_tiv" : row["tiv_total_usd"] / 1e6, 
            "gn_tech_pre_uw" : row["gn_tech_pre_uw_layer"] / 1e3,
            "aal_cgear_masked" : row["aal_cgear_masked"],
            "aal_weighted_cgear" : row["aal_weighted_cgear"]
            }}
    
    other_data["climate_metrics_score_locations"] = score_locations

    aal_cgear_sum = (climate_pl["aal_cgear_masked"].sum() or 0)
    aal_weighted_cgear_sum = (climate_pl["aal_weighted_cgear"].sum() or 0)

    other_data["climate_metrics_weighted_climate_score"] = (aal_weighted_cgear_sum / aal_cgear_sum) if aal_cgear_sum else 0
    
    other_data["climate_metrics_climate_score_description"] = cgear_message_df[cgear_message_df["C-GEAR Score"] == int(round(other_data["climate_metrics_weighted_climate_score"]))]["Message"].iloc[0]

    '''
    DL EDIT
    additional climate metrics
    ws_gate, occupancy, 
    total_gn_technical_prem_1_pre_uw_layer1
    total_gn_technical_prem_2_pre_uw_layer1
    total_gn_technical_prem_3_pre_uw_layer1
    total_gn_technical_prem_1_post_uw_layer1
    total_gn_technical_prem_2_post_uw_layer1
    total_gn_technical_prem_3_post_uw_layer1

    zip, distance_from_coast, construction description, constr_code

    Note: to covert data frames back to dictionaries to upload to HXD
    - polars: .to_dicts()
    - pandas: .to_dict('records')

    '''

    climate_df = climate_pl.to_pandas()
    
    # ws cc score occupancy
    occ_summary = climate_df[["occupancy", "cgear_score", "tiv_total_usd", "gn_tech_pre_uw_layer"]].groupby(["occupancy"], as_index = False).agg({"cgear_score":"mean", "tiv_total_usd" : "sum", "gn_tech_pre_uw_layer" : "sum"})

    # write occupancy to hxd
    # setattr(hxd, "non_layer_summary.climate_metrics.ws_cc_score_occupancy", occ_summary.to_dict("records"))
    hxd.non_layer_summary.climate_metrics.ws_cc_score_occupancy = occ_summary.to_dict("records")

    # wc CC score by gate
    gate_summary = climate_df[["ws_gate", "cgear_score"]].groupby(["ws_gate", "cgear_score"], as_index = False).size()
    gate_summary = gate_summary.pivot(index = "ws_gate", columns = "cgear_score", values = "size").fillna(0).reset_index()

    # Define the columns to insert
    new_cols = [0, 1, 2, 3, 4, 5]
    cols_to_add = [col for col in new_cols if col not in gate_summary.columns]
    gate_summary.loc[:, cols_to_add] = 0
    gate_summary = gate_summary.rename(columns = {0 : "cgear_0", 1 : "cgear_1", 2 : "cgear_2", 3 : "cgear_3", 4 : "cgear_4", 5 : "cgear_5"})

    # write to hxd
    # setattr(hxd, "non_layer_summary.climate_metrics.ws_cc_score_gate", gate_summary.to_dict("records"))
    hxd.non_layer_summary.climate_metrics.ws_cc_score_gate = gate_summary.to_dict("records")
    # setattr(hxd, "fa_" + premise.replace(" ", "_").lower() + "_summary_rates", df_summary_2.to_dict("records"))

    # ws cc score location detail
    constr_mapping = hx.params.construction_load
    constr_mapping = constr_mapping[["ISO", "Construction"]]
    constr_mapping = constr_mapping.rename(columns = {"ISO" : "constr_code", "Construction" : "constr_desc"})

    location_summary = climate_df[["tiv_total_usd", "aal_weighted_cgear", "cgear_score", "ws_gate", "distance_from_coast", "zip", "occupancy", "constr_code"]]
    location_summary = location_summary.merge(constr_mapping, how = "left", on = "constr_code")
    location_summary = location_summary.sort_values(by = ['aal_weighted_cgear', 'tiv_total_usd'], ascending = False)
    location_summary = location_summary.head(10)
    location_summary = location_summary.drop(["constr_code"], axis = 1)

    # write to hxd
    hxd.non_layer_summary.climate_metrics.ws_cc_score_location = location_summary.to_dict("records")


    return df


def produce_climate_map(hxd, progress):
    '''
    Uses the folium package to generate a .html file of a World map, with the portfolio locations as the heat map,
    and the schedule locations as markers on the map.
    '''
    cgear_score_df = hx.params.cgear_score
    cgear_score_df = cgear_score_df.rename(columns={"Zip": "zip", "C-GEAR Score": "cgear_score"})

    columns = [
        "loc_id" ,"zip", "street_name", "latitude", "longitude"
        ]

    if hxd.policy_information.small_schedule_model:
        portfolio = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])

        portfolio["country"] = [x if x != "Georgia" else "Georgia (Country)" for x in [row.address_dropdown.country for row in hxd.schedule.schedule_table]]
        portfolio["state"] = [row.address_dropdown.state for row in hxd.schedule.schedule_table]
        portfolio["county"] = [row.address_dropdown.county for row in hxd.schedule.schedule_table]
        portfolio["city"] = [row.address_dropdown.city for row in hxd.schedule.schedule_table]

        us_state_code = pd.DataFrame(hx.params.us_state_code)[["US States", "US State Code"]].rename({
            "US States": 'state_name', 
            "US State Code": "state"
        }, axis=1)
        portfolio = portfolio.merge(us_state_code, how="left", on="state")

        # attach c-gear score
        portfolio = portfolio.merge(cgear_score_df, how = "left", on="zip")

        portfolio = portfolio.rename({
            "loc_id": 'index', 
            "street_name": 'name', 
            # "state": 'zone', 
            "tiv_total": 'tiv'
        }, axis=1)

        portfolio['state_or_country'] = portfolio.apply(lambda row: row['state_name'] if row['country'] == "United States" else row['country'], axis=1)


        # Generate the base map
        #f_map = folium.Map(tiles=None, zoom_start=40, control_scale=True)
        f_map_climate = folium.Map(tiles=None, zoom_start=5, control_scale=True)
        folium.TileLayer('openstreetmap', name='Light Mode').add_to(f_map_climate)
        folium.TileLayer('stamentoner', name='Dark Mode').add_to(f_map_climate)
        Geocoder().add_to(f_map_climate)

        # TODO: is this a good idea?
        portfolio = portfolio.fillna(0.0)

        HeatMap(portfolio[["latitude", "longitude", "cgear_score"]], radius=50, name="Climate Heat Map").add_to(f_map_climate)


        # Add each location in the schedule to the map with its own custom marker
        # and a hyperlink to its Google Street View
        # total_schedule_tiv = 0
        for index, location_info in portfolio.iterrows():
            if location_info['latitude'] and location_info['longitude']:
            
                tag = "" + str(location_info['name']) + ", " + str(location_info['cgear_score'])
                # total_schedule_tiv += location_info['tiv']

                marker = folium.Marker(
                    [location_info['latitude'], location_info['longitude']],
                    popup=generate_street_view_href(location_info['latitude'], location_info['longitude']) + tag + "</a>",
                )

                marker.add_to(f_map_climate)

        
        # portfolio = portfolio.merge(hx.params.zone_to_state, how="left", on="zone")
        portfolio = portfolio.groupby('state_or_country').mean()['cgear_score'].reset_index()
        cp = folium.Choropleth(
                geo_data=read_geojson("./model/algorithms/account_segmentation/states_and_countries.json"),
                data=portfolio,
                columns=['state_or_country', 'cgear_score'],  
                key_on='feature.properties.NAME', 
                fill_color='YlOrRd',
                nan_fill_color="White",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name='Climate Score', 
                highlight=True,
                line_color='black',
                name="Choropleth",
                show=False
                )

        # creating a state indexed version of the dataframe so we can lookup values
        sov_df = pd.DataFrame([{"state_or_country": row[1].state_or_country, "cgear_score": row[1].cgear_score} for row in portfolio.iterrows()])
        # schedule = sov_df.merge(hx.params.zone_to_state, how="left", on="zone").groupby('state').sum()['total_tiv'].reset_index()
        schedule = sov_df.groupby('state_or_country').mean()['cgear_score'].reset_index()
        
        # looping thru the geojson object and adding a new property(unemployment)
        # and assigning a value from our dataframe
        for s in cp.geojson.data['features']:
            # state_tiv = portfolio[portfolio['state_or_country'] == s['properties']['NAME']]
            # if len(state_tiv) > 0:
            #     s['properties']['tiv'] = millify(state_tiv['tiv'].iloc[0])
            # else: 
            #     s['properties']['tiv'] = 0

            state_schedule_tiv = schedule[schedule['state_or_country'] == s['properties']['NAME']]
            if len(state_schedule_tiv) > 0:
                s['properties']['cgear_score'] = millify(state_schedule_tiv['cgear_score'].iloc[0])
            else: 
                s['properties']['cgear_score'] = 0
        
        # and finally adding a tooltip/hover to the choropleth's geojson
        folium.GeoJsonTooltip(fields=['NAME', 'cgear_score'], aliases=['State', 'Climate Score']).add_to(cp.geojson)
        cp.add_to(f_map_climate) 
        folium.LayerControl(collapsed=True).add_to(f_map_climate)

        

        # Add titles with key summarised figures to the map
        # insured_name_header = '''<h3 align="center" style="font-size:16px"><b>{}</b></h3>'''.format(hxd.input.quote_input.cedant)
        # total_portfolio_tiv_header = '''<h3 align="center" style="font-size:16px"><b>Total TIV in radius in portfolio: {}</b></h3>'''.format(millify(total_schedule_tiv))
        schedule_cgear_header = '''<h3 align="center" style="font-size:16px"><b>Climate Score in radius in schedule: {}</b></h3>'''.format(millify(portfolio["cgear_score"].mean()))

        # f_map.get_root().html.add_child(folium.Element(insured_name_header))
        # f_map.get_root().html.add_child(folium.Element(total_portfolio_tiv_header))
        f_map_climate.get_root().html.add_child(folium.Element(schedule_cgear_header))
            
        # Save map down 
        f_map_climate.save("map_climate.html")

        # Load the map file, read it as html, convert to text
        with open("map_climate.html") as map_html:
            txt = map_html.read()
            # soup = bs(txt)

        # Output the text to hxd.File
        with hxd.non_layer_summary.climate_metrics.climate_heatmap_file.open("t") as f:
            f.write(str(txt))

        hxd.non_layer_summary.climate_metrics.show_file_component = True




def premium_summary_assignment(hxd, df, other_data):
    cb_countries = pl.from_pandas(hx.params.intl_base_rates)
    cb_countries = set(cb_countries.filter(pl.col("Continent") == "Caribbean").select("Country").to_series().to_list())

    if hxd.policy_information.small_schedule_model:
        # Assign to schedule table
        for status in ['pre', 'post']:
            
            for index, layer in enumerate(hxd.layers, start=1): 

                method = other_data[f'{status}_uw_selected_method_layer{index}']
                summary_assignment_df = df.select(
                    pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                        .then(pl.col(f"earthquake_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"earthquake_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"earthquake_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"flood_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"flood_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"flood_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"hail_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"hail_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"hail_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"tornado_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"tornado_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"tornado_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"wildfire_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"wildfire_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"wildfire_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                    pl.when((pl.col("country") == "United States") | (pl.col("country").is_in(cb_countries)))
                        .then(pl.col(f"windstorm_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"windstorm_intl_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .alias(f"windstorm_gn_technical_prem_{method}_{status}_uw_layer{index}"),
                )

                earthquake_prem_list = summary_assignment_df[f"earthquake_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                flood_prem_list = summary_assignment_df[f"flood_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                hail_prem_list = summary_assignment_df[f"hail_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                tornado_prem_list = summary_assignment_df[f"tornado_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                wildfire_prem_list = summary_assignment_df[f"wildfire_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                windstorm_prem_list = summary_assignment_df[f"windstorm_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()

                fire_prem_list = df[f"fire_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                cyber_prem_list = df[f"cyber_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()
                total_prem_list = df[f"total_gn_technical_prem_{method}_{status}_uw_layer{index}"].fill_nan(0).to_list()

                for i, row in enumerate(hxd.schedule.schedule_table):
                    target_output_by_layer = row.output_by_layer[index-1]

                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_eq", earthquake_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_fire", fire_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_fl", flood_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_ha", hail_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_tn", tornado_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_wf", wildfire_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_ws", windstorm_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_cyber", cyber_prem_list[i])
                    setattr(target_output_by_layer, f"premtp_gn_max_{status}_uw_usd_100_total", total_prem_list[i])

    else:
        for status in ['pre', 'post']:

            for index, layer in enumerate(hxd.layers, start=1): 

                method = other_data[f'{status}_uw_selected_method_layer{index}']
                df = df.with_columns(
                    pl.when((pl.col("country") == "United States") | (pl.col("country") == "Canada"))
                        .then(pl.col(f"earthquake_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"earthquake_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_eq_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"flood_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"flood_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_fl_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"hail_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"hail_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_ha_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"tornado_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"tornado_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_tn_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"wildfire_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"wildfire_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_wf_layer{index}"),
                    pl.when(pl.col("country") == "United States")
                        .then(pl.col(f"windstorm_us_gn_technical_prem_{method}_{status}_uw_layer{index}"))
                        .otherwise(pl.col(f"windstorm_intl_gn_technical_prem_{method}_{status}_uw_layer{index}")).fill_nan(0)
                        .alias(f"premtp_gn_max_{status}_uw_usd_100_ws_layer{index}"),

                    pl.col(f"fire_gn_technical_prem_{method}_{status}_uw_layer{index}").fill_nan(0).alias(f"premtp_gn_max_{status}_uw_usd_100_fire_layer{index}"),
                    pl.col(f"cyber_gn_technical_prem_{method}_{status}_uw_layer{index}").fill_nan(0).alias(f"premtp_gn_max_{status}_uw_usd_100_cyber_layer{index}"),
                    pl.col(f"total_gn_technical_prem_{method}_{status}_uw_layer{index}").fill_nan(0).alias(f"premtp_gn_max_{status}_uw_usd_100_total_layer{index}"),
                )

    return df



def final_technical_premium_columns(hxd, df, other_data):
    for status in ['pre', 'post']:

            for index, layer in enumerate(hxd.layers, start=1): 

                method = other_data[f'{status}_uw_selected_method_layer{index}']
                full_peril_list = ['earthquake_us','earthquake_intl', 'windstorm_us','windstorm_intl', 'flood_us', 'flood_intl', 'hail_us','hail_intl', 'tornado_us', 'tornado_intl', 'wildfire_us', 'wildfire_intl', 'fire','nmp', 'cyber']
                
                df = df.with_columns([
                    pl.col(f"{peril}_gn_technical_prem_{method}_{status}_uw_layer{index}")
                    .alias(f"{peril}_gn_technical_prem_final_{status}_uw_layer{index}")
                    for peril in full_peril_list
                ])
                
                
                df = df.with_columns([
                    (pl.col(f"{peril}_gn_technical_prem_final_{status}_uw_layer{index}") / (1 - layer.brokerage) if layer.brokerage != 1 else pl.lit(0))
                    .alias(f"{peril}_gg_technical_prem_final_{status}_uw_layer{index}")
                    for peril in full_peril_list
                ])

                basis_list = ['gn', 'gg']
                df = df.with_columns(
                    expr
                    for basis in basis_list
                    for expr in [
                    (pl.col(f"earthquake_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"earthquake_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"earthquake_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"windstorm_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"windstorm_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"windstorm_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"flood_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"flood_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"flood_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"hail_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"hail_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"hail_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"tornado_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"tornado_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"tornado_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"wildfire_us_{basis}_technical_prem_final_{status}_uw_layer{index}") + pl.col(f"wildfire_intl_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"wildfire_{basis}_technical_prem_final_{status}_uw_layer{index}"),
                    
                    (pl.col(f"fire_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"fire_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"cyber_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"cyber_{basis}_technical_prem_final_{status}_uw_layer{index}"),

                    (pl.col(f"nmp_{basis}_technical_prem_final_{status}_uw_layer{index}"))
                    .alias(f"nmp_{basis}_technical_prem_final_{status}_uw_layer{index}")
                ])
                
                perils = ['earthquake', 'windstorm', 'flood', 'hail', 'tornado', 'wildfire', 'fire','nmp', 'cyber']

                df = df.with_columns(
                    pl.sum([pl.col(f"{peril}_gn_technical_prem_final_{status}_uw_layer{index}") for peril in perils])
                    .alias(f"total_gn_technical_prem_final_{status}_uw_layer{index}"),
                    
                    pl.sum([pl.col(f"{peril}_gg_technical_prem_final_{status}_uw_layer{index}") for peril in perils])
                    .alias(f"total_gg_technical_prem_final_{status}_uw_layer{index}")
                    )

    return df 


def overall_analysis_summary(hxd, df, other_data, peril_node_names):
    for index, layer in enumerate(hxd.layers, start=1):
        sum_prod_df = overall_modifier_summary(hxd, df, other_data, layer, index, peril_node_names)
        overall_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index)

    return df


def overall_modifier_summary(hxd, df, other_data, layer, index, peril_node_names):
    # modifier_summary_dict = {}
    # Assign to Fire Modifier Summary
    # modifier_summary_dict["peril_name"] = "Hurricane"
    # modifier_summary_dict["no_of_locs"] = len(df)
    # modifier_summary_dict["sum_tiv_total_usd"] = other_data["sum_tiv_total_usd"] 

    # Calculate totals accross perils

    # Calculate the sum product per layer
    # Select a subset of fields to optimise sorting
    sum_prod_df = df.with_columns(
        [
            df.select(
                    [
                        f"fire_{base_rate_condition}_base_rate_layer{index}",
                        f"earthquake_us_{base_rate_condition}_base_rate_layer{index}",
                        f"flood_us_{base_rate_condition}_base_rate_layer{index}",
                        f"tornado_{base_rate_condition}_base_rate_layer{index}",
                        f"hail_{base_rate_condition}_base_rate_layer{index}",
                        f'wildfire_{base_rate_condition}_base_rate_layer{index}', 
                        f"windstorm_us_{base_rate_condition}_base_rate_layer{index}",
                    ]
                ).sum(axis=1).alias(f"total_us_{base_rate_condition}_base_rate_layer{index}")
        for base_rate_condition in ["buildings", "contents", "bi"]]
        +
        [
            df.select(
                    [
                        f"fire_{base_rate_condition}_base_rate_layer{index}",
                        f"earthquake_intl_{base_rate_condition}_base_rate_layer{index}",
                        f"flood_intl_{base_rate_condition}_base_rate_layer{index}",
                        f"tornado_{base_rate_condition}_base_rate_layer{index}",
                        f"hail_{base_rate_condition}_base_rate_layer{index}",
                        f'wildfire_{base_rate_condition}_base_rate_layer{index}', 
                        f"windstorm_intl_{base_rate_condition}_base_rate_layer{index}",
                    ]
                ).sum(axis=1).alias(f"total_intl_{base_rate_condition}_base_rate_layer{index}")
        for base_rate_condition in ["buildings", "contents", "bi"]]
    )

    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.when(pl.col("country") == "United States")
                .then(pl.col(f"earthquake_us_{base_rate_condition}_base_rate_layer{index}"))
                .otherwise(pl.col(f"earthquake_intl_{base_rate_condition}_base_rate_layer{index}"))
            ).alias(f"earthquake_{base_rate_condition}_base_rate_layer{index}")
        for base_rate_condition in ["buildings", "contents", "bi"]]
    )

    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.when(pl.col("country") == "United States")
                .then(pl.col(f"flood_us_{base_rate_condition}_base_rate_layer{index}"))
                .otherwise(pl.col(f"flood_intl_{base_rate_condition}_base_rate_layer{index}"))
            ).alias(f"flood_{base_rate_condition}_base_rate_layer{index}")
        for base_rate_condition in ["buildings", "contents", "bi"]]
    )
    
    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.when(pl.col("country") == "United States")
                .then(pl.col(f"windstorm_us_{base_rate_condition}_base_rate_layer{index}"))
                .otherwise(pl.col(f"windstorm_intl_{base_rate_condition}_base_rate_layer{index}"))
            ).alias(f"windstorm_{base_rate_condition}_base_rate_layer{index}")
        for base_rate_condition in ["buildings", "contents", "bi"]]
    )
    
    perils = ["fire", "earthquake", "flood", "tornado", "hail", "wildfire", "windstorm"]

    # Base weighted sums
    sum_prod_df = sum_prod_df.with_columns(
        [
            (pl.col("tiv_buildings_usd") * 
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"total_us_buildings_base_rate_layer{index}"))
                    .otherwise(pl.col(f"total_intl_buildings_base_rate_layer{index}"))
                )
            ).alias("buildings_cumprod"),
            (pl.col("tiv_contents_total_usd") *
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"total_us_contents_base_rate_layer{index}"))
                    .otherwise(pl.col(f"total_intl_contents_base_rate_layer{index}"))
                )
            ).alias("contents_total_cumprod"),
            (pl.col("tiv_bi_usd") * 
                (pl.when(pl.col("country") == "United States")
                    .then(pl.col(f"total_us_bi_base_rate_layer{index}"))
                    .otherwise(pl.col(f"total_intl_bi_base_rate_layer{index}"))
                )
            ).alias("bi_cumprod"),
        ] +
        [(pl.col("tiv_buildings_usd") * pl.col(f"{peril}_buildings_base_rate_layer{index}")).alias(f"{peril}_buildings_cumprod") for peril in perils] +
        [(pl.col("tiv_contents_total_usd") * pl.col(f"{peril}_contents_base_rate_layer{index}")).alias(f"{peril}_contents_cumprod") for peril in perils] +
        [(pl.col("tiv_bi_usd") * pl.col(f"{peril}_bi_base_rate_layer{index}")).alias(f"{peril}_bi_cumprod") for peril in perils]
    )

    # total_modifier_impact = 1
    multipliers = peril_total_base_and_modifier_columns(other_data)
    
    # for idx, (factor, multiplier_col) in multipliers:
    for peril in multipliers:
        prev_col = peril
        for col in multipliers[peril]:
            factor = col[0]
            multiplier_col = col[1]

            sum_prod_df = sum_prod_df.with_columns(
                [
                    (pl.col(f"{prev_col}_buildings_cumprod") * multiplier_col).alias(f"{factor}_buildings_cumprod"),
                    (pl.col(f"{prev_col}_contents_cumprod") * multiplier_col).alias(f"{factor}_contents_cumprod"),
                    (pl.col(f"{prev_col}_bi_cumprod") * multiplier_col).alias(f"{factor}_bi_cumprod")
                ]
            )

            sum_prod_df = sum_prod_df.with_columns(
                (pl.col(f"{factor}_buildings_cumprod") + pl.col(f"{factor}_contents_cumprod") + pl.col(f"{factor}_bi_cumprod")).alias(f"{factor}_total_cumprod")
            )

            prev_col = factor
        
        sum_prod_df = sum_prod_df.with_columns(pl.col(f"{factor}_total_cumprod").alias(f"{peril}_all_modifiers_total_cumprod"))


    MAX_CALC_METHOD=3

    sum_prod_df = sum_prod_df.with_columns(
        [
            sum_prod_df.select(
                    [f"{peril}_gn_technical_prem_{method}_pre_uw_layer{index}" for peril in peril_node_names]
                ).sum(axis=1).alias(f"total_gn_technical_prem_{method}_pre_uw_layer{index}")
            for method in range(1, MAX_CALC_METHOD+1)
        ] + \
        [
            sum_prod_df.select(
                    [f"{peril}_gn_technical_prem_{method}_post_uw_layer{index}" for peril in peril_node_names]
                ).sum(axis=1).alias(f"total_gn_technical_prem_{method}_post_uw_layer{index}")
            for method in range(1, MAX_CALC_METHOD+1)
        ] + \
        [
            sum_prod_df.select(
                    [f"{peril}_total_expected_loss_pre_uw_layer{index}" for peril in peril_node_names]
                ).sum(axis=1).alias(f"total_total_expected_loss_pre_uw_layer{index}")
        ]   
    )

    return sum_prod_df

def overall_risk_factors_summary(hxd, sum_prod_df, other_data, layer, index):

    occupancy_summary_list = []
    sprinkler_summary_list = []
    constr_summary_list = []
    ws_zone_summary_list = []
    distance_from_coast_summary_list = []
    year_built_summary_list = []
    eq_zone_summary_list = []
    state_summary_list = []
    country_summary_list = []
    state_country_list = []
    state_country_choropleth_list = []

    for column_name, target_list in zip(
                    ("occupancy", "sprinkler", "constr_name", "ws_zone", "dtc_band", "year_built_band", "eq_zone", "state", "country", ["state", "country"], ["state", "country", "latitude", "longitude"]), 
                    (occupancy_summary_list, sprinkler_summary_list, constr_summary_list, ws_zone_summary_list, 
                    distance_from_coast_summary_list, year_built_summary_list, eq_zone_summary_list, state_summary_list, country_summary_list, state_country_list, state_country_choropleth_list)):

        for name, data in sum_prod_df.groupby(column_name):
            total_tiv_usd = data["tiv_total_usd"].sum() or 0
            tiv_buildings_usd = data["tiv_buildings_usd"].sum() or 0

            peril_modifiers = peril_total_base_and_modifier_columns(other_data)
            peril_tech_rates = {}
            peril_gu_prems = {}
            for peril in peril_modifiers:
                peril_tech_rates[peril], peril_gu_prems[peril] = calculate_peril_tech_rate(peril, data, total_tiv_usd, other_data, index)

            total_gg_technical_prem_final_pre_uw = data[f"total_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0

            total_gg_technical_prem_final_post_uw = data[f"total_gg_technical_prem_final_post_uw_layer{index}"].fill_nan(0).sum() or 0

            total_total_expected_loss_pre_uw_sum = data[f"total_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0

            # total_floor_area = data['floor_area'].fill_null(0).sum() or 0

            total_floor_area = data.filter(pl.col("tiv_buildings") != 0)['floor_area'].fill_null(0).sum() or 0
            
            gu_tech_rate = sum([peril_tech_rates[x] for x in peril_tech_rates])
            tech_rate = total_gg_technical_prem_final_pre_uw / total_tiv_usd if total_tiv_usd else 0
            tech_prem = total_gg_technical_prem_final_pre_uw
            gu_prem = sum([peril_gu_prems[x] for x in peril_gu_prems])
            # worth = tech_rate / gu_tech_rate if gu_tech_rate else 0
            # uw_adj_tech_rate = total_gg_technical_prem_final_post_uw / total_tiv_usd if total_tiv_usd else 0
            uw_adj_tech_prem = total_gg_technical_prem_final_post_uw
            gu_loss = total_total_expected_loss_pre_uw_sum
            itv = tiv_buildings_usd / total_floor_area if total_floor_area else 0


            target_list.append({
                "name": name,
                "num_locations": len(data),
                "tiv":  total_tiv_usd,
                "gu_tech_rate": gu_tech_rate,
                "total_gu_tech_rate": gu_tech_rate,
                # "worth": worth,
                "tech_rate": tech_rate,
                "tech_prem": tech_prem,
                # "uw_adj_tech_rate": uw_adj_tech_rate,
                "uw_adj_tech_prem": uw_adj_tech_prem,
                "gu_loss": gu_loss,
                "gu_prem": gu_prem,
                "itv": itv
            })

    for summary_list in [occupancy_summary_list, sprinkler_summary_list, constr_summary_list, ws_zone_summary_list, eq_zone_summary_list, state_summary_list, country_summary_list, state_country_list, state_country_choropleth_list]:
        summary_list.sort(key=lambda d: (d["tiv"], d["name"] or ""), reverse=True)

    for summary_list in [distance_from_coast_summary_list]:
        summary_list.sort(key=lambda d: d["name"])

    year_built_summary_list.sort(key=lambda d: d["name"][-4:])

    summary_lists = [
        occupancy_summary_list, 
        sprinkler_summary_list, 
        constr_summary_list, 
        ws_zone_summary_list, 
        distance_from_coast_summary_list, 
        year_built_summary_list, 
        eq_zone_summary_list
        ]

    existing_summary_lists = [
        f"fire_occupancy_summary_layer{index}", 
        f"fire_sprinkler_summary_layer{index}", 
        f"fire_construction_summary_layer{index}", 
        f"ws_zone_summary_layer{index}", 
        f"distance_from_coast_summary_layer{index}", 
        f"year_built_summary_layer{index}", 
        f"eq_zone_summary_layer{index}"
        ]

    for summary_list, existing_summary_list in zip(summary_lists, existing_summary_lists):
        names = [x['name'] for x in summary_list]
        for name in names:  
            print(name)
            for item in other_data[existing_summary_list]:
                if item['name'] == name:
                    item['total_gu_tech_rate'] = [x for x in summary_list if x['name'] == name][0]['total_gu_tech_rate']

    other_data[f"state_summary_layer{index}"] = state_summary_list
    other_data[f"country_summary_layer{index}"] = country_summary_list
    other_data[f"state_country_summary_layer{index}"] = state_country_list
    other_data[f"state_country_choropleth_summary_layer{index}"] = state_country_choropleth_list



def calculate_peril_tech_rate(peril, data, total_tiv_usd, other_data, index):
    prod_sum_base = (data[f"{peril}_buildings_cumprod"].sum() or 0) + (data[f"{peril}_contents_cumprod"].sum() or 0) + (data[f"{peril}_bi_cumprod"].sum() or 0)
    prod_sum_last = data[f"{peril}_all_modifiers_total_cumprod"].sum() or 0

    base_rate = prod_sum_base / total_tiv_usd if total_tiv_usd else 0
    total_modifier_impact = prod_sum_last / prod_sum_base if prod_sum_base else 0

    if f"{peril}_gg_technical_prem_final_pre_uw_layer{index}" not in data.columns: 
        data = data.with_columns((
            (pl.col(f"{peril}_us_gn_technical_prem_{other_data[f'pre_uw_selected_method_layer{index}']}_pre_uw_layer{index}") +
            pl.col(f"{peril}_intl_gn_technical_prem_{other_data[f'pre_uw_selected_method_layer{index}']}_pre_uw_layer{index}")) / (1 - layer.brokerage) if layer.brokerage != 1 else 0
            ).alias(f"{peril}_gg_technical_prem_final_pre_uw_layer{index}"))

    if f"{peril}_total_expected_loss_pre_uw_layer{index}" not in data.columns: 
        data = data.with_columns((
            pl.col(f"{peril}_us_total_expected_loss_pre_uw_layer{index}") +
            pl.col(f"{peril}_intl_total_expected_loss_pre_uw_layer{index}")
            ).alias(f"{peril}_total_expected_loss_pre_uw_layer{index}"))

    gg_technical_prem_final_pre_uw = data[f"{peril}_gg_technical_prem_final_pre_uw_layer{index}"].fill_nan(0).sum() or 0
    expected_loss_pre_uw_sum = data[f"{peril}_total_expected_loss_pre_uw_layer{index}"].fill_nan(0).sum() or 0

    gu_tech_rate = base_rate * total_modifier_impact * gg_technical_prem_final_pre_uw / expected_loss_pre_uw_sum if expected_loss_pre_uw_sum else 0

    gu_prem = base_rate * total_modifier_impact * total_tiv_usd

    return gu_tech_rate, gu_prem


def peril_total_base_and_modifier_columns(other_data):
    return {
        "fire": [
            # Fire
            ["fire_construction", pl.col("fire_construction_factor")], 
            ["fire_pc_code", pl.col("fire_pc_code_factor")], 
            ["fire_sprinkler", pl.col("fire_sprinkler_factor")], 
            ["bi_waiting_period",pl.col("bi_waiting_period_factor")],
            ['bi_indemnity_period', other_data['bi_indemnity_period_factor']], 
            ['cbi_load', other_data['cbi_load']], 
            ["fire_mexican_fonden", pl.col("fire_mexican_fonden_factor")],
            ["fire_size_discount", pl.col("fire_size_discount_factor")],
        ],
        "earthquake": [
            ["eq_occupancy", pl.col("eq_occupancy_factor")], 
            ["eq_construction", pl.col("eq_construction_factor")], 
            ["eq_year_built", pl.col("eq_year_built_factor")], 
            ["eq_num_floors",pl.col("eq_num_floors_factor")],
            ["eq_construction_quality", pl.col("eq_construction_quality_factor")], 
            ["eq_plan_irregularity", pl.col("eq_plan_irregularity_factor")], 
            ["eq_soft_story", pl.col("eq_soft_story_factor")], 
            ["eq_vertical_irregularity",pl.col("eq_vertical_irregularity_factor")],
            ["eq_ornamentation", pl.col("eq_ornamentation_factor")], 
            ["eq_equipment_bracing", pl.col("eq_equipment_bracing_factor")], 
            ["eq_equipment_maintenance", pl.col("eq_equipment_maintenance_factor")], 
            ["eq_pounding", pl.col("eq_pounding_factor")],
            ["eq_catnet_intl", pl.col("eq_catnet_intl_factor")],
        ],
        "flood": [
            ["fl_construction", pl.col("fl_construction_rating_factor")], 
            ["fl_num_floors", pl.col("fl_num_floors_rating_factor")], 
            ["fl_basement", pl.col("fl_basement_rating_factor")], 
            ["fl_elevation", pl.col("fl_elevation_rating_factor")],
            ["fl_size_discount", pl.col("fl_size_discount_rating_factor")],
        ],
        "tornado": [
            ["tornado_occupancy_load", pl.col("tornado_occupancy_load")], 
            ["tornado_construction_load", pl.col("tornado_construction_load")], 
            ["tornado_year_built_load", pl.col("tornado_year_built_load")],
            ["tornado_catnet_score_load", pl.col("tornado_catnet_score_load")],
            ["tornado_size_discount_load", pl.col("tornado_size_discount_load")],
        ],
        "hail": [
            ["hail_occupancy_load", pl.col("hail_occupancy_load")],
            ["hail_construction_load", pl.col("hail_construction_load")],
            ["hail_year_built_load", pl.col("hail_year_built_load")],
            ["hail_floor_area_load", pl.col("hail_floor_area_load")],
            ["hail_roof_age_load", pl.col("hail_roof_age_load")],
            ["hail_roof_covering_load", pl.col("hail_roof_covering_load")],
            ["hail_roof_geometry_load", pl.col("hail_roof_geometry_load")],
            ["hail_catnet_score_load", pl.col("hail_catnet_score_load")],
             ["hail_size_discount_load", pl.col("hail_size_discount_load")],
        ],
        "wildfire": [
            ['wildfire_occupancy', pl.col('wildfire_occupancy_load')],
            ['wildfire_construction', pl.col('wildfire_construction_load')],
            ['wildfire_pc_code', pl.col('wildfire_pc_code_load')],
            ['wildfire_catnet_score', pl.col('wildfire_catnet_score_load')],
            ['wildfire_size_discount_score', pl.col('wildfire_size_discount_load')],
        ],
        "windstorm": [
            ["ws_occupancy", pl.col("ws_occupancy_factor")], 
            ["ws_construction", pl.col("ws_construction_factor")], 
            ["ws_year_built", pl.col("ws_year_built_factor")], 
            ["ws_floor_area", pl.col("ws_floor_area_factor")],
            ["ws_num_of_floors", pl.col("ws_num_floors_factor")], 
            ["ws_roof_age", pl.col("ws_roof_age_factor")], 
            ["ws_roof_covering",pl.col("ws_roof_covering_factor")], 
            ["ws_roof_geometry", pl.col("ws_roof_geometry_factor")],
            ["ws_construction_quality", pl.col("ws_construction_quality_factor")], 
            ["ws_roof_anchor", pl.col("ws_roof_anchor_factor")], 
            ["ws_roof_bracing", pl.col("ws_roof_bracing_factor")], 
            ["ws_roof_cladding", pl.col("ws_cladding_type_factor")],
            ["ws_frame_connection", pl.col("ws_frame_connection_factor")], 
            ["ws_storm_surge", pl.col("ws_storm_surge_factor")], 
            ["ws_catnet_score", pl.col("ws_catnet_intl_factor")],
        ]
    }