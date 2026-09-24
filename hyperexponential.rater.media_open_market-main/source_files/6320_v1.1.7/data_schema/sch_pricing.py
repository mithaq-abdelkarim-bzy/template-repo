import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers, max_options
import data_schema.sch_utilities as utils
from hx import params as hx_params

def sch_pricing(cds):
    cds.extend_node_rater_defined("cds", {
        # Show/hides for rating summary view
        "rater_priced_standard" : hx.Bool(mode="output"),
        "rater_priced_nonstandard" : hx.Bool(mode="output"),
        "rater_priced_excess" : hx.Bool(mode="output"),
        "coverage_selected_flag" : hx.Bool(mode="output"),

        # Flag to open Excess Pricing tab. Select when pricing excess layer.
        "price_excess_flag": hx.Bool(mode="input", optionality="required", default=False, view={"label": "Price Excess"}),
        "excess_pricing_note": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Notes"}),

        "rating_factors": hx.Structure(children={
            "policy_term": hx.Float(mode="output", async_input=["rarc_task"]),
            "guideline_deductible": hx.Float(mode="output", view={"label": "Guideline Deductible", "format":utils.thousands_format(0)}),
            "ilf_curve": hx.Str(mode="input", optionality="optional", default=None, options=["Low", "Medium", "High"], view={"label": "ILF Curve"}, async_input=["rarc_task"]),
            "default_curve": hx.Str(mode="output"), # Used for pricing calcs. Not shown in view.
            "years_in_business" : hx.Str(mode="input", optionality="optional", default=None, options=hx_params.tbl_longevity_factor["years_in_business"].tolist(), view={"label": "Years in Business"}, async_input=["rarc_task"]),
            "location" : hx.Str(mode="input", optionality="optional", default=None, options=hx_params.table_country["country"].tolist(), view={"label": "Country"}, async_input=["rarc_task"]),
            "territory_factor" : hx.Float(mode="output", view={"label": "Country Factor"}, async_input=["rarc_task"]),            
        }),
    })

    # Options structure (for primary layer pricing) -------------------------------------------------------------------------
    # For Rating Summary tab [standard_rater_masking: Media Liability, Music Liabilty, TV & Film E&O]
    # The selected option will be used for the primary_layer nodes, and mapped to the layers nodes for reporting.

    cds.extend_node_rater_defined("cds", {
        "options": hx.List(mode="input", default_element_count= max_options, view= {"label":"Options"}, children={  #fixed_element_count= max_options
            "option_label": hx.Str(mode="output", view={"label": "Option"}),
            "eec_limit": hx.Float(mode="input", optionality="optional", options=[1e6, 2e6, 3e6, 5e6], allow_custom_value=True, default=None, view={"label": "EEC Limit","format":utils.thousands_format(0)}, async_input= ["rarc_task"]),
            "aggregate_limit": hx.Float(mode="input", optionality="optional", options=[1e6, 2e6, 3e6, 5e6], allow_custom_value=True, default=None, view={"label": "Aggregate Limit","format":utils.thousands_format(0)}, async_input= ["rarc_task"]),
            "eec_excess": hx.Float(mode="input", optionality="optional", options=[10000, 25000, 50000], allow_custom_value=True, default=None, view={"label": "EEC Excess","format":utils.thousands_format(0)}, async_input= ["rarc_task"]), # Non-standard coverages only
            "aggregate_excess": hx.Float(mode="input", optionality="optional", options=[10000, 25000, 50000], allow_custom_value=True, default=None, view={"label": "Aggregate Excess","format":utils.thousands_format(0)}, async_input= ["rarc_task"]), # Non-standard coverages only
            "retention": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Retention","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 10000000000}, async_input= ["rarc_task"]),
            "technical_premium": hx.Float(mode="output", view={"label": "Technical Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000}),
            "benchmark_premium": hx.Float(mode="output", view={"label": "Benchmark Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000}),
            "quoted_premium": hx.Float(mode="input", optionality="optional", default=None, async_output=["start_renewal_task"], view={"label": "Quoted Premium","format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 100000000000}),
            "quoted_bpi": hx.Float(mode="output", view={"label": "Quoted BPI %", "format":utils.percent_format(2)}),
        }),

        #The selected option from the pricing tab        
        "option_selected": hx.Str(mode="input", default="Option 1", options=[f"Option {i}" for i in range(1,max_options+1)], view={"label": "Bound Option"},async_input=["rarc_task"]), 
        
        # IDF for nonstandard coverages - saved down to be used in excess pricing function
        "nonstandard_idf" : hx.Float(mode="output")
    })

    # Primary Layer selected  --------------------------------------------------------------------
    # For Rating Summary tab
    cds.extend_node_rater_defined("cds", {
        "primary": hx.Structure(children={
            "layer_label": hx.Str(mode="output", view={"label": "Layer Label"}),
            "status": hx.Str(mode="input", default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], async_output=["start_renewal_task"], view={"label": "Status"}),
            "status_view": hx.Str(mode="output", view={"label": "Status"}), # For view in excess pricing table
            "brokerage": hx.Float(mode="input", optionality="optional", default=None, view={"label":"Brokerage", "format":utils.percent_format(2)}, async_input=["rarc_task"]),
            # Quoted Premium View: for primary layer, picks up from option selected.
            "quoted_premium_view": hx.Float(mode="output", view={"label": "Quoted Premium", "format":utils.thousands_format(0)}),
            "bound_premium": hx.Float(mode="output", view={"label": "Bound Premium", "format":utils.thousands_format(0)}),
            "bound_premium_input": hx.Float(mode="input", optionality="optional", default=None, async_output=["start_renewal_task"], view={"label": "Bound Premium", "format":utils.thousands_format(0)}, validation={"min_value": 0, "max_value": 1000000000}), 
            "model_premium": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}), # For non-standard raters, which don't use options.
            "benchmark_premium": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Gross Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium_net": hx.Float(mode="output", async_input=["rarc_task"], optionality="optional", view={"label": "Net Benchmark Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "bpi": hx.Float(mode="output", optionality="optional", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "BPI Pre UW Adj", "format": {"output": "percent", "mantissa": 1}}),
            "technical_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "technical_premium_net": hx.Float(mode="output", optionality="optional", view={"label": "Net Technical Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "tpi": hx.Float(mode="output", optionality="optional", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output", optionality="optional", view={"label": "TPI Pre UW Adj", "format": {"output": "percent", "mantissa": 1}}),
            "aggregate_limit_view": hx.Float(mode="output", view={"label": "Aggregate Limit","format":utils.thousands_format(0)}, async_input=["rarc_task"]),
            "attachment": hx.Float(mode="output", view={"label": "Attachment","format":utils.thousands_format(0)}, async_input=["rarc_task"]),
            "expected_loss_cost": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(0)}),
            "expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "", "format":utils.thousands_format(0)}),
            "section_reference_view": hx.Str(mode="output", view={"label": "Section Reference"}), # For view in excess pricing table
            "section_reference": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
        })
    })
    
    # Layers structure --------------------------------------------------------------------------
    # For Rating Summary tab
    cds.extend_node_rater_defined("cds/layers", {
        "layer_label": hx.Str(mode="output", view={"label": "Layer Label"}),
        "excess_flag": hx.Bool(mode="output", view={"label": "view in excess table?"}),
        "attachment": hx.Float(mode="output", view={"label": "Attachment","format":utils.thousands_format(0)}, async_input=["rarc_task"]),
        "implied_price_per_m": hx.Float(mode="output", view={"label": "Implied Price Per Mil","format":utils.thousands_format(0)}), # per million of source currency (not USD)
        "implied_ilf": hx.Float(mode="output", view={"label": "Implied ILF","format":utils.percent_format(2)}),
        "carrier": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Carrier"}),
        "quoted_price_per_m": hx.Float(mode="output", view={"label": "Quoted Price Per Mil","format":utils.thousands_format(0)}), # per million of source currency (not USD)
        "quoted_ilf": hx.Float(mode="output", view={"label": "Quoted ILF","format":utils.percent_format(2)}),
        "bound_premium": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Bound Premium", "format":utils.thousands_format(0)}, async_input=["expiring_policy_fetch_task","rarc_task"], async_output=["start_renewal_task"], validation={"min_value": 0, "max_value": 1000000000}),
        # Input fields: for view in excess pricing, layers 1 to 10
        "quoted_premium_view": hx.Float(mode="input", optionality="optional", default=None, view={"label": "Quoted Premium", "format":utils.thousands_format(0)}, async_input=["expiring_policy_fetch_task","rarc_task"], async_output=["start_renewal_task"], validation={"min_value": 0, "max_value": 1000000000}),
        "status_view": hx.Str(mode="input", default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], async_output=["start_renewal_task"], view={"label": "Status"}),
        "section_reference_view": hx.Str(mode="input", default=None, optionality="optional", async_output=["start_renewal_task"], view={"label": "Section Reference", "options": {"read_only": {"read_only": True}}}),
        # Input fields: for view in excess pricing, layers 0 to 10
        "brokerage_input": hx.Float(mode="input", optionality="optional", default=None, view={"label":"Brokerage", "format":utils.percent_format(2)}),
        # Written line input: for case priced rating summary
        "written_line_input" : hx.Float(mode="input", optionality="optional", default=1, view={"label":"Written Line", "format":utils.percent_format(2)}),
        # Aggregate limit input: for layers 1 to 10 excess pricing.
        "aggregate_limit_view" : hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Limit", "format": {"thousandSeparated": True, "mantissa": 0}}),

        # Added variable to record a bpi where the risk is case priced. Do not remove as used in tpi summary. 
        'bpi_case_priced': hx.Float(mode='input', default=None, optionality='optional', view={'label': 'BPI (Case Priced)', 'format': percent_format(1)}),
        # 'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
        'premium_label': hx.Str(mode='output'),
        # Used for rate change calcs
        'quoted_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
        'benchmark_premium_annualised': hx.Float(mode='output', async_input=["rarc_task"]),
    })

    cds.override_node_properties("cds/layers/brokerage", { "mode": "output", "async_input" : ["rarc_task"]}) # Output for standard KPIs tab. Needed due to difference whether using excess pricing or not. 
    cds.override_node_properties("cds/layers/status", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"]})
    cds.override_node_properties("cds/layers/section_reference", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"]})
    # Quoted premium - change to output as it is picking up quoted_premium from primary node and quoted_premium_input for excess layers
    cds.override_node_properties("cds/layers/quoted_premium", { "mode": "output", "async_input" : ["rarc_task","generate_email_task","generate_referral_email_task"] ,"view":{"label":"Quoted Premium"}})
    
    cds.override_node_properties("cds/layers/pflr_pre_uw_adj", { "view" : {"format":{"output": "percent", "mantissa": 1}}})
    cds.override_node_properties("cds/layers/currency", {"mode": "output", "async_input": ["rarc_task"]})
    cds.override_node_properties("cds/layers/aggregate_limit", {"mode" : "output", "async_input": ["rarc_task"]})
