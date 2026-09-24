# v0.5.0
import hx
from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages



def model_state(hxd):

    ms = hxd.model_state
    
    ms.live_hxd = False if "transient_hxd" in str(type(hxd)) else True

    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # expiring_policy_option_id = 56654 # For debugging in dev mode
    # save the record global variable in the snapshot for governance
    ms.coverage_use = RARC_COVERAGE_USE # Edit v0.3.0
    ms.insured_asset_use = RARC_INSURED_ASSET_USE # Edit v0.3.0
    # Controls which page to show and hide when the start renewal button is pressed
    # Only displays the landing page for policies which are a renewal
    if (expiring_policy_option_id is None) or (ms.pressed_start_renewal_task) or (ms.expiring_policy_option_id == expiring_policy_option_id):
        ms.show_landing_page = False
        ms.show_after_landing_page = True
        # NOTE USE the below for 
        # ms.show_rate_change = True

        ms.show_rate_change_layer_no_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_layer_ia_use = hxd.cds.standard_fields.is_renewal and not RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_no_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and not RARC_INSURED_ASSET_USE
        ms.show_rate_change_coverage_ia_use = hxd.cds.standard_fields.is_renewal and RARC_COVERAGE_USE and RARC_INSURED_ASSET_USE

    else:
        ms.show_landing_page = True
        ms.show_after_landing_page = False

        ms.show_rate_change = False
        
        ms.show_rate_change_layer_no_ia_use = False
        ms.show_rate_change_layer_ia_use = False
        ms.show_rate_change_coverage_no_ia_use = False
        ms.show_rate_change_coverage_ia_use = False


    # show/hide underwriting adjustments
    ms.show_rs_before_uw_adj = ms.show_actuarial
    ms.show_underwriter      = not ms.show_actuarial


    ## plan rates
    # Plan rates shown
    ms.show_rs_not_cvg_not_before_uw_adj = (ms.show_rs_cvg==False) and (ms.show_rs_plan==True)
    ms.show_rs_yes_cvg_not_before_uw_adj = (ms.show_rs_cvg       ) and (ms.show_rs_plan==True)
    ms.show_rs_not_cvg_yes_before_uw_adj = (ms.show_rs_cvg==False) and (ms.show_rs_before_uw_adj) and (ms.show_rs_plan==True)
    ms.show_rs_yes_cvg_yes_before_uw_adj = (ms.show_rs_cvg       ) and (ms.show_rs_before_uw_adj) and (ms.show_rs_plan==True)
    # Plan rates hidden
    ms.show_rs_not_cvg_not_before_uw_adj_not_plan = (ms.show_rs_cvg==False) and (ms.show_rs_plan==False)
    ms.show_rs_yes_cvg_not_before_uw_adj_not_plan = (ms.show_rs_cvg       ) and (ms.show_rs_plan==False)
    ms.show_rs_not_cvg_yes_before_uw_adj_not_plan = (ms.show_rs_cvg==False) and (ms.show_rs_before_uw_adj) and (ms.show_rs_plan==False)
    ms.show_rs_yes_cvg_yes_before_uw_adj_not_plan = (ms.show_rs_cvg       ) and (ms.show_rs_before_uw_adj) and (ms.show_rs_plan==False)


    # show hide EC / NA
    ms.show_event_cancellation  = (hxd.cds.risk_info.product_bool == False) and ms.show_after_landing_page 
    ms.show_non_appearance      = (hxd.cds.risk_info.product_bool == True ) and ms.show_after_landing_page 


    # show hide additional rating on national mourning
    ms.show_ec_terrorism        = (hxd.cds.exposure.granular.event_cancel.base_coverages.terrorism.covered)
    ms.show_ec_national_mourning= (hxd.cds.exposure.granular.event_cancel.base_coverages.national_mourning.covered
                                    and ms.use_nm_app_old_model == False
                                    and ms.show_after_landing_page          )


    # show hide excess/deductible
    ms.show_ec_excess           = hxd.cds.layers[0].coverages.ec_total.excess_use
    ms.show_ec_deductible       = ms.show_ec_excess==False

    # For layers not used in the pricing summary, the rate change and KPI Summary is hidden
    layers = hxd.cds.layers
    num_layers = len(layers)
    for layer_index in range(1,max_layers+1):
        if layer_index <= num_layers: 
            setattr(hxd.cds.rate_change, f"show_layer_{layer_index}", True)
    
    if RARC_COVERAGE_USE: # EDIT v0.3.0
        num_coverages = len(coverages_dict)
        for cvg_index in range(1,max_coverages):
            if cvg_index <= num_coverages:
                setattr(hxd.cds.rate_change, f"show_coverage_{cvg_index}", True)

    # set the shown_by value # Edit # v0.5.0
    ms.layer_no_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == False)
    ms.layer_ia_use = (RARC_COVERAGE_USE==False and RARC_INSURED_ASSET_USE == True)
    ms.coverage_no_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == False)
    ms.coverage_ia_use = (RARC_COVERAGE_USE==True and RARC_INSURED_ASSET_USE == True)

    
    # Set bug report message (update rater name below, use dash for space)
    hxd.bug_report_email = """Please use the following email to report a bug or issue with the model and the support team will get back to you shortly.
    Please include the model name, a brief description of the issue, and the website link to the policy the issue relates to. 
    
    [RatingTeamDev@beazley](mailto:RatingTeamDev@beazley.com?subject=RATERNAME-Rater)"""
    return





def model_state_after(hxd):
    ## show hide ihs or simulation
    # paths
    ms  = hxd.model_state
    cds = hxd.cds
    sf  = hxd.cds.standard_fields
    ec  = hxd.cds.layers[0].coverages.ec_total
    sim = hxd.cds.exposure.granular.event_cancel.simulation
    ihs = hxd.cds.ihs
    cvg = hxd.cds.exposure.granular.event_cancel.base_coverages

    # show simulation
    ms.run_simulation           = ((  sim.check_run_consistent != "Simulation remains valid") and       # if needs running
                                   (( ec.aggregate_limit is not None) or                                # AND agg limit in play
                                    ((ec.aggregate_deductible is not None) and (not ec.excess_use))))   # OR agg ded in play
    ms.show_simulation          = (    ms.show_actuarial or ms.run_simulation)
    
    # show ihs
    ms.run_ihs                  = ((   ihs.check_run_consistent != "IHS Data Remains Valid") and       # if needs running
                                   (   cvg.terrorism.covered                 or                        # AND  if one of ihs cvg in play
                                       cvg.riots_and_civil_commotion.covered or                        # ...
                                       cvg.strike.covered                    or                        # ...
                                       cvg.war.covered  ))
    ms.show_ihs                 = (     ms.show_actuarial or   ms.run_ihs)

    # show settings
    ms.show_ihs_sim_settings    = ms.show_ihs or ms.show_simulation

    ## pages show
    ms.show_page_risk_info          =  ms.show_after_landing_page
    ms.show_page_exposure           =  ms.show_after_landing_page and sf.is_rater_priced 
    ms.show_page_national_mourning  =  ms.show_after_landing_page and sf.is_rater_priced and cvg.national_mourning.covered and (not ms.use_nm_app_old_model)
    ms.show_page_non_appearance     =  ms.show_after_landing_page and sf.is_rater_priced and cds.risk_info.product_bool
    ms.show_page_experience         =  ms.show_after_landing_page and sf.is_rater_priced 
    ms.show_page_actuarial          =  ms.show_after_landing_page and ms.show_actuarial
    ms.show_page_kpi_case           =  ms.show_after_landing_page and sf.is_case_priced
    ms.show_page_kpi                =  ms.show_after_landing_page and sf.is_rater_priced
    ms.show_page_rat_sum_case       =  ms.show_after_landing_page and sf.is_case_priced
    ms.show_page_rat_sum            = (ms.show_after_landing_page and sf.is_rater_priced and (   ms.show_actuarial or
                                                                                               ((not ms.run_ihs) and (not ms.run_simulation)))) 

    return


def allow_policy_doc_download(hxd):
    layer = hxd.cds.layers[0]
    doc = hxd.policy_doc
        
    tp = layer.technical_premium_100 or 0
    bp = layer.benchmark_premium_100 or 0
    qp = layer.quoted_premium_100 or 0
    
    if bp <= 0:
        doc.premium_check = f"Benchmark Premium has not been calculated. Please fill in the relevant fields in to calculate premium."
        doc.show_premium_check = True
    elif tp <= 0:
        doc.premium_check = "Benchmark Premium has not been fully calculated. Please check the validation errors at the bottom right corner."
        doc.show_premium_check = True
    elif qp <= 0:
        doc.premium_check = "Quoted Premium should be greater than 0. Please input a valid number in Rating Summary."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True
            