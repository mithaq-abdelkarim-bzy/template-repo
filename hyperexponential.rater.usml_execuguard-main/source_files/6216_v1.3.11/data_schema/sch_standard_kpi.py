import hx_data_schema as hx

def sch_standard_kpi(cds):

    cds.override_node_properties("cds/layers/bpi_case_priced", {"view": {"label": "BPI (Case Priced)", "options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/layers/premium", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})


    cds.override_node_properties("cds/standard_fields/policy_reference", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})

    cds.override_node_properties("cds/standard_fields/rating_methodology", {"view": {"options": {
        "read_only": {"read_only": True}
    }}})
