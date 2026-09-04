import hx
import json
import pandas as pd
pd.set_option("display.max_columns", None)
import numpy as np
from algorithms import parameter_tables_schema as params
from algorithms.data_schema.sch_rater_defined import ihs_risk_names
from algorithms.rate_utilities import one_layer, look_up, look_up_closest, find_closest, usd, rgetattr, rsetattr, get_countries_retrieved
from algorithms.rate_utilities import title_rc, linear_interp, mbbefd, ratio, pd_df_from_hx_list, write_pd_to_hxd, tp_components
from algorithms.rate_constants import bi_weighting, cbi_load

### --- HELPER FUNCTIONS --- ###
def merge_ihs_rates(left_df, right_df, left_on, right_on, right_columns=None, direction="backward"):
    
    ## prepare left dataframe - coerce errors and sort
    left                    = left_df.copy()
    left[left_on]           = pd.to_numeric(  left[left_on],   errors='coerce')         # Convert left_on to numeric, coercing errors to NaN
    left["_original_order"] = np.arange(len(left))                                      # Save the original order
    left_sorted             = left.sort_values(left_on)                                 # Sort left_df by the merge key
    
    ## prepare right dataframe - coerce errors, using selected columns where given  and sort
    right           = right_df.copy()
    right[right_on] = pd.to_numeric(right[right_on], errors='coerce')                   # Convert left_on to numeric, coercing errors to NaN

    if   (right_columns is not None) and (right_on not in right_columns):     right_columns = list(right_columns) + [right_on]
    elif (right_columns is not None):                                         right_columns = list(right_columns)
    else:                                                                     right_columns = right.columns  

    right_sorted    = right[ right_columns ].sort_values( right_on )

    # Perform the merge, Restore the original order and drop the temporary column
    merged          = pd.merge_asof(left_sorted, right_sorted, left_on=left_on, right_on=right_on, direction=direction)
    merged          = merged.sort_values("_original_order").drop(["_original_order", right_on], axis=1)      
    
    return merged



def scale_sum_insured(curves_df):
    # Take a copy of df
    curves_df = curves_df.copy()

    # Initialize result as a numeric Series (blank categories will remain NaN)
    result               = pd.Series(np.nan, index=curves_df.index)
    
    # Process only rows where category is not blank
    non_blank_mask       = curves_df["category"].notna() & (curves_df["category"] != "")
    
    # ----- TOP category -----
    top_mask             = curves_df["category"] == "Top"
    result.loc[top_mask] = curves_df.loc[top_mask, "si_unscaled"]
    
    # ----- SECOND TOP category -----
    second_top_mask      = curves_df["category"] == "Second top"
    st_sum               = curves_df["si_unscaled"].shift(1) + curves_df["si_unscaled"]
    st_within_mask       = second_top_mask & (st_sum <= curves_df["selected_sum_insured"])
    st_over_mask         = second_top_mask & (st_sum > curves_df["selected_sum_insured"])
    
    # If within the limit, allocate: previous si_unscaled * distribution_assumption
    result.loc[st_within_mask]  = curves_df.loc[st_within_mask, "si_unscaled"]

    # Otherwise, allocate the remainder of the sum insured after subtracting previous si_unscaled
    curves_df["top_value"]      = np.where(pd.isna(curves_df["pml"]), curves_df["selected_sum_insured"], curves_df["pml"])
    result.loc[st_over_mask]    = curves_df.loc[st_over_mask, "selected_sum_insured"]  -  curves_df.loc[st_over_mask, "top_value"]

    # ----- OTHER categories (Deciles) -----
    other_mask          = non_blank_mask & ~curves_df["category"].isin(["Top", "Second top"])
    
    # Get the "Top" and "Second top" si_unscaled per country (using country_number as key)
    top_values          = curves_df.loc[top_mask       ].set_index("country_number")["si_unscaled"]
    second_top_values   = curves_df.loc[second_top_mask].set_index("country_number")["si_unscaled"]
    top_value           = curves_df["country_number"].map(top_values)
    second_top_value    = curves_df["country_number"].map(second_top_values)
    
    # Condition: top + second top <= selected_sum_insured
    condition           = (top_value + second_top_value) <= curves_df["selected_sum_insured"]
    
    # For each country, compute the sum of si_unscaled for the "other" (non-Top, non-Second top) rows.
    other_sum_by_country= curves_df.loc[other_mask].groupby("country_number")["si_unscaled"].sum()
    offset_sum          = curves_df["country_number"].map(other_sum_by_country)
    
    # Compute the allocation fraction only if the condition is met; otherwise use 0.
    fraction                  = pd.Series(0, index=curves_df.index)
    valid_other               = other_mask & condition
    alloc_amount              = curves_df.loc[valid_other, "selected_sum_insured"]  -  top_value[valid_other] -  second_top_value[valid_other]
    alloc_factor              = np.where(offset_sum[valid_other]==0,     0,     alloc_amount / offset_sum[valid_other])
    fraction.loc[valid_other] = curves_df.loc[valid_other, "si_unscaled"]  *  alloc_factor

    # Candidate allocation from the “Second top” part (i.e. second_top * no_in_category)
    candidate               = second_top_value * curves_df["no_in_category"]
    
    # For each "other" row, the final allocation is the minimum of the computed fraction and candidate.
    other_result            = np.minimum(fraction, candidate)
    result.loc[other_mask]  = other_result.loc[other_mask]
    
    return result



def scale_sum_insured_again(curves_df):
    # Initialize result as a Series (default NaN)
    result = pd.Series(np.nan, index=curves_df.index)

    # For rows where category is "Top": simply return si_scaled
    top_mask = curves_df["category"] == "Top"
    result.loc[top_mask] = curves_df.loc[top_mask, "si_scaled"]

    # For non-"Top" rows, apply the scaling adjustment
    non_top_mask = curves_df["category"] != "Top"

    # For each country, get the si_scaled value of the "Top" row
    top_by_country = curves_df.loc[top_mask].groupby("country_number")["si_scaled"].first()
    top_si_scaled = curves_df["country_number"].map(top_by_country)

    # For each country, sum si_scaled for non-"Top" rows
    sum_non_top = curves_df.loc[non_top_mask].groupby("country_number")["si_scaled"].sum()
    sum_non_top_mapped = curves_df["country_number"].map(sum_non_top)

    # Compute the factor:
    #   (selected_sum_insured - top_si_scaled) / (sum of si_scaled for non-Top rows for that country)
    factor = ratio(curves_df["selected_sum_insured"] - top_si_scaled, sum_non_top_mapped)

    # For non-Top rows, the adjusted si_scaled is: si_scaled * factor
    result.loc[non_top_mask] = curves_df.loc[non_top_mask, "si_scaled"] * factor.loc[non_top_mask]

    return result

def calculate_mbbefd(curves_df, b, g, bi_wait_period, pd_or_bi, main_or_sub):

    deductible_or_nil   = curves_df["deductible"].fillna(0)
    sublimit_or_nil     = curves_df["sublimit"].fillna(0)
    excess_or_nil       = curves_df["excess"].fillna(0)

    # Compute the common denominator: (si_scaled_2 / no_in_category)
    denominator         = ratio(curves_df["si_scaled_2"], curves_df["no_in_category"])
    
    # Compute the "extra" component for sub based on whether it's PD or BI
    bi_wait_ded_nil     = np.where( pd_or_bi == "bi" and bi_wait_period is not None,    0,      deductible_or_nil)


    if (main_or_sub != "main") and (main_or_sub != "sub"):
        raise ValueError("main_or_sub must be either \"main\" or \"sub\"")
        hx.errors.validation("main_or_sub must be either \"main\" or \"sub\"")

    elif main_or_sub == "main":
        # First argument for mbbefd: MIN((excess + limit) / denominator, 1)
        xs_lim          = curves_df["limit"] + excess_or_nil
        arg1            = np.minimum(       ratio(xs_lim, denominator),     1)
        result1         = mbbefd(b, g, arg1)

        # Compute the "extra" component based on whether it's PD or BI    
        condition       = (curves_df["subcoverage"] == "Liability")   |   (sublimit_or_nil == 0)
        extra           = np.where( condition,    bi_wait_ded_nil,    sublimit_or_nil)

        # Second argument for mbbefd: MIN((excess + extra) / denominator, 1)
        xs_extra        = excess_or_nil + extra
        arg2            = np.minimum(       ratio(xs_extra, denominator),   1)
        result2         = mbbefd(b, g, arg2)

        # Compute the final result - for rows where coverage is "Liability", the result is 0
        final_result    = result1 - result2
        final_result    = np.where(curves_df["coverage"] == "Liability", 0, final_result)

        return final_result


    elif main_or_sub == "sub":
        # First argument for mbbefd: MIN((excess + sublimit) / denominator, 1)
        xs_sublim       = excess_or_nil + sublimit_or_nil        
        arg1            = np.minimum(       ratio(xs_sublim, denominator),  1)
        result1         = mbbefd(b, g, arg1)

        # Second argument for mbbefd: MIN((excess + extra_sub) / denominator, 1)
        xs_extra_sub    = excess_or_nil+ bi_wait_ded_nil
        arg2            = np.minimum(   ratio(xs_extra_sub, denominator),   1)
        result2         = mbbefd(b, g, arg2)

        # Compute the final result - for rows where subcoverage is "Liability" or 0, the result is 0
        final_result    = result1 - result2
        final_result    = np.where((curves_df["subcoverage"] == "Liability")  |  (curves_df["subcoverage"] == 0),    0,   final_result)

        return final_result


    else:
        raise ValueError("main_or_sub must be either \"main\" or \"sub\"")

# ILF function
def calculate_ilf(curves_df, ilf_max, ilf_increment, ILFLimit, value_type="limit_excess", limits=["cvg_limit_usd", "cvg_excess_usd"]):
    # Determine the value to use based on the source:
    # "limit_excess" -> total = cvg_limit_usd + cvg_excess_usd
    # "excess"       -> total = cvg_excess_usd

    if value_type not in ["limit_excess","excess"]:
        raise ValueError("value_type must be either \"limit_excess\" or \"excess\"")
        hx.errors.validation("value_type must be either \"limit_excess\" or \"excess\"")
        return 


    total       = curves_df[limits[1]].copy()
    total      += curves_df[limits[0]] if value_type == "limit_excess" else 0
    
    ilf_limit   = ILFLimit["Limit"]


    # Branch 1: if total > ilf_max
    idx_max_arr = np.where(ilf_limit == ilf_max)[0]
    if len(idx_max_arr) == 0:       raise ValueError("ilf_max not found in ilf_limit")
    
    idx_max     = idx_max_arr[0]
    base_ilf    = ILFLimit.iloc[idx_max, 1]  # second column
    branch1     = base_ilf + ilf_increment * (total - ilf_max) / 1000000


    # Branch 2: else case
    rounded_up  = np.ceil( total / 1000000) * 1000000
    rounded_down= np.floor(total / 1000000) * 1000000

    # np.searchsorted with side="right" gives the insertion index; subtract 1 for approximate match
    index_up    = np.searchsorted(ilf_limit.to_numpy(), rounded_up, side="right") - 1
    index_down  = np.searchsorted(ilf_limit.to_numpy(), rounded_down, side="right") - 1
    index_up    = np.clip(index_up, 0, len(ilf_limit) - 1)
    index_down  = np.clip(index_down, 0, len(ilf_limit) - 1)

    # Extract second column values and convert to numpy arrays
    value_up    = ILFLimit.iloc[index_up, 1].to_numpy()
    value_down  = ILFLimit.iloc[index_down, 1].to_numpy()

    # Compute the fraction safely
    delta       = rounded_up - rounded_down
    fraction    = np.where(delta != 0, (total - rounded_down) / delta, 0)
    branch2     = (value_up - value_down) * fraction + value_down


    # Final result
    result = np.where(total > ilf_max, branch1, branch2)
    return result


### --- RATING --- ###

def rate_countries(hxd):
    
    # links to hx structures
    cds             = hxd.cds
    layer, cvg      = one_layer(hxd)
    sf              = hxd.cds.standard_fields
    expo            = hxd.cds.exposure.granular
    ccy_table       = params.fx_rates.df()

    # links to hx nodes
    inception_date  = hxd.hx_core.inception_date
    ccy             = hxd.cds.currencies.source_currency

    # Initialise param tables
    countries_tbl       = hx.params.countries
    IHSGroupCountry     = hx.params.IHSGroupCountry
    country_risk_tbl    = hx.params.country_risk
    BIWaitPeriod        = hx.params.BIWaitPeriod
    BIIndemnityPeriod   = hx.params.BIIndemnityPeriod
    CoverageName        = hx.params.CoverageName
    BIIHSRate           = hx.params.BIIHSRate
    PDIHSRate           = hx.params.PDIHSRate
    IHSRate             = hx.params.IHSRate
    CoverageIdentifier  = hx.params.CoverageIdentifier
    MinROL              = hx.params.MinROL
    LocationDistribution= hx.params.LocationDistribution
    LocationDeciles     = hx.params.LocationDeciles
    SalzmannB           = hx.params.SalzmannB
    ILFLimit            = hx.params.ILFLimit
    ILF                 = hx.params.ILF
    ILFBase             = hx.params.ILFBase

    # Get NMP load
    tp_dict             = tp_components(hxd, sf.benchmark_class)
    nmp_load            = tp_dict["nmp_load"]

    # Check at least one country has been input
    countries_present   = [c.country for c in expo.countries if c.country is not None]
    expo.has_at_least_one_country = countries_present != []

    # Get df with exposure
    countries_df        = pd_df_from_hx_list(expo.countries)

    # Calculate total selected sum insured
    has_total_si                        = countries_df["total_sum_insured"].notna()
    bi_pd_missing                       = pd.isna(countries_df["bi_sum_insured"]) & pd.isna(countries_df["pd_sum_insured"])
    bi_pd_sum_insured_or_nil            = pd.Series(countries_df["bi_sum_insured"].fillna(0) + countries_df["pd_sum_insured"].fillna(0))
    bi_pd_sum_insured_or_nan            = pd.Series(np.where(bi_pd_missing, np.nan,   bi_pd_sum_insured_or_nil)) 
    countries_df["selected_sum_insured"]= countries_df["total_sum_insured"].fillna( bi_pd_sum_insured_or_nan )

    # Check inputs and provide warning if needed
    check_multi_si      = (pd.notna(countries_df["total_sum_insured"])  & (  pd.notna(countries_df["bi_sum_insured"]) | pd.notna(countries_df["pd_sum_insured"])      ))
    check_missing       = (pd.notna(countries_df["no_of_locations"])    &    pd.notna(countries_df["pml"])            & pd.notna(countries_df["selected_sum_insured"]) )
    check_negatives     = (   (countries_df["no_of_locations"]      < 0)    
                            | (countries_df["bi_sum_insured"]       < 0)
                            | (countries_df["pd_sum_insured"]       < 0)
                            | (countries_df["total_sum_insured"]    < 0)
                            | (countries_df["pml"]                  < 0)
                            | (countries_df["limit"]                < 0)
                            | (countries_df["excess"]               < 0)
                            | (countries_df["sublimit"]             < 0)
                            | (countries_df["deductible"]           < 0))

    #YZ: 24/10/2025 Add country validation check
    check_countries =  (pd.notna(countries_df["country"])) & ( ~ countries_df["country"].isin(countries_tbl["Country"]))
    




    loc_one_pml_no      = ((countries_df["no_of_locations"] == 1)       & (  countries_df["pml"] != countries_df["selected_sum_insured"]))
    loc_multi_pml_yes   = ((countries_df["no_of_locations"] > 1)        & (  countries_df["pml"] == countries_df["selected_sum_insured"]))
    loc_condition       = ( check_missing &    (loc_one_pml_no | loc_multi_pml_yes))
    

    warning_multi_si    = "🔴 Please enter only Total or BI / PD Sum Insured"
    warning_tiv_loc     = "🔴 Inconsistent # Locations, Top TIV and Total TIV"
    warning_negatives   = "🔴 One, or more negative entries"
    warning_countries = "🔴 Country input is not in the dropdown list. The input is case sensitive"

    countries_df["warning"] = np.where(         check_multi_si,         warning_multi_si
                                , np.where(     loc_condition,          warning_tiv_loc
                                    , np.where( check_negatives,        warning_negatives      
                                        ,np.where(check_countries , warning_countries, ""))))



    if check_multi_si.any() or loc_condition.any() or check_negatives.any() or check_countries.any():
        expo.show_warning = True
        hx.errors.validation("Please fix the warning(s) in the Countries page.")




    #YZ: 24/10/205 Add the tidy up countries columns

    def clean_country_name(name):
        if not isinstance(name, str):
            return name #return None 
        name = name.lower()
        return ' '.join([
            word.capitalize() if word not in {'and', 'of','the'} else word
            for word in name.split()
        ])

    countries_df["country_clean"] = countries_df["country"].apply(clean_country_name)
    



    # Continue with country-level calcs
    countries_df["rated_country"]           = np.where(pd.isna(countries_df["proxy_rating_country"]),   countries_df["country"],        countries_df["proxy_rating_country"])
    countries_df["country_code_original"]   = look_up(countries_df["rated_country"], "Country", "Code", countries_tbl).replace("", np.nan)
    countries_df["country_code"]            = np.where(pd.isna(countries_df["country_code_original"]),  countries_df["rated_country"],  countries_df["country_code_original"])

    # establish if task has failed and set prompts
    refresh_prompt = "❗❗ Click on 'Refresh IHS Scores' to retrieve the risk scores for each country. ❗❗"
    has_api_failed = hxd.ihs_countries_retrieved == "failed"
    ihs_validation_msg = "Please click on 'Refresh IHS Scores' in the Countries page."


    # build a flag concatenating country coverage subcoverage
    countries_df['country_cvg_subcvg_live'] = (          countries_df['rated_country'].astype(str) 
                                                 + "&" + countries_df['coverage'     ].astype(str) 
                                                 + "&" + countries_df['subcoverage'  ].astype(str))

    # Push to hxd now so values are available to IHS fetch task even if exit directly below - this is the only push to countries list
    output_cols = ["rated_country",  "country_code_original", "country_clean" ,"country_code",  "selected_sum_insured",  "warning", 'country_cvg_subcvg_live']
    write_pd_to_hxd(countries_df, expo.countries, output_cols, replace_nan=True) 

    # if IHS scores are not present and task failed - set error message and exit
    if len(hxd.ihs) <= 1 and has_api_failed:
        expo.refresh_message = f"❌ Failed to retrieve country risk scores. Error message:\n\n{expo.ihs_api_error_msg}"
        return pd.DataFrame(), pd.DataFrame()

    # if ihs scores are not present but we have rated_country to analyse - set error message
    if (len(hxd.ihs) <= 1)  and   (~pd.isna(countries_df["rated_country"]).all()):
        # hx.errors.validation(ihs_validation_msg)
        expo.refresh_message = refresh_prompt

    # Display success message if countries retrieved match countries rated or equivalent failure message
    countries_retrieved_temp = json.loads(hxd.ihs_countries_retrieved or "[]")
    countries_retrieved_current = get_countries_retrieved(hxd, matching_key="country_cvg_subcvg_live")
    if countries_retrieved_temp == countries_retrieved_current:
        expo.refresh_message = "✅ Country risk scores successfully retrieved."
        expo.show_chart = True
    else:
        expo.refresh_message = refresh_prompt
        hx.errors.validation(ihs_validation_msg)

    ####################################
    ### --- IHS Score Adjustment --- ###
    ####################################

    # set the columns we want in roe df and source them from countries
    roe_columns = [    "rated_country",     "no_of_locations",  "attritional_risk", "geog_risk",            "location_cat_risk"
                    ,  "total_sum_insured", "bi_sum_insured",   "pd_sum_insured",   "selected_sum_insured", "coverage",         "subcoverage"
                    ,  "political",         "terrorism_raw",    "labour_strikes",   "protests_riots",       "interstate_war"
                    ,  "civil_war",         "override_war",     "override_terrorism","override_civil_unrest"]

    roe_df      = countries_df[roe_columns].copy().rename(columns = {'rated_country': 'country'})

    # Look up the coverage identifiers
    roe_df["coverage_code"]     = look_up(roe_df["coverage"],    "Coverage", "Coverage Code", CoverageName)
    roe_df["subcoverage_code"]  = look_up(roe_df["subcoverage"], "Coverage", "Coverage Code", CoverageName)
    
    cvg_cols_to_join            = ["coverage_code", "cvg_terrorism", "cvg_civil_unrest", "cvg_war", "cvg_loading"]
    subcvg_cols_to_join         = ["subcoverage_code", "subcvg_terrorism", "subcvg_civil_unrest", "subcvg_war", "subcvg_loading"]

    roe_df                      = pd.merge(roe_df, CoverageIdentifier[cvg_cols_to_join],    how="left", on="coverage_code")
    roe_df                      = pd.merge(roe_df, CoverageIdentifier[subcvg_cols_to_join], how="left", on="subcoverage_code")

    # Calculate IHS averages
    roe_df["civil_unrest"]      = roe_df[["labour_strikes", "protests_riots"]].mean(axis=1)
    roe_df["war"]               = roe_df[["interstate_war", "civil_war"]].mean(axis=1)
    roe_df["terrorism"]         = roe_df[["political", "terrorism_raw", "civil_unrest", "war"]].mean(axis=1)


    # Loop through the perils and add adjusted score for each one
    perils = ["civil_unrest", "war", "terrorism"]
    for peril in perils:
        # Check peril is covered
        roe_df[f"has_{peril}"] = (   (roe_df[f"cvg_{peril}"]).astype(bool) 
                                   | (roe_df[f"subcvg_{peril}"]).astype(bool)  )     if not roe_df.empty else False

        # Calculate UW adjusted scores
        if peril == "terrorism": # Allow previous adjustments to flow through into selected, whilst not in default- request from AC 27/6/25
            ihs_terrorism_selected_ss   = roe_df[["political", "terrorism_raw", "selected_civil_unrest", "selected_war"]].mean(axis=1)
            roe_df[f"selected_{peril}"] = roe_df[f"override_{peril}"].fillna(ihs_terrorism_selected_ss).fillna(0)                                               # notice WE USE ihs_terrorism_selected_ss NOT roe_df[peril]
            roe_df[f"{peril}_uw_adj"]   = np.where(  ihs_terrorism_selected_ss==0,  1,   roe_df[f"selected_{peril}"] / ihs_terrorism_selected_ss.fillna(0)  )   # notice WE USE ihs_terrorism_selected_ss NOT roe_df[peril]
        else:
            roe_df[f"selected_{peril}"] = roe_df[f"override_{peril}"].fillna(roe_df[peril]).fillna(0)
            roe_df[f"{peril}_uw_adj"]   = np.where(  roe_df[peril]==0,  1,   roe_df[f"selected_{peril}"] / roe_df[peril].fillna(0)  )

        # Lookup values for ROE calculations
        c_values_calculated     = look_up_closest(  roe_df[peril],                "ihs_score", f"{peril}_c", IHSRate, if_not_found=0)
        b_values_calculated     = look_up_closest(  roe_df[peril],                "ihs_score", f"{peril}_b", IHSRate, if_not_found=0)
        c_values_selected       = look_up_closest(  roe_df[f"selected_{peril}"],  "ihs_score", f"{peril}_c", IHSRate, if_not_found=0)
        b_values_selected       = look_up_closest(  roe_df[f"selected_{peril}"],  "ihs_score", f"{peril}_b", IHSRate, if_not_found=0)

        # Calculate ROE
        roe_df[f"{peril}_roe_calculated"]   = c_values_calculated     * np.exp(b_values_calculated  * roe_df[peril])               * roe_df[f"has_{peril}"].astype(int)
        roe_df[f"{peril}_roe_selected"]     = c_values_selected       * np.exp(b_values_selected    * roe_df[f"selected_{peril}"]) * roe_df[f"has_{peril}"].astype(int)

        # Record countries not covered
        countries_not_covered               = roe_df.loc[roe_df[f"has_{peril}"] == False, "country"].tolist()

        # Add info if peril is not covered
        peril_info = f"{title_rc(peril)} not covered for {', '.join(filter(None, countries_not_covered))}. ROE defaulting to 0." if countries_not_covered else None
        setattr(expo, f"{peril}_info", peril_info)

        # Check UW adjustment is valid
        invalid_msg = "All adjustments must be between 50% and 200% (inclusive)."
        if any((roe_df[f"{peril}_uw_adj"] > 2) | (roe_df[f"{peril}_uw_adj"] < 0.5)):
            setattr(expo, f"{peril}_uw_adj_info", invalid_msg)
            setattr(expo, f"{peril}_uw_adj_invalid", True)
        else:
            setattr(expo, f"{peril}_uw_adj_valid", True)




    ################################
    ### --- ROE Calculations --- ###
    ################################

    # load values from hxd for analysis
    bi_wait_period      = hxd.cds.exposure.aggregate.details.bi_wait_period
    bi_indemnity_period = hxd.cds.exposure.aggregate.details.bi_indemnity_period
    contingent_bi       = hxd.cds.exposure.aggregate.details.contingent_bi

    
    # determine scalar multipliers for bi_wait_period & bi_indemnity_period if one has been specified, calculating overall bi_multiplier and writing down to cds
    if bi_indemnity_period is not None: 
        bi_indemnity_period_min  = BIIndemnityPeriod["BI Indemnity Period"].min()
        bi_indemnity_period_max  = BIIndemnityPeriod["BI Indemnity Period"].max()
        bi_indemnity_period      = np.clip(bi_indemnity_period,        bi_indemnity_period_min,     bi_indemnity_period_max)
        
        if bi_indemnity_period == bi_indemnity_period_min or bi_indemnity_period == bi_indemnity_period_max:
            bi_indem_mult            = BIIndemnityPeriod[  BIIndemnityPeriod["BI Indemnity Period"] == bi_indemnity_period  ]["Rate"].iat[0]
        else:
            bi_indem_mult            = linear_interp(BIIndemnityPeriod["BI Indemnity Period"],   BIIndemnityPeriod["Rate"],  bi_indemnity_period)       
    else:
        bi_indem_mult            = 1


    if bi_wait_period is not None: 
        bi_wait_period_min  = BIWaitPeriod["BI Wait Period"].min()
        bi_wait_period_max  = BIWaitPeriod["BI Wait Period"].max()
        bi_wait_period      = np.clip(bi_wait_period,        bi_wait_period_min,     bi_wait_period_max)
        
        if bi_wait_period == bi_wait_period_min or bi_wait_period == bi_wait_period_max:
            bi_wait_mult            = BIWaitPeriod[  BIWaitPeriod["BI Wait Period"] == bi_wait_period  ]["Rate"].iat[0]
        else:
            bi_wait_mult            = linear_interp(BIWaitPeriod["BI Wait Period"],   BIWaitPeriod["Rate"],  bi_wait_period)       
    else:
        bi_wait_mult        = 1


    expo.bi_multiplier  = bi_wait_mult * bi_indem_mult * (1 + contingent_bi * cbi_load)


    # calculate number of rows of country data and write to cds
    expo.no_of_countries= roe_df.shape[0]

    # calculate vector of multipliers for attritional_risk, geog_risk, location_cat_risk by country and store in df as risk_multiplier
    attr_mult                   = look_up(roe_df["attritional_risk"],   "Attr Risk", "Attr Multiplier", country_risk_tbl)
    geog_mult                   = look_up(roe_df["geog_risk"],          "Geog Risk", "Geog Multiplier", country_risk_tbl)
    cat_mult                    = look_up(roe_df["location_cat_risk"],  "Cat Risk",  "Cat Multiplier",  country_risk_tbl)
    roe_df["risk_multiplier"]   = attr_mult * geog_mult * cat_mult


    # Helper function to return a dictionary of perils, each with a list of names for both b and c parameters contemplating peril and coverage
    def ihs_cols(cvg="bi"):
        return {
            "civil_unrest": [f"{cvg}_civil_unrest_c",   f"{cvg}_civil_unrest_b"],
            "war":          [f"{cvg}_war_c",            f"{cvg}_war_b"],
            "terrorism":    [f"{cvg}_terrorism_c",      f"{cvg}_terrorism_b"]
        }

    # Looks up b & c parameters for each country (vectorised),      each coverage = cvg in ["bi", "pd"],    and each ihs peril
    for table, cvg in zip([BIIHSRate, PDIHSRate], ["bi", "pd"]):
        for risk, cols in ihs_cols(cvg).items():
            roe_df = merge_ihs_rates(roe_df, table, risk, "ihs_score", cols)

    # calculates roe (country vectorised) for  each coverage = cvg in ["bi", "pd"],    and each ihs peril = risk
    # contemplates b & C parameters, risk_multiplier and any bi_multiplier if relevant
    for cvg in ["bi", "pd"]:
        risk_multiplier = roe_df["risk_multiplier"] * (expo.bi_multiplier if cvg=="bi" else 1)
        for risk in ihs_cols(cvg).keys():
            b                           = roe_df[f"{cvg}_{risk}_b"]
            c                           = roe_df[f"{cvg}_{risk}_c"]
            roe_df[f"{cvg}_{risk}_roe"] = risk_multiplier   *   c   *   np.exp( b   *   roe_df[risk])

    # helper calc for next step conditioning on if sum insured is empty use nil
    bi_si_or_nil    = roe_df["bi_sum_insured"].fillna(0)
    pd_si_or_nil    = roe_df["pd_sum_insured"].fillna(0)

    # calculates roe (country vectorised) for each ihs peril = risk
    # contemplates b & C parameters, risk_multiplier, any bi_multiplier if relevant, composition between pd & bi
    for risk in ihs_cols().keys():
        bi_roe_or_nil   = roe_df[f"bi_{risk}_roe"].fillna(0)
        pd_roe_or_nil   = roe_df[f"pd_{risk}_roe"].fillna(0)
        fallback        = bi_roe_or_nil * bi_weighting   +   pd_roe_or_nil * (1 - bi_weighting)
        numerator       = bi_roe_or_nil * bi_si_or_nil   +   pd_roe_or_nil * pd_si_or_nil
        denominator     = bi_si_or_nil + pd_si_or_nil
        roe_df[f"selected_{risk}_roe"] = np.where( denominator == 0,    fallback,   ratio(numerator, denominator)  )


    # calculate overall ihs average score Default
    roe_df["ihs_average_default"] = np.where(
        roe_df[["cvg_terrorism", "cvg_civil_unrest", "cvg_war"]].sum(axis=1) == 0,
        roe_df[["terrorism", "civil_unrest", "war"]].mul(roe_df[["subcvg_terrorism", "subcvg_civil_unrest", "subcvg_war"]].values).max(axis=1),
        roe_df[["terrorism", "civil_unrest", "war"]].mul(roe_df[["cvg_terrorism", "cvg_civil_unrest", "cvg_war"]].values).max(axis=1)
    )


    # calculate overall ihs average score Selected
    roe_df["ihs_average_selected"] = np.where(
        roe_df[["cvg_terrorism", "cvg_civil_unrest", "cvg_war"]].sum(axis=1) == 0,
        roe_df[["selected_terrorism", "selected_civil_unrest", "selected_war"]].mul(roe_df[["subcvg_terrorism", "subcvg_civil_unrest", "subcvg_war"]].values).max(axis=1),
        roe_df[["selected_terrorism", "selected_civil_unrest", "selected_war"]].mul(roe_df[["cvg_terrorism", "cvg_civil_unrest", "cvg_war"]].values).max(axis=1)
    ) 



    # calculates non liability (nl) ... and non construction roe (country vectorised) 
    # for each (i) Coverage = cvg in ["bi", "pd", "selected"]:;  (ii) Basis = c in ["cvg", "subcvg"]:
    # aggregates previously derived roe scores at a peril level, weighting oon if included (wgt_matrix), and any given loading
    for cvg in ["bi", "pd", "selected"]:
        for c in ["cvg", "subcvg"]:
            cvg_name    = cvg                if cvg != "selected"   else "total"
            cvg_col     = roe_df["coverage"] if c == "cvg"          else roe_df["subcoverage"]
            
            condition   = cvg_col == "Liability"
            roe_matrix  = roe_df[[f"{cvg}_terrorism_roe",   f"{cvg}_civil_unrest_roe",  f"{cvg}_war_roe"]]
            wgt_matrix  = roe_df[[f"{c}_terrorism",         f"{c}_civil_unrest",        f"{c}_war"]      ].values
            wgt_roe     = roe_df[f"{c}_loading"] * roe_matrix.mul(  wgt_matrix ).max(axis=1)

            roe_df[f"{cvg_name}_{c}_nl_roe"] = np.where(condition, 0, wgt_roe)


    # calculates multiplier by basis = c in ["cvg", "subcvg"]
    # contemplates previously derived overall risk multiplier, loading by basis, and any loading for bi on its constituent proportion
    bi_weight       = np.where((bi_si_or_nil + pd_si_or_nil) == 0,  bi_weighting,    bi_si_or_nil /    (bi_si_or_nil + pd_si_or_nil))
    for c in ["cvg", "subcvg"]:
        loading                     = roe_df[f"{c}_loading"]
        roe_df[f"{c}_multiplier"]   = roe_df["risk_multiplier"]  * loading *     (1   +     (expo.bi_multiplier - 1) * bi_weight)

    # gets minimum rol for liab & nl by country (vectorised) allowing for if it is us or non-us
    us_min_rol              = look_up("US",     "Country", "UW Multiplier", MinROL, 0,  "single")
    non_us_min_rol          = look_up("Non US", "Country", "UW Multiplier", MinROL, 0,  "single")
    min_rol                 = np.where(roe_df["country"]=="US", us_min_rol, non_us_min_rol) 
    roe_df["nl_min_rol"]    = np.where(roe_df["coverage"]=="Liability", 0, min_rol)
    roe_df["liab_min_rol"]  = np.where(roe_df["coverage"]!="Liability", 0, min_rol)


    # gets minimum rol for liab & nl OVERALL and writes to hxd
    total_sum_insured       = roe_df["selected_sum_insured"].sum()
    total_nl_si_x_rol       = (roe_df["nl_min_rol"]   * roe_df["selected_sum_insured"]).sum(skipna=True) or 0       # unclear why we are multiplying a rol to sum_insured, but looks to be just weighting so probably ok
    total_liab_si_x_rol     = (roe_df["liab_min_rol"] * roe_df["selected_sum_insured"]).sum(skipna=True) or 0       # unclear why we are multiplying a rol to sum_insured, but looks to be just weighting so probably ok
    expo.wa_nl_min_rol      = ratio(total_nl_si_x_rol,   total_sum_insured, 0)
    expo.wa_liab_min_rol    = ratio(total_liab_si_x_rol, total_sum_insured, 0)
    

     


    ########################################################################
    ## ADDITIONAL FUNCTIONALITY REQUESTED BY UW JUNE 30, 2025 - 
    ########################################################################
    # calculate leading peril
    roe_df["leading_peril_amt"] = np.where(roe_df[["cvg_terrorism", "cvg_civil_unrest", "cvg_war"]].sum(axis=1) == 0, roe_df["pd_subcvg_nl_roe"], roe_df["pd_cvg_nl_roe"])
    roe_df["leading_peril"]     = np.where(         roe_df["leading_peril_amt"] == roe_df["pd_terrorism_roe"],    "Terrorism"
                                    ,np.where(      roe_df["leading_peril_amt"] == roe_df["pd_civil_unrest_roe"], "Civil Unrest"
                                        ,np.where(  roe_df["leading_peril_amt"] == roe_df["pd_war_roe"],          "War",           np.nan)))
    roe_df["leading_peril"]     = roe_df["leading_peril"].fillna("Unknown") 

    # calculate TIV %
    total_sum_insured                           =   roe_df["selected_sum_insured"].sum()
    roe_df["selected_sum_insured_contribution"] = ( roe_df["selected_sum_insured"]  /  total_sum_insured   if total_sum_insured != 0 else 1)
    

    ##########################################
    ### --- Chart of historical values --- ###
    ##########################################
    full_ihs_df = pd_df_from_hx_list(hxd.ihs)

    if expo.selected_country and full_ihs_df.shape[0] >= 1:
        # Show message if region selected
        country_groups              = set(IHSGroupCountry["group"].unique())
        expo.show_country_message   = True if expo.selected_country in country_groups else False

        # Get selected country code
        selected_country            = look_up(expo.selected_country, "Country", "Code", countries_tbl, lookup_type="single")
        
        # filter ihs data to just selected country giving selected_country_ihs_df
        selected_country_ihs_df     = full_ihs_df[(full_ihs_df["country_code"]==selected_country)]
        ihs_descriptions            = []

        for node, risk_name in ihs_risk_names.items():
            # filter ihs data for selected country to just be 1 of the 6 available ihs risks giving ihs_df
            ihs_df = selected_country_ihs_df[(full_ihs_df["risk_name"]==risk_name)]

            # if ihs_df is empty goto next ihs risk
            if ihs_df.empty:
                continue
            
            # write historic values for selected country and given peril to hxd for charting
            setattr(hxd, f"ihs_{node}", ihs_df.to_dict("records"))

            # Get latest descriptions
            ihs_df["updated_on"]    = pd.to_datetime(ihs_df["updated_on"])
            description             = ihs_df.loc[ihs_df["updated_on"].idxmax(), "description"] or "N/A"
            description             = description.removeprefix("Score affirmation: ")
            ihs_description         = {"risk_name": risk_name, "description": description}
            ihs_descriptions.append(ihs_description)

        # write determined ihs descriptions to hxd
        hxd.ihs_descriptions = ihs_descriptions


    #################################################
    ### Push to hxd
    #################################################

    # resetting index so we push to correct places
    roe_df.reset_index(drop=True, inplace=True)


    ## pushing values to countries list
    ####################################
    
    # identifying main columns
    countries_cols  = [col for peril in perils
                              for col in [      peril,                      f"selected_{peril}",        f"{peril}_uw_adj"
                                            ,   f"{peril}_roe_calculated",  f"{peril}_roe_selected",    f"has_{peril}"     ]]
    countries_cols += ["leading_peril", "selected_sum_insured_contribution"]

    # pushing to countries list
    write_pd_to_hxd(roe_df, expo.countries, countries_cols, replace_nan=True)


    ## pushing values to roe list
    ##################################
       
    # identify all columns that are NOT required to be written to roe list
    basic_columns_todrop    = [     "political",        "terrorism_raw",    "labour_strikes"
                                ,   "protests_riots",   "interstate_war",   "civil_war"
                                ,   "leading_peril_amt","leading_peril",    "selected_sum_insured_contribution"]
    other_columns_todrop    = [ col for peril in perils    
                                        for col in [f"{peril}_uw_adj",          f"override_{peril}",     f"selected_{peril}",    
                                                    f"{peril}_roe_calculated",  f"{peril}_roe_selected", f"has_{peril}"         ]] # cant use countries_cols above as that includes peril which we still want to keep
    all_columns_todrop      = basic_columns_todrop + other_columns_todrop
    export_columns  = [col for col in roe_df.columns if col not in (all_columns_todrop)]
    
    # converting to object allows df to contain Nones (unlike pandas NaN) so we can flick to dictionary
    roe_df          = roe_df.astype(object).where(pd.notnull(roe_df), None)                                     
    
    # writes all of df to hxd by converting to dictionary allows to pass an object
    expo.roe        = roe_df[export_columns].to_dict("records")      


    ################################################
    ### --- Expanded Calcs (Exposure Curves) --- ###
    ################################################
    curves = []

    # builds curves_df by setting up a list of relevant information from expo.countries and converting to df
    for idx, c in enumerate(expo.countries):
        for i in range(0, 12):
            curves.append({
                "index":                idx, # For merging purposes
                "country_number":       idx + 1,
                "location_number":      i + 1,
                "country":              c.rated_country,
                "pml":                  c.pml or np.nan,
                "coverage":             c.coverage,
                "limit":                c.limit or np.nan,
                "excess":               c.excess or np.nan,
                "subcoverage":          c.subcoverage,
                "sublimit":             c.sublimit or np.nan,
                "deductible":           c.deductible or np.nan,
                "total_sum_insured":    c.total_sum_insured or np.nan,
                "bi_sum_insured":       c.bi_sum_insured or np.nan,
                "pd_sum_insured":       c.pd_sum_insured or np.nan,
                "selected_sum_insured": c.selected_sum_insured or np.nan,
                "liability_risk":       c.liability_risk,
                "attritional_risk":     c.attritional_risk,
                "geog_risk":            c.geog_risk,
                "location_cat_risk":    c.location_cat_risk,
            })

    curves_df = pd.DataFrame(curves)
    
    # appends to curves_df the no_of_locations from roe_df
    roe_df['index']                 = roe_df.index.values
    curves_df["no_of_locations"]    = look_up(curves_df["index"],         "index", "no_of_locations", roe_df)

    # builds loc_dist_dedup_df by deduplicates the equivalent parameter table (Location Distribution)
    loc_dist_dedup_df               = LocationDistribution[["no_of_locations", "band"]].drop_duplicates() 

    # for each curves_df row (vectorised) finds closest no_of_locations in loc_dist_dedup_df and calls it closest_loc
    curves_df["closest_loc"]        = find_closest(loc_dist_dedup_df,       "no_of_locations", curves_df["no_of_locations"])

    # sources band and category for curves_df (vectorised) using lookups on loc_dist_dedup_df and LocationDeciles
    curves_df["band"]               = look_up(curves_df["closest_loc"],     "no_of_locations", "band",     loc_dist_dedup_df)
    curves_df["category"]           = look_up(curves_df["location_number"], "location_number", "category", LocationDeciles)

    # curves_df["no_of_locations"] is a repeating vector of numbers from 1 to 12 for the number of locations i.e. 6 locations the complete vector will be 6 lots of 1...12 stacked vertically
    # in that repeating vector of 12 the first and second item are top and "second top" respectively
    # the step below assigns a value of 1 to 10 (deciles) for the remaining 10 values in the repeating vector and calls it "kth_smallest"
    condition                       = (curves_df["category"] == "Top") | (curves_df["category"] == "Second top")
    otherwise                       = np.minimum(   curves_df["no_of_locations"] + 1 - curves_df["location_number"]
                                                  , 13 - curves_df["location_number"])                                  
    curves_df["kth_smallest"]       = np.where(condition,     np.nan,    otherwise)

    num_loc_arr                     = curves_df["no_of_locations"]
    
    # highest value
    top_one                         = 1
    
    # second highest value
    top_second_condition            = (num_loc_arr > 10) & (num_loc_arr < 20)
    top_second_response             = np.maximum(0,     num_loc_arr / 10 - 1)
    top_second                      = np.where(top_second_condition,    top_second_response,    1)

    # decile 1 but not top 2 values
    decile_one_condition            = num_loc_arr <= 10
    decile_one_otherwise            = np.maximum(0,     num_loc_arr / 10 - 2)
    decile_one                      = np.where( decile_one_condition,   1,      decile_one_otherwise)

    # not decile 1
    not_decile_one                  = np.where(num_loc_arr <= 10,   1,  num_loc_arr / 10)

    # no in category
    curves_df["no_in_category"]     = np.where(         curves_df["category"] == "Top",         top_one
                                        ,np.where(      curves_df["category"] == "Second top",  top_second
                                            ,np.where(  curves_df["category"] == "Decile 1",    decile_one,    not_decile_one))) 

    decile_condition                = curves_df["category"].isin(["Top", "Second top"])
    denom = np.minimum(curves_df["no_of_locations"], 10)
    decile_otherwise = np.where(
        denom > 0,
        np.round(curves_df["kth_smallest"] / denom - 0.1, 1),
        np.nan)
    curves_df["decile"] = np.where(decile_condition, np.nan, decile_otherwise)

    # decile_otherwise                = np.round(curves_df["kth_smallest"] / np.minimum(curves_df["no_of_locations"], 10) - 0.1, 1)
    # curves_df["decile"]             = np.where(decile_condition,    np.nan,     decile_otherwise)

    curves_df["band_decile"]        = curves_df["band"].astype(str) + "_" + curves_df["decile"].astype(str)
    curves_df["distribution_assumption"] = look_up(curves_df["band"].astype(str) + "_Assumption", "band_decile", "value", LocationDistribution)



    curves_df['top_value']          = curves_df["pml"].fillna(  curves_df["selected_sum_insured"]  )
    curves_df['decile_dist_assump'] = look_up(curves_df["band_decile"], "band_decile", "value", LocationDistribution)
    curves_df["si_unscaled"]        = np.where(         curves_df["category"] == "Top",             curves_df['top_value']
                                        , np.where(     curves_df["category"] == "Second top",      curves_df['top_value']      * curves_df["distribution_assumption"]
                                            ,                                                       curves_df["no_in_category"] * curves_df["pml"] * curves_df['decile_dist_assump'] ))
    curves_df["si_scaled"]          = scale_sum_insured(curves_df)
    curves_df["si_scaled_2"]        = scale_sum_insured_again(curves_df)

    roe_col_names   = ["index", "bi_cvg_nl_roe", "bi_subcvg_nl_roe", "pd_cvg_nl_roe", "pd_subcvg_nl_roe"]
    curves_df       = pd.merge( curves_df,  roe_df[roe_col_names],        how="left",        on="index"    )                    # joining on index as joining on country was erroring where the same country was used multiple times

    bi_si_or_nil    = curves_df["bi_sum_insured"].fillna(0)     # notice this variable has been repurposed to refer to curves, unlike earlier on roe
    pd_si_or_nil    = curves_df["pd_sum_insured"].fillna(0)     # notice this variable has been repurposed to refer to curves, unlike earlier on roe


    curves_df["bi_weighting"]   = ratio(bi_si_or_nil,     bi_si_or_nil + pd_si_or_nil,     if_undefined=np.nan)
    curves_df["pd_weighting"]   = ratio(pd_si_or_nil,     bi_si_or_nil + pd_si_or_nil,     if_undefined=np.nan)
    bi_weight                   = curves_df["bi_weighting"].fillna(     bi_weighting )
    pd_weight                   = curves_df["pd_weighting"].fillna( 1 - bi_weighting )

    curves_df["cvg_bi_rate_si"]     = curves_df["bi_cvg_nl_roe"]    * curves_df["si_scaled_2"] * bi_weight
    curves_df["cvg_pd_rate_si"]     = curves_df["pd_cvg_nl_roe"]    * curves_df["si_scaled_2"] * pd_weight
    curves_df["subcvg_bi_rate_si"]  = curves_df["bi_subcvg_nl_roe"] * curves_df["si_scaled_2"] * bi_weight
    curves_df["subcvg_pd_rate_si"]  = curves_df["pd_subcvg_nl_roe"] * curves_df["si_scaled_2"] * pd_weight


    # MBBEFD calculations - Non-Liability - COVERAGE LEVEL
    b = SalzmannB["b"].iloc[0]
    g = SalzmannB["g"].iloc[0]

    curves_df["cvg_bi_mbbefd"]       = calculate_mbbefd(curves_df, b, g, bi_wait_period, "bi", "main")
    curves_df["cvg_pd_mbbefd"]       = calculate_mbbefd(curves_df, b, g, bi_wait_period, "pd", "main")
    selected_cvg_bi_mbbefd           = np.where(bi_wait_period is None,  curves_df["cvg_pd_mbbefd"],  curves_df["cvg_bi_mbbefd"])
    curves_df["cvg_bi_base_premium"] = curves_df["cvg_bi_rate_si"] * selected_cvg_bi_mbbefd     * (1 + nmp_load)         
    curves_df["cvg_pd_base_premium"] = curves_df["cvg_pd_rate_si"] * curves_df["cvg_pd_mbbefd"] * (1 + nmp_load)
 
    
    # MBBEFD calculations - Non-Liability - SUB-COVERAGE LEVEL
    curves_df["subcvg_bi_mbbefd"]       = calculate_mbbefd(curves_df, b, g, bi_wait_period, "bi", "sub")
    curves_df["subcvg_pd_mbbefd"]       = calculate_mbbefd(curves_df, b, g, bi_wait_period, "pd", "sub")
    selected_subcvg_bi_mbbefd           = np.where(bi_wait_period is None,  curves_df["subcvg_pd_mbbefd"],  curves_df["subcvg_bi_mbbefd"])
    curves_df["subcvg_bi_base_premium"] = curves_df["subcvg_bi_rate_si"] * selected_subcvg_bi_mbbefd     * (1 + nmp_load)
    curves_df["subcvg_pd_base_premium"] = curves_df["subcvg_pd_rate_si"] * curves_df["subcvg_pd_mbbefd"] * (1 + nmp_load)


    # ILF Calculations - Liability - COVERAGE LEVEL
    for col_1, col_2 in zip(["limit", "excess", "sublimit"], ["cvg_limit_usd", "cvg_excess_usd", "subcvg_sublimit_usd"]):
        curves_df[col_2] = usd(curves_df[col_1], pd.Series([ccy] * len(curves_df), index=curves_df.index), lookup_type="array")

    ilf_max                     = ILF[ILF["ILF"]=="MaxValue"]["Value"].iloc[0]
    ilf_increment               = ILF[ILF["ILF"]=="Increment"]["Value"].iloc[0]
    

    curves_df["cvg_ilf_upper"]  = calculate_ilf(curves_df, ilf_max, ilf_increment, ILFLimit, "limit_excess")
    curves_df["cvg_ilf_lower"]  = calculate_ilf(curves_df, ilf_max, ilf_increment, ILFLimit, "excess")
    curves_df["liab_risk_value"]= look_up(curves_df["liability_risk"], "Risk", "Value", ILFBase)
    
    cvg_liab_condition                  = (curves_df["coverage"] == "Liability")   &   (curves_df["category"] == "Top")
    cvg_liab_response                   = (curves_df["cvg_ilf_upper"] - curves_df["cvg_ilf_lower"])    * curves_df["liab_risk_value"] * (1 + nmp_load)
    curves_df["cvg_liab_base_premium"]  = np.where(cvg_liab_condition, cvg_liab_response, 0)


    # ILF Calculations - Liability - SUB-COVERAGE LEVEL
    curves_df["subcvg_ilf_upper"]       = calculate_ilf(curves_df, ilf_max, ilf_increment, ILFLimit, "limit_excess",  ["subcvg_sublimit_usd", "cvg_excess_usd"])
    subcvg_liab_condition               = (curves_df["subcoverage"] == "Liability")   &   (curves_df["category"] == "Top")
    subcvg_liab_response                = (curves_df["subcvg_ilf_upper"] - curves_df["cvg_ilf_lower"]) * curves_df["liab_risk_value"] * (1 + nmp_load)
    curves_df["subcvg_liab_base_premium"]=np.where(subcvg_liab_condition,   subcvg_liab_response,   0)


    # Final trapped exposure
    ded_or_nil_series   = curves_df["deductible"].fillna(0)
    min_series          = pd.Series(0, index=curves_df.index)
    max_series          = curves_df["limit"] - ded_or_nil_series
    calc_series         = ratio(  curves_df["si_scaled_2"],   curves_df["no_in_category"])      - ded_or_nil_series
    median_series       = pd.concat(  [min_series, max_series, calc_series]  , axis=1).median(axis=1)
    curves_df["trapped_exposure"] = curves_df["no_in_category"] * median_series

    # Summary
    expo.fx_to_usd              = look_up(ccy, "ccy", "fx_rate", ccy_table, if_not_found=1, lookup_type="single")
    expo.trapped_exposure       = curves_df["trapped_exposure"].sum()
    expo.limit_ded_difference   = (cds.exposure.aggregate.policy_limit or 0) - (cds.exposure.aggregate.policy_deductible or 0)
    expo.expo_limit_ratio       = ratio(expo.trapped_exposure,  expo.limit_ded_difference)

    # Push to hxd
    curves_df.drop(columns=[
        "band_decile", 
        "distribution_assumption", 
        "bi_weighting", 
        "pd_weighting",
        "liab_risk_value",
        "top_value",
        "decile_dist_assump",
        "closest_loc"
    ], inplace=True)

    curves_df = curves_df.replace([np.inf, -np.inf], np.nan)
    curves_df = curves_df.astype(object).where(pd.notnull(curves_df), None)
    expo.curves = curves_df.to_dict("records")

    # curves_df   = curves_df.astype(object).where(pd.notnull(curves_df), None)
    # expo.curves = curves_df.to_dict("records")

    return roe_df, curves_df














