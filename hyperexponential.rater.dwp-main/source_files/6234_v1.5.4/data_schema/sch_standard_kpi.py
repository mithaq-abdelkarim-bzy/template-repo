import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_standard_kpi(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced_view": hx.Float(mode="output", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
        "quoted_premium_view": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": thousands_format()}),
        "written_line_view": hx.Float(mode="output", optionality="optional", view={"label": "Written Line", "format":percent_format(1)}),
        "brokerage_view": hx.Float(mode="output", optionality="optional",  view={"label": "Brokerage (excl. PC's)", "format":percent_format(1)}),
        "status_view": hx.Str(mode="output", view={"label": "Status"}),
        "section_reference_view": hx.Str(mode="output", view={"label": "Section Reference"}),
        "pflr_pre_uw_adj": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
        "benchmark_premium_view": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": thousands_format()}),
    })

    cds.override_node_properties(
        "cds/layers/technical_premium", { "view":{"label": "Gross Technical Premium"}} 
    )

   
