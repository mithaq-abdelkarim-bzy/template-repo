import hx_data_schema as hx
import data_schema.utilities as utils
import algorithms.utils_global_lists as lst
from algorithms.utils_functions import create_title
from algorithms.rate_constants import max_options
from libraries.common_data_schema.algorithms import parameter_tables_schema as params


def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format":utils.percent_format(1)}),
        "status_view": hx.Str(mode="output", view={"label": "Status"}),
        "pflr_pre_uw_adj": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
    })
    
    cds.extend_node_rater_defined("cds", {
        "options": hx.List(mode= "input", default_element_count = 1, view = {"label":"Options"}, children={
            "quoted_premium": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium (Case Priced)", "format": utils.thousands_format(0)}),     
            "benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": utils.thousands_format(0)}),   
            "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium", "format": utils.thousands_format(0)}),                
            "status": hx.Str(mode="input", options=params.status.column("Status"), default="Assessment Pending", view={"label": "Status"}),
            "section_reference": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference"}),
            "bpi": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": {"output": "percent", "mantissa": 1}}),
            "tpi": hx.Float(mode="output", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "roc": hx.Float(mode="output", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
            "written_line": hx.Float(mode="input",default=1, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}), 
            "brokerage": hx.Float(mode="input", default=0, view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),    
            "status_view": hx.Str(mode="output", view={"label": "Status"})
     })
    })

    cds.extend_node_rater_defined("cds", {
        "rate_change": hx.Structure(children={
            **{f"show_option_{index}": hx.Bool(mode="output") for index in range(1,max_options+1)},
        })
    })