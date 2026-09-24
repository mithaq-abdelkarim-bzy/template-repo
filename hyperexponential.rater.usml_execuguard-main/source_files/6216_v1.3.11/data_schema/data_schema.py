import hx_data_schema as hx


from data_schema.sch_employee_count import sch_employee_count
from data_schema.sch_exposure_details import sch_exposure_details, sch_exposure_details_non_cds
from data_schema.sch_extend_coverages import sch_extend_coverages
from data_schema.sch_rate_change import sch_rate_change
from data_schema.sch_rating_summary import sch_rating_summary
from data_schema.sch_risk_information import sch_risk_information
from data_schema.sch_usml_epl_inputs import sch_epl_non_cds, sch_usml_epl_inputs, sch_running_prem_summary_epl
from data_schema.sch_usml_fiduciary_inputs import sch_fiduciary_non_cds, sch_usml_fiduciary_inputs, sch_running_prem_summary_fid
from data_schema.sch_usml_pcl_inputs import sch_pcl_non_cds, sch_usml_pcl_inputs, sch_running_prem_summary_pcl
from data_schema.sch_modifiers import sch_modifiers
from data_schema.sch_admitted_excess_local import sch_admitted_excess_local, sch_excess_rate_change
from data_schema.sch_skeleton_overrides import sch_skeleton_overrides
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from libraries.admitted_excess_premium.data_schema.sch_admitted_excess import sch_admitted_excess
from data_schema.sch_claims import sch_claims
from data_schema.sch_experience_rating import sch_experience_rating
from data_schema.sch_model_state import sch_model_state
from data_schema.sch_standard_kpi import sch_standard_kpi
from libraries.email_notification.data_schema.bug_report_schema import bug_report


def sch_common_data_schema():
    cds = CommonDataSchema()
    sch_skeleton_overrides(cds)
    sch_extend_coverages(cds)
    sch_employee_count(cds)
    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_rating_summary(cds)     
    sch_usml_pcl_inputs(cds)
    sch_running_prem_summary_pcl(cds)    
    sch_usml_epl_inputs(cds)
    sch_running_prem_summary_epl(cds)
    sch_usml_fiduciary_inputs(cds)
    sch_running_prem_summary_fid(cds)
    sch_modifiers(cds)
    sch_admitted_excess(cds)
    sch_excess_rate_change(cds)
    # additional admitted excess for non library calculations
    sch_admitted_excess_local(cds)
    #we need these two for the cds to work
    sch_experience_rating(cds)
    sch_claims(cds)
    sch_standard_kpi(cds)
   

    return cds.get_data_schema()

#these are the data schema items used for formatting and don't go into the cds
def sch_non_cds_items():
    return {
        "non_cds": hx.Structure(children={
            **sch_exposure_details_non_cds(),
            **sch_fiduciary_non_cds(),
            **sch_pcl_non_cds(),
            **sch_epl_non_cds(),
            "quoted_premium_case_priced_label": hx.Str(mode = "output")
        })
    }  


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        **sch_non_cds_items(),
        **bug_report()
    })