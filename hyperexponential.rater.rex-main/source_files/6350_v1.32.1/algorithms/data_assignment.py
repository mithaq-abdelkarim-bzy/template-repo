import hx
import polars as pl
from algorithms.constant import fire_rating_factors
import gc
import pandas as pd
from algorithms.utilities import pd_df_from_hx_list
import ast
import json
from collections import defaultdict

def data_assignment(hxd, other_data):
    '''
    Assigns data to frontend UI
    '''
    if hxd.policy_information.small_schedule_model and "cresta_zone" in other_data:
        for index, row in enumerate(hxd.schedule.schedule_table):
            if index < len(other_data["cresta_zone"]):
                row.cresta_zone = other_data["cresta_zone"][index] or "N/A"
                row.ws_tier = other_data["ws_tier"][index]
                row.wf_tier = other_data["wf_tier"][index]
                row.eq_gate = other_data["eq_gate"][index]
                row.ws_gate = other_data["ws_gate"][index]
    
                row.tiv_total = other_data["tiv_total"][index]
                for peril in ["eq", "ws", "fl", "scs", "wf"]:
                    setattr(row, f"risk_level_{peril}", other_data[f"risk_level_{peril}"][index] or "Unknown")
    
    if hxd.policy_information.large_schedule_model and "total_tiv_total" in other_data:
        hxd.schedule.schedule_total.tiv_total = other_data["total_tiv_total"]
    
    if other_data["valid_schedule"]:

        exchange_rate = hxd.policy_information.exchange_rate or 1

        # Account Segmentation
        for path in [
            "state", 
            "country",
            "state_country",
            "state_country_choropleth",
            "fire_occupancy", 
            "ws_zone", 
            "eq_zone", 
            "fl_risk_category", 
            "wf_risk_category", 
            "scs_risk_category"
        ]:
            summary_sc = [{k: (v * exchange_rate if k in ["tiv", "gu_loss", "gu_prem", "tech_prem_layer1", "tech_prem_layer2", "tech_prem_layer3", "tech_prem_layer4", "tech_prem_layer5", "tech_prem_layer6", "uw_adj_tech_prem_layer1", "uw_adj_tech_prem_layer2", "uw_adj_tech_prem_layer3", "uw_adj_tech_prem_layer4", "uw_adj_tech_prem_layer5", "uw_adj_tech_prem_layer6"] else v) for k, v in i.items()} for i in other_data.get(f"segmentation_{path}", [])]
            setattr(hxd.pricing_layer_segmentation, path, summary_sc)

            # we parse the summary_sc object for 'state_country' so we can send it to the choropleth custom UI component
            if path == 'state_country_choropleth':
                result = create_choropleth_charts_data(summary_sc)
                setattr(hxd.pricing_layer_segmentation, "state_country_choropleth_data", json.dumps(result))

        for index, layer in enumerate(hxd.layers, start=1):
            if f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}" in other_data:
                # Pre/Post UW Adj Summary
                layer.pre_uw_adjustment.gross_tech_prem.us_cat = {k: v * exchange_rate for k, v in other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"].items()}
                layer.pre_uw_adjustment.gross_tech_prem.intl_cat = {k: v * exchange_rate for k, v in other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"].items()}
                layer.post_uw_adjustment.gross_tech_prem.us_cat = {k: v * exchange_rate for k, v in other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"].items()}
                layer.post_uw_adjustment.gross_tech_prem.intl_cat = {k: v * exchange_rate for k, v in other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"].items()}

                if f"pre_uw_adjustment_expected_loss_us_cat_layer{index}" in other_data: # Condition included because updated policy model versions/renewed policies may have the rest of other data populated without these nodes
                    layer.pre_uw_adjustment.expected_loss.us_cat = {k: v * exchange_rate for k, v in other_data[f"pre_uw_adjustment_expected_loss_us_cat_layer{index}"].items()}
                    layer.pre_uw_adjustment.expected_loss.intl_cat = {k: v * exchange_rate for k, v in other_data[f"pre_uw_adjustment_expected_loss_intl_cat_layer{index}"].items()}
                    layer.post_uw_adjustment.expected_loss.us_cat = {k: v * exchange_rate for k, v in other_data[f"post_uw_adjustment_expected_loss_us_cat_layer{index}"].items()}
                    layer.post_uw_adjustment.expected_loss.intl_cat = {k: v * exchange_rate for k, v in other_data[f"post_uw_adjustment_expected_loss_intl_cat_layer{index}"].items()}

                    layer.pre_uw_adjustment.expected_loss.fire = other_data[f"pre_uw_adjustment_expected_loss_fire_layer{index}"] * exchange_rate
                    layer.post_uw_adjustment.expected_loss.fire = other_data[f"post_uw_adjustment_expected_loss_fire_layer{index}"] * exchange_rate

                    layer.pre_uw_adjustment.expected_loss.cyber = other_data.get(f"pre_uw_adjustment_expected_loss_cyber_layer{index}",0) * exchange_rate #.get() used to error capture for renewals
                    layer.post_uw_adjustment.expected_loss.cyber = other_data.get(f"post_uw_adjustment_expected_loss_cyber_layer{index}",0) * exchange_rate

                    layer.pre_uw_adjustment.expected_loss.us_cat.us_cat_total = other_data[f"pre_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] * exchange_rate
                    layer.pre_uw_adjustment.expected_loss.intl_cat.intl_cat_total = other_data[f"pre_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] * exchange_rate

                    layer.post_uw_adjustment.expected_loss.us_cat.us_cat_total = other_data[f"post_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] * exchange_rate
                    layer.post_uw_adjustment.expected_loss.intl_cat.intl_cat_total = other_data[f"post_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.gross_tech_prem.fire = other_data[f"pre_uw_adjustment_gross_tech_prem_fire_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.gross_tech_prem.fire = other_data[f"post_uw_adjustment_gross_tech_prem_fire_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.gross_tech_prem.cyber = other_data.get(f"pre_uw_adjustment_gross_tech_prem_cyber_layer{index}",0) * exchange_rate
                layer.perils.cyber.calculated_premium = other_data.get(f"pre_uw_adjustment_gross_tech_prem_cyber_layer{index}",0) * exchange_rate
                layer.post_uw_adjustment.gross_tech_prem.cyber = other_data.get(f"post_uw_adjustment_gross_tech_prem_cyber_layer{index}",0) * exchange_rate

                if f"pre_uw_adjustment_gross_tech_prem_nmp_layer{index}" in other_data:
                    layer.pre_uw_adjustment.gross_tech_prem.nmp = other_data[f"pre_uw_adjustment_gross_tech_prem_nmp_layer{index}"] * exchange_rate
                    layer.post_uw_adjustment.gross_tech_prem.nmp = other_data[f"post_uw_adjustment_gross_tech_prem_nmp_layer{index}"] * exchange_rate

                    layer.pre_uw_adjustment.expected_loss.nmp = other_data[f"pre_uw_adjustment_expected_loss_nmp_layer{index}"] * exchange_rate
                    layer.post_uw_adjustment.expected_loss.nmp = other_data[f"post_uw_adjustment_expected_loss_nmp_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total = other_data[f"pre_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.gross_tech_prem.gross_tech_prem_total = other_data[f"post_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.net_tech_prem.net_tech_prem_total = other_data[f"pre_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.net_tech_prem.net_tech_prem_total = other_data[f"post_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] * exchange_rate
                                                                                
                layer.pre_uw_adjustment.gross_tech_prem.us_cat.us_cat_total = other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] * exchange_rate
                layer.pre_uw_adjustment.gross_tech_prem.intl_cat.intl_cat_total = other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] * exchange_rate

                layer.post_uw_adjustment.gross_tech_prem.us_cat.us_cat_total = other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.gross_tech_prem.intl_cat.intl_cat_total = other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.gross_tech_prem_rate.us_cat = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"]
                layer.post_uw_adjustment.gross_tech_prem_rate.us_cat = other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"] 

                layer.pre_uw_adjustment.gross_tech_prem_rate.intl_cat = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"]
                layer.post_uw_adjustment.gross_tech_prem_rate.intl_cat = other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"]

                layer.pre_uw_adjustment.gross_tech_prem_rate.fire = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_fire_layer{index}"]
                layer.post_uw_adjustment.gross_tech_prem_rate.fire = other_data[f"post_uw_adjustment_gross_tech_prem_rate_fire_layer{index}"]

                layer.pre_uw_adjustment.gross_tech_prem_rate.cyber = other_data.get(f"pre_uw_adjustment_gross_tech_prem_rate_cyber_layer{index}",0)
                layer.post_uw_adjustment.gross_tech_prem_rate.cyber = other_data.get(f"post_uw_adjustment_gross_tech_prem_rate_cyber_layer{index}",0)

                if f"pre_uw_adjustment_gross_tech_prem_rate_nmp_layer{index}" in other_data:
                    layer.pre_uw_adjustment.gross_tech_prem_rate.nmp = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_nmp_layer{index}"]
                    layer.post_uw_adjustment.gross_tech_prem_rate.nmp = other_data[f"post_uw_adjustment_gross_tech_prem_rate_nmp_layer{index}"]

                layer.pre_uw_adjustment.gross_tech_prem_rate.gross_tech_prem_rate_total = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_gross_tech_prem_rate_total_layer{index}"]
                layer.post_uw_adjustment.gross_tech_prem_rate.gross_tech_prem_rate_total = other_data[f"post_uw_adjustment_gross_tech_prem_rate_gross_tech_prem_rate_total_layer{index}"]

                layer.pre_uw_adjustment.achieved_premium = other_data[f"pre_uw_adjustment_achieved_premium_layer{index}"]
                layer.post_uw_adjustment.achieved_premium = other_data[f"post_uw_adjustment_achieved_premium_layer{index}"]

                layer.pre_uw_adjustment.achieved_rate = other_data[f"pre_uw_adjustment_achieved_rate_layer{index}"]
                layer.post_uw_adjustment.achieved_rate = other_data[f"post_uw_adjustment_achieved_rate_layer{index}"]

                layer.pre_uw_adjustment.gross_tech_prem_rate.us_cat.us_cat_total = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"]
                layer.pre_uw_adjustment.gross_tech_prem_rate.intl_cat.intl_cat_total = other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"]

                layer.post_uw_adjustment.gross_tech_prem_rate.us_cat.us_cat_total = other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"]
                layer.post_uw_adjustment.gross_tech_prem_rate.intl_cat.intl_cat_total = other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"]

                # KPIs
                layer.pre_uw_adjustment.expected_loss.expected_loss = other_data[f"sum_total_expected_loss_pre_uw_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.expected_loss.expected_loss = other_data[f"sum_total_expected_loss_post_uw_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.benchmark_premium.benchmark_premium = other_data[f"total_gg_benchmark_premium_pre_uw_layer{index}"] * exchange_rate
                layer.post_uw_adjustment.benchmark_premium.benchmark_premium = other_data[f"total_gg_benchmark_premium_post_uw_layer{index}"] * exchange_rate

                layer.pre_uw_adjustment.expected_loss.elr = layer.pre_uw_adjustment.expected_loss.expected_loss / (layer.pre_uw_adjustment.achieved_premium * (1 - layer.brokerage)) if layer.pre_uw_adjustment.achieved_premium !=0 else 0
                layer.post_uw_adjustment.expected_loss.elr = layer.post_uw_adjustment.expected_loss.expected_loss / (layer.post_uw_adjustment.achieved_premium * (1 - layer.brokerage)) if layer.post_uw_adjustment.achieved_premium !=0 else 0

                layer.pre_uw_adjustment.benchmark_premium.bpi = layer.pre_uw_adjustment.achieved_premium / layer.pre_uw_adjustment.benchmark_premium.benchmark_premium if layer.pre_uw_adjustment.benchmark_premium.benchmark_premium !=0 else 0
                layer.post_uw_adjustment.benchmark_premium.bpi = layer.post_uw_adjustment.achieved_premium / layer.post_uw_adjustment.benchmark_premium.benchmark_premium if layer.post_uw_adjustment.benchmark_premium.benchmark_premium !=0 else 0

                layer.pre_uw_adjustment.gross_tech_prem.tpi = layer.pre_uw_adjustment.achieved_premium / layer.pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total if layer.pre_uw_adjustment.gross_tech_prem.gross_tech_prem_total !=0 else 0
                layer.post_uw_adjustment.gross_tech_prem.tpi = layer.post_uw_adjustment.achieved_premium / layer.post_uw_adjustment.gross_tech_prem.gross_tech_prem_total if layer.post_uw_adjustment.gross_tech_prem.gross_tech_prem_total !=0 else 0
                
                # 1 in 250 to CAT Premium Ratio
                us_cat_achieved_premium = layer.post_uw_adjustment.gross_tech_prem.tpi * (other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"]["windstorm_us"] + other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"]["earthquake_us"]) * exchange_rate
                layer.risk_appetite_summary.oep_impact_1_in_250_cat_premium_ratio  = ((layer.risk_appetite_summary.oep_impact_1_in_250 or 0) / us_cat_achieved_premium) if (us_cat_achieved_premium and (us_cat_achieved_premium > 0)) else 0

                # Fire Summary
                layer.perils.fire.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"fire_modifier_summary_layer{index}"].items()}

                layer.perils.fire.occupancy_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fire_occupancy_summary_layer{index}"]]
                layer.perils.fire.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fire_construction_summary_layer{index}"]]
                layer.perils.fire.sprinkler_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fire_sprinkler_summary_layer{index}"]]

                # Wildfire Summary
                layer.perils.wildfire.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"wf_modifier_summary_layer{index}"].items()}

                layer.perils.wildfire.risk_category_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"wf_risk_category_summary_layer{index}"]]
                layer.perils.wildfire.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"wf_construction_summary_layer{index}"]]
                layer.perils.wildfire.occupancy_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"wf_occupancy_summary_layer{index}"]]

                # Windstorm Summary
                layer.perils.named_windstorm.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"ws_modifier_summary_layer{index}"].items()}

                layer.perils.named_windstorm.occupancy_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"ws_occupancy_summary_layer{index}"]]
                layer.perils.named_windstorm.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"ws_construction_summary_layer{index}"]]
                layer.perils.named_windstorm.gate_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"ws_gate_summary_layer{index}"]]
                layer.perils.named_windstorm.ws_zone_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"ws_zone_summary_layer{index}"]]
                layer.perils.named_windstorm.distance_from_coast_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"distance_from_coast_summary_layer{index}"]]
                layer.perils.named_windstorm.year_built_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"year_built_summary_layer{index}"]]
                layer.perils.named_windstorm.risk_category_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"ws_risk_category_summary_layer{index}"]]

                # Earthquake Summary
                layer.perils.quake.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"eq_modifier_summary_layer{index}"].items()}

                layer.perils.quake.occupancy_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"eq_occupancy_summary_layer{index}"]]
                layer.perils.quake.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"eq_construction_summary_layer{index}"]]
                layer.perils.quake.cresta_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"eq_cresta_summary_layer{index}"]]
                layer.perils.quake.risk_category_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"eq_risk_category_summary_layer{index}"]]
                layer.perils.quake.eq_zone_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"eq_zone_summary_layer{index}"]]

                # Flood Summary
                layer.perils.flood.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"fl_modifier_summary_layer{index}"].items()}

                layer.perils.flood.risk_category_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fl_risk_category_summary_layer{index}"]]
                layer.perils.flood.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fl_construction_summary_layer{index}"]]
                layer.perils.flood.num_of_floors_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"fl_num_of_floors_summary_layer{index}"]]

                # SCS Summary
                layer.perils.scs.modifier_summary = {k: (v * exchange_rate if k in ["sum_tiv_total_usd", "uw_adj_tech_prem"] else v) for k, v in other_data[f"scs_modifier_summary_layer{index}"].items()}

                layer.perils.scs.risk_category_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"scs_risk_category_summary_layer{index}"]]
                layer.perils.scs.construction_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"scs_construction_summary_layer{index}"]]
                layer.perils.scs.occupancy_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "uw_adj_tech_prem", "gu_loss", "gu_prem"] else v) for k, v in i.items()} for i in other_data[f"scs_occupancy_summary_layer{index}"]]

                # Cat AOP Split
                us_aop_perils = ["fire_us", "wildfire_us", "hail_us", "tornado_us", "flood_us"]
                intl_aop_perils = ["fire_intl", "wildfire_intl", "hail_intl", "tornado_intl", "flood_intl"]
                intl_cat_perils = ["windstorm_intl", "earthquake_intl"]

                us_aop_perils_premium = sum([other_data[f"{peril}_gg_technical_premium_post_uw_layer{index}"] for peril in us_aop_perils]) * exchange_rate
                intl_aop_perils_premium = sum([other_data[f"{peril}_gg_technical_premium_post_uw_layer{index}"] for peril in intl_aop_perils]) * exchange_rate
                intl_cat_perils_premium = sum([other_data[f"{peril}_gg_technical_premium_post_uw_layer{index}"] for peril in intl_cat_perils]) * exchange_rate

                #exclude nmp premium for calculating aop/cat splits to ensure it adds u to 100%
                gross_technnical_prem_excl_nmp = layer.post_uw_adjustment.gross_tech_prem.gross_tech_prem_total #HM: Removed logic here to subtract NMP premium following update to set NMP load to 0

                layer.cat_aop_split.perc_us_wind = other_data[f"windstorm_us_gg_technical_premium_post_uw_layer{index}"] * exchange_rate / gross_technnical_prem_excl_nmp if gross_technnical_prem_excl_nmp != 0 else 0
                layer.cat_aop_split.perc_us_quake = other_data[f"earthquake_us_gg_technical_premium_post_uw_layer{index}"] * exchange_rate / gross_technnical_prem_excl_nmp if gross_technnical_prem_excl_nmp !=0 else 0
                layer.cat_aop_split.perc_us_aop = us_aop_perils_premium / gross_technnical_prem_excl_nmp if gross_technnical_prem_excl_nmp !=0 else 0
                layer.cat_aop_split.perc_intl_cat = intl_cat_perils_premium / gross_technnical_prem_excl_nmp if gross_technnical_prem_excl_nmp !=0 else 0
                layer.cat_aop_split.perc_intl_aop = intl_aop_perils_premium / gross_technnical_prem_excl_nmp if gross_technnical_prem_excl_nmp !=0 else 0

                
                try:
                    if other_data[f"sum_total_trapped_exposure_usd_layer{index}"]:
                        layer.trapped_exposure = other_data[f"sum_total_trapped_exposure_usd_layer{index}"] * exchange_rate
                        layer.trapped_exposure_rate = other_data[f"achieved_premium_100_gg_usd_layer{index}"] / other_data[f"sum_total_trapped_exposure_usd_layer{index}"] if other_data[f"sum_total_trapped_exposure_usd_layer{index}"] !=0 else 0
                except KeyError:
                    pass

                # TP Components
                layer.pre_uw_adjustment.tech_prem_components.coc = other_data[f'total_coc_pre_uw_layer{index}'] * exchange_rate
                layer.pre_uw_adjustment.tech_prem_components.direct_expenses = other_data[f'total_direct_expenses_pre_uw_layer{index}'] * exchange_rate
                layer.pre_uw_adjustment.tech_prem_components.indirect_expenses = other_data[f'total_indirect_expenses_pre_uw_layer{index}'] * exchange_rate
                layer.pre_uw_adjustment.tech_prem_components.lae = other_data[f'total_lae_pre_uw_layer{index}'] * exchange_rate
                layer.pre_uw_adjustment.tech_prem_components.ri = other_data[f'total_ri_pre_uw_layer{index}'] * exchange_rate
                layer.pre_uw_adjustment.tech_prem_components.sd = other_data[f'total_sd_pre_uw_layer{index}'] * exchange_rate
                if f'total_investment_income_pre_uw_layer{index}' in other_data:
                    layer.pre_uw_adjustment.tech_prem_components.investment_income = other_data[f'total_investment_income_pre_uw_layer{index}'] * exchange_rate

                layer.post_uw_adjustment.tech_prem_components.coc = other_data[f'total_coc_post_uw_layer{index}'] * exchange_rate
                layer.post_uw_adjustment.tech_prem_components.direct_expenses = other_data[f'total_direct_expenses_post_uw_layer{index}'] * exchange_rate
                layer.post_uw_adjustment.tech_prem_components.indirect_expenses = other_data[f'total_indirect_expenses_post_uw_layer{index}'] * exchange_rate
                layer.post_uw_adjustment.tech_prem_components.lae = other_data[f'total_lae_post_uw_layer{index}'] * exchange_rate
                layer.post_uw_adjustment.tech_prem_components.ri = other_data[f'total_ri_post_uw_layer{index}'] * exchange_rate
                layer.post_uw_adjustment.tech_prem_components.sd = other_data[f'total_sd_post_uw_layer{index}'] * exchange_rate
                if f'total_investment_income_post_uw_layer{index}' in other_data:
                    layer.post_uw_adjustment.tech_prem_components.investment_income = other_data[f'total_investment_income_pre_uw_layer{index}'] * exchange_rate

                # Top 20 Summaries
                for peril_name, peril_abbr in zip(["fire", "wildfire", "named_windstorm", "quake", "flood", "scs"],
                                                    ["fire", "wf", "ws", "eq", "fl", "scs"]):
                    struct = getattr(layer.perils, peril_name)
                    if hxd.policy_information.top_20_sort_by == "TIV":
                        struct.top_20_locations_summary = [{k: (v * exchange_rate if k in ["tiv_buildings", "tiv_contents_total", "tiv_bi", "tiv_total", "uw_adj_tech_prem", "itv"] else v) for k, v in i.items()} for i in other_data[f"{peril_abbr}_top_20_locations_summary_layer{index}_tiv"]]
                    elif hxd.policy_information.top_20_sort_by == "Expected Loss":
                        struct.top_20_locations_summary = [{k: (v * exchange_rate if k in ["tiv_buildings", "tiv_contents_total", "tiv_bi", "tiv_total", "uw_adj_tech_prem", "itv"] else v) for k, v in i.items()} for i in other_data[f"{peril_abbr}_top_20_locations_summary_layer{index}_rate"]]


                # Other Summaries
                layer.other_segmentations.state_summary = [{k: (v * exchange_rate if k in ["tiv", "itv", "tech_prem", "gu_loss", "gu_prem", "uw_adj_tech_prem"] else v) for k, v in i.items()} for i in other_data[f"state_summary_layer{index}"]]

                # CGear metrics
                climate_metrics = hxd.non_layer_summary.climate_metrics
                climate_metrics.score_locations = other_data["climate_metrics_score_locations"]
                climate_metrics.weighted_climate_score = other_data["climate_metrics_weighted_climate_score"]
                climate_metrics.climate_score_description = other_data["climate_metrics_climate_score_description"]

                # Account Segmentation
                setattr(hxd.pricing_layer_segmentation.marginal_impact_summary.mi_1_in_10_aep_pt, f"layer{index}", other_data[f'aep_impact_layer{index}'] * exchange_rate)
                setattr(hxd.pricing_layer_segmentation.marginal_impact_summary.mi_1_in_250_oep_pt, f"layer{index}", other_data[f'oep_impact_layer{index}'] * exchange_rate)


def generate_output_file(hxd, df, other_data):
    '''
    Generate output feather file (large policy model) for actuarial use
    '''
    
    columns = [
        "loc_id", "zip", "state", "county", "country", "occupancy", "eq_gate_no", "ws_gate_no", "tiv_buildings", "tiv_contents", "tiv_other", "tiv_bi",
        "cresta_zone", "ws_tier", "wf_tier", "catnet_score_tn", "catnet_score_ha", "catnet_score_fl", "catnet_score_wf", "catnet_score_ws", "catnet_score_eq",
        "exchange_rate", "longitude", "latitude", "industry", "fire_covered", "scs_covered", "fl_covered", "wf_covered", "ws_covered", "eq_covered",
        "bi_waiting_period_factor", "fire_construction_factor", "fire_sprinkler_factor", "fire_pc_code_factor", "fire_mexican_fonden_factor", "fire_size_discount_factor",
        "wildfire_catnet_score_load", "wildfire_occupancy_load", "wildfire_construction_load", "wildfire_pc_code_load", "wildfire_size_discount_load", "wildfire_riskmeter_load",
        "ws_occupancy_factor", "ws_construction_factor", "ws_year_built_factor", "ws_floor_area_factor", "ws_num_floors_factor", "ws_roof_age_factor", 
        "ws_roof_covering_factor", "ws_roof_geometry_factor", "ws_storm_surge_factor", "ws_catnet_intl_factor", "eq_occupancy_factor", "eq_construction_factor",
        "eq_year_built_factor", "eq_num_floors_factor", "eq_catnet_intl_factor", "hail_occupancy_load", "hail_construction_load", "hail_year_built_load",
        "hail_floor_area_load", "hail_roof_age_load", "hail_roof_covering_load", "hail_roof_geometry_load", "hail_catnet_score_load", "hail_size_discount_load", "tornado_occupancy_load",
        "tornado_construction_load", "tornado_year_built_load", "tornado_catnet_score_load", "tornado_size_discount_load", "fl_construction_rating_factor", "fl_num_floors_rating_factor",
        "fl_basement_rating_factor", "fl_elevation_rating_factor", "fl_catnet_rating_factor", "fl_size_discount_rating_factor", "constr_code", "year_built", "sprinkler", "pc_code", "currency",
        "floor_area", "roof_age", "roof_covering", "roof_geometry", "num_stories", "basement", "building_elevation", "distance_from_coast",
        "property_description", "constr_description", "num_buildings", "fire_deductible",

        "fl_katrisk_risk_rating_factor",
        "cgear_score_total",

        'tiv_buildings_usd', 'tiv_contents_usd', 
        'tiv_other_usd', 'tiv_bi_usd', 'tiv_total_usd', 
        "atc_code"
        ]
    
    if "fema_flood_zone" in df.columns:
        columns += ["fema_flood_zone"]

    for index, layer in enumerate(hxd.layers, start=1):
        columns += [
            f"fire_deductible_layer{index}", 
            f"ws_deductible_layer{index}", 
            f"eq_deductible_layer{index}", 
            f"scs_deductible_layer{index}", 
            f"fl_deductible_layer{index}", 
            f"earthquake_us_total_expected_loss_pre_uw_layer{index}",
            f"windstorm_us_total_expected_loss_pre_uw_layer{index}",
            f"earthquake_us_total_expected_loss_post_uw_layer{index}",
            f"windstorm_us_total_expected_loss_post_uw_layer{index}",
            f"windstorm_us_sd_pre_uw_layer{index}",
            f"earthquake_us_sd_pre_uw_layer{index}",
            f"windstorm_us_sd_post_uw_layer{index}",
            f"earthquake_us_sd_post_uw_layer{index}",
            f"eq_selected_sublimit_layer{index}",
            f"ws_selected_sublimit_layer{index}",
            f"fl_selected_sublimit_layer{index}",
            f"scs_selected_sublimit_layer{index}",
            f"earthquake_us_ri_cost_pre_uw_layer{index}",
            f"windstorm_us_ri_cost_pre_uw_layer{index}",
            f"earthquake_us_ri_cost_post_uw_layer{index}",
            f"windstorm_us_ri_cost_post_uw_layer{index}",
            f"earthquake_us_lae_pre_uw_layer{index}",
            f"windstorm_us_lae_pre_uw_layer{index}",
            f"earthquake_us_lae_post_uw_layer{index}",
            f"windstorm_us_lae_post_uw_layer{index}",
                    ]

        perils_short = ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]
        perils_short_scs = ["eq", "fire", "fl", "scs", "wf", "ws"]
        perils = ["earthquake", "fire", "flood", "hail", "tornado", "wildfire", "windstorm"]
        perils_scs = ["fire", "wildfire", "windstorm", "earthquake", "scs", "flood"]

        for status in ["pre", "post"]:
            for peril in perils_short + ["total"]:
                columns += [
                    f"premtp_gn_max_{status}_uw_usd_100_{peril}_layer{index}",
                ]

            for peril in perils:
                columns += [
                    f"{peril}_total_expected_loss_{status}_uw_layer{index}", 
                    f"{peril}_cost_of_capital_{status}_uw_layer{index}", 
                ]

        for peril in perils:
            columns += [f"{peril}_entry_perc_layer{index}", f"{peril}_exit_perc_layer{index}", f"{peril}_worth_percent_layer{index}"]

        for peril in perils_scs:
            columns += [f"{peril}_tiv_exposed_layer{index}"]

        for peril in perils_short_scs:
            columns += [f"rate_base_total_{peril}_layer{index}"]

    output_df = df[columns]

    output_df = output_df.with_columns(
        pl.lit(other_data["bi_indemnity_period_factor"]).alias("rfr_bi_indemnityperiod"),
        pl.lit(other_data["cbi_load"]).alias("rfr_bi_cbi"),
        pl.lit(0).alias("tiv_contents1_usd") # replicates logic for small model. TODO: correct?
    )

    del df
    gc.collect()

    output_df = output_df.rename({
        # "eq_gate_no": "gate_no_eq", "ws_gate_no": "gate_no_ws", 
        "eq_gate_no": "eq_gate", "ws_gate_no": "ws_gate", 
        "exchange_rate": "ex_rate", "bi_waiting_period_factor": "rfr_bi_waitingperiod",
        "fire_construction_factor": "rfr_construction_fire", "fire_sprinkler_factor": "rfr_sprinkler_fire", "fire_pc_code_factor": "rfr_ppc_fire",
        "fire_mexican_fonden_factor": "rfr_mexicanfonden_fire", "fire_size_discount_factor": "rfr_sizedisc_fire","wildfire_catnet_score_load": "rfr_hazardscore_wf", "wildfire_occupancy_load": "rfr_occ_wf",
        "wildfire_construction_load": "rfr_construction_wf", "wildfire_pc_code_load": "rfr_ppc_wf", "wildfire_size_discount_load": "rfr_size_discount_wf", "wildfire_riskmeter_load": "rfr_hazardscoreriskmeter_wf",
        "ws_occupancy_factor": "rfr_occ_ws", "ws_construction_factor": "rfr_construction_ws", "ws_year_built_factor": "rfr_yearbuilt_ws", 
        "ws_floor_area_factor": "rfr_floorarea_ws", "ws_num_floors_factor": "rfr_nofloors_ws", "ws_roof_age_factor": "rfr_roofage_ws", 
        "ws_roof_covering_factor": "rfr_roofcovering_ws", "ws_roof_geometry_factor": "rfr_roofgeometry_ws", "ws_storm_surge_factor": "rfr_ss_ws", 
        "ws_catnet_intl_factor": "rfr_hazardscore_ws", "eq_occupancy_factor": "rfr_occ_eq", "eq_construction_factor": "rfr_construction_eq", 
        "eq_year_built_factor": "rfr_yearbuilt_eq", "eq_num_floors_factor": "rfr_nofloors_eq", "eq_catnet_intl_factor": "rfr_hazardscore_eq",
        "hail_occupancy_load": "rfr_occ_ha", "hail_construction_load": "rfr_construction_ha", "hail_year_built_load": "rfr_yearbuilt_ha",
        "hail_floor_area_load": "rfr_floorarea_ha", "hail_roof_age_load": "rfr_roofage_ha", "hail_roof_covering_load": "rfr_roofcovering_ha", 
        "hail_roof_geometry_load": "rfr_roofgeometry_ha", "hail_catnet_score_load": "rfr_hazardscore_ha", "hail_size_discount_load": "rfr_size_discount_ha" ,"tornado_occupancy_load": "rfr_occ_tn",
        "tornado_construction_load": "rfr_construction_tn", "tornado_year_built_load": "rfr_yearbuilt_tn", "tornado_catnet_score_load": "rfr_hazardscore_tn", "tornado_size_discount_load": "rfr_size_discount_tn",
        "fl_construction_rating_factor": "rfr_construction_fl", "fl_num_floors_rating_factor": "rfr_nofloors_fl", "fl_basement_rating_factor": "rfr_basement_fl", 
        "fl_elevation_rating_factor": "rfr_elevation_fl", "fl_catnet_rating_factor": "rfr_hazardscore_fl", "fl_size_discount_rating_factor": "rfr_size_discount_fl",

        "fl_katrisk_risk_rating_factor": "rfr_katriskscore_fl",
        "tiv_buildings_usd": "tiv_building_usd",
    })

    
    output_df = output_df.with_columns(
        pl.lit(other_data['fire_risk_quality_factor']).alias('rfr_riskquality_fire')
    )

    for index, layer in enumerate(hxd.layers, start=1):
        output_df = output_df.rename({
            f"fire_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_fire_total_layer{index}",
            f"wildfire_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_wf_layer{index}", 
            f"windstorm_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_ws_layer{index}", 
            f"earthquake_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_eq_layer{index}",
            f"hail_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_ha_layer{index}",
            f"tornado_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_tn_layer{index}",
            f"flood_total_expected_loss_pre_uw_layer{index}": f"el_pre_uw_usd_100_fl_layer{index}",
            f"fire_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_fire_total_layer{index}",
            f"wildfire_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_wf_layer{index}", 
            f"windstorm_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_ws_layer{index}", 
            f"earthquake_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_eq_layer{index}",
            f"hail_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_ha_layer{index}",
            f"tornado_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_tn_layer{index}",
            f"flood_total_expected_loss_post_uw_layer{index}": f"el_post_uw_usd_100_fl_layer{index}",
            f"fire_deductible_layer{index}": f"deductible_usd_fire_layer{index}", 
            f"fire_tiv_exposed_layer{index}": f"tivexposed_total_usd_fire{index}",
            f"wildfire_tiv_exposed_layer{index}": f"tivexposed_total_usd_wf_layer{index}",
            f"ws_deductible_layer{index}": f"deductible_usd_ws_layer{index}",
            f"windstorm_tiv_exposed_layer{index}": f"tivexposed_total_usd_ws_layer{index}", 
            f"eq_deductible_layer{index}": f"deductible_usd_eq_layer{index}",
            f"earthquake_tiv_exposed_layer{index}": f"tivexposed_total_usd_eq_layer{index}",
            f"scs_deductible_layer{index}": f"deductible_usd_scs_layer{index}",
            f"scs_tiv_exposed_layer{index}": f"tivexposed_total_usd_scs_layer{index}",
            f"fl_deductible_layer{index}": f"deductible_usd_fl_layer{index}",
            f"flood_tiv_exposed_layer{index}": f"tivexposed_total_usd_fl_layer{index}",
            f"earthquake_us_ri_cost_pre_uw_layer{index}": f"ri_cost_pre_uw_eq_usd100_layer{index}",
            f"windstorm_us_ri_cost_pre_uw_layer{index}": f"ri_cost_pre_uw_ws_usd100_layer{index}",
            f"earthquake_us_lae_pre_uw_layer{index}": f"lae_pre_uw_eq_usd100_layer{index}",
            f"windstorm_us_lae_pre_uw_layer{index}": f"lae_pre_uw_ws_usd100_layer{index}",
            f"earthquake_us_total_expected_loss_pre_uw_layer{index}": f"aal_pre_uw_eq_us_usd_100_layer{index}",
            f"windstorm_us_total_expected_loss_pre_uw_layer{index}": f"aal_pre_uw_ws_us_usd_100_layer{index}",
            f"earthquake_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_eq_layer{index}",
            f"flood_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_fl_layer{index}",
            f"hail_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_ha_layer{index}",
            f"tornado_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_tn_layer{index}",
            f"wildfire_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_wf_layer{index}",
            f"windstorm_cost_of_capital_pre_uw_layer{index}": f"coc_pre_uw_usd_100_ws_layer{index}",
            f"earthquake_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_eq_layer{index}",
            f"flood_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_fl_layer{index}",
            f"hail_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_ha_layer{index}",
            f"tornado_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_tn_layer{index}",
            f"wildfire_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_wf_layer{index}",
            f"windstorm_cost_of_capital_post_uw_layer{index}": f"coc_post_uw_usd_100_ws_layer{index}",
            f"earthquake_us_total_expected_loss_post_uw_layer{index}": f"aal_post_uw_eq_us_usd_100_layer{index}",
            f"windstorm_us_total_expected_loss_post_uw_layer{index}": f"aal_post_uw_ws_us_usd_100_layer{index}", 
            f"windstorm_us_sd_pre_uw_layer{index}": f"sd_pre_uw_ws_usd100_layer{index}",
            f"earthquake_us_sd_pre_uw_layer{index}": f"sd_pre_uw_eq_usd100_layer{index}",
            f"windstorm_us_sd_post_uw_layer{index}": f"sd_post_uw_ws_usd100_layer{index}",
            f"earthquake_us_sd_post_uw_layer{index}": f"sd_post_uw_eq_usd100_layer{index}",
            f"eq_selected_sublimit_layer{index}": f"sublimit_usd_eq_layer{index}",
            f"ws_selected_sublimit_layer{index}": f"sublimit_usd_ws_layer{index}",
            f"fl_selected_sublimit_layer{index}": f"sublimit_usd_fl_layer{index}",
            f"scs_selected_sublimit_layer{index}": f"sublimit_usd_scs_layer{index}",
            f"earthquake_us_ri_cost_post_uw_layer{index}": f"ri_cost_post_uw_eq_usd100_layer{index}",
            f"windstorm_us_ri_cost_post_uw_layer{index}": f"ri_cost_post_uw_ws_usd100_layer{index}",
            f"earthquake_us_lae_post_uw_layer{index}": f"lae_post_uw_eq_usd100_layer{index}",
            f"windstorm_us_lae_post_uw_layer{index}": f"lae_post_uw_ws_usd100_layer{index}",
        })

        perils = {
            "fire": "fire", 
            "wildfire": "wf", 
            "windstorm": "ws", 
            "earthquake": "eq", 
            "tornado": "tn", 
            "hail": "ha", 
            "flood": "fl"
        }

        for peril in perils:
            output_df = output_df.rename({
                f"{peril}_entry_perc_layer{index}": f"flc_entry_{perils[peril]}_layer{index}",
                f"{peril}_exit_perc_layer{index}": f"flc_exit_{perils[peril]}_layer{index}",
                f"{peril}_worth_percent_layer{index}": f"flc_worth_{perils[peril]}_layer{index}",
            })

        perils = ["fire_total", "wf", "ws", "eq", "tn", "ha", "fl"]
        output_df = output_df.with_columns(
            output_df.select([f"el_pre_uw_usd_100_{peril}_layer{index}" for peril in perils]).sum(axis=1)\
                .alias(f"el_pre_uw_usd_100_total_layer{index}"),
            output_df.select([f"el_post_uw_usd_100_{peril}_layer{index}" for peril in perils]).sum(axis=1)\
                .alias(f"el_post_uw_usd_100_total_layer{index}"),
            )

    with hxd.schedule.large_schedule_workflow.schedule_output_file.open("b") as f:
        output_df.write_ipc(f)

def create_country_state_summary(hxd, input_list):
    'Create country/summary nested list for Selector purposes in the UI'
    if len(input_list)>0:
        # Convert hx list to pandas DataFrame
        state_summary_df = pd_df_from_hx_list(input_list)

        # Separate a single State/Country column into state and country columns
        state_summary_df['name'] = state_summary_df['name'].apply(ast.literal_eval)
        state_summary_df[['state', 'country']] = pd.DataFrame(state_summary_df['name'].tolist(), index=state_summary_df.index)

        # Create nested list
        final_summary_table = []

        for country, group in state_summary_df.groupby("country"):
            country_dict = {
                "country": country,
                "country_list": []
            }
            total_tiv_sum = 0
            for _, row in group.iterrows():
                state_dict = {
                    "name": row["state"],
                    "tiv": row["tiv"],
                    "num_locations": row["num_locations"],
                    "gu_loss": row["gu_loss"],
                    "gu_tech_rate": row["gu_tech_rate"],
                    "gu_prem": row["gu_prem"],
                    "tech_prem_layer1": row["tech_prem_layer1"],
                    "tech_prem_layer2": row["tech_prem_layer2"],
                    "tech_prem_layer3": row["tech_prem_layer3"],
                    "tech_prem_layer4": row["tech_prem_layer4"],
                    "tech_prem_layer5": row["tech_prem_layer5"],
                    "tech_prem_layer6": row["tech_prem_layer6"],
                    "uw_adj_tech_prem_layer1": row["uw_adj_tech_prem_layer1"],
                    "uw_adj_tech_prem_layer2": row["uw_adj_tech_prem_layer2"],
                    "uw_adj_tech_prem_layer3": row["uw_adj_tech_prem_layer3"],
                    "uw_adj_tech_prem_layer4": row["uw_adj_tech_prem_layer4"],
                    "uw_adj_tech_prem_layer5": row["uw_adj_tech_prem_layer5"],
                    "uw_adj_tech_prem_layer6": row["uw_adj_tech_prem_layer6"]
                }
                country_dict["country_list"].append(state_dict)
                total_tiv_sum  +=row["tiv"]
            country_dict["total_tiv"] = total_tiv_sum
            final_summary_table.append(country_dict)
        # Sort table to have highest TIV country (usually USA) as a default selector
        final_summary_table.sort(key=lambda x: x["total_tiv"], reverse=True)
        
        
        hxd.pricing_layer_segmentation.state_country_outer = final_summary_table


def create_choropleth_charts_data(summary_sc):
    """
    Normalizes the summary_sc data in a better format for the frontend.
    Args:
        data (list[dict]): A list of dictionaries containing the summary_sc data for 'state_country'
    Returns:
        list[dict]: A new list of dictionaries with normalized and flattened data to be used in the Choropleth charts 
    """

    # Normalize and flatten the data first
    # We do a try/catch in case the data is in the old format. If we're coming from a version that does not support the new choropleth charts,
    # then we just return an empty list as this data will not be used.

    normalized_data = list()
    try:
        for row in summary_sc:
            summary_dict = {
                "state": row["name"][0],
                "country": row["name"][1],
                "lat": row["name"][2],
                "lon": row["name"][3],
                "tiv": row["tiv"],
                "num_locations": row["num_locations"],
                "gu_loss": row["gu_loss"],
                "gu_tech_rate": row["gu_tech_rate"]
            }
            normalized_data.append(summary_dict)
    except Exception as err:
        pass

    return normalized_data