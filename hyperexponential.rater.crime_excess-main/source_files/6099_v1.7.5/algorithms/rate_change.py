import hx
import pandas as pd
import numpy as np
import copy
import algorithms.utils_global_lists as lst
from algorithms.layer_calcs import *
from algorithms.rate_constants import *
from libraries.admitted_excess_premium.algorithms.rate_admitted_excess import excess_attach_factor_calculations, base_limit_factor_calculation, load_and_prepare_data
import shutil
import os
from bisect import bisect_right
from functools import lru_cache


# This rate change file inputs the parameters of the expiring policy into the functions from 'rating_functions' to rate up the expiring policy.
# The deductible, limits and exposures are then changed in term to split out the impact of updating each of these individually
# which means the rating is done three times


def rate_change(hxd):
    
    cds = hxd.cds
    layer = cds.layers[0]
    rc = layer.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    hxd.expiring_policy_option_id = rc.expiring_policy_option_id.selected
    rating = cds.rating_factors
    dataframes= load_and_prepare_data(hxd)
    df_ilf = dataframes.excess_2_ilf
    df_type = dataframes.excess_state_type
    state = cds.standard_fields.insured_state_or_province
    # Pulling types    
    if df_type["State"].isin([state]).any():
        type_row = df_type[df_type["State"] == state].iloc[0]
    else:
        hx.errors.validation("The State Selected is not recognised")
        return None

    param_other_perils = fx.df_to_dict(hx.params.other_perils, "Other Perils", ["On-Premises", "Off-Premises"])

# first define all needed inputs, then back out factor, then re-add the expiring factors
    excess_attachment_factor = excess_attach_factor_calculations(cds.admitted_excess, df_ilf,  type_row["ILF Type"]) # new-new
    basic_limit_factor = base_limit_factor_calculation(cds.admitted_excess, df_ilf, type_row["ILF Type"]) # dont need
    rc_backed_out_premium = layer.unity_premium*(basic_limit_factor/excess_attachment_factor) # dont need

##redfine list to expiring (old/old)
    rc_expring_excess_expiring = copy.deepcopy(cds.admitted_excess)
    rc_expring_excess_expiring.excess_limit = rc.expiring_limit or 0
    rc_expring_excess_expiring.excess_attachment_point = rc.expiring_excess or 0
    
#re-reun fucntion with expring list
    rc_excess_attach_factor_expiring = excess_attach_factor_calculations(rc_expring_excess_expiring, df_ilf, type_row["ILF Type"]) # old-old
    rc_basic_limit_factor_expiring = base_limit_factor_calculation(rc_expring_excess_expiring, df_ilf, type_row["ILF Type"]) # dont need

#redfine list to expiring (new/old)
    rc_expring_excess_new_limit = copy.deepcopy(cds.admitted_excess)
    rc_expring_excess_new_limit.excess_limit.value = cds.admitted_excess.excess_limit.value or 0
    rc_expring_excess_new_limit.excess_attachment_point = rc.expiring_excess or 0

#re-reun fucntion with expring list
    rc_excess_attach_factor_expiring_new_limt = excess_attach_factor_calculations(rc_expring_excess_new_limit, df_ilf, type_row["ILF Type"]) # new-old
    rc_basic_limit_factor_expiring_new_limit = base_limit_factor_calculation(rc_expring_excess_new_limit, df_ilf, type_row["ILF Type"]) # dont need

# # calculate expiring premiums
#     rc_old_old_unity_premium = rc_backed_out_premium*(rc_excess_attach_factor_expiring/rc_basic_limit_factor_expiring)
#     rc_new_old_unity_premium = rc_backed_out_premium*(rc_excess_attach_factor_expiring_new_limt/rc_basic_limit_factor_expiring_new_limit)


# # Return unity premium for layer to price
    # if cds.underlying_rate_per_m and cds.beazley_limit and cds.beazley_share and rc.expiring_beazley_share:

    #     (ded_factor, weight_df, implied_pricing, renewing_excess, renewing_limit, renewing_calcs, primary) = benchmark_calcs(hxd)

    #     rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    #     hxd.expiring_policy_option_id = rc.expiring_policy_option_id.selected

    #     # Calculate base premiums for all 3 structures based on expiring exposures
    #     rate_revenue_rc = base_rate_calc(hxd, "Revenue", rc.expiring_revenue)
    #     rate_assets_rc = base_rate_calc(hxd, "Assets", rc.expiring_assets)
    #     rate_employees_rc = base_rate_calc(hxd, "Employees", rc.expiring_employees)

    #     adj_fct_locations_rc = max(0.8, min(1.25, (1.6 + math.log10( rc.expiring_locations + 1 )) / 3))
    #     adj_fct_assets_rc = 0.875 if rc.expiring_assets < 100000 else (math.log10( rc.expiring_assets) + 12.5 ) / 20
    #     adj_fct_max_rc = max(adj_fct_locations_rc, adj_fct_assets_rc)

    #     commercial_main_rc = (rate_revenue_rc + rate_employees_rc) / 2 * adj_fct_locations_rc * adj_fct_assets_rc
    #     commercial_se_rc = rate_revenue_rc * adj_fct_assets_rc

    #     std_struct_main_rc = commercial_main_rc * hxd.total_adj_factor
    #     std_struct_se_rc = commercial_se_rc * hxd.total_adj_factor  if cds.has_social_engineering else 0
    #     std_struct_other_rc = (std_struct_main_rc + std_struct_se_rc) * max(0.025, param_other_perils[rating.other_on_premises]["On-Premises"] + param_other_perils[rating.other_off_premises]["Off-Premises"]) if cds.has_other_coverages else 0

    #     calcs_dfs = {}
    #     for df in ['primary_struct', 'expiring_df']:
    #         calcs_dfs[df] = pd.DataFrame(index = ["main", "se", "other"])

    #     primary_struct = calcs_dfs['primary_struct']
    #     primary_struct['std_struct_rc'] = [std_struct_main_rc, std_struct_se_rc, std_struct_other_rc]

    #     primary_struct['std_lim_ded_adj_rc'] = primary_struct['std_struct_rc'] * ded_factor

    #     # Replace implied pricing for base structure by the expiring one. For simplicity, all other layers' implied pricing will not change.
    #     calcs_dfs['implied_pricing_std_lim_ded_adj_rc'] = implied_pricing
    #     calcs_dfs['implied_pricing_std_lim_ded_adj_rc']['Base'] = primary_struct['std_lim_ded_adj_rc'] 

    #     std_lim_pol_ded_price_rc = (calcs_dfs['implied_pricing_std_lim_ded_adj_rc'] * weight_df).sum(axis=1)

    #     # Set expiring limits/deductibles. Assume other coverage limit/deductible does not change to reduce the number of expiring inputs asked.
    #     calcs_dfs['expiring_df']['excess'] = [rc.expiring_excess, rc.expiring_excess_social_engineering, renewing_excess.loc['other']]
    #     calcs_dfs['expiring_df']['limit'] = [rc.expiring_limit, rc.expiring_limit_social_engineering,  renewing_limit.loc['other']]

    #     # Run several iterations of the calculated premium with expiring inputs and updating each at a time.
    #     calcs_df_exp = exposure_factor(hxd, calcs_dfs['expiring_df']['excess'], calcs_dfs['expiring_df']['limit'], primary)

    #     calcs_df_update_deductible = exposure_factor(hxd, renewing_excess, calcs_dfs['expiring_df']['limit'], primary)

    #     calcs_df_update_deductible_limit = renewing_calcs

    #     # Annualised premiums from expiring inputs 
    #     unity_premium_exp = (calcs_df_exp * std_lim_pol_ded_price_rc).sum(axis=0)
    #     unity_premium_update_deductible = (calcs_df_update_deductible * std_lim_pol_ded_price_rc).sum(axis=0)
    #     unity_premium_update_deductible_limit = (calcs_df_update_deductible_limit.multiply(std_lim_pol_ded_price_rc, axis=0)).sum(axis=0).iloc[0]

    # ~~~~~~~~~~~~~~ SET INDIVIDUAL RATE CHANGE ELEMENTS ~~~~~~~~~~~~~~~~~~~

    
    # Set all default rate change values as 1, this is only applicable for other and T&Cs
    rc_list = [item + "_change" for item in lst.rate_change_list_static]
    for item in rc_list:
        rc_vbl = getattr(rc,item)
        setattr(rc_vbl.uw_selected, "calculated", 1)
        rc_vbl.model_calculated = rc_vbl.uw_selected.calculated

    # Calculate rate change

    # Exposure change
    # number of employees change    
    if rc.expiring_employees != 0:
        employee_change = cds.exposure.aggregate.employees / rc.expiring_employees - 1
        employee_change_factor = 1 + employee_change / 2
    else:
        employee_change_factor = 1


    # Assets change
    if rc.expiring_assets != 0:
        assets_change = cds.exposure.aggregate.assets / rc.expiring_assets
        assets_change_factor = assets_change ** 0.2
    else:
        assets_change_factor = 1

    #Revenue Change
    param_rev = fx.df_to_dict(
        hx.params.revenue_base_rates,      
        "revenue_lb",                     
        ["revenue_ub", "base_rate"]        
    )

    # Normalize keys to int in case they came in as strings
    param_rev = {int(float(lb)): {"revenue_ub": int(float(v["revenue_ub"])),
                                "base_rate": float(v["base_rate"])}
                for lb, v in param_rev.items()}

    @lru_cache(maxsize=1)
    def _rev_lbs_sorted():
        lbs = sorted(param_rev.keys())
        return lbs

    def revenue_base_rate(revenue_value: float, clamp_below_min: bool = True) -> float:
        """
        Excel-style approximate match:
        pick the band with the largest revenue_lb <= revenue_value (no interpolation).
        """
        if revenue_value is None:
            raise ValueError("Revenue value is None")
        lbs = _rev_lbs_sorted()
        i = bisect_right(lbs, int(revenue_value)) - 1
        if i < 0:
            if clamp_below_min:
                i = 0
            else:
                raise ValueError(f"Revenue {revenue_value} is below the minimum bracket {lbs[0]}")
        lb = lbs[i]
        return float(param_rev[lb]["base_rate"])

    revenues_new_base_rate = revenue_base_rate(cds.exposure.aggregate.revenue)
    revenues_expiring_base_rate = revenue_base_rate(rc.expiring_revenue)
    revenues_change_factor = revenues_new_base_rate / revenues_expiring_base_rate  

    # Number of locations
    param_loc = fx.df_to_dict(
        hx.params.number_of_locations,     
        "break",                           
        ["lb_factor", "ub_factor"]         
    )

    # Normalize keys/values (ensure numeric types) and precompute sorted breaks
    param_loc = {
        float(b): {
            "lb_factor": float(v["lb_factor"]),
            "ub_factor": float(v["ub_factor"])
        }
        for b, v in param_loc.items()
    }

    @lru_cache(maxsize=1)
    def _loc_breaks_and_factors():
        breaks = sorted(param_loc.keys())                 
        lb = [param_loc[b]["lb_factor"] for b in breaks]  # per-row LB factors
        ub = [param_loc[b]["ub_factor"] for b in breaks]  # per-row UB factors
        if len(breaks) < 2:
            raise ValueError("Locations table must have at least two break rows.")
        return breaks, lb, ub

    def location_factor(num_locations: float) -> float:
    
        if num_locations is None:
            raise ValueError("num_locations is None")
        x = float(num_locations)
        breaks, lb, ub = _loc_breaks_and_factors()

        # Ceiling rule (>= final breakpoint)
        if x >= breaks[-1]:
            return ub[-1]

        # Find i such that breaks[i] <= x < breaks[i+1]
        i = bisect_right(breaks, x) - 1
        i = max(0, min(i, len(breaks) - 2))  # clamp for safety

        x0, x1 = breaks[i], breaks[i + 1]
        y0, y1 = lb[i], ub[i]

        # Linear interpolation
        t = 0.0 if x1 == x0 else (x - x0) / (x1 - x0)
        return y0 + t * (y1 - y0)

    number_locations_new_base_rate = location_factor(cds.exposure.aggregate.locations)
    number_locations_expiring_base_rate = location_factor(rc.expiring_locations)
    number_locations_change_factor = number_locations_new_base_rate / number_locations_expiring_base_rate

    # Total Exposure Change
    rc.exposure_change.uw_selected.calculated = (
        employee_change_factor 
        * assets_change_factor
        * revenues_change_factor
        * number_locations_change_factor
    )
    
    rc.exposure_change.model_calculated = rc.exposure_change.uw_selected.calculated

    # Limit
    rc.limit_change.uw_selected.calculated = rc_excess_attach_factor_expiring_new_limt / rc_excess_attach_factor_expiring if cds.total_layer_limit and rc_excess_attach_factor_expiring else 1
    rc.limit_change.model_calculated = rc.limit_change.uw_selected.calculated

    # Deductible
    rc.deductible_change.uw_selected.calculated = excess_attachment_factor / rc_excess_attach_factor_expiring_new_limt if cds.total_layer_limit and rc_excess_attach_factor_expiring_new_limt else 1
    rc.deductible_change.model_calculated = rc.deductible_change.uw_selected.calculated

    # Brokerage
    if rc.expiring_brokerage and layer.brokerage:
        rc.brokerage_change.uw_selected.calculated = (1 - rc.expiring_brokerage) / (1  - layer.brokerage) if rc.expiring_brokerage != 1 and layer.brokerage != 1 else 1
        rc.brokerage_change.model_calculated = rc.brokerage_change.uw_selected.calculated

    # Calculate final rate change by taking the product of all selected rate changes in the static list 
    final_rc = 1
    final_rc_calculated_only = 1
    for item in rc_list:
        rc_vbl = getattr(rc,item)
        final_rc *= rc_vbl.uw_selected.selected
        final_rc_calculated_only *= rc_vbl.model_calculated
    
    # Calculate annualised renewing and expiring premiums at 100% line size
    if layer.final_premium_annual and cds.beazley_share:
        renewal_premium = layer.final_premium_annual / cds.beazley_share
        if rc.expiring_beazley_share:
            if rc.expiring_premium_annual:
                expiring_premium = rc.expiring_premium_annual / rc.expiring_beazley_share
            else:
                expiring_premium = (rc.expiring_premium / (rc.expiring_policy_term / 12)) / rc.expiring_beazley_share
        else:
            expiring_premium = 0

        # Divide actual premium change by calculated rate change to get 'true' rate change
        premium_percentage_change = renewal_premium / expiring_premium if expiring_premium else 0
        rc.rate_change.uw_selected = premium_percentage_change/final_rc if final_rc else 0
        rc.rate_change.model_calculated = premium_percentage_change/final_rc_calculated_only if final_rc_calculated_only else 0

    pass