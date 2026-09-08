import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers
from algorithms.data_schema.sch_rater_defined import input_dict, claims_dict, expe_rating_summary_dict

def sch_experience_rating(cds):

    cds.extend_node_rater_defined("cds/experience_rating", {
        **input_dict,
        "show_experience_rating": hx.Bool(mode="output"),
        "claims": hx.List(mode="input", default_element_count=10, async_output=[{"task": task, "reset": False} for task in ["show_airlines_task", "show_ga_task", "start_renewal_task"]], children=claims_dict),
        "hull": hx.Structure(view={"label": "Hull"}, children=expe_rating_summary_dict),
        "liability": hx.Structure(view={"label": "Liability"}, children=expe_rating_summary_dict)
        }
    )
    cds.override_node_properties("cds/experience_rating/claims_available", {"async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/experience_rating/claims_fgu", {"async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]})
    cds.override_node_properties("cds/experience_rating/claims_net_of_deductible", {"async_input": ["rarc_task"], "async_output": [{"task": "start_renewal_task", "reset": False}]})