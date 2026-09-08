import hx_data_schema as hx
from libraries.common_data_schema.data_schema.sch_common_data_schema import CommonDataSchema
from data_schema.sch_risk_information   import sch_risk_information
from data_schema.sch_exposure_details   import sch_exposure_details
from data_schema.sch_rate_change        import sch_rate_change
from data_schema.sch_rating_summary     import sch_rating_summary
from data_schema.sch_model_state        import sch_model_state
from data_schema.sch_show_hide          import sch_show_hide
from data_schema.sch_overrides          import sch_overrides
from data_schema.sch_ihs                import sch_ihs
from data_schema.sch_rationale          import sch_rationale
from data_schema.sch_pricing            import sch_pricing

def sch_common_data_schema():
    cds = CommonDataSchema()

    sch_risk_information(cds)
    sch_rate_change(cds)
    sch_exposure_details(cds)
    sch_pricing(cds)
    sch_rating_summary(cds)
    sch_ihs(cds)
    sch_show_hide(cds)
    # sch_experience_rating(cds) 
    sch_overrides(cds) 
    sch_rationale(cds)

    return cds.get_data_schema()


@hx.data_schema
def data_schema():
    return hx.Structure(children={
        **sch_common_data_schema(),
        **sch_model_state(),
        "live_hxd":  hx.Bool(mode="output",                  async_input =  ['task_sim_political'], view={"label": "hxd live = True; hxd transient= False"}   ),
    })