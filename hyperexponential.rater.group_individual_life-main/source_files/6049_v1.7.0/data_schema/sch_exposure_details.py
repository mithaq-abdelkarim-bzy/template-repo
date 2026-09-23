import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.data_schema.sch_rater_defined import exposure_dict


def sch_exposure_details(cds):
    
    # For aggregate exposure e.g. total revenue, sum insured etc. please add to the aggregate exposures node
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        
        # PLACEHOLDER value used in experience rating, the experience rating should connect to the total exposure value of the model
        "exposure": hx.Float(mode="input", default=0, view={"label": "Exposure", "format": thousands_format(0)}),
        
    })

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", exposure_dict)