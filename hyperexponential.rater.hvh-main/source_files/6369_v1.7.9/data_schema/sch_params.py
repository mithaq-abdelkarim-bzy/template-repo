import hx

product_lines = hx.params.table_product_line
construction_type = hx.params.table_construction_type
roof_type = hx.params.table_roof_type
building_occupancy = hx.params.table_building_occupancy
ppc = hx.params.table_ppc
number_of_units_list = ["Single Family","Duplex","Quadplex"]
roof_shape_list = [
    "Flat roof",
    "Gabled Roof",
    "Hip Roof",
    "Unknown",
    "Gable roof low pitch",
    "Gable Roof unknown pitch",
]
occupation_list = [
    "Professional Employment",
    "Student",
    "Unemployed",
    "Social Media personality",
    "Reality TV personality",
    "Music Producer / Performer",
    "Athlete",
    "Political Figure",
    "Film Producer/Actor",
    "Non-standard profession (e.g. Professional Gambler)",
    "Retired",
    "Other",
]
us_states = sorted(list(set(hx.params.table_hazard_mappings['State Code'])))
us_counties = list(hx.params.table_hazard_mappings['County'])
ws_deductible_list = ["Wind & Hail","Named Storm","All Perils"]
all_perils = ["aop","wildfire", "liability", "ws", "eb", "fl", "eq", "paf"]
all_perils_dict = {
    "aop":"AOP",
    "liability":"Liability",
    "ws":"WS",
    "eq":"EQ",
    "fl":"Excess FL",
    "wildfire":"Wildfire",
    "paf":"PAF",
    "eb":"Equipment Breakdown"
    }

factor_list = [   
    "policy_term", 
    "product_line",
    "construction_type",
    "roof_type",
    "year_built",
    "roof_year",
    "building_occupancy",
    "number_of_storeys",
    "fire_alarm",
    "burglar_alarm",
    "sprinkler",
    "ppc",
    "updated_wiring_year",
    "updated_plumbing_year",
    "updated_heating_year",
    "updated_roof_year",
    "square_foot",
    "number_of_units",
    "basement",
    "roof_shape",
    "crime_score",
    "wildfire_score",
    "insured_occupation",
    "high_profile_client",
    "distance_to_coast",
    "distance_to_coast_options",
    "state_county_zone",
    "hazard_zone",
    "loss",
    "safe",
    "credit_score",
    "tiv_scale",
    "total_modifier_impact",
    #"tp_uplift",
    "retrofit",
    "soft_storey",
    "lowest_floor_elevation",
    "include_ws",
    "include_eq",
    "include_fl",
    "include_wildfire",
    "five_year_burn",
    "peril",
    "retrofit",
    "soft_storey"
    ]

# List of collectible classifications for scheduled and blanket coverages
scheduled_and_blanket_coverages = [
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
excluded_blanket_variables = {"audio_visual_equipment", "bicycles", "computers", "misc"}
specific_schedules = [
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
    ("Jewellery & Watches", "Scheduled Jewellery/Watches - Bank Vault Only", "jewellery_watches_scheduled_jewellery_watches_bank_vault_only"),
    ("Jewellery & Watches", "Blanket", "jewellery_watches_blanket"),
    ("Musical Instruments", "Scheduled - Professional Use", "musical_instruments_scheduled_professional_use"),
    ("Musical Instruments", "Scheduled - Personal Use", "musical_instruments_scheduled_personal_use"),
    ("Musical Instruments", "Blanket", "musical_instruments_blanket"),
]