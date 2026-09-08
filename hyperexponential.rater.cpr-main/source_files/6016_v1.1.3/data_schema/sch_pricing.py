import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_pricing(cds):
    cds.extend_node_rater_defined("cds", {
    # Use the following bucket for policy level information which does not vary by layer. 
    # See the user guide for more information. 
    # Extend the below as required.
        "rating_factors": hx.Structure(children={
            "policy_term": hx.Float(mode="output"),
            # Add rating factors here 

            
        }),
    })


