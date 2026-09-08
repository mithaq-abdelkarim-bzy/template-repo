import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import ratio, one_layer, pd_df_from_hx_list, write_pd_to_hxd
from algorithms.rate_utilities import look_up, look_up_closest, look_up_with_bounds, usd, to_ccy, policy_term
from algorithms.rate_constants import benchmark_lr
from algorithms.rate_ux import fill_check_columns, validate_table
from algorithms.data_schema.sch_rater_defined import airlines_validation_cols
from scipy.stats import beta

### --- PARAM TABLES --- ###
AttritionalLoad = hx.params.al_AttritionalLoad
BuildYearFreq = hx.params.al_BuildYearFreq
BuildYearSev = hx.params.al_BuildYearSev
FleetDiscountParameter = hx.params.al_FleetDiscountParameter
HullBaseFreq = hx.params.al_HullBaseFreq
HullBaseSev = hx.params.al_HullBaseSev
HullExposure = hx.params.al_HullExposure
HullFreqBuildYear = hx.params.al_HullFreqBuildYear
HullFreqClass = hx.params.al_HullFreqClass
HullFreqPrev12monthshours = hx.params.al_HullFreqPrev12monthshours
HullFreqRegion = hx.params.al_HullFreqRegion
HullFreqStatus = hx.params.al_HullFreqStatus
HullFreqUsage = hx.params.al_HullFreqUsage
HullSevBuildYear = hx.params.al_HullSevBuildYear
HullSevClass = hx.params.al_HullSevClass
HullSevOperatingMTOW = hx.params.al_HullSevOperatingMTOW
HullSevPrevious12monthshours = hx.params.al_HullSevPrevious12monthshours
HullSevRussianBuild = hx.params.al_HullSevRussianBuild
ILFParam = hx.params.al_ILFParam
ILFTable = hx.params.al_ILFTable
LiabBaseFreq = hx.params.al_LiabBaseFreq
LiabFreqBuildYearNumeric = hx.params.al_LiabFreqBuildYearNumeric
LiabFreqClass = hx.params.al_LiabFreqClass
LiabFreqPrev12monthshours = hx.params.al_LiabFreqPrev12monthshours
LiabFreqRegion = hx.params.al_LiabFreqRegion
LiabFreqStatus = hx.params.al_LiabFreqStatus
LiabFreqUsage = hx.params.al_LiabFreqUsage
LiabSeverity = hx.params.al_LiabSeverity
LowValue = hx.params.al_LowValue
OperatorClass = hx.params.al_OperatorClass
OperatorTLOGroup = hx.params.al_OperatorTLOGroup
PLLAdditionalTPCover = hx.params.al_PLLAdditionalTPCover
PLLAwards = hx.params.al_PLLAwards
StatusMapping = hx.params.al_StatusMapping
TLOFreqAdjustment = hx.params.al_TLOFreqAdjustment
TPLFleetSizeDiscount = hx.params.al_TPLFleetSizeDiscount
TPLLimitsRates = hx.params.al_TPLLimitsRates
TPLMisc = hx.params.al_TPLMisc
UsageMapping = hx.params.al_UsageMapping
OperatorCountryList = hx.params.OperatorCountryList

### --- HELPER FUNCTIONS --- ###

def get_countries(hxd, ac):
    OperatorCountryList = hx.params.OperatorCountryList
    cirium_region = look_up(ac.operator_region, "Region Airlines", "Region", OperatorCountryList, if_not_found="N/A", lookup_type="single")
    
    if cirium_region == "N/A":
        countries_df = OperatorCountryList.rename(columns={"Country": "country"})
    else:
        countries_df = OperatorCountryList[OperatorCountryList["Region"] == cirium_region].rename(columns={"Country": "country"})
    
    ac.countries = countries_df[["country"]].to_dict("records")


def calculate_status_rel(status_split, airlines_df, freq_status_table, use_time_in_service=False):
    in_service = status_split.get("in_service")
    storage = status_split.get("storage")
    other = status_split.get("other")
    status_split_present = in_service is not None or storage is not None or other is not None

    if status_split_present:
        status_rel_in_service = (in_service or 0) * look_up("In Service", "Status", "Parameter", freq_status_table, lookup_type="single")
        status_rel_storage = (storage or 0) * look_up("Storage", "Status", "Parameter", freq_status_table, lookup_type="single")
        status_rel_other = (other or 0) * look_up("Other", "Status", "Parameter", freq_status_table, lookup_type="single")
        status = status_rel_in_service + status_rel_storage + status_rel_other
    else:
        if use_time_in_service:
            # Hull case: include time_in_service calculations
            status_rel_in_service = airlines_df["time_in_service"] * look_up("In Service", "Status", "Parameter", freq_status_table, lookup_type="single")
            status_rel_storage = (1 - airlines_df["time_in_service"]) * look_up("Storage", "Status", "Parameter", freq_status_table, lookup_type="single")
            status_rel = status_rel_in_service + status_rel_storage

            status = np.where(
                pd.to_numeric(airlines_df["time_in_service"], errors="coerce").notnull(),
                status_rel,
                look_up(airlines_df["aircraft_status"], "Status", "Parameter", freq_status_table, if_not_found=np.nan)
            )
        else:
            # Liability case: directly perform lookup using 'aircraft_status'
            status = look_up(airlines_df["aircraft_status"], "Status", "Parameter", freq_status_table, if_not_found=np.nan)

    return status


def calculate_ilf_point(airlines_df, point_type):    
    # Validate point_type
    if point_type not in ["limit", "attachment"]:
        raise ValueError("point_type must be either 'limit' or 'attachment'")
    
    # Extract ILF Parameter Values
    ILFParamA = look_up("ILF Parameter A", "Parameter", "Value", ILFParam, lookup_type="single").astype(float)
    ILFParameterB = look_up("ILF Parameter B", "Parameter", "Value", ILFParam, lookup_type="single").astype(float)
    ILFCap = look_up("ILF Cap", "Parameter", "Value", ILFParam, lookup_type="single").astype(float)
    
    # Calculate the Sum or Direct Value Based on point_type
    if point_type == "limit":
        sum_limit = airlines_df["liability_limit_usd"] + airlines_df["liability_excess_usd"]
    elif point_type == "attachment":
        sum_limit = airlines_df["liability_excess_usd"]
    
    # Determine if sum_limit exceeds or equals ILFCap
    condition = sum_limit >= ILFCap
    
    # Calculate the True Condition Value - handle cases where sum_limit might be zero or negative to avoid taking log of non-positive numbers
    with np.errstate(divide="ignore", invalid="ignore"):
        value_if_true = ILFParamA * np.log(sum_limit) + ILFParameterB
        value_if_true = pd.Series(value_if_true).replace([np.inf, -np.inf], np.nan).values
    
    # Find the matched_limit and matched_ILF
    matched_limit = look_up_closest(sum_limit, "Limit", "Limit", ILFTable)
    matched_ILF = look_up_closest(sum_limit, "Limit", "ILF", ILFTable)
    
    # Prepare ILFTable with next_Limit and next_ILF for interpolation
    ILFTable_sorted = ILFTable.sort_values("Limit").reset_index(drop=True).copy()
    ILFTable_sorted["Next_Limit"] = ILFTable_sorted["Limit"].shift(-1)
    ILFTable_sorted["Next_ILF"] = ILFTable_sorted["ILF"].shift(-1)
    
    # Find the next_Limit and next_ILF based on matched_limit
    matched_next_limit = look_up_closest(matched_limit, "Limit", "Next_Limit", ILFTable_sorted)
    matched_next_ILF = look_up_closest(matched_limit, "Limit", "Next_ILF", ILFTable_sorted)
    
    # Identify if the matched_limit is the last limit and the sum_limit exactly matches it
    is_last_limit = matched_limit == ILFTable["Limit"].max()
    is_exact = (sum_limit - matched_limit).abs() <= 1e-8
    mask_exact_last = is_last_limit & is_exact
    
    # Calculate the interpolated ILF - ensure denominator is not zero
    denominator = matched_next_limit - matched_limit
    with np.errstate(divide="ignore", invalid="ignore"):
        interpolated_ILF = matched_ILF + (
            (matched_next_ILF - matched_ILF) / denominator
        ) * (sum_limit - matched_limit)
    
    interpolated_ILF = pd.Series(interpolated_ILF).replace([np.inf, -np.inf], np.nan).values
    
    # Use matched_ILF where it's an exact match with the last limit, else use interpolated_ILF
    value_if_false = np.where(mask_exact_last, matched_ILF, interpolated_ILF)
    
    # Combine True and False Conditions
    limit_point = np.where(condition, value_if_true, value_if_false)
    
    # Handle Errors by Replacing NaN with
    limit_point_series = pd.Series(limit_point, index=airlines_df.index)
    limit_point_series = limit_point_series.replace([np.inf, -np.inf], np.nan).fillna(0)
    
    return limit_point_series


def calculate_tpl_rate_on_limit(airlines_df):
    # 1. Extract TPL parameters from TPLMisc
    NonExposedTPLRate = look_up("NonExposedTPLRate", "Factor", "Value", TPLMisc, lookup_type="single")
    TPLLowerLimit = look_up("TPLLowerLimit", "Factor", "Value", TPLMisc, lookup_type="single")
    TPLLowerLimitRate = look_up("TPLLowerLimitRate", "Factor", "Value", TPLMisc, lookup_type="single")
    TPLUpperLimit = look_up("TPLUpperLimit", "Factor", "Value", TPLMisc, lookup_type="single")
    TPLMinRate = look_up("TPLMinRate", "Factor", "Value", TPLMisc, lookup_type="single")

    # 2. Extract Other Necessary Columns
    liability_limit_usd = airlines_df["liability_limit_usd"]
    tpl_liab_limit_exposed = airlines_df["tpl_liab_limit_exposed"]
    tpl_usage = airlines_df["tpl_usage"]

    # 3. Initialize rate with zeros
    rate = pd.Series(0, index=airlines_df.index)

    # 4. Condition 1: liability_limit_usd < TPLLowerLimit
    condition_lower = liability_limit_usd < TPLLowerLimit
    rate.loc[condition_lower] = TPLLowerLimitRate

    # 5. Condition 2: liability_limit_usd > TPLUpperLimit
    condition_upper = liability_limit_usd > TPLUpperLimit
    rate.loc[condition_upper] = TPLMinRate

    # 6. Condition 3: TPLLowerLimit <= liability_limit_usd <= TPLUpperLimit
    condition_middle = (~condition_lower) & (~condition_upper) & (~liability_limit_usd.isna())

    if condition_middle.any():
        # Extract relevant rows where condition_middle is True
        sum_limit_middle = liability_limit_usd[condition_middle]
 

        # 6.1. Find the matched_limit and matched_rate
        matched_limit = look_up_closest(sum_limit_middle, "CSL", "CSL", TPLLimitsRates)
        matched_rate = look_up_closest(sum_limit_middle, "CSL", "Rate", TPLLimitsRates)
        
        matched_limit.index = sum_limit_middle.index
        matched_rate.index = sum_limit_middle.index
       

        # 6.2. Prepare TPLLimitsRates with Next_Limit and Next_Rate for interpolation
        TPLLimitsRates_sorted = TPLLimitsRates.sort_values("CSL").reset_index(drop=True).copy()
        TPLLimitsRates_sorted["Next_Limit"] = TPLLimitsRates_sorted["CSL"].shift(-1)
        TPLLimitsRates_sorted["Next_Rate"] = TPLLimitsRates_sorted["Rate"].shift(-1)

        # 6.3. Find the Next_Limit and Next_Rate based on matched_limit
        matched_next_limit = look_up_closest(matched_limit, "CSL", "Next_Limit", TPLLimitsRates_sorted)
        matched_next_rate = look_up_closest(matched_limit, "CSL", "Next_Rate", TPLLimitsRates_sorted)

        matched_next_limit.index = sum_limit_middle.index
        matched_next_rate.index = sum_limit_middle.index

        # 6.4. Identify Exact Matches with the Last Limit
        is_last_limit = matched_limit == TPLLimitsRates["CSL"].max()
        is_exact = (sum_limit_middle - matched_limit).abs() <= 1e-8
        mask_exact_last = is_last_limit & is_exact

        # 6.5. Calculate the Interpolated Rate
        denominator = matched_next_limit - matched_limit
        with np.errstate(divide="ignore", invalid="ignore"):
            interpolated_rate = matched_rate + (
                (matched_next_rate - matched_rate) / denominator
            ) * (sum_limit_middle - matched_limit)

        # Replace infinities with NaN
        interpolated_rate = interpolated_rate.replace([np.inf, -np.inf], np.nan)

        # 6.6. Final Rate for Condition Middle
        final_rate_middle = matched_rate.copy()
        final_rate_middle[~mask_exact_last] = interpolated_rate[~mask_exact_last]

        # 6.7. Handle any remaining NaNs in final_rate_middle
        final_rate_middle = final_rate_middle.fillna(0)

        # 6.8. Assign the Final Rate to the Main Rate Series using .loc
        rate.loc[condition_middle] = final_rate_middle

    # 7. Calculate the TPL rate on limit
    tpl_rol = (rate * tpl_usage * tpl_liab_limit_exposed) + (NonExposedTPLRate * (1 - tpl_liab_limit_exposed))

    # 8. Zero NaN and rows where limit exposed is 0
    tpl_rol = tpl_rol.replace([np.inf, -np.inf], np.nan).fillna(0)
    tpl_rol = tpl_rol.where(tpl_liab_limit_exposed != 0, 0)

    # 9. Convert to pandas Series aligned with airlines_df
    tpl_rol_series = pd.Series(tpl_rol, index=airlines_df.index)

    return tpl_rol_series


def calculate_tpl_fleet_discount(tpl_fleet_size):
    # Exit early if fleet size is not at least 1
    if tpl_fleet_size < 1:
        return 1
    
    # Check if tpl_fleet_size exceeds the maximum fleet size
    max_fleet_size = look_up("TPLMaximumFleetSize", "Factor", "Value", TPLMisc, lookup_type="single")
    max_fleet_discount = look_up("TPLMaxFleetDiscount", "Factor", "Value", TPLMisc, lookup_type="single")
    if tpl_fleet_size > max_fleet_size:
        return max_fleet_discount
    
    # Find the largest Mid-point less than or equal to tpl_fleet_size
    matched_mid_point = look_up_closest(tpl_fleet_size, "Mid-point", "Mid-point", TPLFleetSizeDiscount, lookup_type="single")
    
    # Retrieve the row corresponding to the matched_mid_point
    match_row = TPLFleetSizeDiscount[TPLFleetSizeDiscount["Mid-point"] == matched_mid_point]
    
    if match_row.empty:
        # If no match is found, return NaN
        return np.nan
    
    # Get the index of the matched row
    match_index = match_row.index[0]
    
    # Check if the matched row is the last row and the fleet size exactly matches the Mid-point
    is_last_row = (match_index == TPLFleetSizeDiscount.index[-1])
    is_exact_match = np.isclose(tpl_fleet_size, matched_mid_point, atol=1e-8)
    
    if is_last_row and is_exact_match:
        # Exact match at the maximum defined Mid-point
        discount = look_up(matched_mid_point, "Mid-point", "Parameter", TPLFleetSizeDiscount, lookup_type="single")
        return discount
    else:
        # Retrieve the current discount
        current_discount = look_up(matched_mid_point, "Mid-point", "Parameter", TPLFleetSizeDiscount, lookup_type="single")
        
        # Ensure there is a next row to interpolate with
        if match_index + 1 < len(TPLFleetSizeDiscount):
            next_mid_point = TPLFleetSizeDiscount.loc[match_index + 1, "Mid-point"]
            next_discount = TPLFleetSizeDiscount.loc[match_index + 1, "Parameter"]
            
            # Calculate the difference in fleet size and discounts
            size_diff = next_mid_point - matched_mid_point
            discount_diff = next_discount - current_discount
            
            if size_diff == 0:
                # Avoid division by zero if Mid-points are identical
                interpolated_discount = current_discount
            else:
                # Linear interpolation
                interpolated_discount = current_discount + (discount_diff / size_diff) * (tpl_fleet_size - matched_mid_point)
            
            return interpolated_discount
        else:
            # If there's no next row, return the current discount
            return current_discount

### --- ACTUAL RATING --- ###

def rate_airlines(hxd):
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    airlines = expo.airlines
    airlines_default = expo.airlines_default

    # Useful fields
    ccy = hxd.cds.currencies.source_currency
    liability_cvg = cvg.liability.coverage
    hull_brokerage = cvg.hull.brokerage
    liab_brokerage = cvg.liability.brokerage
    hull_quoted_premium = cvg.hull.quoted_premium
    liab_quoted_premium = cvg.liability.quoted_premium

    # Look up operator class
    for op in expo.operators:
        op.operator_class = look_up(op.operator, "Operator", "Mapped TLO Group", OperatorTLOGroup, lookup_type="single", if_not_found="Not Found")

    # Get df with exposure
    airlines_df = pd_df_from_hx_list(airlines)
    airlines_df = airlines_df.loc[:, ~airlines_df.columns.str.startswith("countries")] # Remove unnecessary columns

    # Validate entries in the table
    validate_table(hxd, airlines_df)

    # Calculate PPL Award and total value
    airlines_df["operator_region"] = look_up(airlines_df["operator_country"], "Country", "Region Airlines", OperatorCountryList, if_not_found=np.nan)
   
    #FS 24/08/2025 Additional conditions added for pll award for storage and time in service
    airlines_df["country_pll_award"] = look_up(airlines_df["operator_region"], "Country", "PLL Awards", PLLAwards, if_not_found=0)   
    airlines_df["pll_award"] = np.where((airlines_df["aircraft_status"] == "Storage") | (airlines_df["time_in_service"] == 0),
        0,
        airlines_df["country_pll_award"]
    )

    airlines_df["value_ccy"] = to_ccy(usd(airlines_df["value"], airlines_df["hull_ccy"], lookup_type="array").fillna(0), ccy)
    total_value = airlines_df.loc[airlines_df["include"] == True, "value_ccy"].sum()

    hull_premium_from_rate = 0

    # Combine df and looping to avoid repeated look-ups but handle overrides correctly
    for idx, ac in enumerate(airlines):
        # Avoid None errors
        total_seats = airlines_df["total_seats"].iloc[idx] or 0
        liability_limit = airlines_df["liability_limit"].iloc[idx] or 0

        ac.pll_award.calculated = airlines_df["pll_award"].iloc[idx]
        ac.tpl_limit_exposed.calculated = min(1, ratio(ac.pll_award.selected * total_seats + PLLAdditionalTPCover["Parameter"].iloc[0], liability_limit))
        ac.achieved_hull_rate.calculated = ratio(cvg.hull.quoted_premium, total_value)
        hull_premium_from_rate += ac.achieved_hull_rate.selected * airlines_df["value_ccy"].iloc[idx] * airlines_df["include"].iloc[idx].astype(int)

    # Assign region
    write_pd_to_hxd(airlines_df, expo.airlines, ["operator_region"], replace_nan=True)

    # Assign hull premiums
    expo.hull_premium.from_slip = cvg.hull.quoted_premium
    expo.hull_premium.from_rate = hull_premium_from_rate

    if abs(expo.hull_premium.from_slip - expo.hull_premium.from_rate) > 0.01: # Allow for small tolerance in difference
        expo.hull_premium.are_premiums_different = True
        expo.hull_premium.are_premiums_equal = False
        expo.hull_premium.difference_msg = "Ensure Gross Achieved Hull Rate aligns with slip values."
    else:
        expo.hull_premium.are_premiums_different = False
        expo.hull_premium.are_premiums_equal = True
        expo.hull_premium.difference_msg = None

    # --- RATING --- #
    airlines_df = pd_df_from_hx_list(airlines) # Get df with updated calculated values
    airlines_df = airlines_df.loc[:, ~airlines_df.columns.str.startswith("countries")] # Remove unnecessary columns

    status_split = {"in_service": expo.status_split.in_service, "storage": expo.status_split.storage, "other": expo.status_split.other}
    operator_class = expo.selected_operator_class

    # Calculate fleet size and check for duplicate registrations
    filtered_regs = airlines_df.loc[airlines_df["include"] & airlines_df["registration"].notna(), "registration"]
    expo.fleet_size.calculated = filtered_regs.nunique()
    fleet_size = max(expo.fleet_size.selected, 1) # Prevent div by 0 errors

    if filtered_regs.nunique() < len(filtered_regs):
        expo.has_duplicate_regs = True
        duplicate_mask = filtered_regs.duplicated(keep=False)
        duplicate_indices = (filtered_regs[duplicate_mask].index + 1).tolist()
        
        expo.has_duplicate_regs_msg = f"⚠️ Ensure fleet size is correct. Duplicate registrations found on rows: {', '.join(map(str, duplicate_indices))}."
        
        # Prompt confirmation of fleet size
        if expo.fleet_size.override is None:
            hx.errors.validation("Please confirm the fleet size is correct by overriding the Fleet Size field in Airlines Details. If the fleet size is already correct, please override it with the same number.")

    # Check for bulk rating
    has_bulk_rating = airlines_df[airlines_df["include"] & (airlines_df["no_of_aircraft"] > 1)].shape[0] > 0

    if has_bulk_rating:
        expo.has_duplicate_regs = True # Using the same node for warning message even though it's not strictly true
        expo.has_duplicate_regs_msg = "⚠️ Aircrafts subject to bulk pricing. Please update the fleet size above."

    # Helper columns
    tpl_fleet_size = airlines_df[(airlines_df["include"] == True) & (airlines_df["tpl_limit_exposed"] > 0)]["no_of_aircraft"].sum()
    airlines_df["value_usd"] = usd(airlines_df["value"], airlines_df["hull_ccy"], lookup_type="array").fillna(0)
    airlines_df["hull_limit_usd"] = usd(airlines_df["hull_limit"], airlines_df["hull_ccy"], lookup_type="array").fillna(0) #TODO: check this is correct behaviour
    airlines_df["hull_excess_usd"] = usd(airlines_df["hull_excess"], airlines_df["hull_ccy"], lookup_type="array").fillna(0)
    airlines_df["liability_limit_usd"] = usd(airlines_df["liability_limit"], airlines_df["liability_ccy"], lookup_type="array").fillna(0) #TODO: check this is correct behaviour
    airlines_df["liability_excess_usd"] = usd(airlines_df["liability_excess"], airlines_df["liability_ccy"], lookup_type="array").fillna(0)
    airlines_df["term_adj"] = policy_term(pd.to_datetime(airlines_df["attachment_date"]), pd.to_datetime(airlines_df["expiry_date"]))

    # Hull frequency
    airlines_df["hull_f_base"] = HullBaseFreq["Base Hull Frequency"].iloc[0]
    airlines_df["hull_f_status"] = calculate_status_rel(status_split, airlines_df, HullFreqStatus, use_time_in_service=True)
    airlines_df["hull_f_operator_region"] = look_up(airlines_df["operator_region"], "Region2", "Parameter", HullFreqRegion, if_not_found=1)
    airlines_df["hull_f_previous12_months_hours"] = np.exp(np.log(HullFreqPrev12monthshours["Parameter"].iloc[0]) * airlines_df["previous12_months_hours"].fillna(0))
    airlines_df["hull_f_market_class"] = look_up(airlines_df["market_class"], "Class", "Parameter", HullFreqClass, if_not_found=1)
    airlines_df["hull_f_build_year_group"] = look_up_with_bounds(airlines_df["build_year"], "Lower", "Upper", "Group", BuildYearFreq, if_not_found="Pre 1995")
    airlines_df["hull_f_build_year"] = look_up(airlines_df["hull_f_build_year_group"], "Build Year", "Parameter", HullFreqBuildYear)
    airlines_df["hull_f_usage"] = look_up(airlines_df["usage"], "Usage", "Parameter", HullFreqUsage, if_not_found=1)
    hull_freq_cols = ["no_of_aircraft", "hull_f_base", "hull_f_status", "hull_f_operator_region", "hull_f_previous12_months_hours", "hull_f_market_class", "hull_f_build_year", "hull_f_usage"]
    tlo_freq_adj_factor = TLOFreqAdjustment["Total Loss Only Frequency Adjustment"].iloc[0]
    tlo_freq_adj = np.where(airlines_df["coverage"] == "TLO",
                            look_up(operator_class, "Class", "Factor", OperatorClass, if_not_found=1, lookup_type="single") * tlo_freq_adj_factor, 1) # Having 1 as if_not_found so subsequent multiplication doesn't fail
    airlines_df["hull_frequency"] = tlo_freq_adj * airlines_df[hull_freq_cols].prod(axis=1, skipna=True)

    # Hull severity
    airlines_df["hull_s_base"] = HullBaseSev["Base Hull Severity"].iloc[0]
    airlines_df["hull_s_previous12_months_hours"] = np.exp(np.log(HullSevPrevious12monthshours["Parameter"].iloc[0]) * airlines_df["previous12_months_hours"].fillna(0))
    airlines_df["hull_s_market_class"] = look_up(airlines_df["market_class"], "Class", "Parameter", HullSevClass, if_not_found=1)
    russian_args = {"lookup_col": "Russian Build", "return_col": "Parameter", "df": HullSevRussianBuild, "lookup_type": "single"}
    airlines_df["hull_s_russian_built"] = np.where(airlines_df["russian_built"], look_up("Yes", **russian_args), look_up("No", **russian_args))
    airlines_df["hull_s_mtow"] = np.exp(np.log(HullSevOperatingMTOW["Parameter"].iloc[0]) * airlines_df["operating_mtow_lb"].fillna(0))
    airlines_df["hull_s_build_year_group"] = look_up_with_bounds(airlines_df["build_year"], "Lower", "Upper", "Group", BuildYearSev, if_not_found="Pre 1995")
    airlines_df["hull_s_build_year"] = look_up(airlines_df["hull_s_build_year_group"], "Build Year", "Parameter", HullSevBuildYear)
    hull_sev_cols = ["hull_s_base", "hull_s_previous12_months_hours", "hull_s_market_class", "hull_s_russian_built", "hull_s_mtow", "hull_s_build_year"]
    #YZ 07.06.2026: When coverage is TLO, no uplift for Attritional. And the total severity % should not be greater than 100%. 
    airlines_df["hull_severity"] = np.minimum(
        np.where(airlines_df["coverage"] == "TLO", 1, airlines_df[hull_sev_cols].prod(axis=1, skipna=True)),
        1)

    # Hull EL
    low_value_args = {"lookup_col": "Parameter", "return_col": "Value", "df": LowValue, "lookup_type": "single"}
    airlines_df["hull_low_value_load"] = np.maximum(
        np.log(airlines_df["value_usd"].clip(lower=1e-8)) * look_up("A", **low_value_args) + look_up("B", **low_value_args), # Use 'clip' to avoid getting np.inf
        1
    )
    discount_args = {"lookup_col": "Parameter", "return_col": "Value", "df": FleetDiscountParameter, "lookup_type": "single"}
    airlines_df["hull_fleet_adj"] = np.maximum(
        look_up("A", **discount_args) * fleet_size ** look_up("B", **discount_args), 0.5)
    airlines_df["hull_attr_uplift"] = 1 + np.where(
        airlines_df["coverage"] == "TLO", 0, look_up("Hull", "Cover", "Attritional Uplift", AttritionalLoad, lookup_type="single"))
    hull_loss_cost_gu_cols = ["value_usd", "hull_frequency", "hull_severity", "hull_low_value_load", "hull_fleet_adj", "hull_attr_uplift"]
    airlines_df["hull_loss_cost_gu_usd"] = airlines_df[hull_loss_cost_gu_cols].prod(axis=1, skipna=True)

    beta_dist_args = {"lookup_col": "Parameter", "return_col": "Value", "df": HullExposure, "lookup_type": "single"}
    alpha_param = look_up("Alpha", **beta_dist_args)
    beta_param = look_up("Beta", **beta_dist_args)
    airlines_df["hull_limit_point"] = airlines_df[["hull_limit_usd", "hull_excess_usd", "value_usd"]].apply(
        lambda x: beta.cdf(min((x["hull_limit_usd"] + x["hull_excess_usd"]) / x["value_usd"], 1), alpha_param, beta_param), axis=1
    )
    airlines_df["hull_excess_point"] = airlines_df[["hull_limit_usd", "hull_excess_usd", "value_usd"]].apply(
        lambda x: beta.cdf(min((x["hull_excess_usd"]) / x["value_usd"], 1), alpha_param, beta_param), axis=1
    )
    airlines_df["hull_ilf"] = airlines_df["hull_limit_point"] - airlines_df["hull_excess_point"]
    hull_loss_cost_cols = ["hull_loss_cost_gu_usd", "hull_ilf", "term_adj"]
    airlines_df["hull_loss_cost_usd"] = airlines_df[hull_loss_cost_cols].fillna(0).prod(axis=1, skipna=True)

    # PAX Liability
    airlines_df["pax_seats_in_service"] = np.where(airlines_df["aircraft_status"]=="In Service", airlines_df["total_seats"], 0)
    airlines_df["pax_base_freq_year_built"] = np.exp(np.log(float(LiabBaseFreq["Base Liab Frequency"].iloc[0])) + np.log(look_up("Build Year", "Usage", "Parameter", LiabFreqBuildYearNumeric, lookup_type="single")) * airlines_df["build_year"].fillna(1900)) # Filling build_year with oldest found in Cirium data
    airlines_df["pax_status"] = calculate_status_rel(status_split, airlines_df, LiabFreqStatus, use_time_in_service=False)
    airlines_df["pax_operator_region"] = look_up(airlines_df["operator_region"], "Region2", "Parameter", LiabFreqRegion, if_not_found=1)
    airlines_df["pax_12_months_hours"] = np.exp(np.log(LiabFreqPrev12monthshours["Parameter"].iloc[0]) * airlines_df["previous12_months_hours"].fillna(0))
    airlines_df["pax_market_class"] = look_up(airlines_df["market_class"], "Class", "Parameter", LiabFreqClass, if_not_found=1)
    airlines_df["pax_severity_per_seat_usd"] = look_up(airlines_df["operator_region"], "Country", "Major Loss Airline Pax Liab Severity per Seat", LiabSeverity)
    airlines_df["pax_attr_uplift"] = 1 + look_up("Liability", "Cover", "Attritional Uplift", AttritionalLoad, lookup_type="single")
    pax_liab_per_seat_cols = ["pax_base_freq_year_built", "pax_status", "pax_operator_region", "pax_12_months_hours", "pax_market_class", "pax_severity_per_seat_usd", "pax_attr_uplift"]
    airlines_df["pax_liability_per_seat"] = airlines_df[pax_liab_per_seat_cols].prod(axis=1, skipna=True)
    airlines_df["pax_fleet_adj"] = airlines_df["hull_fleet_adj"]
    airlines_df["pax_loss_cost_gu_usd"] = airlines_df[["pax_seats_in_service", "pax_liability_per_seat", "pax_fleet_adj"]].prod(axis=1, skipna=True)
    airlines_df["pax_limit_point"] = calculate_ilf_point(airlines_df, point_type="limit")
    airlines_df["pax_attachment_point"] = calculate_ilf_point(airlines_df, point_type="attachment")
    airlines_df["pax_ilf"] = airlines_df["pax_limit_point"] - airlines_df["pax_attachment_point"]
    pax_loss_cost_cols = ["pax_loss_cost_gu_usd", "pax_ilf", "term_adj"]
    airlines_df["pax_loss_cost_usd"] = 0 if liability_cvg == "Third Party" else airlines_df[pax_loss_cost_cols].prod(axis=1, skipna=True)

    # TPL Liability
    airlines_df["tpl_liab_limit_exposed"] = airlines_df["tpl_limit_exposed"] #FS 24/09/2025: Removal of pll_award condition - np.where((pd.isna(airlines_df["pll_award"]) | (airlines_df["pll_award"] == 0)), 0, airlines_df["tpl_limit_exposed"])
    airlines_df["tpl_usage"] = look_up(airlines_df["usage"], "Usage", "Parameter", LiabFreqUsage, if_not_found=0) / look_up("Passenger", "Usage", "Parameter", LiabFreqUsage, lookup_type="single", if_not_found=1)
    airlines_df["tpl_rate_on_limit"] = calculate_tpl_rate_on_limit(airlines_df)
    airlines_df["tpl_base_loss_cost_usd"] = airlines_df[["liability_limit_usd", "tpl_rate_on_limit"]].prod(axis=1, skipna=True) * look_up("TPLTargetLR", "Factor", "Value", TPLMisc, lookup_type="single", if_not_found=1)
    airlines_df["tpl_fleet_adj"] = calculate_tpl_fleet_discount(tpl_fleet_size)
    tpl_loss_cost_cols = ["tpl_base_loss_cost_usd", "tpl_fleet_adj", "term_adj"]
    airlines_df["tpl_loss_cost_usd"] = 0 if liability_cvg == "Passenger" else airlines_df[tpl_loss_cost_cols].prod(axis=1, skipna=True)

    # Benchmarking
    airlines_df["bm_term_adj"] = airlines_df["term_adj"]
    airlines_df["bm_hull_large_loss_cost"] = ratio(airlines_df["hull_loss_cost_usd"], airlines_df["hull_attr_uplift"])
    airlines_df["bm_hull_large_severity"] = ratio(airlines_df["bm_hull_large_loss_cost"], airlines_df["hull_frequency"])
    liab_large_frequency_cols = ["pax_base_freq_year_built", "pax_status",	"pax_operator_region", "pax_12_months_hours", "pax_market_class"]
    airlines_df["bm_liab_large_frequency"] = airlines_df["include"].astype(int) * airlines_df[liab_large_frequency_cols].prod(axis=1, skipna=True)
    airlines_df["bm_liab_large_loss_cost"] = ratio(airlines_df["pax_loss_cost_usd"], airlines_df["pax_attr_uplift"])
    airlines_df["bm_liab_large_severity"] = ratio(airlines_df["bm_liab_large_loss_cost"], airlines_df["bm_liab_large_frequency"])
    airlines_df["bm_hull_benchmark"] = ratio(ratio(airlines_df["hull_loss_cost_usd"], benchmark_lr), 1 - hull_brokerage)
    airlines_df["bm_hull_benchmark_rate"] = ratio(airlines_df["bm_hull_benchmark"], airlines_df["no_of_aircraft"] * airlines_df["value"])
    airlines_df["bm_pax_liab_benchmark_cost"] = ratio(ratio(airlines_df["pax_loss_cost_usd"], benchmark_lr), 1 - liab_brokerage)
    airlines_df["bm_pax_liability_per_seat"] = ratio(airlines_df["bm_pax_liab_benchmark_cost"], airlines_df["no_of_aircraft"] * airlines_df["total_seats"])
    airlines_df["bm_tpl_benchmark"] = ratio(ratio(airlines_df["tpl_loss_cost_usd"], benchmark_lr), 1 - liab_brokerage)
    airlines_df["bm_allocated_hull_premium"] = ratio(airlines_df["hull_loss_cost_usd"], airlines_df["hull_loss_cost_usd"].sum()) * hull_quoted_premium
    airlines_df["bm_aircraft_in_expiry_fleet"] = False # TODO: check what this is for (it's for RC, but is it needed?)
    airlines_df["bm_total_liab_premium"] = airlines_df["pax_loss_cost_usd"] + airlines_df["tpl_loss_cost_usd"]
    airlines_df["bm_allocated_liab_premium"] = ratio(airlines_df["bm_total_liab_premium"], airlines_df["bm_total_liab_premium"].sum()) * liab_quoted_premium

    # --- Airlines Rating --- #
    
    # Summary table
    ar_summary = expo.airlines_rating_summary
    ar_summary.fleet_size = expo.fleet_size.selected
    ar_summary.hull_loss_cost = airlines_df.loc[airlines_df["include"], "hull_loss_cost_usd"].sum()
    ar_summary.total_seats = airlines_df.loc[airlines_df["include"], "pax_seats_in_service"].sum()
    ar_summary.pax_loss_cost = airlines_df.loc[airlines_df["include"], "pax_loss_cost_usd"].sum()
    ar_summary.tpl_loss_cost = airlines_df.loc[airlines_df["include"], "tpl_loss_cost_usd"].sum()
    ar_summary.hull_large_severity = ratio((airlines_df["bm_hull_large_severity"] * airlines_df["hull_frequency"]).sum(), airlines_df["hull_frequency"].sum())
    ar_summary.liab_large_severity = ratio((airlines_df["bm_liab_large_severity"] * airlines_df["bm_liab_large_frequency"]).sum(), airlines_df["bm_liab_large_frequency"].sum())

    # Push to hxd
    airlines_df[["market_class", "registration"]] = airlines_df[["market_class", "registration"]].fillna("")
    expo.airlines_rating = airlines_df[["market_class", "registration"]].to_dict("records")

    ar_output_cols = [
        "no_of_aircraft",
        "value_usd",
        "coverage",
        "attachment_date",
        "expiry_date",
        "usage",
        "build_year",
        "aircraft_status",
        "previous12_months_hours",
        "operator_region",
        "russian_built",
        "total_seats",
        "operating_mtow_lb",
        "include",
        "hull_f_base",
        "hull_f_status",
        "hull_f_operator_region",
        "hull_f_previous12_months_hours",
        "hull_f_market_class",
        "hull_f_build_year_group",
        "hull_f_build_year",
        "hull_f_usage",
        "hull_frequency",
        "hull_s_base",
        "hull_s_previous12_months_hours",
        "hull_s_market_class",
        "hull_s_russian_built",
        "hull_s_mtow",
        "hull_s_build_year_group",
        "hull_s_build_year",
        "hull_severity",
        "hull_low_value_load",
        "hull_fleet_adj",
        "hull_attr_uplift",
        "hull_loss_cost_gu_usd",
        "hull_limit_point",
        "hull_excess_point",
        "hull_loss_cost_usd",
        "hull_limit_usd",
        "hull_excess_usd",
        "pax_seats_in_service",
        "pax_base_freq_year_built",
        "pax_status",
        "pax_operator_region",
        "pax_12_months_hours",
        "pax_market_class",
        "pax_severity_per_seat_usd",
        "pax_attr_uplift",
        "pax_liability_per_seat",
        "pax_fleet_adj",
        "pax_loss_cost_gu_usd",
        "pax_limit_point",
        "pax_attachment_point",
        "liability_limit_usd",
        "liability_excess_usd",
        "pax_loss_cost_usd",
        "tpl_liab_limit_exposed",
        "tpl_usage",
        "tpl_rate_on_limit",
        "tpl_base_loss_cost_usd",
        "tpl_fleet_adj",
        "tpl_loss_cost_usd",
        "bm_term_adj",
        "bm_hull_large_loss_cost",
        "bm_hull_large_severity",
        "bm_liab_large_frequency",
        "bm_liab_large_loss_cost",
        "bm_liab_large_severity",
        "bm_hull_benchmark",
        "bm_hull_benchmark_rate",
        "bm_pax_liab_benchmark_cost",
        "bm_pax_liability_per_seat",
        "bm_tpl_benchmark",
        "bm_allocated_hull_premium",
        "bm_aircraft_in_expiry_fleet",
        "bm_total_liab_premium",
        "bm_allocated_liab_premium"
    ]

    airlines_df = airlines_df.fillna(np.nan).replace([np.nan, np.inf, -np.inf], [None, None, None])
    write_pd_to_hxd(airlines_df, expo.airlines_rating, ar_output_cols, replace_nan=True)

    # --- Aircraft Summary --- #

    # Push to hxd
    expo.aircraft_summary = airlines_df[["include", "market_class", "registration"]].to_dict("records")

    # Aircraft summary
    airlines_df["hull_value"] = to_ccy(airlines_df["value_usd"], ccy)
    airlines_df["hull_benchmark"] = to_ccy(airlines_df["bm_hull_benchmark"], ccy)
    airlines_df["hull_benchmark_rate"] = airlines_df["bm_hull_benchmark_rate"]
    airlines_df["pax_limit"] = (airlines_df["no_of_aircraft"] * to_ccy(airlines_df["liability_limit_usd"], ccy)).fillna(0)
    airlines_df["pax_liab_benchmark"] = to_ccy(airlines_df["bm_pax_liab_benchmark_cost"], ccy)
    airlines_df["pax_liab_benchmark_per_seat"] = to_ccy(airlines_df["bm_pax_liability_per_seat"], ccy)
    airlines_df["tpl_benchmark"] = to_ccy(airlines_df["bm_tpl_benchmark"], ccy)
    airlines_df["total_hull_benchmark"] = airlines_df["hull_benchmark"]
    airlines_df["total_liab_benchmark"] = airlines_df[["pax_liab_benchmark", "tpl_benchmark"]].sum(axis=1)
    airlines_df["total_benchmark"] = airlines_df[["total_hull_benchmark", "total_liab_benchmark"]].sum(axis=1)
   
    as_output_cols = [
        "no_of_aircraft",
        "hull_value", 
        "hull_benchmark",
        "hull_benchmark_rate",
        "pax_limit",
        "pax_liab_benchmark",
        "pax_liab_benchmark_per_seat",
        "tpl_benchmark",
        "total_hull_benchmark",
        "total_liab_benchmark",
        "total_benchmark",
    ]

    write_pd_to_hxd(airlines_df, expo.aircraft_summary, as_output_cols, replace_nan=True)

    # Totals
    tot = expo.aircraft_summary_total

    sum_cols = [
        "hull_benchmark", 
        "pax_liab_benchmark", 
        "tpl_benchmark", 
        "total_hull_benchmark", 
        "total_liab_benchmark", 
        "total_benchmark"
    ]

    for col in sum_cols:
        total_sum = airlines_df.loc[airlines_df["include"], col].sum()
        setattr(tot, col, total_sum)

    tot.hull_value = np.dot(airlines_df[airlines_df["include"] == True]["no_of_aircraft"].fillna(0), airlines_df[airlines_df["include"] == True]["hull_value"])
    tot.hull_benchmark_rate = ratio(tot.hull_benchmark, tot.hull_value)
    tot.pax_limit = airlines_df["pax_limit"].max()

    total_seats_in_service = airlines_df.loc[airlines_df["include"], "pax_seats_in_service"].sum()
    tot.pax_liab_benchmark_per_seat = ratio(tot.pax_liab_benchmark, total_seats_in_service)

    # For minimum premium
    max_liab_limit = airlines_df["liability_limit"].fillna(0).max()

    return airlines_df, max_liab_limit
    


    
