# v0.5.0
### --- DEFINING THE NODES HERE SO THAT THEIR PROPERTIES ARE DYNAMICALLY ACCESSIBLE BY THE RATING ALGORITHM --- ###
import hx_data_schema as hx
from algorithms.data_schema.sch_utilities import thousands_format, percent_format, integer_format

### --- TRACK RATER USE OF COVERAGES AND FLEET --- ###
# NOTE: Set RARC_COVERAGE_USE to True if using coverages for Rate Adjusted Rate Change (RARC).
# This setting is stored in cds/rate_change/rarc_coverage_use and can be independent of model_state/coverage_use.
RARC_COVERAGE_USE = False 
# NOTE: Set RARC_INSURED_ASSET_USE to True if the Rate Change is calculated at an insured interest level (e.g., for aircraft, vessels, spacecrafts, etc.).
# This setting is stored in cds/rate_change/rarc_insured_asset_use and can be independent of model_state/insured_asset_use.
RARC_INSURED_ASSET_USE = False 


if RARC_COVERAGE_USE:
    ### --- DEFINE COVERAGES HERE --- ###
    # NOTE: provide coverage name and the label for the view
    coverages_dict={
        "example_coverage_1": {"label": "Example Coverage 1"},
        "example_coverage_2": {"label": "Example Coverage 2"},
    }

    COVERAGES_LIST = list(coverages_dict.keys())

    max_coverages= len(coverages_dict)
    
    example_coverage_generic_dict={
        "example_common_coverage_variable": hx.Float(mode="input", default=0, view={"label": "Common Coverage Variable"}),
    }
    example_coverage_1_specific_dict={
        "example_specific_coverage_variable": hx.Float(mode="input", default=0, view={"label": "Specific Coverage 1 Variable"}),
    }
    example_coverage_2_specific_dict={
        "example_specific_coverage_variable": hx.Float(mode="input", default=0, view={"label": "Specific Coverage 2 Variable"}),
    }

def sch_coverages_defined(cds):
    '''
    NOTE This function extends the cds to allow for rater defined fields. In this example we have extended 
    the root 'cds' although it will also extend the following nodes:
    {'cds/layers/coverages'}.
    '''

    ### --- Adding coverages to the list of layers --- ####
    # NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_items("cds/layers/coverages", {**coverages_dict})

    ### --- Adding rated-defined field to ALL coverages --- ####
    cds.extend_node_rater_defined("cds/layers/coverages", {**example_coverage_generic_dict})

    ### --- Adding a rated-defined field to a specifc coverage --- #### 
    cds.extend_node_rater_defined("cds/layers/coverages/example_coverage_1", {**example_coverage_1_specific_dict})
    cds.extend_node_rater_defined("cds/layers/coverages/example_coverage_2", {**example_coverage_2_specific_dict})
