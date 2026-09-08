import hx_data_schema as hx
import data_schema.utilities as utils

def sch_standard_kpi(cds):
 
    cds.override_node_properties("cds/layers/brokerage", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/layers/section_reference", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/options/bpi", {"view": {"label": "BPI", "options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/options/brokerage", {"view": {"label": "Brokerage (excl. PC's)", "options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/options/quoted_premium", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/options/written_line", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})


    cds.override_node_properties("cds/standard_fields/policy_reference", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/options/section_reference", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})



    






