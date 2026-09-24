# v0.5.0
import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term, yearfrac
from operator import itemgetter
from algorithms.rate_constants import (exposure_details_notes, get_inflation_tables, client_details_notes, 
    project_type_map, incomplete_column, complete_column, profession_dict, project_type_parent_categories, get_aop_aec_parent_categories, get_aop_lpl_parent_categories)
import datetime

def populate_notes(hxd):
    hxd.cds.exposure.granular.client_details_lawyers.notes = client_details_notes
    hxd.cds.exposure.granular.client_details_AEC.notes = client_details_notes

def set_table_bools(hxd):
    path = hxd.cds.exposure.granular.client_details_lawyers
    path.bool_is_pcnt_not = not path.bool_is_pcnt

    path = hxd.cds.exposure.granular.client_details_AEC
    path.bool_aop_is_pcnt_not = not path.bool_aop_is_pcnt
    path.bool_ipt_is_pcnt_not = not path.bool_ipt_is_pcnt
    path.bool_ipt_enter_at_level_not = not path.bool_ipt_enter_at_level

def get_years_list(is_pcnt: bool):
    years_pcnt = ["year_0_pcnt", "year_1_pcnt","year_2_pcnt","year_3_pcnt","year_4_pcnt","year_5_pcnt"]
    years_value = ["year_0_value", "year_1_value","year_2_value","year_3_value","year_4_value","year_5_value"] 
    if is_pcnt:
        return years_pcnt
    else:
        return years_value

def AEC_ipt_summary_totals(hxd):
    nodes_1 = [
        "airport_runways",
        "arenas_stadiums_convention_centers",
        "bridges_tunnels",
        "chemical_pharmaceutical_plants",
        "dams_harbours_jetties_wetland_mitigation",
        "hospitals",
        "mining",
        "modular_buildings",
        "oil_refineries_pipelines_powerplants",
        "parking_garages",
        "processing_treatment",
        "residential_buildings_high_rise",
        "warehouses_data_centres",
        "residential_buildings_low_rise",
        "institutional_lower_risk_output",
        "recreational_lower_risk_output",
        "general_building_lower_risk_output",
        "infrastructure_lower_risk_output",
        "industrial_lower_risk_output",
        "environmental_lower_risk_output"
    ]
    nodes_2 = [
        "airport_runways",
        "arenas_stadiums_convention_centers",
        "bridges_tunnels",
        "chemical_pharmaceutical_plants",
        "dams_harbours_jetties_wetland_mitigation",
        "hospitals",
        "mining",
        "modular_buildings",
        "oil_refineries_pipelines_powerplants",
        "parking_garages",
        "processing_treatment",
        "residential_buildings_high_rise",
        "warehouses_data_centres",
        "residential_buildings_low_rise",
        "institutional_lower_risk_input",
        "recreational_lower_risk_input",
        "general_building_lower_risk_input",
        "infrastructure_lower_risk_input",
        "industrial_lower_risk_input",
        "environmental_lower_risk_input"
    ]

    sub_nodes = {
        "institutional_lower_risk_output": [
            "churches",
            "colleges_universities_schools",
            "convalescent_retirement_facilities",
            "correctional_facilities_jails",
            "courthouses",
            "institutional_other",
            "military"
        ],
        "recreational_lower_risk_output": [
            "amusement_park",
            "casinos",
            "parks_playgrounds_pools",
            "recreational_other",
            "sports_facilities"           
        ],
        "general_building_lower_risk_output":[
            "airport_terminals",
            "general_building_other",
            "hotels_motels",
            "libraries_museums",
            "offices",
            "retail_malls_shopping_centers_restaurants"           
        ],
        "infrastructure_lower_risk_output":[
            "infrastructure_other",
            "rail",
            "roads",
            "utilities"            
        ],
        "industrial_lower_risk_output":[
            "industrial_other",
            "manufacturing_facilities",
            "nuclear_facilities"           
        ],
        "environmental_lower_risk_output":[
            "asbestos_abatement",
            "environmental_other",
            "waste_brokering"
        ]
    }


    path = hxd.cds.exposure.granular.client_details_AEC
    wt_threshold = path.weighted_pcnt_filter_value or 0
    years = get_years_list(path.bool_ipt_is_pcnt)
    nodes = nodes_1 if path.bool_ipt_enter_at_level else nodes_2

    #SubTotals
    sub_total_fields = [
        "institutional_lower_risk_output",
        "recreational_lower_risk_output",
        "general_building_lower_risk_output",
        "infrastructure_lower_risk_output",
        "industrial_lower_risk_output",
        "environmental_lower_risk_output"
    ]

    is_negative_check = False
    for year in years:
        for field in sub_total_fields:
            total = 0
            for key, value in project_type_map.items():
                if value["parent"] == field:
                    if (getattr(getattr(path.individual_project_types, key), year) or 0) < 0:
                        is_negative_check = True

                    total += (getattr(getattr(path.individual_project_types, key), year) or 0)

            setattr(getattr(path.individual_project_types, field), year, total)

    # Totals
    year_total_dict = {}
    for year in years:
        total = 0
        for node in nodes:
            if (getattr(getattr(path.individual_project_types, node), year) or 0) < 0:
                is_negative_check = True
            total += (getattr(getattr(path.individual_project_types, node), year) or 0)
        
        year_total_dict[year] = total #record the total
        year_label = getattr(hxd.cds.exposure.granular.territory.summary_year_labels, year[:6]) # this is ok - same labels
        
        # if path.bool_ipt_is_pcnt:
        #     setattr(getattr(path.individual_project_types, "total"), year, total)
        #     if round(total,2) == 1:
        #         setattr(path.summary_year_total_ipt_labels, year[:6], f"{year_label}{complete_column}")
        #     elif total == 0:
        setattr(path.summary_year_total_ipt_labels, year[:6], f"{year_label}")
        #     else:
        #         hx.errors.validation(f"AEC IPT total for year {year_label} is not equal to 100%")
        #         setattr(path.summary_year_total_ipt_labels, year[:6], f"{year_label}{incomplete_column}")
        # else:
        #     if total > 0:
        #         setattr(getattr(path.individual_project_types, "total"), year, 1)
        #         setattr(path.summary_year_total_ipt_labels, year[:6], f"{year_label}{complete_column}")
        #     else:
        #         setattr(getattr(path.individual_project_types, "total"), year, 0)
        #         setattr(path.summary_year_total_ipt_labels, year[:6], f"{year_label}")

    # Weighted Summary
    profession_index = profession_dict[(hxd.cds.profession or "Lawyers")]

    # Raw Weights
    df_weights = hx.params.ref_exposure_weightings
    df_weights = df_weights.iloc[::-1]   #reverse to get the correct index
    # check year totals - if they are zero then zero out the weight for that year
    for year in years:
        year_index = years.index(year)
        if getattr(path.individual_project_types.total, year) == 0:
            df_weights.iloc[year_index] = 0

    # Reallocate weightings
    df_weights = df_weights/df_weights.sum().replace(0,1)

    # Loadings Table   Project Type,Frequency,Severity
    df_loadings = hx.params.ref_ae_pt_loading

    nodes.append("total")
    for node in nodes:
        total = 0
        for year in years:
            year_index = years.index(year)
            value = getattr(getattr(path.individual_project_types, node), year) 
            if path.bool_ipt_is_pcnt:
                total += (value or 0) * (df_weights.iloc[year_index, profession_index] or 0)
            else:
                if node == "total":
                    total = 1
                else:
                    total += 0 if year_total_dict[year] == 0 else (value or 0)/year_total_dict[year] * (df_weights.iloc[year_index, profession_index] or 0)

        setattr(getattr(path.individual_project_types, node), "weighted", total)

        # freq sev loadings here
        if node != "total":
            mask = df_loadings["Project Type"] == project_type_map[node]["label"]
            df_loadings_filtered = df_loadings[mask]
            if not df_loadings_filtered.empty:
                setattr(getattr(path.individual_project_types, node), "frequency", df_loadings_filtered["Frequency"].iloc[0]) 
                setattr(getattr(path.individual_project_types, node), "severity", df_loadings_filtered["Severity"].iloc[0]) 

        if total >= wt_threshold:
            setattr(getattr(path.individual_project_types, node), "filter", True)
        else:
            setattr(getattr(path.individual_project_types, node), "filter", False)

    for key_node, sub_node_items in sub_nodes.items():
        filter_bool = getattr(getattr(path.individual_project_types, key_node), "filter")
        for node in sub_node_items:
            setattr(getattr(path.individual_project_types, node), "filter", filter_bool)

    if is_negative_check:
        hx.errors.validation("There are negative values in the Individual Project Type table in the Client Details - AEC page")

def weights_where_grid_is_list(hxd, path, is_pcnt_bool: bool, year_total_dict):
    # Weighted Summary
    profession_index = profession_dict[(hxd.cds.profession or "Lawyers")]

    # Ladoings DataFrame
    df_loadings = hx.params.ref_lpl_aop_loading if hxd.cds.profession == "Lawyers" else hx.params.ref_ae_aop_loading

    # Raw Weights
    df_weights = hx.params.ref_exposure_weightings
    df_weights = df_weights.iloc[::-1]   #reverse to get the correct index
    # check year totals - if they are zero then zero out the weight for that year
    years = get_years_list(is_pcnt_bool)
    for year in years:
        year_index = years.index(year)
        if getattr(path.areas_of_practice_total, year) == 0:
            df_weights.iloc[year_index] = 0

    # Reallocate weightings
    df_weights = df_weights/df_weights.sum().replace(0,1)

    for entry in path.areas_of_practice:
        total = 0
        for year in years:
            year_index = years.index(year)
            value = getattr(entry, year)
            if is_pcnt_bool:
                total += (value or 0) * (df_weights.iloc[year_index, profession_index] or 0)
            else:
                total += 0 if year_total_dict[year] == 0 else (value or 0)/year_total_dict[year] * (df_weights.iloc[year_index, profession_index] or 0)
        entry.weighted = total

        # Loadings
        df_loadings_filtered = df_loadings[df_loadings["Area of Practice"]==entry.areas_of_practice]
        if not df_loadings_filtered.empty:
            entry.frequency = df_loadings_filtered["Frequency"].iloc[0]
            entry.severity = df_loadings_filtered["Severity"].iloc[0]

        # Set laodings

    total = 0
    for year in years:
        year_index = years.index(year)
        value = getattr(path.areas_of_practice_total, year)
        total += value * (df_weights.iloc[year_index, profession_index] or 0)
    path.areas_of_practice_total.weighted = total


def AEC_aop_totals(hxd):
    path = hxd.cds.exposure.granular.client_details_AEC
    total = hxd.cds.exposure.granular.client_details_AEC.areas_of_practice_total
    total_y0 = 0; total_y1 = 0; total_y2 = 0; total_y3 = 0; total_y4 = 0; total_y5 = 0
    year_pcnt_list = ["year_0_pcnt", "year_1_pcnt", "year_2_pcnt", "year_3_pcnt", "year_4_pcnt", "year_5_pcnt"]
    year_value_list = ["year_0_value", "year_1_value", "year_2_value", "year_3_value", "year_4_value", "year_5_value"]

    # Loadings Table   Area of Practice,Frequency,Severity
    df_loadings = hx.params.ref_ae_aop_loading

    is_negative_check = False
    #loop through the list entries
    if path.bool_aop_is_pcnt:
        for entry in path.areas_of_practice:

            for node in year_pcnt_list:
                if (getattr(entry, node) or 0) < 0:
                    is_negative_check = True

            total_y0 += entry.year_0_pcnt or 0
            total_y1 += entry.year_1_pcnt or 0
            total_y2 += entry.year_2_pcnt or 0
            total_y3 += entry.year_3_pcnt or 0
            total_y4 += entry.year_4_pcnt or 0
            total_y5 += entry.year_5_pcnt or 0

        # Set the aop total amounts
        # total.year_0_pcnt = total_y0
        # total.year_1_pcnt = total_y1
        # total.year_2_pcnt = total_y2
        # total.year_3_pcnt = total_y3
        # total.year_4_pcnt = total_y4
        # total.year_5_pcnt = total_y5

        results_dict = {
            "year_0_pcnt": total_y0,
            "year_1_pcnt": total_y1,
            "year_2_pcnt": total_y2,
            "year_3_pcnt": total_y3,
            "year_4_pcnt": total_y4,
            "year_5_pcnt": total_y5
        }

    else:
        for entry in path.areas_of_practice:

            for node in year_value_list:
                if (getattr(entry, node) or 0) < 0:
                    is_negative_check = True

            total_y0 += entry.year_0_value or 0
            total_y1 += entry.year_1_value or 0
            total_y2 += entry.year_2_value or 0
            total_y3 += entry.year_3_value or 0
            total_y4 += entry.year_4_value or 0
            total_y5 += entry.year_5_value or 0
    
        # Set the aop total amounts
        # total.year_0_value = 1 if total_y0 > 0 else 0
        # total.year_1_value = 1 if total_y1 > 0 else 0
        # total.year_2_value = 1 if total_y2 > 0 else 0
        # total.year_3_value = 1 if total_y3 > 0 else 0
        # total.year_4_value = 1 if total_y4 > 0 else 0
        # total.year_5_value = 1 if total_y5 > 0 else 0

        results_dict = {
            "year_0_value": total_y0,
            "year_1_value": total_y1,
            "year_2_value": total_y2,
            "year_3_value": total_y3,
            "year_4_value": total_y4,
            "year_5_value": total_y5
        }

    year_total_dict = {}
    for year, total_value in results_dict.items():
        
        year_total_dict[year] = total_value
        year_trimmed = year[:6]
        year_label = getattr(hxd.cds.exposure.granular.territory.summary_year_labels, year_trimmed)

        if path.bool_aop_is_pcnt:
            if round(total_value, 2) == 1: 
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{complete_column}")
            elif total_value == 0:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}")
            else:
                #hx.errors.validation(f"AEC AOP total for year {year_label} is not equal to 100%")
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{incomplete_column}")
        else:
            if total_value > 0:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{complete_column}")
            else:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}")

    weights_where_grid_is_list(hxd, path, path.bool_aop_is_pcnt, year_total_dict) 
    if is_negative_check:
        hx.errors.validation("There are negative values in the AOP table in the Client Details - AEC page")       

def lawyers_aop_totals(hxd):
    path = hxd.cds.exposure.granular.client_details_lawyers
    total = hxd.cds.exposure.granular.client_details_lawyers.areas_of_practice_total
    total_y0 = 0; total_y1 = 0; total_y2 = 0; total_y3 = 0; total_y4 = 0; total_y5 = 0
    year_pcnt_list = ["year_0_pcnt", "year_1_pcnt", "year_2_pcnt", "year_3_pcnt", "year_4_pcnt", "year_5_pcnt"]
    year_value_list = ["year_0_value", "year_1_value", "year_2_value", "year_3_value", "year_4_value", "year_5_value"]

    # Loadings Table   Area of Practice,Frequency,Severity
    df_loadings = hx.params.ref_lpl_aop_loading

    is_negative_check = False
    #loop through the list entries
    if path.bool_is_pcnt:
        for entry in path.areas_of_practice:
            
            for node in year_pcnt_list:
                x = getattr(entry, node)
                if (x or 0) < 0:
                    is_negative_check = True

            total_y0 += entry.year_0_pcnt or 0
            total_y1 += entry.year_1_pcnt or 0
            total_y2 += entry.year_2_pcnt or 0
            total_y3 += entry.year_3_pcnt or 0
            total_y4 += entry.year_4_pcnt or 0
            total_y5 += entry.year_5_pcnt or 0

        # Set the aop total amounts
        # total.year_0_pcnt = total_y0
        # total.year_1_pcnt = total_y1
        # total.year_2_pcnt = total_y2
        # total.year_3_pcnt = total_y3
        # total.year_4_pcnt = total_y4
        # total.year_5_pcnt = total_y5

        results_dict = {
            "year_0_pcnt": total_y0,
            "year_1_pcnt": total_y1,
            "year_2_pcnt": total_y2,
            "year_3_pcnt": total_y3,
            "year_4_pcnt": total_y4,
            "year_5_pcnt": total_y5
        }

    else:
        for entry in path.areas_of_practice:

            for node in year_value_list:
                if (getattr(entry, node) or 0) < 0:
                    is_negative_check = True

            total_y0 += entry.year_0_value or 0
            total_y1 += entry.year_1_value or 0
            total_y2 += entry.year_2_value or 0
            total_y3 += entry.year_3_value or 0
            total_y4 += entry.year_4_value or 0
            total_y5 += entry.year_5_value or 0
    
        # Set the aop total amounts
        # total.year_0_value = 1 if total_y0 > 0 else 0
        # total.year_1_value = 1 if total_y1 > 0 else 0
        # total.year_2_value = 1 if total_y2 > 0 else 0
        # total.year_3_value = 1 if total_y3 > 0 else 0
        # total.year_4_value = 1 if total_y4 > 0 else 0
        # total.year_5_value = 1 if total_y5 > 0 else 0

        results_dict = {
            "year_0_value": total_y0,
            "year_1_value": total_y1,
            "year_2_value": total_y2,
            "year_3_value": total_y3,
            "year_4_value": total_y4,
            "year_5_value": total_y5
        }

    year_total_dict = {}
    for year, total_value in results_dict.items():

        year_total_dict[year] = total_value
        year_trimmed = year[:6]
        year_label = getattr(hxd.cds.exposure.granular.territory.summary_year_labels, year_trimmed)

        if path.bool_is_pcnt:
            if round(total_value, 2) == 1: 
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{complete_column}")
            elif total_value == 0:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}")           
            else:
                #hx.errors.validation(f"Lawyers AOP total for year {year_label} is not equal to 100%")
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{incomplete_column}")
        else:
            if total_value > 0:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}{complete_column}")
            else:
                setattr(path.summary_year_total_aop_labels, year_trimmed, f"{year_label}")          

    weights_where_grid_is_list(hxd, path, path.bool_is_pcnt, year_total_dict)
    if is_negative_check:
        hx.errors.validation("There are negative values in the AOP table in the Client Details - Lawyers page")    

def populate_aop_chart(hxd, lawyers_bool):
    if lawyers_bool:
        categories = get_aop_lpl_parent_categories()
        path = hxd.cds.exposure.granular.client_details_lawyers.areas_of_practice_chart
    else:
        categories = get_aop_aec_parent_categories()
        path = hxd.cds.exposure.granular.client_details_AEC.areas_of_practice_chart

    for node in categories:
        setattr(getattr(path, node), "expected_loss_cost", 100)

def populate_ipt_chart(hxd):
    categories = project_type_parent_categories
    path = hxd.cds.exposure.granular.client_details_AEC.individual_project_types_chart

    for node in categories:
        setattr(getattr(path, node), "expected_loss_cost", 100)

def rate_client_details(hxd):
    populate_notes(hxd)
    set_table_bools(hxd)
    if hxd.cds.profession_lawyers_bool:
        lawyers_aop_totals(hxd)
    else:
        AEC_ipt_summary_totals(hxd)
        AEC_aop_totals(hxd)
        populate_ipt_chart(hxd)
    populate_aop_chart(hxd, hxd.cds.profession_lawyers_bool)