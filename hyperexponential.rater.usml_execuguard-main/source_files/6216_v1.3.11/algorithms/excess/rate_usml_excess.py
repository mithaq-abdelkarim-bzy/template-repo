import hx
import copy
from types import SimpleNamespace
from algorithms import rate_constants as constants
# from algorithms.rate_utilities import input_validation, interpolation_factor, look_up, look_up_with_bounds
from algorithms import rate_utilities as utils
from libraries.admitted_excess_premium.algorithms.rate_admitted_excess import (excess_attach_factor_calculations, base_limit_factor_calculation, load_and_prepare_data, calc_additional_rating_factor, setup_steps)
from algorithms.excess.rate_usml_excess_helpers import (excess_attachement_factor_calculation, single_limit_factor_calculation, pro_rata_factor_calculation, one_plus)

def excess_rc_calcs(hxd):
    admitted_excess = hxd.cds.admitted_excess
    excess_rc = hxd.cds.excess_rate_change

    # assign hxd nodes 
    excess_rc.new_prem.rate_change = admitted_excess.rounded_premium.value.selected
    excess_rc.deductible.renewal = admitted_excess.excess_attachment_point.value
    excess_rc.limit.renewal = admitted_excess.excess_limit.value

    #Calculated renewal premium for Limit and Deductible calculation
    excess_calculated_prem_renewal = admitted_excess.rounded_premium.value.calculated

    # set ded_adjusted_excess to be in the format of hxd and set expiring values to ded for RC calcs
    ded_adjusted_excess = SimpleNamespace()
    ded_adjusted_excess.excess_limit = SimpleNamespace(value=admitted_excess.excess_limit.value)
    ded_adjusted_excess.excess_attachment_point = SimpleNamespace(value=excess_rc.deductible.expiry)
    ded_adjusted_excess.primary_retention = SimpleNamespace(value=admitted_excess.primary_retention.value)
    ded_adjusted_excess.large_loss_potential = SimpleNamespace(value=admitted_excess.large_loss_potential.value)
    
    # ded prem assuming the old ded is used
    ded_prem_rc = admitted_premium_calculations_altered(hxd, ded_adjusted_excess, admitted_excess)   

    # set limit_adjusted_excess to be in the format of hxd and set expiring values to limit for RC calcs
    limit_adjusted_excess = SimpleNamespace()
    
    limit_adjusted_excess.excess_limit = SimpleNamespace(value=excess_rc.limit.expiry)
    limit_adjusted_excess.excess_attachment_point = SimpleNamespace(value=admitted_excess.excess_attachment_point.value)
    limit_adjusted_excess.primary_retention = SimpleNamespace(value=admitted_excess.primary_retention.value)
    limit_adjusted_excess.large_loss_potential = SimpleNamespace(value=admitted_excess.large_loss_potential.value)
    

    # limit prem assuming the old limit is used
    limit_prem_rc = admitted_premium_calculations_altered(hxd, limit_adjusted_excess, admitted_excess)
    
    # Calculate RC for Limit and Ded 
    if excess_rc.deductible.expiry is None:
        excess_rc.deductible.rate_change = 1
    else:
        #excess_rc.deductible.rate_change = excess_rc.new_prem.rate_change / ded_prem_rc if ded_prem_rc else 1
        excess_rc.deductible.rate_change = excess_calculated_prem_renewal / ded_prem_rc if ded_prem_rc else 1

    if excess_rc.limit.expiry is None:
        excess_rc.limit.rate_change = 1
    else:
        #excess_rc.limit.rate_change = excess_rc.new_prem.rate_change / limit_prem_rc if limit_prem_rc else 1
        excess_rc.limit.rate_change = excess_calculated_prem_renewal / limit_prem_rc if limit_prem_rc else 1

    # Exposure RC calcs 
    excess_rc.exposure.fte.rate_change = (excess_rc.exposure.fte.renewal / excess_rc.exposure.fte.expiry) ** .7 if (excess_rc.exposure.fte.renewal and excess_rc.exposure.fte.expiry) else 1
    excess_rc.exposure.plan_assets.rate_change = (excess_rc.exposure.plan_assets.renewal / excess_rc.exposure.plan_assets.expiry) ** .2 if (excess_rc.exposure.plan_assets.renewal and excess_rc.exposure.plan_assets.expiry) else 1
    excess_rc.exposure.plan_participants.rate_change = (excess_rc.exposure.plan_participants.renewal / excess_rc.exposure.plan_participants.expiry) ** .5 if (excess_rc.exposure.plan_participants.renewal and excess_rc.exposure.plan_participants.expiry) else 1
    excess_rc.exposure.total_assets.rate_change = (excess_rc.exposure.total_assets.renewal / excess_rc.exposure.total_assets.expiry) ** .2 if (excess_rc.exposure.total_assets.renewal and excess_rc.exposure.total_assets.expiry) else 1


    fte_weights = excess_rc.exposure.fte.weights if excess_rc.exposure.fte.weights else 0
    plan_assets_weights = excess_rc.exposure.plan_assets.weights if excess_rc.exposure.plan_assets.weights else 0
    plan_participants_weights = excess_rc.exposure.plan_participants.weights if excess_rc.exposure.plan_participants.weights else 0
    total_assets_weights = excess_rc.exposure.total_assets.weights if excess_rc.exposure.total_assets.weights else 0
    total_weights = sum([fte_weights, plan_assets_weights, plan_participants_weights,total_assets_weights])

    excess_rc.exposure.total_rate_change.rate_change =(excess_rc.exposure.fte.rate_change * fte_weights + excess_rc.exposure.plan_assets.rate_change * plan_assets_weights + excess_rc.exposure.plan_participants.rate_change * plan_participants_weights + excess_rc.exposure.total_assets.rate_change * total_assets_weights)/total_weights

    # Brokerage RC 
    excess_rc.brokerage.renewal = hxd.cds.layers[0].brokerage if hxd.cds.layers[0].brokerage else 0 
    #excess_rc.brokerage.rate_change = (1 - excess_rc.brokerage.renewal) / (1 - excess_rc.brokerage.expiry) if (excess_rc.brokerage.expiry and excess_rc.brokerage.expiry != 1) else 1
    excess_rc.brokerage.rate_change = (1 - excess_rc.brokerage.expiry) / (1 - excess_rc.brokerage.renewal) if (excess_rc.brokerage.expiry is not None and excess_rc.brokerage.renewal != 1) else 1


    # calcuate expected new prem and RC 
    excess_rc.expected_new_prem.rate_change = excess_rc.annualized_expiring_prem.rate_change * excess_rc.exposure.total_rate_change.rate_change * excess_rc.risk_char.rate_change * excess_rc.deductible.rate_change * \
        excess_rc.limit.rate_change * excess_rc.terms_and_conditions.rate_change * excess_rc.brokerage.rate_change if (excess_rc.annualized_expiring_prem.rate_change  and excess_rc.exposure.total_rate_change.rate_change) else None

    excess_rc.final_rc.rate_change = excess_rc.new_prem.rate_change / excess_rc.expected_new_prem.rate_change if (excess_rc.new_prem.rate_change and excess_rc.expected_new_prem.rate_change) else None

    # Validation to ensure the exposure weights = 100%
    if sum([fte_weights, plan_assets_weights, plan_participants_weights,total_assets_weights]) != 1:
        hx.errors.validation("Exposure Rate Change weights must add to 100%.")

    # ############### Calculate Benchmark Premium #####################################

    # # Get subjective factors that were included in Model Premium to be removed
    # primary_premium = admitted_excess.primary_premium.value or 1
    # corrective_factor = (admitted_excess.primary_rate_adequacy_correction.value + 1) or 1
    # industry_sector_factor = (admitted_excess.industry_sector_factor.value + 1) or 1
    # company_factor = (admitted_excess.company_factor.value + 1) or 1
    # litigation_factor = (admitted_excess.litigation_factor.value +1) or 1
    # product_three_sev_factors = industry_sector_factor * company_factor * litigation_factor
    # schedule_rating_factor = (admitted_excess.fl_schedule_rating_factor.value + 1) or 1
    # surplus_deviation = (admitted_excess.surplus_deviation.value + 1) if (
    #     admitted_excess.surplus_deviation.value is not None and
    #     hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus") else 1

    # # Get total subjective adjustments
    # unity_premium_total_adj =( 
    #     corrective_factor_adj
    #     * industry_sector_factor_adj
    #     * company_factor_adj
    #     * litigation_factor_adj
    #     * schedule_rating_factor
    #     * surplus_deviation

    #     )
  
    # unity_premium = (admitted_excess.model_premium.value/unity_premium_total_adj) if unity_premium_total_adj else 0
    # expected_loss = unity_premium * .5  # PFLR
    # benchmark_premium = expected_loss / .7
    # hxd.cds.admitted_excess_local.benchmark_term_premium.value = benchmark_premium

    # pro_rata_factor = pro_rata_factor_calculation(hxd)

    # # pro_rata_benchark_premium = benchmark_premium
    # hxd.cds.admitted_excess_local.benchmark_term_premium.value = benchmark_premium
    # hxd.cds.admitted_excess_local.benchmark_term_premium_pre_uw_adj.value = benchmark_premium
    
    # hxd.cds.admitted_excess_local.bpi.value = (hxd.cds.admitted_excess.rounded_premium.value.selected / benchmark_premium) if (hxd.cds.admitted_excess.rounded_premium.value.selected) and (benchmark_premium > 0) else 0


def admitted_premium_calculations_altered(hxd, attach_input, limit_input):
    """
    Performs admitted premium calculations.

    Args:
        hxd: The hxd object containing relevant data.
    """
    base_path = hxd.cds.admitted_excess 
    dataframes = load_and_prepare_data(hxd)

    # Defining parameter tables
    df_type = dataframes.excess_state_type 
    df_ilf = dataframes.excess_2_ilf
    df_singlelimit = dataframes.excess_4_single_limit
    df_rounding = dataframes.excess_5_rounding

    #set the shownby condition for the Surplus Deviation factor
    hxd.cds.is_excess_surplus = True if hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus" else False
    hxd.cds.not_excess_surplus = not(hxd.cds.is_excess_surplus)
    
    # Setting values from hxd    
    primary_premium = base_path.primary_premium.value or 1
    corrective_factor = (base_path.primary_rate_adequacy_correction.value + 1) or 1
    industry_sector_factor = (base_path.industry_sector_factor.value + 1) or 1
    company_factor = (base_path.company_factor.value  + 1) or 1
    litigation_factor = (base_path.litigation_factor.value  + 1) or 1
    product_three_sev_factors = industry_sector_factor * company_factor * litigation_factor
    schedule_rating_factor = (base_path.fl_schedule_rating_factor.value  + 1) or 1
    surplus_deviation = (base_path.surplus_deviation.value + 1) if (
        base_path.surplus_deviation.value is not None and
        hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus") else 1

    state = hxd.cds.standard_fields.insured_state_or_province
    # Pulling types    
    if df_type["State"].isin([state]).any():
        type_row = df_type[df_type["State"] == state].iloc[0]
    else:
        hx.errors.validation("The State Selected is not recognised")
        return None

    # Calling limit functions functions
    excess_attach_factor = excess_attach_factor_calculations(attach_input, df_ilf, type_row["ILF Type"])
    basic_limit_factor = base_limit_factor_calculation(base_path, df_ilf, type_row["ILF Type"])

    exc_no_policies = base_path.no_of_policies_sharing_single_limit.value
    single_limit_factor = utils.look_up(exc_no_policies,"Number of", "Single Limit Factor", df_singlelimit, 1) if exc_no_policies is not None else 0
    additional_rating_factor = calc_additional_rating_factor(base_path)
    # Calculates model premium
    model_premium =(
          primary_premium  
        * corrective_factor  
        * (excess_attach_factor/basic_limit_factor)  
        * product_three_sev_factors  
        * schedule_rating_factor  
        * single_limit_factor 
        * additional_rating_factor
        * surplus_deviation
        )
  
    return model_premium

def excess_bp_tp_calculations(hxd):
    admitted_excess = hxd.cds.admitted_excess

    # Get subjective factors that were included in Model Premium to be removed
    corrective_factor_adj = one_plus(admitted_excess.primary_rate_adequacy_correction.value) or 1
    industry_sector_factor_adj = one_plus(admitted_excess.industry_sector_factor.value) or 1
    company_factor_adj = one_plus(admitted_excess.company_factor.value) or 1
    litigation_factor_adj = one_plus(admitted_excess.litigation_factor.value) or 1
    schedule_rating_factor = one_plus(admitted_excess.fl_schedule_rating_factor.value) or 1
    surplus_deviation = (admitted_excess.surplus_deviation.value) if (
        admitted_excess.surplus_deviation.value is not None and
        hxd.cds.standard_fields.is_admitted_or_surplus == "Surplus") else 1

    # Get total subjective adjustments
    unity_premium_total_adj =( 
        corrective_factor_adj
        * industry_sector_factor_adj
        * company_factor_adj
        * litigation_factor_adj
        * schedule_rating_factor
        * surplus_deviation

        )
  
    unity_premium = (admitted_excess.model_premium.value/unity_premium_total_adj) if (unity_premium_total_adj and admitted_excess.model_premium.value) else 0
    expected_loss = unity_premium * .5  # PFLR
    benchmark_premium_unadj= expected_loss / .7
    assumed_primary_brokerage= constants.excess_assumed_primary_brokerage
    brokerage = hxd.cds.layers[0].brokerage or 0

    benchmark_premium = benchmark_premium_unadj * (1-assumed_primary_brokerage)/(1-brokerage)


    # hxd.cds.admitted_excess_local.benchmark_term_premium.value = benchmark_premium

    pro_rata_factor = pro_rata_factor_calculation(hxd)

    # pro_rata_benchark_premium = benchmark_premium
    hxd.cds.admitted_excess_local.benchmark_term_premium.value = benchmark_premium * pro_rata_factor
    hxd.cds.admitted_excess_local.benchmark_term_premium_pre_uw_adj.value = benchmark_premium * pro_rata_factor
    
    hxd.cds.admitted_excess_local.bpi.value = (hxd.cds.admitted_excess.rounded_premium.value.selected / benchmark_premium) if (hxd.cds.admitted_excess.rounded_premium.value.selected) and (benchmark_premium > 0) else 0
