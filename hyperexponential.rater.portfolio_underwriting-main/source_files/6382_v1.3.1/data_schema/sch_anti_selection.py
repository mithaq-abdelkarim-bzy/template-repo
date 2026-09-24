# Note - sch_uncertainty and sch_anti_selection follow very similar formats - when updating, consider the other
import hx_data_schema as hx
from data_schema.sch_utilities import percent_format, create_node
import algorithms.rate_constants as constants

def generate_matrix_common_nodes(label, options=[], default=None, is_overall=False):
    nodes = {
        "guideline_min":    create_node("Guideline Min",    "output",   format=percent_format(2), group="Anti-Selection Charge"),
        "guideline_max":    create_node("Guideline Max",    "output",   format=percent_format(2), group="Anti-Selection Charge"),
        "suggested":        create_node("Suggested",        "output",   format=percent_format(2), group="Anti-Selection Charge"),
        "final_selected":   create_node("Final Selected",   "override", format=percent_format(2), group="Anti-Selection Charge"),
        "comments":         create_node("Comments", type='str', async_output=["start_renewal_task"]),
        "guidelines":       hx.Str(mode='output')        
    }
    if not is_overall:
        nodes['selection'] =create_node("Selection", type='str', options=options, default=default,async_output=["start_renewal_task"])
    return hx.Structure(    view={"label": label},        children=nodes    )

def generate_matrix():
    nodes = {
            "baseline":                 generate_matrix_common_nodes("Baseline",                                  "table_antiselection_1/Grade", "Standard Contract"),
            "competing_portfolio":      generate_matrix_common_nodes("Competing portfolio",                       "table_antiselection_2/Grade", "MGA - With competing portfolio"),
            "delegation_scope":         generate_matrix_common_nodes("Scope and degree of delegation",            "table_antiselection_3/Grade", "Average"),
            "quantity_quality":         generate_matrix_common_nodes("Data quality / quantity",                   "table_antiselection_4/Grade", "Average"),
            "cover_holder_alignment":   generate_matrix_common_nodes("Alignment of coverholder's terms with BST", "table_antiselection_5/Grade", "Average"),
            "participation":            generate_matrix_common_nodes("Differential participation",                "table_antiselection_6/Grade", "Varying participation"),
            "overall_selected":         generate_matrix_common_nodes("Overall selected", is_overall=True)}
    return nodes

def generate_applied_charge_summary_nodes(is_model_weighting=False):
    common_nodes = {
        "own_performance":      create_node("Own Performance",      "output", format=percent_format(0)),
        "lloyds_performance":   create_node("Lloyds Performance",   "output", format=percent_format(0)),
        "beazley_performance":  create_node("Beazley Performance",  "output", format=percent_format(0)),
        "business_plan":        create_node("Business Plan",        "output", format=percent_format(0)),
        "case_pricing":         create_node("Case Pricing",         "output", format=percent_format(0)),
        "pricing_2623_623":     create_node("2623/623 Pricing",     "output", format=percent_format(0)),
    }
    if not is_model_weighting:
        common_nodes["selected_lob"]            = create_node("Selected Lob",           "output",   type='str')
        common_nodes["anti_selection_charge"]   = create_node("Anti-Selection Charge",  "override", async_input=["sync_lob_lists_task"], format=percent_format(2))
        common_nodes["is_row_visible"]          = hx.Bool(                         mode="output")
    return common_nodes

def sch_anti_selection(cds):
    cds.extend_node_rater_defined("cds",
        {"anti_selection": hx.Structure(children={
            "charge_required": hx.Bool(mode='input', default=True, view={'label': 'Anti-Selection Charge Required?'}, async_output=["fetch_bbt_task", "start_renewal_task"]),
            "matrix":          hx.Structure(children={  **generate_matrix()}),
            "applied_charge":  hx.Structure(children={ 
                "model_weighting": hx.Structure( view={"label": "Model Weighting"},  
                                                 children=generate_applied_charge_summary_nodes(is_model_weighting=True)),
                "table":          hx.List(       mode="input",   
                                                 async_output=[{"task": "sync_lob_lists_task", "reset": False}],
                                                 default_element_count=constants.DEFAULT_NUM_LOB,
                                                 children=generate_applied_charge_summary_nodes())})})})