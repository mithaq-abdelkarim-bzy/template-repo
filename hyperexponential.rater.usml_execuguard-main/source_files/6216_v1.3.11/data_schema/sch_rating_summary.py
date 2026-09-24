import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers, tp_summary_layers
import data_schema.sch_utilities as utils


def sch_rating_summary(cds):
    cds.extend_node_rater_defined(
        "cds/layers",
        {
            # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary.
            "bpi_case_priced": hx.Float(
                mode="input",
                default=None,
                optionality="optional",
                view={"label": "BPI (Case Priced)", "format": percent_format(2)},
            ),
            "pflr_pre_uw_adj": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        },
    )

    # Override values
    cds.override_node_properties("cds/layers", {"max_element_count": tp_summary_layers})

    # cds.override_node_properties("cds/quote_grid_summary/epl/limit", {"async_input":["rarc_task"]})
    # cds.override_node_properties("cds/quote_grid_summary/epl/adl", {"async_input":["rarc_task"]})
    # cds.override_node_properties("cds/quote_grid_summary/epl/retention", {"async_input":["rarc_task"]})
    # cds.override_node_properties("cds/quote_grid_summary/epl/benchmark_premium", {"async_input":["rarc_task"]})
    # cds.override_node_properties("cds/quote_grid_summary/epl/pre_rounding_admitted_premium", {"async_input":["rarc_task"]})   
    # cds.override_node_properties("cds/quote_grid_summary/epl/selected_premium", {"async_input":["rarc_task"]})          
    # cds.override_node_properties("cds/quote_grid_summary/epl/post_rounding_admitted_premium", {"async_input":["rarc_task"]})   
    # cds.override_node_properties("cds/quote_grid_summary/epl/final_term_premium", {"async_input":["rarc_task"]})   
    # cds.override_node_properties("cds/quote_grid_summary/epl/bpi", {"async_input":["rarc_task"]})

    cds.override_node_properties("cds/quote_grid_summary/fid/benchmark_premium", {"async_input":["rarc_task"]})
    cds.override_node_properties("cds/quote_grid_summary/pcl/benchmark_premium", {"async_input":["rarc_task"]})
    

    cds.override_node_properties(
        "cds/layers/bpi_case_priced", {"default": 0, "optionality": "required"}
    )
    # cds.override_node_properties("cds/layers/written_line", {"mode": "output"})
