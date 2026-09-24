import hx_data_schema as hx
import data_schema.sch_utilities as utils
import hx as hx_files

def sch_historical_freq(cds):

    # Number of columns depends on the number of years in the parameter table
    df_hist_freq = hx_files.params.historical_freq
    years = list(df_hist_freq.columns.values)
    years = years[2:]
 
    cds.extend_node_rater_defined("cds", {
        "sector_display": hx.Str(mode="output", view={"label": "Sector"}),
        "linked_spreadsheet" : hx.Str(mode="output", view={"label": ""}),
        "table_explained" : hx.Str(mode="output", view={"label": ""}),
        "graph_explained" : hx.Str(mode="output", view={"label": ""}),
        "historical_freq": hx.List(mode="input", default_element_count=len(years), children={
            "display_year" : hx.Str(mode="output", view={"label": "Year"}),
            "claims" : hx.Float(mode="output", view={"label": "Claims", "format": {"mantissa": 0}}),
            "exposure" : hx.Float(mode="output", view={"label": "Exposure", "format": {"mantissa": 0}}),
            "base_frequency" : hx.Float(mode="output", view={"label": "Base Frequency", "format": {"output": "percent", "mantissa": 1}}),
            "mc_frequency" : hx.Float(mode="output", view={"label": "MC Frequency", "format": {"output": "percent", "mantissa": 1}})
        })
    })
