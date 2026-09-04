import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format
from algorithms.data_schema.sch_rater_defined import aggregate_exposure_dict, granular_exposure_dict


def sch_exposure_details(cds):

    cds.extend_node_rater_defined("cds/exposure/aggregate", aggregate_exposure_dict)
    cds.extend_node_rater_defined("cds/exposure/granular", granular_exposure_dict)

