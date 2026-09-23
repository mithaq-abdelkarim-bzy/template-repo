import hx

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6

benchmark_lr = 0.7

all_perils = ["aop","wildfire", "liability", "ws", "eq", "fl", "paf", "eb"]

all_perils_dict = {
    "aop":"AOP",
    "liability":"Liability",
    "ws":"WS",
    "eq":"EQ",
    "fl":"Excess FL",
    "wildfire":"Wildfire",
    "paf":"PAF",
    "eb":"Equipment breakdown"
    }

aop_sub_perils = [
    "WaterDamage",
    "Hail",
    "Wind",
    "Other",
    "RoofDamageLeak",
    "Theft",
    "Lightning",
    "Fire",
    "IceSnowDamage",
    "PowerSurge",
    "WinterStorm"
]

deductible_type_mapping = {
    "AOP": [],
    "Percentage (%)": [3, 5, 10, 20, 25, 50, 75],
    "Dollar ($)": [100000, 250000, 500000, 750000, 1000000, 2500000, 5000000, 10000000, 15000000, 25000000],
    "Excluded": []
}

excluded_blanket_variables = {"audio_visual_equipment", "bicycles", "computers", "misc"}
specific_schedules_tuples = [
    ("Cameras", "Scheduled - Professional Use", "cameras_scheduled_professional_use"),
    ("Cameras", "Scheduled - Personal Use", "cameras_scheduled_personal_use"),
    ("Cameras", "Blanket", "cameras_blanket"),
    ("Fine Art", "Scheduled - Non Fragile", "fine_art_scheduled_non_fragile"),
    ("Fine Art", "Scheduled - Fragile", "fine_art_scheduled_fragile"),
    ("Fine Art", "Blanket", "fine_art_blanket"),
    ("Gold/ Silver Bullion", "Bank Vault", "gold_silver_bullion_bank_vault"),
    ("Gold/ Silver Bullion", "Home Safe", "gold_silver_bullion_home_safe"),
    ("Golf Clubs", "Scheduled", "golf_clubs_scheduled"),
    ("Golf Clubs", "Scheduled - Golf Carts - Excluding Collision", "golf_clubs_scheduled_golf_carts_excluding_collision"),
    ("Jewellery & Watches", "Scheduled - Jewellery", "jewellery_watches_scheduled_jewellery"),
    ("Jewellery & Watches", "Scheduled - Watches", "jewellery_watches_scheduled_watches"),
    ("Jewellery & Watches", "Scheduled Jewellery/Watches - Bank vault only", "jewellery_watches_scheduled_jewellery_watches_bank_vault_only"),
    ("Jewellery & Watches", "Blanket", "jewellery_watches_blanket"),
    ("Musical Instruments", "Scheduled - Professional Use", "musical_instruments_scheduled_professional_use"),
    ("Musical Instruments", "Scheduled - Personal Use", "musical_instruments_scheduled_personal_use"),
    ("Musical Instruments", "Blanket", "musical_instruments_blanket"),
]
# List of collectible classifications for scheduled and blanket coverages
scheduled_and_blanket_coverages_tuples = [
    ("Antique Furniture", "antique_furniture"),
    ("Baseball/ Sports Cards & Comic books", "baseball_sports_cards_and_comic_books"),
    ("Books", "books"),
    ("Coins", "coins"),
    ("Furs", "furs"),
    ("Guns", "guns"),
    ("Handbags", "handbags"),
    ("Memorabilia", "memorabilia"),
    ("Rugs", "rugs"),
    ("Silverware", "silverware"),
    ("Stamps", "stamps"),
    ("Wine & Cigars", "wine_and_cigars"),
    ("Audio/ Visual Equipment", "audio_visual_equipment"),
    ("Bicycles", "bicycles"),
    ("Computers", "computers"),
    ("Misc.", "misc")
]

target_loss_ratios_dict = {
    "AOP": 0.5,
    "Liability": 0.5,
    "WS": 0.4,
    "EQ": 0.4,
    "Excess FL": 0.57,
    "Wildfire": 0.5,
    "Equipment breakdown": 0.5,
    "PAF": 0.55
}

peril_configs = {
    'AOP': ('aop', [
        'policy_term','product_line', 'state_county_zone', 'construction_type', 'roof_type', 'year_built', 
        'roof_year', 'building_occupancy', 'fire_alarm', 'burglar_alarm', 'sprinkler', 
        'ppc', 'loss', 'tiv_scale'
    ]), #TODO: Crime Score (Pending decision from actuary)
    'Wildfire': ('wildfire', [
        'policy_term','product_line', 'state_county_zone', 'construction_type', 'roof_type', 'year_built',
        'roof_year', 'building_occupancy', 'fire_alarm', 'sprinkler',
        'ppc', 'loss', 'tiv_scale'
    ]), #TODO: Wildfire Score (Pending decision from actuary)
    'Liability': ('liability', ['policy_term','state_county_zone','product_line','ppc','construction_type','year_built','building_occupancy','loss', 'tiv_scale']),
    'Equipment breakdown': ('eb', ['policy_term','loss']),
    'WS': ('ws', [
        'policy_term','state_county_zone','square_foot','product_line', 'construction_type', 'roof_type', 'year_built',
        'roof_year', 'building_occupancy', 'distance_to_coast_options', 'peril', 'loss', 'tiv_scale'
    ]),
    'EQ': ('eq', [
        'policy_term','product_line','basement', 'state_county_zone', 'construction_type', 'roof_type', 'year_built',
        'roof_year', 'building_occupancy', 'number_of_storeys', 'retrofit', 'soft_storey',
        'loss', 'tiv_scale'
    ]),
    'Excess FL': ('fl', [
        'policy_term','product_line','basement', 'state_county_zone', 'construction_type', 'roof_type', 'year_built',
        'roof_year', 'building_occupancy', 'number_of_storeys', 'lowest_floor_elevation',
        'loss',
    ]),
    'PAF': ('paf', [
        'policy_term','fire_alarm', 'burglar_alarm', 'safe', 'credit_score', 'include_ws', 
        'include_eq', 'include_fl'
    ])
}

pricing_limits_table_rules = {
    "show_coverage_a_building_limit": lambda option: True,
    "show_coverage_b_other_structures_limit": lambda option: False if option == "Condominium (HO6)" else True,
    "show_coverage_c_personal_property_limit": lambda option: True,
    "show_coverage_d_loss_of_use_limit": lambda option: True,
    "show_coverage_e_additional_living_expense_limit": lambda option: False if option in ["Homeowners (HO3)", "Homeowners (HO5)", "Condominium (HO6)"] else True,
    "show_coverage_l_liability_limit": lambda option: True,
    "show_coverage_m_med_pay_limit": lambda option: True,
}

peril_pricing_calc_settings = {
    'aop': {'column': 'AOP', 'default_deductible': 2500}, 
    'wildfire': {'column': 'Wildfire', 'default_deductible': 2500},
    'liability': {'column': 'Liability', 'uses_aop_deductible': True},
    'eb': {'column': 'Equipment breakdown', 'deductible_table': 'table_eb_deductible_load'},
    'ws': {'column': 'WS', 'ws_deductible': True},
    'eq': {'column': 'EQ', 'eq_deductible':True}
}

xs_flood_limit_available = 5_000_000
flood_excess_limit_dict = {
    'building':250_000,
    'contents':100_000
}

xs_wind_hail_limit_dict = {
    'building':1_000_000,
    'contents':300_000
} 

paf_single_item_impact_dict = {
    "0%": 1.0,
    "10%": 1.0,
    "20%": 1.0,
    "30%": 1.0,
    "40%": 1.05,
    "50%": 1.1,
    "60%": 1.15,
    "70%": 1.2,
    "80%": 1.25,
    "90%": 1.3,
    "100%": 1.5
} 

paf_loss_surcharge = 0.15
paf_max_ded_credit = 0.5 

base_commercial_rates_factors = {
"include_peril":True,
"assumed_tiv":3_000_000,  
"product_line":"Homeowners (HO5)", 
"deductible":{'eq':0.03,'all':0}, 
"building_occupancy":"Primary", 
"construction_type":"Non Combustible", 
"year_built":2022, 
"roof_year":'AGE_6_10', 
"ppc":5,
"fire_alarm":False, 
"burglar_alarm":False, 
"safe":False,
"sprinkler":"None",
"retrofit":False, 
"number_of_storeys":'St_1', 
"soft_storey":False, 
"basement":False, 
"loss":'NO_LOSSES' ,
"square_foot":2000
}

min_year_built = min(hx.params.table_year_built['Values'])
max_year_built = max(hx.params.table_year_built['Values'])