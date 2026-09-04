import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format

def sch_non_cds():
    return{
        "uw_validation": hx.Structure(children={
            "underwriter_warning": hx.Str(mode="output"),
            "show_underwriter_warning": hx.Bool(mode="output"),
        })
    }