import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

# Transform into HX structure
def get_risk_codes():
    return [  
    ("risk_code", "Risk Code"),
    ("high_level_cob", "High Level Class of Business"),
    ("generic_cob", "Generic Class of Business"),
    ("type_of_placement", "Terrorism subject to overseas legislation - offshore energy - property"),
    ("risk_code_description","Risk Code Description"),
    ("risk_code_explained", "Risk Code Description - Expanded"),
    ("oecd_class_mapping", "OECD Class Mapping"),
    ("assigned_tracker", "Assigned Tracker"),
    ("assigned_bp_class", "Assigned BP Class"),
    ("do_we_model", "Do we model?")
    ]
def get_lloyds_group():
    return[    
    ("gnpi_lloyds", "GNPI"),
    ("incured_lloyds", "Incurred"),
    
    ]
def get_beazley_group():
    return[
    ("gnpi_beazley", "GNPI"),
    ("incurred_beazley", "Incurred"),
    
    ]  

def sch_risk_code_library(cds):
    cds.extend_node_rater_defined("cds", {
        # Risk Codes Table        
        "risk_code_library": hx.List(mode = "input",
        default_element_count=200,
        view={"label": "Risk Codes"}, children={
            **{
                field: hx.Str(mode="output",  view={"label": label})
                for field, label in get_risk_codes()
            },
             **{
                field: hx.Int(mode="output",  view={"label": label, "group":"Lloyds Industry Performance", "format": thousands_format(0)})
                for field, label in get_lloyds_group()
            },
            "gn_ilr_lloyds": hx.Float(mode="output",  view={"label": "GN ILR", "group":"Lloyds Industry Performance", "format": {"output": "percent", "mantissa": 0}}),
             **{
                field: hx.Int(mode="output",  view={"label": label, "group":"Beazley Group Performance", "format": thousands_format(0)})
                for field, label in get_beazley_group()
            },
            "gn_ilr_beazley": hx.Float(mode="output",  view={"label": "GN ILR", "group":"Beazley Group Performance", "format": percent_format(0)})
        }),
    
        "year_start": hx.Int(mode="input", default=2020, view={"label": "Year Start","format": integer_format(0)}),
        "year_end": hx.Int(mode="input", default=2024, view={"label": "Year End","format": integer_format(0)}),
        "risk_code_description_expanded": hx.Bool(
                        mode="input",
                        default=False,
                        optionality="required",
                        view={"label": "Risk Code Description Expanded"}
                        
                    )

        })



