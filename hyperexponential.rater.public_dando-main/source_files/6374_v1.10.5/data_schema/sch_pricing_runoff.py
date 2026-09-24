import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
import data_schema.sch_utilities as utils
import algorithms.rate_constants as const

def sch_pricing_runoff(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "runoff_original_premium": hx.Float(mode="input", default=1, view={"label": "Runoff Original Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "runoff_adjustment": hx.Float(mode="input", default=1, view={"label": "Runoff Factor"}),
        "runoff_premium": hx.Float(mode="input", default=1, view={"label": "Runoff Premium", "format": {"thousandSeparated": True, "mantissa": 0}})
    })