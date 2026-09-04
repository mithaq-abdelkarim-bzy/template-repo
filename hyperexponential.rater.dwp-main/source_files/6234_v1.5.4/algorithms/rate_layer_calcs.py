import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, df_to_dict, write_pd_to_hxd, look_up, ratio, interp2d_agg_factors, extract_subkey_values
from algorithms import parameter_tables_schema as params
from operator import itemgetter

def rate_layer_calcs(hxd):

    # Shortcuts
    rf = hxd.cds.rating_factors
    fx_rates = params.fx_rates.df()

    gu_el_ed = hxd.cds.ground_up_expected_loss.education
    gu_el_non_ed = hxd.cds.ground_up_expected_loss.non_education

    pol = hxd.cds.layers[0]
    pricing_ilf = hx.params.ilf_pricing
    market_ilf = hx.params.ilf_market

    # FX rate
    fx = look_up(hxd.cds.currencies.source_currency, "ccy", "fx_rate", fx_rates, if_not_found=1)

    # Liability cover factor
    liab_coverage_ftr_dict = df_to_dict(hx.params.liability_coverage_factor, "Liability Coverage", "Factor")
    liability_factor = liab_coverage_ftr_dict["Yes"] if rf.liability_covered else liab_coverage_ftr_dict["No"]

    # Calc ILF factor for min premium base ($1m limit, no deductible)
    ilf_factor_min_premium_base = np.interp(1e6, pricing_ilf["Limit"], pricing_ilf["ILF"])
    ed_min_prem = hxd.cds.min_premium_base.education
    non_ed_min_prem = hxd.cds.min_premium_base.non_education    

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CALC ILFS AND OTHER RATING FACTORS BY LAYER   
    
    # Convert policy terms to USD (i.e. first layer)
    # Only the limit / agg limit varies in the other layers for the alternative view, which will get updated in the loop
    limit_usd = (pol.limit or 0)/fx
    excess_usd = (pol.excess or 0)/fx
    deductible_usd = (pol.deductible or 0)/fx
    agg_usd = (pol.aggregate_limit or 0)/fx

    # Agg ratio factor is common for all layers (even though limit varies)
    agg_ratio = agg_usd / limit_usd if limit_usd > 0 else 0
    
    # Loop to calc expected loss by layer, updating the params which vary by layer
    for idx, layer in enumerate(hxd.cds.layers):

        # Overwrite limit with other inputs for alternate layers (first will be the same as above)
        if idx > 0:
            limit_usd = (layer.alt_limit.selected or 0)/fx
            agg_usd = (layer.alt_agg_limit.selected or 0)/fx

        # Overwrite agg limit ratio if this is updated in the model (for alt limits only)
        agg_ratio = agg_usd / limit_usd if limit_usd > 0 else 0

        # Agg limit multiplier, custom function for 2D linear interpolation given an agg ratio factor
        if agg_ratio in [1,2,3,4,5]:
            # EDUCATION
            agg_limit_ilf_factor_ed = interp2d_agg_factors(
                hx.params.agg_limit_factors, 
                hxd.cds.exposure.aggregate.total_schools,
                limit_usd,
                agg_ratio
            )
            # NON EDUCATION
            agg_limit_ilf_factor_non_ed = interp2d_agg_factors(
                hx.params.agg_limit_factors, 
                hxd.cds.exposure.aggregate.total_non_ed_est,
                limit_usd,
                agg_ratio
            )
        else:
            agg_limit_ilf_factor_ed = agg_limit_ilf_factor_non_ed = 0
            if idx == 0:
                hx.errors.validation("Error: Aggregate limit is not within 1 to 5x Limit. Please check.")
            else:
                hx.errors.validation(f"Error: Scenario {idx} aggregate limit is not within 1 to 5x Limit. Please check.")
       
        # ILF
        lower = deductible_usd if pol.type == "Deductible" else excess_usd
        upper = limit_usd if pol.type == "Deductible" else excess_usd + limit_usd

        if upper > lower:
            pricing_ilf_factor = np.interp(upper, pricing_ilf["Limit"], pricing_ilf["ILF"]) - np.interp(lower, pricing_ilf["Limit"], pricing_ilf["ILF"])
            market_ilf_factor = np.interp(upper, market_ilf["Limit"], market_ilf["ILF"]) - np.interp(lower, market_ilf["Limit"], market_ilf["ILF"])
        else:
            pricing_ilf_factor = 0
            market_ilf_factor = 0
            if idx == 0: # Only run validation on main layer
                hx.errors.validation(f"Error: Deductible is not less than Limit. Please check.")

        # Save base market ILF factor for Suggested EPI calc 
        if idx == 0:
            base_market_ilf = market_ilf_factor
        else:
            layer.suggested_epi = pol.quoted_premium * (market_ilf_factor / base_market_ilf) if base_market_ilf and pol.quoted_premium else None

        # BI TIV as a % of limit 
        # Note this varies by layer as is dependent on limit
        bi_tiv_tbl = hx.params.bi_tiv
        bi_tiv_col = "Separate limits" if rf.seperate_bi_ee_agg_limits else "Combined limits"

        if rf.bi_and_ee_cover:
            tiv_lim_ratio = ratio((rf.bi_tiv or 0 ), (layer.limit or 0), if_undefined=0)
            bi_ee_factor = bi_tiv_tbl[tiv_lim_ratio >= bi_tiv_tbl["(BI TIV) / Limit"]][bi_tiv_col].iloc[-1]
        else:
            bi_ee_factor = 1

        layer.expected_loss.education = (
            gu_el_ed
            * pricing_ilf_factor
            * agg_limit_ilf_factor_ed # Ed
            * rf.preparedness_factor_ed # Ed
            * liability_factor
            * bi_ee_factor
            * (1 + rf.extensions_covered)
            # Convert back to policy currency
            * fx
        )

        layer.expected_loss.non_education = (
            gu_el_non_ed
            * pricing_ilf_factor
            * agg_limit_ilf_factor_non_ed # Non ed
            * rf.preparedness_factor_non_ed # Non ed
            * liability_factor
            * bi_ee_factor
            * (1 + rf.extensions_covered)
            # Convert back to policy currency
            * fx
        )

        # Calculate min premiums by layer
        min_premium_scale = max(pricing_ilf_factor / ilf_factor_min_premium_base, 1)
        layer.min_premium.education = ed_min_prem * min_premium_scale / (1 - pol.brokerage)
        layer.min_premium.non_education = non_ed_min_prem * min_premium_scale / (1 - pol.brokerage)

        
        pass # End loop
    


