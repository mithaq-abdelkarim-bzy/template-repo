import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.rate_constants import max_layers

def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": percent_format(1)}, async_output= [{"task": "start_renewal_task", "reset": False}]),
        "quoted_premium_case_priced": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium (Case Priced)", "format": thousands_format()}, async_output= [{"task": "start_renewal_task", "reset": False}]),
        "deal_status_record": hx.Str(mode="output", view={"label": "Deal Status by Renewal Layers"}),
        # Used for rate change calcs
        "quoted_premium_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
        "benchmark_premium_annualised": hx.Float(mode='output', async_input=["rarc_task"])
    })
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers, "async_output": [{"task": "start_renewal_task", "reset": False}]})

    # Override default values
    cds.override_node_properties("cds/layers/section_reference", {"mode": "output", "view": {"info": "Reporting Hull section reference."}})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode": "output", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/brokerage", {"mode": "output", "view": {"info": "Premium-weighted average of Hull and Liability brokerage."}})
    cds.override_node_properties("cds/layers/written_line", {"mode": "output", "view": {"info": "Premium-weighted average of Hull and Liability written line."}})
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/standard_fields/uw_rationale", {"async_output": [{"task": "start_renewal_task", "reset": False}]})

    coverages = ["hull", "liability"]
    for cvg in coverages:
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/benchmark_premium", {"async_input": ["rarc_task"], "view": {"info": "Includes NMP adjustment"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/pflr", {"view": {"label": "Implied Gross LR"}})

        cds.extend_node_rater_defined(f"cds/layers/coverages/{cvg}", {
            # Used for rate change calcs
            "quoted_premium_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
            "benchmark_premium_annualised": hx.Float(mode='output', async_input=["rarc_task"])
        })
        
