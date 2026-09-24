# v0.5.0
import hx
import numpy as np
import pandas as pd
from typing import Dict, Tuple

from algorithms.rate_constants import no_of_simulations, benchmark_lr
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, pd_df_from_hx_list_columns_task
import ast 

import os

# Uncomment for debugging on comment before saving the model version
# output_dir = "/workspace/editing/test_cases/"
# os.makedirs(output_dir, exist_ok=True)


def advanced_features(hxd, progress):
    """
    Calculate advanced reinsurance features for each layer.
    Returns a dictionary of Pandas Series for each output feature.
    """
    ##############################
    ## Initialize variables
    ##############################
    cds = hxd.cds
    cds_layers = cds.layers
    er = hxd.cds.steer.experience_rating
    ms = hxd.model_state

    has_missing_pure_premiums = hxd.model_state.is_pure_premium_not_calculated
    steer_bc_pattern_not_updated = ms.is_steer_experience_rating and er.is_not_experience_selected_updated

    ##############################
    ## Data validation
    ##############################
    if has_missing_pure_premiums or steer_bc_pattern_not_updated:
        return  # Exit function

    if len(cds_layers) == 0:
        return  # Exit function

    async_input_nodes = [
        "epi_100",
        "excess",
        "limit",
        "upfront_premium_gross_100",
        "pricing_selection/final_selection/pure_premium",
        "brokerage",
        "ceding_commission",
        "brokerage_inc_swing",
        "advanced_features_input/aad",
        "ncb",
        "profit_commission_rate",
        "expense_allowance",
        "loss_corridor/insured_participation",
        "loss_corridor/max_rate",
        "loss_corridor/min_rate",
        "loss_cap_used",
        "cap_gross_pct",
        "no_reinstatement",
        'reinstatement_pct_1',
        'reinstatement_pct_2',
        'reinstatement_pct_3',
        'reinstatement_pct_4',
        'reinstatement_pct_5',
        'reinstatement_pct_6',
        'reinstatement_pct_7',
        'reinstatement_pct_8',
        'reinstatement_pct_9',
        'reinstatement_pct_10',
        "number_of_rips",
        "swing_rates/deposit_rate",
        "swing_rates/min_rate",
        "swing_rates/max_rate",
        "swing_rates/margin",
        "swing_rates/loading_factor",
        "expected_loss" # this is 100 before AD
    ]

    layers_df = pd_df_from_hx_list_columns_task(hxd.cds.layers, async_input_nodes)
    layers_df["is_unlimited_rips"] = layers_df["no_reinstatement"] == "Unlimited"
    layers_df["num_rips"] = np.where(layers_df['is_unlimited_rips'], 999, layers_df['number_of_rips'])
    layers_df["brokerage_ad"] = (
        layers_df["brokerage_inc_swing"].fillna(0) +
        layers_df["ceding_commission"].fillna(0)
    )

    ##############################
    ## Extract policy parameters
    ##############################
    num_layers = len(cds_layers)
    alpha = cds.pricing_selection.pareto_parameters.selected
    odf_parameter = cds.pricing_selection.odf_parameters.selected
    sliding_scale_ind = cds.risk_information.include_swing_rates
    pc_ind = cds.risk_information.include_profit_commission
    ncb_ind = cds.risk_information.include_ncb
    loss_corridor_ind = cds.risk_information.include_loss_corridor
    aad_ind = cds.risk_information.include_aad
    num_simulations = no_of_simulations

    ##############################
    ## Calculate advanced features
    ##############################
    outputs_df = calculate_advanced_features(
        layers_df=layers_df,
        alpha=alpha,
        odp=odf_parameter,
        target_lr=benchmark_lr,
        sliding_scale_flag=sliding_scale_ind,
        pc_flag=pc_ind,
        ncb_flag=ncb_ind,
        loss_corridor_flag=loss_corridor_ind,
        aad_flag=aad_ind,
        num_simulations=num_simulations,
    )

    async_output_nodes = [
        "expected_aad",
        "loss_corridor_loss_cost",
        "expected_reinstatement_factor",
        "expected_ncb_pct",
        "profit_commission",
        "swing_premium",
        "claim_frequency",
        "average_cost_per_claim",
    ]

    outputs_df[async_output_nodes] = outputs_df[async_output_nodes].fillna(0)

    ##############################
    ## Write in HXD
    ##############################
    write_pd_to_hxd(outputs_df, hxd.cds.layers, async_output_nodes)

    ##############################
    ## Create Data Validation List
    ##############################
    layers_df = layers_df[async_input_nodes]
    task_layer_data_list = layers_df.to_dict(orient='records')

    alpha = cds.pricing_selection.pareto_parameters.selected
    odf_parameter = cds.pricing_selection.odf_parameters.selected
    sliding_scale_ind = cds.risk_information.include_swing_rates
    loss_corridor_ind = cds.risk_information.include_loss_corridor
    aad_ind = cds.risk_information.include_aad

    task_data_dict = {
        "alpha": alpha,
        "odf_parameter": odf_parameter,
        "sliding_scale_ind": sliding_scale_ind,
        "loss_corridor_ind": loss_corridor_ind,
        "aad_ind": aad_ind,
    }

    ms.data_used_in_advanced_features_task = task_data_dict
    ms.layer_data_used_in_advanced_features_task = task_layer_data_list
    ms.has_run_advanced_features = True


def calculate_advanced_features(
    layers_df: pd.DataFrame,
    alpha: float,
    odp: float,
    target_lr: float,
    sliding_scale_flag: str,
    pc_flag: str,
    ncb_flag: str,
    loss_corridor_flag: str,
    aad_flag: str,
    num_simulations: int = no_of_simulations,
    actual_loading_factor: pd.Series = None,
) -> pd.DataFrame:
    """
    Calculation of advanced reinsurance features for all layers.
    Args:
        layers_df: DataFrame where each row represents a layer.
        alpha: Pareto parameter.
        odp: Overdispersed factor.
        target_lr: Target loss ratio.
        sliding_scale_flag: Flag for sliding scale inclusion.
        pc_flag: Flag for profit commission inclusion.
        ncb_flag: Flag for no-claims bonus inclusion.
        loss_corridor_flag: Flag for loss corridor inclusion.
        aad_flag: Flag for aggregate deductible inclusion.
        num_simulations: Number of simulations to run.
        actual_loading_factor: Optional loading factor.
    Returns:
        DataFrame with all calculated features as columns.
    """
    #################################################################
    ## Helper Function For Debugging
    #################################################################
    def save_csv(array, name):
        file_path = os.path.join(output_dir, f"layer_{layer_index}_{name}.csv")
        pd.DataFrame(array).to_csv(file_path, index=False, header=[name])

    ##############################
    ## Global parameters
    ##############################
    no_layers = len(layers_df)
    total_simulations = num_simulations

    ##############################
    ## Output initialization
    ##############################
    output_df = pd.DataFrame(index=layers_df.index)
    output_df["expected_aad"] = np.zeros(no_layers)
    output_df["loss_corridor_loss_cost"] = np.zeros(no_layers)
    output_df["expected_reinstatement_factor"] = np.zeros(no_layers)
    output_df["expected_ncb_pct"] = np.zeros(no_layers)
    output_df["profit_commission"] = np.zeros(no_layers)
    output_df["swing_premium"] = np.zeros(no_layers)
    output_df["expected_claims"] = np.zeros(no_layers)
    output_df["claim_frequency"] = np.zeros(no_layers)
    output_df["average_cost_per_claim"] = np.zeros(no_layers)

    #################################################################
    ## Helper functions
    #################################################################
    def calculate_negative_binomial_distribution(claim_frequency: float, negative_binomial_dispersion: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate the Negative Binomial distribution for claim counts.
        Returns:
            Tuple of (probability mass function, cumulative distribution function).
        """
        probability_mass_function = np.zeros(200)
        cumulative_probability = np.zeros(200)

        probability_mass_function[0] = (negative_binomial_dispersion / (negative_binomial_dispersion + claim_frequency)) ** negative_binomial_dispersion
        cumulative_probability[0] = probability_mass_function[0]

        for i in range(1, 200):
            probability_mass_function[i] = (
                probability_mass_function[i - 1]
                * (claim_frequency / (negative_binomial_dispersion + claim_frequency))
                * (i + negative_binomial_dispersion - 1)
                / i
            )
            cumulative_probability[i] = cumulative_probability[i - 1] + probability_mass_function[i]

        return probability_mass_function, cumulative_probability

    def simulate_layer_claims(
        num_simulations: int,
        cumulative_probability: np.ndarray,
        layer_sum_insured: float,
        excess: float,
        alpha: float,
        aggregate_deductible: float,
        aggregate_limit: float,
        random_counter: int,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Simulate claims for a layer.
        Returns:
            Tuple of (number of claims, total claim amounts, claims after reinsurance, claims excluding aggregate deductible, random numbers used).
        """
        no_of_claims = np.zeros(num_simulations)
        total_claim_amounts = np.zeros(num_simulations)
        total_claims_after_reinsurance = np.zeros(num_simulations)
        total_claims_excluding_aggregate_deductible = np.zeros(num_simulations)
        all_random_numbers = []

        for i in range(num_simulations):
            # x = (i + 1 - 0.5) / num_simulations
            probability = (i + 1 - 0.5) / num_simulations
            nt = 0

            # while nt < len(cumulative_probability) - 1 and x > cumulative_probability[nt]:
            while nt < len(cumulative_probability) - 1 and probability > cumulative_probability[nt]:
                nt += 1

            n = nt

            if n > 0:
                # TODO: Replace with np.random.uniform when the seed
                # implementation is available.
                #
                # u = np.random.uniform(
                #     0.0,
                #     1.0,
                #     claim_count,
                # )
                u = random_numbers[random_counter:random_counter + n]
                random_counter += n
                all_random_numbers.extend(u)

                # z = np.minimum(layer_sum_insured, excess / ((1 - u) ** (1 / alpha))) - excess
                claim_amounts = np.minimum(layer_sum_insured, excess / ((1 - u) ** (1 / alpha))) - excess

                no_of_claims[i] = n
                # total_claim_amounts[i] = np.sum(z)
                total_claim_amounts[i] = np.sum(claim_amounts)

                total_claims_after_reinsurance[i] = np.minimum(
                    aggregate_limit,
                    np.maximum(total_claim_amounts[i] - aggregate_deductible, 0)
                )
                total_claims_excluding_aggregate_deductible[i] = np.minimum(
                    aggregate_limit,
                    total_claim_amounts[i]
                )

        return no_of_claims, total_claim_amounts, total_claims_after_reinsurance, total_claims_excluding_aggregate_deductible, np.array(all_random_numbers)

    #################################################################
    ## Main loop
    #################################################################
    random_numbers_df = hx.params.random_numbers
    random_numbers = random_numbers_df["x"].values
    random_counter = 0

    for layer_index in range(no_layers):
        ##############################
        ## Extract inputs
        ##############################
        epi = layers_df.loc[layer_index, "epi_100"] or 0
        excess = layers_df.loc[layer_index, "excess"]
        limit_val = layers_df.loc[layer_index, "limit"]
        layer_sum_insured = (0 if pd.isna(limit_val) or limit_val == 0 else limit_val) + excess

        bound_premium = layers_df.loc[layer_index, "upfront_premium_gross_100"] or 0
        pure_premium = layers_df.loc[layer_index, "pricing_selection/final_selection/pure_premium"] or 0

        brokerage_ad = layers_df.loc[layer_index, "brokerage_ad"]
        brokerage = np.where(pd.isna(brokerage_ad), 0, brokerage_ad)
        loss_cap_used = layers_df.loc[layer_index, "loss_cap_used"]
        loss_cap = layers_df.loc[layer_index, "cap_gross_pct"]

        is_unlimited_rips = layers_df.loc[layer_index, "is_unlimited_rips"]

        rip = layers_df.loc[layer_index, [
            'reinstatement_pct_1', 'reinstatement_pct_2', 'reinstatement_pct_3',
            'reinstatement_pct_4', 'reinstatement_pct_5', 'reinstatement_pct_6',
            'reinstatement_pct_7', 'reinstatement_pct_8', 'reinstatement_pct_9',
            'reinstatement_pct_10'
        ]]

        aggregate_deductible = layers_df.loc[layer_index, "advanced_features_input/aad"]
        ncb = layers_df.loc[layer_index, "ncb"] or 0
        pc_rate = layers_df.loc[layer_index, "profit_commission_rate"] or 0
        pc_expense_allowance = layers_df.loc[layer_index, "expense_allowance"] or 0

        loss_corridor_share = layers_df.loc[layer_index, "loss_corridor/insured_participation"] or 0
        loss_corridor_max = layers_df.loc[layer_index, "loss_corridor/max_rate"]
        loss_corridor_min = layers_df.loc[layer_index, "loss_corridor/min_rate"]

        sliding_scale_deposit_rate = layers_df.loc[layer_index, "swing_rates/deposit_rate"]
        sliding_scale_min_rate = layers_df.loc[layer_index, "swing_rates/min_rate"]
        sliding_scale_max_rate = layers_df.loc[layer_index, "swing_rates/max_rate"]
        sliding_scale_margin = layers_df.loc[layer_index, "swing_rates/margin"]
        sliding_scale_actual_loading_factor = layers_df.loc[layer_index, "swing_rates/loading_factor"]

        ##############################
        ## Reinstatement setup
        ##############################
        if is_unlimited_rips:
            rip = np.zeros(999) # equivalent of pct input in page risk Information
            num_rips = 999 # calculated as non zero percentage, displayed in page Advanced Features
        else:
            num_rips = layers_df["number_of_rips"][layer_index] # calculated as non zero percentage, displayed in page Advanced Features

        ##############################
        ## Frequency and severity
        ##############################
        average_cost_per_claim = excess / (alpha - 1) * (1 - (excess / layer_sum_insured) ** (alpha - 1))
        claim_frequency = pure_premium / average_cost_per_claim
        negative_binomial_dispersion = claim_frequency / (odp - 1)

        probability_mass_function, cumulative_probability = calculate_negative_binomial_distribution(
            claim_frequency, negative_binomial_dispersion
        )

        ##############################
        ## Aggregate limit
        ##############################
        total_reinstatement_factors = 0
        cumulative_reinstatement_factors = np.zeros(int(num_rips))

        if is_unlimited_rips:
            aggregate_limit = (layer_sum_insured - excess) * 999 + aggregate_deductible

        if num_rips == 0:
            aggregate_limit = (layer_sum_insured - excess) + aggregate_deductible

        if num_rips > 0 and not is_unlimited_rips:
            for i in range(int(num_rips)):
                cumulative_reinstatement_factors[i] = np.sum(rip[:i + 1])
                total_reinstatement_factors = cumulative_reinstatement_factors[i]
                aggregate_limit = (layer_sum_insured - excess) * (num_rips + 1) + aggregate_deductible

        if loss_cap_used:
            aggregate_limit = loss_cap * bound_premium + aggregate_deductible
            # TODO Revised? Should this be the min of this formulae or the calculated aggregate limit calculated from the cases above?
            # aggregate_limit = min(loss_cap * bound_premium + aggregate_deductible, aggregate_limit)
            

        ##############################
        ## Simulate claims
        ##############################
        no_of_claims, total_claim_amounts, total_claims_after_reinsurance, total_claims_excluding_aggregate_deductible, u = simulate_layer_claims(
            total_simulations, cumulative_probability, layer_sum_insured, excess, alpha, aggregate_deductible, aggregate_limit, random_counter
        )

        ##############################
        ## Reinstatement usage
        ##############################
        reinstatement_count = np.zeros(total_simulations)
        partial_reinstatement_usage = np.zeros(total_simulations)
        total_reinstatement_factor = np.zeros(total_simulations)
        total_reinstatement_usage = np.zeros(total_simulations)

        if is_unlimited_rips or num_rips == 0:
            reinstatement_count[:] = 0
            partial_reinstatement_usage[:] = 0
            total_reinstatement_factor[:] = 0
            total_reinstatement_usage[:] = 0

        if num_rips > 0 and not is_unlimited_rips:
            for i in range(total_simulations):
                reinstatement_count[i] = int(total_claims_after_reinsurance[i] / (layer_sum_insured - excess))
                partial_reinstatement_usage[i] = total_claims_after_reinsurance[i] / (layer_sum_insured - excess) - reinstatement_count[i]

                if reinstatement_count[i] == 0:
                    total_reinstatement_factor[i] = partial_reinstatement_usage[i] * cumulative_reinstatement_factors[0]

                if reinstatement_count[i] >= num_rips:
                    total_reinstatement_factor[i] = total_reinstatement_factors

                if reinstatement_count[i] > 0 and reinstatement_count[i] < num_rips:
                    total_reinstatement_factor[i] = (
                        cumulative_reinstatement_factors[int(reinstatement_count[i]) - 1]
                        + rip[int(reinstatement_count[i])] * partial_reinstatement_usage[i]
                    )

                if reinstatement_count[i] == 0:
                    total_reinstatement_usage[i] = partial_reinstatement_usage[i]

                if reinstatement_count[i] >= num_rips:
                    total_reinstatement_usage[i] = num_rips

                if reinstatement_count[i] > 0 and reinstatement_count[i] < num_rips:
                    total_reinstatement_usage[i] = reinstatement_count[i] + partial_reinstatement_usage[i]

        ##############################
        ## Loss corridor
        ##############################
        if loss_corridor_flag:
            loss_corridor = loss_corridor_share * np.maximum(
                0,
                np.minimum(loss_corridor_max * epi, total_claims_after_reinsurance - loss_corridor_min * epi),
            )

            output_df["loss_corridor_loss_cost"][layer_index] = np.mean(loss_corridor)
            total_claims_after_reinsurance = total_claims_after_reinsurance - loss_corridor
            total_claims_excluding_aggregate_deductible = total_claims_excluding_aggregate_deductible - loss_corridor_share * np.maximum(
                0,
                np.minimum(loss_corridor_max * epi, total_claims_excluding_aggregate_deductible - loss_corridor_min * epi),
            )

        ##############################
        ## NCB (No Claims Bonus)
        ##############################
        prob_no_claims = np.sum(no_of_claims == 0) / len(no_of_claims)
        if ncb_flag:
            output_df["expected_ncb_pct"][layer_index] = prob_no_claims * ncb
        else:
            output_df["expected_ncb_pct"][layer_index] = 0

        ##############################
        ## Expected metrics
        ##############################
        expected_claims = np.mean(total_claims_after_reinsurance)
        expected_reinstatement_factor = np.mean(total_reinstatement_factor)

        output_df["expected_claims"][layer_index] = expected_claims
        output_df["expected_reinstatement_factor"][layer_index] = expected_reinstatement_factor

        if aad_flag:
            if np.any(aggregate_deductible != 0):
                output_df["expected_aad"][layer_index] = np.mean(total_claims_excluding_aggregate_deductible) - expected_claims

        output_df["claim_frequency"][layer_index] = np.mean(no_of_claims)
        output_df["average_cost_per_claim"][layer_index] = (
            expected_claims / output_df["claim_frequency"][layer_index]
        )

        ##############################
        ## Premium calculation
        ##############################
        if pc_flag:
            profit_commission_values = np.zeros(total_simulations)

            for i in range(total_simulations):
                profit_commission_values[i] = max(
                    (
                        (bound_premium - (total_claims_after_reinsurance[i] * (1 - output_df["expected_ncb_pct"][layer_index])))
                        - (bound_premium * pc_expense_allowance)
                    )
                    * pc_rate,
                    0,
                )

            output_df["profit_commission"][layer_index] = np.mean(profit_commission_values)

        ##############################
        ## Sliding scale
        ##############################
        if sliding_scale_flag:
            sliding_scale_premium = np.zeros(total_simulations)
            sliding_scale_loading = np.zeros(total_simulations)

            deposit_premium = sliding_scale_deposit_rate * epi
            min_premium = sliding_scale_min_rate * epi
            max_premium = sliding_scale_max_rate * epi
            brokerage_margin = epi * sliding_scale_margin * (brokerage or 0)

            for i in range(total_simulations):
                loaded_claims = total_claim_amounts[i] * sliding_scale_actual_loading_factor

                sliding_scale_premium[i] = min(
                    min_premium + loaded_claims, max_premium
                )

                sliding_scale_loading[i] = max(
                    sliding_scale_premium[i] - brokerage_margin - deposit_premium,
                    0,
                )

                if total_claims_after_reinsurance[i] == 0:
                    sliding_scale_loading[i] = (
                        min_premium - deposit_premium - brokerage_margin
                    )

                sliding_scale_loading = np.array(sliding_scale_loading)

            output_df["swing_premium"][layer_index] = np.mean(sliding_scale_loading)

        # Convert scalar agg_limit to array for consistency
        agg_limit_array = np.full(total_simulations, aggregate_limit)        
        # Uncomment for debugging on comment before saving the model version
        # # Save all required variables

        # save_csv(agg_limit_array, "agg_limit_aggregate_limit")
        # save_csv(total_claim_amounts, "y_total_claim_amounts")
        # save_csv(total_claims_after_reinsurance, "c_total_claims_after_reinsurance")
        # save_csv(total_claims_excluding_aggregate_deductible, "c_ad_total_claims_excluding_aggregate_deductible")
        # save_csv(u, "u_new")
        # save_csv(total_reinstatement_factor, "r_total_reinstatement_factor")

    return output_df
    