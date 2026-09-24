import hx
import re
import pandas as pd
import numpy as np
import math
import algorithms.rate_utilities as utils
import algorithms.global_parameters as gparams
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as params
from scipy.stats import gamma, poisson, lognorm, norm
from algorithms import parameter_tables_schema as params
from operator import itemgetter
from datetime import datetime, date
from dateutil import relativedelta

def rate_pricing(hxd):

#### Setup ####
    mcap = hxd.cds.exposure.aggregate.revised_market_cap
    is_side_a = hxd.cds.is_side_a

#### Algorithms ####
    # Frequency and dismissal rates
    variables = process_freq_variables(hxd)
    if mcap is not None:
        variables = process_freq(hxd, variables)

    # Severity
        variables = process_sev(hxd, mcap, variables)

    # Additional Side A factors
        if is_side_a is not None:
            variables = calc_side_a_factors(hxd, variables)

    # TPI metrics
        tpi_metrics = process_tpi_metrics(hxd, is_side_a, variables)
        
    # Layer technical price
        process_layers(hxd, is_side_a, variables)
        
    # Bridge premium
    if hxd.cds.bridge_countries:
        process_bridge_premium(hxd)

#### Data Capure ####
    # Setting fields in the cds for downstream processes
    set_commmon_fields(hxd)

### For data with no cleaned comments - check and clean comments
    clean_comments(hxd)



def strip_html_tags(text):
    # Remove HTML tags using a regular expression
    if text is None:
        clean_text = None
    else:
        clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text

def clean_comments(hxd):
    modifiers=[
        'management_corp_gov',
        'business_financial_model_factors',
        'significant_event_factors',
        'stock_market_factors',
        'derivative',
        'regulatory',
        'ma'
    ]
    
    for mod in modifiers:
        comment = getattr(getattr(hxd.cds.modifiers, mod),"comment")
        comment_plain_text = getattr(getattr(hxd.cds.modifiers, mod),"comment_plain_text")
        # if (comment_plain_text is None) and (comment is not None):
        comment_plain_text = strip_html_tags(comment)
        setattr(getattr(hxd.cds.modifiers, mod),"comment_plain_text", comment_plain_text)
    


#####################################################################################################################
################################################ Frequency Functions ################################################
#####################################################################################################################

def process_freq(hxd, variables):
    ind = hxd.cds.key_industry
    freq = hxd.cds.frequency
    calc = hxd.cds.tpi_calculations

    # Inputs from hxd
    sector_ids = [ind.sector_id, ind.sector_id_2, ind.sector_id_3]
    sectors =  [ind.sector_name, ind.sector_2, ind.sector_3]
    blended = ind.blended_sic
    variables["blended"] = blended
    sector_wghts = [
        ind.sic_percentage if ind.sic_percentage else 0, 
        ind.sic_percentage_2 if ind.sic_percentage_2 else 0, 
        ind.sic_percentage_3 if ind.sic_percentage_3 else 0
        ]
    overrides = [
        ind.sector_uw_override,
        ind.sector_uw_override_2,
        ind.sector_uw_override_3
    ]
    variables["sca_override"] = freq.sca_freq_override 
    
    if (ind.sic_percentage is not None): #and (ind.sector_id is not None):
#### Frequencies ####
        # Calculate frequencies for each claim type and their interactions
        variables = calc_freq_sca(sector_ids, blended, sector_wghts, overrides, variables)
        variables = calc_freq_der(sector_ids, blended, sector_wghts, variables)
        variables = calc_freq_ma(sectors, blended, sector_wghts, variables)
        variables = calc_freq_inter(sector_ids, blended, sector_wghts, variables)

        # Outputs to hxd
        set_frequencies(sectors, sector_wghts, blended, freq, ind, variables)

        # Updates TPI Calculation screen
        set_tpi_calcs_freq(calc, sectors, blended, sector_wghts, variables)

#### Frequency after Dismissal rates ####
        variables = calc_dismissal_freq(sector_ids, blended, sector_wghts, variables)

        # Updates TPI Calculation screen
        set_tpi_calcs_dismissal(calc, sectors, sector_wghts, variables)

    return variables


def process_freq_variables(hxd):
    """
    Generates the frequency variables used to calculate the final frequency.

    Includes:
      1) IPO lag
      2) CapIQ factor
      3) Subjective modifiers
      4) Market cap frequency
      5) Other claim type frequency factors
      6) Base frequencies
      7) Sector IPO factors
      8) Interaction terms
      9) Dismissal rates
      10) Domicile factor
    """

    # Creating empty data dictionary to be populated
    variables = {}

    agg = hxd.cds.exposure.aggregate
    ind = hxd.cds.key_industry
    freq = hxd.cds.frequency
    calc = hxd.cds.tpi_calculations
    mod = hxd.cds.modifiers

    # Used for dismissal rates and IPO sector factors
    df_base_freq = hx.params.ref_base_frequencies

#### IPO factor ####
    # Pulling max ipo parameter
    df_ipo = hx.params.ref_ipo_lag
    ipo_max = max(df_ipo["Lag"])  

    # Setting the lag 
    variables["ipo_lag"] = calc_ipo_lag(df_ipo, hxd.hx_core.inception_date, agg.ipo_date, ipo_max, agg.ignore_ipo)

#### CapIQ factor ####
    df_min_trading_vol = hx.params.ref_min_trading_volumne
    df_vol_of_trading = hx.params.ref_volatility_of_trading
    df_execs_under_50 = hx.params.ref_execs_under_50
    df_years_in_business = hx.params.ref_years_in_business
    df_capiq  = hx.params.ref_capiq

    min_trading_vol = agg.minimum_trading_volume 
    vol_of_trading = agg.volatility_of_trading
    execs_under_50 = agg.execs_under_age_50

    # Set defaults for when no values are extracted from CapIQ
    min_trading_vol_factor = 1
    vol_of_trading_factor = 1
    execs_under_50_factor = 1
    years_in_business_factor = 1

    # Pulling CapIQ parameters
    capiq_min = utils.look_up("min", "ParameterName", "Value", df_capiq,0)
    capiq_max = utils.look_up("max", "ParameterName", "Value", df_capiq,0)
    capiq_scale = utils.look_up("scale", "ParameterName", "Value", df_capiq,0)

    # Calculates years in business from the year founded
    if (hxd.hx_core.inception_date is not None) and (agg.year_founded is not None):
        if hxd.hx_core.inception_date.year >= agg.year_founded:
            years_in_business = hxd.hx_core.inception_date.year - agg.year_founded
        else:
            hx.errors.validation("Year founded must be on or before inception year")
            years_in_business = None
    else:
        years_in_business = None

    # Final factor
    # Interpolates each of the values against the corresponding tables
    if min_trading_vol is not None:
        min_trading_vol_factor = interp_table_row(df_min_trading_vol, min_trading_vol, "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    if vol_of_trading is not None:
        vol_of_trading_factor = interp_table_row(df_vol_of_trading, vol_of_trading, "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    if execs_under_50 is not None:
        execs_under_50_factor = interp_table_row(df_execs_under_50, execs_under_50, "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
    if years_in_business is not None:
        years_in_business_factor = interp_table_row(df_years_in_business, years_in_business, "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)

    # Calculates the CapIQ factor subject to min, max and scale entered
    capiq_factor = min_trading_vol_factor * vol_of_trading_factor * execs_under_50_factor * years_in_business_factor
    capiq_factor = max(min(capiq_factor, capiq_max), capiq_min)
    variables["capiq_factor"] = 1 + (capiq_factor - 1) / capiq_scale

    # Set the fields in the TPI Calculations screen
    calc.minimum_trading_volume_factor.value = min_trading_vol_factor
    calc.volatility_of_trading_factor.value = vol_of_trading_factor
    calc.execs_under_age_50_factor.value = execs_under_50_factor
    calc.years_in_business_factor.value = years_in_business_factor
    calc.capiq_total_factor.value = variables["capiq_factor"]

    # Comment is hardcoded
    calc.capiq_total_factor.info = (
        "Factor of 1 is the expected value for the book. Above 1 means the account is riskier on average by the given metric, and less risky when less than 1."
    )

#### Subjective modifiers ####
    # Defining parameter table
    df_freq_mod_bounds = hx.params.ref_freq_mod_bounds 

    ## SCA ##
    # Handles blank modifiers
    mod_management_corp_gov = mod.management_corp_gov.value / 100 if mod.management_corp_gov.value else 0
    mod_business_financial_model_factors  = mod.business_financial_model_factors.value / 100 if mod.business_financial_model_factors.value else 0 
    mod_significant_event_factors = mod.significant_event_factors.value / 100 if mod.significant_event_factors.value else 0
    mod_stock_market_factors = mod.stock_market_factors.value / 100 if mod.stock_market_factors.value else 0
    mod_regulatory = mod.regulatory.value / 100 if mod.regulatory.value else 0 

    modifier_nodes = ["management_corp_gov", "business_financial_model_factors", "significant_event_factors", "stock_market_factors", "regulatory"]

    # Calculates the modifier, sets the min and max in the rater, and performs the validations
    variables["mod_sca"] = calc_subj_modifier( 
        hxd.non_cds.modifier_labels,
        mod,
        ["Management and Corporate Gov", "Business/Financial Model Factors", "Significant Event Factors", "Stock Market Factors", "Regulatory"],
        modifier_nodes,      
        modifier_nodes,         
        [mod_management_corp_gov, mod_business_financial_model_factors, mod_significant_event_factors, mod_stock_market_factors, mod_regulatory],
        df_freq_mod_bounds,
        gparams.sca_max_discount
    )

    # Display the SCA modifier as the frquency adjustment factor
    mod.freq_adj_factor.value = variables["mod_sca"]

    # Combining with objective factors to make overall freq adjustments clearer to users
    mod.obj_freq_adj_factor.value = variables["capiq_factor"]
    mod.obj_freq_adj_factor.info = "Total of the CapIQ factors detailed in the TPI Calculations page" 
    mod.total_freq_adj_factor.value = variables["mod_sca"] * variables["capiq_factor"]

    ## Derivative ##
    mod_derivative = mod.derivative.value / 100 if mod.derivative.value else 0
    
    variables["mod_der"] = calc_subj_modifier(
            hxd.non_cds.modifier_labels, 
            mod,
            ["Derivative"],
            ["derivative"],
            ["derivative"],        
            [mod_derivative],
            df_freq_mod_bounds,
            0
        )
    
    ## MA ##
    # Modifier has been removed but want to include a comment
    mod.ma.info = "Modifier has been removed but comment from expiry is shown for reference. Any change in risk should be applied in other modifiers"

#### Market cap frequency ####
    variables["mcap"] = agg.revised_market_cap
    # Parameter table needed here and to calculate dismissal rates
    df_derivative_freq_mod = hx.params.ref_derivative_freq_modifiers
    # Parameter table needed here and to calculate domicile factor
    df_sca_freq_mod = hx.params.ref_sca_freq_modifiers

    if variables["mcap"] is not None:
        #Setting min and max to avoid errors
        variables["mcap_bound"] = min(max(1, variables["mcap"]), 999e9)

        # Parameter tables only needed in this statement
        df_mcap_banding = hx.params.ref_mcap_banding
        df_ma_freq_mod = hx.params.ref_ma_freq_modifiers

        # Calculates the market cap frequencies for the given coverage
        # The maxmium market cap used to calculate the frequency is different for Side A policies
        variables["mcap_factor_sca"] = calc_mcap_factor("sca", df_sca_freq_mod, variables["mcap_bound"], hxd.cds.is_side_a)
        variables["mcap_factor_der"] = calc_mcap_factor("der", df_mcap_banding, variables["mcap_bound"])
        variables["mcap_factor_ma"] = calc_mcap_factor("ma", df_mcap_banding, variables["mcap_bound"])

        # This is used as the frequency cap throughout the rest of the code
        variables["mcap_freq_cap"] = utils.look_up("SCAFrequencyCap", "ParameterName", "Value", df_sca_freq_mod, 0)
        variables["mcap_freq_min"] = utils.look_up("MinBand5Trigger", "ParameterName", "Value", df_sca_freq_mod, 0)

#### Other claim type frequency factors ####
        variables["scale_factor_der"] = utils.look_up("DerivativeScaleFactor", "ParameterName", "Value", df_derivative_freq_mod, 0)
        variables["freq_cap_der"] = utils.look_up("DerivFrequencyCap","ParameterName", "Value", df_sca_freq_mod, 0)
        
        variables["scale_factor_ma"] = utils.look_up("MAScaleFactor", "ParameterName", "Value", df_ma_freq_mod, 0)

#### Base frequencies ####
    variables["freq_base_sca_1"] = ind.sector_base_frequency if ind.sector_base_frequency else 0
    variables["freq_base_sca_2"] = ind.sector_base_frequency_2 if ind.sector_base_frequency_2 else 0
    variables["freq_base_sca_3"] = ind.sector_base_frequency_3 if ind.sector_base_frequency_3 else 0

#### IPO sector factors ####
    variables["ipo_factor_1"] = utils.look_up(ind.sector_name, "Sector_Desc", "IPO Factor", df_base_freq, 0)
    variables["ipo_factor_2"] = utils.look_up(ind.sector_2, "Sector_Desc", "IPO Factor", df_base_freq, 0)
    variables["ipo_factor_3"] = utils.look_up(ind.sector_3, "Sector_Desc", "IPO Factor", df_base_freq, 0)

#### Interaction terms ####
    df_interactions = hx.params.ref_interaction_modifiers
    variables["inter_sca_der"] = utils.look_up("SCADerivative", "ParameterName", "Value", df_interactions, 0)

#### Dismissal rates ####
    df_dismissal_mod = hx.params.ref_dismissal_modifiers
    
    variables["dr_sca_1"] = utils.look_up(ind.sector_name, "Sector_Desc", "Dismissal rates", df_base_freq, 0)
    variables["dr_sca_2"] = utils.look_up(ind.sector_2, "Sector_Desc", "Dismissal rates", df_base_freq, 0)
    variables["dr_sca_3"] = utils.look_up(ind.sector_3, "Sector_Desc", "Dismissal rates", df_base_freq, 0)

    variables["dr_der"] = utils.look_up("Derivatives", "ParameterName", "Value", df_dismissal_mod, 0)
    variables["dr_ma"] = utils.look_up("M&A", "ParameterName", "Value", df_dismissal_mod, 0)

    # Dismissal rate for derivative for this case only comes from the frequency table
    variables["freq_dr_der"] = utils.look_up("DerivativeDismissalRate", "ParameterName", "Value", df_derivative_freq_mod, 0)

#### Domicile factor ####
    # Pulling Canada factor
    variables["canada_factor"] = utils.look_up("CanadaFactor", "ParameterName", "Value", df_sca_freq_mod, 0)
    # Saving company to directory
    variables["country"] = hxd.cds.company_country

    return variables

def calc_ipo_lag(df, inception, ipo_date, ipo_max, ignore):
    """
    Calculates the IPO lag between inception and ipo date subject to a maxmium
    """

    if (ipo_date is not None) and (ignore is False):
        # Uses the pro rata calc function
        ipo_lag = calc_pro_rata(ipo_date, inception, 2) * 360
        ipo_lag = min(math.floor(ipo_lag / 360), ipo_max)

        # Validation
        #if utils.year_diff(ipo_date, inception, False) < 0:
        #    hx.errors.validation("IPO date must be on or before inception")
    else:
        ipo_lag = ipo_max
    
    return ipo_lag


def calc_pro_rata(inception, expiry, method):
    """
    For a given inception date and expiry date calculates the pro rata loading
    There are multiple methods in this function that can be seleced by the "method" input. Including:
    1) Using the function from utitilies to calculate yeardiff between inception and expiry
        Pro: most accurate formula. Con: won't match excel
    2) Recreates excel function YEARFRAC with basis 0.
        Pro: will equal old excel rater when testing. Con: less accurate
    """

    # Method 1:
    if method == 1:
        pro_rata = utils.year_diff(inception, expiry, False)
    # Method 2:
    elif method == 2:
        # Using the max to avoid a 0 when inception = expiry
        pro_rata = max((360 * (expiry.year - inception.year) + (30 * (expiry.month - inception.month) + (expiry.day - inception.day))), 1)
        pro_rata = pro_rata / 360

    return pro_rata


def calc_capiq_factor(values, tables, capiq_min, capiq_max, capiq_scale):
    """
    Calculates the capiq factor from the values and ref tables for each factor
    Starts by interpolating to find each value from the table
    The columns in the ref tables need to be: "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper"
    Then calculates the final factor subject to a min, max and scale
    """
    capiq_factor = 1
    
    for i, value in enumerate(values):
        if value is not None:
            factor = interp_table_row(tables[i], value, "Lower", "Upper", "SelectedRelativityLower", "SelectedRelativityUpper", 1)
            capiq_factor = capiq_factor * factor

    capiq_factor = max(min(capiq_factor, capiq_max), capiq_min)
    capiq_factor = 1 + (capiq_factor - 1) / capiq_scale
    
    return capiq_factor


def interp_table_row(df, value, x_lower, x_upper, f_lower, f_upper, if_out_of_range):
    """
    Interpolates a value from a given table
    Looks up the x value above and below and looks up f(x) from the table
    Returns input "if_out_of_range" if no above and below value in the table can be found
    """

    if (
        (value >= min(df[x_lower]))  & 
        (value < max(df[x_upper]))
    ):
        df_row = df[(df[x_lower] <= value) & (df[x_upper] > value)].iloc[0]
        xp = [df_row[x_lower], df_row[x_upper]]
        fp = [df_row[f_lower], df_row[f_upper]]
        result = np.interp(value, xp, fp)
    else:
        result = if_out_of_range
    return result


def calc_subj_modifier (modifier_labels_path, path, modifiers, data_labels, label_nodes, values, df_bound, mod_max):
    """
    First set the path of all the modifiers in the cds
    Then accepts the modifiers names, cds label and values as a lists and calculates the loading as the product
    Any modifier must be in the "Mod" column of the table
    The data label must be in the cds
    The modifiers must follow the same structure in the cds to update these correctly
    Sets all the min and max values in the view, and handles the validation
    The final modifier is then capped by the entered max
    """
    modifier = 1
    
    for i, mod in enumerate(modifiers):
        # Calc final modifier
        modifier = modifier * (1 + values[i])

        # Sets the min and max to be shown in the rater
        mod_row = df_bound[df_bound["Mod"] == mod].iloc[0] 
        mod_path = getattr(path, data_labels[i])
        setattr(mod_path, "min", mod_row["Min"])
        setattr(mod_path, "max", mod_row["Max"])

        # Sets validation so entries cannot be outside the range
        # Started coded updates the booleans for conditional formating. Need to figure out how to do this for individual table rows
        if (
            (values[i] < mod_row["Min"] / 100) or 
            (values[i] > mod_row["Max"] / 100)
        ):
            string = mod + " modifier must be within min and max"
            hx.errors.validation(string)
            setattr(modifier_labels_path, label_nodes[i], (f"{modifiers[i]} {const.incomplete_column}"))
        else:
            setattr(modifier_labels_path, label_nodes[i], f"{modifiers[i]}")

    modifier = max(modifier, mod_max)

    return modifier


def calc_mcap_factor(cov, df, mcap, side_a=False):
    """
    Calculates sca, derivative or m&a market cap frequency factor
    For SCA, uses the "calc_sca_mcap_factor" funtion below
    Column names are hardcoded
    """
    if cov == "sca":
        mcap_factor = calc_sca_mcap_factor(df, mcap, side_a)
    else:
        if mcap >= min(df["Lower"]): 
            # Pull upper and lower values from table for interpolation
            df_row = df[(df["Lower"] <= mcap) & (df["Upper"] > mcap)].iloc[0]
            xp = [df_row["Band"], df_row["Band"] + 1]

            # Geometric interpolation
            band = df_row["Band"] + np.log(mcap / df_row["Lower"]) / np.log(df_row["Upper"] / df_row["Lower"])

            if cov == "der":
                fp = [df_row["Derivative Freq Band Lower"], df_row["Derivative Freq Band Upper"]]
                mcap_factor = np.interp(band, xp, fp)
            elif cov == "ma":
                fp = [df_row["M&A Freq Band Lower"], df_row["M&A Freq Band Upper"]]
                mcap_factor = np.interp(band, xp, fp)
        else: 
            if cov == "der":
                mcap_factor = min(df["Derivative Freq Band Lower"])
            elif cov == "ma":
                mcap_factor = min(df["M&A Freq Band Lower"])

    return mcap_factor


def calc_sca_mcap_factor(df, mcap, side_a=False):
    """
    Calculates the sca market cap frequency factor from the ref table and market cap
    """
    mcap_cap = utils.look_up("Side A MCapMin","ParameterName", "Value", df, 0) if side_a else utils.look_up("MCapMin","ParameterName", "Value", df, 0)
    mcap_used = min(mcap_cap, mcap)
    mcap_base = utils.look_up("BaseMCap","ParameterName", "Value", df, 0)

    # Parameter Table designed to change the following values with sector group. But every group value is currently the same
    # Using group S for now, but choice of group is irrelevant
    mcap_a_val = utils.look_up("FreqSa", "ParameterName", "Value", df, 0)
    mcap_b_val = utils.look_up("FreqSb", "ParameterName", "Value", df, 0)

    mcap_factor_sca = (
        (1 - math.exp( - mcap_a_val * pow(np.log(mcap_used) - mcap_b_val, 2))) / 
        (1 - math.exp( - mcap_a_val * pow(np.log(mcap_base) - mcap_b_val, 2)))
    )
    return mcap_factor_sca


def calc_freq_sca(sector_ids, blended, sector_wghts, overrides, variables):
    """
    Calculates SCA frequency
    The frequency is built up using the following naming conventions:
    1) Base: sector frequency from reference table
    2) Mcap: adjusted for market cap
    3) Pre CapIQ: adjusted for ipo lag
    4) Unity: adjusted for CapIQ factors
    5) Unadj: adjusted for sector overrides (called "Sector" in excel tool but renamed here to avoid confusion with individual sector frequencies)
    6) Model: adjusted for subjective modifiers
    7) Used (or just "freq"): adjusted for total SCA override
    """
        
    variables = calc_unity_freq_sca(sector_ids, blended, sector_wghts, variables)
    variables = calc_unadj_freq_sca(sector_ids, blended, sector_wghts, overrides, variables)
    variables = calc_model_freq_sca(sector_ids, blended, sector_wghts, variables)

    # Override applies to the total SCA frequency
    # Adjusts the individual frequencies by the same amount to each this total
    variables["freq_sca"] = 0

    if variables["sca_override"] is not None:
        wgt = utils.ratio(
            min(variables["sca_override"], variables["mcap_freq_cap"]), 
            variables["freq_model_sca"],
            0
        )
    else: 
        wgt = 1

    for i, sector in enumerate(sector_ids):
        if (not blended) and (i > 0):
            break
        
        if sector_wghts[i] > 0 and sector is not None:
            variables[f"freq_sca_{i + 1}"] = variables[f"freq_model_sca_{i + 1}"] * wgt
            variables["freq_sca"] += variables[f"freq_sca_{i + 1}"] * sector_wghts[i]

    return variables


def calc_unity_freq_sca(sector_ids, blended, sector_wghts, variables):
    """
    Calculates SCA unity frequency
    I.e. frequency before UW factors (overrides and subjective factors)
    """
    # Setting default to build up with each sector
    variables["freq_mcap_sca"] = 0
    variables["freq_base_sca"] = 0
    variables["freq_pre_capiq_sca"] = 0
    variables["freq_unity_sca"] = 0

    df_ipo = hx.params.ref_ipo_lag

    for i, sector in enumerate(sector_ids):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break
        
        if sector_wghts[i] > 0 and sector is not None:
            # Mcap frequency
            variables[f"freq_mcap_{i + 1}"] = variables[f"freq_base_sca_{i + 1}"] * variables["mcap_factor_sca"]
            variables[f"freq_mcap_{i + 1}"] = max(variables[f"freq_mcap_{i + 1}"], min(variables[f"freq_base_sca_{i + 1}"], variables["mcap_freq_min"]))
            variables["freq_mcap_sca"] += variables[f"freq_mcap_{i + 1}"] * sector_wghts[i]

            # IPO factor
            ipo_sector = 1 if sector == 1 else 0
            variables["ipo_factor"] = (
                utils.look_up_condition(
                    (df_ipo["Lag"] == variables["ipo_lag"]) & (df_ipo["Sector"] == ipo_sector),
                    "Factor",
                    df_ipo,
                    0
                ) * variables[f"ipo_factor_{i + 1}"]
            )

            # Domicile factor
            domicle_factor = variables["canada_factor"] if variables["country"] == "Canada" else 1
 
            # Update variables
            variables[f"freq_pre_capiq_sca_{i + 1}"] = variables["ipo_factor"] * domicle_factor * variables[f"freq_mcap_{i + 1}"]
            variables[f"freq_unity_sca_{i + 1}"] = min(variables["mcap_freq_cap"], variables[f"freq_pre_capiq_sca_{i + 1}"] * variables["capiq_factor"])
    
            # Sum product of frequencies and blend weights
            variables["freq_base_sca"] += variables[f"freq_base_sca_{i + 1}"] * sector_wghts[i]
            variables["freq_pre_capiq_sca"] += variables[f"freq_pre_capiq_sca_{i + 1}"] * sector_wghts[i]
            variables["freq_unity_sca"] += variables[f"freq_unity_sca_{i + 1}"] * sector_wghts[i]
                
    return variables


def calc_unadj_freq_sca(sector_ids, blended, sector_wghts, overrides, variables):
    """
    Calculates SCA frequency after overrides but before subjective modifiers
    """
    # Setting default to build up with each sector
    variables["freq_unadj_sca"] = 0

    for i, sector in enumerate(sector_ids):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break
        
        if sector_wghts[i] > 0 and sector is not None:

            if overrides[i] is not None:
                variables[f"freq_unadj_sca_{i + 1}"] = min(variables["mcap_freq_cap"], overrides[i])
                
                # Variable to use for TPI calc screen
                variables[f"string_freq_override_{i + 1}"] = "Sector " + str(i + 1) + " Override: " + str(format(overrides[i], ".1%")) + "\n"
            else: 
                variables[f"string_freq_override_{i + 1}"] = ""
                variables[f"freq_unadj_sca_{i + 1}"] = variables[f"freq_unity_sca_{i + 1}"]
            
            # Sum product of frequencies and blend weights
            variables[f"freq_unadj_sca"] += variables[f"freq_unadj_sca_{i + 1}"] * sector_wghts[i]

    return variables


def calc_model_freq_sca(sector_ids, blended, sector_wghts, variables):
    """
    Calculates the "model" SCA frequency
    This is the frequency after subjective modifiers and before the total SCA override
    """
    # Setting default to build up with each sector
    variables["freq_model_sca"] = 0

    for i, sector in enumerate(sector_ids):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break

        if (sector is not None) and (sector_wghts[i] > 0):
            variables[f"freq_model_sca_{i + 1}"] = min(variables["mcap_freq_cap"], variables["mod_sca"] * variables[f"freq_unadj_sca_{i + 1}"])
            
            # Sum product of frequencies and blend weights
            variables["freq_model_sca"] += variables[f"freq_model_sca_{i + 1}"] * sector_wghts[i]

    return variables


def calc_freq_der(sector_ids, blended, sector_wghts, variables):
    """
    Calculates derivative frequency
    The frequency is built up using similar naming conventions to SCA but with less steps
    Also the frequencies interact with the SCA frequencies
    1) Unity: SCA base frequency adjusted for market cap and scale factor. Interacts with SCA unity freq 
    2) Unadj: unity freq interacted with SCA sector freq (called "Sector" in excel tool but renamed here to avoid confusion with individual sector frequencies)
    3) Model: adjusted for subjective modifiers. Interacts with SCA model freq
    4) Used (or just "freq"): model freq interacted with SCA used freq
    """
    # Setting defaults to build up with each sector
    variables["freq_unity_der"] = 0
    variables["freq_unadj_der"] = 0
    variables["freq_model_der"] = 0
    variables["freq_der"] = 0

    for i, sector in enumerate(sector_ids):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break

        if (sector is not None) and (sector_wghts[i] > 0):
            variables[f"sector_freq_unadj_der_{i + 1}"] = variables[f"freq_base_sca_{i + 1}"] * variables["mcap_factor_der"]  * variables["scale_factor_der"] 
            variables[f"sector_freq_der_{i + 1}"] = variables[f"sector_freq_unadj_der_{i + 1}"] * variables["mod_der"]
            variables[f"freq_unity_der_{i + 1}"] = min(max(variables[f"sector_freq_unadj_der_{i + 1}"] - variables[f"freq_unity_sca_{i + 1}"] * variables["inter_sca_der"], 0), variables["freq_cap_der"])
            variables[f"freq_unadj_der_{i + 1}"] = min(max(variables[f"sector_freq_unadj_der_{i + 1}"] - variables[f"freq_unadj_sca_{i + 1}"] * variables["inter_sca_der"], 0), variables["freq_cap_der"])
            variables[f"freq_model_der_{i + 1}"] = min(max(variables[f"sector_freq_der_{i + 1}"] - variables[f"freq_model_sca_{i + 1}"] * variables["inter_sca_der"], 0), variables["freq_cap_der"])
            variables[f"freq_der_{i + 1}"] = min(max(variables[f"sector_freq_der_{i + 1}"] - variables[f"freq_sca_{i + 1}"] * variables["inter_sca_der"], 0), variables["freq_cap_der"])

            # Sum product of frequencies and blend weights
            variables[f"freq_unity_der"] += variables[f"freq_unity_der_{i + 1}"] * sector_wghts[i]
            variables[f"freq_unadj_der"] += variables[f"freq_unadj_der_{i + 1}"] * sector_wghts[i]
            variables[f"freq_model_der"] += variables[f"freq_model_der_{i + 1}"] * sector_wghts[i]
            variables[f"freq_der"] += variables[f"freq_der_{i + 1}"] * sector_wghts[i]
        
    return variables


def calc_freq_ma(sectors, blended, sector_wghts, variables):
    """
    Calculates M&A frequency from M&A, SCA and Derivative factors defined in other functions
    Defines unity, unadj and used frequencies but these are the same
    """
    df_base_freq = hx.params.ref_base_frequencies
    
    # Setting defaults to build up with each sector
    variables["freq_unity_ma"] = 0
    variables["freq_ma"] = 0

    for i, sector in enumerate(sectors):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break

        if (sector is not None) and (sector_wghts[i] > 0):
            variables[f"sector_factor_ma_{i + 1}"] = utils.look_up(sectors[i], "Sector_Desc", "M&A Sector factor", df_base_freq, 0)
            variables[f"sector_freq_unadj_der_{i + 1}"] = variables[f"freq_base_sca_{i + 1}"] * variables["mcap_factor_der"]  * variables["scale_factor_der"] 
            variables[f"freq_unity_ma_{i + 1}"] = variables[f"sector_factor_ma_{i + 1}"] * variables["mcap_factor_ma"] * variables["scale_factor_ma"]
            variables[f"freq_ma_{i + 1}"] = variables[f"freq_unity_ma_{i + 1}"]

            variables["freq_unity_ma"] += variables[f"freq_unity_ma_{i + 1}"] * sector_wghts[i]
            variables["freq_ma"] += variables[f"freq_ma_{i + 1}"] * sector_wghts[i]

    variables["freq_unadj_ma"] = variables["freq_unity_ma"]
    variables["freq_model_ma"] = variables["freq_unity_ma"]
        
    return variables


def calc_freq_inter(sector_ids, blended, sector_wghts, variables):
    """
    Calculates the interaction claims types:
    1) Standalone SCA (s) 
    2) Standalone Derivative (d) 
    3) SCAs that become Derivatives (sd)
    Carried out for the frequency types (unity, unadj, model, used)
    """
    # Loop through each of the frequency types to be calculated
    for freq in (["unity_", "unadj_", "model_", ""]):
        # Setting defaults for each frequency type to build up with each sector
        variables[f"freq_{freq}s"] = 0
        variables[f"freq_{freq}sd"] = 0
        variables[f"freq_{freq}d"] = 0

        for i, sector in enumerate(sector_ids):
            # Loops through all sectors where the weight is greater than 0
            # Ignores sectors later than the first if "blended" not selected
            if (not blended) and (i > 0):
                break

            if (sector is not None) and (sector_wghts[i] > 0):
                variables[f"freq_{freq}s_{i + 1}"] = variables[f"freq_{freq}sca_{i + 1}"] * (1 - variables["inter_sca_der"])
                variables[f"freq_{freq}s"] += variables[f"freq_{freq}s_{i + 1}"] * sector_wghts[i]

                variables[f"freq_{freq}sd_{i + 1}"] = variables[f"freq_{freq}sca_{i + 1}"] * variables["inter_sca_der"]
                variables[f"freq_{freq}sd"] += variables[f"freq_{freq}sd_{i + 1}"] * sector_wghts[i]

        # Already allowed for the interactions when calculating the derivative frequency
        variables[f"freq_{freq}d"] = variables[f"freq_{freq}der"] 

    return variables


def calc_dismissal_freq(sector_ids, blended, sector_wghts, variables):
    """
    Calculates frequencies adjusted for the dismissal rates
    """
    # Loop through each of the frequency types to be calculated
    for freq in (["unity_", "unadj_", "model_", ""]): 
        # Setting defaults to build up with each sector
        variables[f"freq_{freq}sca_dismissed"] = 0
        variables[f"freq_{freq}s_dismissed"] = 0
        variables[f"freq_{freq}sd_dismissed"] = 0

        for i, sector in enumerate(sector_ids):
            # Loops through all sectors where the weight is greater than 0
            # Ignores sectors later than the first if "blended" not selected
            if (not blended) and (i > 0):
                break

            if (sector is not None) & (sector_wghts[i] > 0):
                variables[f"freq_{freq}sca_dismissed"] += variables[f"freq_{freq}sca_{i + 1}"] * variables[f"dr_sca_{i + 1}"] * sector_wghts[i]
                variables[f"freq_{freq}s_dismissed"] += variables[f"freq_{freq}s_{i + 1}"] * variables[f"dr_sca_{i + 1}"] * sector_wghts[i]
                variables[f"freq_{freq}sd_dismissed"] += variables[f"freq_{freq}sd_{i + 1}"] * variables[f"dr_sca_{i + 1}"] * sector_wghts[i]

        variables[f"freq_{freq}final_sca"] = variables[f"freq_{freq}sca"] - variables[f"freq_{freq}sca_dismissed"]
        variables[f"freq_{freq}final_s"] = variables[f"freq_{freq}s"] - variables[f"freq_{freq}s_dismissed"]
        variables[f"freq_{freq}final_sd"] = variables[f"freq_{freq}sd"] - variables[f"freq_{freq}sd_dismissed"]

        variables[f"freq_{freq}d_dismissed"] = variables[f"freq_{freq}d"] * variables["dr_der"]
        variables[f"freq_{freq}final_d"] = variables[f"freq_{freq}d"] - variables[f"freq_{freq}d_dismissed"] 

        variables[f"freq_{freq}ma_dismissed"] = variables[f"freq_{freq}ma"] * variables["dr_ma"]
        variables[f"freq_{freq}final_ma"] = variables[f"freq_{freq}ma"] - variables[f"freq_{freq}ma_dismissed"]    
        
    return variables


def set_frequencies(sectors, sector_wghts, blended, freq_path, ind_path, variables):
    """
    Sets the frequencies in the hxd
    Includes the industry path as sector level unity frequencies need to be saved
    """
    ind_path.sector_unity_frequency = variables["freq_unity_sca_1"] if sector_wghts[0] > 0 and sectors[0] is not None else None
    if blended:
        if (sectors[1] is not None) and (sector_wghts[1] > 0):
            ind_path.sector_unity_frequency_2 = variables["freq_unity_sca_2"]
        if (sectors[2] is not None) and (sector_wghts[2] > 0):
            ind_path.sector_unity_frequency_3 = variables["freq_unity_sca_3"]

    # Unity
    freq_path.sd_unity_freq = variables["freq_unity_sd"]
    freq_path.s_unity_freq = variables["freq_unity_s"]
    freq_path.sca_unity_freq = variables["freq_unity_sca"]
    freq_path.d_unity_freq = variables["freq_unity_d"]
    freq_path.ma_unity_freq = variables["freq_unity_ma"]

    # Sector
    freq_path.sd_sector_freq = variables["freq_unadj_sd"]
    freq_path.s_sector_freq = variables["freq_unadj_s"]
    freq_path.sca_sector_freq = variables["freq_unadj_sca"]
    freq_path.d_sector_freq = variables["freq_unadj_d"]
    freq_path.ma_sector_freq = variables["freq_unadj_ma"]

    # Model
    freq_path.sd_model_freq = variables["freq_model_sd"]
    freq_path.s_model_freq = variables["freq_model_s"]
    freq_path.sca_model_freq = variables["freq_model_sca"]
    freq_path.d_model_freq = variables["freq_model_d"]
    freq_path.ma_model_freq = variables["freq_model_ma"]

    # Used
    freq_path.sd_model_freq = variables["freq_sd"]
    freq_path.s_model_freq = variables["freq_s"]
    freq_path.sca_used_freq = variables["freq_sca"]
    freq_path.d_used_freq = variables["freq_d"]
    freq_path.ma_used_freq = variables["freq_ma"]


    # Only shown for used frequency as it has no impact on price and is only for display
    freq_path.total_freq = (
        variables["freq_sca"] +
        variables["freq_d"] +
        variables["freq_ma"]
    )


####################################################################################################################
################################################ Severity Functions ################################################
####################################################################################################################


def process_sev(hxd, mcap, variables):
    """
    Calculates the mean and sigma parameters for the various claim types
    """
    # Initial mu
    df_sca_sev_mod = hx.params.ref_sca_severity_modifiers
    variables["initial_mu"] = calc_initial_mu(df_sca_sev_mod, mcap)

    # Adj mcap mu
    df_mcap_mod = hx.params.ref_mcap_factor
    #variables["mu_mcap_load"] = calc_mu_mcap_load(df_mcap_mod, variables["mcap"])
    #variables["mcap_adj_mu"] = variables["initial_mu"] * variables["mu_mcap_load"]   
    # TODO: Revert or uncomment above line once change is finalised
    variables["mcap_adj_mu"] = variables["initial_mu"]

    # SCA sigma
    variables["sigma_sca"] = calc_sigma_sca(df_sca_sev_mod, mcap)
 
    # Derivative sigma
    df_der_sev_mod = hx.params.ref_derivative_sev_modifiers
    variables["sigma_der"] = utils.look_up("sdlog", "ParameterName", "Value", df_der_sev_mod, 0)

    # M&A sigma
    df_ma_sev_mod = hx.params.ref_ma_sev_modifiers
    variables["sigma_ma"] = calc_sigma_ma(df_ma_sev_mod, mcap)

    # Defense costs factor
    df_sca_def_costs = hx.params.ref_sca_defense_costs
    variables["defense_sca_factor"] = calc_defense_sca_factor(df_sca_def_costs, variables["mcap_adj_mu"], variables["sigma_sca"])

    # SCA claim types' mu
    df_interactions = hx.params.ref_interaction_modifiers
    sd_load = utils.look_up("SDLoad", "ParameterName", "Value", df_interactions, 1)
    variables["mu_sca"] = variables["mcap_adj_mu"] + np.log(1 + variables["defense_sca_factor"])
    variables["mu_sd"] = variables["mu_sca"] + np.log(sd_load)

    # Standalone derivative
    variables["initial_mu_der"] = utils.look_up("mulog", "ParameterName", "Value", df_der_sev_mod, 0) 
    variables["mu_der"] = variables["initial_mu_der"] + np.log(1 + variables["defense_sca_factor"])

    # M&A mu
    variables["mu_ma"] = calc_mu_ma(df_ma_sev_mod, mcap, variables["defense_sca_factor"])

    # Defence dismissed sigma      
    variables["sigma_def_dis"] = utils.look_up("DefenseDismissalSCA_si", "ParameterName", "Value", df_sca_sev_mod, 0)
                
    # Expected defence costs if dismissed
    df_sca_dis_costs = hx.params.ref_sca_dismissed_costs
    variables["mean_def_dis"] = calc_mean_def_dis(df_sca_dis_costs, mcap)
            
    variables["mu_def_dis"] = np.log(variables["mean_def_dis"]) - 0.5 * pow(variables["sigma_def_dis"], 2) 

    # 75th percentile
    if hxd.cds.is_side_a:
        df_plaintiff_fees = hx.params.ref_plaintiff_fees
        variables["plaintiff_fees"] = calc_plaintiff_fees(df_plaintiff_fees, mcap)
    else:
        variables["plaintiff_fees"] = 0

    variables["at_cost_75"] = (
        np.exp(norm.ppf(0.75, variables["mcap_adj_mu"] + np.log(1 + variables["defense_sca_factor"]), variables["sigma_sca"])) + 
        variables["plaintiff_fees"]
    )  

    variables["adj_rate_75"] = max(0, (0.75 - variables["dr_sca_1"]) / (1 - variables["dr_sca_1"]))

    variables["incl_dimissals_75"] = (
        np.exp(norm.ppf(variables["adj_rate_75"], variables["mcap_adj_mu"] + np.log(1 + variables["defense_sca_factor"]), variables["sigma_sca"])) + 
        variables["plaintiff_fees"]
    )  

    # Setting TPI Calculation and comment fields
    set_tpi_calcs_sev(hxd.cds.tpi_calculations, variables)

    return variables
       

def calc_initial_mu(df, mcap):
    """
    Calcultes the initial mu for each claim type
    Accepts a ref table but column names are set
    """
    sev_a = utils.look_up("a", "ParameterName", "Value", df, 0)
    sev_b = utils.look_up("b", "ParameterName","Value", df, 0)
    sev_c = utils.look_up("c", "ParameterName", "Value", df, 0)
    # Calculates the initial mu value before loading for claim type
    mu = (
        sev_a * pow(np.log(mcap), 2) + 
        sev_b * np.log(mcap) + 
        sev_c
        )

    return mu

def calc_mu_mcap_load(df, mcap):
    """
    Calcuates a factor based on market cap to be applied to the initial mu in the severity curve
    Interpolates the parameter table using geometric interpolation
    """
    if mcap < max(df["Mcap Lower"]): 
        # Pull upper and lower values from table for interpolation
        df_row = df[(df["Mcap Lower"] <= mcap) & (df["Mcap Upper"] > mcap)].iloc[0]

        if df_row["Factor Upper"] == df_row["Factor Lower"]:
            factor = df_row["Factor Lower"]
        else:
            # Geometric interpolation
            factor = df_row["Factor Lower"] + (df_row["Factor Upper"] - df_row["Factor Lower"]) * np.log(mcap / df_row["Mcap Lower"]) / np.log(df_row["Mcap Upper"] / df_row["Mcap Lower"])
    else: 
        factor = df["Factor Upper"].iloc[-1]

    return factor

def calc_sigma_sca(df, mcap):
    """
    Calcultes the sigma for SCA claims
    Accepts a ref table but column names are set
    """
   # Always one value but the below functionaility is built to potentially change with market cap in the future
    mc_1 = utils.look_up("MC1", "ParameterName", "Value", df, 0)
    mc_2 = utils.look_up("MC2", "ParameterName", "Value", df, 0)

    if mcap < mc_1:
        sd_lookup = "sd_1"
    elif mcap < mc_2:
        sd_lookup = "sd_2"
    else: 
        sd_lookup = "sd_3"

    sigma_sca = utils.look_up(sd_lookup, "ParameterName", "Value", df, 0)

    return sigma_sca  

def calc_sigma_ma(df, mcap):
    ma_mc = utils.look_up("MASE.MC", "ParameterName", "Value", df, 0) 
    ma_sd_a = utils.look_up("MASE.sd_a", "ParameterName", "Value", df, 0) 
    ma_sd_b1 = utils.look_up("MASE.sd_b1", "ParameterName", "Value", df, 0) 
    ma_sd_b2 = utils.look_up("MASE.sd_b2", "ParameterName", "Value", df, 0) 

    if mcap < ma_mc:
        sigma_ma = ma_sd_b1
    else:
        sigma_ma = ma_sd_b2 + ma_sd_a * np.log(mcap)

    return sigma_ma

def calc_defense_sca_factor(df, mu, sigma):
    dc_mean = math.exp(mu + 0.5 * pow(sigma , 2))
    dc_indemnity_lower = utils.look_up_with_bounds(dc_mean, "Indemnity Lower", "Indemnity Upper", "Indemnity Lower", df, 0)
    dc_factor = utils.look_up_with_bounds(dc_mean, "Indemnity Lower", "Indemnity Upper", "Factor", df,0)
    dc_cumf = utils.look_up_with_bounds(dc_mean, "Indemnity Lower", "Indemnity Upper", "CumF", df,0)
    defense_sca_factor = ((dc_mean - dc_indemnity_lower) * dc_factor + dc_indemnity_lower * dc_cumf) / dc_mean

    return defense_sca_factor

def calc_mu_ma(df, mcap, defense_sca_factor):
    mu_ma_a = utils.look_up("MASE.alpha", "ParameterName", "Value", df, 0) 
    mu_ma_b = utils.look_up("MASE.beta", "ParameterName", "Value", df, 0) 
    ma_initial_mu = mu_ma_a + mu_ma_b  * np.log(mcap)

    mu_ma = ma_initial_mu + np.log(1 + defense_sca_factor)

    return mu_ma

def calc_mean_def_dis(df, mcap):
    df_row = (
        df[(df["MarketCap Lower"] <= mcap) & 
        (df["MarketCap Upper"] > mcap)].iloc[0]
    )
    mean_def_dis = (
        df_row["Cost Lower"] +  
        (df_row["Cost Upper"] - df_row["Cost Lower"])*
        np.log(mcap / df_row["MarketCap Lower"]) / np.log(df_row["MarketCap Upper"] / df_row["MarketCap Lower"])
    )  

    return mean_def_dis  


def calc_plaintiff_fees(df, mcap):
    """
    # Calculates the plaintiff fees that get added to the 75th cost for Side A business
    """

    x1 = min(df["MarketCap"])
    x2 = max(df["MarketCap"])
    y1 = min(df["Cost"])
    y2 = max(df["Cost"])

    xp = [x1, x2]
    fp = [y1, y2]        
    plaintiff_fees = np.interp(mcap, xp, fp)   

    return plaintiff_fees

##################################################################################################################
################################################ Sida A Functions ################################################
##################################################################################################################


def calc_side_a_factors(hxd, variables):
    """
    Calculates all the additional factors that only apply for Side A. Includes:
    1) Extracts variables to calculte the DIC adjustment at a layer level
    2) Calculates the average bankruptcy load using the Z-score and Credit Score
    """

    agg = hxd.cds.exposure.aggregate

    # Defining parameter tables
    df_dic_adj = hx.params.ref_dic_adjustment
    df_side_a_mod = hx.params.ref_side_a_modifiers
    df_bankruptcy = hx.params.ref_side_a_bankruptcy

    # Setting default values
    variables["bankruptcy_load"] = 1
    variables["dic_adjustment"] = 1

    # Extracts DIC adjustment factors that will be used for each layer
    variables["prim_standalone"] = utils.look_up("Primary Standalone", "ParameterName", "Value", df_dic_adj, 0)
    variables["side_a_xs_abc"] = utils.look_up("Side A xs ABC", "ParameterName", "Value", df_dic_adj, 0)
    variables["side_a_xs_side_a"] = utils.look_up("Side A xs Side A", "ParameterName", "Value", df_dic_adj, 0)

    # The following financials are required
    financials = {
        "ebit": agg.ebit if agg.ebit is not None else 0,
        "period": agg.period if agg.period is not None else 0,
        "current_assets": agg.current_assets if agg.current_assets is not None else 0,
        "current_liabilities": agg.current_liabilities if agg.current_liabilities is not None else 0,
        "total_assets": agg.total_assets if agg.total_assets is not None else 0,
        "total_liabilities": agg.total_liabilities if agg.total_liabilities is not None else 0,
        "retained_earnings": agg.retained_earnings if agg.retained_earnings is not None else 0,
        "market_value_of_equity": agg.market_value_of_equity if agg.market_value_of_equity is not None else 0,
        "net_sales": agg.net_sales if agg.net_sales is not None else 0
    }

    variables["z_score"] = calc_z_score(df_side_a_mod, financials)
    agg.z_score = variables["z_score"]

    # Z bankruptcy score
    variables["z_bankruptcy_score"] = calc_z_bankruptcy_score(df_side_a_mod, variables["z_score"])
    agg.bankruptcy_score = variables["z_bankruptcy_score"]

    # Average bankruptcy score 
    # This is the average of z bankruptcy score and credit score
    variables["average_bankruptcy_score"] = calc_average_bankruptcy_score(df_bankruptcy, agg.credit_rating, variables["z_bankruptcy_score"])
    agg.average_bankruptcy_score = variables["average_bankruptcy_score"]
    
    # Bankruptcy load
    #bankruptcy_load = utils.look_up_condition((df_bankruptcy["BankruptcyScore"] <= bankruptcy_score), "Load", df_bankruptcy, 1)
    if variables["average_bankruptcy_score"] is not None and variables["average_bankruptcy_score"] >= df_bankruptcy["BankruptcyScore"].min():
        variables["bankruptcy_load"] = df_bankruptcy[df_bankruptcy["BankruptcyScore"] <= variables["average_bankruptcy_score"]]["Load"].max()

    return variables


def calc_z_score(df, financials):
    """
    Calculates the Z score from the company financials
    """

    z_a = utils.ratio((financials["current_assets"] - financials["current_liabilities"]), financials["total_assets"], 0)
    z_b = utils.ratio(financials["retained_earnings"], financials["total_assets"], 0)
    z_c = utils.ratio(utils.ratio(financials["ebit"], financials["total_assets"], 0) * 12, financials["period"], 0)
    z_d = utils.ratio(financials["market_value_of_equity"], financials["total_liabilities"], 0)
    z_e = utils.ratio(utils.ratio(financials["net_sales"], financials["total_assets"], 0) * 12 ,financials["period"], 0)

    z_wgt_a = utils.look_up("Z_T1", "ParameterName", "Value", df, 0) 
    z_wgt_b = utils.look_up("Z_T2", "ParameterName", "Value", df, 0) 
    z_wgt_c = utils.look_up("Z_T3", "ParameterName", "Value", df, 0) 
    z_wgt_d = utils.look_up("Z_T4", "ParameterName", "Value", df, 0) 
    z_wgt_e = utils.look_up("Z_T5", "ParameterName", "Value", df, 0)

    z_score = (
        z_a * z_wgt_a +
        z_b * z_wgt_b +
        z_c * z_wgt_c +
        z_d * z_wgt_d +
        z_e * z_wgt_e
    )

    return z_score


def calc_z_bankruptcy_score(df, z_score):
    """
    Accepts a z score and converts this into a bankruptcy score
    """
    z_base = utils.look_up("Z_BaseConstant", "ParameterName", "Value", df, 0)
    z_lambda = utils.look_up("Z_BaseLambda", "ParameterName", "Value", df, 0)
    z_max = utils.look_up("Z_Max", "ParameterName", "Value", df, 0)

    z_bankruptcy_score = min(z_base * math.exp(z_lambda * z_score), z_max)

    return z_bankruptcy_score


def calc_average_bankruptcy_score(df, credit_rating, z_bankruptcy_score):
    if credit_rating is not None:
        credit_score = utils.look_up(credit_rating, "Bankruptcy Rating", "BankruptcyScore", df, 0)
        bankruptcy_score = (z_bankruptcy_score + credit_score) / 2
    else: bankruptcy_score = z_bankruptcy_score

    return bankruptcy_score

 
#######################################################################################################################
################################################ TPI Metrics Functions ################################################
#######################################################################################################################


def process_tpi_metrics(hxd, is_side_a, variables):
    """
    Calculate the metrics used to calculate the TPI
    Also sets the book averages for the TPI calculation sheet
    """
    import algorithms.rate_utilities as utils
    
    ## Non modelled lossses
    variables = calc_non_modelled_load(is_side_a, variables)

    ## Plan metrics
    # Excel reference table
    df_tpi_params = hx.params.ref_tpi_params
    # Central parameter table
    #df_tpi_params = params.tp_parameters.df()

    # This is a global parameter that needs updating each year
    # Currently held in the constants file
    ###DJ: plan_year = const.plan_year

    # Calculates the plan year based on the inception date
    plan_year = utils.calc_tp_year(hxd)

    # Saves UW location as a variables, which impacts the plan metrics
    variables["uw_location"] = hxd.cds.uw_location 

    variables = calc_plan_metrics(df_tpi_params, variables["uw_location"], plan_year, variables)

    # Sets the book averages in the TPI Calculation sheet
    df_book_averages = hx.params.ref_book_averages
    set_tpi_calcs_book_averages(hxd.cds.tpi_calculations, df_book_averages, is_side_a, variables)

    return variables


def calc_non_modelled_load(is_side_a, variables):
    """
    Calculates the non-modelled loading for the coverage
    This is an uplift to the expected loss to allow for losses not in the dataset used to parameterise the model
    """
    # Placeholder as we review the ELR method
    elr = const.elr
    
    # Defining parameter tables
    df_dic_adj = hx.params.ref_dic_adjustment
    df_side_a_mod = hx.params.ref_side_a_modifiers
    df_sca_sev_mod = hx.params.ref_sca_severity_modifiers
    #df_mcap_mod = hx.params.ref_mcap_catload_factor
    # TODO: Remove all commented mcap adjustment lines once 2025 recalibration method agreed

    if is_side_a:
        # Pulls the Side A Cat Load to be used for each layer later
        experience_lr = utils.look_up("Experience LR", "ParameterName", "Value", df_dic_adj, 0)
        additional_cat = utils.look_up("Additional Cat Load", "ParameterName", "Value", df_dic_adj, 0)
        side_a_cat = utils.look_up("SideACatLoad", "ParameterName", "Value", df_side_a_mod, 0) 
        #variables["mcap_adj_cat_load"] = calc_mcap_non_modelled_load(df_mcap_mod, variables["mcap"], side_a_cat, elr)

        #variables["non_modelled_load"] = (variables["mcap_adj_cat_load"] + additional_cat) / experience_lr
        variables["non_modelled_load"] = (side_a_cat + additional_cat) / experience_lr

        variables["side_a_scale"] = experience_lr / elr
    else: 
        # Pulls the ABC Cat Load to be used for each layer later
        abc_cat_load = utils.look_up("ABCCatLoad", "ParameterName", "Value", df_sca_sev_mod, 0)
        #variables["mcap_adj_cat_load"] = calc_mcap_non_modelled_load(df_mcap_mod, variables["mcap"], abc_cat_load, elr)
        #variables["non_modelled_load"] = variables["mcap_adj_cat_load"] / elr
        variables["non_modelled_load"] = abc_cat_load / elr

    return variables

def calc_mcap_non_modelled_load(df, mcap, load, elr):
    """
    Pulls the loading by market cap from a parameter table
    Uses geometric interpolation to calculate the loading for market caps between ranges
    Calculates the required loading to the non-modelled claim type load that will achieve the increase by market cap
    """
    if mcap < max(df["Mcap Lower"]): 
        # Pull upper and lower values from table for interpolation
        df_row = df[(df["Mcap Lower"] <= mcap) & (df["Mcap Upper"] > mcap)].iloc[0]

        if df_row["Factor Upper"] == df_row["Factor Lower"]:
            factor = df_row["Factor Lower"]
        else:
            # Geometric interpolation
            factor = df_row["Factor Lower"] + (df_row["Factor Upper"] - df_row["Factor Lower"]) * np.log(mcap / df_row["Mcap Lower"]) / np.log(df_row["Mcap Upper"] / df_row["Mcap Lower"])
    else: 
        factor = df["Factor Upper"].iloc[-1]

    # Following formula ensures that the total loss cost equals the original loss cost multiplied by the factor
    mcap_adj_cat_load = factor * (load + elr) - elr

    return mcap_adj_cat_load


def calc_plan_metrics(df, uw_location, year, variables):
    """
    Produces the plan metrics for a given year and location
    """
    
    tp_params_df = params.tp_parameters.df()

    if uw_location == "UK":
        bp_class = "London D&O"
    else:
        bp_class = "US D&O"

    tp_params = tp_params_df[(tp_params_df['business_plan_class'] == bp_class) &
        ((tp_params_df['year'] == year))]

    # Using reference tables from excel tool (should be replaced by the central table)
    plan_metrics = df[(df["Year"] == year) & (df["Class"] == uw_location)].iloc[0]

    variables["ri_cost"] = tp_params['cost_of_ri'].iloc[0] - tp_params['ri_rec'].iloc[0]
    variables["inv_inc"] = tp_params['inv_inc'].iloc[0]
    variables["var_exp"] = tp_params["var_exp"].iloc[0] + plan_metrics["CHE Rate"]
    variables["capital_factor"] = plan_metrics["Scale Factor"] * tp_params["capital_req"].iloc[0]
    variables["fixed_exp"] = tp_params['fixed_exp'].iloc[0]
    variables["cat_load"] = plan_metrics["CAT Load"]



    ###DJ: variables["ri_cost"] = plan_metrics["Cost of RI"]
    ###DJ: variables["var_exp"] = plan_metrics["Variable Expenses"] + plan_metrics["CHE Rate"]
    ###DJ: variables["fixed_exp"] = plan_metrics["Fixed Expenses"]
    ###DJ: variables["inv_inc"] = plan_metrics["Invesment Income"]
    ###DJ: variables["capital_factor"] = plan_metrics["Scale Factor"] * plan_metrics["Captial Per GNP"]

    
    return variables

###################################################################################################################################
################################################ Layer Technical Premium Functions ################################################
###################################################################################################################################


def process_layers(hxd, is_side_a, variables):
    """
    Calculates all the outputs at a layer level (e.g., TPI, ROC, etc.)
    """
    # Defining parameter tables
    df_monitoring_mod = hx.params.ref_monitoring_modifiers
    df_side_a_mod = hx.params.ref_side_a_modifiers
    df_excess_load = hx.params.ref_excess_load

    # Sector blend inputs
    ind = hxd.cds.key_industry

    sector_wghts = [
        ind.sic_percentage if ind.sic_percentage else 0, 
        ind.sic_percentage_2 if (ind.sic_percentage_2) and (ind.blended_sic) else 0, 
        ind.sic_percentage_3 if (ind.sic_percentage_3) and (ind.blended_sic) else 0
        ]
    sector_ids = [ind.sector_id, ind.sector_id_2, ind.sector_id_3]

    # Pro rata factor
    if (hxd.hx_core.inception_date is not None) and (hxd.hx_core.expiry_date is not None):
        # Method 2 replicates excel function YEARFRAC with basis 0
        if hxd.cds.is_runoff:
            variables["pro_rata"] = 1
        else:
            variables["pro_rata"] = calc_pro_rata(hxd.hx_core.inception_date, hxd.hx_core.expiry_date, 2) 

    # List to loop over
    layers = hxd.cds.layers

    # # Used to show the selected layer in the TPI calcs
    # layer_number = 1

    for idx, layer in enumerate(layers):
        #### Setup ####
        # Sets the path to the relevant coverage
        cov = layer.coverages.side_a if is_side_a else layer.coverages.abc
            
        # Display tech premium for each option at top of screen
        if idx < const.max_layers:
            tech_path = f"show_tech_prem_{idx + 1}"
            setattr(hxd.cds, tech_path, True)
        
        # Setting the limit and excess fields depending on coverage
        variables["limit"] = cov.limit if cov.limit else 0
        variables["excess"] = cov.excess or 0
        variables["deductible"] = cov.deductible or 0
        variables["tower"] = layer.coverages.side_a.tower if is_side_a and layer.coverages.side_a.tower is not None else 0

        layer_fields = [
            variables["limit"], 
            variables["excess"], 
            variables["deductible"], 
            variables["tower"]
            ]

        if variables["limit"] > 0 and any(sector_id is not None for sector_id in sector_ids) and any(wght > 0 for wght in sector_wghts):
            if all(lf >= 0 for lf in layer_fields):
                #### Calculations ####
                # Show total excess ex deductible but include deductible for all calculations
                cov.total_excess = variables["excess"] + variables["tower"]

                # Layer fields that require inputs
                variables["total_excess"] = variables["excess"] + variables["deductible"] + variables["tower"]

                variables["ma_retention"] = layer.coverages.abc.ma_retention

                if is_side_a:
                    variables["total_excess_ma"] = variables["excess"]
                else:
                    if variables["ma_retention"] is not None:
                        variables["total_excess_ma"] = variables["excess"]  + variables["ma_retention"]
                    else:  variables["total_excess_ma"]  = variables["total_excess"]

                # Calculate the severity to the layer for each claim type
                variables = calc_layer_sev(df_monitoring_mod, is_side_a, variables)

                # Calculates the expected loss to the layer for each claim type
                variables = calc_expected_loss(sector_ids, sector_wghts, variables)
                # Adjusts the individual expected loss if side a
                if is_side_a: 
                    variables = calc_side_a_loss_adj(df_side_a_mod, variables)

                # Sum the individual losses 
                # Adjusts for non-modelled loss cost and side a factors
                variables = calc_total_el(is_side_a, variables)
                        
                # Calculates the outputs for each layer given the premium
                # is_runoff  - Update premium here 
                if hxd.cds.is_runoff:
                    variables["premium"] = (cov.premium / layer.runoff_adjustment) if (cov.premium / layer.runoff_adjustment) else 0              #layer.runoff_premium
                else:
                    variables["premium"] = cov.premium if cov.premium else 0

                if cov.brokerage is None:
                    hx.errors.validation("Brokerage is required for option "+ str(idx + 1))   

                variables["is_runoff"] = hxd.cds.is_runoff
                variables["runoff_adjustment"] = layer.runoff_adjustment
                variables["brokerage"] = cov.brokerage if cov.brokerage else 0
                variables["written_line"] = cov.written_line if cov.written_line else 0

                # Calculates benchmark premium
                # Happens before the below as we should show this before they enter a premium
                variables["benchmark_prem"] = variables["total_el"] / (0.7 * (1 - variables["brokerage"]))
                
                # if hxd.cds.is_runoff:
                #     variables["benchmark_prem"] /= (1 if layer.runoff_adjustment == 0 else layer.runoff_adjustment)

                cov.benchmark_premium = variables["benchmark_prem"]

                variables = calc_layer_tpi(df_excess_load, variables)
                
                # Updates layer fields in the Pricing sheet of the hxd
                set_layer_outputs(hxd, cov, layer, variables)

                hxd.cds.standard_fields.is_rater_priced = hxd.cds.review_type.rater_priced

                # Sets technical price at top of screen
                if idx < const.max_layers:
                    tech_path = f"technical_premium_{idx + 1}"
                    setattr(hxd.cds, tech_path, cov.technical_premium)

                # if variables["premium"] > 0:
                 #### Set TPI Calculation sheet ####
                calc = hxd.cds.tpi_calculations
        
                if idx + 1 == calc.selected_option:
                    # Unhides the relevant loss cost section
                    calc.is_abc = not is_side_a
                    calc.is_side_a = is_side_a
                    # Sets the fields and comments
                    set_tpi_calcs_loss_cost(calc, is_side_a, sector_ids, sector_wghts, variables)
                    set_tpi_calcs_outputs(calc, is_side_a, variables)

                    # Set Side A fields in the TPI calculations sheet. Includes:
                    #   1) Bankruptcy load
                    #   2) DIC Adjustment 
                    set_tpi_calcs_side_a_factors(hxd.cds.tpi_calculations, variables)          
            else:
                # Validation
                hx.errors.validation("Layer details cannot be < 0")   

        #### Model premium for admitted ####
        if hxd.cds.admitted_excess.is_primary_excess == "Excess":
            layer.model_premium = hxd.cds.admitted_excess.adm_exc_round_prem.value.selected
        elif hxd.cds.admitted_excess.is_primary_excess == "Primary":
            if hxd.cds.admitted.insurer == "BICI":
                layer.model_premium = hxd.cds.admitted.bici.rounded_premium.selected 
            elif hxd.cds.admitted.insurer == "BAIC":
                layer.model_premium = hxd.cds.admitted.baic.rounded_premium.selected 
        
        if layer.bpi is None:
            hx.errors.validation("Insufficient information entered to calculate a TPI for layer " + str(idx + 1))



def calc_layer_sev(df_monitoring_mod, is_side_a, variables):
    """
    Calculates the severity to the layer for each claim type
    The table column names for the two dataframe inputs are fixed
    """
    # SCA
    variables["sev_layer_s"] = truncated_lognormal(variables["mu_sca"], variables["sigma_sca"], variables["limit"], variables["total_excess"])
    variables["sev_layer_sd"] = truncated_lognormal(variables["mu_sd"], variables["sigma_sca"], variables["limit"], variables["total_excess"])

    # Derivative
    variables["sev_layer_d"] = truncated_lognormal(variables["mu_der"], variables["sigma_der"], variables["limit"], variables["total_excess"])

    # M&A
    variables["sev_layer_ma"] = truncated_lognormal(variables["mu_ma"], variables["sigma_ma"], variables["limit"], variables["total_excess_ma"])

    # Costs
    dismissal_rates = [variables["dr_sca_1"], variables["dr_sca_2"], variables["dr_sca_3"]]
    variables = calc_cost_severity(df_monitoring_mod, dismissal_rates, variables)

    return variables


def calc_expected_loss(sector_ids, sector_wghts, variables):
    """
    Calculates the expected loss to the layer for each claim type
    Multiplies the frequency and severity for each sector  + freq + 
    Blends the sectors by the sector weights
    """
    # Loop through each of the loss cost types to be calculated
    for freq in (["unity_", "unadj_", "model_", ""]): 
        # Setting defaults to build up with each sector
        variables["el_" + freq + "sca_monc"] = 0
        variables["el_" + freq + "def_dis"] = 0
        variables["el_" + freq + "der_monc"] = 0
        variables["el_" + freq + "def_dis"] = 0

        # Initial step of the derivative monitoring used in each sector
        el_der_monc = (1 - variables["freq_dr_der"]) * variables["der_monc"] + variables["freq_dr_der"] * variables["der_dis_monc"]

        for i, sector in enumerate(sector_ids):
            # Loops through all sectors where the weight is greater than 0
            # Ignores sectors later than the first if "blended" not selected
            if (not variables["blended"]) and (i > 0):
                break

            if (sector is not None) and (sector_wghts[i] > 0):
                ## Costs ##
                # SCA monitoring
                variables[f"el_{freq}sca_monc_{i + 1}"] = variables[f"sca_monc_{i + 1}"] * (variables[f"freq_{freq}s_{i + 1}"] + variables[f"freq_{freq}sd_{i + 1}"])
                variables[f"el_{freq}sca_monc"] += variables[f"el_{freq}sca_monc_{i + 1}"] * sector_wghts[i]
                # Derivative monitoring
                variables[f"el_{freq}der_monc_{i + 1}"] = el_der_monc * variables[f"freq_{freq}der_{i + 1}"]
                variables[f"el_{freq}der_monc"] += variables[f"el_{freq}der_monc_{i + 1}"] * sector_wghts[i] 
                # Defence dismissal
                variables[f"def_{freq}dis_{i + 1}"] = variables[f"dr_sca_{i + 1}"] * (variables[f"freq_{freq}s_{i + 1}"] + variables[f"freq_{freq}sd_{i + 1}"]) * variables["def_dis_factor"]
                variables[f"el_{freq}def_dis"] += variables[f"def_{freq}dis_{i + 1}"] * sector_wghts[i]

                ## Sector EL ##
                # Totals are calculated from single variables
                # These individual losses are needed for the TPI calculations
                # No need to calculate them for each of the frequency types (review this)
                # SCA
                variables[f"el_s_{i + 1}"] = variables["sev_layer_s"] * variables[f"freq_s_{i + 1}"] * (1 - variables[f"dr_sca_{i + 1}"])
                variables[f"el_sd_{i + 1}"] = variables["sev_layer_sd"] * variables[f"freq_sd_{i + 1}"] * (1 - variables[f"dr_sca_{i + 1}"])
                # Derivative
                variables[f"el_d_{i + 1}"] = variables["sev_layer_d"] * variables[f"freq_der_{i + 1}"] * (1 - variables["dr_der"])
                # M&A    
                variables[f"el_ma_{i + 1}"] = variables["sev_layer_ma"] * variables[f"freq_ma_{i + 1}"] * (1 - variables["dr_ma"])

        #### Adjusted for Pro Rata
        # Costs
        variables[f"el_{freq}sca_monc"] *= variables["pro_rata"]
        variables[f"el_{freq}der_monc"] *= variables["pro_rata"]
        variables[f"el_{freq}def_dis"] *= variables["pro_rata"]

        # SCA
        variables[f"el_{freq}s"] = variables[f"freq_{freq}final_s"] * variables["sev_layer_s"] * variables["pro_rata"]
        variables[f"el_{freq}sd"] = variables[f"freq_{freq}final_sd"] * variables["sev_layer_sd"] * variables["pro_rata"]

        # Derivative
        variables[f"el_{freq}d"] = variables[f"freq_{freq}final_d"] * variables["sev_layer_d"] * variables["pro_rata"]

        # M&A
        variables[f"el_{freq}ma"] = variables[f"freq_{freq}final_ma"] * variables["sev_layer_ma"] * variables["pro_rata"]
    
    return variables               


def calc_side_a_loss_adj(df, variables):
    """
    Adjusts the expected loss for side a policies
    """
    variables["side_a_adj_s"] = utils.look_up("s_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_sd"] = utils.look_up("sd_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_d"] = utils.look_up("d_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_ma"] = utils.look_up("ma_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_def_dis"] = utils.look_up("def_dis_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_sca_monc"] = utils.look_up("sca_monc_adjustment", "ParameterName", "Value", df, 0)
    variables["side_a_adj_der_monc"] = utils.look_up("der_monc_adjustment", "ParameterName", "Value", df, 0)

    # Loop through each of the loss cost types to be adjusted
    for freq in (["unity_", "unadj_", "model_", ""]): 
        variables[f"el_{freq}s"] *= variables["side_a_adj_s"]
        variables[f"el_{freq}sd"] *= variables["side_a_adj_sd"]
        variables[f"el_{freq}d"] *= variables["side_a_adj_d"]
        variables[f"el_{freq}ma"] *= variables["side_a_adj_ma"]
        variables[f"el_{freq}def_dis"] *= variables["side_a_adj_def_dis"]
        variables[f"el_{freq}sca_monc"] *= variables["side_a_adj_sca_monc"]
        variables[f"el_{freq}der_monc"] *= variables["side_a_adj_der_monc"]

    return variables


def calc_total_el(is_side_a, variables):
    """
    Calculates the total expected loss from the different loss types
     Does this for all the frequency types
    Then adjusts for the non-modelled losses and the sid
    """

    # Additional side a factors
    if is_side_a: 
        variables["side_a_final_adj"] = calc_side_a_adjustment(variables)
    else: variables["side_a_final_adj"] = 1

    # Loop through each of the loss cost types to calculate
    for freq in (["unity_", "unadj_", "model_", ""]): 
        variables[f"total_{freq}el"] = (
            variables[f"el_{freq}s"] + 
            variables[f"el_{freq}sd"] + 
            variables[f"el_{freq}d"] + 
            variables[f"el_{freq}ma"] + 
            variables[f"el_{freq}def_dis"] + 
            variables[f"el_{freq}sca_monc"] + 
            variables[f"el_{freq}der_monc"]    
        )

        # Non-modelled loss costs loading 
        variables[f"total_{freq}el"] *= (1 + variables["non_modelled_load"])

        # Apply side a adjustment
        variables[f"total_{freq}el"] *= variables["side_a_final_adj"]

    return variables


def calc_cost_severity(df, dismissal_rates, variables):
    """
    Calclates the cost severities
    Changes with sector as depends on the dismissal rate
    """
    variables["sev_def_dis"] = truncated_lognormal(variables["mu_def_dis"], variables["sigma_def_dis"], variables["limit"], variables["total_excess"], True)
    variables["mc_atcost"] = utils.look_up("AtCost", "ParameterName", "Value", df, 0)
    
    dis_monc_rate = utils.look_up("MCDismissalRate", "ParameterName", "Value", df, 0)
    dis_monc_min = utils.look_up("MCDismissalMin", "ParameterName", "Value", df, 0)
    dis_monc_max = utils.look_up("MCDismissalMax", "ParameterName", "Value", df, 0)

    # SCA monitoring costs
    variables["sca_monc"] = variables["mc_atcost"] * truncated_lognormal(variables["mu_sca"], variables["sigma_sca"], variables["limit"], variables["total_excess"], True)
    variables["sca_dis_monc"] = min(max(dis_monc_min, dis_monc_rate * variables["sev_def_dis"]), dis_monc_max)

    for i, rate in enumerate(dismissal_rates):
        if (not variables["blended"]) and (i > 0):
            break

        if rate > 0:
            variables[f"sca_monc_{i + 1}"] = (1 - variables[f"dr_sca_{i + 1}"]) * variables["sca_monc"] + variables[f"dr_sca_{i + 1}"] * variables["sca_dis_monc"]

    # Derivative monitoring costs
    variables["der_monc"] = variables["mc_atcost"] * truncated_lognormal(variables["mu_der"], variables["sigma_der"], variables["limit"], variables["total_excess"], True)
    variables["der_dis_monc"] = variables["sca_dis_monc"] 

    # Defense dismissal factor
    variables["def_dis_factor"] = (
        variables["sev_def_dis"] * 
        (1 - norm.cdf((np.log(variables["total_excess"]) - (variables["mu_def_dis"] + np.log(1 + variables["defense_sca_factor"])))/(variables["sigma_def_dis"])))
    )

    return variables


def calc_side_a_adjustment(variables):
    """
    Calculates the layer DIC adjustment
    Multiplies this by the other side a factors to calculate the final adjustment
    """
    if (variables["tower"] > 1) or (variables["excess"] > 1):
        variables["abc_per_tower"] = variables["tower"] / (variables["excess"] + variables["tower"])
        variables["dic_adjustment"] = variables["side_a_xs_side_a"] + variables["abc_per_tower"] * (variables["side_a_xs_abc"] - variables["side_a_xs_side_a"])
    else:
        variables["dic_adjustment"] = variables["prim_standalone"]

    adjustment = variables["dic_adjustment"] * variables["bankruptcy_load"] * variables["side_a_scale"]

    return adjustment


def truncated_lognormal(mu, sigma, limit, excess, above_layer = False, order = 1):
    """
    Applies the truncated lognormal distribution to a layer
    """
    # Capping at $1bn to avoid divide by zero errors
    upper = min(limit + excess, 1e9)
    lower = min(excess, 1e9)

    levupper_upper_k = (np.log(upper) - mu) / sigma - order * sigma
    levupper_phi_upper_k = norm.cdf(levupper_upper_k)
    levupper_upper = (np.log(upper) - mu) / sigma
    levupper_phi_upper = norm.cdf(levupper_upper) 
    levupper_lnorm = np.exp(order * mu + 0.5 * pow(order, 2) * pow(sigma, 2)) * (levupper_phi_upper_k) + pow((upper), order) * (1 - levupper_phi_upper)

    levlower_upper_k = (np.log(lower) - mu) / sigma - order * sigma
    levlower_phi_upper_k = norm.cdf(levlower_upper_k)
    levlower_upper = (np.log(lower) - mu) / sigma
    levlower_phi_upper = norm.cdf(levlower_upper) 
    levlower_lnorm = np.exp(order * mu + 0.5 * pow(order, 2) * pow(sigma, 2)) * (levlower_phi_upper_k) + pow((lower), order) * (1 - levlower_phi_upper)

    if above_layer:
        levlower = (np.log(lower) - mu) / sigma
        levlower_phi = norm.cdf(levlower)
        return (levupper_lnorm - levlower_lnorm) / (1 - levlower_phi)
    else:
        return levupper_lnorm - levlower_lnorm


def calc_layer_tpi(df_excess_load, variables):
    """
    Calculates the outputs for each layer
    """
    #Perform necessary runoff adjustments
    #Scale down premium and expected loss
    premium_reset = variables["premium"]
    total_el_reset = variables["total_el"]
    # if variables["is_runoff"]:
    #     variables["premium"] = variables["premium"] if variables["runoff_adjustment"] == 0 else variables["premium"] / variables["runoff_adjustment"]
        #variables["total_el"] = variables["total_el"] if variables["runoff_adjustment"] == 0 else variables["total_el"] / variables["runoff_adjustment"]

    # Calculates the capital load based on the excess
    variables["excess_load"] = calc_excess_load(df_excess_load, variables["excess"], variables["tower"])

    # Calcualtes technical premium
    variables["roc_target"] = const.roc_target # TODO: remove if using central parameter table
    variables["tech_premium_net"] = calc_tech_premium(variables["total_el"], variables, True)
    variables["tech_premium"] = calc_tech_premium(variables["total_el"], variables)

    # Calculates technical premium without UW adjustments
    # This is the equivalent of using the unity premium
    variables["tech_premium_pre_uw_adj"] = calc_tech_premium(variables["total_unity_el"], variables)

    if variables["premium"] > 0:
        # Calculates profit
        variables["net_premium"] = variables["premium"] * (1 - variables["brokerage"])

        variables["profit"] = (
            variables["net_premium"] - 
            variables["total_el"] - 
            variables["fixed_exp"] - 
            variables["net_premium"] * (variables["ri_cost"] + variables["var_exp"] - variables["inv_inc"])
        )

        # Calculates BPI
        variables["elr"] = variables["total_el"] / variables["net_premium"]
        variables["bpi"] = 0.7 / variables["elr"]
        variables["elr_pre_uw_adj"] = variables["total_unity_el"] / variables["net_premium"]
        variables["bpi_pre_uw_adj"] = 0.7 / variables["elr_pre_uw_adj"]

        # Calculates ROC
        variables["total_capital"] = variables["net_premium"] * variables["capital_factor"] * variables["excess_load"]
        variables["roc"] = variables["profit"] / variables["total_capital"]

        # Calculates TPI
        variables["tpi"] = variables["premium"] / variables["tech_premium"]

        # Calcultes TPI without UW adjustments
        variables["tpi_pre_uw_adj"] = variables["premium"] / variables["tech_premium_pre_uw_adj"]
  

    # remove the adjustment to el and premium in the case of runoff
    variables["premium"] = premium_reset
    variables["total_el"] = total_el_reset
    return variables


def calc_excess_load(df, excess, tower):
    """
    Calculates the load for the additional capital requirements for excess policies
    Column names are set
    """
    load_excess = excess + tower 

    excess_load = 1
    if (load_excess is not None): 
        if (
            (load_excess >= min(df["Excess Lower"]))  & 
            (load_excess < max(df["Excess Upper"]))
        ):
            df_row = df[
                (df["Excess Lower"] <= load_excess) & 
                (df["Excess Upper"] > load_excess)
                ].iloc[0]
            xp = [df_row["Excess Lower"],df_row["Excess Upper"]]
            fp = [df_row["Factor Lower"],df_row["Factor Upper"]]
            excess_load = np.interp(load_excess, xp, fp)

    return excess_load


def calc_tech_premium(el, variables, net = False):
    """
    Calculates the technical premium from a given expected loss
    Assumes the plan metrics are saved in the variables directory
    Can be calculated net or gross, defaulting to gross
    """

    brkge = 0 if net else variables["brokerage"]

    tech_premium = (
        (el + variables["fixed_exp"] * variables["pro_rata"]) /
        (
            (1 - brkge) * 
            (
                1 - 
                variables["cat_load"] - 
                variables["ri_cost"] - 
                variables["var_exp"] + 
                variables["inv_inc"] - 
                variables["roc_target"] * 
                variables["capital_factor"] * 
                variables["excess_load"]
            )
        )
    )

    return tech_premium


def set_layer_outputs(hxd, cov, layer, variables):
    """
    Updates layer fields in the Pricing sheet of the hxd
    Also updates the fields at the layer level based on the selected coverage
    Some fields require premium to be entered first. This is handeled as an input so some fields can still be populated if there is no premium
    """

    cov.at_cost_75 = variables["at_cost_75"]
    cov.incl_dimissals_75 = variables["incl_dimissals_75"]
    cov.technical_premium = variables["tech_premium"]
    cov.technical_premium_pre_uw_adj = variables["tech_premium_pre_uw_adj"]

    ## Data capture   
    # Setting the final premium fields 
    # Can depend on coverage or be a new value that isn't captured at a coverage level
    layer.expected_loss_cost = variables["total_el"]
    layer.expected_loss_cost_pre_uw_adj = variables["total_unity_el"]
    layer.uw_adj_impact = utils.ratio(variables["total_el"], variables["total_unity_el"]) - 1  
    layer.brokerage = cov.brokerage         
    layer.benchmark_premium = cov.benchmark_premium
    layer.written_line = cov.written_line
    layer.limit = layer.aggregate_limit = cov.limit
    layer.excess = layer.aggregate_excess = cov.excess
    layer.deductible = layer.aggregate_deductible = cov.deductible
    layer.technical_premium = cov.technical_premium
    layer.technical_premium_pre_uw_adj = cov.technical_premium_pre_uw_adj
    layer.technical_premium_net = variables["tech_premium_net"]

    if variables["premium"] > 0:
        cov.elr = variables["elr"]
        cov.tpi = variables["tpi"]
        cov.quoted_market_share = variables["premium"] * variables["written_line"]
        cov.bpi = variables["bpi"]
        cov.roc = variables["roc"]
        cov.tpi_pre_uw_adj = variables["tpi_pre_uw_adj"]    
        cov.bpi_pre_uw_adj = variables["bpi_pre_uw_adj"]  

        ## Data capture   
        layer.quoted_premium = layer.premium = cov.premium
        layer.pflr = cov.elr

        # bpi/tpi
        layer.bpi = cov.bpi
        layer.tpi = cov.tpi
        
        
        layer.roc = cov.roc
        layer.bpi_pre_uw_adj = cov.bpi_pre_uw_adj 
        # What are model and unity premium? Are they needed
        layer.profit = variables["profit"]
        layer.total_capital = variables["total_capital"]



########################################################################################################################
################################################ Other Rating Functions ################################################
########################################################################################################################


def process_bridge_premium(hxd):
    """
    Looks up the bridge premium for each country and sums them together
    """
    df_bridge = hx.params.ref_bridge_countries

    bridge_countries = hxd.cds.bridge_country

    for bridge in bridge_countries:
        bridge.premium = utils.look_up(bridge.country, "Country", "BridgePricing", df_bridge, 0)

    bridge_premium = sum([country.premium for country in bridge_countries])

    hxd.cds.bridge_premium.calculated = bridge_premium


def set_commmon_fields(hxd):
    """
    Sets fields in the cds for downstream processes
    Not needed in the premium calculations
    """
    # Saving paths as variables for readability
    stan = hxd.cds.standard_fields

    hxd.cds.key_industry.code_type = "SIC_USA"

    # Standard fields
    # Excluding: insured_country, _postal code and state_or_provinance. We don't use 3 letter codes in the rater
    # facility_reference as this will always be blank
    stan.expiry_date = hxd.hx_core.expiry_date
    stan.inception_date = hxd.hx_core.inception_date
    stan.is_free_trade_zone = True if hxd.cds.company_state == "New York (FTZ)" else False
    stan.is_case_priced = False
    stan.is_rater_priced = hxd.cds.review_type.rater_priced
    if (hxd.cds.uw_location == "US"):
        if stan.is_admitted_or_surplus.selected == "Admitted":
            stan.trifocus = "BICI D&O MM" if hxd.cds.admitted.insurer == "BICI" else "BAIC D&O MM"
        else:
            stan.trifocus = hxd.cds.trifocus_us_surplus
    elif hxd.cds.standard_fields.underwriter in ['Denis Panariti', 'Defne Tuncer' ,'Lucas Prete', 'Mathew DiGirolamo', 'Caed Hunter', 'Michael Zador']:
        stan.trifocus = "BCL D&O"
    else:
        stan.trifocus = "D&O"
    
#################################################################################################################################
################################################ TPI Calculation Sheet Functions ################################################
#################################################################################################################################


def set_tpi_calcs_capiq(path, min_trading_vol_factor, vol_of_trading_factor, execs_under_50_factor, capiq_factor):
    """
    Populates CapIQ table in SCA Frequency section
    """
    path.minimum_trading_volume_factor.value = min_trading_vol_factor
    path.volatility_of_trading_factor.value = vol_of_trading_factor
    path.execs_under_age_50_factor.value = execs_under_50_factor
    path.years_in_business.value = years_in_business_factor
    path.capiq_total_factor.value = capiq_factor

    # Comment is hardcoded
    path.capiq_total_factor.info = (
        """"Factor of 1 is the expected value for the book. 
        Above 1 means the account is riskier on average by the given metric, 
        and less risky when less than 1."""
    )



def set_tpi_calcs_freq(hxd_path, sectors, blended, sector_wghts, variables):
    """
    Updates all the frequency fields in SCA Frequency section
    """
    #### Base frequencies ####
    base_freq_comment = ""
    override_comment = ""

    for i, sector in enumerate(sectors):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not blended) and (i > 0):
            break

        if (sector is not None) and (sector_wghts[i] > 0):
            ## Base frequency comment ##
            # Don't need the sector number in the string if there is only one sector
            if (i == 0) & (len([w for w in sector_wghts if w is not None]) == 1): 
                string_start = "Sector"
            else: 
                string_start = "Sector " + str(i + 1)
            
            base_freq_comment += string_start + ": " + str(sector or "") + " , Base Frequency: " + str(format(variables[f"freq_base_sca_{i + 1}"], ".1%")) + "\n"

            override_comment += variables[f"string_freq_override_{i + 1}"]
    
    hxd_path.sca_base_frequency.value = variables["freq_base_sca"]    
    hxd_path.sca_base_frequency.comment = base_freq_comment  

#### Market cap ####
    hxd_path.market_cap_factor.value = utils.ratio(
        variables["freq_mcap_sca"],
        variables["freq_base_sca"],
        0
    )

    hxd_path.market_cap_factor.comment = "Revised Market Cap: $" + "{:,.0f}".format(variables["mcap"])  

#### IPO factor ####

    hxd_path.ipo_factor.value = utils.ratio(
        variables["freq_pre_capiq_sca"],
        variables["freq_mcap_sca"],
        0
    )

    #hxd_path.ipo_factor.value = variables.get("ipo_factor") or None
    #NOTE: need to deal with IPO factors being different for each sector

    if variables["ipo_lag"] == 1:
        string = " Year since IPO"
    else:
        string = " Years since IPO"

    hxd_path.ipo_factor.comment  = str(variables["ipo_lag"]) + string or None

#### Final freqencies ####

    hxd_path.freq_sca_after_capiq.value = variables["freq_unity_sca"]
    hxd_path.freq_sca_after_overrides.value = variables["freq_unadj_sca"]

    hxd_path.freq_sca_after_overrides.comment = override_comment
    hxd_path.freq_sca_after_modifiers.value = variables["freq_sca"]

    # Comment depends on whether there were overrides or modifiers
    if variables["mod_sca"] != 0:
        string1 = "SCA Modifiers: " + str(format(variables["mod_sca"] - 1,".1%")) + "\n"
    else: 
        string1 = ""
    if variables["sca_override"] is not None:
        string2 = "SCA Override: " + str(format(variables["sca_override"],".1%"))
    else:
        string2 = ""

    hxd_path.freq_sca_after_modifiers.comment = (
        string1 + string2
        )  
   


def set_tpi_calcs_sev(hxd_path, variables):
    """
    Updates all the fields in SCA Severity section
    """
    hxd_path.ground_up_sca_dismissal.value = variables["mean_def_dis"]
    hxd_path.ground_up_sca_dismissal.comment = "The expected loss assuming the claim has been dismissed" 



def set_tpi_calcs_dismissal(hxd_path, sectors, sector_wghts, variables):
    """
    Updates the SCA dismissal rate and comment in Technical Premium section
    """
    # Set defaults
    variables["dr_sca"] = 0
    comment = ""

    for i, sector in enumerate(sectors):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not variables["blended"]) and (i > 0):
            break

        if (sector is not None) and (sector_wghts[i] > 0):
            # Don't need the sector number in the string if there is only one sector
            if (i == 0) & (len([w for w in sector_wghts if w is not None]) == 1): 
                string_start = "Sector "
            else: 
                string_start = "Sector " + str(i + 1)
            
            variables["dr_sca"] += variables[f"dr_sca_{i + 1}"] * sector_wghts[i]
            comment += string_start + ": " + str(sector or "") + ",  " + str(format(variables[f"dr_sca_{i + 1}"], ".1%")) + "\n"
            
    hxd_path.sca_dismissal_rate.value = variables["dr_sca"]
    hxd_path.sca_dismissal_rate.comment = comment




def set_tpi_calcs_loss_cost(hxd_path, is_side_a, sector_ids, sector_wghts, variables):
    """
    Updates the loss costs fields in Technical Premium section
    """
    # The sheet shows the total SCA severity, which isn't calculted to produce the TPI
    # It is only calculated here
    # To get the total SCA severity we divide the sum of the SCA loss costs by the SCA frequency

    # Setting defaults to build up with each sector
    variables["el_sca"] = 0

    # Defaulting these variables as they will not have been set if the policy wasn't side a
    # These make the formulas easier to write out
    if not is_side_a:
        variables["side_a_adj_s"] = 1
        variables["side_a_adj_sd"] = 1
        variables["side_a_scale"] = 1
        variables["dic_adjustment"] = 1 
        variables["bankruptcy_load"] = 1 

    for i, sector in enumerate(sector_ids):
        # Loops through all sectors where the weight is greater than 0
        # Ignores sectors later than the first if "blended" not selected
        if (not variables["blended"]) and (i > 0):
            break

        if (sector is not None) & (sector_wghts[i] > 0):
            variables[f"el_sca_{i + 1}"] = variables[f"el_s_{i + 1}"] * variables["side_a_adj_s"] + variables[f"el_sd_{i + 1}"] * variables["side_a_adj_sd"]
            variables["el_sca"] += variables[f"el_sca_{i + 1}"] *  sector_wghts[i]

    #variables["el_sca"] *= variables["side_a_adj_s"] * variables["side_a_adj_sd"]

    sev_layer_sca = utils.ratio(variables["el_sca"], variables["freq_sca"], 0)
    sev_layer_sca = utils.ratio(sev_layer_sca, (1 - variables["dr_sca"]), 0) * variables["side_a_scale"]

    hxd_path.sca_loss_to_layer.value = sev_layer_sca

    # Builds comment for the layer
    # When side a need to include the ABC tower
    if is_side_a:
        hxd_path.sca_loss_to_layer.comment = (
            "Side A Deductible: " + "{:,.0f}".format(variables["deductible"]) + "\n"
            "ABC Tower: " + "{:,.0f}".format(variables["tower"]) + "\n"
            "Side A Excess: " + "{:,.0f}".format(variables["excess"]) + "\n"
            "Excess + Deductible + Tower: " + "{:,.0f}".format(variables["total_excess"]) + "\n"
            "Limit: " + "{:,.0f}".format(variables["limit"])
        )
    else:
        hxd_path.sca_loss_to_layer.comment = (
            "Deductible: " + "{:,.0f}".format(variables["deductible"]) + "\n"
            "Excess: " + "{:,.0f}".format(variables["excess"]) + "\n"
            "Excess + Deductible: " + "{:,.0f}".format(variables["total_excess"]) + "\n"
            "Limit: " + "{:,.0f}".format(variables["limit"])
        )



def set_tpi_calcs_side_a_factors(hxd_path, variables):
    hxd_path.dic_adjustment.value = variables["dic_adjustment"]
    hxd_path.bankruptcy_load.value = variables["bankruptcy_load"]



def set_tpi_calcs_outputs(hxd_path, is_side_a, variables):
    """
    Updates the TPI outputs (profit, ROC, TPI, etc.)
    """
    # Calculates the SCA and non-SCA loss costs prior to the pro rata adjustment
    # These are not used to calculate the technical price
    # They are only calculated here to show the split between SCA and non-SCA
    el_pre_pro_rata_sca = (
        variables["freq_final_s"] * variables["sev_layer_s"] * variables["side_a_adj_s"] + 
        variables["freq_final_sd"] * variables["sev_layer_sd"] * variables["side_a_adj_sd"]
    ) * variables["side_a_scale"]
    el_pre_pro_rata_non_sca = (
        variables["total_el"] / 
        ((1 + variables["non_modelled_load"]) * variables["pro_rata"] * variables["dic_adjustment"] * variables["bankruptcy_load"]) - 
        el_pre_pro_rata_sca
    )
    cat_load_pre_pro_rata = (el_pre_pro_rata_sca + el_pre_pro_rata_non_sca) * variables["non_modelled_load"]
    el_pre_pro_rata = (el_pre_pro_rata_sca + el_pre_pro_rata_non_sca + cat_load_pre_pro_rata) * variables["dic_adjustment"] * variables["bankruptcy_load"]

    hxd_path.sca_loss_cost.value = el_pre_pro_rata_sca
    if is_side_a:
        hxd_path.sca_loss_cost.info = "= Frequency After Modifiers * Expected SCA Loss to Layer * (1 - Dismissal Rate) * Side A Adjustment"
    else:
        hxd_path.sca_loss_cost.info = "= Frequency After Modifiers * Expected SCA Loss to Layer * (1 - Dismissal Rate)"
    hxd_path.non_sca_loss_cost.value = el_pre_pro_rata_non_sca
    hxd_path.cat_load.value = cat_load_pre_pro_rata
    hxd_path.abc_loss_cost.value = el_pre_pro_rata
    hxd_path.abc_loss_cost.info = "= SCA Loss Cost + Non-SCA Loss Cost + Cat Load"
    hxd_path.side_a_loss_cost.value = el_pre_pro_rata
    hxd_path.side_a_loss_cost.info = "= (SCA Loss Cost + Non-SCA Loss Cost + Cat Load) * DIC Adjustment * Bankruptcy Load"

    if not math.isclose(1,variables["pro_rata"]):
        hxd_path.abc_loss_cost.comment = (
            "After Pro-Rata factor of " +
            str(format(variables["pro_rata"], ".3")) +
            " becomes: " +
            "{:,.0f}".format(variables["total_el"])
        )

    hxd_path.side_a_loss_cost.comment = hxd_path.abc_loss_cost.comment

    # Display TPI variables
    hxd_path.profit.info = "= Net Premium - Loss Cost - Cost of Reinsurance - Expenses + Investment Income"
    hxd_path.roc.info = "= Profit / Capital Required to Service the Risk"
    hxd_path.technical_premium.info = "= (Loss Cost + Fixed Expenses) / {( 1 - Brokerage)*(1 - RI Costs % - Variable Expenses % + Investment Returns % - 15% * Capital Factor)}"
    hxd_path.tpi.info = "= Net Premium / Technical Premium"
    hxd_path.technical_premium.value = variables["tech_premium"]

    if variables["premium"] > 0:
        hxd_path.net_premium.value = variables["net_premium"]
        hxd_path.profit.value = variables["profit"]
        hxd_path.roc.value = variables["roc"]
        hxd_path.tpi.value = variables["tpi"]
        
    # Calculates the profit required to achieve the target ROC
    profit_required = variables["roc_target"] * variables["tech_premium"] * (1 - variables["brokerage"]) * variables["capital_factor"] * variables["excess_load"]

    hxd_path.net_premium.comment = (
        "Brokerage: " + str(format(variables["brokerage"], ".1%")) + "\n" + 
        "Cost of Reinsurance per Net Premium: " + str(format(variables["ri_cost"], ".1%")) + "\n" +
        "Varibale Expenses per Net Premium: " + str(format(variables["var_exp"], ".1%")) + "\n" +
        "Fixed Expenses (USD): " + "{:,.0f}".format(variables["fixed_exp"]) + "\n" +
        "Investment Income per Net Premium: " + str(format(variables["inv_inc"], ".1%")) + "\n" +
        "Profit Required for " + str(format(variables["roc_target"], ".0%")) + " ROC: " + "{:,.0f}".format(profit_required)
    )



def set_tpi_calcs_book_averages(hxd_path, df, is_side_a ,variables):
    """
    Sets the book averages for each field based on uw location and coverage
    """
   
    if is_side_a is True:
        if variables["uw_location"] == "UK":
            lookup_col = "Side A UK Average"
        else:
            lookup_col = "Side A US Average"
    else:
        if variables["uw_location"] == "UK":
            lookup_col = "ABC UK Average"
        else:
            lookup_col = "ABC US Average"

    # New tpi calcs sheet
    hxd_path.sca_base_frequency.book_average = utils.look_up("Sector Base Frequency", "Field", lookup_col, df, 0)
    hxd_path.market_cap_factor.book_average = utils.look_up("Market Cap Factor", "Field", lookup_col, df, 0) 
    hxd_path.ipo_factor.book_average = utils.look_up("IPO Factor", "Field", lookup_col, df, 0)
    hxd_path.minimum_trading_volume_factor.book_average = utils.look_up("Minimum Trading Volume Factor", "Field", lookup_col, df, 0)
    hxd_path.volatility_of_trading_factor.book_average = utils.look_up("Volatility of Trading During Downturn Factor", "Field", lookup_col, df, 0)
    hxd_path.execs_under_age_50_factor.book_average = utils.look_up("Percentage of Executives under age 50 Factor", "Field", lookup_col, df, 0)
    hxd_path.years_in_business_factor.book_average = utils.look_up("Years in Business Factor", "Field", lookup_col, df, 0)
    hxd_path.capiq_total_factor.book_average = utils.look_up("Total Factor", "Field", lookup_col, df, 0)
    hxd_path.freq_sca_after_capiq.book_average = utils.look_up("Frequency After CapIQ Score", "Field", lookup_col, df, 0)
    hxd_path.freq_sca_after_overrides.book_average = utils.look_up("Frequency After Sector SCA Overrides", "Field", lookup_col, df, 0)
    hxd_path.freq_sca_after_modifiers.book_average = utils.look_up("Frequency After Modifiers", "Field", lookup_col, df, 0)
    hxd_path.sca_dismissal_rate.book_average = utils.look_up("SCA Dismissal Rate", "Field", lookup_col, df, 0)
    hxd_path.dic_adjustment.book_average = utils.look_up("DIC Adjustment", "Field", lookup_col, df, 0)
    hxd_path.bankruptcy_load.book_average = utils.look_up("Bankruptcy Load", "Field", lookup_col, df, 0)



def calc_ipo_rarc(hxd):
    """
    Calculates risk characteristics rate change looking up the ipo lag in a param table
    Done for each sector and then weighted
    """
    ind = hxd.cds.key_industry
    agg = hxd.cds.exposure.aggregate
    
    rarc = 1
    if (not agg.ignore_ipo) and (agg.ipo_date is not None):
        rarc = 0

        sector_ids = [ind.sector_id, ind.sector_id_2, ind.sector_id_3]
        sector_wghts = [
            ind.sic_percentage if ind.sic_percentage else 0, 
            ind.sic_percentage_2 if ind.sic_percentage_2 else 0, 
            ind.sic_percentage_3 if ind.sic_percentage_3 else 0
            ]

        df_ipo_rarc = hx.params.ref_ipo_lag

        ipo_max = max(df_ipo_rarc["Lag"])  
        ipo_lag = calc_pro_rata(agg.ipo_date, hxd.hx_core.inception_date, 2) * 360
        ipo_lag = min(math.floor(ipo_lag / 360), ipo_max) 

        for i, sector in enumerate(sector_ids):
            if (not ind.blended_sic) and (i > 0):
                break
            
            if sector_wghts[i] > 0 and sector is not None:
                ipo_sector = 1 if sector == 1 else 0
                change = utils.look_up_condition((df_ipo_rarc["Lag"] == ipo_lag) & (df_ipo_rarc["Sector"] == ipo_sector),
                    "Reduction to apply in RC",
                    df_ipo_rarc,
                    0
                )
                rarc += change * sector_wghts[i]

        rarc = 1 if rarc == 0 else rarc

    return rarc   