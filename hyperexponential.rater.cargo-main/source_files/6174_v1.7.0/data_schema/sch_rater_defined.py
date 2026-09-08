import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import *

def sch_rater_defined(cds):
    cds.extend_node_items("cds/layers/coverages", coverages_dict)
    cds.extend_node_rater_defined("cds", cover_selection_dict)
    cds.extend_node_rater_defined("cds", policy_info_dict)
    cds.extend_node_rater_defined("cds/layers", layers_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/cargo_transit", cargo_transit_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/cargo_storage", cargo_storage_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/specie_transit", specie_transit_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/specie_storage", specie_storage_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/conloss_transit", conloss_transit_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/conloss", conloss_dict)
    # add cargo_cyber which is to mirror cargo
    cds.extend_node_rater_defined("cds/layers/coverages/cargo_cyber_transit", cargo_cyber_transit_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/cargo_cyber_storage", cargo_cyber_storage_dict)
    #Create nodes for Cargo Cyber add on for Cargo Main Coverage - This is as at layer aggregate level
    cds.extend_node_rater_defined("cds/layers/coverages/cargo_cyber_addon", layers_dict_cargo_cyber)
    cds.override_node_properties("cds/layers/coverages/cargo_cyber_addon/brokerage",  {"default": 0, "view": {"label": "Deductions"},"async_output": [{"task":"load_cargo_input", "reset": False}]})
    cds.override_node_properties("cds/layers/coverages/cargo_cyber_addon/written_line", {"default": 0,"async_output": [{"task":"load_cargo_input", "reset": False}]})


