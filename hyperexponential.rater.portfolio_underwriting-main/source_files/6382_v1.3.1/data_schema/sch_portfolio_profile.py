import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms import rate_constants as constants


def generate_years_structure(group: str, start: int = 0, end: int = constants.YEARS_TO_CONSIDER_IN_PORTFOLIO_PROFILE):
    return hx.Structure(
        children={
            f"year_{year}": hx.Float(
                mode="output",
                view={"label": f"year_{year}",
                      "format": percent_format(1), "group": group}
            )
            for year in range(start, end)
        }
    )


def generate_common_nodes():
    return {
        'selected_lob': hx.Str(mode='output', view={"label": 'Selected LoB'}),
        'bp_class': hx.Str(mode='output', view={"label": 'Business Plan Class'}),
        'risk_code': hx.Str(mode='output', view={"label": 'Risk Code'}),
        'selected_premium': hx.Float(mode='output', view={"label": 'Selected Premium', "format": thousands_format(0)}),
        'weighting': hx.Float(mode='output', view={"label": 'Weighting', "format": percent_format(0)}),
        'rate_change_with_selection_override': generate_years_structure('Rate Change - With Selection Override'),
        'rate_change_no_override': generate_years_structure('Rate Change - No Override'),
        'lloyds_incurred_development': generate_years_structure('Lloyds - Incurred Development'),
        'lloyds_paid_development': generate_years_structure('Lloyds - Paid Development'),
        'lloyds_premium_development': generate_years_structure('Lloyds - Premium Development'),
        'lloyds_risk_code_results': hx.Structure(
            children={
                "final_gn_ulr": hx.Float(mode="output", view={"label": "Final GN ULR", "format": percent_format(1), "group": "Lloyds Risk Code - Result"}),
                "selected_ielr": hx.Float(mode="output", view={"label": "Selected IELR", "format": percent_format(1), "group": "Lloyds Risk Code - Result"}),
                "model_ielr": hx.Float(mode="output", view={"label": "Model IELR", "format": percent_format(1), "group": "Lloyds Risk Code - Result"})
            }
        ),
        'beazley_risk_code_results': hx.Structure(
            children={
                "final_gn_ulr": hx.Float(mode="output", view={"label": "Final GN ULR", "format": percent_format(1), "group": "Beazley Risk Code - Result"})
            }
        ),
    }


def sch_portfolio_profile(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "portfolio_profile": hx.Structure(
                children={
                    "selected_lob_and_risk_code_combination": hx.List(
                        mode='output',
                        children=generate_common_nodes()
                    ),
                    "selected_lob_and_risk_code_combination_str": hx.Str(
                        mode="output",
                        async_input=[]
                    ),
                    "summary_by_lob": hx.List(
                        mode='output',
                        children=generate_common_nodes()
                    ),
                    "selected_by_lob_str": hx.Str(
                        mode="output",
                        async_input=[]
                    ),
                }
            )
        }
    )
