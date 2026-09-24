import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

# The following code set out examples of how to use the built in cds functions. 
# Please remove these example nodes for live models. 

def sch_example_code(cds):
        
    # Extending cds nodes
    '''
    NOTE This function extends the cds to allow for rater defined fields. In this example we have extended 
    the root 'cds' although it will also extend the following nodes:
    {'cds/experience_rating', 'cds/layers', 'cds/experience_rating/claims', 'cds', 'cds/exposure/granular', 
    'cds/layers/rate_change', 'cds/exposure/aggregate', 'cds/layers/coverages'}.
    '''
    cds.extend_node_rater_defined("cds", {
        "example_structure": hx.Structure(view={"label": "Example Code"}, children={
            "example_child1": hx.Float(mode="input", default=0, view={"label": "Example Child 1"}),
            "example_child2": hx.Float(mode="input", default=0, view={"label": "Example Child 2"}),
        }),
    })

    # Adding coverages to the layers list. NOTE this code duplicates all the common fields from layer to each coverage.
    cds.extend_node_items("cds/layers/coverages", {
        "example_coverage_1": {"label": "Example Coverage 1"},
        "example_coverage_2": {"label": "Example Coverage 2"},
    })

    
    # Adding a rated-defined field to ALL coverages
    cds.extend_node_rater_defined("cds/layers/coverages", {
        "example_common_coverage_variable": hx.Float(mode="input", default=0, view={"label": "Common Coverage Variable"}),
    })

    # Adding a rated-defined field to a specifc coverage.
    cds.extend_node_rater_defined("cds/layers/coverages/example_coverage_1", {
        "example_specific_coverage_variable": hx.Float(mode="input", default=0, view={"label": "Common Coverage Variable"}),
    })
