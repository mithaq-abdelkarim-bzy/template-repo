import hx
import pandas as pd
import numpy as np
import traceback
from algorithms.rate_ux import fill_check_columns
from algorithms.rate_utilities import ratio, one_layer, pd_df_from_hx_list, write_pd_to_hxd, usd, validate_empty_fields
from algorithms.rate_utilities import find_closest, look_up_closest, look_up
from algorithms.rate_utilities import calculate_logit, calculate_approx_lx, calculate_qx, calculate_exp_params, calculate_x_value, calculate_r1, calculate_ci_exp_param
from algorithms.rate_constants import benchmark_lr,uk_qx_adjustment

# Initialise param tables - defined as global variables for multiple functions to use
tblStandardLife = hx.params.tblStandardLife
tblCountryFactor = hx.params.tblCountryFactor
tblAgeFactor = hx.params.tblAgeFactor
tblRefPoints = hx.params.tblRefPoints
tblRepat = hx.params.tblRepat
tblCI_UK_base_rate = hx.params.tblCI_UK_base_rate
TI_proportions = hx.params.TI_proportions
tblInsuredAdj = hx.params.tblInsuredAdj
tblOccupation = hx.params.tblOccupation
lifeDevelopingCountryadj = hx.params.lifeDevelopingCountryadj
tblCauseSplit = hx.params.tblCauseSplit
life_CauseSplitIntercept = hx.params.life_CauseSplitIntercept
life_CauseSplitCoeff = hx.params.life_CauseSplitCoeff
tblXfactor = hx.params.tblXfactor
tblAgeBand = hx.params.tblAgeBand
lstCountry = hx.params.lstCountry
tblRegionRates = hx.params.tblRegionRates
tblCI_multiplier_pivoted = hx.params.tblCI_multiplier_pivoted

# Intial calcs
def calculate_sum_insured(hxd):

    expo = hxd.cds.exposure.granular
    lives = expo.lives

    [setattr(life, "sum_insured", life.no_lives * life.salary * life.salary_multiple) for life in lives]

# For map chart
def aggregate_lives(hxd):

    expo = hxd.cds.exposure.granular

    if not expo.show_exposure_map:
        return

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)
    lives_df = lives_df[["no_lives", "sum_insured", "nationality", "location"]]

    # Calculate total_sum_insured
    lives_df["total_sum_insured"] = lives_df["sum_insured"] # "sum_insured" field is already the total (= no_lives * salary * salary_multiple)

    # Extract columns
    lives_df_nat = lives_df[["no_lives", "sum_insured", "nationality", "total_sum_insured"]]
    lives_df_loc = lives_df[["no_lives", "sum_insured", "location", "total_sum_insured"]]

    # Aggregate the sum insured and total sum insured by nationality
    agg_exposure_df_nat = lives_df_nat.groupby("nationality").agg(
        total_sum_insured=pd.NamedAgg(column="total_sum_insured", aggfunc="sum"),
        sum_insured=pd.NamedAgg(column="sum_insured", aggfunc="sum"),
        no_lives=pd.NamedAgg(column="no_lives", aggfunc="sum")
    ).reset_index()

    agg_exposure_df_nat["country_iso3"] = look_up(
        lookup_value = agg_exposure_df_nat["nationality"],
        lookup_col="lstCountry",
        return_col="ISO3",
        df=lstCountry
    )

    # Aggregate the sum insured and total sum insured by location
    agg_exposure_df_loc = lives_df_loc.groupby("location").agg(
        total_sum_insured=pd.NamedAgg(column="total_sum_insured", aggfunc="sum"),
        sum_insured=pd.NamedAgg(column="sum_insured", aggfunc="sum"),
        no_lives=pd.NamedAgg(column="no_lives", aggfunc="sum")
    ).reset_index()

    agg_exposure_df_loc["country_iso3"] = look_up(
        lookup_value = agg_exposure_df_loc["location"],
        lookup_col="lstCountry",
        return_col="ISO3",
        df=lstCountry
    )

    # Push to hxd
    expo.lives_by_nation = agg_exposure_df_nat.to_dict("records")
    expo.lives_by_location = agg_exposure_df_loc.to_dict("records")


### --- COVERAGE-SPECIFIC RATING --- ###
def rate_db_or_ti(hxd, lives_df, which):
    layer, cvg = one_layer(hxd)
    db = cvg.death
    ti = cvg.terminal_illness

    # Policy details
    cover_type = db.cover_type
    accidental_death_adj = db.accidental_death_adj
    sick_weight_to_nationality = db.sick_weight_to_nationality
    sick_affluence = db.sick_affluence
    accidental_death_rate = db.accidental_death_rate
    has_terminal_illness = ti.is_covered

    if which == "db":
        age_col = "age_attained"
    elif which == "ti":
        # Set-up
        lives_df["ti_cover"] = has_terminal_illness * (lives_df["age_attained"] <= 70) * (lives_df["age_attained"] >= 18)
        lives_df["age_attained_plus1"] = lives_df["age_attained"] + 1
        age_col = "age_attained_plus1"
    else:
        raise ValueError("which must be either 'db' or 'ti'")

    lives_df["S_age_actual_Actual_Age_group"] = look_up_closest(lives_df[age_col], "Age (lower bound)", "Age Band", tblAgeBand)
    lives_df["S_age_actual_Nominal_average_age"] = look_up(lives_df["S_age_actual_Actual_Age_group"], "Age Band", "Average age", tblAgeBand)
    lives_df["S_age_above_Age_group_above"] = look_up_closest(lives_df[age_col], "Age (lower bound)", "Age Band", tblAgeBand, direction="higher")
    lives_df["S_age_above_Nominal_average_age"] = look_up(lives_df["S_age_above_Age_group_above"], "Age Band", "Average age", tblAgeBand)
    lives_df["S_age_plus2_Age_Group_+2/-1"] = np.where(
        (lives_df[age_col]) >= lives_df["S_age_actual_Nominal_average_age"],
        look_up_closest(lives_df["S_age_above_Nominal_average_age"], "Average age", "Age Band", tblAgeBand, direction="higher"),
        look_up_closest(lives_df["S_age_above_Nominal_average_age"], "Average age", "Age Band", tblAgeBand, direction="lower", distance=3)
    )
    lives_df["S_age_plus2_Nominal_average_age"] = look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age Band", "Average age", tblAgeBand)

    lives_df["S_g&t_actual_Gamma"] = look_up(lives_df["S_age_actual_Actual_Age_group"], "Age", "gamma", tblAgeFactor)
    lives_df["S_g&t_actual_Theta"] = look_up(lives_df["S_age_actual_Actual_Age_group"], "Age", "theta", tblAgeFactor)
    lives_df["S_g&t_above_Gamma"] = look_up(lives_df["S_age_above_Age_group_above"], "Age", "gamma", tblAgeFactor)
    lives_df["S_g&t_above_Theta"] = look_up(lives_df["S_age_above_Age_group_above"], "Age", "theta", tblAgeFactor)
    lives_df["S_g&t_plus2_Gamma"] = look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age", "gamma", tblAgeFactor)
    lives_df["S_g&t_plus2_Theta"] = look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age", "theta", tblAgeFactor)
    lives_df["S_adj_actual_Ultimate_to_Duration"] = np.where(
        lives_df["sex"] == "M", 
        look_up(lives_df["S_age_actual_Actual_Age_group"], "Age Band_shifted", "M", tblInsuredAdj),
        look_up(lives_df["S_age_actual_Actual_Age_group"], "Age Band_shifted", "F", tblInsuredAdj) # Assuming values in Sex can only be M or F
    )
    lives_df["S_adj_above_Ultimate_to_Duration"] = np.where(
        lives_df["sex"] == "M", 
        look_up(lives_df["S_age_above_Age_group_above"], "Age Band_shifted", "M", tblInsuredAdj),
        look_up(lives_df["S_age_above_Age_group_above"], "Age Band_shifted", "F", tblInsuredAdj) # Assuming values in Sex can only be M or F
    )
    lives_df["S_adj_plus2_Ultimate_to_Duration"] = np.where(
        lives_df["sex"] == "M", 
        look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age Band_shifted", "M", tblInsuredAdj),
        look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age Band_shifted", "F", tblInsuredAdj) # Assuming values in Sex can only be M or F
    )

    # Nationality
    nationality = pd.Series(["United Kingdom"] * len(lives_df), index=lives_df.index) if sick_affluence else lives_df["nationality"]

    lives_df["N_a&b_0_Decode_(Nationality&sex)"] = nationality + np.where(lives_df["sex"] == "M", "Male", "Female")
    lives_df["N_a&b_0_Alpha"] = look_up(lives_df["N_a&b_0_Decode_(Nationality&sex)"], "CountrySex", "alpha", tblCountryFactor)
    lives_df["N_a&b_0_Beta"] = look_up(lives_df["N_a&b_0_Decode_(Nationality&sex)"], "CountrySex", "beta", tblCountryFactor)
    lives_df["N_a&b_0_logit_(l(20-24))"] = look_up(lives_df["N_a&b_0_Decode_(Nationality&sex)"], "CountrySex", "logit (l(20-24))", tblCountryFactor)
    lives_df["N_a&b_0_logit_(l(65-69))"] = look_up(lives_df["N_a&b_0_Decode_(Nationality&sex)"], "CountrySex", "logit (l(65-69))", tblCountryFactor)
    lives_df["N_a&b_0_factor_for_dev_country"] = np.where(
        look_up(nationality, "lstCountry", "lstDevelopingIndicator", lstCountry) == 0, 1, lifeDevelopingCountryadj["ValueD"].iloc[0]
    )
    lives_df["N_lx_actual_logit(l(x))"] = look_up(lives_df["S_age_actual_Actual_Age_group"], "Age band", "logit(l(x))", tblStandardLife)
    lives_df["N_lx_actual_Logit_(lx)"] = calculate_logit(
        lives_df["N_a&b_0_Alpha"], lives_df["N_a&b_0_Beta"], lives_df["N_lx_actual_logit(l(x))"],
        lives_df["S_g&t_actual_Gamma"], lives_df["N_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_actual_Theta"], lives_df["N_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["N_lx_actual_Approx_l(x)"] = calculate_approx_lx(lives_df["N_lx_actual_Logit_(lx)"])
    lives_df["N_lx_above_logit(l(x))"] = look_up(lives_df["S_age_above_Age_group_above"], "Age band", "logit(l(x))", tblStandardLife)
    lives_df["N_lx_above_Logit_(lx)"] = calculate_logit(
        lives_df["N_a&b_0_Alpha"], lives_df["N_a&b_0_Beta"], lives_df["N_lx_above_logit(l(x))"],
        lives_df["S_g&t_above_Gamma"], lives_df["N_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_above_Theta"], lives_df["N_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["N_lx_above_Approx_l(x)"] = calculate_approx_lx(lives_df["N_lx_above_Logit_(lx)"])
    lives_df["N_lx_plus2_logit(l(x))"] = look_up(lives_df["S_age_plus2_Age_Group_+2/-1"], "Age band", "logit(l(x))", tblStandardLife)
    lives_df["N_lx_plus2_Logit_(lx)"] = calculate_logit(
        lives_df["N_a&b_0_Alpha"], lives_df["N_a&b_0_Beta"], lives_df["N_lx_plus2_logit(l(x))"],
        lives_df["S_g&t_plus2_Gamma"], lives_df["N_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_plus2_Theta"], lives_df["N_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["N_lx_plus2_Approx_l(x)"] = calculate_approx_lx(lives_df["N_lx_plus2_Logit_(lx)"])
    lives_df["N_qx_0_Qx_lower"] = calculate_qx(lives_df, which="lower", prefix="N")
    lives_df["N_qx_0_Qx_upper"] = calculate_qx(lives_df, which="upper", prefix="N")
    lives_df["N_qx_0_c_calue"] = calculate_exp_params(lives_df, which="c", prefix="N")
    lives_df["N_qx_0_B_value"] = calculate_exp_params(lives_df, which="b", prefix="N")
    lives_df["N_qx_0_x_value"] = calculate_x_value(lives_df, age_col=age_col)
    lives_df["N_qx_0_Qx_pure"] = lives_df["N_qx_0_c_calue"] * np.exp(lives_df["N_qx_0_B_value"] * lives_df["N_qx_0_x_value"])
    lives_df["N_qx_0_Occupation_modifier"] = look_up(lives_df["occupation_code"], "Occupation code", "Modifier", tblOccupation)
    # Yifei: 27/01/2026: Add UK adjustment for mortality
    lives_df["N_uk_mortality_adjustment"] = np.where(lives_df["nationality"] == "United Kingdom", uk_qx_adjustment, 1)
    lives_df["N_qx_0_Base_rate_for_Nationality"] = lives_df["N_qx_0_Qx_pure"] * 1000 * lives_df["N_qx_0_Occupation_modifier"] * lives_df["N_uk_mortality_adjustment"]

    # Location
    lives_df["L_a&b_0_Decode_(Location&sex)"] = lives_df["location"] + np.where(lives_df["sex"] == "M", "Male", "Female")
    lives_df["L_a&b_0_Alpha"] = look_up(lives_df["L_a&b_0_Decode_(Location&sex)"], "CountrySex", "alpha", tblCountryFactor)
    lives_df["L_a&b_0_Beta"] = look_up(lives_df["L_a&b_0_Decode_(Location&sex)"], "CountrySex", "beta", tblCountryFactor)
    lives_df["L_a&b_0_logit_(l(20-24))"] = look_up(lives_df["L_a&b_0_Decode_(Location&sex)"], "CountrySex", "logit (l(20-24))", tblCountryFactor)
    lives_df["L_a&b_0_logit_(l(65-69))"] = look_up(lives_df["L_a&b_0_Decode_(Location&sex)"], "CountrySex", "logit (l(65-69))", tblCountryFactor)
    lives_df["L_a&b_0_factor_for_dev_country"] = np.where(
        look_up(lives_df["location"], "lstCountry", "lstDevelopingIndicator", lstCountry) == 0, 1, lifeDevelopingCountryadj["ValueD"].iloc[0]
    )
    lives_df["L_lx_actual_logit(l(x))"] = lives_df["N_lx_actual_logit(l(x))"]
    lives_df["L_lx_actual_Logit_(lx)"] = calculate_logit(
        lives_df["L_a&b_0_Alpha"], lives_df["L_a&b_0_Beta"], lives_df["L_lx_actual_logit(l(x))"],
        lives_df["S_g&t_actual_Gamma"], lives_df["L_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_actual_Theta"], lives_df["L_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["L_lx_actual_Approx_l(x)"] = calculate_approx_lx(lives_df["L_lx_actual_Logit_(lx)"])
    lives_df["L_lx_above_logit(l(x))"] = lives_df["N_lx_above_logit(l(x))"]
    lives_df["L_lx_above_Logit_(lx)"] = calculate_logit(
        lives_df["L_a&b_0_Alpha"], lives_df["L_a&b_0_Beta"], lives_df["L_lx_above_logit(l(x))"],
        lives_df["S_g&t_above_Gamma"], lives_df["L_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_above_Theta"], lives_df["L_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["L_lx_above_Approx_l(x)"] = calculate_approx_lx(lives_df["L_lx_above_Logit_(lx)"])
    lives_df["L_lx_plus2_logit(l(x))"] = lives_df["N_lx_plus2_logit(l(x))"]
    lives_df["L_lx_plus2_Logit_(lx)"] = calculate_logit(
        lives_df["L_a&b_0_Alpha"], lives_df["L_a&b_0_Beta"], lives_df["L_lx_plus2_logit(l(x))"],
        lives_df["S_g&t_plus2_Gamma"], lives_df["L_a&b_0_logit_(l(20-24))"], lives_df["S_g&t_plus2_Theta"], lives_df["L_a&b_0_logit_(l(65-69))"],
        tblRefPoints
    )
    lives_df["L_lx_plus2_Approx_l(x)"] = calculate_approx_lx(lives_df["L_lx_plus2_Logit_(lx)"])
    lives_df["L_qx_0_Qx_lower"] = calculate_qx(lives_df, which="lower", prefix="L")
    lives_df["L_qx_0_Qx_upper"] = calculate_qx(lives_df, which="upper", prefix="L")
    lives_df["L_qx_0_c_calue"] = calculate_exp_params(lives_df, which="c", prefix="L")
    lives_df["L_qx_0_B_value"] = calculate_exp_params(lives_df, which="b", prefix="L")
    lives_df["L_qx_0_x_value"] = lives_df["N_qx_0_x_value"]
    lives_df["L_qx_0_Qx_pure"] = lives_df["L_qx_0_c_calue"] * np.exp(lives_df["L_qx_0_B_value"] * lives_df["L_qx_0_x_value"])
    lives_df["L_qx_0_Occupation_modifier"] = lives_df["N_qx_0_Occupation_modifier"]
    # Yifei: 27/01/2026: Add UK adjustment for mortality
    lives_df["L_uk_mortality_adjustment"] = np.where(lives_df["location"] == "United Kingdom", uk_qx_adjustment, 1)
    lives_df["L_qx_0_Base_rate_for_Location"] = lives_df["L_qx_0_Qx_pure"] * 1000 * lives_df["L_qx_0_Occupation_modifier"] * lives_df["L_uk_mortality_adjustment"]

    # Blending mortality rates
    lives_df["B_nat_nation_Parameter_m"] = look_up(accidental_death_rate, "Group", "Parameter, m", tblCauseSplit, lookup_type="single")
    lives_df["B_nat_nation_R1"] = calculate_r1(lives_df, life_CauseSplitCoeff, life_CauseSplitIntercept, age_col=age_col)
    lives_df["B_nat_nation_q_(Non-natural)"] = lives_df["B_nat_nation_R1"] * lives_df["N_qx_0_Base_rate_for_Nationality"]
    lives_df["B_nat_nation_q_(Natural)"] = (1-lives_df["B_nat_nation_R1"]) * lives_df["N_qx_0_Base_rate_for_Nationality"]
    lives_df["B_nat_loc_Parameter_m"] = lives_df["B_nat_nation_Parameter_m"]
    lives_df["B_nat_loc_R2"] = lives_df["B_nat_nation_R1"]
    lives_df["B_nat_loc_q_(Non-natural)"] = lives_df["B_nat_loc_R2"] * lives_df["L_qx_0_Base_rate_for_Location"]
    lives_df["B_nat_loc_q(Natural)"] = (1-lives_df["B_nat_loc_R2"]) * lives_df["L_qx_0_Base_rate_for_Location"]
    lives_df["B_nat_blend_f(location,occupation)"] = look_up(lives_df["occupation_code"], "Occupation code", accidental_death_adj, tblXfactor)
    lives_df["B_nat_blend_q(Natural_only)"] = sick_weight_to_nationality * lives_df["B_nat_nation_q_(Natural)"] + (1-sick_weight_to_nationality) * lives_df["B_nat_loc_q(Natural)"]
    lives_df["B_nat_blend_q(Non-natural_only)"] = lives_df["B_nat_loc_q_(Non-natural)"] * lives_df["B_nat_blend_f(location,occupation)"]

    # Region Factor
    lives_df["Region_lookup"] = lives_df["location"].astype(str) + lives_df["region"].astype(str) + lives_df["sex"].astype(str)
    lives_df["Region_factor"] = look_up(lives_df["Region_lookup"],"Lookup","Factor",tblRegionRates,1)

    if which == "db":
        lives_df["db_qx"] = (lives_df["B_nat_blend_q(Natural_only)"] if cover_type == "Nat Cause" else lives_df["B_nat_blend_q(Natural_only)"] + lives_df["B_nat_blend_q(Non-natural_only)"])*lives_df["Region_factor"]
    elif which == "ti":
        lives_df["ti_qx"] = lives_df["B_nat_blend_q(Natural_only)"] # Terminal illness only uses natural mortality even when "Any Cause" is covered

    return lives_df


def rate_ci(hxd, lives_df):
    layer, cvg = one_layer(hxd)
    ci = cvg.critical_illness
    has_critical_illness = ci.is_covered

    # Calculate premium
    lives_df["ci_cover"] = has_critical_illness * (lives_df["age_attained"] <= 64) * (lives_df["age_attained"] >= 18)
    lives_df["ci_age_band_min"] = look_up_closest(lives_df["age_attained"], "Age", "Age", tblCI_UK_base_rate, direction="lower")
    lives_df["ci_age_band_max"] = look_up_closest(lives_df["age_attained"], "Age", "Age", tblCI_UK_base_rate, direction="higher")
    lives_df["ci_uk_base_rate_lower_age"] = np.where(
        lives_df["sex"] == "M", 
        look_up(lives_df["ci_age_band_min"], "Age", "M", tblCI_UK_base_rate) / 10,
        look_up(lives_df["ci_age_band_min"], "Age", "F", tblCI_UK_base_rate) / 10
    )
    lives_df["ci_uk_base_rate_upper_age"] = np.where(
        lives_df["sex"] == "M", 
        look_up(lives_df["ci_age_band_max"], "Age", "M", tblCI_UK_base_rate) / 10,
        look_up(lives_df["ci_age_band_max"], "Age", "F", tblCI_UK_base_rate) / 10
    )
    lives_df["ci_multiplier_lookup_lower"] = lives_df[["sex", "location", "ci_age_band_min"]].astype(str).agg("".join, axis=1)
    lives_df["ci_multiplier_lookup_upper"] = lives_df[["sex", "location", "ci_age_band_max"]].astype(str).agg("".join, axis=1)
    lives_df["ci_multiplier_lower_age"] = look_up(lives_df["ci_multiplier_lookup_lower"], "SCA", "Value", tblCI_multiplier_pivoted)
    lives_df["ci_multiplier_upper_age"] = look_up(lives_df["ci_multiplier_lookup_upper"], "SCA", "Value", tblCI_multiplier_pivoted)
    lives_df["ci_rate_lower_age"] = lives_df["ci_uk_base_rate_lower_age"] * lives_df["ci_multiplier_lower_age"]
    lives_df["ci_rate_upper_age"] = lives_df["ci_uk_base_rate_upper_age"] * lives_df["ci_multiplier_upper_age"]
    lives_df = calculate_ci_exp_param(lives_df)
    lives_df["ci_rate"] = lives_df["ci_c_param"] * np.exp(lives_df["ci_b_param"] * lives_df["age_attained"])

    if ci.benefit == "Fixed":
        lives_df["ci_sum_insured"] = lives_df["no_lives"] * ci.benefit_amount_fixed
        lives_df["ci_sum_insured_post_cap"] = np.minimum(lives_df["ci_sum_insured"], lives_df["no_lives"] * lives_df["salary"] * ci.cap_pct) if ci.cap_pct else lives_df["ci_sum_insured"]
    elif ci.benefit == "Perc_salary":
        lives_df["ci_sum_insured"] = lives_df["no_lives"] * lives_df["sum_insured"] * ci.benefit_amount_pct
        lives_df["ci_sum_insured_post_cap"] = np.minimum(lives_df["ci_sum_insured"], lives_df["no_lives"] * ci.cap_amount) if ci.cap_amount else lives_df["ci_sum_insured"]

    return lives_df


def rate_agg_limits(hxd):
    layer, cvg = one_layer(hxd)
    temp = layer.temp
    expo = hxd.cds.exposure.granular
    db = cvg.death

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)

    db.el_cost_no_sim = sum(lives_df[lives_df["db_expected_loss_cost_pre_uw_adj"] > 0]["db_expected_loss_cost_pre_uw_adj"])
    db.agg_impact_on_el = 0

    if not temp.is_agg_priced or not db.el_cost_post_sim.selected or ((layer.aggregate_deductible is None) and (layer.aggregate_limit is None)):
        return

    db.agg_impact_on_el = ratio(db.el_cost_post_sim.selected, db.el_cost_post_sim_pre_agg) - 1

    #YZ add some condition to remove the simulation noise to adjust the expected cost from aggregate
    if abs(db.agg_impact_on_el ) <= 0.005:
        db.agg_impact_on_el  = 0

### --- OVERALL RATING --- ###
def rate_lives(hxd):

    # Only run when Group selected
    if hxd.cds.is_individual:
        return

    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    ccy = hxd.cds.currencies.source_currency
    cover = hxd.cds.cover_selection

    db = cvg.death
    adb = cvg.additional_death
    ti = cvg.terminal_illness
    ci = cvg.critical_illness
    re = cvg.repat_exp

    # Check death benefit details have been filled in
    if not cover.are_db_fields_full:
        return

    # Get DataFrame with exposures
    lives = expo.lives
    lives_df = pd_df_from_hx_list(lives)
    input_cols = [
        "no_lives", 
        "sex", 
        "age_attained", 
        "salary", 
        "salary_multiple",
        "sum_insured",
        "nationality", 
        "location", 
        "region",
        "occupation_code"
        ]
    lives_df = lives_df[input_cols]

    # Validate entries in the table
    lives_df, all_fields_valid, check_labels = fill_check_columns(lives_df)

    okay_msg = "✅ All entries are valid."
    error_msg = "⚠️ Click on 'Validate data' and check the table."
    expo.data_check = okay_msg if all_fields_valid else error_msg
     
    if expo.show_check_cols:
        expo.data_check = "🔴 Fix the invalid entries."
        check_cols = [(col + "_check") for col in input_cols]
        
        # Push validation to hxd
        write_pd_to_hxd(lives_df, lives, check_cols)
        expo.check_col_labels = check_labels
    
    # Check entries are valid
    if not all_fields_valid:
        hx.errors.validation("Some entries in the table of lives in Premium are invalid and must be fixed.")
        #Confirm regions have been entered via drop down menus for the UK
        if check_labels["region_check_label"] == "⚠️ Warning":
            expo.region_warning = "⚠️ UK regions are not valid"
        else:
            expo.region_warning = "✅ Uk regions are valid"
        return
    
    # Confirm all fields are valid
    expo.data_check = okay_msg

    #Confirm regions have been entered via drop down menus for the UK
    if check_labels["region_check_label"] == "⚠️ Warning":
            expo.region_warning = "⚠️ UK regions are not valid"
    else:
        expo.region_warning = "✅ UK regions are valid"
 
    # Policy details
    brokerage = layer.brokerage or 0
    db_uw_adj = db.uw_adj
    adb_uw_adj = adb.uw_adj
    re_uw_adj = re.uw_adj
    ci_uw_adj = ci.uw_adj
    ti_uw_adj = ti.uw_adj

    ### --- DEATH BENEFIT --- ###
    lives_df = rate_db_or_ti(hxd, lives_df, "db")
    lives_df["db_expected_loss_cost_pre_uw_adj"] = lives_df["sum_insured"] * lives_df["db_qx"] / 1000
    lives_df["db_technical_premium_pre_uw_adj"] = ratio(ratio(lives_df["db_expected_loss_cost_pre_uw_adj"], benchmark_lr), 1-brokerage) 
    lives_df["db_expected_loss_cost"] = lives_df["db_expected_loss_cost_pre_uw_adj"] * db_uw_adj
    lives_df["db_technical_premium"] = ratio(ratio(lives_df["db_expected_loss_cost"], benchmark_lr), 1-brokerage)

    # Define output columns to push to the hxd
    risk_rate_cols = ["db_qx"]
    output_cols = [
        "db_qx", 
        "db_expected_loss_cost_pre_uw_adj", 
        "db_technical_premium_pre_uw_adj", 
        "db_expected_loss_cost", 
        "db_technical_premium"
    ]

    ### --- ADDITIONAL DEATH BENEFITS --- ###
    if adb.is_covered:
        expo.show_adb = True
        lives_df["adb_qx"] = lives_df["B_nat_blend_q(Non-natural_only)"]
        lives_df["adb_expected_loss_cost_pre_uw_adj"] = lives_df["adb_qx"] * lives_df["sum_insured"] / 1000
        lives_df["adb_technical_premium_pre_uw_adj"] = ratio(ratio(lives_df["adb_expected_loss_cost_pre_uw_adj"], benchmark_lr), 1-brokerage) 
        lives_df["adb_expected_loss_cost"] = lives_df["adb_expected_loss_cost_pre_uw_adj"] * adb_uw_adj
        lives_df["adb_technical_premium"] = ratio(ratio(lives_df["adb_expected_loss_cost"], benchmark_lr), 1-brokerage)
        risk_rate_cols.append("adb_qx")

        adb_output_cols = [
            "adb_qx", 
            "adb_expected_loss_cost_pre_uw_adj", 
            "adb_technical_premium_pre_uw_adj", 
            "adb_expected_loss_cost", 
            "adb_technical_premium"
        ]
        output_cols.extend(adb_output_cols)

    ### --- REPATRIATION EXPENSES --- ###
    if re.is_covered:
        expo.show_re = True
        limit_in_usd = usd(value=re.limit, ccy=ccy)
        lives_df["re_rate"] = look_up_closest(limit_in_usd, "Limit (USD)", "Rate per 1000 Limit", tblRepat, lookup_type="single")
        lives_df["re_expected_loss_cost_pre_uw_adj"] = lives_df["re_rate"] * lives_df["no_lives"] * re.limit / 1000
        lives_df["re_technical_premium_pre_uw_adj"] = ratio(ratio(lives_df["re_expected_loss_cost_pre_uw_adj"], benchmark_lr), 1-brokerage) 
        lives_df["re_expected_loss_cost"] = lives_df["re_expected_loss_cost_pre_uw_adj"] * re_uw_adj
        lives_df["re_technical_premium"] = ratio(ratio(lives_df["re_expected_loss_cost"], benchmark_lr), 1-brokerage)
        risk_rate_cols.append("re_rate")

        re_output_cols = [
            "re_rate",
            "re_expected_loss_cost_pre_uw_adj",
            "re_technical_premium_pre_uw_adj",
            "re_expected_loss_cost",
            "re_technical_premium"
        ]
        output_cols.extend(re_output_cols)

    ### --- CRITICAL ILLNESS --- ###
    if cover.are_ci_fields_full:
        expo.show_ci = True
        lives_df = rate_ci(hxd, lives_df)
        lives_df["ci_expected_loss_cost_pre_uw_adj"] = lives_df["ci_cover"] * lives_df["ci_rate"] * lives_df["ci_sum_insured_post_cap"] / 1000
        lives_df["ci_technical_premium_pre_uw_adj"] = ratio(ratio(lives_df["ci_expected_loss_cost_pre_uw_adj"], benchmark_lr), 1-brokerage) 
        lives_df["ci_expected_loss_cost"] = lives_df["ci_expected_loss_cost_pre_uw_adj"] * ci_uw_adj
        lives_df["ci_technical_premium"] = ratio(ratio(lives_df["ci_expected_loss_cost"], benchmark_lr), 1-brokerage)
        risk_rate_cols.append("ci_rate")

        ci_output_cols = [
            "ci_cover",
            "ci_rate",
            "ci_sum_insured",
            "ci_sum_insured_post_cap",
            "ci_expected_loss_cost_pre_uw_adj",
            "ci_technical_premium_pre_uw_adj",
            "ci_expected_loss_cost",
            "ci_technical_premium"
        ]
        output_cols.extend(ci_output_cols)

    ### --- TERMINAL ILLNESS --- ###
    if ti.is_covered:
        expo.show_ti = True
        lives_df = lives_df[input_cols + output_cols]
        lives_df = rate_db_or_ti(hxd, lives_df, "ti")
        lives_df["ti_proportion"] = np.where(
            lives_df["sex"] == "M", 
            look_up_closest(lives_df["age_attained"], "Age to match", "M", TI_proportions),
            look_up_closest(lives_df["age_attained"], "Age to match", "F", TI_proportions) # Assuming values in Sex can only be M or F
        )
        lives_df["ti_rate"] = lives_df["ti_cover"] * lives_df["ti_qx"] * lives_df["ti_proportion"]
        lives_df["ti_expected_loss_cost_pre_uw_adj"] = lives_df["sum_insured"] * lives_df["ti_rate"] / 1000
        lives_df["ti_technical_premium_pre_uw_adj"] = ratio(ratio(lives_df["ti_expected_loss_cost_pre_uw_adj"], benchmark_lr), 1-brokerage) 
        lives_df["ti_expected_loss_cost"] = lives_df["ti_expected_loss_cost_pre_uw_adj"] * ti_uw_adj
        lives_df["ti_technical_premium"] = ratio(ratio(lives_df["ti_expected_loss_cost"], benchmark_lr), 1-brokerage)
        risk_rate_cols.append("ti_rate")

        ti_output_cols = [
            "ti_cover",
            "ti_proportion",
            "ti_rate",
            "ti_expected_loss_cost_pre_uw_adj",
            "ti_technical_premium_pre_uw_adj",
            "ti_expected_loss_cost",
            "ti_technical_premium"
        ]
        output_cols.extend(ti_output_cols)

    # Additional calcs
    lives_df["no_claim_prob"] = (1 - lives_df[risk_rate_cols].sum(axis=1) / 1000) ** lives_df["no_lives"]
    output_cols.append("no_claim_prob")

    # Push to hxd
    write_pd_to_hxd(lives_df, lives, output_cols)

    return lives_df