import hx_data_schema as hx

def sch_extend_coverages(cds):
    cds.extend_node_items("cds/layers/coverages",{
        "epl":{"label": "Employment Practices Liability"},
        "fid":{"label": "Fiduciary"},
        "pcl":{"label": "Private Company Liability"}
    })




