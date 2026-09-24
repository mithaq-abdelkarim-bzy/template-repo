import hx
import numpy as np
from algorithms import rate_constants as constants
from algorithms.rate_utilities import look_up, look_up_with_bounds, agg_lim_calc, pd_df_from_hx_structure, input_validation, value_less_than_min_validation

#a validation function that catches some essential inputs to this rater
def validation_functions_pcl(hxd):
    validation_failed = False  # Flag to track validation status

    # fid plan validation inputs    
    if hxd.cds.coverage_elections.pcl:
        total_employees = hxd.cds.us_states.Total.fte + hxd.cds.us_states.Total.pte
        if  total_employees == 0:
                    hx.errors.validation(
                        f"There must be at least one employee in one state in either full time or part time"
                    )
                    validation_failed = True
        if hxd.cds.exposure.granular.pcl.base_rate.asset_size is None:
            hx.errors.validation("The Asset Size has no value in PCL Inputs")
            validation_failed = True
        #this means the asset size can't be less than 1 or bigger than 999,999,999
        if not input_validation(
            constants.assets_base_rate_pcl_min,
            constants.assets_base_rate_pcl_max,
            hxd.cds.exposure.granular.pcl.base_rate.asset_size,
            "PCL Asset Size",
            ):
            validation_failed = True

        if hxd.cds.exposure.granular.pcl.base_rate.revenue is None:
            hx.errors.validation("The Revenue has no value in PCL Inputs")
            validation_failed = True
        #this means the asset size can't be less than 1 or bigger than 999,999,999
        if not input_validation(
            constants.revenue_base_rate_pcl_min,
            constants.revenue_base_rate_pcl_max,
            hxd.cds.exposure.granular.pcl.base_rate.revenue,
            "PCL Revenue",
            ):
            validation_failed = True      

    return validation_failed  

def validate_option_pcl(option, results,state_info):
    validation_passed = True    

    if not input_validation(
        state_info.get("minimum_limit"),
        constants.aggregate_limit_pcl_max,
        option.aggregate_limit,
        "PCL Aggregate Limit Size",
    ):
        validation_passed = False    

    return validation_passed

def calc_admitted_retention_factor(option, state_info, results,idx):
      # change the table depending on the state
    if state_info['state_code'] == "FL":
        table = hx.params.table_pcl_retention_factors_fl        
    else:
        table = hx.params.table_pcl_retention_factors_cw
        

    input_value = option.retention
    input_to_use = input_value if input_value else constants.retention_pcl_default

    # set the retention factor based on the asset size
    asset_size_category_pcl = results.get("asset_size_category_pcl") + 1

    row_to_use = table[
        (table["Retention - Low"] <= input_to_use)
        & (table["Retention - High"] > input_to_use)
    ].iloc[0]

    retention_low = row_to_use["Retention - Low"]
    if row_to_use["Retention - High"] == 999999999 :
        retention_high = retention_low
    else:
         retention_high = row_to_use["Retention - High"]

    factor_low = table.loc[
        table["Retention - Low"] == retention_low,
        table.columns[asset_size_category_pcl],
    ].iloc[0]
    factor_high = table.loc[
        table["Retention - Low"] == retention_high,
        table.columns[asset_size_category_pcl],
    ].iloc[0]
    admitted_retention_pcl = (
        factor_low
        if factor_low == factor_high
        else factor_low
        + ((input_to_use - retention_low) / (retention_high - retention_low))
        * (factor_high - factor_low)
    )

    # set the min and max for the retention based on the size of the asset
    if results["asset_size_category_pcl"] == 1:
        retention_pcl_max = constants.retention_pcl_max_choice_1
        retention_pcl_min = constants.retention_pcl_min_choice_1
    elif results["asset_size_category_pcl"] == 2:
        retention_pcl_max = constants.retention_pcl_max_choice_2
        retention_pcl_min = constants.retention_pcl_min_choice_2
    else:
        retention_pcl_max = constants.retention_pcl_max_choice_3
        retention_pcl_min = constants.retention_pcl_min_choice_3

    # Check the retention is between min and max retention
    if option.retention is not None:
        if option.retention > retention_pcl_max or option.retention < retention_pcl_min:
            hx.errors.validation(f"PCL: The retention for option {idx + 1} should be between {retention_pcl_min}-{retention_pcl_max}")

    results.setdefault("admitted_retention_pcl", []).append(admitted_retention_pcl)
    results.setdefault("retention_pcl_max", []).append(retention_pcl_max)
    results.setdefault("retention_pcl_min", []).append(retention_pcl_min)
    results.setdefault("retention_pcl_value", []).append(input_to_use)
    #set the minimum retention output field.
    option.miniumum_retention = results.get("retention_pcl_min")[0]



def calc_admitted_limit_factor(option, results):
    retention_low = results.get("asset_size_retention_low")
    retention_high = results.get("asset_size_retention_high")

    input_to_use = option.aggregate_limit or constants.aggregate_limit_pcl_default
    table = hx.params.table_pcl_limit_factors_cw

    df_res = look_up_with_bounds(input_to_use, "Limit - low", "Limit - High", ["Limit - low", "Limit - High"], table)
    limit_low = df_res["Limit - low"]
    limit_high = df_res["Limit - High"]

    factor_low = look_up(limit_low, "Limit - low", "Factor", table)
    factor_high = look_up(limit_high, "Limit - low", "Factor", table)

    admitted_limit_factor_pcl =(factor_low if factor_low == factor_high
        else factor_low + (factor_high - factor_low)*((input_to_use - limit_low) / (limit_high- limit_low))
    )

    results.setdefault("admitted_limit_factor_pcl", []).append(admitted_limit_factor_pcl)



def calc_combined_retention_and_limit_factor(option, state_info, results, option_index):
    retention_factor = results.get("admitted_retention_pcl")[option_index]
    limit_factor = results.get("admitted_limit_factor_pcl")[option_index]

    combined_retention_and_limit_factor = retention_factor + limit_factor if state_info["state_code"] == "FL" else retention_factor * limit_factor

    option.limit_retention = combined_retention_and_limit_factor
    results.setdefault("combined_retention_and_limit_factor", []).append(combined_retention_and_limit_factor)


def calc_admitted_unrounded_premium(hxd, option, state_info, results, option_index):
    basic_limit_premium_eligibility = state_info.get("basic_limit_premium_eligibility")
    base_premium = results.get("assets_base_rate_pcl")
    combined_retention_and_limit_factor = results.get("combined_retention_and_limit_factor")[option_index]
    admitted_total_risk_characteristics_factor_pcl = results.get("admitted_total_risk_characteristics_factor_pcl")
    admitted_cob_factor = results.get("admitted_cob_factor")
    admitted_punitive_damages_factor = results.get("admitted_punitive_damages_factor")
    admitted_schedule_rating_factor = results.get("admitted_schedule_rating_factor")
    ne_deviation_factor = results.get("ne_deviation_factor_pcl")
    surplus_deviation_factor = results.get("surplus_deviation_factor_pcl")

    premium_before_schedule_rating = (
        base_premium
        * combined_retention_and_limit_factor
        * admitted_total_risk_characteristics_factor_pcl
        * admitted_cob_factor
        * admitted_punitive_damages_factor
    )

    if state_info["state_code"] == "NE":
        result = ne_deviation_factor
    elif state_info["state_code"] == "LA":
        if premium_before_schedule_rating * admitted_schedule_rating_factor > basic_limit_premium_eligibility:
            result = admitted_schedule_rating_factor
        else:
            result = 1
    else:
        if premium_before_schedule_rating > basic_limit_premium_eligibility:
            result = admitted_schedule_rating_factor
        else:
            result = 1

    state_code_multplier = result * surplus_deviation_factor
    admitted_unrounded_premium_pcl = premium_before_schedule_rating * state_code_multplier

    option.admitted_premium = admitted_unrounded_premium_pcl
    results.setdefault("admitted_unrounded_premium_pcl", []).append(admitted_unrounded_premium_pcl)

    # set values back to the cds for running prem totals
    prem_sum = hxd.cds.layers[0].coverages.pcl.running_prem_sum

    if hxd.cds.layers[0].coverages.pcl.quote_grid.qg_options[option_index].option_selected == True:
        prem_sum.base_rate.prem = base_premium
        prem_sum.combined_retention_and_limit_adj.modifier = combined_retention_and_limit_factor
        prem_sum.combined_retention_and_limit_adj.prem = combined_retention_and_limit_factor * prem_sum.base_rate.prem
        prem_sum.risk_char_adj.modifier = admitted_total_risk_characteristics_factor_pcl
        prem_sum.risk_char_adj.prem = admitted_total_risk_characteristics_factor_pcl * prem_sum.combined_retention_and_limit_adj.prem
        prem_sum.cob_adj.modifier = admitted_cob_factor
        prem_sum.cob_adj.prem = admitted_cob_factor * prem_sum.risk_char_adj.prem
        prem_sum.punitive_damages_adj.modifier = admitted_punitive_damages_factor
        prem_sum.punitive_damages_adj.prem = admitted_punitive_damages_factor * prem_sum.cob_adj.prem
        prem_sum.state_adj.modifier = result
        prem_sum.state_adj.prem = result * prem_sum.punitive_damages_adj.prem
        prem_sum.surp_dev_adj.modifier = surplus_deviation_factor
        prem_sum.surp_dev_adj.prem = surplus_deviation_factor * prem_sum.state_adj.prem


def fetch_eec_info(option, results):
    input_to_use = option.aggregate_limit
    table = hx.params.table_pcl_ilfs_agg

    df_res = look_up_with_bounds(input_to_use, "EELimitFrom", "EELimitTo", ["EELimitFrom", "EELimitTo"], table)
    limit_from = df_res["EELimitFrom"]
    limit_to = df_res["EELimitTo"]

    results.setdefault("limit_from", []).append(limit_from)
    results.setdefault("limit_to", []).append(limit_to)


def calc_ilf_ib(option, hxd, results, option_index):
    if hxd.cds.layers[0].is_primary_excess != "Primary":
        results.setdefault("ib_ilf", []).append(1)
        return

    ilf_table = hx.params.table_pcl_ilfs_agg
    ilf_table["lookup"] = ilf_table["lookup"].astype(str)

    agg_eec_ratio = option.aggregate_limit / option.aggregate_limit

    f1_lookup_value = str(int(results.get("limit_from")[option_index])) + str(int(round(agg_eec_ratio, 0)))
    f2_lookup_value = str(int(results.get("limit_from")[option_index])) + str(int(round(agg_eec_ratio + 1, 0)))
    f3_lookup_value = str(int(results.get("limit_to")[option_index])) + str(int(round(agg_eec_ratio, 0)))
    f4_lookup_value = str(int(results.get("limit_to")[option_index])) + str(int(round(agg_eec_ratio + 1, 0)))

    f1 = look_up(f1_lookup_value, "lookup", "Factor", ilf_table)
    f2 = look_up(f2_lookup_value, "lookup", "Factor", ilf_table) 
    f3 = look_up(f3_lookup_value, "lookup", "Factor", ilf_table) 
    f4 = look_up(f4_lookup_value, "lookup", "Factor", ilf_table) 

    # NOTE: as with fid, alpha and beta will always produce the same result as it stands, but this matched excel
    agg_lim_calc(option, results, "alpha", hx.params.table_pcl_ilfs_agg, "EELimitFrom", "EELimitTo")
    agg_lim_calc(option, results, "beta", hx.params.table_pcl_ilfs_agg, "EELimitFrom", "EELimitTo")

    alpha = results["alpha"][option_index]
    beta = results["beta"][option_index]
    ib_ilf = (f1 + alpha*(f3 - f1) + beta*(f2 - f1) + beta*beta*(f4 + f1 - f2 - f3))
    
    results.setdefault("ib_ilf", []).append(ib_ilf)
    

def calc_retention_factor_ib(option, hxd, results, option_index):
    if hxd.cds.layers[0].is_primary_excess != "Primary":
        results.setdefault("ib_retention_factor", []).append(1)
        return

    ib_base_premium_input_basis = results.get("ib_base_premium_input_basis")

    if ib_base_premium_input_basis < 50000000:
        column_increase = 0
    elif ib_base_premium_input_basis > 150000000:
        column_increase = 4
    else:
        column_increase = 2

    # SA: if statement on a constant condition?
    table = hx.params.table_pcl_retention_assets if constants.ib_basis == "Assets" else hx.params.table_pcl_retention_revenue

    lower_column = 0
    upper_column = 1
    lower_rate_column = 5 + column_increase
    upper_rate_column = 6 + column_increase

    lower_rate_col = table.columns[lower_rate_column]
    upper_rate_col = table.columns[upper_rate_column]
    lower_value_col = table.columns[lower_column]
    upper_value_col = table.columns[upper_column]

    input_to_use = results.get("retention_pcl_value")[option_index] or constants.ib_guideline_retention_default  # SA: This default can't be hit because retention_pcl_value already has a default
    
    # SA: Guideline_retention was calculated but unused
    # guideline_retention = look_up_with_bounds(input_to_use, "Lower", "Upper", "Amount", hx.params.table_pcl_guide_retentions)

    df_res = look_up_with_bounds(input_to_use, "Lower", "Upper", [lower_rate_col, upper_rate_col, lower_value_col, upper_value_col], table)

    lower_rate = df_res[lower_rate_col]
    upper_rate = df_res[upper_rate_col]
    lower_value = df_res[lower_value_col]
    upper_value = df_res[upper_value_col]

    ib_retention_factor = upper_rate + ((lower_rate - upper_rate) / (upper_value - lower_value)) * (upper_value - input_to_use)

    results.setdefault("ib_retention_factor", []).append(ib_retention_factor)

    #also set the minimum retention output field.  This is always static and for user reference
    option.miniumum_retention = results.get("retention_pcl_min")[0]
    #option.miniumum_retention = constants.retention_pcl_default

def calc_limit_retention_factor_ib(option, hxd, results, option_index):
    if hxd.cds.layers[0].is_primary_excess != "Primary":
        results.setdefault("ib_clrf", []).append(1)
        return
    
    ilf_table = hx.params.table_pcl_combined_limit_retention_factor
    input_limit = option.aggregate_limit
    input_retention = option.retention
    input_limit_retention = input_limit + input_retention
    
    ilf_upper = np.interp(input_limit_retention,ilf_table['Limit'], ilf_table['Factor'])
    ilf_lower = np.interp(input_retention, ilf_table['Limit'], ilf_table['Factor'])

    ib_clrf = ilf_upper - ilf_lower

    results.setdefault("ib_clrf", []).append(ib_clrf)


def calc_model_premium_ib(option,hxd, results, option_index):
    ib_model_premium = (
        results.get("ib_base_premium_before_minimum")
        #* results.get("ib_ilf")[option_index]
        #* results.get("ib_retention_factor")[option_index]
        * results.get("ib_clrf")[option_index]
        * results.get("ib_objective_modifiers")
        * results.get("ib_subjective_modifiers")
    )

    london_brokerage = constants.london_brokerage
    us_brokerage = hxd.cds.layers[0].brokerage or 0

    adjusted_model_premium = ib_model_premium * (1 - london_brokerage) / (1 - us_brokerage)

    ib_subjective_modifiers = results.get("ib_subjective_modifiers")

    option.internal_benchmark = adjusted_model_premium
    option.internal_benchmark_pre_uw_adj = 0 if ib_subjective_modifiers == 0 else adjusted_model_premium/ ib_subjective_modifiers
    results.setdefault("ib_model_premium", []).append(adjusted_model_premium)


def calc_bpi_percent(option, results, option_index):
    admitted_unrounded_premium = results.get("admitted_unrounded_premium_pcl")[option_index]
    ib_model_premium = results.get("ib_model_premium")[option_index]

    bpi_percent = 0 if ib_model_premium == 0 else admitted_unrounded_premium / ib_model_premium

    option.bpi = bpi_percent
    results.setdefault("bpi_percent", []).append(bpi_percent)


def calc_guideline_minimium_premium(option, hxd, state_info):
    states_df = pd_df_from_hx_structure(hxd.cds.us_states).fillna(0).drop("Total")

    state_risk_df = hx.params.table_epl_state_risk_level
    state_risk_df.index = state_risk_df["State"].str.replace(" - ", "_").str.replace(" ", "_").str.replace("-", "_")

    states_df = states_df.join(state_risk_df[["Risk Group"]])

    employee_factors_df = hx.params.table_epl_empfact
    ef_transposed_df = employee_factors_df[employee_factors_df["Emp Fact"].isin(["FT", "PT"])].set_index("Emp Fact")[["Part-Time"]].T

    states_df = states_df.reset_index()
    states_df = states_df.join(ef_transposed_df, how="cross")
    states_df = states_df.set_index("index")

    states_df["fte"] = states_df["fte"]*states_df["FT"] + states_df["pte"]*states_df["PT"]

    state_groupings_df = hx.params.table_epl_state_groupings.set_index("Risk Profile")
    states_df = states_df.merge(state_groupings_df, left_on="Risk Group", right_index=True) 

    # Equivalency state
    insured_state = hxd.cds.state
    county = hxd.cds.county
    liberal_search = str(insured_state) + str(county)
    liberal_state = look_up(liberal_search, "Lookup", "Liberal", hx.params.table_epl_liberal_county, if_not_found="FALSE")

    states_df["is_insured_state"] = states_df.index == insured_state
    states_df["insured_state_is_liberal"] = liberal_state == "TRUE"

    table_epl_state_factor = hx.params.table_epl_state_factor[["State", "Liberal", "NonLiberal"]]
    table_epl_state_factor["State"] = table_epl_state_factor["State"].str.replace(" - ", "_").str.replace(" ", "_").str.replace("-", "_")
    table_epl_state_factor = table_epl_state_factor.set_index("State")
    
    states_df = states_df.join(table_epl_state_factor)

    use_liberal_weight = (states_df['is_insured_state']) & (states_df["insured_state_is_liberal"])
    states_df['equivalency_state'] = np.where(use_liberal_weight, states_df["Liberal"], states_df["NonLiberal"])
    
    totals = states_df.sum().to_dict()
    total_risk_factor = sum(states_df["fte"].fillna(0)*states_df["Risk Factor"].fillna(0)) / totals["fte"] if totals["fte"] else 0
    total_state = sum(states_df["fte"].fillna(0)*states_df["equivalency_state"].fillna(0)) / totals["fte"] if totals["fte"] else 0
    
    lower_eec = look_up_with_bounds(option.aggregate_limit, "EE Limit From", "EE Limit To", "EE Limit From", hx.params.table_epl_min_prem_limit_ee, if_not_found=500000)
    lower_agg = look_up_with_bounds(option.aggregate_limit, "Agg Limit From", "Agg Limit To", "Agg Limit From", hx.params.table_epl_min_prem_limit_agg, if_not_found=0)

    lookup_value = f"{lower_eec}&{lower_agg}"
    state_group = look_up_with_bounds(total_state, "LowerState", "UpperState", "RetGroup", hx.params.table_epl_state_groups)

    minimum_premium = look_up(lookup_value, "Lookup Value", state_group, hx.params.table_pcl_min_premium_limits)
    option.guideline_minimum_premium = minimum_premium



