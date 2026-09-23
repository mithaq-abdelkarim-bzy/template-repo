import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_pricing(cds):

        
    # Adding coverages to the layers list. NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_items("cds/layers/coverages", {
        "eo": {"label": "E&O"},
        "mediatech": {"label": "Media Tech"},
        "gl": {"label": "General Liability"},
    })


    # Adding a rated-defined field to ALL coverages
    cds.extend_node_rater_defined("cds/layers/coverages", {
        "guideline_deductible": hx.Float(mode="output", view={"label": "Guideline Retention", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "expected_loss_cost_pre_uw_adj_usd":hx.Float(mode="output", view={"label": "Expected Claims Cost Before UW Adjustment (USD)"}),
        "expected_loss_cost_usd":hx.Float(mode="output", view={"label": "Expected Claims Cost After UW Adjustment (USD) "}),
        "expected_loss_cost_pre_uw_adj":hx.Float(mode="output", view={"label": "Expected Claims Cost Before UW Adjustment"}),
        "expected_loss_cost":hx.Float(mode="output", view={"label": "Expected Claims Cost After UW Adjustment"}),
        "benchmark_premium_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_pre_uw_adj_usd": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment) (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_usd": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_usd": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_pre_uw_adj_usd": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (Pre-UW Adjustment) (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_net_usd": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_net_pre_uw_adj_usd": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (Pre-UW Adjustment) (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_net_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_net_usd": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium ", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_net_pre_uw_adj_usd": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (Pre-UW Adjustment) (USD)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "benchmark_premium_net_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "Net Benchmark Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "limit_relativity": hx.Float(mode = "output", view = {"label": "Limit Relativity"}),
        "deductible_relativity": hx.Float(mode = "output", view = {"label": "Deductible Relativity"}),
        "expected_loss_cost_before_minimum_premium_usd":hx.Float(mode="output", view={"label": "Expected Claims Cost After UW Adjustment and Before Minimum Premium (USD)"}),
        "expected_loss_cost_before_minimum_premium":hx.Float(mode="output", view={"label": "Expected Claims Cost After UW Adjustment and Before Minimum Premium"}),
        "technical_premium_net_before_minimum_prem_usd": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium (USD) Before Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_before_minimum_prem_usd": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (USD) Before Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_net_before_minimum_prem": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium Before Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "technical_premium_before_minimum_prem": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium Before Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "option_selected": hx.Str(mode = "input", default="No", options=["Yes", "No"], view={"label": "Option Selected: Yes/No"}),
        "pflr_pre_uw_adj": hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        "policy_section_reference_label": hx.Str(mode="input", default="Policy Section Reference"),
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
    })
    # add Additional Defense Limit Per Claim to Media Tech
    cds.extend_node_rater_defined("cds/layers/coverages/mediatech", {
        "additional_defense_limit": hx.Float(mode = "input", async_input=["rarc_task"], default = None, optionality = "optional", view={"label": "Additional Defense Limit", "format": {"thousandSeparated": True, "mantissa": 0}} )

    })

    # add more inputs to GL cover
    cds.extend_node_rater_defined("cds/layers/coverages/gl", {
        # "product_limit_agg": hx.Float(mode = "output", view={"label": "Product Liability Limits AGG", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "gl_limit_agg": hx.Float(mode = "output", view={"label": "General Liability Limits AGG", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "personal_advertise_limit_agg": hx.Float(mode = "output", view={"label": "Personal Advertising Liability Limit EEC", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "defence_outside_limit": hx.Str(mode = "input", async_input=["rarc_task"], optionality="optional", default = None, options_table="table_gl_product_defence_limit", options_column="defence_over_limits", view = {"label": "Defence Outside Limits"}),
        "excess_of": hx.Float(mode = "input", async_input=["rarc_task"], optionality = "optional", default = None, view={"label": "Excess Of", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "excess_relativity": hx.Float(mode = "output", view = {"label": "Excess Relativity"}),
        #local currency converted
        "limit_local_currency":hx.Float(mode = "output", view= {"label":"Liability Limits EEC", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "aggregate_limit_local_currency": hx.Float(mode = "output", view={"label": "Product Liability Limits AGG", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "gl_limit_agg_local_currency": hx.Float(mode = "output", view={"label": "General Liability Limits AGG", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "personal_advertise_limit_agg_local_currency": hx.Float(mode = "output", view={"label": "Personal Advertising Liability Limit EEC", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "defence_outside_limit_local_currency": hx.Float(mode = "output", view = {"label": "Defence Outside Limits", "format": {"thousandSeparated": True, "mantissa": 0}}),
        "excess_of_local_currency": hx.Float(mode = "output", view={"label": "Excess Of", "format": {"thousandSeparated": True, "mantissa": 0}} ),
        "deductible_local_currency": hx.Float(mode = "output", view={"label": "Primary Deductible", "format": {"thousandSeparated": True, "mantissa": 0}} ),
    })


    cds.extend_node_rater_defined("cds/layers", {
        "option_selected": hx.Str(mode = "output", view={"label": "Renewal Option Selected: Yes/No"}),
        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        "bpi_case_priced": hx.Float(mode="input", default=None, optionality="optional", view={"label": "BPI (Case Priced)", "format": percent_format(1)}),
    })

    # change the labelling
    cds.override_node_properties('cds/layers/coverages/eo/deductible', {"mode": "override", "async_input": ["rarc_task"],"view": {"label":"Retention"}})
    cds.override_node_properties('cds/layers/coverages/mediatech/deductible', {"mode": "override","async_input": ["rarc_task"],"view": {"label":"Retention"}})
    cds.override_node_properties('cds/layers/coverages/gl/deductible', {"async_input": ["rarc_task"], "options_table": "table_gl_product_primary_deductible", "options_column": "primary_deductible", "allow_custom_value": True,"view": {"label":"Primary Deductible"}})
    cds.override_node_properties('cds/layers/deductible', {"default": 0, "view": {"label":"Retention"}})
    cds.override_node_properties('cds/layers/written_line', {"default": 1})
    
    cds.override_node_properties('cds/layers/benchmark_premium', {"async_input": ["rarc_task"]})
    cds.override_node_properties('cds/layers/quoted_premium', {"async_input": ["rarc_task"], "mode": "output"})

    cds.override_node_properties('cds/layers/limit', {"default": 0,"view": {"label":"Each and Every Limit"}})
    cds.override_node_properties('cds/layers/coverages/eo/limit', { "async_input": ["rarc_task"],"view": {"label":"Each and Every Limit"}})
    cds.override_node_properties('cds/layers/coverages/mediatech/limit', {"async_input": ["rarc_task"],"view": {"label":"Each and Every Limit"}})
    cds.override_node_properties('cds/layers/coverages/gl/limit', {"async_input": ["rarc_task"], "options_table": "table_gl_product_eec_limit", "options_column": "eec_limit", "default": None,"allow_custom_value": True, "view": {"label":"Liability Limits EEC"}})
    
    cds.override_node_properties('cds/layers/coverages/gl/aggregate_limit',{"mode": "output", "view":{"label": "Product Liability Limits AGG"}})
    cds.override_node_properties('cds/layers/coverages/eo/aggregate_limit',{"mode": "override", "async_input": ["rarc_task"]})
    cds.override_node_properties('cds/layers/coverages/mediatech/aggregate_limit',{"mode": "override","async_input": ["rarc_task"]})

    cds.override_node_properties('cds/layers/coverages/eo/brokerage', { "async_input": ["rarc_task"], "validation": {"min_value": 0.0, "max_value":1.0}, "view": {"options": {
        "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True}
        },
        "label": "Brokerage"
    }})
    cds.override_node_properties('cds/layers/coverages/mediatech/brokerage', { "async_input": ["rarc_task"],"validation": {"min_value": 0.0, "max_value":1.0}, "view": {"options": {
        "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True}
        },
        "label": "Brokerage"
    }})
    cds.override_node_properties('cds/layers/coverages/gl/brokerage', { "async_input": ["rarc_task"],"validation": {"min_value": 0.0, "max_value":1.0}, "view": {"options": {
        "read_only": {"label": "Brokerage (excl. PC's)", "read_only": True}
        },
        "label": "Brokerage"
    }})

    cds.override_node_properties('cds/layers/coverages/eo/written_line', {"default": 1, "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/gl/written_line', {"default": 1, "view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/mediatech/written_line', {"default": 1, "view": {"options": {"read_only": {"read_only": True}}}})

    cds.override_node_properties('cds/layers/coverages/eo/technical_premium', {"view": {"label":"Gross Technical Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Technical Premium"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/mediatech/technical_premium', {"view": {"label":"Gross Technical Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Technical Premium"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/gl/technical_premium', {"view": {"label":"Gross Technical Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Technical Premium"
        }
    }}})

    cds.override_node_properties('cds/layers/coverages/eo/benchmark_premium', {"view": {"label":"Gross Benchmark Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Benchmark Premium"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/mediatech/benchmark_premium', {"view": {"label":"Gross Benchmark Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Benchmark Premium"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/gl/benchmark_premium', {"view": {"label":"Gross Benchmark Premium After Minimum Premium", "options": {
        "short_label": {
            "label": "Gross Benchmark Premium"
        }
    }}})

    cds.override_node_properties('cds/layers/coverages/eo/section_reference',{"view": {"options": {
        "read_only": {
            "read_only": True
        },
        "rater_priced_label": {
            "label": "Policy Section Reference",
        },
        "case_priced_label": {
            "label": "Section Reference"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/mediatech/section_reference', {"view": {"options": {
        "read_only": {
            "read_only": True
        },
        "rater_priced_label": {
            "label": "Policy Section Reference",
        },
        "case_priced_label": {
            "label": "Section Reference"
        }
    }}})
    cds.override_node_properties('cds/layers/coverages/gl/section_reference', {"view": {"options": {
        "read_only": {
            "read_only": True
        },
        "rater_priced_label": {
            "label": "Policy Section Reference",
        },
        "case_priced_label": {
            "label": "Section Reference"
        }
    }}})
    cds.override_node_properties('cds/layers/section_reference', {"view": {"label":"Policy Section Reference"}})    

    cds.override_node_properties('cds/layers/coverages/eo/quoted_premium', {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/mediatech/quoted_premium', {"view": {"options": {"read_only": {"read_only": True}}}})
    cds.override_node_properties('cds/layers/coverages/gl/quoted_premium', {"view": {"options": {"read_only": {"read_only": True}}}})
    
    
    # add dynamic labelling
    cds.extend_node_rater_defined("cds", {
        "eo_fees_currency_label": hx.Str(mode = "output"),
        "mediatech_revenue_currency_label": hx.Str(mode = "output"),
        "gl_revenue_currency_label": hx.Str(mode = "output"),
        "gl_revenue_total_currency_label": hx.Str(mode = "output"),
        "gl_local_currency_label": hx.Str(mode = "output")

    })

    cds.extend_node_rater_defined("cds", {
        "gl_local_currency": hx.Bool(mode = "input", default = False, view = {"label": "Show Pricing Inputs in Source Currency"}),

    })



  