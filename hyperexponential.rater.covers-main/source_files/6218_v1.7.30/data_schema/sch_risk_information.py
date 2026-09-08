import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from data_schema.sch_show_hide_and_dropdown import coverage_list, follow_lead_list, business_type_list, yes_no_list, country_list, uw_list


def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id"                       : hx.Int(mode="output",                                                                                                                                                     view={"label": "Database ID", "format": integer_format(0)}),
        "application_date"                  : hx.Date(mode="input", default="2000-01-01",                                                                                                                               view={"label": "Application Date"}),
        "dropdown"                          : hx.List(mode = "input",                                      async_input=["bi_intelligence_fetch_binders_task"] , async_output=["bi_intelligence_fetch_binders_task"],    children={
            "insured_party"                 : hx.Str(mode="input",   default=None, optionality="optional", async_input=["bi_intelligence_fetch_binders_task"] , async_output=["bi_intelligence_fetch_binders_task"]),
            "binder_ref"                    : hx.Str(mode="input",   default=None, optionality="optional", async_input=["bi_intelligence_fetch_binders_task"] , async_output=["bi_intelligence_fetch_binders_task"])}),
        "insured_name_dropdown"             : hx.Str(mode="input",   default=None, optionality="optional", options_data = "../dropdown", options_field = "insured_party",                                               view={"label": "Insured Name"}),
        "binder_dropdown"                   : hx.Str(mode="input",   default=None, optionality="optional", options_data = "../dropdown", options_field = "binder_ref",                                                  view={"label": "Binder Reference"}),
        "broker_contact"                    : hx.Str(mode="input",   default="",                                                                                                                                        view={"label": "Broker Contact"}),
        "source_currency"                   : hx.Str(mode="input",   default="",                                                                                                                                        view={"label": "Currency"}),
        })
    
    cds.override_node_properties('cds/standard_fields/underwriter'
        ,{  "allow_custom_value": True
            ,'options_table'    : "table_input_underwriters"
            ,'options_column'   : "underwriter"
            ,"async_input"      : ["start_renewal_task",  "generate_uw_doc_task"]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })


    cds.override_node_properties("cds/layers/status"
        ,{  "view"              : {"label": "Deal Status"}
            ,"default"          : "Rating" 
            ,"async_input"      : ["generate_uw_doc_task", "run_bordereau_rater_task", "bi_clm_and_mvmt_exc_triangles_fetch_task"]
            ,"async_output"     : ["start_renewal_task"]
            })


    cds.override_node_properties("cds/standard_fields/is_renewal"
        ,{  "view"               : {"label": "Renewal"}
            ,"async_output"      : [{"task": "bi_facility_fetch_task", "reset": False}
                                    ,"start_renewal_task"   ] 
            })
    
    cds.extend_node_rater_defined("cds/layers", {
        "quoted_premium_100pct"             : hx.Float(mode="input",  default=None,                            optionality="optional",   validation={"min_value": 0},                  view={"label": "EPI (GG 100%)", "options": {"rationale": {"read_only": True, "label": "Current Year EPI (GG 100%)"}}},       async_input=["bi_clm_and_mvmt_exc_triangles_fetch_task","run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"]), 
        "expiry_signed_line"                : hx.Float(mode="input",  default=0,                               optionality="optional",   validation={"min_value": 0, "max_value": 1},  view={"label": "Expiry signed Line", "format":percent_format(2)},   async_input=["pull_in_exposure_management_data_task", "run_bordereau_rater_task" , "simulate_pc_task"]),
        "follow_lead"                       : hx.Str(mode="input",    default="",    options=follow_lead_list,                                                                         view={"label": "Follow or Lead?"},                                  async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
        "commission"                        : hx.Float(mode="input",  default=0,                                optionality="optional",   validation={"min_value": 0, "max_value": 1}, view={"label": "Flat Commission (%)", "format":percent_format(2)},  async_input=["run_bordereau_rater_task", "simulate_pc_task"]),
        "ipt"                               : hx.Float(mode="input",  default=0,                                optionality="optional",   validation={"min_value": 0, "max_value": 1}, view={"label": "IPT (%)", "format":percent_format(2)}),        
        "total_deductions"                  : hx.Float(mode="output",                                                                                                                  view={"label": "Total Deductions (%)", "format":percent_format(2)}, async_input=["bi_clm_and_mvmt_exc_triangles_fetch_task","run_bordereau_rater_task" , "simulate_pc_task", "generate_uw_rationale_doc_task"]),
        "country"                           : hx.Str(mode="input",    default="US",  options=country_list,      optionality="optional",                                                view={"label": "Country"},                                          async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
        "standard_non_standard"             : hx.Str(mode="input",    default="No",  options=yes_no_list,       optionality="optional",                                                view={"label": "Non-Standard", "info": "Use for Known Excess accounts and deductible buydowns"}, async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
        "HO6_coverage"                      : hx.Str(mode="input",    default=None, options=yes_no_list,       optionality="optional",                                                view={"label": "Is Coverage Type HO6"},                             async_input=["pull_in_exposure_management_data_task"]),
        "extra_expense_coverage"            : hx.Str(mode="input",    default="Yes", options=yes_no_list,       optionality="optional",                                                view={"label": "Extra Expense Cover"},                              async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
        "signed_line"                       : hx.Float(mode="input",  default=0,                                optionality="optional",   validation={"min_value": 0, "max_value": 1}, view={"label": "Signed Line", "format":percent_format(2)}),        
    })

    cds.extend_node_rater_defined("cds", {
        "risk_info": hx.Structure(children={
            "coverage"                          : hx.Str(mode="input", default="Special", options=coverage_list, view={"label": "Coverage"},                         async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "fire"                              : hx.Bool(mode="override",                                       view={"label": "Fire"},                             async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "explosion"                         : hx.Bool(mode="override",                                       view={"label": "Explosion"},                        async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "vandalism_and_malicious_mischief"  : hx.Bool(mode="override",                                       view={"label": "Vandalism & Malicious Mischief"},   async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "sprinkler_leakage"                 : hx.Bool(mode="override",                                       view={"label": "Sprinkler Leakage"},                async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "mold_due_to_bg_1_perils"           : hx.Bool(mode="override",                                       view={"label": "Mold due to BG I Perils"},          async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "mold_due_to_bg_2_perils"           : hx.Bool(mode="override",                                       view={"label": "Mold due to BG II Perils"},         async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "mold_due_to_scl_perils"            : hx.Bool(mode="override",                                       view={"label": "Mold due to SCL Perils"},           async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "tn"                                : hx.Bool(mode="override",                                       view={"label": "Tornado"},                          async_input=["run_bordereau_rater_task" , "simulate_pc_task"]), # This is Wind in the CMT but is referencing TN 
            "ha"                                : hx.Bool(mode="override",                                       view={"label": "Hail"},                             async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "wf"                                : hx.Bool(mode="override",                                       view={"label": "Wildfire"},                         async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "wts"                               : hx.Bool(mode="override",                                       view={"label": "Winter Storm"},                     async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "fl"                                : hx.Bool(mode="override",                                       view={"label": "Flood"},                            async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "riot_or_civil_commotion"           : hx.Bool(mode="override",                                       view={"label": "Riot or Civil Commotion"},          async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "theft"                             : hx.Bool(mode="override",                                       view={"label": "Theft"},                            async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "water_damage"                      : hx.Bool(mode="override",                                       view={"label": "Water Damage"},                     async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "all_other_causes"                  : hx.Bool(mode="override",                                       view={"label": "All Other Causes"},                 async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "freezing"                          : hx.Bool(mode="override",                                       view={"label": "Freezing"},                         async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "collapse_due_to_weight_of_ice_etc" : hx.Bool(mode="override",                                       view={"label": "Collapse due to wt. of Ice etc."},  async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),
            "collapse_due_to_other_causes"      : hx.Bool(mode="override",                                       view={"label": "Collapse due to Other Causes"},     async_input=["run_bordereau_rater_task" , "simulate_pc_task"]),

            #### From BBT ####
            # "application_date"               : hx.Date(mode="input",default=None, optionality="optional", view={"label": "Application Date"}),
            "new_insured"                      : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "New/Replacement"}),
            "facility_reference2"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 2"},                         async_input=["bi_facility_fetch_task"]),
            "facility_reference3"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 3"},                         async_input=["bi_facility_fetch_task"]),
            "facility_reference4"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 4"},                         async_input=["bi_facility_fetch_task"]),
            "facility_reference5"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 5"},                         async_input=["bi_facility_fetch_task"]),
            "facility_reference6"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 6"},                         async_input=["bi_facility_fetch_task"]),
            "facility_reference7"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Facility Reference 7"},                         async_input=["bi_facility_fetch_task"]),
            "department"                       : hx.Str(mode="output",                                        view={"label": "Department"}),
            "division"                         : hx.Str(mode="output",                                        view={"label": "Division"}),
            "trifocus_valid"                   : hx.Bool(mode="output",                                       view={"label": "Is Trifocus Valid:"}),
            "proxy_trifocus"                   : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Override or Proxy Trifocus"},  options_table="table_tfgmappings", options_column="Trifocus"),
            "business_plan_mi_group"           : hx.Str(mode="output",                                        view={"label": "Benchmark Planning MI Name"}),
            "ibnr_group"                       : hx.Str(mode="output",                                        view={"label": "IBNR Group"}),
            "st_or_lt"                         : hx.Str(mode="output",                                        view={"label": "Short-tailed or Long-tailed"}), ### not currently exposed to user but uused through model
            # "trifocus_previous"              : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Trifocus Previous"},           options_table="tb_tfgmappings", options_column="Trifocus"),
            # "ibnr_group_previous"            : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "IBNR Group Previous"},         options_table="lst_ibnrgroup", options_column="Reserving Class"),
            "sov_available"                    : hx.Str(mode="input",   default="No",                         view={"label": "SOV Available?"},                   options=yes_no_list),
            "new_to_market"                    : hx.Str(mode="input",   default="No",                         view={"label": "New to Market"},                    options=yes_no_list),
            "rms_modelling_available"          : hx.Str(mode="input",   default="No",                         view={"label": "Show RMS Analysis"},                options=yes_no_list),
            "pc_modelling_required"            : hx.Str(mode="input",   default="No",                         view={"label": "Show Profit Commission Analysis"},  options=yes_no_list),
            "case_priced"                      : hx.Str(mode="input",   default="No",                         view={"label": "Case Priced?"},                     options=yes_no_list),
            "tri_modelling_required"           : hx.Str(mode="input",   default="No",                         view={"label": "Show Triangle Analysis"},           options=yes_no_list),
            "srcc_coverage_given_indicator"    : hx.Str(mode="input",   default="No",                         view={"label": "Is SRCC Coverage given?"},          options=yes_no_list),
            "srcc_fully_excluded_indicator"    : hx.Str(mode="input",   default="No",                         view={"label": "Is SRCC fully excluded?"},          options=yes_no_list),
            "srcc_sublimit_indicator"          : hx.Str(mode="input",   default="No",                         view={"label": "Is SRCC sub-limitted"},             options=yes_no_list),
            "srcc_sublimit"                    : hx.Float(mode="input", default=None, optionality="optional", view={"label": "SRCC sub-limit"},   validation={"min_value": 0}),
            "rms_data_asat"                    : hx.Date(mode="input",  default=None, optionality="optional", view={"label": "RMS Data As At"}),
            "broker_contact"                   : hx.Str(mode="input",   default=None, optionality="optional", view={"label": "Broker Contact"}),
            "final_data_asat"                  : hx.Date(mode="output",                                       view={"label": "Final Data As At"}),
            "bic_data_asat"                    : hx.Date(mode="input",  default=None, optionality="optional", view={"label": "BIC Data As At"},                              async_input=["tri_exclusions_setup_task"], async_output=["bi_clm_and_mvmt_inc_triangles_fetch_task", "bi_clm_and_mvmt_exc_triangles_fetch_task"]),
        })
    })
   
