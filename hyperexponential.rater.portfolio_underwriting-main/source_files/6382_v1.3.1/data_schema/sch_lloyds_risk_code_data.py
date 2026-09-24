import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms import rate_constants as constants


def generate_years_structure(group: str, format = percent_format(0), start: int = 0, end: int = constants.YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE):
    return hx.Structure(
        children={
            f"year_{year}": hx.Float(
                mode="output",
                view={"label": f"year_{year}",
                      "format": format, "group": group}
            )
            for year in range(start, end)
        }
    )


def sch_lloyds_risk_code_data(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "lloyds_risk_code_data": hx.List(
                mode='output',
                children={
                    'lloyds_risk_code': hx.Str(mode='output',view={'label':'Lloyds Risk Code'}),
                    'yoa': hx.Str(mode='output',view={'label':'Year of Account'}),
                    'gpi': hx.Float(mode='output',view={'label':'GPI'}),
                    'gnpi': hx.Float(mode='output',view={'label':'GNPI'}),
                    'acquisition_cost': hx.Float(mode='output',view={'label':'Acquisition Cost'}),
                    'latest_paid_position': hx.Float(mode='output',view={'label':'Latest Paid Position'}),
                    'latest_incurred_position': hx.Float(mode='output',view={'label':'Latest Incurred Position'}),
                    'gn_ulr': hx.Float(mode='output',view={'label':'GN ULR'}),
                    'incurred_development': hx.Float(mode='output',view={'label':'Incurred Development'}),
                    'paid_development': hx.Float(mode='output',view={'label':'Paid Development'}),
                    'premium_development': hx.Float(mode='output',view={'label':'Premium Development'}),
                }
            )
        }
    
    )
