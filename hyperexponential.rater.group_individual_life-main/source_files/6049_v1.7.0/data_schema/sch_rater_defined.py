import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import * 

def sch_rater_defined(cds):

    ### --- GENERAL --- ###
    cds.extend_node_rater_defined("cds", cover_selection_dict)

    ### --- COVERAGES --- ####
    cds.extend_node_items("cds/layers/coverages", coverages_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/death", death_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/additional_death", additional_death_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/terminal_illness", terminal_illness_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/critical_illness", critical_illness_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/repat_exp", repat_exp_dict)

    ### --- LAYERS --- ###
    cds.extend_node_rater_defined("cds/layers", layers_dict)

    ### --- OVERRIDES --- ###

    cds.override_node_properties("cds/exposure/granular", {"view": {"label": None}})
    
    # Coverage
    hxd_cvg_struct = ["death", "additional_death", "terminal_illness", "critical_illness", "repat_exp"]

    for cvg in hxd_cvg_struct:
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/model_premium", {
            "view": {"label": "U/W Adj modelled Premium"},
        })
        cds.override_node_properties(f"cds/layers/coverages/{cvg}/quoted_premium", {
            "mode": "output",
            "view": {"label": "Commercially Achieved Premium"},
        })

    cds.override_node_properties("cds/layers/coverages/repat_exp/limit", {
            "optionality": "required", "default": 0, "async_input": ["rarc_task"], "async_output": ["start_renewal_task"], "view": {"label": "Limit per person"}
        })

