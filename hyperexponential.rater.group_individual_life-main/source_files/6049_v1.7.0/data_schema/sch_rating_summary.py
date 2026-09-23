import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        "quoted_premium_case_priced": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium (Case Priced)", "format": thousands_format()}),
        "deal_status_record": hx.Str(mode="output", view={"label": "Deal Status by Renewal Layers"}),
        "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format":percent_format(1)}),
        "brokerage_view": hx.Float(mode="output", optionality="optional",  view={"label": "Brokerage (excl. PC's)", "format":percent_format(1)}),
        "status_view": hx.Str(mode="output", view={"label": "Status"}),
        "section_reference_view": hx.Str(mode="output", view={"label": "Section Reference"}),
        "pflr_pre_uw_adj": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
    })
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})

    # Override default values
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output", "async_input": ["rarc_task"]}) # Premium is calculated from quoted rate
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})

    cds.override_node_properties("cds/layers/section_reference",{"mode": "output"})
    
    # Coverage specific
    coverages = [
        "death",
        "additional_death",
        "terminal_illness",
        "critical_illness",
        "repat_exp"
    ]
    for cvg in coverages:
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/uw_adj_impact", {"view": {"label": "Implied Commercial Adjustment", "format": thousands_format(2)}})
    