import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import coverages_dict

def sch_rating_summary(cds):

    cds.extend_node_rater_defined("cds/layers", {
        "bpi_case_priced": hx.Float(mode="input", default=0, view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        'premium_label': hx.Str(mode='output'),
        
        "quoted_premium_100_pct": hx.Float(   mode          = "input"
                                            , default       = None
                                            , view          = {"label": "Gross Quoted Premium (100%)", "format": thousands_format()}
                                            , optionality   = "optional"
                                            , validation    = {"min_value": 0}),

        "quoted_premium_case_priced": hx.Float(mode="output",  async_input=["rarc_task"],view={"label": "Gross Quoted Premium (Case Priced)", "format": thousands_format()}),
        "deal_status_record": hx.Str(mode="output", view={"label": "Deal Status by Renewal Layers"}),        
        # Used for rate change calcs
        "quoted_premium_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
        "benchmark_premium_annualised": hx.Float(mode='output', async_input=["rarc_task"])
    })
    cds.override_node_properties("cds/layers", {"max_element_count": max_layers})

    # Override default values
    cds.override_node_properties("cds/layers/benchmark_premium", {"async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/quoted_premium", {"mode":"output", "async_input": ["rarc_task"]})

    # overrides have to occur here as when they are coded in algorithms.data_schema.sch_rater_defined > cvg_fields_combined the cds dominates and resets them to its defaults
    for cvg in coverages_dict.keys():
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/benchmark_premium"
                                        , {"async_input":   ["rarc_task"]
                                        ,  "view":          { "info":   "Includes NMP adjustment"
                                                            , "label":  "Benchmark Premium"
                                                            , "format": thousands_format()}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/pflr",                            { "view": {"label": "Priced Loss Ratio - Gross Gross"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium", {"mode": "output", "view": {"label": "Offered Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/technical_premium",               { "view": {"label": "Technical Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/technical_premium_pre_uw_adj",    { "view": {"label": "Technical Premium (Pre-UW Adjustment)"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/model_premium",                   { "view": {"label": "Plan Premium"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/tpi_pre_uw_adj",                  { "view": {"label": "TPI (Pre-UW Adjustment)"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/bpi_pre_uw_adj",                  { "view": {"label": "BPI (Pre-UW Adjustment)"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/tpi",                             { "view": {"label": "TPI", "style_row": "hx-neutral"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/bpi",                             { "view": {"label": "BPI", "style_row": "hx-neutral"}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/pflr_pre_uw_adj",                 { "view": {"label": "Priced-for Loss Ratio (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}})
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/benchmark_premium_pre_uw_adj",    { "view": {"label": "Benchmark Premium (Pre-UW Adjustment)",     "info":"Includes NMP adjustment","format": thousands_format()}})



        cds.extend_node_rater_defined(f"cds/layers/coverages/{cvg}", {
            # Used for rate change calcs
            "quoted_premium_annualised": hx.Float(mode="output", async_input=["rarc_task"]),
            "benchmark_premium_annualised": hx.Float(mode='output', async_input=["rarc_task"])
        })
        
