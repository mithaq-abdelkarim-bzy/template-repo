import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_exposure_details import sch_exposure_details
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_model_state import sch_model_state

from data_schema.sch_modelling import sch_modelling
from data_schema.sch_non_modelled_perils import sch_non_modelled_perils
from data_schema.sch_pml_curves import sch_pml_curves
from data_schema.sch_burn import sch_burn
from data_schema.sch_curve_aggregator import sch_curve_aggregator
from data_schema.sch_peril_allocation import sch_peril_allocation
from data_schema.sch_quote import sch_quote
from data_schema.sch_summary import sch_summary
from data_schema.sch_simulation import sch_simulation
from data_schema.sch_bi_data import sch_bi_data
from data_schema.sch_calculator import sch_calculator
from data_schema.sch_additional_pages import sch_additional_pages
from data_schema.sch_risk_xl_exposure_rating import sch_risk_xl_exposure_rating

from data_schema.sch_overrides import sch_overrides

def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_rating_summary(cds)
    sch_modelling(cds)
    sch_non_modelled_perils(cds)
    sch_pml_curves(cds)
    sch_burn(cds)
    sch_curve_aggregator(cds)
    sch_peril_allocation(cds)
    sch_quote(cds)
    sch_summary(cds)
    sch_simulation(cds)
    sch_bi_data(cds)
    sch_calculator(cds)
    sch_additional_pages(cds)

    sch_risk_xl_exposure_rating(cds)

    sch_overrides(cds)   

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state()
    })