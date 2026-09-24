# v0.5.0
import hx_data_schema as hx
import data_schema.sch_utilities as utils

def sch_risk_information(cds):
    cds.extend_node_rater_defined("cds", {                                
        # Do not remove
        "policy_option_id": hx.Int(mode="output", view={"label": "Policy Option ID", "format": utils.integer_format(0)}),
        "broker_contact": hx.Str(mode="input", default="", view={"label": "Broker Contact"}),
        "case_pricing_analysis_location": hx.Str(mode="input", optionality="optional", default=None, view={"label": "Case Pricing Analysis Filepath"}),
        "profession": hx.Str(mode="input", options=["Lawyers", "Architects and Engineers", "Contractors"], async_input=["run_simulation_task"], optionality="optional", default=None, view={"label": "Profession"}),  
        "lawyers_num_attorneys_full": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "No. of Attorneys (Full)"}),
        "lawyers_num_attorneys_fte": hx.Float(mode="input", async_input=["rarc_task"], default=None, optionality="optional", view={"label": "No. of Attorneys (FTE)"}),
        "retro_date": hx.Date(mode="input", optionality="optional", async_input=["run_simulation_task", "rarc_task"], default=None, view={"label": "Retro Date"}),
        "risk_comments": hx.Str(mode="input", optionality="optional", default=None, view={"label":"Comments"}),
        "profession_lawyers_bool": hx.Bool(mode="output"),
        "profession_lawyers_bool_not": hx.Bool(mode="output"),
        "profession_AE_bool": hx.Bool(mode="output"),
        "profession_contractors_bool": hx.Bool(mode="output")
        # ~~~~~
    })

    cds.override_node_properties("cds/standard_fields/benchmark_class", {"options":["Large Client Professional"]})
    

 