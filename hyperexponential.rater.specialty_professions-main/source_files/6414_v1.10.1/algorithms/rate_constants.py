import hx_data_schema as hx

# If changing the max_layers below, you must also update in vw_constants to the same number
max_layers = 6

# If changing the max_options below, you must also update in vw_constants to the same number
max_options = 4

# benchmark lr
benchmark_lr_const = 0.7

# assumed_lr - based on BUSA model
# W:\SL\Actuarial\04 Raters\BeazleyPro\BEAZLEYARCHITECTSANDENGINEERS\Admitted & Surplus\Current
assumed_lr_const = 0.76

# BUSA Rater Commission
# W:\SL\Actuarial\04 Raters\BeazleyPro\BEAZLEYARCHITECTSANDENGINEERS\Admitted & Surplus\Current
# This rater was built based on the BUSA rater, which has 15% commission embedded in the rates.
# Therefore, need to rebase this rater downwards by 15%.
busa_commission_rebase = 0.15

# benchmark class
bp_class = 'Specialty Professions'

# RATE CHANGE LISTS ##############

expiring_layer_names = [
        "Primary Layer",
        "Excess Layer 1",
        "Excess Layer 2",
        "Excess Layer 3",
        "Excess Layer 4",
        "Excess Layer 5",
        ]

def model_change_list():
    model_change_path = [
        {"node":"cds/options/excess_1_excess", "override":True, "source_from_expiring":True},
        {"node":"cds/options/excess_2_excess", "override":True, "source_from_expiring":True},
        {"node":"cds/options/excess_3_excess", "override":True, "source_from_expiring":True},
        {"node":"cds/options/excess_4_excess", "override":True, "source_from_expiring":True},
        {"node":"cds/options/excess_5_excess", "override":True, "source_from_expiring":True},
    ]
    return(model_change_path)

def exposure_change_list():
    exposure_change_path = [
        "cds/exposure/granular/construction_with_in_house_design/current_yr_construction_value",
        "cds/exposure/granular/construction_with_in_house_design/current_yr_professional_fees",
        "cds/exposure/granular/construction_with_in_house_design/last_yr_construction_value",
        "cds/exposure/granular/construction_with_in_house_design/last_yr_professional_fees",
        "cds/exposure/granular/construction_with_in_house_design/two_yr_ago_construction_value",
        "cds/exposure/granular/construction_with_in_house_design/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/construction_with_sub_contracted_design/current_yr_construction_value",
        "cds/exposure/granular/construction_with_sub_contracted_design/current_yr_professional_fees",
        "cds/exposure/granular/construction_with_sub_contracted_design/last_yr_construction_value",
        "cds/exposure/granular/construction_with_sub_contracted_design/last_yr_professional_fees",
        "cds/exposure/granular/construction_with_sub_contracted_design/two_yr_ago_construction_value",
        "cds/exposure/granular/construction_with_sub_contracted_design/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/design_only_no_construction/current_yr_construction_value",
        "cds/exposure/granular/design_only_no_construction/current_yr_professional_fees",
        "cds/exposure/granular/design_only_no_construction/last_yr_construction_value",
        "cds/exposure/granular/design_only_no_construction/last_yr_professional_fees",
        "cds/exposure/granular/design_only_no_construction/two_yr_ago_construction_value",
        "cds/exposure/granular/design_only_no_construction/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/construction_only_no_design/current_yr_construction_value",
        "cds/exposure/granular/construction_only_no_design/current_yr_professional_fees",
        "cds/exposure/granular/construction_only_no_design/last_yr_construction_value",
        "cds/exposure/granular/construction_only_no_design/last_yr_professional_fees",
        "cds/exposure/granular/construction_only_no_design/two_yr_ago_construction_value",
        "cds/exposure/granular/construction_only_no_design/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/at_risk_construction_management/current_yr_construction_value",
        "cds/exposure/granular/at_risk_construction_management/current_yr_professional_fees",
        "cds/exposure/granular/at_risk_construction_management/last_yr_construction_value",
        "cds/exposure/granular/at_risk_construction_management/last_yr_professional_fees",
        "cds/exposure/granular/at_risk_construction_management/two_yr_ago_construction_value",
        "cds/exposure/granular/at_risk_construction_management/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/agency_construction_management/current_yr_construction_value",
        "cds/exposure/granular/agency_construction_management/current_yr_professional_fees",
        "cds/exposure/granular/agency_construction_management/last_yr_construction_value",
        "cds/exposure/granular/agency_construction_management/last_yr_professional_fees",
        "cds/exposure/granular/agency_construction_management/two_yr_ago_construction_value",
        "cds/exposure/granular/agency_construction_management/two_yr_ago_professional_fees",
        
        "cds/exposure/granular/other/current_yr_construction_value",
        "cds/exposure/granular/other/current_yr_professional_fees",
        "cds/exposure/granular/other/last_yr_construction_value",
        "cds/exposure/granular/other/last_yr_professional_fees",
        "cds/exposure/granular/other/two_yr_ago_construction_value",
        "cds/exposure/granular/other/two_yr_ago_professional_fees",
    
        {"node":"cds/exposure/granular/construction_with_in_house_design/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/construction_with_sub_contracted_design/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/design_only_no_construction/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/construction_only_no_design/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/at_risk_construction_management/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/agency_construction_management/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},
        {"node":"cds/exposure/granular/other/selected_avg_rateable_exposure", "override":True, "source_from_expiring":False},

        {"node":"cds/exposure/granular/total/override_avg_rateable_exposure", "override":True, "source_from_expiring":False},

        "cds/exposure/granular/engineering/aerospace/percentage",
        {"node":"cds/exposure/granular/engineering/aerospace/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/architect_comm/percentage",
        {"node":"cds/exposure/granular/engineering/architect_comm/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/architect_resi/percentage",
        {"node":"cds/exposure/granular/engineering/architect_resi/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/aviation/percentage",
        {"node":"cds/exposure/granular/engineering/aviation/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/chemical/percentage",
        {"node":"cds/exposure/granular/engineering/chemical/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/civil/percentage",
        {"node":"cds/exposure/granular/engineering/civil/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/civil_bridges_roads/percentage",
        {"node":"cds/exposure/granular/engineering/civil_bridges_roads/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/cm_atrisk/percentage",
        {"node":"cds/exposure/granular/engineering/cm_atrisk/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/cm_agency/percentage",
        {"node":"cds/exposure/granular/engineering/cm_agency/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/drafting/percentage",
        {"node":"cds/exposure/granular/engineering/drafting/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/electrical/percentage",
        {"node":"cds/exposure/granular/engineering/electrical/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/enviro_cons/percentage",
        {"node":"cds/exposure/granular/engineering/enviro_cons/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/enviro_labs/percentage",
        {"node":"cds/exposure/granular/engineering/enviro_labs/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/fp/percentage",
        {"node":"cds/exposure/granular/engineering/fp/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/forensic/percentage",
        {"node":"cds/exposure/granular/engineering/forensic/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/geotechnical/percentage",
        {"node":"cds/exposure/granular/engineering/geotechnical/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/hvac/percentage",
        {"node":"cds/exposure/granular/engineering/hvac/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/int_design/percentage",
        {"node":"cds/exposure/granular/engineering/int_design/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/landscape/percentage",
        {"node":"cds/exposure/granular/engineering/landscape/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/leed_cons/percentage",
        {"node":"cds/exposure/granular/engineering/leed_cons/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/mech/percentage",
        {"node":"cds/exposure/granular/engineering/mech/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/mech_electrical/percentage",
        {"node":"cds/exposure/granular/engineering/mech_electrical/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/mining/percentage",
        {"node":"cds/exposure/granular/engineering/mining/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/non_destructive_testing/percentage",
        {"node":"cds/exposure/granular/engineering/non_destructive_testing/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/nuclear/percentage",
        {"node":"cds/exposure/granular/engineering/nuclear/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/oil_gas/percentage",
        {"node":"cds/exposure/granular/engineering/oil_gas/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/process/percentage",
        {"node":"cds/exposure/granular/engineering/process/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/struct_resi_inst/percentage",
        {"node":"cds/exposure/granular/engineering/struct_resi_inst/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/struct_steel_stairs/percentage",
        {"node":"cds/exposure/granular/engineering/struct_steel_stairs/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/struct_non_resi_inst/percentage",
        {"node":"cds/exposure/granular/engineering/struct_non_resi_inst/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/surveyor/percentage",
        {"node":"cds/exposure/granular/engineering/surveyor/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/surveyor_resi/percentage",
        {"node":"cds/exposure/granular/engineering/surveyor_resi/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/engineering/other_one/percentage",
        "cds/exposure/granular/engineering/other_one/base_rate_override",
        "cds/exposure/granular/engineering/other_two/percentage",
        "cds/exposure/granular/engineering/other_two/base_rate_override",
        "cds/exposure/granular/engineering/other_three/percentage",
        "cds/exposure/granular/engineering/other_three/base_rate_override",
        "cds/exposure/granular/engineering/other_four/percentage",
        "cds/exposure/granular/engineering/other_four/base_rate_override",
        "cds/exposure/granular/engineering/other_five/percentage",
        "cds/exposure/granular/engineering/other_five/base_rate_override",
        
        "cds/exposure/granular/contractor/asbestos_lead/percentage",
        {"node":"cds/exposure/granular/contractor/asbestos_lead/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/build_envelop/percentage",
        {"node":"cds/exposure/granular/contractor/build_envelop/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/carpenter/percentage",
        {"node":"cds/exposure/granular/contractor/carpenter/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/concrete/percentage",
        {"node":"cds/exposure/granular/contractor/concrete/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/demolition/percentage",
        {"node":"cds/exposure/granular/contractor/demolition/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/drywall/percentage",
        {"node":"cds/exposure/granular/contractor/drywall/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/electrical/percentage",
        {"node":"cds/exposure/granular/contractor/electrical/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/enviro/percentage",
        {"node":"cds/exposure/granular/contractor/enviro/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/fp_dry/percentage",
        {"node":"cds/exposure/granular/contractor/fp_dry/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/fp_wet/percentage",
        {"node":"cds/exposure/granular/contractor/fp_wet/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/foundation_excav/percentage",
        {"node":"cds/exposure/granular/contractor/foundation_excav/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/general_comm/percentage",
        {"node":"cds/exposure/granular/contractor/general_comm/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/general_resi/percentage",
        {"node":"cds/exposure/granular/contractor/general_resi/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/glazing/percentage",
        {"node":"cds/exposure/granular/contractor/glazing/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/hvac_industrial/percentage",
        {"node":"cds/exposure/granular/contractor/hvac_industrial/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/hvac_non_industrial/percentage",
        {"node":"cds/exposure/granular/contractor/hvac_non_industrial/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/landscape/percentage",
        {"node":"cds/exposure/granular/contractor/landscape/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/masonry/percentage",
        {"node":"cds/exposure/granular/contractor/masonry/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/mech/percentage",
        {"node":"cds/exposure/granular/contractor/mech/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/reno_non_resi/percentage",
        {"node":"cds/exposure/granular/contractor/reno_non_resi/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/oil_gas/percentage",
        {"node":"cds/exposure/granular/contractor/oil_gas/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/painting/percentage",
        {"node":"cds/exposure/granular/contractor/painting/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/plumbing/percentage",
        {"node":"cds/exposure/granular/contractor/plumbing/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/resi_reno/percentage",
        {"node":"cds/exposure/granular/contractor/resi_reno/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/roofing/percentage",
        {"node":"cds/exposure/granular/contractor/roofing/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/steel/percentage",
        {"node":"cds/exposure/granular/contractor/steel/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/telecom_heavy/percentage",
        {"node":"cds/exposure/granular/contractor/telecom_heavy/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/telecom_light/percentage",
        {"node":"cds/exposure/granular/contractor/telecom_light/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/utilities/percentage",
        {"node":"cds/exposure/granular/contractor/utilities/base_rate_override", "override":True, "source_from_expiring":False},
        "cds/exposure/granular/contractor/other_one/percentage",
        "cds/exposure/granular/contractor/other_one/base_rate_override",
        "cds/exposure/granular/contractor/other_two/percentage",
        "cds/exposure/granular/contractor/other_two/base_rate_override",
        "cds/exposure/granular/contractor/other_three/percentage",
        "cds/exposure/granular/contractor/other_three/base_rate_override",
        "cds/exposure/granular/contractor/other_four/percentage",
        "cds/exposure/granular/contractor/other_four/base_rate_override",
        "cds/exposure/granular/contractor/other_five/percentage",
        "cds/exposure/granular/contractor/other_five/base_rate_override",
        
    ]
    return(exposure_change_path)

def risk_characteristics_change_list():
    risk_characteristics_change_path = [
        "cds/rating_factors/location/states",

        "cds/modifiers/exp_mod/incurred_loss",
        "cds/modifiers/exp_mod/number_of_claims",
        "cds/modifiers/exp_mod/number_of_incidents",
        "cds/modifiers/exp_mod/written_premium",
        {"node":"cds/modifiers/exp_mod/incurred_lr", "override":True, "source_from_expiring":False},
        {"node":"cds/modifiers/exp_mod/exp_mod_factor", "override":True, "source_from_expiring":False},
        "cds/rating_factors/written_contracts/percentage",
        "cds/rating_factors/written_contracts/written_contracts_factor",
        "cds/rating_factors/longevity_with_carrier/yrs_insured",
        "cds/rating_factors/longevity_with_carrier/lr",
        "cds/rating_factors/longevity/yr_start",
        "cds/rating_factors/resi/resi_proj",
        "cds/rating_factors/resi/multiple_units",
        "cds/rating_factors/resi/high_value",
        "cds/rating_factors/resi/condos",

        "cds/exposure/granular/project_type",

        "cds/modifiers/schedule_rating_factor/qual_of_staff/factor",
        "cds/modifiers/schedule_rating_factor/rm_attendance/factor",
        "cds/modifiers/schedule_rating_factor/foreign_work/factor",
        "cds/modifiers/schedule_rating_factor/loss_prev/factor",
        "cds/modifiers/schedule_rating_factor/client_type/factor",
        "cds/modifiers/schedule_rating_factor/contractual_practices/factor",
        "cds/modifiers/schedule_rating_factor/engi_procure_construct/factor",
        "cds/modifiers/schedule_rating_factor/peer_review/factor",
    ]
    return(risk_characteristics_change_path)


def deductible_change_list():
    deductible_change_path = [
        {"node":"cds/options/excess_1_excess", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_2_excess", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_3_excess", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_4_excess", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_5_excess", "override":True, "source_from_expiring":False},
        "cds/options/deductible",
    ]
    return(deductible_change_path)

def limit_change_list():
    limit_change_path = [
        "cds/options/ilf_type",
        "cds/options/limit",
        {"node":"cds/options/aggregate_limit", "override":True, "source_from_expiring":False},
        "cds/options/excess_1_limit",
        "cds/options/excess_2_limit",
        "cds/options/excess_3_limit",
        "cds/options/excess_4_limit",
        "cds/options/excess_5_limit",
    ]
    return(limit_change_path)  

def terms_and_conditions_change_list():
    terms_and_conditions_change_path = [
        "cds/rating_factors/erp/erp",
        "cds/rating_factors/opt_coverages/full_prior_act",
        "cds/rating_factors/opt_coverages/full_prior_act_date",
        "cds/rating_factors/opt_coverages/cpl",
        "cds/rating_factors/opt_coverages/tech",
        "cds/rating_factors/opt_coverages/non_contributary",                    
    ]
    return(terms_and_conditions_change_path)

def brokerage_change_list():
    brokerage_change_path = [
        "cds/brokerage",
        {"node":"cds/options/brokerage_primary", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_1_brokerage", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_2_brokerage", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_3_brokerage", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_4_brokerage", "override":True, "source_from_expiring":False},
        {"node":"cds/options/excess_5_brokerage", "override":True, "source_from_expiring":False},
    ]
    return(brokerage_change_path)


  

   



def rc_discipline_lst():    
    # Engineering disciplines
    engi_discipline = ["aerospace",   
        "architect_comm",
        "architect_resi",
        "aviation",
        "chemical",
        "civil",
        "civil_bridges_roads",
        "cm_atrisk",
        "cm_agency",
        "drafting",
        "electrical",
        "enviro_cons",
        "enviro_labs",
        "fp",
        "forensic",
        "geotechnical",
        "hvac",
        "int_design",
        "landscape",
        "leed_cons",
        "mech",
        "mech_electrical",
        "mining",
        "non_destructive_testing",
        "nuclear",
        "oil_gas",
        "process",
        "struct_resi_inst",
        "struct_steel_stairs",
        "struct_non_resi_inst",
        "surveyor",
        "surveyor_resi",
        "other_one",
        "other_two",
        "other_three",
        "other_four",
        "other_five"
    ]

    # Contractor disciplines
    con_discipline = [
        "asbestos_lead",
        "build_envelop",
        "carpenter",
        "concrete",
        "demolition",
        "drywall"
        "electrical",
        "enviro",
        "fp_dry",
        "fp_wet",
        "foundation_excav",
        "general_comm",
        "general_resi",
        "glazing",
        "hvac_industrial",
        "hvac_non_industrial",
        "landscape",
        "masonry",
        "mech",
        "reno_non_resi",
        "oil_gas",
        "painting",
        "plumbing",
        "resi_reno",
        "roofing",
        "steel",
        "telecom_heavy",
        "telecom_light",
        "utilities",
        "other_one",
        "other_two",
        "other_three",
        "other_four",
        "other_five"
    ]
        
    engi_perc_lst = ["cds/exposure/granular/engineering/" + item + "/percentage" for item in engi_discipline]
    engi_base_rate_override_lst = ["cds/exposure/granular/engineering/" + item + "/base_rate_override" for item in engi_discipline]    
    con_perc_lst = ["cds/exposure/granular/contractor/" + item + "/percentage" for item in con_discipline]
    con_base_rate_override_lst = ["cds/exposure/granular/contractor/" + item + "/base_rate_override" for item in con_discipline]           
    
    return(
        engi_perc_lst +
        engi_base_rate_override_lst +
        con_perc_lst +
        con_base_rate_override_lst
    )


