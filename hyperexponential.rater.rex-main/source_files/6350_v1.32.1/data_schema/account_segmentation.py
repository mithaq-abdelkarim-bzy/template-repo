import hx_data_schema as hx
from data_schema.utilities import thousands_format, percent_format

def account_segmentation():
    '''
    Data schema for comments section in page policy info
    '''
    return {
        "pricing_layer_segmentation": hx.Structure(children={
            "state": hx.List(mode="output", view={"label": "State"}, children={**pricing_layer_segmentation_table("State")}),
            "country": hx.List(mode="output", view={"label": "Country"}, children={**pricing_layer_segmentation_table("Country")}),
            "state_country": hx.List(mode="output", view={"label": "State/Country"}, children={**pricing_layer_segmentation_table("State/Country")}),
            "state_country_choropleth": hx.List(mode="output", view={"label": "State/Country"}, children={**pricing_layer_segmentation_table("State/Country Choropleth")}),
            "state_country_choropleth_data": hx.Str(mode="output"),
            "state_country_outer": hx.List(mode="output", view={"label": "State Country"}, children={
                "country": hx.Str(mode="output", view={"label": "Country"}),
                "total_tiv": hx.Float(mode="output"), # for sorting only
                "country_list": hx.List(mode="output", view={"label": "State/Country"}, children={**pricing_layer_segmentation_table("State")}),
                }),
            "fire_occupancy": hx.List(mode="output", view={"label": "Occupancy"}, children={**pricing_layer_segmentation_table("Fire Occupancy")}),
            "ws_zone": hx.List(mode="output", view={"label": "Wind Zone"}, children={**pricing_layer_segmentation_table("Wind Zone")}),
            "eq_zone": hx.List(mode="output", view={"label": "Quake Zone"}, children={**pricing_layer_segmentation_table("Quake Zone")}),
            "fl_risk_category": hx.List(mode="output", view={"label": "Flood Risk Level"}, children={**pricing_layer_segmentation_table("Flood Risk Level")}),
            "wf_risk_category": hx.List(mode="output", view={"label": "Wildfire Risk Level"}, children={**pricing_layer_segmentation_table("Wildfire Risk Level")}),
            "scs_risk_category": hx.List(mode="output", view={"label": "Convective Risk Level"}, children={**pricing_layer_segmentation_table("Convective Risk Level")}),
            "marginal_impact_summary": hx.Structure(children={
                "mi_1_in_10_aep_pt": hx.Structure(view={"label": "1 in 10 AEP P&T"}, children={
                    "layer1": hx.Float(mode="output", view={"label": "L1 Premium"}),
                    "layer2": hx.Float(mode="output", view={"label": "L2 Premium"}),
                    "layer3": hx.Float(mode="output", view={"label": "L3 Premium"}),
                    "layer4": hx.Float(mode="output", view={"label": "L4 Premium"}),
                    "layer5": hx.Float(mode="output", view={"label": "L5 Premium"}),
                    "layer6": hx.Float(mode="output", view={"label": "L6 Premium"}),
                }),
                "mi_1_in_250_oep_pt": hx.Structure(view={"label": "1 in 250 OEP P&T"}, children={
                    "layer1": hx.Float(mode="output", view={"label": "L1 Premium"}),
                    "layer2": hx.Float(mode="output", view={"label": "L2 Premium"}),
                    "layer3": hx.Float(mode="output", view={"label": "L3 Premium"}),
                    "layer4": hx.Float(mode="output", view={"label": "L4 Premium"}),
                    "layer5": hx.Float(mode="output", view={"label": "L5 Premium"}),
                    "layer6": hx.Float(mode="output", view={"label": "L6 Premium"}),
                }),
            }),
            "show_file_component": hx.Bool(mode="input", default=False, async_output=["produce_heatmap_task"]),
            "heatmap_file": hx.File(mode="output", async_output=["produce_heatmap_task"], file_name="exposure-map.html", view={"label": "Exposure Map"}),
            "geojson": hx.Str(mode="input", optionality="optional", default=None, async_output=["create_regions_chart_task"], view={"read_only": True}),
            "show_regions_chart": hx.Bool(mode="input", optionality="optional", default=None, async_output=["create_regions_chart_task"], view={"read_only": True})
        })
    }

def pricing_layer_segmentation_table(name):
    return {
        "name": hx.Str(mode="output", view={"label": name}),
        "name_populated": hx.Bool(mode="output"),
        "tiv": hx.Float(mode="output", view={"label": "TIV", "format": thousands_format(mantissa=0)}),
        "num_locations": hx.Int(mode="output", view={"label": "Number of Locations", "format": thousands_format(mantissa=0)}),
        "gu_loss": hx.Float(mode="output", view={"label": "GU Loss", "format": thousands_format(mantissa=0)}),
        "gu_tech_rate": hx.Float(mode="output", view={"label": "GU Rate", "format": percent_format(mantissa=3)}),
        "gu_prem": hx.Float(mode="output", view={"label": "GU Premium", "format": thousands_format(mantissa=0)}),
        **{f"tech_prem_layer{i}": hx.Float(mode="output", view={"label": f"L{i} Pre UW Premium", "format": thousands_format(mantissa=0)}) for i in range(1,7)},
        **{f"uw_adj_tech_prem_layer{i}": hx.Float(mode="output", view={"label": f"L{i} Post UW Premium", "format": thousands_format(mantissa=0)}) for i in range(1,7)}
    }
