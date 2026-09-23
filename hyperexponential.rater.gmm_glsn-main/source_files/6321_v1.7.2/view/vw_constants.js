// If changing the max_layers below, you must also update in rate_constants to the same number
function max_layers() {
  return 10
}
function max_options() {
  return 6
}

function account_scoring() {
  return [{ datum: "financials_quality", labelAlign: "left" },
  { datum: "claims_handling", labelAlign: "left" },
  { datum: "claims_experience", labelAlign: "left" },
  { datum: "jurisdiction_venue", labelAlign: "left" },
  { datum: "wordings", labelAlign: "left" },
  { datum: "level_of_service", labelAlign: "left" },
  { datum: "knowledge_of_account", labelAlign: "left" },
  { datum: "nfp_gov_fp", labelAlign: "left" },
  { datum: "broker", labelAlign: "left" },
  { datum: "corporate_integrity", labelAlign: "left" },
  ]
}

function venue_us() {
  return [{ datum: "alaska", labelAlign: "left" },
  { datum: "alabama", labelAlign: "left" },
  { datum: "arkansas", labelAlign: "left" },
  { datum: "arizona", labelAlign: "left" },
  { datum: "california_counties", labelAlign: "left" },
  { datum: "california_rest", labelAlign: "left" },
  { datum: "colorado", labelAlign: "left" },
  { datum: "connecticut", labelAlign: "left" },
  { datum: "district_of_columbia", labelAlign: "left" },
  { datum: "delaware", labelAlign: "left" },
  { datum: "florida_counties", labelAlign: "left" },
  { datum: "florida_rest", labelAlign: "left" },
  { datum: "georgia", labelAlign: "left" },
  { datum: "hawaii", labelAlign: "left" },
  { datum: "iowa", labelAlign: "left" },
  { datum: "idaho", labelAlign: "left" },
  { datum: "illinois_counties", labelAlign: "left" },
  { datum: "illinois_rest", labelAlign: "left" },
  { datum: "indiana", labelAlign: "left" },
  { datum: "international", labelAlign: "left" },
  { datum: "kansas", labelAlign: "left" },
  { datum: "kentucky", labelAlign: "left" },
  { datum: "louisiana", labelAlign: "left" },
  { datum: "massachusetts", labelAlign: "left" },
  { datum: "maryland_counties", labelAlign: "left" },
  { datum: "maryland_rest", labelAlign: "left" },
  { datum: "maine", labelAlign: "left" },
  { datum: "michigan_rest", labelAlign: "left" },
  { datum: "michigan_counties", labelAlign: "left" },
  { datum: "minnesota_counties", labelAlign: "left" },
  { datum: "minnesota_rest", labelAlign: "left" },
  { datum: "missouri_rest", labelAlign: "left" },
  { datum: "missouri_counties", labelAlign: "left" },
  { datum: "mississippi", labelAlign: "left" },
  { datum: "montana", labelAlign: "left" },
  { datum: "north_carolina", labelAlign: "left" },
  { datum: "north_dakota", labelAlign: "left" },
  { datum: "nebraska", labelAlign: "left" },
  { datum: "new_hampshire", labelAlign: "left" },
  { datum: "new_jersey", labelAlign: "left" },
  { datum: "new_mexico", labelAlign: "left" },
  { datum: "nevada", labelAlign: "left" },
  { datum: "new_york_city_counties", labelAlign: "left" },
  { datum: "new_york_rest", labelAlign: "left" },
  { datum: "ohio_counties", labelAlign: "left" },
  { datum: "ohio_rest", labelAlign: "left" },
  { datum: "oklahoma", labelAlign: "left" },
  { datum: "oregon", labelAlign: "left" },
  { datum: "pennsylvania_counties", labelAlign: "left" },
  { datum: "pennsylvania_rest", labelAlign: "left" },
  { datum: "puerto_rico_usa", labelAlign: "left" },
  { datum: "rhode_island", labelAlign: "left" },
  { datum: "south_carolina", labelAlign: "left" },
  { datum: "south_dakota", labelAlign: "left" },
  { datum: "tennessee", labelAlign: "left" },
  { datum: "texas_rest", labelAlign: "left" },
  { datum: "texas_counties", labelAlign: "left" },
  { datum: "utah", labelAlign: "left" },
  { datum: "virginia", labelAlign: "left" },
  { datum: "vermont", labelAlign: "left" },
  { datum: "washington", labelAlign: "left" },
  { datum: "wisconsin", labelAlign: "left" },
  { datum: "west_virginia", labelAlign: "left" },
  { datum: "wyoming", labelAlign: "left" },

  ]
}

function venue_international() {
  return [{ datum: "asia", labelAlign: "left" },
  { datum: "australia", labelAlign: "left" },
  { datum: "brazil", labelAlign: "left" },
  { datum: "canada", labelAlign: "left" },
  { datum: "chile", labelAlign: "left" },
  { datum: "china", labelAlign: "left" },
  { datum: "colombia", labelAlign: "left" },
  { datum: "france", labelAlign: "left" },
  { datum: "germany", labelAlign: "left" },
  { datum: "hong_kong", labelAlign: "left" },
  { datum: "ireland", labelAlign: "left" },
  { datum: "island_economies", labelAlign: "left" },
  { datum: "israel", labelAlign: "left" },
  { datum: "italy", labelAlign: "left" },
  { datum: "malaysia", labelAlign: "left" },
  { datum: "mexico", labelAlign: "left" },
  { datum: "middle_east", labelAlign: "left" },
  { datum: "netherlands", labelAlign: "left" },
  { datum: "peru", labelAlign: "left" },
  { datum: "puerto_rico_international", labelAlign: "left" },
  { datum: "row_high", labelAlign: "left" },
  { datum: "row_low", labelAlign: "left" },
  { datum: "row_medium", labelAlign: "left" },
  { datum: "singapore", labelAlign: "left" },
  { datum: "south_africa", labelAlign: "left" },
  { datum: "spain", labelAlign: "left" },
  { datum: "taiwan", labelAlign: "left" },
  { datum: "thailand", labelAlign: "left" },
  { datum: "uk", labelAlign: "left" },
  { datum: "usa", labelAlign: "left" },

  ]
}


function glsn_danger_ingred_1() {
  return [{ datum: "dimethylamylamine_dmaa", labelAlign: "left" },
  { datum: "aconite", labelAlign: "left" },
  { datum: "aegeline", labelAlign: "left" },
  { datum: "amp_citrate_1_3_dimethylbutylamine_citrate_1_3_dimethylbutylamine_hcl_methylpentanamine", labelAlign: "left" },
  { datum: "androsteredione", labelAlign: "left" },
  { datum: "aristolochic_acid", labelAlign: "left" },
  { datum: "bitter_orange_synephrine", labelAlign: "left" },
  { datum: "chaparral", labelAlign: "left" },
  { datum: "colloidal_silver", labelAlign: "left" },
  { datum: "comfrey", labelAlign: "left" },
  { datum: "dendrobium", labelAlign: "left" },
  { datum: "ephedra_ephedrine", labelAlign: "left" },
  { datum: "germander", labelAlign: "left" },
  { datum: "jin_bu_huan", labelAlign: "left" },
  { datum: "kava_kava_kava", labelAlign: "left" },
  { datum: "lobelia", labelAlign: "left" },
  { datum: "over_the_counter_drugs_otc", labelAlign: "left" },
  { datum: "pennyroyal_oil", labelAlign: "left" },
  { datum: "picamilon_n_nicotinoyl_gaba_pycamilon_pikamilon", labelAlign: "left" },
  { datum: "r_beta_methylphenylethylamine_n_methyl_beta_methylphenylethylamine", labelAlign: "left" },
  { datum: "stephania", labelAlign: "left" },
  { datum: "tiratricol", labelAlign: "left" },
  { datum: "vinpocetine_cavinton_intelectol_ethyl_apovincaminate", labelAlign: "left" },
  { datum: "yohimbe", labelAlign: "left" },

  ]
}

function glsn_danger_ingred_2() {
  return [{ datum: "baby_formula", labelAlign: "left" },
  { datum: "benzodiazepines", labelAlign: "left" },
  { datum: "blood_pressure_pharmaceutcials", labelAlign: "left" },
  { datum: "blood_derived_products", labelAlign: "left" },
  { datum: "birth_control", labelAlign: "left" },
  { datum: "cannabidiol_cbd", labelAlign: "left" },
  { datum: "cochlear_implants", labelAlign: "left" },
  { datum: "cold_therapy_cryotherapy_products", labelAlign: "left" },
  { datum: "cpap_bipap_machines", labelAlign: "left" },
  { datum: "diabetes_pharmaceuticals", labelAlign: "left" },
  { datum: "ear_plugs", labelAlign: "left" },
  { datum: "energy_drinks", labelAlign: "left" },
  { datum: "generic_or_off_patent_pharmaceuticals", labelAlign: "left" },
  { datum: "hip_implants_metal_on_metal", labelAlign: "left" },
  { datum: "ivc_filters", labelAlign: "left" },
  { datum: "intrauterine_devices_iuds", labelAlign: "left" },
  { datum: "medical_marijuana", labelAlign: "left" },
  { datum: "morcellators", labelAlign: "left" },
  { datum: "mri_contrast_agents", labelAlign: "left" },
  { datum: "neurovascular_stents", labelAlign: "left" },
  { datum: "opioids", labelAlign: "left" },
  { datum: "pain_pumps", labelAlign: "left" },
  { datum: "proton_pump_inhibitors_ppis_antacids", labelAlign: "left" },
  { datum: "sexual_enhancement_pharmaceuticals", labelAlign: "left" },
  { datum: "silicone_breast_implants", labelAlign: "left" },
  { datum: "surgical_mesh", labelAlign: "left" },
  { datum: "talcum_powder", labelAlign: "left" },
  { datum: "thalidomide", labelAlign: "left" },
  { datum: "weight_loss_pharmaceuticals", labelAlign: "left" },

  ]
}

function tech_eo_class() {
  return [{ datum: "reseller_distributor", labelAlign: "left" },
  { datum: "training_education", labelAlign: "left" },
  { datum: "prepackaged_software_products_services", labelAlign: "left" },
  { datum: "live_video_mobile_health_store_forward", labelAlign: "left" },
  { datum: "teleneurology_or_teleradiology", labelAlign: "left" },
  { datum: "technology_companies_platform_hosts", labelAlign: "left" },
  { datum: "software_hardware_management_systems_non_medical", labelAlign: "left" },
  { datum: "custom_software_development", labelAlign: "left" },
  { datum: "internet_based_services_products", labelAlign: "left" },
  { datum: "other", labelAlign: "left" },
  { datum: "custom_hardware_development", labelAlign: "left" },
  { datum: "software_hardware_medical_management", labelAlign: "left" },

  ]
}
function cyber_schedule_rating() {
  return [{ datum: "cyber_financial_condition", labelAlign: "left" },
  { datum: "cyber_maturity_of_business", labelAlign: "left" },
  { datum: "cyber_quality_of_management", labelAlign: "left" },
  { datum: "cyber_volume_of_information_stored", labelAlign: "left" },

  ]
}

function gmm_umbrella_class() {
  return [{ datum: "auto_liability", labelAlign: "left" },
  { datum: "employers_liability", labelAlign: "left" },
  { datum: "general_liability", labelAlign: "left" },
  { datum: "foreign_liability", labelAlign: "left" },
  { datum: "aircraft_nonowned", labelAlign: "left" },
  { datum: "aircraft_owned", labelAlign: "left" },
  { datum: "auto_ambulance", labelAlign: "left" },
  { datum: "educators_liability", labelAlign: "left" },
  { datum: "garage_keepers_liability", labelAlign: "left" },
  { datum: "helipad", labelAlign: "left" },
  { datum: "liquor_law_liability", labelAlign: "left" },
  { datum: "managed_care_eo_health_plan", labelAlign: "left" },
  { datum: "managed_care_eo_nonhealth_plan", labelAlign: "left" },
  { datum: "watercraft_nonowned", labelAlign: "left" },
  { datum: "watercraft_owned", labelAlign: "left" },

  ]
}

function glsn_umbrella_class() {
  return [{ datum: "auto_liability", labelAlign: "left" },
  { datum: "employers_liability", labelAlign: "left" },
  { datum: "general_liability", labelAlign: "left" },
  { datum: "foreign_liability", labelAlign: "left" },
  { datum: "aircraft_nonowned", labelAlign: "left" },
  { datum: "aircraft_owned", labelAlign: "left" },
  { datum: "garage_keepers_liability", labelAlign: "left" },
  { datum: "liquor_law_liability", labelAlign: "left" },
  { datum: "watercraft_non_owned", labelAlign: "left" },
  { datum: "watercraft_owned", labelAlign: "left" },
  { datum: "foreign_employers_liability", labelAlign: "left" },
  { datum: "foreign_general_liability", labelAlign: "left" },
  { datum: "foreign_auto_liability", labelAlign: "left" },

  ]
}

function gmm_schedule_mods() {
  return [{ datum: "loss_experience", labelAlign: "left" },
  { datum: "claims_handling_cooperation_experience", labelAlign: "left" },
  { datum: "risk_management_protocols_in_place", labelAlign: "left" },
  { datum: "use_of_standardized_written_contract", labelAlign: "left" },
  { datum: "accreditations", labelAlign: "left" },
  { datum: "hiring_credentialing_practices", labelAlign: "left" },
  { datum: "management_and_financial_condition", labelAlign: "left" },
  { datum: "shared_limit_with_physicians", labelAlign: "left" },
  { datum: "entity_only_vicarious_liability", labelAlign: "left" },
  { datum: "per_location_limit_increased_aggregate", labelAlign: "left" },
  { datum: "per_physician_limit_increased_aggregate", labelAlign: "left" },
  { datum: "sublimited_coverages_not_those_shown_on_pricing_tab", labelAlign: "left" },
  { datum: "transportation_exposure", labelAlign: "left" },
  { datum: "pediatric_senior_care_dd_exposure", labelAlign: "left" },
  { datum: "pcf_state_required_limits", labelAlign: "left" },
  { datum: "sexual_abuse_sublimit", labelAlign: "left" },
  { datum: "media_content_review_and_control_procedures_vc_only", labelAlign: "left" },
  { datum: "privacy_controls_and_procedures_vc_only", labelAlign: "left" },
  { datum: "total_schedule_rating", labelAlign: "left" },

  ]
}
function glsn_schedule_mods() {
  return [{ datum: "loss_history", labelAlign: "left" },
  { datum: "contractual_agreements", labelAlign: "left" },
  { datum: "protocol_and_informed_consent", labelAlign: "left" },
  { datum: "fda_inspections", labelAlign: "left" },
  { datum: "product_type_litigation_history", labelAlign: "left" },
  { datum: "management_quality_and_financial_condition", labelAlign: "left" },
  { datum: "risk_management_protocols_in_place", labelAlign: "left" },
  { datum: "vulnerable_populations", labelAlign: "left" },
  { datum: "drug_of_last_resort", labelAlign: "left" },
  { datum: "foreign_sales", labelAlign: "left" },
  { datum: "exceptions_to_dangerous_ingredients", labelAlign: "left" },
  { datum: "imported_api_and_or_imported_finished_products", labelAlign: "left" },
  { datum: "gl_exposure_retail_locations_warehouses_wet_labs_etc", labelAlign: "left" },
  { datum: "sublimited_coverages_not_shown_on_pricing_page", labelAlign: "left" },
  { datum: "per_location_limit_increased_aggregate", labelAlign: "left" },
  { datum: "hiring_credentialing", labelAlign: "left" },
  { datum: "other", labelAlign: "left" },
  { datum: "total_schedule_rating", labelAlign: "left" },

  ]
}

export { max_layers, max_options, account_scoring, venue_us, venue_international, glsn_danger_ingred_1, glsn_danger_ingred_2, tech_eo_class, cyber_schedule_rating, gmm_umbrella_class, glsn_umbrella_class, gmm_schedule_mods, glsn_schedule_mods };