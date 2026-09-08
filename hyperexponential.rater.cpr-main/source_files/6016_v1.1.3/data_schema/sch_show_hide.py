# show hide on tables must be contained within the respective lists & algorithms rather than here
# show hide on standard skeleton model characteristics is contained where they were coded



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
                "show_exposure_detail"      : hx.Bool(mode="output"),
                "show_ihs"                  : hx.Bool(mode="output"),
                "show_rating_summary"       : hx.Bool(mode="output"),
                "show_rationale"            : hx.Bool(mode="output"),
                "show_actuarial"            : hx.Bool(mode="output"),
                "show_rate_change"          : hx.Bool(mode="output"),

            }),
            "node":    hx.Structure(children={
                "show_crcf"                     : hx.Bool(mode="output"),
                "show_cr_only"                  : hx.Bool(mode="output"), # used to identify credit risk (cr) as opposed to contract frustration (cf)
                "show_political"                : hx.Bool(mode="output"),
                "show_pre_shipment_risk"        : hx.Bool(mode="output"),
                "show_pre_shipment_risk_not"    : hx.Bool(mode="output"),

#                "load_show_hide"                : hx.Bool(mode="output"),
                "show_hide_flat"                : hx.Bool(mode="output"),
                "show_hide_flat_not"            : hx.Bool(mode="output"),
                "show_hide_step"                : hx.Bool(mode="output"),
            }),
        }),
    })
