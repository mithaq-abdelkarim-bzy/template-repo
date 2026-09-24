# v0.5.0
import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict , max_coverages

def sch_model_state():
    '''
    Internal Model State that controls the workflow
    '''
    return {
        "model_state": hx.Structure(children={
            "pressed_start_renewal_task": hx.Bool(mode="output", async_output=["task_start_renewal"]),
            "show_landing_page": hx.Bool(mode="output"),
            "show_after_landing_page": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "landing_page_info": hx.Str(
                mode="input",
                default="Click the 'import expiring policy data' arrow in the top right corner then click **Start Policy**. ",
                async_output=["task_start_renewal"],
                view={"read_only":True}
            ),
            "expiring_policy_option_id": hx.Int(mode="input", default=None, optionality="optional", async_output=["task_start_renewal", "sync_expiring_ids"]),

            "live_hxd":  hx.Bool(mode="output",                  async_input =  ['task_simulation'], view={"label": "hxd live = True; hxd transient= False"}   ),

            "coverage_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            "insured_asset_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. Required for governance # Edit v0.3.0
            
            "show_rate_change_layer_no_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_layer_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_coverage_no_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0
            "show_rate_change_coverage_ia_use": hx.Bool(mode="output"), # NOTE: Can be removed for the case unused Edit v0.3.0

            "layer_no_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "layer_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "coverage_no_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
            "coverage_ia_use": hx.Bool(mode="output"), # NOTE: related to the premium calculation. ShownBy for skeleton. Can be remove for the case unused # Edit v0.3.0
      
            # enable old national mourning approach
            "use_nm_app_old_model" : hx.Bool(mode="input", default=False, optionality="required", view={"label": "Use National Mourning Approach (old excel model)"}, async_input=['rarc_task'], async_output=["task_start_renewal"]), 

            # enable old model deterministic agg limit/ded approach
            "use_determ_agg_calc"  : hx.Bool(mode="input", default=False, optionality="required", view={"label": "Run Deterministic Agg Approach (old excel model)"}, async_input=['rarc_task'], async_output=["task_start_renewal"]), 

            "is_migrated"       : hx.Bool(mode="input", default=False, optionality="required", view={"label": "Is Migrated"},        async_output=["task_start_renewal"]),    
            "disable_validation": hx.Bool(mode="input", default=False, optionality="required", view={"label": "Disable Validation"}, async_output=["task_start_renewal"]),    


            # EC NA CUSTOMISATION BELOW
            "show_rs_cvg"                       : hx.Bool(mode="input",  view={"label": "Coverage Level Analysis"},             default=False),         
            "show_rs_before_uw_adj"             : hx.Bool(mode="output", view={"label": "Show Values Before UW Adjustment"}                  ),
            "show_rs_plan"                      : hx.Bool(mode="input",  view={"label": "Show plan rates"},                     default=False),
            "show_actuarial"                    : hx.Bool(mode="input",  view={"label": "Show Actuarial View"},                 default=False),
            "show_underwriter"                  : hx.Bool(mode="output", view={"label": "Show Underwriter View"},                            ),
            "show_exposure_curve_warning"       : hx.Bool(mode="output", view={"label": "Show Exposure Curve Warning"}                       ),
            "show_tiv_warning"                  : hx.Bool(mode="output", view={"label": "Show TIV Warning"}                                  ),
            "show_ec_excess"                    : hx.Bool(mode="output", view={"label": "Show Excess"}                                       ),
            "show_ec_deductible"                : hx.Bool(mode="output", view={"label": "Show Deductible"}                                   ),


            # Plan rates shown
            "show_rs_not_cvg_not_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_not_before_uw_adj"}),
            "show_rs_yes_cvg_not_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_not_before_uw_adj"}),
            "show_rs_not_cvg_yes_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_yes_before_uw_adj"}),
            "show_rs_yes_cvg_yes_before_uw_adj" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_yes_before_uw_adj"}),
            # Plan rates hidden
            "show_rs_not_cvg_not_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_not_before_uw_adj_not_plan"}),
            "show_rs_yes_cvg_not_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_not_before_uw_adj_not_plan"}),
            "show_rs_not_cvg_yes_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_not_cvg_yes_before_uw_adj_not_plan"}),
            "show_rs_yes_cvg_yes_before_uw_adj_not_plan" : hx.Bool(mode="output", view={"label": "show_rs_yes_cvg_yes_before_uw_adj_not_plan"}),      
      

            "show_non_appearance"       : hx.Bool(mode="output", view={"label": "show_non_appearance"}),         
            "show_event_cancellation"   : hx.Bool(mode="output", view={"label": "show_event_cancellation"}),  
            "show_ec_terrorism"         : hx.Bool(mode="output", view={"label": "show_ec_terrorism"}),  
            "show_ec_national_mourning" : hx.Bool(mode="output", view={"label": "show_ec_national_mourning"}),  
            
            # ihs sim
            "run_simulation"            : hx.Bool(mode="output", view={"label": "run_simulation"}),  
            "show_simulation"           : hx.Bool(mode="output", view={"label": "show_simulation"}),  
            "run_ihs"                   : hx.Bool(mode="output", view={"label": "run_ihs"}),  
            "show_ihs"                  : hx.Bool(mode="output", view={"label": "show_ihs"}),  
            "show_ihs_sim_settings"     : hx.Bool(mode="output", view={"label": "show_ihs_sim_settings"}),  


            # show pages
            "show_page_risk_info"           : hx.Bool(mode="output", view={"label": "show_page_risk_info"}),  
            "show_page_exposure"            : hx.Bool(mode="output", view={"label": "show_page_exposure"}),  
            "show_page_national_mourning"   : hx.Bool(mode="output", view={"label": "show_page_national_mourning"}),  
            "show_page_non_appearance"      : hx.Bool(mode="output", view={"label": "show_page_non_appearance"}),  
            "show_page_experience"          : hx.Bool(mode="output", view={"label": "show_page_experience"}),  
            "show_page_actuarial"           : hx.Bool(mode="output", view={"label": "show_page_actuarial"}),  
            "show_page_rat_sum"             : hx.Bool(mode="output", view={"label": "show_page_rat_sum"}),  
            "show_page_rat_sum_case"        : hx.Bool(mode="output", view={"label": "show_page_rat_sum_case"}),  

            "show_page_kpi"                 : hx.Bool(mode="output", view={"label": "show_page_kpi"}),  
            "show_page_kpi_case"            : hx.Bool(mode="output", view={"label": "show_page_kpi_case"}),  

        }),
        "bug_report_email": hx.Str(mode="output"),

        "policy_doc": hx.Structure(children={
            "data_dict": hx.Str(mode="output", async_input=["policy_to_excel_task"]),
            "output_file": hx.File(mode="output", async_output=["policy_to_excel_task"], file_name="Policy_Summary.xlsx"),
            "task_data_dict": hx.Str(mode="output", async_output=["policy_to_excel_task"]),
            "show_generate_button": hx.Bool(mode="output"),
            "show_download": hx.Bool(mode="output"),
            "premium_check": hx.Str(mode="output"),
            "show_premium_check": hx.Bool(mode="output"),

        }),

    }