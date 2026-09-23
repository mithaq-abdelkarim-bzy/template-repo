import hx_data_schema as hx
from data_schema.sch_z_utilities import thousands_format
from data_schema.sch_z_utilities import percent_format
from data_schema.sch_z_utilities import integer_format

def sch_show_page(cds):
    '''
    Internal Model State that controls the workflow
    '''
    # SA: Do these need to be in the cds?
    cds.extend_node_rater_defined("cds", {
        "show_page": hx.Structure(children={
            "show_jb": hx.Bool(mode="output"),
            "show_fa": hx.Bool(mode="output"),
            "show_cit": hx.Bool(mode="output"),
            "show_gs": hx.Bool(mode="output"),
            "show_rate_change": hx.Bool(mode="output"),
            "show_risk_information": hx.Bool(mode="output"),
            "show_other": hx.Bool(mode="output"),
        }),
    })
