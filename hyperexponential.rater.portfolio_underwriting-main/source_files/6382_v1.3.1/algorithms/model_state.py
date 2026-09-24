import hx
from algorithms.rate_constants import max_layers

def model_state(hxd):
    '''
    Controls which page to show and hide when the start renewal button is pressed
    '''

    # Get pathways
    ms          = hxd.model_state
    sf          = hxd.cds.standard_fields
    ri          = hxd.cds.risk_information
    
    # get expiring id from metadata
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    
    # NOTE: This only displays the landing page for policies which are a renewal, to display the landing page always, then remove the first boolean
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False

    # Extract key flags
    is_alp              = ms.show_after_landing_page 
    is_bbt              = ri.follow_main_syndicate
    is_large_model_mode = ri.is_large_model_mode 
    is_premium          = ri.prem_data_available
    is_claim            = ri.det_claims_data_available
    is_actuarial        = ri.priced_by == "Actuarial"
    is_rater_priced     = sf.rating_methodology == "Rater"
    is_cat              = ri.cat_modelling_available
    is_refs             = ri.show_refs
    is_pc               = ri.is_profit_comission
    is_not_bbt          = is_bbt == False
    is_case_priced      = is_rater_priced == False


    # assign values - 
    # {this was previously done within a range of individual pages, but several new conditions needed to be added - hence centralised here
    ms.show_risk_information    = is_alp
    ms.show_risk_code_library   = is_alp and is_rater_priced and is_not_bbt
    ms.show_policy_data         = is_alp and is_rater_priced and is_not_bbt and is_premium
    ms.show_claim_data          = is_alp and is_rater_priced and is_not_bbt and is_claim
    ms.show_risk_code_comp      = is_alp and is_rater_priced and is_not_bbt
    ms.show_deductions          = is_alp and is_rater_priced and is_not_bbt
    ms.show_rate_change         = is_alp and is_rater_priced and is_not_bbt
    ms.show_inflation           = is_alp and is_rater_priced and is_not_bbt and is_actuarial and is_refs
    ms.show_premium_limit_prof  = is_alp and is_rater_priced and is_not_bbt
    ms.show_cat                 = is_alp and is_rater_priced and is_not_bbt and is_cat
    ms.show_portfolio_profile   = is_alp and is_rater_priced and is_not_bbt and is_refs
    ms.show_own_experience      = is_alp and is_rater_priced and is_not_bbt and is_premium
    ms.show_lloyds_proj         = is_alp and is_rater_priced and is_not_bbt and is_actuarial
    ms.show_beazley_proj        = is_alp and is_rater_priced and is_not_bbt and is_actuarial
    ms.show_bp_proj             = is_alp and is_rater_priced and is_not_bbt and is_actuarial
    ms.show_anti_select         = is_alp and is_rater_priced 
    ms.show_uncertainty         = is_alp and is_rater_priced 
    ms.show_pc                  = is_alp and is_rater_priced and is_not_bbt and is_pc
    ms.show_rat_sum_std         = is_alp and is_rater_priced and is_not_bbt
    ms.show_rat_sum_bbt         = is_alp and is_rater_priced and is_bbt
    ms.show_rat_sum_case        = is_alp and is_case_priced
    ms.show_kpi                 = is_alp 
    ms.show_rationale           = is_alp 
    ms.show_json_view           = is_alp and is_actuarial
    ms.show_timer               = True                                              # not used - done via library

    hxd.cds.policy_level_data_table.use_policy_level_data_ungrouped = not hxd.cds.policy_level_data_table.use_policy_level_data_grouped
    hxd.cds.claim_level_data_table.use_claim_level_data_ungrouped = not hxd.cds.claim_level_data_table.use_claim_level_data_grouped
    

               