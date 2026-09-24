import hx_data_schema as hx
from data_schema.sch_utilities import thousands_format, percent_format, integer_format
from algorithms import rate_constants as constants


def generate_years_headers_list(start: int, end: int):
    return [f"year_{year}" for year in range(start, end + 1)]


def sch_base_inf(cds):
    cds.extend_node_rater_defined(
        "cds",
        {
            "base_inf": hx.List(
                mode='output',
                children={
                    'bp_class': hx.Str(mode='output',view={'label':'Business Plan Class'}),
                     **{year: hx.Float(mode="output", view={"label": f"{year}","format":percent_format(1)})for year in generate_years_headers_list(0,25)},
                }
            )
        }
    
    )
