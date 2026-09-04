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

            }),
        }),
    })
