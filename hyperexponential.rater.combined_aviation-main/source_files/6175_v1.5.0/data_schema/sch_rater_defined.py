import hx_data_schema as hx
from algorithms.data_schema.sch_rater_defined import * 

def sch_rater_defined(cds):

    ### --- GENERAL --- ###
    cds.extend_node_rater_defined("cds", cover_selection_dict)

    ### --- COVERAGES --- ####
    cds.extend_node_items("cds/layers/coverages", coverages_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/hull", hull_dict)
    cds.extend_node_rater_defined("cds/layers/coverages/liability", liability_dict)

    ### --- LAYERS --- ###
    cds.extend_node_rater_defined("cds/layers", layers_dict)

    ### --- OVERRIDES --- ###
    
