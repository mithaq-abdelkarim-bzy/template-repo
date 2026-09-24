import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from libraries.common_data_schema.algorithms import parameter_tables_schema as params
import data_schema.sch_utilities as utils
from algorithms.rate_constants import max_layers, max_options
from data_schema.sch_rate_change import rarc_task_name

# For expiring nodes, change all the inputs/overrides to output so we can fetch expiring information
def sch_rating_summary(cds):
    cds.extend_node_rater_defined("cds", {
        # Retention Layer
        "retention": hx.Structure(view = {"label":"SIR"}),

        # Option selected
        "option_selected": hx.Float(mode="input", default=1, optionality="optional", options_data ="../options", options_field="option_label", async_input=["rarc_task"], view={"label": "Selected Option", "format": utils.thousands_format(0)}),                

        # flag for Beazley or carrier primary
        "carrier_primary": hx.Bool(mode="output"),

        # Flags for excess layers
        **excess_layers(layers=5),

        # Options for Primary Layer
        "options": hx.List(mode= "input", default_element_count = max_options, max_element_count=max_options, view = {"label":"Options"}, children={
            "expiring_option": hx.Int(mode="output", async_output=["rarc_task"]),
            "ilf_type": hx.Str(mode="input", async_input=["rarc_task"], default="Light", options=["Light", "Heavy", "BUSA A&E"], view={"label": "ILF Type"}),
            "limit": hx.Float(mode="input", async_input=["rarc_task"], default=1_000_000, view={"label": "Limit", "format": utils.thousands_format(0)}),
            "number_of_reinstatements": hx.Float(mode="output", view={"label": "Aggregate-Individual Limit Ratio", "format": {"mantissa": 2}}),
            "aggregate_limit": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Aggregate Limit", "format": utils.thousands_format(0)}),
            "deductible": hx.Float(mode="input", async_input=["rarc_task"], default=0, view={"label": "Deductible", "format": utils.thousands_format(0)}),
            "guideline_deductible": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Guideline Deductible", "format": utils.thousands_format(0)}),            
            "written_line_view": hx.Float(mode="input", async_input=["rarc_task"], default=1, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),
            "brokerage_primary": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Brokerage", "format": percent_format(1)}),
            "benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": utils.thousands_format(0)}),
            "benchmark_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (Pre-UW Adjustment)", "format": utils.thousands_format(0)}),
            "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium", "format": utils.thousands_format(0)}),            
            "technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Technical Premium (Pre-UW Adjustment)", "format": utils.thousands_format(0)}),            
            "technical_premium_net": hx.Float(mode="output", view={"label": "Net Technical Premium", "format": utils.thousands_format(0)}),                        
            "beazley_primary": hx.Bool(mode="input", default=True, view={"label": "Beazley Primary?"}),
            "carrier": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Carrier"}),
            "carrier_premium": hx.Float(mode="input", default=0, optionality="optional" , view={"label": "Gross Quoted Premium (Carrier)", "format": utils.thousands_format(0)}),
            "quoted_ilf_curve": hx.Float(mode="output", view={"label": "Quoted ILF Curve"}),
            "quoted_premium": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium", "format": utils.thousands_format(0)}),            
            "status": hx.Str(mode="output", view={"label": "Status"}),
            "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
            "bpi": hx.Float(mode="output", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),
            "bpi_pre_uw_adj": hx.Float(mode="output", view={"label": "BPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "tpi": hx.Float(mode="output", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),
            "tpi_pre_uw_adj": hx.Float(mode="output", view={"label": "TPI (Pre-UW Adjustment)", "format": {"output": "percent", "mantissa": 1}}),
            "pflr": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "pflr_att": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Att)", "format": {"output": "percent", "mantissa": 1}}),
            "roc": hx.Float(mode="output", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),
            "uw_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Commentary"}),            
            "ilf_factor": hx.Float(mode="output", view={"label": "ILF Factor"}),
            "reinstatements_factor": hx.Float(mode="output", view={"label": "Reinstatements Factor"}),
            "deductible_factor": hx.Float(mode="output", view={"label": "Deductible Factor"}),
            "expected_loss_cost": hx.Float(mode="output", view={"label": "Expected Loss Cost", "format": utils.thousands_format(0)}),
            "expected_loss_cost_pre_uw_adj": hx.Float(mode="output", view={"label": "Expected Loss Cost (Pre-UW Adjustment)", "format": utils.thousands_format(0)}),
            "quoted_premium_net": hx.Float(mode="output", view={"label": "Net Quoted Premium", "format": utils.thousands_format(0)}),        
            "model_premium": hx.Float(mode="output", view={"label": "Gross Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "model_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Gross Model Premium (Pre-UW Adjustment)", "format": {"thousandSeparated": True, "mantissa": 0}}),                        
            "option_label": hx.Float(mode="output", view={"label": "Option Label", "format": utils.thousands_format(0)}),
            "minimum_premium": hx.Float(mode="output", view={"label": "Gross Minimum Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "minimum_premium_flag": hx.Str(mode="output", view={"label": "Minimum Premium used in \n Benchmark or Technical Premium?", "format": utils.thousands_format(0)}),
            "minimum_deductible": hx.Float(mode="output", view={"label": "Minimum Deductible", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "minimum_deductible_flag": hx.Str(mode="output", view={"label": "Minimum Deductible used in \n Guideline Deductible?", "format": utils.thousands_format(0)}),

            # Options for excess layers
            **excess_options(layers=5),            
        
            # Set these up because of different inputs and output modes between primary and excess layers, but want to show on same view column
            # aggregate_limit_view = limit in primary layer (this is different to aggregate_limit in primary layer which applies reinstatements)
            "aggregate_limit_view": hx.Float(mode="output", view={"label": "Aggregate Limit", "format": utils.thousands_format(0)}),
            "quoted_premium_view": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": utils.thousands_format(0)}),                        
            "status_view": hx.Str(mode="input", optionality="optional", options=params.status.column("Status"), default=None, view={"label": "Status"}),
            "section_reference_view": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference"}),

            # For case pricing
            "technical_premium_case_priced": hx.Float(mode="output", view={"label": "Gross Technical Premium", "format": utils.thousands_format(0)}),            
            "benchmark_premium_case_priced": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": utils.thousands_format(0)}),            
            "bpi_case_priced": hx.Float(mode="input", default=0, optionality="optional", view={"label": "BPI (Case Priced)",  "format": {"output": "percent", "mantissa": 1}}),
            "bpi_case_priced_view": hx.Float(mode="output", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),            
            "tpi_case_priced": hx.Float(mode="output", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),     
            "pflr_case_priced": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),  
            "roc_case_priced": hx.Float(mode="output", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),  
            "brokerage_view": hx.Float(mode="output", view={"label": "Brokerage (excl. PC's)", "format": {"output": "percent", "mantissa": 1}}),      
            "brokerage": hx.Float(mode="input", default=0, view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),    
            "written_line_case_priced": hx.Float(mode="output", view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),  
            "pflr_cat": hx.Float(mode="output", optionality="optional", view={"label": "Priced-for Loss Ratio (Cat)", "format": {"output": "percent", "mantissa": 1}}),
            'pflr_pre_uw_adj': hx.Float(mode='output', optionality='optional', view={'label': 'Priced-for Loss Ratio (Pre-UW Adj.)', 'format': {'output': 'percent', 'mantissa': 1}}),
            "uw_adj_impact": hx.Float(mode="output", optionality="optional", view={"label": "Impact of Underwriting Adjustments", "format": {"output": "percent", "mantissa": 1}}),
        }),
        # Primary Layer - this is purely used in view page because cannot combine two lists together        
        "primary": hx.Structure(view = {"label":"Primary"}, children={                        
            "limit": hx.Float(mode="output", view={"label": "Limit", "format": utils.thousands_format(0)}),
            "aggregate_limit_view": hx.Float(mode="output", view={"label": "Aggregate Limit", "format": utils.thousands_format(0)}),
            "brokerage": hx.Float(mode="output", view={"label": "Brokerage", "format": percent_format(1)}),
            "model_premium": hx.Float(mode="output", view={"label": "Gross Model Premium", "format": {"thousandSeparated": True, "mantissa": 0}}),
            "benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": utils.thousands_format(0)}),            
            "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium", "format": utils.thousands_format(0)}),                                   
            "carrier": hx.Str(mode="output", optionality="optional", view={"label": "Carrier"}),
            "carrier_premium": hx.Float(mode="output", optionality="optional", view={"label": "Gross Quoted Premium (Carrier)", "format": utils.thousands_format(0)}),                        
            "quoted_premium": hx.Float(mode="output", view={"label": "Gross Quoted Premium", "format": utils.thousands_format(0)}),
            "benchmark_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Benchmark Premium (100%)", "format": utils.thousands_format(0)}),
            "technical_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Technical Premium (100%)", "format": utils.thousands_format(0)}),
            "quoted_premium_100": hx.Float(mode="output", optionality="optional", view={"label": "Gross Quoted Premium (100%)", "format": utils.thousands_format(0)}),
            "status_view": hx.Str(mode="input", async_output=["start_renewal_task"], optionality="optional", options=params.status.column("Status"), default=None, view={"label": "Status"}),
            "section_reference_view": hx.Str(mode="input", async_output=["start_renewal_task"], default=None, optionality="optional", view={"label": "Section Reference", "info": "Enter Section Reference for Open Market or Binder Reference for Binders"}),
            "bpi": hx.Float(mode="output", view={"label": "BPI", "format": {"output": "percent", "mantissa": 1}}),            
            "tpi": hx.Float(mode="output", view={"label": "TPI", "format": {"output": "percent", "mantissa": 1}}),            
            "pflr": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio", "format": {"output": "percent", "mantissa": 1}}),
            "pflr_att": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio (Att)", "format": {"output": "percent", "mantissa": 1}}),
            "roc": hx.Float(mode="output", view={"label": "Return on Capital", "format": {"output": "percent", "mantissa": 1}}),                                           
        }),

        # Excess Layer considerations
        "xslayer_considerations": hx.Str(mode="output", view={"label": "Excess Layer Considerations"}),
    }),

    # Separate out SIR, primary and excess layer because of different inputs/outputs
    # Excess Layer
    cds.extend_node_rater_defined("cds/layers", {
        "layer_label": hx.Str(mode="output", view={"label": "Layer Label"}),
        "ilf_curve": hx.Float(mode="output", view={"label": "ILF Curve", "format": {"output": "percent", "mantissa": 1}}),
        "model_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Model Premium (Pre-UW Adjustment)", "format": utils.thousands_format(0)}),
        "carrier": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Carrier"}),
        "carrier_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Quoted Premium (Carrier)", "format": utils.thousands_format(0)}),
        "quoted_ilf_curve": hx.Float(mode="output", view={"label": "Quoted ILF Curve", "format": {"output": "percent", "mantissa": 1}}),
        "cum_attachment": hx.Float(mode="output", view={"label": "Attachment Point", "format": utils.thousands_format(0)}),
        "cum_benchmark_premium": hx.Float(mode="output", view={"label": "Cumulative Benchmark Premium (Excess)", "format": utils.thousands_format(0)}),        
        "cum_model_premium": hx.Float(mode="output", view={"label": "Cumulative Model Premium (Excess)", "format": utils.thousands_format(0)}),
        "cum_model_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Cumulative Model Premium (Excess, Pre-UW Adjustment)", "format": utils.thousands_format(0)}),
        "cum_technical_premium": hx.Float(mode="output", view={"label": "Cumulative Technical Premium (Excess)", "format": utils.thousands_format(0)}),
        "cum_technical_premium_pre_uw_adj": hx.Float(mode="output", view={"label": "Cumulative Technical Premium (Excess, Pre-UW Adjustment)", "format": utils.thousands_format(0)}),
        "cum_carrier_premium": hx.Float(mode="output", view={"label": "Cumulative Carrier Premium (Excess)", "format": utils.thousands_format(0)}),
        "excess_flag": hx.Bool(mode="output", view={"label": "On View Excess Page?"}),        
        
        # Set these up because of different inputs and output modes between primary and excess layers, but want to show on same view column
        "aggregate_limit_view": hx.Float(mode="input", async_input=["rarc_task"], default_index=0, options_table="lst_excessilfs", options_column="Excess Limit", view={"label": "Aggregate Limit", "format": utils.thousands_format(0)}),
        "quoted_premium_view": hx.Float(mode="input", default=0, view={"label": "Quoted Premium", "format": utils.thousands_format(0)}),        
        "status_view": hx.Str(mode="input", async_output=["start_renewal_task"], default=None, optionality="optional", options=["Assessment Pending", "Rating", "Quoted", "Bound", "Post Bind Complete", "Declined", "Not Taken Up"], view={"label": "Status"}),
        "section_reference_view": hx.Str(mode="input", async_output=["start_renewal_task"], default=None, optionality="optional", view={"label": "Section Reference", "info": "Enter Section Reference for Open Market or Binder Reference for Binders"}),
        "written_line_view": hx.Float(mode="input", default=1, view={"label": "Written Line", "format": {"output": "percent", "mantissa": 1}}),

        # USD
        "model_premium_usd": hx.Float(mode="output", view={"label": "Gross Model Premium (USD)", "format": utils.thousands_format(0)}),
        "technical_premium_usd": hx.Float(mode="output", view={"label": "Gross Technical Premium (USD)", "format": utils.thousands_format(0)}),
        "benchmark_premium_usd": hx.Float(mode="output", view={"label": "Gross Benchmark Premium (USD)", "format": utils.thousands_format(0)}),
        "expected_loss_cost_usd": hx.Float(mode="output", view={"label": "Expected Loss Cost (USD)", "format": utils.thousands_format(0)}),

        }),    

    # Override values
    cds.override_node_properties("cds/layers", {
        "default_element_count": max_layers,
        "max_element_count": max_layers
        })

    # Aggregate limit - change to output as it is picking up aggregate_limit_view in primary and excess layer
    cds.override_node_properties("cds/layers/aggregate_limit", {
        "mode": "output"        
        })

    # Quoted premium - change to output as it is picking up quoted_premium_view in primary and excess layer
    cds.override_node_properties("cds/layers/quoted_premium", {
        "mode": "output",
        "async_input" : ["rarc_task"]
        })

    # Benchmark premium - for rarc calculation
    cds.override_node_properties("cds/layers/benchmark_premium", {
        "async_input" : ["rarc_task"]
        # "async_output": ["expiring_policy_fetch_task"]        
        })
        
    # Brokerage - change to output as brokerage across all layers will be set to the policy level brokerage
    cds.override_node_properties("cds/layers/brokerage", {
        "mode": "output",
        "async_input": [rarc_task_name]     
        })
    
    # Status - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/status", {
        "mode": "output"        
        })

    # Section reference - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/section_reference", {
        "mode": "output"        
        })

    # is primary or excess - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/is_primary_excess", {
        "mode": "output"        
        })

    # written line - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/written_line", {
        "mode": "output" 
        })

    # limit - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/limit", {
        "mode": "output",
        "async_input": [rarc_task_name]
        })

    # excess - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/excess", {
        "mode": "output",
        "async_input": [rarc_task_name]
        })

    # deductible - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/deductible", {
        "mode": "output",
        "async_input": [rarc_task_name]
        })

    # currency - change to output due to differences in mode between primary and excess layers, and where we want to display the primary layer variable as 'read only' in the excess layer table
    cds.override_node_properties("cds/layers/currency", {
        "mode": "output",
        "async_input": [rarc_task_name]
        })

def excess_layers(layers):
    return {
        **{f"add_excess_{layer}": hx.Bool(mode="input", default=False, optionality="required", view={"label": "Add Excess Layer"}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_beazley_participation": hx.Bool(mode="output") for layer in range(1, layers+1)},
    }

def excess_options(layers):
    return {
        # Excess nodes 
        **{f"excess_{layer}_beazley_participation": hx.Bool(mode="input", default=False, view={"label": "Beazley Participation?"}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_brokerage": hx.Float(mode="override", async_input=["rarc_task"], view={"label": "Brokerage", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_excess": hx.Float(mode="override", async_input=["rarc_task"]) for layer in range(1, layers+1)},
        **{f"excess_{layer}_cum_attachment": hx.Float(mode="output", view={"label": "Attachment", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_limit": hx.Float(mode="input", default=1_000_000, async_input=["rarc_task"], view={"label": "Limit", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_carrier_premium": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium (Carrier)", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_quoted_premium": hx.Float(mode="input", default=0, view={"label": "Gross Quoted Premium", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium", "format": thousands_format(0)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_ilf_curve": hx.Float(mode="output", view={"label": "ILF Curve", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_bpi": hx.Float(mode="output", view={"label": "BPI", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_tpi": hx.Float(mode="output", view={"label": "TPI", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_pflr": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_roc": hx.Float(mode="output", view={"label": "Return on Capital", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_carrier_bpi": hx.Float(mode="output", view={"label": "BPI (Carrier)", "format": percent_format(1)}) for layer in range(1, layers+1)},
        **{f"excess_{layer}_carrier_tpi": hx.Float(mode="output", view={"label": "TPI (Carrier)", "format": percent_format(1)}) for layer in range(1, layers+1)},
    }