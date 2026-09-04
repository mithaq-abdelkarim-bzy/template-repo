import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import look_up, df_to_dict, format_millions, policy_term
from operator import itemgetter


# Function to calculate cumulative index
def calc_cumulative_index(inflation_series):
    cumulative_index = [1]
    for inflation in inflation_series:
        new_index = cumulative_index[-1] * (1 + inflation)
        cumulative_index.append(new_index)
    cumulative_index.pop()  # Drop the final value to match inf length
    return cumulative_index


def validate_underwriter(hxd):
    UNDERWRITERS_LIST = list(hx.params.lst_underwriters['Underwriters'])
    value = hxd.cds.standard_fields.underwriter
    hxd.uw_validation.show_underwriter_warning = False
        
    if value not in (UNDERWRITERS_LIST + [None]):
        hxd.uw_validation.show_underwriter_warning = True
        hx.errors.validation("The selected Underwriter name is outside the dropdown list. Please choose one from the list.")
        hxd.uw_validation.underwriter_warning = "❗❗ The selected Underwriter name is outside the dropdown list. Please choose one from the list ❗❗"
    

def rate_risk_information(hxd):
    
    #~~~~~~~~~~~~~~~~~~~~~~~
    # CONTROLS & MESSAGES

    validate_underwriter(hxd)
 
    pol = hxd.cds.layers[0]
    ccy = hxd.cds.currencies.source_currency

    hxd.messages.policy_info_note = f"Note: All Figures at 100% line size and in {ccy}"
    hxd.messages.epi_heading = "Gross Quoted Premium" if ccy == "USD" else f"Gross Quoted Premium ({ccy})"
    hxd.messages.crime_website = f"Crime Grade Website   [https://crimegrade.org/](https://crimegrade.org/)"

    deductible = pol.deductible if pol.type == 'Deductible' else pol.excess
    hxd.messages.rating_summary_note = f"""Note: All Figures at 100% line size and in {ccy}.

    Limit: {format_millions(pol.limit, ccy)}
    Aggregate limit: {format_millions(pol.aggregate_limit, ccy)}
    {pol.type}: {format_millions(deductible, ccy)}
    """
    
        
    
    # Set agg limits dropdown (ALT set below)
    occ_limit = pol.limit or 1e6       
    pol.agg_limits_list = [{"values": (i+1)*occ_limit} for i in range(5)]


    hxd.flags.deductible_flag = pol.type == "Deductible"
    hxd.flags.excess_flag = pol.type == "Excess"

    # Benchmark Class
    hxd.cds.standard_fields.benchmark_class = "DWP"
    
    # Experience rating info
    hxd.messages.experience_rating_note = "Exposure adjusted losses with TIV"


    #~~~~~~~~~~~~~~~~~~~~~~~
    # COMMON FACTORS
    rf = hxd.cds.rating_factors

    # Policy term, note the minimum policy term is 2 months
    rf.policy_term = max(
        policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date),
        2/12
    )


    # Preparedness factors
    social_media_dict = df_to_dict(hx.params.preparedness_factor_social_media, "Social Media", "Factor")
    high_profile_event_dict = df_to_dict(hx.params.preparedness_factor_high_profile_event, "High Profile Event", "Factor")
    
    social_media_factor = social_media_dict["Yes"] if rf.social_media else social_media_dict["No"]

    # High profile event factor (non-education only) (E.g. London Marathon, Olympic Games etc.)
    high_profile_event_factor = high_profile_event_dict[rf.high_profile_event]

    preparedness_factor_df = hx.params.preparedness_factor
    pepartness_factors_other = (
        look_up(rf.risk_preparedness,"Level", "Risk Preparedness", preparedness_factor_df)
        * look_up(rf.security,"Level", "Security", preparedness_factor_df)
        * look_up(rf.crisis_management,"Level", "Crisis Management", preparedness_factor_df)
    )
    
    rf.preparedness_factor_ed = pepartness_factors_other * social_media_factor
    rf.preparedness_factor_non_ed = pepartness_factors_other * social_media_factor * high_profile_event_factor

    



    #~~~~~~~~~~~~~~~~~~~~~~~
    # ALT LIMITS

    # layer[idx] : limit
    alt_limits_dict = {
        1: 1e6,
        2: 3e6,
        3: 5e6,
        4: 10e6,
        5: 20e6
    }

    # Set alt agg limits using the same ratio as the policy layer 
    # Note this is all in policy currency
    agg_ratio = max((pol.aggregate_limit or 0) / (pol.limit or 0) if pol.limit else 1, 1)
    for idx in range(1, 6):
        hxd.cds.layers[idx].alt_limit.calculated = alt_limits_dict[idx]
        hxd.cds.layers[idx].alt_agg_limit.calculated = alt_limits_dict[idx] * agg_ratio

        # Set ALT agg limits dropdown
        occ_limit = hxd.cds.layers[idx].alt_limit.calculated or 1e6
        hxd.cds.layers[idx].agg_limits_list = [{"values": (i+1)*occ_limit} for i in range(5)]
    
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # INFLATION

    inf = hx.params.inflation.sort_values(by="YOA")    

    # Calculate cumulative indices for each type of inflationm, starting at 100%
    inf['Base Index'] = calc_cumulative_index(inf['Base Inflation'])
    inf['Social Index'] = calc_cumulative_index(inf['Social Inflation'])

    # Assume event happens half way through policy term
    est_event_yr = max(
        (hxd.hx_core.inception_date + (hxd.hx_core.expiry_date - hxd.hx_core.inception_date)/2).year,
        min(inf['YOA'])
    )
    
    # Assign to hxd
    hxd.cds.rating_factors.base_inflation = look_up(est_event_yr, "YOA", "Base Index", inf, if_not_found=1)
    hxd.cds.rating_factors.social_inflation = look_up(est_event_yr, "YOA", "Social Index", inf, if_not_found=1)

