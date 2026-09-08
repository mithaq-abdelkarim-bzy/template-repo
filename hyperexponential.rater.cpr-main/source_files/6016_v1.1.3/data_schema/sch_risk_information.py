#########################################################################################################
########################################### Outstanding Items ###########################################
#########################################################################################################
### 1) 
### 2) 
### 2) 
### 4) 
#########################################################################################################

import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "policy_option_id":         hx.Int( mode="output",                  view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "database_id":              hx.Int( mode="output",                  view={"label": "Database ID", "format": utils.integer_format(0)}),
        "broker_contact":           hx.Str( mode="input",    default="",    view={"label": "Broker Contact"}),
        "product":                  hx.Str( mode="input",    default="",    view={"label": "Product"},          options_table="lst_product",         options_column="Product"),


        # CRCF Specifc
        "risk_info"  : hx.Structure(children={
            "crcf_industry_group":      hx.Str(mode="input",    default="",    view={"label": "Industry Group"},   options_table="lst_industry_group",  options_column="Industry Group"),
            "crcf_industry":            hx.Str(mode="input",    default="",    view={"label": "Industry"},         options_table="tbl_industry",        options_column="Industry"       ,allow_custom_value= True),
            "crcf_obligor":             hx.Str(mode="input",    default="",    view={"label": "Obligor"}),
            "crcf_country":             hx.Str(mode="input",    default="",    view={"label": "Country"},          options_table="tbl_ihs_country",     options_column="IHS Country"),
            "crcf_term":                hx.Float(mode="output",                view={"label": "Policy Term", "format": utils.thousands_format(0)}),
        }),

        # relating to the task to use sql to load from Beazley Intelligence
        "bi"  : hx.Structure(children={
            "last_run_status"           : hx.Str( mode="output", view={"label": "Status - Last load of BI Data"}),
            "last_run_date"             : hx.Str( mode="output", view={"label": "Date - Last load of BI Data"}),
            "last_run_value"            : hx.Str( mode="output", view={"label": "Check Value - Last load of BI Data"}),
            "calc_run_value"            : hx.Str( mode="output", view={"label": "BI data to be extracted"}),
            "check_run_consistent"      : hx.Str( mode="output", view={"label": "Does data need to be reloaded:"}),
        })

    })


 