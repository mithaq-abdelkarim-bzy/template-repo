# Note - sch_uncertainty and sch_anti_selection follow very similar formats - when updating, consider the other
import hx_data_schema as hx
from data_schema.sch_utilities import percent_format, create_node
import algorithms.rate_constants as constants

def generate_matrix_common_nodes(label, options=[], default=None, has_selection=True):
    nodes = {
        "guideline_min":    create_node("Guideline Min",    "output",   format=percent_format(2), group="Uncertainty Load"),
        "guideline_max":    create_node("Guideline Max",    "output",   format=percent_format(2), group="Uncertainty Load"),
        "suggested":        create_node("Suggested",        "output",   format=percent_format(2), group="Uncertainty Load"),
        "final_selected":   create_node("Final Selected",   "override", format=percent_format(2), group="Uncertainty Load"),
        "comments":         create_node("Comments", type='str',async_output=["start_renewal_task"]),
        "guidelines":       hx.Str(mode='output'),
    }
    if has_selection:
        nodes['selection'] = create_node("Selection", type='str', options=options, default=default,async_output=["start_renewal_task"])
    return hx.Structure( view={"label": label},  children=nodes  )

def generate_matrix():
    nodes = {   "quantity":                 generate_matrix_common_nodes("Data Quantity",                   "table_uncertainty_1/Grade", "Average"),
                "quality":                  generate_matrix_common_nodes("Data Quality",                    "table_uncertainty_2/Grade", "Average"),
                "new_or_existing_facility": generate_matrix_common_nodes("New or Existing Facility",        "table_uncertainty_3/Grade", "New Business - Established"),
                "perf_volatility":          generate_matrix_common_nodes("Performance Volatility",          "table_uncertainty_4/Grade", "Low"),
                "reliance_on_ext_modelling":generate_matrix_common_nodes("Reliance on External Modelling",  "table_uncertainty_5/Grade", "Less than 50%"),
                "add_subjectivity":         generate_matrix_common_nodes("Additional Subjectivity",         has_selection=False),
                "perf_discount":            generate_matrix_common_nodes("Performance Discount (Renewals)", has_selection=False),
                "overall_selected":         generate_matrix_common_nodes("Overall selected",                has_selection=False)   }
    return nodes

def generate_applied_charge_summary_nodes(is_model_weighting=False):
    common_nodes = {
        "own_performance":      create_node("Own Performance",      "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
        "lloyds_performance":   create_node("Lloyds Performance",   "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
        "beazley_performance":  create_node("Beazley Performance",  "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
        "business_plan":        create_node("Business Plan",        "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
        "case_pricing":         create_node("Case Pricing",         "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
        "pricing_2623_623":     create_node("2623/623 Pricing",     "output", format=percent_format(0), async_input=["sync_lob_lists_task"]),
    }
    if not is_model_weighting:
        common_nodes["selected_lob"]   = create_node("Selected Lob",     "output",   type='str')
        common_nodes["load"]           = create_node("Uncertainty Load", "override",  format=percent_format(2))
        common_nodes["is_row_visible"] = hx.Bool(mode="output")
    return common_nodes

def sch_uncertainty(cds):
    cds.extend_node_rater_defined("cds",
        {"uncertainty": hx.Structure(children={
            "charge_required":  hx.Bool(mode='input', default=True, view={'label': 'Uncertainty Loading Required?'}, async_output=["fetch_bbt_task", "start_renewal_task"]),
            "matrix":           hx.Structure(children={ **generate_matrix()}),
            "applied_charge":   hx.Structure(children={
                "model_weighting":  hx.Structure( view={"label": "Model Weighting"},
                                                  children=generate_applied_charge_summary_nodes(is_model_weighting=True)),
                "table":            hx.List(      mode="input",
                                                  default_element_count=constants.DEFAULT_NUM_LOB,
                                                  async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                  children=generate_applied_charge_summary_nodes())})})})