# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from algorithms.rate_constants import (territory_notes, territory_labels, 
                                        incomplete_column, complete_column, profession_dict,
                                        exposure_rate_per_million_revenue_aec, exposure_rate_per_million_revenue_lpl,
                                        get_territory_groups_2)

nodes_1 = [
        "united_kingdom",
        "australia",
        "canada",
        "quebec",
        "ireland",
        "united_states",
        "asia_pac_south_africa",
        "europe",
        "middle_east",
        "tax_haven",
        "rest_of_world"
    ]

nodes_2 = [
    "united_kingdom",
    "australia",
    "canada",
    "quebec",
    "ireland",
    "united_states",
    "asia_pac_south_africa_country_sum",
    "europe_country_sum",
    "middle_east_country_sum",
    "tax_haven_country_sum",
    "rest_of_world_country_sum"
]

nodes_3 = [
    "united_kingdom",
    "australia",
    "canada",
    "quebec",
    "ireland",
    "united_states_state_sum",
    "asia_pac_south_africa",
    "europe",
    "middle_east",
    "tax_haven",
    "rest_of_world"
]

nodes_4 = [
    "united_kingdom",
    "australia",
    "canada",
    "quebec",
    "ireland",
    "united_states_state_sum",
    "asia_pac_south_africa_country_sum",
    "europe_country_sum",
    "middle_east_country_sum",
    "tax_haven_country_sum",
    "rest_of_world_country_sum"
]

node_map = {
    "united_kingdom":"united_kingdom",
    "australia":"australia",
    "canada": "canada",
    "quebec":"quebec",
    "ireland":"ireland",
    "united_states":"united_states",
    "united_states_state_sum":"united_states",
    "asia_pac_south_africa":"asia_pac_south_africa",
    "asia_pac_south_africa_country_sum":"asia_pac_south_africa",
    "europe":"europe",
    "europe_country_sum":"europe",
    "middle_east":"middle_east",
    "middle_east_country_sum":"middle_east",
    "tax_haven":"tax_haven",
    "tax_haven_country_sum":"tax_haven",
    "rest_of_world":"rest_of_world",
    "rest_of_world_country_sum":"rest_of_world",
}

def set_summary_label(hxd):
    if hxd.cds.profession == "Lawyers":
        label = "Please enter by Office Location"
    else:
        label = "Please enter by Project Location"

    hxd.cds.exposure.granular.territory.summary_label = label

def get_year_nodes(hxd):
    if hxd.cds.exposure.granular.territory.is_percentage_bool:
        year_nodes = ["year_0_pcnt", "year_1_pcnt","year_2_pcnt","year_3_pcnt","year_4_pcnt","year_5_pcnt"]
    else:
        year_nodes = ["year_0_value", "year_1_value","year_2_value","year_3_value","year_4_value","year_5_value"]

    return year_nodes

def set_table_bool(hxd):

    path = hxd.cds.exposure.granular.territory
    c_bool = path.bool_individual_country_level
    s_bool = path.bool_individual_state_level
    path.is_percentage_bool_not = not path.is_percentage_bool

    if path.is_percentage_bool:
        path.bool_incept_year_value = False
        path.bool_incept_year_pcnt = True if hxd.cds.exposure.granular.bool_show_inception_year_client_details_input else False
    else:
        path.bool_incept_year_pcnt = False
        path.bool_incept_year_value = True if hxd.cds.exposure.granular.bool_show_inception_year_client_details_input else False

    path.bool_table_1 = False
    path.bool_table_2 = False
    path.bool_table_3 = False
    path.bool_table_4 = False

    if (c_bool == False and s_bool == False):
        path.bool_table_1 = True
    elif (c_bool == True and s_bool == False):
        path.bool_table_2 = True
    elif (c_bool == False and s_bool == True):
        path.bool_table_3 = True
    else:
        path.bool_table_4 = True

def load_individual_countries_tbl(hxd):
    df = hx.params.ref_region_country
    hxd.cds.exposure.granular.territory.individual_countries.country = df["country"].to_dict()

def populate_territory_instructions(hxd):
    hxd.cds.exposure.granular.territory.instructions = territory_notes

def set_summary_modifier_labels(hxd):
    for key, value in territory_labels.items():
        setattr(hxd.cds.exposure.granular.territory.summary_modifier_labels, key, value)

def set_summary_year_labels(hxd):
    years = ["year_0", "year_1", "year_2", "year_3", "year_4", "year_5"]
    incept_date = hxd.hx_core.inception_date
    incept_year = incept_date.year

    for idx, year in enumerate(years):
        setattr(hxd.cds.exposure.granular.territory.summary_year_labels, year, incept_year - idx)

def summary_totals(hxd):
    years = get_year_nodes(hxd)
    path = hxd.cds.exposure.granular.territory

    if path.bool_table_1: nodes=nodes_1
    elif path.bool_table_2: nodes=nodes_2
    elif path.bool_table_3: nodes=nodes_3
    else: nodes=nodes_4

    # Totals
    year_total_dict = {}
    for year in years:
        total = 0
        for node in nodes:
            total += (getattr(getattr(path.summary, node), year) or 0)
        
        year_total_dict[year] = total #record the total
        year_label = getattr(hxd.cds.exposure.granular.territory.summary_year_labels, year[:6])

        if path.is_percentage_bool:
            setattr(getattr(path.summary, "total"), year, total)
            if round(total,2) == 1:
                setattr(hxd.cds.exposure.granular.territory.summary_year_total_labels, year[:6], f"{year_label}{complete_column}")
            elif total == 0:
                setattr(hxd.cds.exposure.granular.territory.summary_year_total_labels, year[:6], f"{year_label}")
            else:
                hx.errors.validation(f"Territory total for year {year_label} is not equal to 100%")
                setattr(hxd.cds.exposure.granular.territory.summary_year_total_labels, year[:6], f"{year_label}{incomplete_column}")
        else:
            if total > 0:
                setattr(getattr(path.summary, "total"), year, 1)
                setattr(hxd.cds.exposure.granular.territory.summary_year_total_labels, year[:6], f"{year_label}{complete_column}")
            else:
                setattr(getattr(path.summary, "total"), year, 0)
                setattr(hxd.cds.exposure.granular.territory.summary_year_total_labels, year[:6], f"{year_label}")
    
    # Weighted Summary
    profession_index = profession_dict[(hxd.cds.profession or "Lawyers")]

    # For territory loadings display
    df_territory_loadings = hx.params.ref_lpl_territory_loading if hxd.cds.profession == "Lawyers" else hx.params.ref_ae_territory_loading

    # Raw Weights
    df_weights = hx.params.ref_exposure_weightings
    df_weights = df_weights.iloc[::-1]   #reverse to get the correct index
    # check year totals - if they are zero then zero out the weight for that year
    for year in years:
        year_index = years.index(year)
        if getattr(path.summary.total, year) == 0:
            df_weights.iloc[year_index] = 0

    # Reallocate weightings
    df_weights = df_weights/df_weights.sum().replace(0,1)

    nodes.append("total")
    for node in nodes:
        total = 0
        for year in years:
            year_index = years.index(year)
            value = getattr(getattr(path.summary, node), year) 
            if path.is_percentage_bool:
                total += (value or 0) * (df_weights.iloc[year_index, profession_index] or 0)
            else:
                if node=="total":
                    total = 1
                else:
                    total += 0 if year_total_dict[year] == 0 else (value or 0)/year_total_dict[year] * (df_weights.iloc[year_index, profession_index] or 0)

        setattr(getattr(path.summary, node), "weighted", total)
        
        if node != "total":
            setattr(getattr(path.summary, node), "frequency", df_territory_loadings[df_territory_loadings["Territory"]==node_map[node]]["Frequency"].iloc[0])
            setattr(getattr(path.summary, node), "severity", df_territory_loadings[df_territory_loadings["Territory"]==node_map[node]]["Severity"].iloc[0])

def write_to_reporting_nodes(hxd):
    years = get_year_nodes(hxd)
    years.append("weighted")
    path = hxd.cds.exposure.granular.territory

    if path.bool_table_1: nodes=nodes_1
    elif path.bool_table_2: nodes=nodes_2
    elif path.bool_table_3: nodes=nodes_3
    else: nodes=nodes_4 

    nodes.remove("total")           #added in summary_totals

    for year in years:
        for node in nodes:
            setattr(getattr(path.summary, f"{node_map[node]}_reporting" ), year, getattr(getattr(path.summary, node), year))

def sum_state_by_year(hxd):
    total_y0 = 0; total_y1 = 0; total_y2 = 0; total_y3 = 0; total_y4 = 0; total_y5 = 0

    if hxd.cds.exposure.granular.territory.is_percentage_bool:
        #loop through the list entries
        for entry in hxd.cds.exposure.granular.territory.state:
            total_y0 += entry.year_0_pcnt or 0
            total_y1 += entry.year_1_pcnt or 0
            total_y2 += entry.year_2_pcnt or 0
            total_y3 += entry.year_3_pcnt or 0
            total_y4 += entry.year_4_pcnt or 0
            total_y5 += entry.year_5_pcnt or 0

        # Set the state total amounts
        summary = hxd.cds.exposure.granular.territory.summary.united_states_state_sum
        summary.year_0_pcnt = total_y0
        summary.year_1_pcnt = total_y1
        summary.year_2_pcnt = total_y2
        summary.year_3_pcnt = total_y3
        summary.year_4_pcnt = total_y4
        summary.year_5_pcnt = total_y5
    else:
        for entry in hxd.cds.exposure.granular.territory.state:
            total_y0 += entry.year_0_value or 0
            total_y1 += entry.year_1_value or 0
            total_y2 += entry.year_2_value or 0
            total_y3 += entry.year_3_value or 0
            total_y4 += entry.year_4_value or 0
            total_y5 += entry.year_5_value or 0

        # Set the state total amounts
        summary = hxd.cds.exposure.granular.territory.summary.united_states_state_sum
        summary.year_0_value = total_y0
        summary.year_1_value = total_y1
        summary.year_2_value = total_y2
        summary.year_3_value = total_y3
        summary.year_4_value = total_y4
        summary.year_5_value = total_y5       

def sum_country_by_year(hxd):
    regions = [
        "Rest of World",
        "Tax Haven",
        "Europe (high risk)",
        "Middle East (high risk)",
        "Asia Pac (Developed) & South Africa"
        ]

    region_dict= {
        region: {f"year_{i}": 0 for i in range(6)}
        for region in regions
    }

    years = get_year_nodes(hxd)

    # Calculate the region totals
    for entry in hxd.cds.exposure.granular.territory.individual_countries:
        if entry.region in regions:
            for year in years:
                region_dict[entry.region][year[:6]] += (getattr(entry, year) or 0)

    region_summary_dict={
        "asia_pac_south_africa_country_sum":"Asia Pac (Developed) & South Africa",
        "europe_country_sum":"Europe (high risk)",
        "middle_east_country_sum": "Middle East (high risk)",
        "tax_haven_country_sum":"Tax Haven",
        "rest_of_world_country_sum":"Rest of World"
    }

    # Set the summary values
    for key, value in region_summary_dict.items():
        for year in years:
            setattr(getattr(hxd.cds.exposure.granular.territory.summary, key), year, region_dict[value][year[:6]])

def populate_loss_cost_chart(hxd):
    exp_rate = exposure_rate_per_million_revenue_lpl if hxd.cds.profession == "Lawyers" else exposure_rate_per_million_revenue_aec
    summary = hxd.cds.exposure.granular.territory.summary
    expected_exposure = hxd.cds.exposure.granular.exposure_expected_current_year

    for territory_key in get_territory_groups_2():
        rate = exp_rate.get(territory_key)
        if rate is None:
            continue

        territory_node = getattr(summary, territory_key, None)
        if territory_node is None:
            continue

        territory_node.expected_loss_cost = rate * expected_exposure / 1e6

def rate_territory(hxd):
    set_summary_label(hxd)
    set_table_bool(hxd)
    populate_territory_instructions(hxd) 
    set_summary_modifier_labels(hxd)
    set_summary_year_labels(hxd)
    sum_country_by_year(hxd)
    sum_state_by_year(hxd)
    populate_loss_cost_chart(hxd)
    summary_totals(hxd)
    write_to_reporting_nodes(hxd)
