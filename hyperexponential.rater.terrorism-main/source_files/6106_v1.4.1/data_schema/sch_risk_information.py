import hx_data_schema as hx
from data_schema.sch_utilities import *
from algorithms.data_schema.sch_rater_defined import coverages_dict
import algorithms.rate_constants as c

def sch_risk_information(cds):

    cds.extend_node_rater_defined("cds", { 
        # If needed
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": integer_format(0)}),
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": integer_format(0)}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        "authority_ccy_label": hx.Str(mode="output"),
        "policy_ccy_label": hx.Str(mode="output"),
        # Additional policy info
        "policy_info": hx.Structure(children={
            "term"              : hx.Float(mode="output",                                               view={"label": "Term",                "format": {**thousands_format(5), "trimMantissa": True}},                  async_input=["rarc_task"]),
            "terrorism_only"    : hx.Float(mode="input",  default=1,                                    view={"label": "TO (Terrorism Only)", "format": percent_format(1)}, validation={"min_value": 0, "max_value": 1}, ),
            "war_on_land"       : hx.Float(mode="input",  default=0,                                    view={"label": "WL (War on Land)",    "format": percent_format(1)}, validation={"min_value": 0, "max_value": 1}, ),
            "application_date"  : hx.Date( mode="input",  default=None,         optionality="optional", view={"label": "Application Date"},                                                                              ),
            "broker_contact"    : hx.Str(  mode="input",  default="",                                   view={"label": "Broker Contact"},                                                                                ),
            "source_system"     : hx.Str(  mode="input",  default="Eurobase",   optionality="optional", view={"label": "Source System"},        options=["Eurobase", "BeazleyPro", "Unirisx", "Etrek"],                  ),
            "single_country_only" : hx.Bool(mode="input", default=False, view={"label": "Single Country Only"}),
        })

    })


    ######################################################################################################
    ### Override on standard fields                                                                    ###
    ######################################################################################################
    cds.override_node_properties("cds/standard_fields/underwriter"  , {   'options_table'       : 'Underwriters'
                                                                        , 'allow_custom_value'  : True
                                                                        , 'options_column'      : 'name'})

    
    cds.override_node_properties("cds/standard_fields/insured_name" , {   'options_table'       : 'lst_insured_names'
                                                                        , 'options_column'      : 'insured_name'
                                                                        , "async_input"         : ["start_renewal_task"]
                                                                        , 'allow_custom_value'  : True})

    cds.override_node_properties("cds/standard_fields/broker"       , {   'allow_custom_value'  : True
                                                                        , 'options_table'       : 'lst_broker_names'
                                                                        , 'options_column'      : 'broker_name'})

    cds.override_node_properties("cds/standard_fields/is_renewal"   , {   "async_output"        : ["start_renewal_task"]})

    # cds.override_node_properties("cds/standard_fields/rating_methodology",{"async_output"       : ["start_renewal_task"]})

    cds.override_node_properties('cds/layers/status'                 , {  "view"                : {'options'  : {'read_only': {'read_only': True}}}
                                                                        , "default"             : "Rating"
                                                                        , "async_output"        : ["start_renewal_task"]})

    cds.override_node_properties("cds/currencies/source_currency"   , {   "default"             : "USD"
                                                                        , "options"             : c.ccy_options
                                                                        , "async_input"         : ["rarc_task"]})
    
    cds.override_node_properties("cds/layers/brokerage"             , {   "optionality"         : "required"
                                                                        , "default"             : 0.25
                                                                        , "view"                : { "format" : percent_format(1)
                                                                                                   ,"options": {"read_only" : {"read_only"   : True}}}
                                                                        , "validation"          : {"min_value": 0, "max_value": 1}
                                                                        , "async_input"         : ["rarc_task"]})
    
    cds.override_node_properties("cds/layers/aggregate_limit"       , {   "async_input"         : ["rarc_task"]
                                                                        , "validation"          : {"min_value": 0}})

    cds.override_node_properties("cds/layers/aggregate_deductible"  , {   "async_input"         : ["rarc_task"]
                                                                        , "validation"          : {"min_value": 0}})

    cds.override_node_properties("cds/layers/written_line"          , {   "optionality"         : "required"
                                                                        , "default"             : 1
                                                                        , "view"                : { "format" : percent_format(1)
                                                                                                   ,"options": {"read_only" : {"read_only"   : True}}}
                                                                        , "validation"          : {"min_value": 0, "max_value": 1}
                                                                        , "async_input"         : ["rarc_task"]})

    cds.override_node_properties("cds/layers/pflr_pre_uw_adj",          { "view"                : {"format": percent_format(1)}}),

    cds.override_node_properties("cds/standard_fields/benchmark_class", { "mode"                : "output"})

    cds.override_node_properties('cds/layers/section_reference'     , {   'view'                : { 'label'  : 'Policy Section Reference'
                                                                                                   ,'options': {'read_only': {'read_only': True}}}
                                                                        , "async_input"         : [ "task_fetch_ihs_data", "task_confirm_limits"
                                                                                                   ,"task_policy_to_excel", "expiring_policy_fetch_task"
                                                                                                   , "rarc_task", "sync_expiring_ids"]
                                                                        , "async_output"        : [{"task": "start_renewal_task", "reset": False}]})      # notice non-resetting


    cds.override_node_properties("cds/standard_fields/policy_reference", {"mode"                : "output"})
    cds.override_node_properties("cds/standard_fields/trifocus"        , {"mode"                : "output"})

    cds.override_node_properties("cds/layers/limit"                    , {"mode"                : "output"})
    cds.override_node_properties("cds/layers/excess"                   , {"mode"                : "output"})
    cds.override_node_properties("cds/layers/deductible"               , {"mode"                : "output"})
    cds.override_node_properties("cds/layers/currency"                 , {"mode"                : "output"})
    cds.override_node_properties("cds/layers/trifocus"                 , {"mode"                : "output"})
    cds.override_node_properties('cds/layers/bpi_case_priced'          , {"view"              : {'label'  : 'BPI', 'options'  : {'read_only': {'read_only': True}}}})


    # cds.override_node_properties("cds/layers/currency", {
    #    "default": "USD", "options": c.ccy_options, "async_output": ["start_renewal_task"], "view": {"label": "Line (currency)"}
    # })



    ######################################################################################################
    ### Override on coverage fields                                                                    ###
    ######################################################################################################

    for cvg in coverages_dict.keys():
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/brokerage"    , {   "optionality"     : "required"
                                                                                    , "default"         : 0
                                                                                    , "view"            : {"format": percent_format(1)}
                                                                                    , "validation"      : {"min_value": 0, "max_value": 1}
                                                                                    , "async_input"     : ["rarc_task"]})

        cds.override_node_properties(f"cds/layers/coverages/{cvg}/written_line" , {   "optionality"     : "required"
                                                                                    , "default"         : 0
                                                                                    , "view"            : {"format": percent_format(1)}
                                                                                    , "validation"      : {"min_value": 0, "max_value": 1}
                                                                                    , "async_input"     : ["rarc_task"]})

        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium", {  "optionality"     : "required"
                                                                                    , "default"         : 0
                                                                                    , "validation"      : {"min_value": 0}
                                                                                    , "async_input"     : ["rarc_task"]})

        cds.override_node_properties(f"cds/layers/coverages/{cvg}/limit"        , {   "default"         : 0
                                                                                    , "optionality"     : "required"
                                                                                    , "validation"      : {"min_value": 0}
                                                                                    , "async_input"     : ["rarc_task"]})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/excess"       , {   "default"         : 0
                                                                                    , "optionality"     : "required"
                                                                                    , "validation"      : {"min_value": 0}
                                                                                    , "async_input"     : ["rarc_task"]})
