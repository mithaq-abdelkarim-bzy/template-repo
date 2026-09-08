import hx
import json
import pandas as pd
pd.set_option("display.max_columns", None)
import numpy as np
import math as math
from algorithms.rate_utilities import ratio, one_layer, pd_df_from_hx_list, write_pd_to_hxd
from algorithms.rate_utilities import look_up, look_up_closest, look_up_with_bounds, find_closest, usd, to_ccy, policy_term
from algorithms.rate_constants import benchmark_lr
from algorithms.rate_ux import validate_table
from scipy.stats import beta

### --- PARAM TABLES --- ###

# FS 27/08/2025: Parameter tables have all been updated and partial loss tables have been added
# W:\Finance\Actuarial\Pricing\02 - Marine\08 - Aviation\HX Aviation\GA GLM 2025 Updates\New Parameter Tables
Base = hx.params.ga_Base
BaseUse = hx.params.ga_BaseUse
BaseOccupancy = hx.params.ga_BaseOccupancy
SeatOccupancy = hx.params.ga_SeatOccupancy
SeatOccupancyCountry = hx.params.ga_SeatOccupancyCountry
SeatNumberAdjustment = hx.params.ga_SeatNumberAdjustment
FatalityRateAB = hx.params.ga_FatalityRateAB
AirplaneUse = hx.params.ga_AirplaneUse
Region = hx.params.ga_Region
TotalFreqBase = hx.params.ga_TotalFreqBase
ForLinear = hx.params.ga_ForLinear
StatusMod = hx.params.ga_StatusMod
BuildLocationMod = hx.params.ga_BuildLocationMod
RegionMod = hx.params.ga_RegionMod
UseMod = hx.params.ga_UseMod
FleetSizeMod = hx.params.ga_FleetSizeMod
PartialConversion = hx.params.ga_PartialConversionFactor
PartialBaseSeverity = hx.params.ga_PartialBaseSeverity
PartialBuildYearMod = hx.params.ga_PartialBuildYearMod
PartialEngineMod = hx.params.ga_PartialEngineMod
HullAttr = hx.params.ga_HullAttr
LiabFreqAdj = hx.params.ga_LiabFreqAdj
PAXAward = hx.params.ga_PAXAward
PAXNetWorth = hx.params.ga_PAXNetWorth
LiabAttr = hx.params.ga_LiabAttr
TPL = hx.params.ga_TPL
TPLUnexposedRate = hx.params.ga_TPLUnexposedRate
RateIncrease = hx.params.ga_RateIncrease
OperatorCountryList = hx.params.OperatorCountryList

### --- HELPER FUNCTIONS --- ###

def get_countries(hxd, ac):
    OperatorCountryList = hx.params.OperatorCountryList
    cirium_region = look_up(ac.operator_region, "Region GA", "Region", OperatorCountryList, if_not_found="N/A", lookup_type="single")
    
    if cirium_region == "N/A":
        countries_df = OperatorCountryList.rename(columns={"Country": "country"})
    else:
        countries_df = OperatorCountryList[OperatorCountryList["Region"] == cirium_region].rename(columns={"Country": "country"})
    
    ac.countries = countries_df[["country"]].to_dict("records")

def calculate_seat_occupancy(row):
    # Extract necessary fields from the row
    operator_region = row["operator_region"]
    aircraft_class = row["aircraft_class"]
    use = row["use"]
    total_seats = row["total_seats"] or 0

    # Region look up
    region = look_up(operator_region, "Region Detailed", "Region", Region, lookup_type="single")
    if pd.isna(region):
        return 0 

    # FS 27/08/2025: Seat Occupancy Base Rate
    seat_occupancy_value = look_up(aircraft_class, "Class", "Base Rate", SeatOccupancy, lookup_type = "single")
    if pd.isna(seat_occupancy_value):
        return 0

    # FS 27/08/2025: Country Factor Calc
    country_factor = look_up(region, "Country", "Factor", SeatOccupancyCountry, lookup_type = "single")
    if pd.isna(country_factor):
        return 0

    # FS 27/08/2025: Seat Number Adjustment Calcs (linear interpolation)
    lower_seat_num = find_closest(df=SeatNumberAdjustment, column="Number of Seats", lookup_value=total_seats, direction="lower", if_not_found=np.nan, lookup_type="single")
    upper_seat_num = find_closest(df=SeatNumberAdjustment, column="Number of Seats", lookup_value=total_seats, direction="upper", if_not_found=np.nan, lookup_type="single")

    if np.isnan(lower_seat_num) or np.isnan(upper_seat_num):
        return 0

    Y1 = look_up(lower_seat_num, "Number of Seats", "Factor", SeatNumberAdjustment, if_not_found=np.nan, lookup_type="single")
    Y2 = look_up(upper_seat_num, "Number of Seats", "Factor", SeatNumberAdjustment, if_not_found=np.nan, lookup_type="single")

    if np.isnan(Y1) or np.isnan(Y2):
        return 0
    
    # Perform linear interpolation for seat number adjustment
    seat_num_adjustor = Y1 + (Y2 - Y1) / (upper_seat_num - lower_seat_num) * (total_seats - lower_seat_num)

    # # FS 27/08/2025: Seat Occupancy Use Factor
    seat_occupancy_use = look_up(use, "AirplaneUse", "Seat Occupancy", AirplaneUse, lookup_type="single")
    if pd.isna(seat_occupancy_use):
        return 0

    # Final calculation
    expression = seat_occupancy_value * country_factor * seat_num_adjustor * seat_occupancy_use
    result = min(1, expression)

    return result

def calculate_fatality(row):
    # Extract necessary fields from the row
    operator_region = row["operator_region"]
    aircraft_class = row["aircraft_class"]
    use = row["use"]
    total_seats = row["total_seats"] or 0
    seat_occupancy = row["seat_occupancy"] or 0

    # --- Lookups for First Calculation
    region = look_up(operator_region, "Region Detailed", "Region", Region, lookup_type="single")
    if pd.isna(region):
        return 0 

    # FS 27/08/2025: Fatality base rate calculation after "region" removed as rating factor
    base_value = look_up(aircraft_class, "Class", "Factor", Base, lookup_type="single")
    if pd.isna(base_value):
        return 0

    fatality_a = FatalityRateAB["Paramater A"].iloc[0]
    fatality_b = FatalityRateAB["Paramater B"].iloc[0]

    u_w_product = total_seats * seat_occupancy

    # Conditional Calculations for Numerator
    if u_w_product > 10:
        num_cond = (fatality_a * 10) + fatality_b
    elif u_w_product <= 1:
        num_cond = 1
    else:
        num_cond = (fatality_a * u_w_product) + fatality_b

    # Lookup BaseOccupancy Value
    base_occupancy = look_up(region, "Country", aircraft_class, BaseOccupancy, lookup_type="single")
    if pd.isna(base_occupancy):
        return 0

    min_base_occupancy = min(base_occupancy, 10)
    denominator = (min_base_occupancy * fatality_a) + fatality_b

    # Calculate Ratio
    ratio_ = ratio(num_cond, denominator)

    # Lookups for Second Part 
    seat_occupancy_use = look_up(use, "AirplaneUse", "Fatality %", AirplaneUse, lookup_type="single")
    if pd.isna(seat_occupancy_use):
        return 0

    base_use = look_up(region, "Country", aircraft_class, BaseUse, lookup_type="single")
    if pd.isna(base_use):
        return 0

    seat_occupancy_base_use = look_up(base_use, "AirplaneUse", "Fatality %", AirplaneUse, lookup_type="single")
    if pd.isna(seat_occupancy_base_use):
        return 0

    # Final Calculation
    expression = base_value * ratio_ * seat_occupancy_use / seat_occupancy_base_use
    result = min(1, expression)

    return result

def calculate_hull_value_adj(row, ref_df=ForLinear):

    aircraft_class = row["aircraft_class"]
    hull_value = row["hull_value_usd"]
    
    # Filter the reference DataFrame for the specific class
    class_ref = ref_df[ref_df["Class"] == aircraft_class].sort_values("Value Band")
    if class_ref.empty:
        return 0
    
    # Check for exact match using the look_up function
    exact_adjuster = look_up(hull_value, "Value Band", "Adjuster", class_ref, if_not_found=np.nan, lookup_type="single")   
    if not np.isnan(exact_adjuster):
        return exact_adjuster
    
    # Find the lower and upper bound
    lower = find_closest(df=class_ref, column="Value Band", lookup_value=hull_value, direction="lower", if_not_found=np.nan, lookup_type="single")
    upper = find_closest(df=class_ref, column="Value Band", lookup_value=hull_value, direction="upper", if_not_found=np.nan, lookup_type="single")
    if np.isnan(lower) or np.isnan(upper):
        return 0
    
    # Retrieve Adjuster values for lower and upper bounds
    Y1 = look_up(lower, "Value Band", "Adjuster", class_ref, if_not_found=np.nan, lookup_type="single")
    Y2 = look_up(upper, "Value Band", "Adjuster", class_ref, if_not_found=np.nan, lookup_type="single")
    if np.isnan(Y1) or np.isnan(Y2):
        return 0
    
    # Perform linear interpolation
    adjuster = Y1 + (Y2 - Y1) / (upper - lower) * (hull_value - lower)
    return adjuster

def calculate_tpl_rol(row, TPL=TPL):

    # Get required variables
    tpl_limit_usd = row["tpl_limit_usd"]
    tpl_min = TPL["CSL"].min()
    tpl_min_rate = TPL["Net RoL"].iloc[0]

    tpl_max = TPL["CSL"].max()
    tpl_max_rate = TPL["Net RoL"].iloc[-1]

    tpl_limits = TPL["CSL"]
    tpl_rol = TPL["Net RoL"]

    if tpl_limit_usd < tpl_min:
        return tpl_min_rate

    if tpl_limit_usd > tpl_max:
        return tpl_max_rate

    # Find the position of tpl_limit_usd in tpl_limits
    idx = np.searchsorted(tpl_limits, tpl_limit_usd, side="right") - 1

    if idx == len(tpl_limits) - 1 or abs(tpl_limit_usd - tpl_limits[idx]) <= 1e-8:
        return tpl_rol[idx]

    # Linear interpolation
    lower_limit = tpl_limits[idx]
    upper_limit = tpl_limits[idx + 1]
    lower_rate = tpl_rol[idx]
    upper_rate = tpl_rol[idx + 1]

    interpolated_rate = lower_rate + (upper_rate - lower_rate) * ratio(tpl_limit_usd - lower_limit, upper_limit - lower_limit)
    return interpolated_rate

def calculate_fleet_adj(row, size_df = FleetSizeMod):
    # FS 27/08/2025: fleet size adjustment calculator (linear interpolcation)
    size = row["fleet_size"]

    lower = find_closest(df=size_df, column="Fleet Size", lookup_value=size, direction="lower", if_not_found=np.nan, lookup_type="single")
    upper = find_closest(df=size_df, column="Fleet Size", lookup_value=size, direction="upper", if_not_found=np.nan, lookup_type="single")
    if np.isnan(lower) or np.isnan(upper):
        return 0
    
    # Retrieve adjuster values for lower and upper bounds
    Y1 = look_up(lower, "Fleet Size", "Factor", size_df, if_not_found=np.nan, lookup_type="single")
    Y2 = look_up(upper, "Fleet Size", "Factor", size_df, if_not_found=np.nan, lookup_type="single")
    if np.isnan(Y1) or np.isnan(Y2):
        return 0

    # Apply linear interpolation to calculate fleet adjuster value
    if upper == lower:
        adjuster = Y1
    else: 
        adjuster = Y1 + (Y2 - Y1) / (upper - lower) * (size - lower)
    return adjuster

def calculate_build_year_adj(row, year_df = PartialBuildYearMod):
    # FS 27/08/2025: Build year adjustment for partial losses calculator (linear interpolcation)
    year = row["build_year"]

    if year == None or np.isnan(year) or year == 0:
        return 0

    lower = find_closest(df=year_df, column="Year", lookup_value=year, direction="lower", if_not_found=np.nan, lookup_type="single")
    upper = find_closest(df=year_df, column="Year", lookup_value=year, direction="upper", if_not_found=np.nan, lookup_type="single")
    if np.isnan(lower) or np.isnan(upper):
        return 0

    # Condition for min/max adjuster (used when build year is outside the range of the parameter table)
    if lower == 2015 or upper == 1970:
        return look_up(lower, "Year", "Factor", year_df, if_not_found=np.nan, lookup_type="single")

    # Retrieve Adjuster values for lower and upper bounds
    Y1 = look_up(lower, "Year", "Factor", year_df, if_not_found=np.nan, lookup_type="single")
    Y2 = look_up(upper, "Year", "Factor", year_df, if_not_found=np.nan, lookup_type="single")
    if np.isnan(Y1) or np.isnan(Y2):
        return 0

    adjuster = Y1 + (Y2 - Y1) / (upper - lower) * (year - lower)
    return adjuster

### --- ACTUAL RATING --- ###

def rate_ga(hxd):
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    aircrafts = expo.aircrafts
    aircrafts_default = expo.aircrafts_default

    # Useful fields
    inception_date = hxd.hx_core.inception_date
    ccy = hxd.cds.currencies.source_currency
    liability_cvg = cvg.liability.coverage
    hull_brokerage = cvg.hull.brokerage
    liab_brokerage = cvg.liability.brokerage
    hull_quoted_premium = cvg.hull.quoted_premium
    liab_quoted_premium = cvg.liability.quoted_premium

    # Get df with exposure
    aircrafts_df = pd_df_from_hx_list(aircrafts)
    aircrafts_df = aircrafts_df.loc[:, ~aircrafts_df.columns.str.startswith("countries")] # Remove unnecessary columns

    # Validate entries in the table
    validate_table(hxd, aircrafts_df)
    
    # Calculate hull value and deductible
    aircrafts_df["operator_region"] = look_up(aircrafts_df["operator_country"], "Country", "Region GA", OperatorCountryList, if_not_found=np.nan)
    aircrafts_df["value_ccy"] = to_ccy(usd(aircrafts_df["value"], aircrafts_df["hull_ccy"], lookup_type="array").fillna(0), ccy)
    total_value = aircrafts_df.loc[aircrafts_df["include"] == True, "value_ccy"].sum()
    aircrafts_df["per_occ_deductible"] = np.where(
        pd.isna(aircrafts_df["per_occ_deductible"]),
        aircrafts_df[["value", "per_occ_deductible_pct"]].fillna(0).prod(axis=1),
        aircrafts_df["per_occ_deductible"]
    )

    hull_premium_from_rate = 0

    # Combine df and looping to handle overrides correctly
    for idx, ac in enumerate(aircrafts):
        ac.achieved_hull_rate.calculated = ratio(hull_quoted_premium, total_value)
        hull_premium_from_rate += ac.achieved_hull_rate.selected * aircrafts_df["value_ccy"].iloc[idx] * aircrafts_df["include"].iloc[idx].astype(int)

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

    # Calculate seat occupancy and fatality
    aircrafts_df["seat_occupancy"] = aircrafts_df.apply(calculate_seat_occupancy, axis=1)
    aircrafts_df["fatality"] = aircrafts_df.apply(calculate_fatality, axis=1)

    # Check renewing aircrafts
    expiring_aircrafts = json.loads(hxd.rate_change.expiring_aircrafts or "[]")
    aircrafts_df["renewing_aircraft"] = np.where(aircrafts_df["registration"].isin(expiring_aircrafts), "✅", "❌")

    # FS 27/08/2025: Number of engines value assigned based off aircraft selected
    aircrafts_df["number_of_engines"] = aircrafts_df["aircraft_class"].apply(lambda x : None if x == None else ("Multi" if x[-1] == "2" else "Single"))
    
    output_cols = ["number_of_engines", "operator_region", "seat_occupancy", "fatality", "renewing_aircraft"]
    write_pd_to_hxd(aircrafts_df, aircrafts, output_cols, override_cols_to_write=["per_occ_deductible"], replace_nan=True)

    # --- RATING --- #
    
    # Calculate fleet size and check for duplicate registrations
    filtered_regs = aircrafts_df.loc[aircrafts_df["include"] & aircrafts_df["registration"].notna(), "registration"]
    
    expo.fleet_size.calculated = filtered_regs.nunique()
    fleet_size = max(expo.fleet_size.selected, 1)

    if filtered_regs.nunique() < len(filtered_regs):
        expo.has_duplicate_regs = True
        duplicate_mask = filtered_regs.duplicated(keep=False)
        duplicate_indices = (filtered_regs[duplicate_mask].index + 1).tolist()
        
        expo.has_duplicate_regs_msg = f"⚠️ Ensure fleet size is correct. Duplicate registrations found on rows: {', '.join(map(str, duplicate_indices))}."
        
        # Prompt confirmation of fleet size
        if expo.fleet_size.override is None:
            hx.errors.validation("Please confirm the fleet size is correct by overriding the Fleet Size field in Aircraft Details. If the fleet size is already correct, please override it with the same number.")

    # Check for bulk rating
    has_bulk_rating = aircrafts_df[aircrafts_df["include"] & (aircrafts_df["no_of_aircraft"] > 1)].shape[0] > 0

    if has_bulk_rating:
        expo.has_duplicate_regs = True # Using the same node for warning message even though it's not strictly true
        expo.has_duplicate_regs_msg = "⚠️ Aircrafts subject to bulk pricing. Please update the fleet size above."

    # Helper columns
    aircrafts_df["bm_term_adj"] = policy_term(pd.to_datetime(aircrafts_df["attachment_date"]), pd.to_datetime(aircrafts_df["expiry_date"]))

    # Total Loss Freq
    filtered_RateIncrease = RateIncrease[RateIncrease["Year"] <= inception_date.year]
    hull_rate_increase = filtered_RateIncrease["Hull"].iloc[0] if not filtered_RateIncrease["Hull"].empty else 1
    liab_rate_increase = filtered_RateIncrease["Liability"].iloc[0] if not filtered_RateIncrease["Liability"].empty else 1

    aircrafts_df["base_rate"] = look_up(aircrafts_df["aircraft_class"], "Total Loss EL Rates", "Paramater", TotalFreqBase, if_not_found=0)
    aircrafts_df["base_freq_all_aircraft"] = aircrafts_df[["base_rate", "no_of_aircraft"]].prod(axis=1, skipna=True)
    aircrafts_df["hull_value_usd"] = usd(aircrafts_df["value"], aircrafts_df["hull_ccy"], lookup_type="array").fillna(0)
    aircrafts_df["hull_value_adjuster"] = aircrafts_df.apply(calculate_hull_value_adj, axis=1)
    aircrafts_df["status_adjuster"] = aircrafts_df["time_in_service"].fillna(0) * look_up("In-Service", "Status", "Class", StatusMod, lookup_type="single") + \
        (1 - aircrafts_df["time_in_service"]).fillna(0) * look_up("Storage", "Status", "Class", StatusMod, lookup_type="single")
    aircrafts_df["build_location_adjuster"] = look_up(aircrafts_df["build_location"], "Build Location", "Paramater", BuildLocationMod, if_not_found=1)
    # FS 27/08/2025: Utilising new region categories to calculate region adjuster
    aircrafts_df["frequency_region"] = look_up(aircrafts_df["operator_country"], "Country", "Region GA Frequency", OperatorCountryList, if_not_found=np.nan)
    aircrafts_df["region_adjuster"] = look_up(aircrafts_df["frequency_region"], "Country", "Adjuster", RegionMod, if_not_found=0)
    aircrafts_df["use_adjuster"] = look_up(aircrafts_df["use"], "Use", "Adjuster", UseMod, if_not_found=0)
    
    # FS 27/08/2025: Updated calculation for fleet size adjuster
    aircrafts_df["fleet_size"] = fleet_size
    aircrafts_df["fleet_size_adjuster"] = aircrafts_df.apply(calculate_fleet_adj, axis = 1)
    exp_losses_cols = ["base_freq_all_aircraft", "hull_value_adjuster", "status_adjuster", "build_location_adjuster", "region_adjuster", "use_adjuster", "fleet_size_adjuster"]
    aircrafts_df["exp_total_losses"] = aircrafts_df[exp_losses_cols].prod(skipna=True, axis=1) * hull_rate_increase
    aircrafts_df["partial_conversion"] = look_up(aircrafts_df["aircraft_class"],"Type", "Factor", PartialConversion, if_not_found=0)
    aircrafts_df["exp_partial_losses"] = aircrafts_df[["exp_total_losses", "partial_conversion"]].prod(skipna=True, axis=1)

    # Hull Rating

    # Total Loss
    aircrafts_df["hull_per_occ_deductible_usd"] = usd(aircrafts_df["per_occ_deductible"], aircrafts_df["hull_ccy"], lookup_type="array").fillna(0)
    aircrafts_df["hull_severity"] = np.where(aircrafts_df["hull_value_usd"] > 0, aircrafts_df["hull_value_usd"] - aircrafts_df["hull_per_occ_deductible_usd"], 0)
    aircrafts_df["hull_severity"] = aircrafts_df[["hull_severity","bm_term_adj"]].prod(skipna=True, axis=1)
    # FS 27/08/2025: Total loss calculated seperately
    aircrafts_df["hull_total_loss_unadjusted"] = aircrafts_df[["hull_severity", "exp_total_losses"]].prod(skipna=True, axis=1)
    
    # FS 27/08/2025: Partial loss calculations added
    aircrafts_df["hull_partial_base_severity"] = PartialBaseSeverity["Base Severity"].iloc[0]
    aircrafts_df["hull_partial_engine_adjuster"] = look_up(aircrafts_df["number_of_engines"],"Engine","Factor",PartialEngineMod,if_not_found=0)
    aircrafts_df["hull_partial_build_year_adjuster"] = aircrafts_df.apply(calculate_build_year_adj, axis = 1)
    aircrafts_df["hull_partial_loss_unadjusted"] = aircrafts_df[["exp_partial_losses","hull_severity", "hull_partial_base_severity", "hull_partial_engine_adjuster", "hull_partial_build_year_adjuster"]].prod(skipna=True, axis = 1)

    # FS 04/09/2025: Partial loss validation
     

    # FS 27/08/2025: Expected loss calculation altered to allow for partial losses as well as total losses
    aircrafts_df["hull_expected_loss_unadjusted"] = aircrafts_df[["hull_total_loss_unadjusted","hull_partial_loss_unadjusted"]].sum(skipna=True, axis = 1)
    aircrafts_df["hull_attritional_adjuster"] = HullAttr["Paramater"].iloc[0]
    aircrafts_df["hull_expected_loss"] = aircrafts_df[["hull_expected_loss_unadjusted", "hull_attritional_adjuster"]].prod(skipna=True, axis=1)
    aircrafts_df["hull_benchmark_cost"] = ratio(ratio(aircrafts_df["hull_expected_loss"], benchmark_lr), 1 - hull_brokerage)
    aircrafts_df["hull_net_rate"] = ratio(aircrafts_df["hull_expected_loss"], aircrafts_df[["hull_value_usd", "no_of_aircraft"]].prod(skipna=True, axis=1))
    aircrafts_df["hull_benchmark_rate"] = ratio(aircrafts_df["hull_benchmark_cost"], aircrafts_df[["hull_value_usd", "no_of_aircraft"]].prod(skipna=True, axis=1))

    # PAX Rating
    aircrafts_df["freq_region"] = look_up(aircrafts_df["operator_region"], "Region Detailed", "Region", Region)
    aircrafts_df["pax_freq_adjustment"] =  aircrafts_df.apply(
        lambda x: (
            LiabFreqAdj[LiabFreqAdj["Country"] == x["freq_region"]].loc[:, x["aircraft_class"]].iloc[0]
            if pd.notna(x["freq_region"]) and pd.notna(x["aircraft_class"]) else 0
        ),
        axis=1
    )
    aircrafts_df["pax_exp_total_losses"] = aircrafts_df[["exp_total_losses", "pax_freq_adjustment"]].prod(axis=1, skipna=True) * ratio(liab_rate_increase, hull_rate_increase)
    aircrafts_df["total_seats_all_aircraft"] = aircrafts_df["no_of_aircraft"].fillna(0) * aircrafts_df["total_seats"].fillna(0)
    aircrafts_df["exp_no_of_deaths"] = aircrafts_df[["total_seats", "seat_occupancy", "fatality"]].prod(axis=1, skipna=True)
    aircrafts_df["pax_award_usd"] = look_up(aircrafts_df["operator_region"], "Country", "Passenger Awards (USD)", PAXAward) * look_up(aircrafts_df["pax_net_worth"], "Net Worth", "Adjutments", PAXNetWorth, if_not_found=1)
    aircrafts_df["pax_limit_usd"] = np.where(
        pd.isna(aircrafts_df["per_pax_liab_limit"]), np.nan, usd(aircrafts_df["per_pax_liab_limit"], aircrafts_df["liability_ccy"], lookup_type="array")
    )
    aircrafts_df["apply_pax_limit"] = np.where(
        pd.isna(aircrafts_df["pax_limit_usd"]), aircrafts_df["pax_award_usd"], np.where(
            pd.isna(aircrafts_df["pax_award_usd"]), aircrafts_df["pax_limit_usd"], np.minimum(aircrafts_df["pax_award_usd"], aircrafts_df["pax_limit_usd"])
        )
    )
    aircrafts_df["gu_pax_losses"] = aircrafts_df["apply_pax_limit"] * aircrafts_df["exp_no_of_deaths"] * (1 - ratio(aircrafts_df["crew_seats"], aircrafts_df["total_seats"]))
    aircrafts_df["max_pax_losses"] = aircrafts_df[["apply_pax_limit", "exp_no_of_deaths"]].prod(axis=1, skipna=True)
    aircrafts_df["pax_per_occ_limit_usd"] = usd(aircrafts_df["combined_single_limit"], aircrafts_df["liability_ccy"], lookup_type="array").fillna(0)
    aircrafts_df["pax_apply_occ_limit_ded"] = np.minimum(aircrafts_df["gu_pax_losses"], aircrafts_df["pax_per_occ_limit_usd"])
    aircrafts_df["pax_apply_occ_limit_ded_to_max_loss"] = np.minimum(aircrafts_df["max_pax_losses"], aircrafts_df["pax_per_occ_limit_usd"])
    aircrafts_df["pax_apply_occ_limit_ded_to_max_loss"] = aircrafts_df[["pax_apply_occ_limit_ded_to_max_loss", "bm_term_adj"]].prod(axis=1, skipna=True)
    aircrafts_df["pax_exp_loss_from_total_losses"] = aircrafts_df[["pax_exp_total_losses", "pax_apply_occ_limit_ded"]].prod(axis=1, skipna=True)
    aircrafts_df["pax_attritional_adjuster"] = LiabAttr["Paramater"].iloc[0]
    aircrafts_df["pax_expected_loss"] = aircrafts_df[["pax_exp_loss_from_total_losses", "pax_attritional_adjuster"]].prod(axis=1, skipna=True)
    aircrafts_df["pax_benchmark_cost"] = ratio(ratio(aircrafts_df["pax_expected_loss"], benchmark_lr), 1 - liab_brokerage)
    aircrafts_df["pax_benchmark_per_seat"] = ratio(
        aircrafts_df["pax_benchmark_cost"], 
        aircrafts_df["total_seats_all_aircraft"] * (1 - ratio(aircrafts_df["crew_seats"], aircrafts_df["total_seats"]))
    )

    # TPL Rating
    aircrafts_df["tpl_limit_usd"] = usd(aircrafts_df["combined_single_limit"], aircrafts_df["liability_ccy"], lookup_type="array").fillna(0)
    aircrafts_df["tpl_net_rol_exposed"] = aircrafts_df.apply(calculate_tpl_rol, axis=1)
    aircrafts_df["tpl_net_rol_unexposed"] = TPLUnexposedRate["TPL Unexposed Rate"].iloc[0]
    aircrafts_df["tpl_net_rol"] = aircrafts_df["tpl_limit_exposed"].fillna(0) * aircrafts_df["tpl_net_rol_exposed"] + (1 - aircrafts_df["tpl_limit_exposed"].fillna(0)) * aircrafts_df["tpl_net_rol_unexposed"]
    aircrafts_df["tpl_expected_loss_unadjusted"] = aircrafts_df[["tpl_net_rol", "tpl_limit_usd", "no_of_aircraft"]].prod(axis=1, skipna=True)
    aircrafts_df["tpl_expected_loss"] = aircrafts_df[["tpl_expected_loss_unadjusted", "fleet_size_adjuster", "bm_term_adj"]].prod(axis=1, skipna=True) * liab_rate_increase
    aircrafts_df["tpl_benchmark_cost"] = ratio(ratio(aircrafts_df["tpl_expected_loss"], benchmark_lr), 1 - liab_brokerage)
    aircrafts_df["tpl_net_rate"] = ratio(aircrafts_df["tpl_expected_loss"], aircrafts_df["tpl_limit_usd"])
    aircrafts_df["tpl_gross_rate"] = ratio(aircrafts_df["tpl_benchmark_cost"], aircrafts_df["tpl_limit_usd"])

    # Push to hxd
    # FS 27/08/2025: Additional output columns added for validating partial loss calculation
    output_cols = [
        "include",
        "bm_term_adj",
        "aircraft_class",
        "base_rate",
        "base_freq_all_aircraft",
        "hull_value_usd",
        "hull_value_adjuster",
        "status_adjuster",
        "build_location",
        "build_location_adjuster",
        "freq_region",
        "use",
        "region_adjuster",
        "use_adjuster",
        "fleet_size",
        "fleet_size_adjuster",
        "exp_total_losses",
        "exp_partial_losses",
        "hull_per_occ_deductible_usd",
        "hull_severity",
        "hull_partial_base_severity",
        "hull_partial_engine_adjuster",
        "hull_partial_build_year_adjuster",
        "hull_total_loss_unadjusted",
        "hull_partial_loss_unadjusted",
        "hull_expected_loss_unadjusted",
        "hull_attritional_adjuster",
        "hull_expected_loss",
        "hull_benchmark_cost",
        "hull_net_rate",
        "hull_benchmark_rate",
        "pax_exp_total_losses",
        "total_seats_all_aircraft",
        "seat_occupancy",
        "fatality",
        "exp_no_of_deaths",
        "operator_region",
        "pax_award_usd",
        "pax_limit_usd",
        "apply_pax_limit",
        "gu_pax_losses",
        "max_pax_losses",
        "pax_per_occ_limit_usd",
        "pax_apply_occ_limit_ded",
        "pax_apply_occ_limit_ded_to_max_loss",
        "pax_exp_loss_from_total_losses",
        "pax_attritional_adjuster",
        "pax_expected_loss",
        "pax_benchmark_cost",
        "pax_benchmark_per_seat",
        "tpl_limit_usd",
        "tpl_limit_exposed",
        "tpl_net_rol_exposed",
        "tpl_net_rol_unexposed",
        "tpl_expected_loss_unadjusted",
        "tpl_expected_loss",
        "tpl_benchmark_cost",
        "tpl_net_rate",
        "tpl_gross_rate"
    ]

    expo.ga_rating = aircrafts_df[["include", "no_of_aircraft", "total_seats", "time_in_service"]].fillna(0).to_dict("records")
    aircrafts_df = aircrafts_df.fillna(np.nan).replace([np.nan], [None])
    write_pd_to_hxd(aircrafts_df, expo.ga_rating, output_cols)

    # --- Aircraft Summary --- #

    # Push to hxd
    expo.aircraft_summary = aircrafts_df[["include", "no_of_aircraft", "aircraft_class", "registration"]].fillna(0).to_dict("records")

    aircrafts_df["hull_value"] = to_ccy(aircrafts_df["hull_value_usd"], ccy)
    aircrafts_df["hull_benchmark"] = to_ccy(aircrafts_df["hull_benchmark_cost"], ccy)
    aircrafts_df["hull_benchmark_rate"] = aircrafts_df["hull_benchmark_rate"]
    aircrafts_df["pax_limit"] = (aircrafts_df["no_of_aircraft"] * to_ccy(aircrafts_df["pax_per_occ_limit_usd"], ccy)).fillna(0)
    aircrafts_df["pax_liab_benchmark"] = to_ccy(aircrafts_df["pax_benchmark_cost"], ccy)
    aircrafts_df["pax_liab_benchmark_per_seat"] = to_ccy(aircrafts_df["pax_benchmark_per_seat"], ccy)
    aircrafts_df["tpl_benchmark"] = to_ccy(aircrafts_df["tpl_benchmark_cost"], ccy)
    aircrafts_df["total_hull_benchmark"] = aircrafts_df["hull_benchmark"]
    aircrafts_df["total_liab_benchmark"] = aircrafts_df[["pax_liab_benchmark", "tpl_benchmark"]].sum(axis=1)
    aircrafts_df["total_benchmark"] = aircrafts_df[["total_hull_benchmark", "total_liab_benchmark"]].sum(axis=1)
   
    as_output_cols = [
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

    write_pd_to_hxd(aircrafts_df, expo.aircraft_summary, as_output_cols)

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
        total_sum = aircrafts_df.loc[aircrafts_df["include"], col].sum()
        setattr(tot, col, total_sum)

    tot.hull_value = np.dot(aircrafts_df[aircrafts_df["include"] == True]["no_of_aircraft"].fillna(0), aircrafts_df[aircrafts_df["include"] == True]["hull_value"])
    tot.hull_benchmark_rate = ratio(tot.hull_benchmark, tot.hull_value)
    tot.pax_limit = aircrafts_df["pax_limit"].max()

    aircrafts_df["crew_seats_all_aircraft"] = aircrafts_df[["no_of_aircraft", "crew_seats"]].prod(axis=1, skipna=True)
    total_seats_in_service = (aircrafts_df.loc[aircrafts_df["include"], "total_seats_all_aircraft"] - aircrafts_df.loc[aircrafts_df["include"], "crew_seats_all_aircraft"]).sum()
    tot.pax_liab_benchmark_per_seat = ratio(tot.pax_liab_benchmark, total_seats_in_service)

    # Result columns in Aircraft Details
    aircrafts_df["bm_allocated_hull_premium"] = hull_quoted_premium * ratio(aircrafts_df["total_hull_benchmark"], aircrafts_df["total_hull_benchmark"].sum())
    aircrafts_df["bm_allocated_liab_premium"] = liab_quoted_premium * ratio(aircrafts_df["total_liab_benchmark"], aircrafts_df["total_liab_benchmark"].sum())

    result_cols = [
        "hull_benchmark_rate",
        "pax_liab_benchmark_per_seat",
        "tpl_benchmark",
        "total_hull_benchmark",
        "total_liab_benchmark",
        "bm_allocated_hull_premium",
        "bm_allocated_liab_premium"
    ]
    write_pd_to_hxd(aircrafts_df, aircrafts, result_cols)

    return aircrafts_df, 0 # Adding 0 to match return structure of rate_airlines()
    