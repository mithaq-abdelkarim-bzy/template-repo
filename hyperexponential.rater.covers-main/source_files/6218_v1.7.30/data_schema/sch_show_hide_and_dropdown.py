import hx_data_schema as hx
import data_schema.sch_utilities as utils
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format


def sch_show_hide(cds):
    '''
    Internal Model State that controls the workflow
    '''

    cds.extend_node_rater_defined("cds", {
        "show_hide": hx.Structure(children={
            "page":    hx.Structure(children={
                "show_rms"                  : hx.Bool(mode="output"),
                "show_actuarial"            : hx.Bool(mode="output"),
                "show_profit_commission"    : hx.Bool(mode="output"),
                "show_triangle"             : hx.Bool(mode="output"),
                "show_sov"                  : hx.Bool(mode="output"),
            }),
            "node":    hx.Structure(children={
                "pc_standard"               : hx.Bool(mode="output"),
                "pc_threshold"              : hx.Bool(mode="output"),
                "pc_sliding_scale"          : hx.Bool(mode="output"),

                "rs_att_rationale"          : hx.Bool(mode="output"),
                "rs_lrg_rationale"          : hx.Bool(mode="output"),
                "rs_cat_rationale"          : hx.Bool(mode="output"),

                "not_new_to_market"         : hx.Bool(mode="output"),        

                "loss_ratio_rms"            : hx.Bool(mode="output"),        
                "loss_ratio_benchmark"      : hx.Bool(mode="output"),        

                "ri_proxy_trifocus"         : hx.Bool(mode="output"),  

                "show_experience"           : hx.Bool(mode="output"),

                "signed_line"               : hx.Bool(mode="output")

            }),
        }),
    })


#################################################
################# Dropdown Lists ################
#################################################

### Risk Information page

business_type_list =["", "Residential", "Commerical"]

coverage_list = ["", "Special", "Basic", "HO1", "HO2", "HO3", "HO5", "DP3"]

follow_lead_list = ["", "Follow", "Lead"]

uw_list = ["Alex Hardy", "John Taylor", "Alasdair Lea", "Laura Evans", "David Pentecost", "Alex Burgess", "Tanis Harding"]


### Schedule Page

schedule_policy_type =["Unknown", "New", "Renewal", "Endorsement", "Reinstatement", "New Business"] # will need to consolidate New Business and New in code 

# sprinkler 
sprinkler_list = ["", "Yes", "Partial", "No", "Unknown"]

covered_list = ["Yes", "No"]

yes_no_list = ["Yes", "No"]

gn_list = ["Gross", "Net"]

pc_structure_type_list = ["No", "Threshold", "Sliding Scale"]

basis_list = ["Gross Gross", "Gross Net"]

country_list = ["US","Canada","New Zealand","Australia","United Kingdom","France","Germany","ROW"]
