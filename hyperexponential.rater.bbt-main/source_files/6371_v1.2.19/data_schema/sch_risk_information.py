##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################
### Note for the standard CDS fields it is necessary to include the async tasks here - all others are stored on sch_async_overrides
##############################################################################################################################


import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),

    })

    cds.extend_node_rater_defined("cds", {
        "risk_info": hx.Structure(children={
            "application_date"              : hx.Date(mode="input",default=None, optionality="optional", view={"label": "Application Date"}),
            "new_insured"                   : hx.Str(mode="input", default=None, optionality="optional", view={"label": "New/Replacement"}),
            "facility_reference2"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 2"}),
            "facility_reference3"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 3"}),
            "facility_reference4"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 4"}),
            "facility_reference5"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 5"}),
            "facility_reference6"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 6"}),
            "facility_reference7"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Facility Reference 7"}),
            "department"                    : hx.Str(mode="output",                                      view={"label": "Department"}),
            "division"                      : hx.Str(mode="output",                                      view={"label": "Division"}),
            "trifocus_valid"                : hx.Bool(mode="output",                                     view={"label": "Is Trifocus Valid:"}),
            "proxy_trifocus"                : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Override or Proxy Trifocus"},  options_table="tb_tfgmappings", options_column="Trifocus"),
            "business_plan_mi_group"        : hx.Str(mode="output",                                      view={"label": "Benchmark Planning MI Name"}),
            "ibnr_group"                    : hx.Str(mode="output",                                      view={"label": "IBNR Group"}),
            "st_or_lt"                      : hx.Str(mode="output",                                      view={"label": "Short-tailed or Long-tailed"}), ### not currently exposed to user but uused through model
            "trifocus_previous"             : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Trifocus Previous"},           options_table="tb_tfgmappings", options_column="Trifocus"),
            "ibnr_group_previous"           : hx.Str(mode="input", default=None, optionality="optional", view={"label": "IBNR Group Previous"},         options_table="lst_ibnrgroup", options_column="Reserving Class"),
            "new_to_market"                 : hx.Str(mode="input", default="No",                         view={"label": "New to Market"},               options_table="lst_yn", options_column="YesNo"),
            "rms_modelling_available"       : hx.Str(mode="input", default="No",                         view={"label": "Show RMS Analysis"},           options_table="lst_yn", options_column="YesNo"),
            "pc_modelling_required"         : hx.Str(mode="input", default="No",                         view={"label": "Show Profit Commission Analysis"},  options_table="lst_yn", options_column="YesNo"),
            "tri_modelling_required"        : hx.Str(mode="input", default="No",                         view={"label": "Show Triangle Analysis"},      options_table="lst_yn", options_column="YesNo"),
            "srcc_coverage_given_indicator" : hx.Str(mode="input", default="No",                         view={"label": "Is SRCC Coverage given?"},     options_table="lst_yn", options_column="YesNo"),
            "srcc_fully_excluded_indicator" : hx.Str(mode="input", default="No",                         view={"label": "Is SRCC fully excluded?"},     options_table="lst_yn", options_column="YesNo"),
            "srcc_sublimit_indicator"       : hx.Str(mode="input", default="No",                         view={"label": "Is SRCC sub-limitted"},        options_table="lst_yn", options_column="YesNo"),
            "srcc_sublimit"                 : hx.Float(mode="input",default=None,optionality="optional", view={"label": "SRCC sub-limit"},   validation={"min_value": 0}),
            "rms_data_asat"                 : hx.Date(mode="input",default=None, optionality="optional", view={"label": "RMS Data As At"}),
            "broker_contact"                : hx.Str(mode="input", default=None, optionality="optional", view={"label": "Broker Contact"}),
            "final_data_asat"               : hx.Date(mode="output",                                     view={"label": "Final Data As At"}),
            "bic_data_asat"                 : hx.Date(mode="input",default=None, optionality="optional", view={"label": "BIC Data As At"}),
        })
    })
   
    cds.extend_node_rater_defined("cds/layers", {
            "quoted_premium_100pct"     : hx.Float(mode="input",    default=None, optionality="optional",   view={"label": "EPI (GG 100%)"}                                    , validation={"min_value": 0}),
            "commission"                : hx.Float(mode="input",    default=None, optionality="optional",   view={"label": "Flat Commission (%)",   "format":percent_format(2)}, validation={"min_value": 0, "max_value": 1}),
            "ipt"                       : hx.Float(mode="input",    default=None, optionality="optional",   view={"label": "IPT (%)",               "format":percent_format(2)}, validation={"min_value": 0, "max_value": 1}),
            "total_deductions"          : hx.Float(mode="output",                                           view={"label": "Total Deductions (%)",  "format":percent_format(2)}),
    })



    
    cds.override_node_properties('cds/layers/written_line'
        ,{  "view"              : {"label": "AFB Signed Line (%)",          "format":percent_format(2)}
            ,"async_input"      : ["generate_uw_doc_task"]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            ,"validation"       : {"min_value": 0, "max_value": 1}
            })
   
    cds.override_node_properties('cds/standard_fields/underwriter'
        ,{  "allow_custom_value": True
            ,'options_table'    : "table_input_underwriters"
            ,'options_column'   : "underwriter"
            ,"async_input"      : ["start_renewal_task",  "generate_uw_doc_task"]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })
    
    cds.override_node_properties('cds/currencies/source_currency'
        ,{  'default'           : "USD" 
            ,"view"             : {"label": "Settlement Currency"}
            ,"async_input"      : ["bi_clm_and_mvmt_inc_triangles_fetch_task",      "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                   ,"generate_uw_doc_task" ]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })


    cds.extend_node_items("cds/layers/coverages"
        ,{  "all"               : {"label": "All"}
            })

    cds.override_node_properties("cds/layers/status"
        ,{  "view"              : {"label": "Deal Status"}
            ,"default"          : "Rating" 
            ,"async_input"      : ["generate_uw_doc_task"]
            ,"async_output"     : ["start_renewal_task"]
            })

    cds.override_node_properties("cds/standard_fields/insured_name"
        ,{  "view"              : {"label": "Binder Name"}
            ,"allow_custom_value": True
            ,"options_table"    : "lst_insurednames"
            ,"options_column"   : "Description"
            ,"async_input"      : ["generate_uw_doc_task"]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })

    cds.override_node_properties("cds/standard_fields/facility_reference"
        ,{  "view"              : {"label": "Master Binder Reference"}
            ,"async_input"      : ["edm_fetch_task",    "bi_facility_fetch_task",    "generate_uw_doc_task"]
            })

    cds.override_node_properties("cds/layers/quoted_premium"
        ,{  "view"              : {"label": "AFB EPI (Net of Aqn, Gross of PC)"}
            ,"mode"             : "output"
            ,"validation"       : {"min_value": 0}
            })


    cds.override_node_properties("cds/standard_fields/is_renewal"
        ,{  "view"               : {"label": "Renewal"}
            ,"async_output"      : [{"task": "bi_facility_fetch_task", "reset": False}
                                    ,"start_renewal_task"   ] 
            })

    cds.override_node_properties("cds/standard_fields/trifocus"
        ,{  "view"              : {"label": "TriFocus"}
            ,"allow_custom_value": True
            ,"options_table"    : "tb_tfgmappings"
            ,"options_column"   : "Trifocus"
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })

    cds.override_node_properties("cds/standard_fields/broker"
        ,{  "allow_custom_value": True
            ,"options_table"    : "lst_brokers"
            ,"options_column"   : "Broker Name"
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })

    cds.override_node_properties("cds/standard_fields/benchmark_class"
        ,{  "mode"              : "output"
            ,"async_input"      : ["bi_clm_and_mvmt_inc_triangles_fetch_task",      "bi_clm_and_mvmt_exc_triangles_fetch_task"]
            })

    cds.override_node_properties("cds/layers/brokerage"
        ,{  "view"              : {"label": "Brokerage (%)",     "format"   : percent_format(2)}
            ,"validation"       : {"min_value": 0, "max_value": 1}
            })

    cds.override_node_properties("hx_core/expiry_date"
        ,{    "async_input"       : ["generate_uw_doc_task"]
            , "async_output"      : [{"task": "bi_facility_fetch_task", "reset": False}]
            })

    cds.override_node_properties("hx_core/inception_date"
        ,{  "async_input"       : ["bi_clm_and_mvmt_inc_triangles_fetch_task",      "bi_clm_and_mvmt_exc_triangles_fetch_task"
                                    ,"tri_exclusions_setup_task"             ,      "tri_override_setup_task"
                                    ,   "generate_uw_doc_task"   ]
            ,"async_output"     : [{"task": "bi_facility_fetch_task", "reset": False}]
            })
