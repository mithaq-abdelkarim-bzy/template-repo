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

            "last_run_status"           : hx.Str( mode="output", view={"label": "Status - Last load of IHS Data"}),
            "last_run_date"             : hx.Str( mode="output", view={"label": "Date - Last load of IHS Data"}),
            "last_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Last load of IHS Data"}),
            "calc_run_value"            : hx.Str( mode="output", view={"label": "IHS data to be extracted"}),
            "check_run_consistent"      : hx.Str( mode="output", view={"label": "Does data need to be reloaded:"}),


            # listing of individual facilities (technically section references)
            "ihs_outlook": hx.List(mode="input", children={
                "country"                     : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Country "}),
                "risk_name"                   : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Risk Name"}),
                "outlook"                     : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Outlook"}),
                "outlook_description"         : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Outlook Description"}),
                "last_updated_date"           : hx.Date(mode="input", default=None,   optionality="optional", view={"label": "Last Updated Date"}),
                "last_updated_value"          : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Last Updated Value",          "format": utils.thousands_format(2)}),
            }),

            # listing of individual facilities (technically section references)
            "ihs_detail": hx.List(mode="input", children={
                "country"                     : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Country "}),
                "risk_name"                   : hx.Str(mode="input",  default=None,   optionality="optional", view={"label": "Risk Name"}),
                "historic_updated_date"       : hx.Date(mode="input", default=None,   optionality="optional", view={"label": "Historic Updated Date"}),
                "historic_updated_value"      : hx.Float(mode="input",default=None,   optionality="optional", view={"label": "Historic Updated Value",  "format": utils.thousands_format(2)}),
            }),
       })
    })


 