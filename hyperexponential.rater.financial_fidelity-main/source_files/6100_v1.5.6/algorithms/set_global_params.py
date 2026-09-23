import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Function to check for leap year
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# Function to check if the policy covers a leap day
def covers_leap_day(inception, expiry):
    # If the policy spans multiple years
    for year in range(inception.year, expiry.year + 1):
        if is_leap_year(year):
            feb29 = datetime(year, 2, 29).date()
            if inception <= feb29 <= expiry:
                return True
    return False


def set_global_params(hxd):
    layer = hxd.cds.layers[0]  # Use only first layer as model not currently set up for multiple layers
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
    state_param = hx.params.StateLookup
    institution_param = hx.params.InstitutionTypes
    params_cov = hx.params.Coverages
    params_basic_cov = hx.params.BasicUnitOfCoverage

    # ~~~~~~~~~~~~~~ GLOBAL ~~~~~~~~~~~~~~~~~~~
    
    gbl_params = hx.params.GlobalParams
    
    gbl_params_key = {
        "priced_to_lr": None,
        "benchmark_lr": None,
        "assumed_brokerage": None,
        "min_deductible": None,
        "basic_unit_upper_limit": None,
    }

    for key in gbl_params_key.keys():
        gbl_params_key[key] = gbl_params[gbl_params["Variable"] == key]["Value"].iloc[0]

    # Set global variables
    layer.priced_to_lr = gbl_params_key["priced_to_lr"] # Set to 0.7 for debugging
    layer.benchmark_lr = gbl_params_key["benchmark_lr"]
    layer.assumed_brokerage = gbl_params_key["assumed_brokerage"] # Set to 0 for debugging
    layer.min_deductible = gbl_params_key["min_deductible"]  

    hxd.cds.database_id = hx.meta.policy_option_id

    hxd.cds.yoa = hxd.hx_core.inception_date.year  


    # ~~~~~~~~~~~~~~ GENERAL PARAMETERS ~~~~~~~~~~~~~~~~~~~
    # Set USD default
    hxd.hx_core.premium_currency = "USD"

    # Set primary/excess
    layer.is_primary_excess = "Primary"

    # Set bound status
    layer.is_bound = True if layer.status=="Bound" else False

    # # Set flag to show rate change page
    if hxd.model_state.show_landing_page: 
        hxd.show_rate_change = False
    else:
        hxd.show_rate_change = hxd.cds.standard_fields.is_renewal 
    
    hxd.pricing_info = f"Note: Input all figures at 100% share"

    # Set Safe Deposit/Computer Crime flags
    layer.include_safe_deposit_box = max(
        layer.coverages.cover_24_liability_depository.include,
        layer.coverages.cover_25_loss_property_damage.include
        )
    layer.include_computer_crime = max(
        layer.coverages.cover_26_computer_fraud.include,
        layer.coverages.cover_27_data_processing.include,
        layer.coverages.cover_28_voice_transfer_fraud.include,
        layer.coverages.cover_29_telefacsimile_transfer_fraud.include,
        layer.coverages.cover_30_hacker.include,
        layer.coverages.cover_31_virus.include,
        layer.coverages.cover_32_voice_computer_fraud.include,
        layer.coverages.cover_33_account_takeover.include
        )

    # Calculate term adjustment factor. Divide the actual policy period by the number of effective days for a one-year policy with the same 
    # inception date to account for leap days.
    days_in_year = ((hxd.hx_core.inception_date + relativedelta(years=+1))- hxd.hx_core.inception_date).days
    layer.term_adjustment = ((hxd.hx_core.expiry_date - hxd.hx_core.inception_date).days)/(days_in_year)
    
    if hxd.cds.standard_fields.insured_state_or_province:
        layer.insured_state_loss_cost_multiplier = state_param[state_param["State"] == hxd.cds.standard_fields.insured_state_or_province]["LCM"].iloc[0]
        layer.rating_note = state_param[state_param["State"] == hxd.cds.standard_fields.insured_state_or_province]["Rating Note"].iloc[0]
    
    else:
        layer.insured_state_loss_cost_multiplier = 0
        
    hxd.cds.policy_form_used = institution_param[institution_param["institution_type"] == hxd.cds.type_of_insured]["form"].iloc[0]
    
    # Calculate average assets, there is a validation to ensure UW fill in both
    hxd.cds.exposure.aggregate.average_assets = (hxd.cds.exposure.aggregate.assets_june + hxd.cds.exposure.aggregate.assets_december) / 2
    
    # layer.basic_unit_of_coverage = np.interp(layer.average_assets, params_basic_cov['assets'], params_basic_cov['basic_unit_of_coverage'])
    hxd.cds.exposure.aggregate.basic_unit_of_coverage = params_basic_cov[params_basic_cov['assets'] <= hxd.cds.exposure.aggregate.average_assets]['basic_unit_of_coverage'].iloc[-1]
    # SA: Where does the 500e3 come from? it's a hardcoded value but it's hidden away at the end of that line. Might be worth moving it to somewhere 
    # more obvious in case it ever needs changing in the future
    layer.basic_unit_upper_limit = gbl_params_key["basic_unit_upper_limit"] if hxd.cds.policy_form_used != "Form 25" else 500e3
    

    # ~~~~~~~~~~~~~~~~~~~~~~~ SET INCLUDE OR EXCLUDE ~~~~~~~~~~~~~~~~~~~~~~~~
    
    # Import static list of nodes and coverage names
    lst_cover_vbl = lst.cover_hxd_vbl(hxd)
    lst_cover_names = lst.cover_names

    # Loop though parameter table to asses whether, for the selected form, the cover is available or not
    for loop_vbl, loop_name in zip(lst_cover_vbl, lst_cover_names):
        if params_cov[params_cov["Coverage Type"] == loop_name][hxd.cds.policy_form_used].iloc[0] == "Yes":
            loop_vbl.available = True
        else:  
            loop_vbl.available = False

    # Create a final include field which combines underwriter selection and cover availability
    for loop_vbl in lst_cover_vbl:
        if loop_vbl.available and loop_vbl.include:  
            loop_vbl.final_include = True
        else:
            loop_vbl.final_include = False
    
    # Flags to show whether the below input tables need to be shown
    hxd.show_safe_deposit_policy_table = any(obj.final_include for obj in lst_cover_vbl[23:25])
    show_computer_systems_fraud_fi = any(obj.final_include for obj in lst_cover_vbl[19:23])
    show_computer_systems_fraud = any(obj.final_include for obj in lst_cover_vbl[25:])
    hxd.show_computer_crime_policy_table = show_computer_systems_fraud_fi or show_computer_systems_fraud
    
    

    # Set info for computer systems fraud inputs

    exp_agg.independent_software_contractors.info = "Are independent software contractors authorized by the insured to design, implement, or service programs for the insured's computer system?"
    exp_agg.access_to_computer.info = "Is access to the insured's computer system (for example by customers, agents, brokers or other outside parties) permitted?"
    exp_agg.atms_accessed_to_system.info = "Are owned or leased ATMs accessed to the insured's computer system?"
    exp_agg.does_include_clearing_houses.info = "Does the insured's operations include Automated Clearing Houses using Federal Reserve computer facilities?"
    exp_agg.additional_computer_system.info = "Does the insured have additional computer system such as but not limited to: CHIPS, SWIFT, etc. (but excluding ATM Systems)?"
    exp_agg.other_atm_systems.info = "Does the insured have shared or other participatory ATM Systems?"
    exp_agg.use_telex.info = "Does the insured use tested telex or other similar means of tested communication?"

    # Set info for specific coverages inputs
    hxd.checking_accounts_info = "Only for Savings Banks, Savings and Loans Associations, and Federal Home Loan Banks"
    hxd.loan_to_deposit_ratio_info = "Only needed for Form 24"

    # Calculate loss cost for computer systems fraud
    # SA: These hardcoded values below - could these be stored in a parameter table or something similar? 
    # It's a lot of hardcoded values at once and these look like they are likely to be changed eventually
    loss_cost_total = 0.06
    if layer.coverages.cover_20_computer_fraud_fi.final_include is True or layer.coverages.cover_26_computer_fraud.final_include is True:
        if exp_agg.independent_software_contractors.include:
            if exp_agg.independent_software_contractors.how_many > 0:
                exp_agg.independent_software_contractors.loss_cost = min(0.08 + (exp_agg.independent_software_contractors.how_many - 1) * 0.03, 0.2)
            else:
                exp_agg.independent_software_contractors.loss_cost = 0
            loss_cost_total += exp_agg.independent_software_contractors.loss_cost

        if exp_agg.access_to_computer.include:
            exp_agg.access_to_computer.loss_cost = 0.06
            loss_cost_total += exp_agg.access_to_computer.loss_cost
        
        if exp_agg.atms_accessed_to_system.include:
            exp_agg.atms_accessed_to_system.loss_cost = min(exp_agg.atms_accessed_to_system.how_many, 15) * 0.005
            loss_cost_total += exp_agg.atms_accessed_to_system.loss_cost

        if exp_agg.does_include_clearing_houses.include:
            exp_agg.does_include_clearing_houses.loss_cost = 0.03
            loss_cost_total += exp_agg.does_include_clearing_houses.loss_cost
        
        if exp_agg.does_use_fed_wire.include:
            exp_agg.does_use_fed_wire.loss_cost = 0.08
            loss_cost_total += exp_agg.does_use_fed_wire.loss_cost
        
        if exp_agg.additional_computer_system.include:
            exp_agg.additional_computer_system.loss_cost = 0.06 * exp_agg.additional_computer_system.how_many
            loss_cost_total += exp_agg.additional_computer_system.loss_cost

        if exp_agg.other_atm_systems.include:
            exp_agg.other_atm_systems.loss_cost = 0.005 * exp_agg.other_atm_systems.how_many
            loss_cost_total += exp_agg.other_atm_systems.loss_cost

        if exp_agg.use_telex.include:
            exp_agg.use_telex.loss_cost = 0.06
            loss_cost_total += exp_agg.use_telex.loss_cost
        
    layer.computer_crime_total.loss_cost = loss_cost_total


