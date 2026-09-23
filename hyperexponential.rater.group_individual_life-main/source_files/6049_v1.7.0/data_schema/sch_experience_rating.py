import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms.rate_constants import max_layers

def sch_experience_rating(cds):

    cds.extend_node_rater_defined("cds/experience_rating", {
            "cut_off_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Data cut-off date"}),
            "date_check": hx.Str(mode="output"),
            "date_check_show": hx.Bool(mode="output"),
            "death_or_all_risks": hx.Str(mode="input", default=None, async_output=["start_renewal_task"], optionality="optional", options=["Death only", "All risk"], view={"label": "Death / all risks"}),
            "life_years": hx.Float(mode="output", view={"label": "Total Life-Years", "format": thousands_format(0)}),
            "cred_weight": hx.Float(mode="output", view={"label": "Credibility Weight", "format": thousands_format(3)}),
            "z_factor": hx.Float(mode="output", view={"label": "Z", "format": thousands_format(3)}),
            "one_minus_z": hx.Float(mode="output", view={"label": "1-Z", "format": thousands_format(3)}),
            "burn_cost": hx.Float(mode="output", view={"label": "Burn Cost", "format": thousands_format()}),
            "death_only_discount": hx.Float(mode="output", view={"label": "Death Only Discount", "format": thousands_format(3), "info": "Discount rate apllied if historic data is Death Only"}),
            "all_risk_discount": hx.Float(mode="output", view={"label": "All Risk Discount", "format": thousands_format(3), "info": "Discount rate apllied if historic data is All Risk"}),
    })

    def claims_fields(mode=None, default=None, async_output=hx.nodes.UNDEFINED):
        
        return {
            "year": hx.Int(mode=mode or "output", view={"label": "Year", "format": integer_format()}),
            "no_lives": hx.Float(mode=mode or "input", default=default or 0, async_output=async_output, validation={"min_value": 0}, view={"label": "# Lives", "format": thousands_format()}),
            "sum_insured": hx.Float(mode=mode or "input", default=default or 0, async_output=async_output, validation={"min_value": 0}, view={"label": "Sum\nInsured", "format": thousands_format()}),
            "incurred": hx.Float(mode=mode or "input", default=default or 0, async_output=async_output, validation={"min_value": 0}, view={"label": "Incurred\nClaims", "format": thousands_format()}),
            "number": hx.Float(mode=mode or "input", default=default or 0, async_output=async_output, validation={"min_value": 0}, view={"label": "# Claims", "format": thousands_format()}),
            "ibnr_factor": hx.Float(mode=mode or "output", view={"label": "IBNR/ER\nFactor", "format": thousands_format(3)}),
            "time_adj": hx.Float(mode=mode or "output", view={"label": "Time Adj", "format": thousands_format(3)}),
            "burn": hx.Float(mode=mode or "output", view={"label": "Burn", "format": thousands_format(3)}),
            "burn_per_mille": hx.Float(mode=mode or "output", view={"label": "Burn\nper mille", "format": thousands_format(3)}),
        }

    cds.extend_node_rater_defined("cds/experience_rating/claims", claims_fields(async_output=["start_renewal_task"]))
    cds.extend_node_rater_defined("cds/experience_rating", {"claims_totals": hx.Structure(view={"label": "Total"}, children=claims_fields(mode="output", default=hx.nodes.UNDEFINED))})

    # Override node properties
    cds.override_node_properties("cds/experience_rating/claims", {"default_element_count": 6, "async_output": ["start_renewal_task"]})
    cds.override_node_properties("cds/experience_rating/claims_available", {"async_output": ["start_renewal_task"]})
