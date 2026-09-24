import hx_data_schema as hx
import data_schema.sch_utilities as utils
from datetime import date

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {
        # Account Details 
        "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                
        # Broker Details
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "brokerage": hx.Float(mode="input", async_input=["rarc_task"], default=0.25, view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),        

        # currency label
        "currency_label": hx.Str(mode="output"),

        # Currency        
        "ccy": hx.Str(mode="input", async_input=["rarc_task"], default="USD", optionality="optional", options_column="Currency code", options_table="tbl_ccy", view={"label": "Source Currency"}),
        "ccy_factor": hx.Float(mode="output", view={"label": "Currency Factor"}),
        "expiring_ccy_factor": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Expiring Currency Factor"}),            

        # term adjustment
        "term_adj_factor": hx.Float(mode="output", view={"label": "Term Adjustment Factor"}),

        "expiring_riskinfo":hx.Structure(children={
            # Account Details 
            "database_id": hx.Int(mode="output", view={"label": "Database ID", "format": utils.integer_format(0)}),
                                    
            # Broker Details
            "broker_contact": hx.Str(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Broker Contact"}),
            "brokerage": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Brokerage", "format": {"output": "percent", "mantissa": 1}}),            

            # currency label
            "currency_label": hx.Str(mode="output"),

            # Currency
            "ccy": hx.Str(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Source Currency"}),
            "ccy_factor": hx.Float(mode="output", view={"label": "Currency Factor"}),
            "expiring_ccy_factor": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Expiring Currency Factor"}),            

            # term adjustment
            "term_adj_factor": hx.Float(mode="output", async_output=["expiring_policy_fetch_task"], view={"label": "Term Adjustment Factor"}),
        }),

    })    

    # Override currency dropdown links
    cds.override_node_properties('cds/currencies/source_currency', {'mode':"output"})    

    # Override underwriter dropdown links
    cds.override_node_properties('cds/standard_fields/underwriter', {'options_table': "lst_underwriters", 'options_column': "Underwriters"})

    # Set to output
    cds.override_node_properties('cds/standard_fields/benchmark_class', {'mode': "output"})

    # insured name - set to async task
    cds.override_node_properties('cds/standard_fields/insured_name', {"async_input": ["start_renewal_task"]})

    # is_renewal - set to async output
    cds.override_node_properties('cds/standard_fields/is_renewal', {"async_output": ["start_renewal_task"]})

    # inception_date - set to async input for rarc
    cds.override_node_properties('cds/standard_fields/inception_date', {"async_input": ["rarc_task"]})

    # expiry_date - set to async output
    cds.override_node_properties('cds/standard_fields/expiry_date', {"async_input": ["rarc_task"]})
    
    
