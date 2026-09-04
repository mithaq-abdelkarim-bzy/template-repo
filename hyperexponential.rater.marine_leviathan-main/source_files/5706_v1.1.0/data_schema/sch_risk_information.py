import hx_data_schema as hx
import data_schema.sch_utilities as utils

def thousands_format(mantissa=0):
    return{"thousandSeparated": True, "mantissa":mantissa}


def percent_format(mantissa=0):
    return{"output": "percent", "mantissa":mantissa}


def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        # ~~~~~

        "yoa": hx.Int(mode="output", view={"label": "YOA", "format":{"thousandSeparated": False}}),
        "beazley_share": hx.Float(mode="input",  default=1, view={"label": "Beazley's share", "format":{"output": "percent", "mantissa":1}}),
        "brokerage": hx.Float(mode="input",  default=0.25,async_input=["rarc_task"],  view={"label": "Brokerage", "format":{"output": "percent", "mantissa":1}}),
        "policy_term": hx.Float(mode="output", async_input=["rarc_task"], view={"label": "Policy term (years)", "format": thousands_format(1)})
        

}),

    

 