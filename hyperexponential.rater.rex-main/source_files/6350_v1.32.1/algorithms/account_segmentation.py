
import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap, MiniMap, Search, Geocoder, DualMap
import math
import hx


def account_segmentation_rater(hxd):
    mapping_dict = {
        "State/Country": "state",
        "Occupancy": "fire_occupancy",
        "Construction": "fire_construction",
        "WS Zone": "ws_zone",
        "DTC": "dtc",
        "Quake Zone": "eq_zone", 
    }

    for layer in hxd.layers:
        selected_graph = layer.segmentation_tables.table_selector

        for graph_option in mapping_dict:
            if selected_graph == graph_option:
                setattr(layer.segmentation_tables.show_segmentation_tables, mapping_dict[graph_option], True)
            else:
                setattr(layer.segmentation_tables.show_segmentation_tables, mapping_dict[graph_option], False)
                


def create_required_summary_tables(hxd, other_data):
    for path in [
        "state", 
        "country",
        "state_country",
        "state_country_choropleth",
        "fire_occupancy", 
        "ws_zone", 
        "eq_zone", 
        "fl_risk_category", 
        "wf_risk_category", 
        "scs_risk_category"
        ]:
        create_single_summary_table(hxd, other_data, path)


def create_single_summary_table(hxd, other_data, path):
    columns = ['name', 'tiv', "num_locations", "gu_loss", "gu_tech_rate", "gu_prem", "tech_prem", 'uw_adj_tech_prem']
    # join_columns = ['name', 'tiv', "num_locations", "gu_loss", "gu_tech_rate", "gu_prem"]
    
    df = pd.DataFrame(other_data[f"{path}_summary_layer1"])[columns].rename({
        "uw_adj_tech_prem": "uw_adj_tech_prem_layer1",
        "tech_prem": "tech_prem_layer1",
        }, axis=1)
    # TODO: This will display GU Loss, GU Rate and GU Premium for Layer 1 on Account Segmentation tab, even though these could vary between layers
    # Is this correct behaviour?

    for i in range(2, 7):
        if f"{path}_summary_layer{i}" in other_data.keys():
            df = df.merge(
                pd.DataFrame(other_data[f"{path}_summary_layer{i}"])[columns].rename({
                    "uw_adj_tech_prem": f"uw_adj_tech_prem_layer{i}",
                    "tech_prem": f"tech_prem_layer{i}",
                    }, axis=1
                )[
                    [
                        "name",
                        f"uw_adj_tech_prem_layer{i}",
                        f"tech_prem_layer{i}",
                    ]
                ], how="left", on=["name"])

    df["name_populated"] = ~(df["name"]=="")  
     
    other_data[f"segmentation_{path}"] = df.to_dict(orient="records")



def produce_heatmap(hxd, progress):
    '''
    Uses the folium package to generate a .html file of a World map, with the portfolio locations as the heat map,
    and the schedule locations as markers on the map.
    '''

    columns = [
        "loc_id", "street_name", "latitude", "longitude", "tiv_total"
        ]

    if hxd.policy_information.small_schedule_model:
        portfolio = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])

        portfolio["country"] = [x if x != "Georgia" else "Georgia (Country)" for x in [row.address_dropdown.country for row in hxd.schedule.schedule_table]]
        portfolio["state"] = [row.address_dropdown.state for row in hxd.schedule.schedule_table]
        portfolio["county"] = [row.address_dropdown.county for row in hxd.schedule.schedule_table]
        portfolio["city"] = [row.address_dropdown.city for row in hxd.schedule.schedule_table]

        us_state_code = pd.DataFrame(hx.params.us_state_code)[["US States", "US State Code"]].rename({
            "US States": 'state_name', 
            "US State Code": "state"
        }, axis=1)
        portfolio = portfolio.merge(us_state_code, how="left", on="state")

        portfolio = portfolio.rename({
            "loc_id": 'index', 
            "street_name": 'name', 
            # "state": 'zone', 
            "tiv_total": 'tiv'
        }, axis=1)

        portfolio['state_or_country'] = portfolio.apply(lambda row: row['state_name'] if row['country'] == "United States" else row['country'], axis=1)

        # Generate the base map
        #f_map = folium.Map(tiles=None, zoom_start=40, control_scale=True)
        f_map = folium.Map(tiles=None, zoom_start=5, control_scale=True)
        folium.TileLayer('openstreetmap', name='Light Mode').add_to(f_map)
        folium.TileLayer('stamentoner', name='Dark Mode').add_to(f_map)
        Geocoder().add_to(f_map)

        # TODO: is this a good idea?
        portfolio = portfolio.fillna(0.0)

        HeatMap(portfolio[["latitude", "longitude", "tiv"]], radius=50, name="Heat Map").add_to(f_map)


        # Add each location in the schedule to the map with its own custom marker
        # and a hyperlink to its Google Street View
        total_schedule_tiv = 0
        for index, location_info in portfolio.iterrows():
            if location_info['latitude'] and location_info['longitude']:
            
                tag = "" + str(location_info['name']) + ", " + str(millify(location_info['tiv']))
                total_schedule_tiv += location_info['tiv']

                marker = folium.Marker(
                    [location_info['latitude'], location_info['longitude']],
                    popup=generate_street_view_href(location_info['latitude'], location_info['longitude']) + tag + "</a>",
                )

                marker.add_to(f_map)

        
        # portfolio = portfolio.merge(hx.params.zone_to_state, how="left", on="zone")
        portfolio = portfolio.groupby('state_or_country').sum()['tiv'].reset_index()
        cp = folium.Choropleth(
                geo_data=read_geojson("./model/algorithms/account_segmentation/states_and_countries.json"),
                data=portfolio,
                columns=['state_or_country', 'tiv'],  
                key_on='feature.properties.NAME', 
                fill_color='YlOrRd',
                nan_fill_color="White",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name='Total TIV', 
                highlight=True,
                line_color='black',
                name="Choropleth",
                show=False
                )

        # creating a state indexed version of the dataframe so we can lookup values
        sov_df = pd.DataFrame([{"state_or_country": row[1].state_or_country, "total_tiv": row[1].tiv} for row in portfolio.iterrows()])
        # schedule = sov_df.merge(hx.params.zone_to_state, how="left", on="zone").groupby('state').sum()['total_tiv'].reset_index()
        schedule = sov_df.groupby('state_or_country').sum()['total_tiv'].reset_index()
        
        # looping thru the geojson object and adding a new property(unemployment)
        # and assigning a value from our dataframe
        for s in cp.geojson.data['features']:
            # state_tiv = portfolio[portfolio['state_or_country'] == s['properties']['NAME']]
            # if len(state_tiv) > 0:
            #     s['properties']['tiv'] = millify(state_tiv['tiv'].iloc[0])
            # else: 
            #     s['properties']['tiv'] = 0

            state_schedule_tiv = schedule[schedule['state_or_country'] == s['properties']['NAME']]
            if len(state_schedule_tiv) > 0:
                s['properties']['schedule_tiv'] = millify(state_schedule_tiv['total_tiv'].iloc[0])
            else: 
                s['properties']['schedule_tiv'] = 0
        
        # and finally adding a tooltip/hover to the choropleth's geojson
        folium.GeoJsonTooltip(fields=['NAME', 'schedule_tiv'], aliases=['State', 'Schedule TIV']).add_to(cp.geojson)
        cp.add_to(f_map) 
        folium.LayerControl(collapsed=True).add_to(f_map)

        

        # Add titles with key summarised figures to the map
        # insured_name_header = '''<h3 align="center" style="font-size:16px"><b>{}</b></h3>'''.format(hxd.input.quote_input.cedant)
        # total_portfolio_tiv_header = '''<h3 align="center" style="font-size:16px"><b>Total TIV in radius in portfolio: {}</b></h3>'''.format(millify(total_schedule_tiv))
        total_schedule_tiv_header = '''<h3 align="center" style="font-size:16px"><b>Total TIV in radius in schedule: {}</b></h3>'''.format(millify(portfolio["tiv"].sum()))

        # f_map.get_root().html.add_child(folium.Element(insured_name_header))
        # f_map.get_root().html.add_child(folium.Element(total_portfolio_tiv_header))
        f_map.get_root().html.add_child(folium.Element(total_schedule_tiv_header))
            
        # Save map down 
        f_map.save("map.html")

        # Load the map file, read it as html, convert to text
        with open("map.html") as map_html:
            txt = map_html.read()
            # soup = bs(txt)

        # Output the text to hxd.File
        with hxd.pricing_layer_segmentation.heatmap_file.open("t") as f:
            f.write(str(txt))

        hxd.pricing_layer_segmentation.show_file_component = True


def millify(n):
    '''
    Formats floats into readable strings to 1 decimal place, for example millify(10400500) = 10.4m
    '''

    millnames = ['','k','m','bn','tn']

    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.1f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def generate_street_view_href(latitude, longitude):
    return f"<a href=http://maps.google.com/?cbll={latitude},{longitude}&cbp=12,20.09,,0,5&layer=c>"


def read_geojson(geojson_path):

    import json
    with open(geojson_path) as f:
        data = json.load(f)

    return data
