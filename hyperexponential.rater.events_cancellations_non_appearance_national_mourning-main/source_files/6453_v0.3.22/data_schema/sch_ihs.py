#########################################################################################################
########################################### Outstanding Items ###########################################
#########################################################################################################
### 1) 
### 2) 
### 2) 
### 4) 
### 5) 
#########################################################################################################

import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_ihs(cds):
    cds.extend_node_rater_defined("cds", {

        "ihs"  : hx.Structure(children={

            "last_run_status"           : hx.Str( mode="output",                                       async_output=["task_fetch_ihs_data"], view={"label": "Status - Last load of IHS Data"}),
            "last_run_date"             : hx.Str( mode="output",                                       async_output=["task_fetch_ihs_data"], view={"label": "Date - Last load of IHS Data"}),
            "last_run_value"            : hx.Str( mode="output",                                       async_output=["task_fetch_ihs_data"], view={"label": "Check Value - Last load of IHS Data"}),
            "calc_run_value"            : hx.Str( mode="output",                                       async_input=["task_fetch_ihs_data"],  view={"label": "IHS data to be extracted"}),
            "check_run_consistent"      : hx.Str( mode="output",                                                                             view={"label": "Does data need to be reloaded:"}),
            "internal_error_msg"        : hx.Str( mode="input",  default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Internal Error Message"}),

            # listing of ihs history
            "ihs_detail": hx.List(mode="input", async_output=["task_fetch_ihs_data"], children={
                "country_code"          : hx.Str(  mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Country Code"}),
                "risk_name"             : hx.Str(  mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Risk Name"}),
                "updated_on"            : hx.Date( mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Updated Date"}),
                "value"                 : hx.Float(mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Value",          "format": utils.thousands_format(2)}),
                "latest_outlook"        : hx.Str(  mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Outlook"}),
                "latest_description"    : hx.Str(  mode="input", default=None, optionality="optional", async_output=["task_fetch_ihs_data"], view={"label": "Outlook Description"}),
            }),

       })
    })


 