import hx_data_schema as hx
from data_schema.sch_utilities import *

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", { 
        # If needed
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": integer_format(0)}),
        "rater": hx.Str(mode="input", default="Group", async_output="start_renewal_task", options=["Group", "Individual"], view={"label": "Group or Individual Life?"}),
        "is_group": hx.Bool(mode="output"),
        "is_individual": hx.Bool(mode="output"),
        
        # Additional policy info
        "policy_info": hx.Structure(children={
            "application_date": hx.Date(mode="input", default="2000-01-01", async_output=["start_renewal_task"], view={"label": "Application Date"}),
            "broker_contact": hx.Str(mode="input", default="", async_output=["start_renewal_task"], view={"label": "Broker Contact"}),
            "direct_ri": hx.Str(mode="input", default="Direct", async_output=["start_renewal_task"], options=["Direct", "Reinsurance"], view={"label": "Direct or RI?"}),
            "has_profit_commission": hx.Bool(mode="input", default=False, async_input=["simulate_years_task","rarc_task"], async_output=["start_renewal_task"], view={"label": "PC?"}),
            "pc_to_gross": hx.Str(mode="input", default="Gross", async_output=["start_renewal_task"], options=["Gross", "Net"] , view={"label": "Applies to G/N premium", "info": "Net = Net of commission\nGross = Gross premium"}),
            "profit_commission": hx.Float(mode="input", default=0, async_input=["simulate_years_task"], async_output=["start_renewal_task"], validation={"min_value": 0, "max_value": 1}, view={"label": "% PC", "format": percent_format(1)}),
            "pc_expenses": hx.Float(mode="input", default=0, async_input=["simulate_years_task"], async_output=["start_renewal_task"], validation={"min_value": 0, "max_value": 1}, view={"label": "PC Expenses", "format": percent_format(1)}),
            "pc_deficit": hx.Float(mode="input", default=0, async_input=["simulate_years_task"], async_output=["start_renewal_task"], validation={"min_value": 0}, view={"label": "PC Deficit", "format": thousands_format()}),
            "has_no_claims_bonus": hx.Bool(mode="input", async_input=["simulate_years_task","rarc_task"], async_output=["start_renewal_task"], default=False,  view={"label": "NCB?"}),
            "ncb_pct": hx.Float(mode="input", default=0, async_input=["simulate_years_task"], async_output=["start_renewal_task"], validation={"min_value": 0, "max_value": 1}, view={"label": "% Bonus", "format": percent_format(1)}),
            "ncb_to_gross": hx.Str(mode="input", default="Gross", async_output=["start_renewal_task"], options=["Gross", "Net"], view={"label": "Applies to G/N premium", "info": "Net = Net of commission\nGross = Gross premium"}),
        })

    })

    # Update underwriters variable to link to dropdown
    cds.override_node_properties("cds/standard_fields/underwriter", {"async_output": ["start_renewal_task"], "options_table": "table_input_underwriters", "options_column": "underwriter"})

    # Override properties
    cds.override_node_properties("cds/standard_fields/insured_name", {"async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/standard_fields/broker", {"async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/standard_fields/is_renewal", {"async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/standard_fields/rating_methodology", {"async_output": ["start_renewal_task"]})

    cds.override_node_properties("cds/currencies/source_currency", {"default": "USD", "async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/layers/brokerage", {
        "optionality": "required", "default": 0, "view": {"format": percent_format(1)}, "validation": {"min_value": 0, "max_value": 1}, "async_input": ["rarc_task", "simulate_years_task"], "async_output": ["start_renewal_task"]
    })
    cds.override_node_properties("cds/layers/written_line", {"mode": "output"})
    cds.override_node_properties("cds/layers/aggregate_limit", {
        "async_input": ["simulate_years_task", "rarc_task"], "async_output": ["start_renewal_task"], "validation": {"min_value": 0}
    })
    cds.override_node_properties("cds/layers/aggregate_deductible", {
        "async_input": ["simulate_years_task", "rarc_task"], "async_output": ["start_renewal_task"], "validation": {"min_value": 0}
    })
    cds.override_node_properties("cds/layers/status", {"async_output": ["start_renewal_task"]})
    
    # Make BM class dependent on Direct/RI
    cds.override_node_properties(
        "cds/standard_fields/benchmark_class", {"mode": "output"}
    )

    #async input for simulate_year_task
    cds.override_node_properties("cds/layers/no_claim_prob", {
        "async_input": ["simulate_years_task"],  "validation": {"min_value": 0}
    })

    cds.override_node_properties("cds/layers/totals/total/quoted_premium", {
        "async_input": ["simulate_years_task", "rarc_task"], "validation": {"min_value": 0}
    })

    