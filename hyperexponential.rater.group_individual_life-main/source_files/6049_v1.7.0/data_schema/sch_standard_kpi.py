import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

def sch_standard_kpi(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced_view": hx.Float(mode="output", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
        "quoted_premium_case_priced_view": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
    })
   