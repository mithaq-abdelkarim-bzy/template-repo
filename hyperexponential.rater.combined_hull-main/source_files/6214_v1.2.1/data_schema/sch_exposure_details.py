import hx_data_schema as hx
import data_schema.sch_utilities as utils

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "exposure": hx.Float(mode="input", default=0, view={"label": "Exposure", "format": utils.thousands_format(0)}),
        
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", {        
        # Replace the below with your models exposures
        "example_granular_field1": hx.Float(mode="input", default=0, view={"label": "Example Granular Exposure Field 1", "format": utils.thousands_format(0)}),
        "example_granular_field2": hx.Float(mode="input", default=0, view={"label": "Example Granular Exposure Field 2", "format": utils.thousands_format(0)}),
    })

