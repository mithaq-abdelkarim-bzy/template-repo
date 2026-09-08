import hx_data_schema as hx
import data_schema.utilities as utils

def sch_core_data(cds):
    cds.extend_node_rater_defined("cds", {
        "yoa": hx.Int(mode="output", view={"label": "YOA"}),
    })

    cds.override_node_properties("cds/standard_fields/insured_name", {
        "async_input": ["start_renewal_task"]
    })

    # Core Data
    cds.override_node_properties("hx_core/charged_premium", {
        "view": {"label": "Gross Quoted Premium", "format": utils.thousands_format(0)}
    })

    cds.override_node_properties("hx_core/premium_currency", {
        "mode": "output", 
        "view": {"label":"Currency"}
    })

    cds.override_node_properties("hx_core/ulr", {
        "view": {"label": "Implied ULR", "format": utils.percent_format(1)}
    })

