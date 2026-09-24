import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms import rate_constants as constants

def sch_standard_kpis(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "standard_kpis": hx.Structure(
                children={
                    'policy_reference': hx.Str(mode='output',view={'label':'Policy Reference'}),
                    'pflr_pre_uw_adj': hx.Float(mode='output',view={'label':'Priced-for Loss Ratio (Pre UW Adj.)', "format":percent_format(2)})
                }
            )
        }
    
    )
