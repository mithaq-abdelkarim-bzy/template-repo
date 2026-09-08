import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers
import data_schema.sch_utilities as utils

def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        "deal_status_record": hx.Str(mode = "output", view = {"label": "Deal Status by Renewal Layers"}),
        "gross_premium_label": hx.Str(mode="output", view={"label": " "})
    })
    
    # Override default values
    cds.override_node_properties(
        "cds/layers/brokerage", 
        {"default": 0, "optionality": "required", "async_input": ["rarc_task", "load_cargo_input"], "view": {"label": "Deductions", "format": percent_format(1)}}
    )
    cds.override_node_properties("cds/layers/written_line", {"default": 0, "optionality": "required", "async_input": ["load_cargo_input"]})
    cds.override_node_properties("cds/layers/quoted_premium", {"default": 0, "optionality": "required", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})  
