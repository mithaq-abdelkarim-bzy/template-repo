import hx_data_schema as hx
import data_schema.sch_utilities as utils

# Replace / remove examples with your models exposures

def sch_exposure_details(cds):
    
    cds.extend_node_rater_defined("cds/exposure/aggregate", {
        "ly_aggregates": hx.Structure(view = {"label": "LY Aggregates"}, children = {
            "exposure_total": hx.Float(mode="output", optionality="optional", view={"label": "Exposure Total", "format": utils.thousands_format(0)}),
            "bespoke_total": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Bespoke Total", "format": utils.thousands_format(0)}),
            "key_zone_total": hx.Float(mode="output", optionality="optional", validation={"min_value": 0}, view={"label": "Key Zone Total", "format": utils.thousands_format(0)}),
        }),
        "ty_aggregates": hx.Structure(view = {"label": "TY Aggregates"}, children = {
            "exposure_total": hx.Float(mode="output", optionality="optional", view={"label": "Exposure Total", "format": utils.thousands_format(0)}),
            "bespoke_total": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "Bespoke Total", "format": utils.thousands_format(0)}),
            "key_zone_total": hx.Float(mode="output", optionality="optional", validation={"min_value": 0}, view={"label": "Key Zone Total", "format": utils.thousands_format(0)}),
        }),
        "value_change": hx.Structure(view = {"label": "Value +-"}, children = {
            "exposure_total": hx.Float(mode="output", optionality="optional", view={"label": "Exposure Total", "format": utils.thousands_format(0)}),
            "bespoke_total": hx.Float(mode="output", view={"label": "Bespoke Total", "format": utils.thousands_format(0)}),
            "key_zone_total": hx.Float(mode="output", view={"label": "Key Zone Total", "format": utils.thousands_format(0)}),
        }),
        "perc_change": hx.Structure(view = {"label": "% Change"}, children = {
            "exposure_total": hx.Float(mode="output", optionality="optional", view={"label": "Exposure Total", "format": {"output": "percent", "mantissa": 1}}),
            "bespoke_total": hx.Float(mode="output", view={"label": "Bespoke Total", "format": {"output": "percent", "mantissa": 1}}),
            "key_zone_total": hx.Float(mode="output", view={"label": "Key Zone Total", "format": {"output": "percent", "mantissa": 1}}),
            ## premium changes
            "prem_change": hx.Float(mode="output", view={"label": "Premium", "format": {"output": "percent", "mantissa": 1}}),
        }),
        "exposure_measure": hx.Str(mode="input", default=None, optionality="optional", options_column="type", options_table="table_exposure_type", view={"label": "Exposure Measure"}),
        "exposure_comments": hx.Str(mode="input", default="", view={"label": "Comments"}),
    })

    cds.extend_node_rater_defined("cds/exposure/granular", {
        "exposures": hx.List(mode="input", default_element_count= 20, children={
            "peril": hx.Str(mode="input", default=None, optionality="optional", options_column="peril_label", options_table="table_peril_name", allow_custom_value=True, view={"label": "Peril"}),
            "address_dropdown": hx.Structure(linked_default_index=0, linked_options_columns=["country", "state", "county"], linked_options_table="table_address", view={"linked_options_selector": "hierarchical"}, children={
                "country": hx.Str(mode="input", view={"label": "Country", "group": "Address"}),
                "state": hx.Str(mode="input", view={"label": "State", "group": "Address"}),
                "county": hx.Str(mode="input", view={"label": "County", "group": "Address"}),
            }),
            "description": hx.Str(mode="input", default=None, optionality="optional", view={"label": "Description"}),
            "key_zone_selector": hx.Bool(mode="input", default = False, view={"label": "Key Zone Selector"}),
            "ly_aggregate": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "LY Aggregate", "format": utils.thousands_format(0)}),
            "ty_aggregate": hx.Float(mode="input", default=None, optionality="optional", validation={"min_value": 0}, view={"label": "TY Aggregate", "format": utils.thousands_format(0)}),
            "value_change": hx.Float(mode="output", optionality="optional", view={"label": "Value +-", "format": utils.thousands_format(0)}),
            "perc_change": hx.Float(mode="output", optionality="optional", view={"label": "% Change", "format": {"output": "percent", "mantissa": 1}}),
        }),
    })

