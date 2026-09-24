# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):

    product_lst=["Event Cancellation", "Non-Appearance"]

    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id":                 hx.Int(mode="output",                                       view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact":                   hx.Str(mode="input",                         default="",    view={"label": "Broker Contact"}),
        "case_pricing_analysis_location":   hx.Str(mode="input", optionality="optional", default=None,  view={"label": "Case Pricing Analysis Filepath"}),
        # ~~~~~
        # Model Specifc
        "risk_info"  : hx.Structure(children={
            "product":                   hx.Str( mode="output",                                                           view={"label": "Product"}),
            "product_bool":              hx.Bool(mode="input",   optionality="required", default=False,                   view={"label": "Include Non-Appearance:"}, async_input=['rarc_task']),
            "event_name":                hx.Str( mode="input",                           default="",                      view={"label": "Event Name"}),
        }),

        # relating to the task to use sql to load from Beazley Intelligence
        "bi"  : hx.Structure(view={"label": "BI Data Load"},children={
            "last_run_status"           : hx.Str( mode="output", async_output=[{"task": "task_sql_bi_data", "reset": False}], view={"label": "Status - Last load"}),
            "last_run_date"             : hx.Str( mode="output", async_output=[{"task": "task_sql_bi_data", "reset": False}], view={"label": "Date - Last load"}),
            "last_run_value"            : hx.Str( mode="output", async_output=[{"task": "task_sql_bi_data", "reset": False}], view={"label": "Check Value - Last load of BI Data"}),
            "calc_run_value"            : hx.Str( mode="output",                                                              view={"label": "Check Value - Calculated"}),
            "check_run_consistent"      : hx.Str( mode="output",                                                              view={"label": "Reload Data?"}),
        })

    })

    cds.override_node_properties("hx_core/expiry_date",    { "async_input":['rarc_task'], "async_output"      : [{"task": "task_start_renewal", "reset": False}] })
    cds.override_node_properties("hx_core/inception_date", { "async_input":['rarc_task'], "async_output"      : [{"task": "task_start_renewal", "reset": False}] })
    cds.override_node_properties("cds/layers/brokerage",                     { "async_input":['rarc_task']})
    cds.override_node_properties("cds/standard_fields/rating_methodology",   { "async_input":['rarc_task']})
    cds.override_node_properties("cds/layers/bpi_case_priced",               { "async_input":['rarc_task']})
