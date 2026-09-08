import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.data_schema.sch_rater_defined import exposure_dict


def sch_exposure_details(cds):

    # For granular exposure lists e.g. aircrafts, hospitals etc, please add to the granular node
    cds.extend_node_rater_defined("cds/exposure/granular", exposure_dict)