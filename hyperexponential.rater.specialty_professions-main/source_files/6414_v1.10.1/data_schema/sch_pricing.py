import hx_data_schema as hx
from data_schema.sch_rating_factors_details import sch_rating_factors_details
from data_schema.sch_modifiers_details import sch_modifiers_details
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_pricing(cds):
    sch_rating_factors_details(cds)
    sch_modifiers_details(cds)


