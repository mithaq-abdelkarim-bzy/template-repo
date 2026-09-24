import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from algorithms.percentage_validations import set_invalid,set_valid

def discipline_baserate_calcs(hxd):

    # define where exposure variables live in data schema
    cons_with_in_house = hxd.cds.exposure.granular.construction_with_in_house_design
    cons_sub_con = hxd.cds.exposure.granular.construction_with_sub_contracted_design
    desi_no_cons = hxd.cds.exposure.granular.design_only_no_construction
    cons_no_desi = hxd.cds.exposure.granular.construction_only_no_design
    at_risk = hxd.cds.exposure.granular.at_risk_construction_management
    agency_con = hxd.cds.exposure.granular.agency_construction_management
    other_exposure = hxd.cds.exposure.granular.other
    total_exposure = hxd.cds.exposure.granular.total

    # Size discount curve ##############################################################

    # Paths
    location = hxd.cds.rating_factors.location
    agg_exposure = hxd.cds.exposure.aggregate

    # Parameter table
    param_size_discount = hx.params.tbl_sizeadjust    
    
    # size discount
    agg_exposure.size_discount = np.interp(total_exposure.override_avg_rateable_exposure.selected, param_size_discount["Rateable Revenue"], param_size_discount["Size discount"])
       
    # Size discount    
    if total_exposure.override_avg_rateable_exposure.selected == 0:
        agg_exposure.size_discount = 0
    else:
        agg_exposure.size_discount = np.interp(total_exposure.override_avg_rateable_exposure.selected, param_size_discount["Rateable Revenue"], param_size_discount["Size discount"])


    # ENGINEERING DISCIPLINE BASE RATES ##############################################################

    # Engineering base rate parameters
    param_engi_baserates = hx.params.tbl_engineering_rates_mins[["Discipline", "Selected Base Rate"]]
    param_engi_baserates = param_engi_baserates[~param_engi_baserates["Discipline"].str.startswith("Other")]

    # define where engineering discipline variables live in data schema
    engi_disc = hxd.cds.exposure.granular.engineering

    # Considerations
    engi_disc.considerations = "Decline: Landman, Roofing Consultants, Roofing Inspector, Safety Consulting, Utility Locating Services, Welding Inspector"

    # Engineering rateable exposure
    eng_selected_rateable_exposure = 0

        # Construction with In House Design
    if (cons_with_in_house.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += cons_with_in_house.override_avg_rateable_exposure
        # Construction with Sun Contracted Design
    if (cons_sub_con.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += cons_sub_con.override_avg_rateable_exposure
        # Design Only - No Construction
    if (desi_no_cons.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += desi_no_cons.override_avg_rateable_exposure
        # Construction Only - No Design
    if (cons_no_desi.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += cons_no_desi.override_avg_rateable_exposure
        # At Risk Construction Management
    if (at_risk.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += at_risk.override_avg_rateable_exposure
        # Agency Construction Management
    if (agency_con.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += agency_con.override_avg_rateable_exposure
        # Other (Specify)
    if (other_exposure.rateable_exposure_discipline == "Engineering"):
        eng_selected_rateable_exposure += other_exposure.override_avg_rateable_exposure        

    # Size discount
    eng_selected_rateable_exposure_size_discount = eng_selected_rateable_exposure * (1 - agg_exposure.size_discount)       

    # List of known discipline variables
    lst_engi_discipline_vbl = [
        engi_disc.aerospace,
        engi_disc.architect_comm,
        engi_disc.architect_resi,
        engi_disc.aviation,
        engi_disc.chemical,
        engi_disc.civil,
        engi_disc.civil_bridges_roads,
        engi_disc.cm_atrisk,
        engi_disc.cm_agency,
        engi_disc.drafting,
        engi_disc.electrical,
        engi_disc.enviro_cons,
        engi_disc.enviro_labs,
        engi_disc.fp,
        engi_disc.forensic,
        engi_disc.geotechnical,
        engi_disc.hvac,
        engi_disc.int_design,
        engi_disc.landscape,
        engi_disc.leed_cons,
        engi_disc.mech,
        engi_disc.mech_electrical,
        engi_disc.mining,
        engi_disc.non_destructive_testing,
        engi_disc.nuclear,
        engi_disc.oil_gas,
        engi_disc.process,
        engi_disc.struct_resi_inst,
        engi_disc.struct_steel_stairs,
        engi_disc.struct_non_resi_inst,
        engi_disc.surveyor,
        engi_disc.surveyor_resi,
        engi_disc.other_one,
        engi_disc.other_two,
        engi_disc.other_three,
        engi_disc.other_four,
        engi_disc.other_five
        ]

    # List of known discipline strings - for matching to parameter levels
    lst_engi_discipline_str = [
        'Aerospace',
        'Architect (Commercial / Other)',
        'Architect (Residential)',
        'Aviation',
        'Chemical',
        'Civil Engineer',
        'Civil Engineer (Bridges & Roads)',
        'Construction Manager @Risk',
        'Construction Manager Agency',
        'Drafting',
        'Electrical Engineering',
        'Environmental Consultant',
        'Environmental Labs',
        'Fire Protection',
        'Forensic Engineer',
        'Geotechnical',
        'HVAC',
        'Interior Designer',
        'Landscape Architecture',
        'LEED Consulting',
        'Mechanical Engineering',
        'Mechanical/Electrical',
        'Mining',
        'Non Destructive Testing',
        'Nuclear',
        'Oil & Gas',
        'Process',
        'Structural (Residential and Institutional)',
        'Structural (Steel Fabricators / Stairs etc)',
        'Structural Engineer (Non resi & Institutional)',
        'Surveyor',
        'Surveyor (Residential)',
        'Other 1 (Specify)',
        'Other 2 (Specify)',
        'Other 3 (Specify)',
        'Other 4 (Specify)',
        'Other 5 (Specify)'
        ]


    # Loop through the discipline variables
    for loop_vbl, loop_str in zip(lst_engi_discipline_vbl, lst_engi_discipline_str):
        
        # Calculate rateable_exposure
        loop_vbl.rateable_exposure = eng_selected_rateable_exposure * loop_vbl.percentage
        loop_vbl.rateable_exposure_size_discount = eng_selected_rateable_exposure_size_discount * loop_vbl.percentage

        # Calculate base premium
        if (loop_vbl in [engi_disc.other_one, engi_disc.other_two, engi_disc.other_three, engi_disc.other_four, engi_disc.other_five]):
            # Set default base rate to override, because UWs enter in the value for Other disciplines            
            loop_vbl.default_base_rate = loop_vbl.base_rate_override
            loop_vbl.base_premium = loop_vbl.base_rate_override * loop_vbl.rateable_exposure/100
            loop_vbl.base_premium_size_discount = loop_vbl.base_rate_override * loop_vbl.rateable_exposure_size_discount/100
        else:
            # Lookup engineering base rates
            loop_vbl.default_base_rate = param_engi_baserates[param_engi_baserates['Discipline'] == loop_str]['Selected Base Rate'].iloc[0]        
            # Default to engineering base rates
            loop_vbl.base_rate_override.calculated = loop_vbl.default_base_rate
            loop_vbl.base_premium = loop_vbl.base_rate_override.selected * loop_vbl.rateable_exposure/100
            loop_vbl.base_premium_size_discount = loop_vbl.base_rate_override.selected * loop_vbl.rateable_exposure_size_discount/100
                                                   
    pass

    # Engineering Guidelines specification
    engi_disc.aerospace.guidelines = 'Avoid Critical Parts & Safety Features'
    engi_disc.architect_resi.guidelines = 'Avoid Condos and Poor states'
    engi_disc.aviation.guidelines = 'Avoid Critical Parts & Safety Features'
    engi_disc.civil.guidelines = 'Avoid Bridges & Road Projects'
    engi_disc.civil_bridges_roads.guidelines = 'Use site safety endorsement'
    engi_disc.drafting.guidelines = 'Sub Stamped by PE'
    engi_disc.fp.guidelines = 'PFOS exposures'
    engi_disc.geotechnical.guidelines = 'Avoid Colorado'
    engi_disc.hvac.guidelines = 'Avoid Industrial HVAC'
    engi_disc.landscape.guidelines = 'Avoid Golf Courses & Condos'
    engi_disc.leed_cons.guidelines = 'Size of project'
    engi_disc.mech.guidelines = 'Look for BI Exposured Projects (Lifts, Cranes)'
    engi_disc.mining.guidelines = "Avoid Tailings Dams / Landfil/Coal. Deposit Estimation - Not for FI's"
    engi_disc.non_destructive_testing.guidelines = 'What are they testing? Avoid infrastrucure and ageing machinery / equipment'
    engi_disc.oil_gas.guidelines = 'Avoid Landmen / Pipeline Inspectors'
    engi_disc.process.guidelines = 'Ask about W2E, Biofuels, Renewables'
    engi_disc.surveyor.guidelines = 'Check for Underground Utility Locating / Underground Work'

    # Total engineering
    engi_disc.total.percentage = sum([vbl.percentage for vbl in lst_engi_discipline_vbl])
    engi_disc.total.rateable_exposure = sum([vbl.rateable_exposure for vbl in lst_engi_discipline_vbl])
    engi_disc.total.base_premium = sum([vbl.base_premium for vbl in lst_engi_discipline_vbl])
    engi_disc.total.base_premium_size_discount = sum([vbl.base_premium_size_discount for vbl in lst_engi_discipline_vbl])

    # Total average engineering
    # Assign names, otherwise get error: 'referenced before assignment'
    sp_engi_base_rate_override = 0
    sp_engi_oth = 0

    # Default base rate x rateable exposure
    sp_engi_def_base_rate = sum([vbl.default_base_rate * vbl.rateable_exposure for vbl in lst_engi_discipline_vbl])

    # Product base rates and exposure
    for loop_vbl in lst_engi_discipline_vbl:

        # Other is an 'input', not an 'override'
        if (loop_vbl in [engi_disc.other_one, engi_disc.other_two, engi_disc.other_three, engi_disc.other_four, engi_disc.other_five]):
            sp_engi_oth = loop_vbl.base_rate_override
        else:
            sp_engi_oth = loop_vbl.base_rate_override.selected

        # Base rate override x rateable exposure
        sp_engi_base_rate_override += sp_engi_oth * loop_vbl.rateable_exposure
        
    # Total average default and selected base rates
    if (engi_disc.total.rateable_exposure == 0):
        engi_disc.total.default_base_rate = 1
        engi_disc.total.base_rate_override = 1
    else:
        engi_disc.total.default_base_rate = sp_engi_def_base_rate / engi_disc.total.rateable_exposure
        engi_disc.total.base_rate_override = sp_engi_base_rate_override / engi_disc.total.rateable_exposure   


# CONTRACTOR DISCIPLINE BASE RATES ##############################################################

    # Contractor base rate parameters
    param_con_baserates = hx.params.tbl_contractors_rates_mins[["Discipline", "Selected Base Rate"]]
    param_con_baserates = param_con_baserates[~param_con_baserates["Discipline"].str.startswith("Other")]

    # Define where contractor discipline variables live in data schema
    con_disc = hxd.cds.exposure.granular.contractor

    # Considerations
    con_disc.considerations = "Consider: Minimums, $10m CVs Lower, RDI, Good state, No resi, No GL Claims, Clean"

    # Contractor rateable exposure
    con_selected_rateable_exposure = 0

        # Construction with In House Design
    if (cons_with_in_house.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += cons_with_in_house.override_avg_rateable_exposure
        # Construction with Sun Contracted Design
    if (cons_sub_con.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += cons_sub_con.override_avg_rateable_exposure
        # Design Only - No Construction
    if (desi_no_cons.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += desi_no_cons.override_avg_rateable_exposure
        # Construction Only - No Design
    if (cons_no_desi.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += cons_no_desi.override_avg_rateable_exposure
        # At Risk Construction Management
    if (at_risk.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += at_risk.override_avg_rateable_exposure
        # Agency Construction Management
    if (agency_con.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += agency_con.override_avg_rateable_exposure
        # Other (Specify)
    if (other_exposure.rateable_exposure_discipline == "Contractor"):
        con_selected_rateable_exposure += other_exposure.override_avg_rateable_exposure     

    # Size discount
    con_selected_rateable_exposure_size_discount = con_selected_rateable_exposure * (1 - agg_exposure.size_discount)

    # List of discipline variables
    lst_con_discipline_vbl = [
        con_disc.asbestos_lead,
        con_disc.build_envelop,
        con_disc.carpenter,
        con_disc.concrete,
        con_disc.demolition,
        con_disc.drywall,
        con_disc.electrical,
        con_disc.enviro,
        con_disc.fp_dry,
        con_disc.fp_wet,
        con_disc.foundation_excav,
        con_disc.general_comm,
        con_disc.general_resi,
        con_disc.glazing,
        con_disc.hvac_industrial,
        con_disc.hvac_non_industrial,
        con_disc.landscape,
        con_disc.masonry,
        con_disc.mech,
        con_disc.reno_non_resi,
        con_disc.oil_gas,
        con_disc.painting,
        con_disc.plumbing,
        con_disc.resi_reno,
        con_disc.roofing,
        con_disc.steel,
        con_disc.telecom_heavy,
        con_disc.telecom_light,
        con_disc.utilities,
        con_disc.other_one,
        con_disc.other_two,
        con_disc.other_three,
        con_disc.other_four,
        con_disc.other_five
        ]

    # List of discipline strings - for matching to parameter levels
    lst_con_discipline_str = [
        'Asbestos / Lead Contractor',
        'Building Enveloping Contractor',
        'Carpenter',
        'Concrete Contractor',
        'Demolition Contractor',
        'Drywall Contractor',
        'Electrical Contractor',
        'Environmental Contractor',
        'Fire Protection (Dry) Contractor',
        'Fire Protection (Wet) Contractor',
        'Foundation & Excavation Contractor',
        'General Contractor (Commercial)',
        'General Contractor (Residential)',
        'Glazing Contractor ',
        'HVAC (Industrial) Contractor',
        'HVAC (Non-Industrial) Contractor',
        'Landscape Contractor',
        'Masonry Contractor',
        'Mechanical Contractor',
        'Non residential Renovation Contractor',
        'O&G Contractor',
        'Painting Contractor',
        'Plumbing Contractor',
        'Renovation Contractor (Residential)',
        'Roofing Contractor',
        'Steel Contractor',
        'Telecommunications (Heavy) Contractor ',
        'Telecommunications (Light) Contractor ',
        'Utility Contractor',
        'Other 1 (Specify)',
        'Other 2 (Specify)',
        'Other 3 (Specify)',
        'Other 4 (Specify)',
        'Other 5 (Specify)'        
        ]

    # Loop through the discipline variables
    for loop_vbl, loop_str in zip(lst_con_discipline_vbl, lst_con_discipline_str):
        
        # Calculate rateable_exposure
        loop_vbl.rateable_exposure = con_selected_rateable_exposure * loop_vbl.percentage
        loop_vbl.rateable_exposure_size_discount = con_selected_rateable_exposure_size_discount * loop_vbl.percentage

        # Calculate base premium
        if (loop_vbl in [con_disc.other_one, con_disc.other_two, con_disc.other_three, con_disc.other_four, con_disc.other_five]):
            # Set default base rate to override, because UWs enter in the value for Other disciplines            
            loop_vbl.default_base_rate = loop_vbl.base_rate_override
            loop_vbl.base_premium = loop_vbl.base_rate_override * loop_vbl.rateable_exposure/100
            loop_vbl.base_premium_size_discount = loop_vbl.base_rate_override * loop_vbl.rateable_exposure_size_discount/100
        else:
            # Lookup contractor base rates
            loop_vbl.default_base_rate = param_con_baserates[param_con_baserates['Discipline'] == loop_str]['Selected Base Rate'].iloc[0]        
            # Default to contractor base rates
            loop_vbl.base_rate_override.calculated = loop_vbl.default_base_rate
            loop_vbl.base_premium = loop_vbl.base_rate_override.selected * loop_vbl.rateable_exposure/100
            loop_vbl.base_premium_size_discount = loop_vbl.base_rate_override.selected * loop_vbl.rateable_exposure_size_discount/100
                                                           
    pass
    
    # Contractor Guidelines specification
    con_disc.enviro.guidelines = 'Less EX CPL'
    con_disc.general_resi.guidelines = 'Regret NYC. Watch CT crumbling foundations & concrete'
    con_disc.hvac_industrial.guidelines = 'Industrial HVAC is C. Think about Mold exposures'
    con_disc.landscape.guidelines = 'Referr Golf Courses. Sublimit BI/PD Swimming pools'
    con_disc.oil_gas.guidelines = 'No pipeline work'
    con_disc.resi_reno.guidelines = 'No condo conversions or Metro office space'
    con_disc.telecom_heavy.guidelines = 'Regret Condos. 25% AP for homes over $500k'
    con_disc.utilities.guidelines = 'No California post wildfires'

    # Total contractor
    con_disc.total.percentage = sum([vbl.percentage for vbl in lst_con_discipline_vbl])
    con_disc.total.rateable_exposure = sum([vbl.rateable_exposure for vbl in lst_con_discipline_vbl])
    con_disc.total.base_premium = sum([vbl.base_premium for vbl in lst_con_discipline_vbl])
    con_disc.total.base_premium_size_discount = sum([vbl.base_premium_size_discount for vbl in lst_con_discipline_vbl])
        
    # Total average contractor
    # Assign names, otherwise get error: 'referenced before assignment'
    sp_con_base_rate_override = 0
    sp_con_oth = 0

    # Default base rate x rateable exposure
    sp_con_def_base_rate = sum([vbl.default_base_rate * vbl.rateable_exposure for vbl in lst_con_discipline_vbl])

    # sumproduct base rates and exposure
    for loop_vbl in lst_con_discipline_vbl:

        # other is an 'input', not an 'override'
        if (loop_vbl in [con_disc.other_one, con_disc.other_two, con_disc.other_three, con_disc.other_four,con_disc.other_five]):
            sp_con_oth = loop_vbl.base_rate_override
        else:
            sp_con_oth = loop_vbl.base_rate_override.selected

        # base rate override x rateable exposure
        sp_con_base_rate_override += sp_con_oth * loop_vbl.rateable_exposure
        

    # Total average default and selected base rates
    if (con_disc.total.rateable_exposure == 0):
        con_disc.total.default_base_rate = 1
        con_disc.total.base_rate_override = 1
    else:
        con_disc.total.default_base_rate = sp_con_def_base_rate / con_disc.total.rateable_exposure
        con_disc.total.base_rate_override = sp_con_base_rate_override / con_disc.total.rateable_exposure   

# MINIMUM PREMIUMS ##############################################################

    # Define minimum premium parameter table    
    param_engi_minprem = hx.params.tbl_engineering_rates_mins[["Discipline", "Minimum Premium $1m", "Minimum Retention $1m"]]
    param_con_minprem = hx.params.tbl_contractors_rates_mins[["Discipline", "Minimum Premium $1m", "Minimum Retention $1m"]]


# ENGINEERING MINIMUMS ##############################################################
        
    # Premium
    if (engi_disc.total.rateable_exposure != 0):
        engi_disc.total.min_premium = sum([param_engi_minprem[param_engi_minprem['Discipline'] == string]['Minimum Premium $1m'].iloc[0] * vbl.percentage for vbl, string in zip(lst_engi_discipline_vbl, lst_engi_discipline_str)])
    else: 
        engi_disc.total.min_premium = 0
        
    # Deductible
    if (engi_disc.total.rateable_exposure != 0):
        engi_disc.total.min_deductible = sum([param_engi_minprem[param_engi_minprem['Discipline'] == string]['Minimum Retention $1m'].iloc[0] * vbl.percentage for vbl, string in zip(lst_engi_discipline_vbl, lst_engi_discipline_str)])
    else: 
        engi_disc.total.min_deductible = 0

# CONTRACTOR MINIMUMS ##############################################################

    # Premium
    if (con_disc.total.rateable_exposure != 0):
        con_disc.total.min_premium = sum([param_con_minprem[param_con_minprem['Discipline'] == string]['Minimum Premium $1m'].iloc[0] * vbl.percentage for vbl, string in zip(lst_con_discipline_vbl, lst_con_discipline_str)])
    else:
        con_disc.total.min_premium = 0

    # Deductible
    if (con_disc.total.rateable_exposure != 0):
        con_disc.total.min_deductible = sum([param_con_minprem[param_con_minprem['Discipline'] == string]['Minimum Retention $1m'].iloc[0] * vbl.percentage for vbl, string in zip(lst_con_discipline_vbl, lst_con_discipline_str)])
    else:
        con_disc.total.min_deductible = 0

# VALIDATION CHECKS #################################################################
    # Check engineering percentages sum to 1
    if eng_selected_rateable_exposure > 0:
        if (round(engi_disc.total.percentage * 100)/100 != 1):        
            set_invalid(hxd,"engineering_disp_percentage","Discipline Details Page: Engineering percentages do not sum to 100%.")
        else:
             set_valid(hxd, "engineering_disp_percentage")
    # Check contractors percentages sum to 1
    if con_selected_rateable_exposure > 0:
        if (round(con_disc.total.percentage * 100)/100 != 1):        
            set_invalid(hxd,"contractor_disp_percentage","Discipline Details Page: Contractor percentages do not sum to 100%.")
        else:
            set_valid(hxd, "contractor_disp_percentage")
