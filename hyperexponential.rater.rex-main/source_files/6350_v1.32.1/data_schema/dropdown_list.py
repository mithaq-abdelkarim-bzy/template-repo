'''
File that stores dropdown list used in data schema
'''

### Policy Info page

# Section Policy Information
new_renewal_list = ["", "New", "Renewal"]

status_list = ["", "Quote", "Quote Released", "Bound", "MTA", "Cancellation", "Not Taken Up"]

cyber_cover_list = ["", "None", "LMA 5400", "LMA 5401", "LMA 5426", "NMA 2914 (Unamended)", "NMA 2914 (Amended)", 
                    "NMA 2915 (Unamended)", "NMA 2915 (Amended)", "CL 380", "Other"]

# Section Layers
elt_for_sim_list = ["GU", "GR"]

# Section Deductibles
ded_region_list = ["All", "State", "Tier"]

ded_type_list = ["Percentage with a $ minimum",
                    "Fixed $ amount",
                    "Percentage uncapped",
                    "No deductible",
                    "Percentage capped by $ amount"]

ws_tier_list = ["FL", "FL Tri County and Keys Only", "FL Tri County Only", "Tier 1: FL",
                    "Tier 1: NorthEast", "Tier 1: TX - ME", "Tier 1: TX - NC (Exc Harris)",
                    "Tier 1: TX - NC (Inc Harris)", "Tier 1: TX - VA (Exc Harris)",
                    "Tier 1: TX - VA (Inc Harris)", "Tier 2: FL", "Tier 2: TX - VA"]

scs_tier_list = ["CO, KS, MO, NE, OK, SD, TX", 
                    "AR, IA, IL, IN, MN, MT, ND, SD, WY",
                    "AR, CO, IA, IL, IN, KS, MN, MO, MT, ND, NE, OK, SD, TX, WY"]

fl_region_list = ["All", "State", "FEMA Zone"]

fl_fema_zone_list = ["All A and V", "All B and X Shaded", "All X and C"]

eq_tier_list = ["CA A and B", "CA All Other", "South East", "Great Basin", 
                    "NM", "PNW Counties", "PNW"] 

# Rationale Page
insurance_type_list = ["", "QS", "Primary", "XOL"]


### Schedule Page

schedule_peril_covered_list = ["From Layer", "True", "False"]

schedule_soil_type_list = ["Rock", "Rock to Soft Rock", "Soft Rock", "Soft Rock to Stiff Soil",
                            "Soft Soil", "Stiff Soil", "Stiff to Soft Soil", "Very Soft Soil", "Unknown"]

schedule_liquefaction_list = ["High", "High to Very High", "Low", "Low to Moderate", "Moderate", "Moderate to High",
                                "Very High", "Very Low", "Very Low to Low", "Unknown"]

schedule_landslide_list = schedule_liquefaction_list

schedule_eq_const_qual_list = ["Unknown", "Good", "Average", "Poor"]

schedule_plan_irregularity_list = ["Unknown", "Regular", "Irregular"]

schedule_soft_story_list = ["Unknown", "No", "Yes"]

schedule_vertical_irregularity_list = schedule_soft_story_list

schedule_ornamentation_list = ["Unknown", "Little or None", "Average", "Extensive"]

schedule_equipment_eq_bracing_list = ["Unknown", "Generally Well-Braced", "Somewhat Braced", "Generally Unbraced"]

schedule_equipment_support_maintenance_list = ["Unknown", "No Signs of Fatigue / Good Maintenance", "Few Signs of Fatigue / Average Maintenance", "Obvious Signs of Fatigue / Poor Maintenance"]

schedule_pounding_list = schedule_soft_story_list

schedule_ws_const_qual_list = ["Unknown", "Obvious signs of deterioration or distress", "Certified design & construction"]

schedule_roof_anchor_list = ["Unknown", "Toe nailing or no anchorage", "Clips", "Single wraps", "Double wraps", "Structural"]

schedule_roof_equip_hurricane_bracing_list = ["Unknown", "Properly installed with adequate anchorage", "Obvious signs of deficiencies in the installation", "No equipment present"]

schedule_cladding_type_list = ["Unknown", "Brick Veneer", "Metal Sheathing", "Wood", "EIFS", "Impact rated glazing", "Glazing not designed for impact WITH gravel rooftop within 1,000 ft", 
                                "Glazing not designed for impact without gravel rooftop within 1,000 ft", "Vinyl siding", "Stucco", "None"]

schedule_frame_foundation_connection_list = ["Unknown", "Bolted", "Unbolted", "Engineered"]

schedule_river_flood_zone_code = ["No Data", "X", "X500L", "X500", "AE", "D", "A", "AH", "ANI", "A99", "SR_GFZ3_50", "SR_GFZ3_500", "SR_GFZ3_200", "SR_GFZ3_100", "AO", "VE"]

schedule_river_flood_zone_schema = ["NFHL_FEMA_SR", "SR_GFZ3"]

# schedule_fema_flood_risk = ["X Minimal Zones","Area not evaluated by FEMA","X Moderate Zones","A Zones","D Undetermined","V Zones", "Open Water"]

# schedule_fema_flood_zone = ["X","AREA NOT INCLUDED","AE","D","A","AH","A99", "AO", "VE", "OPEN WATER"]

# schedule_fema_flood_subzone = ["AREA OF MINIMAL FLOOD HAZARD", "AREA WITH REDUCED FLOOD RISK DUE TO LEVEE", "500", "FLOODWAY", "1 PCT FUTURE CONDITIONS", "ADMINISTRATIVE FLOODWAY", "COMMUNITY ENCROACHMENT AREA"]

# schedule_fema_flood_combined_zone = ["X AREA OF MINIMAL FLOOD HAZARD" ,"AREA NOT INCLUDED" ,"X AREA WITH REDUCED FLOOD RISK DUE TO LEVEE" ,"X 500" ,"AE" ,"D" ,"A" ,"X" ,"AH" ,"A99" ,"AE FLOODWAY", "AO", "VE", "X 1 PCT FUTURE CONDITIONS", "A99 AREA WITH REDUCED FLOOD RISK DUE TO LEVEE", "AE ADMINISTRATIVE FLOODWAY", "AE COMMUNITY ENCROACHMENT AREA", "OPEN WATER"]

schedule_surge_flood_label = ["Moderate", "High", "Minimal", "Moderately High", "Negligible", "Low", "Moderately Low", "Very Low", "Very High", "Extreme"]

schedule_flood_rank_text = ["Minimal", "Medium", "Low", "High"]

schedule_flood_label = ["Minimal", "Moderately High", "Very Low", "Moderately Low", "Negligible", "Low", "High", "Extreme", "Moderate", "Very High"]

# Summary
# climate_perils is also duplicated in algorithms/climate_peril_selection.py, due to hx limitations we can't import it directly
climate_perils = ["Hurricane", "Flood"]

climate_aware_response = ["Yes", "No"]

climate_protection_measures_response = [
    "1", 
    "2", 
    "3", 
    "4", 
    "5"
    ]
# climate_awareness_response = [
#     "Is the insured aware of the climate related risks they are exposed to?"
# ]

# climate_protection_measures_response = [
#     "No awareness of the risks, therefore, not prepared", 
#     "Understand the risks but no action taken to embed mitigation practices into business as usual processes", 
#     "Understand the risks, and the business is beginning to give consideration to climate-related risks, however, there are insufficient protection measures in place to manage the impact of a climate risk event", 
#     "Understand the risks, the business has given full consideration to climate-related risks, and has begun to action projects to mitigate the impact of climate related risks", 
#     "Understand the risks arising from climate-related matters. There are physical protection measures in place to limit the impact from climate related risks, and emergency responses to climate-related risks are embedded in business as usual process"
#     ]