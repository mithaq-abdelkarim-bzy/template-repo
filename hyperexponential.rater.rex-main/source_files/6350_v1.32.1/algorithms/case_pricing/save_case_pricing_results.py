import hx 
import json
from algorithms.rating import run_schedule_rater

def save_case_pricing_results(hxd, progress):
    '''
    This function overwrites the values in the Rating Summary tab with the case priced results.
    '''  

    other_data, df = run_schedule_rater(hxd, progress, save_case_pricing = True)

    policy_length = hxd.policy_information.policy_length.selected or 1
    exchange_rate = hxd.policy_information.exchange_rate or 1
    
    us_perils = {
        "us_ws": "windstorm_us",
        "us_eq": "earthquake_us", 
        "us_tn": "tornado_us", 
        "us_ha": "hail_us", 
        "us_fl": "flood_us", 
        "us_wf": "wildfire_us",
    }
    intl_perils = {
        "intl_ws": "windstorm_intl", 
        "intl_eq": "earthquake_intl", 
        "intl_tn": "tornado_intl", 
        "intl_ha": "hail_intl", 
        "intl_fl": "flood_intl", 
        "intl_wf": "wildfire_intl"
    }
    for index, layer in enumerate(hxd.layers, start=1):
        
        cp = layer.case_pricing
        el_obj = layer.case_pricing.expected_loss
        tech_obj = layer.case_pricing.tech_premium

        # NOTE as data_assignment.py converts back to policy currency, need to revert here so not to double convert
           
        # Total KPIs
        
        other_data[f"pre_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] = cp.technical_premium / exchange_rate
        other_data[f"post_uw_adjustment_gross_tech_prem_gross_tech_prem_total_layer{index}"] = cp.technical_premium / exchange_rate

        other_data[f"sum_total_expected_loss_pre_uw_layer{index}"] = cp.total_exp_loss / exchange_rate
        other_data[f"sum_total_expected_loss_post_uw_layer{index}"] = cp.total_exp_loss / exchange_rate

        other_data[f"total_gg_benchmark_premium_pre_uw_layer{index}"] = cp.benchmark_premium / exchange_rate
        other_data[f"total_gg_benchmark_premium_post_uw_layer{index}"] = cp.benchmark_premium / exchange_rate

        brokerage = layer.brokerage or 0
        other_data[f"pre_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] = cp.technical_premium * (1 - brokerage) / exchange_rate
        other_data[f"post_uw_adjustment_net_tech_prem_net_tech_prem_total_layer{index}"] = cp.technical_premium * (1 - brokerage) / exchange_rate

        
        # Fire
        other_data[f"pre_uw_adjustment_expected_loss_fire_layer{index}"] = (el_obj.fire or 0) / exchange_rate
        other_data[f"post_uw_adjustment_expected_loss_fire_layer{index}"] = (el_obj.fire or 0) / exchange_rate
        
        other_data[f"pre_uw_adjustment_gross_tech_prem_fire_layer{index}"] = (tech_obj.fire or 0) / exchange_rate
        other_data[f"post_uw_adjustment_gross_tech_prem_fire_layer{index}"] = (tech_obj.fire or 0) / exchange_rate

        # US
        exp_loss_us = {v: (getattr(el_obj, k) or 0)/exchange_rate for k, v in us_perils.items()}
        other_data[f"pre_uw_adjustment_expected_loss_us_cat_layer{index}"] = exp_loss_us
        other_data[f"post_uw_adjustment_expected_loss_us_cat_layer{index}"] = exp_loss_us
        
        tech_prem_us = {v: (getattr(tech_obj, k) or 0)/exchange_rate for k, v in us_perils.items()}
        other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_layer{index}"] = tech_prem_us
        other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_layer{index}"] = tech_prem_us

        # US Rate
        us_cat_rate_dict = {}
        for peril in us_perils.values():
            us_cat_rate_dict[peril] = tech_prem_us[peril] / (other_data['sum_tiv_total_usd']/exchange_rate * policy_length) if other_data['sum_tiv_total_usd'] else 0
    
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"] = us_cat_rate_dict
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_layer{index}"] = us_cat_rate_dict

        # US totals
        other_data[f"pre_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] = (cp.us_exp_loss or 0) / exchange_rate
        other_data[f"post_uw_adjustment_expected_loss_us_cat_us_cat_total_layer{index}"] = (cp.us_exp_loss or 0) / exchange_rate

        other_data[f"pre_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] = (cp.us_tech_prem or 0) / exchange_rate
        other_data[f"post_uw_adjustment_gross_tech_prem_us_cat_us_cat_total_layer{index}"] = (cp.us_tech_prem or 0) / exchange_rate

        # US totals - rate 
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"] = sum(us_cat_rate_dict.values())
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_us_cat_us_cat_total_layer{index}"] = sum(us_cat_rate_dict.values())

        
        # Intl
        exp_loss_intl = {v: (getattr(el_obj, k) or 0)/exchange_rate for k, v in intl_perils.items()}
        other_data[f"pre_uw_adjustment_expected_loss_intl_cat_layer{index}"] = exp_loss_intl
        other_data[f"post_uw_adjustment_expected_loss_intl_cat_layer{index}"] = exp_loss_intl
        
        tech_prem_intl = {v: (getattr(tech_obj, k) or 0)/exchange_rate for k, v in intl_perils.items()}
        other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"] = tech_prem_intl
        other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_layer{index}"] = tech_prem_intl

        # Intl Rate
        intl_cat_rate_dict = {}
        for peril in intl_perils.values():
            intl_cat_rate_dict[peril] = tech_prem_intl[peril] / (other_data['sum_tiv_total_usd']/exchange_rate * policy_length) if other_data['sum_tiv_total_usd'] else 0
    
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"] = intl_cat_rate_dict
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_layer{index}"] = intl_cat_rate_dict
        
        
        # Intl totals
        other_data[f"pre_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] = (cp.intl_exp_loss or 0) / exchange_rate
        other_data[f"post_uw_adjustment_expected_loss_intl_cat_intl_cat_total_layer{index}"] = (cp.intl_exp_loss or 0) / exchange_rate
      
        other_data[f"pre_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] = (cp.intl_tech_prem or 0) / exchange_rate
        other_data[f"post_uw_adjustment_gross_tech_prem_intl_cat_intl_cat_total_layer{index}"] = (cp.intl_tech_prem or 0) / exchange_rate
        
        
        # Intl totals - rate
        other_data[f"pre_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"] = sum(intl_cat_rate_dict.values())
        other_data[f"post_uw_adjustment_gross_tech_prem_rate_intl_cat_intl_cat_total_layer{index}"] = sum(intl_cat_rate_dict.values())
        
        
        # NMP
        nmp_prem = cp.nmp_premium or 0
        nmp_exp_loss = nmp_prem / cp.technical_premium * cp.total_exp_loss if cp.technical_premium else 0
        other_data[f"pre_uw_adjustment_expected_loss_nmp_layer{index}"] = nmp_exp_loss / exchange_rate
        other_data[f"post_uw_adjustment_expected_loss_nmp_layer{index}"] = nmp_exp_loss / exchange_rate
        other_data[f"pre_uw_adjustment_gross_tech_prem_nmp_layer{index}"] = nmp_prem / exchange_rate
        other_data[f"post_uw_adjustment_gross_tech_prem_nmp_layer{index}"] = nmp_prem / exchange_rate
       

        # Marginal impact
        other_data[f'aep_impact_layer{index}'] = (cp.aep_impact_1_in_10 or 0) / exchange_rate
        other_data[f'oep_impact_layer{index}'] = (cp.oep_impact_1_in_250 or 0) / exchange_rate

        layer.risk_appetite_summary.aep_impact_1_in_10 = (cp.aep_impact_1_in_10 or 0) / exchange_rate
        layer.risk_appetite_summary.oep_impact_1_in_250 = (cp.oep_impact_1_in_250 or 0) / exchange_rate


        # TP params
        tp = layer.case_pricing.tp_breakdown

        other_data[f'total_coc_pre_uw_layer{index}'] = (tp.coc or 0) / exchange_rate
        other_data[f'total_coc_post_uw_layer{index}'] = (tp.coc or 0) / exchange_rate

        other_data[f'total_direct_expenses_pre_uw_layer{index}'] = (tp.dir_exp or 0) / exchange_rate
        other_data[f'total_direct_expenses_post_uw_layer{index}'] = (tp.dir_exp or 0) / exchange_rate

        other_data[f'total_indirect_expenses_pre_uw_layer{index}'] = (tp.ind_exp or 0) / exchange_rate
        other_data[f'total_indirect_expenses_post_uw_layer{index}'] = (tp.ind_exp or 0) / exchange_rate

        other_data[f'total_lae_pre_uw_layer{index}'] = (tp.lae or 0) / exchange_rate
        other_data[f'total_lae_post_uw_layer{index}'] = (tp.lae or 0) / exchange_rate

        other_data[f'total_ri_pre_uw_layer{index}'] = (tp.ri_cost or 0) / exchange_rate
        other_data[f'total_ri_post_uw_layer{index}'] = (tp.ri_cost or 0) / exchange_rate

        other_data[f'total_sd_pre_uw_layer{index}'] = (tp.sd_loading or 0) / exchange_rate
        other_data[f'total_sd_post_uw_layer{index}'] = (tp.sd_loading or 0) / exchange_rate



    # Output amended json
    hxd.temp.output_json = json.dumps(other_data)
    
    



