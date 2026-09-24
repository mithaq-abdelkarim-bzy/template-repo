import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
    })


    
    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})
    cds.override_node_properties("cds/layers/status", {"view": {"options": {
        "input": {"label": "Status"},
        "read_only": {"label": "Deal Status by Renewal Layers", "read_only": True}
    }}})
    
    #cds.override_node_properties("cds/layers/brokerage", {"default": 0, "optionality": "required" })
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output","async_input":["rarc_task"]})
    cds.override_node_properties("cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"})
