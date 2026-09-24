import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format
from data_schema.sch_utilities import percent_format
from data_schema.sch_utilities import integer_format

def sch_rater_defined(cds):
    cds.extend_node_items("cds/layers/coverages", {
        "specialty": {"label": "Specialty"},
    })
    cds.extend_node_rater_defined("cds/exposure/granular", {
        "construction_with_in_house_design": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Engineering", view={"label": "Discipline"}),

        }),
        "construction_with_sub_contracted_design": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Contractors", view={"label": "Discipline"}),

        }),
        "design_only_no_construction": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Engineering", view={"label": "Discipline"}),

        }),
        "construction_only_no_design": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Contractors", view={"label": "Discipline"}),

        }),
        "at_risk_construction_management": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Engineering", view={"label": "Discipline"}),

        }),
        "agency_construction_management": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="input", default=0.0, view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Engineering", view={"label": "Discipline"}),

        }),
        "other": hx.Structure(children={
            "current_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="input", default=0.0, view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Override"}),
            "other_specify": hx.Str(mode="input", default="0", view={"label": "Other (Specify)"}),
            "rateable_exposure_discipline": hx.Str(mode="input", default="Engineering", view={"label": "Discipline"}),

        }),
        "total": hx.Structure(children={
            "current_yr_construction_value": hx.Float(mode="output", view={"label": "Construction Values (Current Year)"}),
            "current_yr_professional_fees": hx.Float(mode="output", view={"label": "Professional Fees (Current Year)"}),
            "current_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Current Year)"}),
            "last_yr_construction_value": hx.Float(mode="output", view={"label": "Construction Values (Last Fiscal Year)"}),
            "last_yr_professional_fees": hx.Float(mode="output", view={"label": "Professional Fees (Last Fiscal Year)"}),
            "last_yr_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (Last Fiscal Year)"}),
            "two_yr_ago_construction_value": hx.Float(mode="output", view={"label": "Construction Values (2 Years Ago)"}),
            "two_yr_ago_professional_fees": hx.Float(mode="output", view={"label": "Professional Fees (2 Years Ago)"}),
            "two_yr_ago_rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure (2 Years Ago)"}),
            "three_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "3 Year Average"}),
            "two_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "2 Year Average"}),
            "current_yr_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Current Fiscal Year"}),
            "selected_avg_rateable_exposure": hx.Float(mode="output", view={"label": "Selected"}),
            "override_avg_rateable_exposure": hx.Float(mode="override", view={"label": "Override"}),

        }),
        "engineering": hx.Structure(children={
            "considerations": hx.Str(mode="output", view={"label": "Considerations"}),
            "aerospace": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "architect_comm": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "architect_resi": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "aviation": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "chemical": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "civil": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "civil_bridges_roads": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "cm_atrisk": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "cm_agency": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "drafting": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "electrical": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "enviro_cons": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "enviro_labs": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "fp": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "forensic": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "geotechnical": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "hvac": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "int_design": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "landscape": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "leed_cons": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "mech": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "mech_electrical": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "mining": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "non_destructive_testing": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "nuclear": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "oil_gas": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "process": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "struct_resi_inst": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "struct_steel_stairs": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "struct_non_resi_inst": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "surveyor": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "surveyor_resi": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "other_one": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_two": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_three": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_four": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_five": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "total": hx.Structure(children={
                "percentage": hx.Float(mode="output", view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="output", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "minimum_premium": hx.Float(mode="output", view={"label": "Minimum Premium"}),

            }),

        }),
        "contractor": hx.Structure(children={
            "considerations": hx.Str(mode="output", view={"label": "Considerations"}),
            "asbestos_lead": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "build_envelop": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "carpenter": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "concrete": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "demolition": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "electrical": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "enviro": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "fp": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "foundation_excav": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "general_comm": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "general_resi": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "glazing": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "hvac": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "landscape": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "masonry": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "mech": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "reno_non_resi": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "oil_gas": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "painting": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "plumbing": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "resi_reno": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "roofing": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "steel": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "telecom": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "utilities": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="override", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),

            }),
            "other_one": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_two": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_three": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_four": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "other_five": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=0.0, view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="input", default=1.0, view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "guidelines": hx.Str(mode="output", view={"label": "Guidelines"}),
                "other_specify": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Other (Specify)"}),

            }),
            "total": hx.Structure(children={
                "percentage": hx.Float(mode="output", view={"label": "Percentage"}),
                "rateable_exposure": hx.Float(mode="output", view={"label": "Rateable Exposure"}),
                "default_base_rate": hx.Float(mode="output", view={"label": "Default Base Rate"}),
                "base_rate_override": hx.Float(mode="output", view={"label": "Base Rate Override"}),
                "base_premium": hx.Float(mode="output", view={"label": "Base Premium"}),
                "minimum_premium": hx.Float(mode="output", view={"label": "Minimum Premium"}),

            }),

        }),
        "expiring": hx.Structure(children={
            "construction_with_in_house_design": hx.Structure(children={
                "current_yr_construction_value": hx.Float(mode="output", view={"label": "Construction Values (Current Year)"}),
                "current_yr_professional_fees": hx.Float(mode="output", view={"label": "Professional Fees (Current Year)"}),

            }),

        }),
    })
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "uw_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Commentary"}),
    })
    cds.extend_node_rater_defined("cds", {
        "modifiers": hx.Structure(children={
            "exp_mod": hx.Structure(children={
                "incurred_loss": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total incurred loss"}),
                "number_of_claims": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of claims"}),
                "number_of_incidents": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Number of incidents"}),
                "written_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Total written premium"}),
                "incurred_lr": hx.Float(mode="output", view={"label": "Total incurred loss ratio"}),
                "exp_mod_factor": hx.Float(mode="input", default=1.0, view={"label": "Experience Modification Factor (Suggested Range: 0.80 - 2.00)"}),
                "uw_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Commentary"}),

            }),
            "written_contracts": hx.Structure(children={
                "percentage": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Enter the percent of projects that use written contracts"}),
                "written_contracts_factor": hx.Float(mode="input", default=1.0, view={"label": "Use of Written Contracts Factor (Suggested Range: 0.95 - 1.05)"}),

            }),
            "longevity_with_carrier": hx.Structure(children={
                "yrs_insured": hx.Float(mode="input", default=1.0, view={"label": "Number of years insured with the Company including this renewal"}),
                "lr": hx.Bool(mode="input", default=True, view={"label": "Loss ratio less than 50% whilst with the Company (calculated up to 5 years with the Company)? "}),

            }),
            "longevity": hx.Structure(children={
                "yr_start": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Enter the year the Insured started in business"}),
                "yrs_in_business": hx.Float(mode="output", view={"label": "Years in business"}),

            }),
            "erp": hx.Structure(children={
                "erp": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Select Extended Reporting Period"}),

            }),
            "resi": hx.Structure(children={
                "resi_proj": hx.Bool(mode="input", default=True, view={"label": "Residential Project?"}),
                "multiple_units": hx.Bool(mode="input", default=True, view={"label": "Multiple Units - Over 25?"}),
                "high_value": hx.Bool(mode="input", default=True, view={"label": "High Value - Largest Projects over $500k?"}),
                "condos": hx.Bool(mode="input", default=True, view={"label": "Condos"}),

            }),
            "opt_coverages": hx.Structure(children={
                "full_prior_act": hx.Bool(mode="input", default=True, view={"label": "7. Full Prior Acts Coverage"}),
                "full_prior_act_date": hx.Date(mode="input", default=None, optionality="optional", view={"label": "Enter Retroactive Date"}),
                "cpl": hx.Bool(mode="input", default=True, view={"label": "8. CPL Coverage"}),
                "tech": hx.Bool(mode="input", default=True, view={"label": "9. Tech Coverage"}),
                "non_contributary": hx.Bool(mode="input", default=True, view={"label": "10. Primary NoN Contributary"}),

            }),
            "schedule_rating_factor": hx.Structure(children={
                "qual_of_staff": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "rm_attendance": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "foreign_work": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "project_type": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "loss_prev": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "client_type": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "contractual_practices": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "engi_procure_construct": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "peer_review": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="input", default=0.0, view={"label": "Schedule Factor"}),
                    "comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Comment"}),

                }),
                "total": hx.Structure(children={
                    "min": hx.Float(mode="output", view={"label": "Min"}),
                    "max": hx.Float(mode="output", view={"label": "Max"}),
                    "factor": hx.Float(mode="output", view={"label": "Schedule Factor"}),

                }),

            }),

        }),
        "brokerage": hx.Float(mode="input", default=0.25, view={"label": "Brokerage"}),
        "location": hx.Structure(children={
            "state": hx.Str(mode="input", default=None, optionality="optional", view={"label": "State"}),
            "risk_group": hx.Str(mode="output", view={"label": "Risk Group"}),

        }),
        "primary": hx.Structure(children={
            "aggregate_limit_view": hx.Float(mode="output", view={"label": "Aggregate Limit"}),
            "benchmark_premium": hx.Float(mode="output", view={"label": "Gross Benchmark Premium"}),
            "technical_premium": hx.Float(mode="output", view={"label": "Gross Technical Premium"}),
            "ilf_curve": hx.Float(mode="output", view={"label": "ILF Curve"}),
            "carrier": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Carrier"}),
            "carrier_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Quoted Premium (Carrier)"}),
            "quoted_ilf_curve": hx.Float(mode="output", view={"label": "Quoted ILF Curve"}),
            "quoted_premium_view": hx.Float(mode="output", view={"label": "Gross Quoted Premium"}),
            "status_view": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Status"}),
            "section_reference_view": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference"}),
            "quoted_premium": hx.Float(mode="input", default=0.0, view={"label": "Gross Quoted Premium"}),
            "status": hx.Str(mode="output", view={"label": "Status"}),
            "section_reference": hx.Str(mode="output", view={"label": "Section Reference"}),
            "bpi": hx.Float(mode="output", view={"label": "BPI"}),
            "tpi": hx.Float(mode="output", view={"label": "TPI"}),
            "uw_comment": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Underwriter Commentary"}),
            "ilf_type": hx.Str(mode="input", default=None, optionality="optional", view={"label": "ILF Type"}),
            "limit": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Limit"}),
            "number_of_reinstatements": hx.Int(mode="input", default=None, optionality="optional", view={"label": "Number of Reinstatements"}),
            "guideline_deductible": hx.Float(mode="output", view={"label": "Guideline Deductible"}),
            "deductible": hx.Float(mode="input", default=0.0, view={"label": "Deductible"}),
            "written_line": hx.Float(mode="input", default=1.0, view={"label": "Written Line"}),
            "pflr": hx.Float(mode="output", view={"label": "Priced-for Loss Ratio"}),
            "roc": hx.Float(mode="output", view={"label": "Return on Capital"}),

        }),
        "currency_label": hx.Str(mode="output", view={"label": "Currency Label"}),
        "xslayer_considerations": hx.Str(mode="output", view={"label": "Excess Layer Considerations"}),
    })
    cds.extend_node_rater_defined("cds/layers", {
        "ilf_curve": hx.Float(mode="output", view={"label": "ILF Curve"}),
        "carrier": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Carrier"}),
        "carrier_premium": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Gross Quoted Premium (Carrier)"}),
        "quoted_ilf_curve": hx.Float(mode="output", view={"label": "Quoted ILF Curve"}),
        "cum_attachment": hx.Str(mode="output", view={"label": "Attachment Point"}),
        "cum_benchmark_premium": hx.Float(mode="output", view={"label": "Cumulative Benchmark Premium (Excess)"}),
        "cum_technical_premium": hx.Float(mode="output", view={"label": "Cumulative Technical Premium (Excess)"}),
        "cum_carrier_premium": hx.Float(mode="output", view={"label": "Cumulative Carrier Premium (Excess)"}),
        "quoted_premium_net": hx.Float(mode="output", view={"label": "Net Quoted Premium"}),
        "aggregate_limit_view": hx.Float(mode="input", default=None, optionality="optional", view={"label": "Aggregate Limit"}),
        "quoted_premium_view": hx.Float(mode="input", default=0.0, view={"label": "Quoted Premium"}),
        "excess_view": hx.Bool(mode="output", view={"label": "Excess Flag"}),
        "status_view": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Status"}),
        "section_reference_view": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Section Reference"}),
    })
