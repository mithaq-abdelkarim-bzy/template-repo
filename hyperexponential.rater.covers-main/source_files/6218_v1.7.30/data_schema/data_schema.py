import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema     import CommonDataSchema
from data_schema.sch_risk_information                                    import sch_risk_information
from data_schema.sch_sov_details                                         import sch_sov_details
from data_schema.sch_em_bi                                               import sch_exposure_management_api, sch_bi_data
from data_schema.sch_triangle_projection                                 import sch_triangle_projection
from data_schema.sch_overrides                                           import sch_async_tasks
from data_schema.sch_summary_exhibits                                    import sch_summary_exhibits
from data_schema.sch_profit_commission                                   import sch_profit_commission
from data_schema.sch_rating_summary                                      import sch_rating_summary
from data_schema.sch_model_state                                         import sch_model_state
from data_schema.sch_show_hide_and_dropdown                              import sch_show_hide
from data_schema.sch_profit_commission                                   import sch_profit_commission
from data_schema.sch_rms                                                 import sch_rms
from data_schema.sch_claim_summary                                       import sch_claim_summary
from data_schema.sch_rms                                                 import sch_rms
from data_schema.sch_rationale                                           import sch_rationale
from data_schema.sch_check_async                                         import sch_check_async

def sch_common_data_schema():
    cds = CommonDataSchema()
    sch_risk_information(cds)
    sch_sov_details(cds)
    sch_rms(cds)
    sch_claim_summary(cds)
    sch_profit_commission(cds)
    sch_rating_summary(cds)
    sch_exposure_management_api(cds)
    sch_bi_data(cds)
    sch_triangle_projection(cds)
    sch_rating_summary(cds)
    sch_show_hide(cds)
    sch_profit_commission(cds)
    sch_summary_exhibits(cds)
    sch_async_tasks(cds)
    sch_rationale(cds)
    sch_check_async(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state()
    })