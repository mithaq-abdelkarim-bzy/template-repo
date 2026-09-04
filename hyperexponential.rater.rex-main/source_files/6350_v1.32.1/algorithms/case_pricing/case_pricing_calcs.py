import hx 



def case_pricing_calc_tech_premium(hxd, progress):

    team = hxd.policy_information.team or "NACP"
    exchange_rate = hxd.policy_information.exchange_rate or 1
    policy_length = hxd.policy_information.policy_length.selected or 1

    tps_team = hx.params.assumption_1_in_250_team.set_index('Field')[team].to_dict()
    tps_pricing = hx.params.assumption_1_in_250_pricing.iloc[0].to_dict()

    wind_uplift = tps_team['CAT Uplift'] + 1
    nmp_load = tps_team['NMP Load'] + 1

    capital = tps_pricing['held_capital']
    group_cat_risk = tps_pricing['gross_group_cat_risk']
    add_group_cat_risk = tps_pricing['additional_group_cat_risk']
    add_capital_req = tps_team['Corresponding Capital Required']
    roc = tps_pricing['roc']

    cov = tps_team["CoV"]
    sd = tps_team["Standard Deviation"]

    non_cat_capital_alloc = tps_pricing['fire_aop_init_capital_allocation']

    lae_perc = tps_team["LAE %"]
    dir_expenses = tps_team["Direct Expenses Per Premium"]
    ind_expenses = tps_team["Indirect Expenses Per Policy"]
    inv_ret = tps_team["Investment Income Per Premium"]

    us_perils = ["us_ws", "us_eq", "us_tn", "us_ha", "us_fl", "us_wf"]
    intl_perils = ["intl_ws", "intl_eq", "intl_tn", "intl_ha", "intl_fl", "intl_wf"]
    all_perils = ["fire"] + us_perils + intl_perils
    cat_perils = ["us_ws", "us_eq"]

    for layer in hxd.layers:
        
        if layer.case_pricing.total_exp_loss == 0:
            continue
        
        el_obj = layer.case_pricing.expected_loss
        tech_obj = layer.case_pricing.tech_premium

        # Total exp loss includes NMP load as this is added in the 'totals' script
        total_exp_loss = layer.case_pricing.total_exp_loss
        total_exp_loss_usd = total_exp_loss / exchange_rate       
        cat_exp_loss_usd = sum([getattr(el_obj, peril) or 0 for peril in cat_perils]) * nmp_load / exchange_rate

        tp_ri_cost = (layer.case_pricing.tp_breakdown.ri_cost or 0) / exchange_rate

        marginal_1_in_250 = (layer.case_pricing.oep_impact_1_in_250 or 0) / exchange_rate
        quoted_prem_usd = (layer.achieved_premium_100_gg or 0) / exchange_rate
        brokerage = layer.brokerage or 0

        # Cost of Capital - Cat
        tp_cat_coc = marginal_1_in_250 * capital / group_cat_risk * add_capital_req * add_group_cat_risk * 100 * roc * policy_length

        # Cost of Capital - Attritional
        tp_att_coc = (total_exp_loss_usd - cat_exp_loss_usd) * non_cat_capital_alloc * roc

        # LAE
        tp_lae = cat_exp_loss_usd * lae_perc

        tp_calc_numerator = total_exp_loss_usd + tp_att_coc + tp_cat_coc + ind_expenses + tp_ri_cost + tp_lae
        # Direct Expenses
        tp_dir_exp = tp_calc_numerator * ((1 / (1 - dir_expenses)) - 1)
        
        # Investment Return
        tp_inv_ret = tp_calc_numerator * ((1 / (1 + inv_ret)) - 1)

        # Benchmark & technical premium
        if total_exp_loss_usd > 0:
            technical_prem_usd = ((tp_calc_numerator) / (1 - dir_expenses + inv_ret)) / (1 - brokerage)
        else:
            technical_prem_usd = 0

        benchmark_prem_usd = (total_exp_loss_usd / 0.7) / (1 - brokerage)   # USD
        technical_prem_minimum = (benchmark_prem_usd * 0.7) / 0.75  # USD

        ri_ratio = tp_ri_cost / cat_exp_loss_usd if cat_exp_loss_usd else 0

        # Conv back to policy currency
        technical_prem = max(technical_prem_usd, technical_prem_minimum) * exchange_rate

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Allocate tech premium by peril
        # NOTE already in policy currency given conversion above 

        # All perils
        for peril in all_perils:
            el = getattr(el_obj, peril) or 0
            peril_tech_prem = el / total_exp_loss * technical_prem if total_exp_loss else 0
            setattr(tech_obj, peril, peril_tech_prem)        
        
        nmp_tech_prem = (nmp_load - 1) / nmp_load * technical_prem
        
        # Write to hxd and conv back to policy currency
        cp = layer.case_pricing

        cp.nmp_premium = nmp_tech_prem
        cp.tp_breakdown.ind_exp = ind_expenses * exchange_rate
        cp.tp_breakdown.dir_exp = tp_dir_exp * exchange_rate
        cp.tp_breakdown.coc = (tp_cat_coc + tp_att_coc) * exchange_rate
        cp.tp_breakdown.sd_loading = total_exp_loss * sd * cov
        cp.tp_breakdown.inv_ret = tp_inv_ret * exchange_rate
        cp.tp_breakdown.lae = tp_lae * exchange_rate

        

            





    






