# v0.5.0
import hx, datetime, numpy as np, pandas as pd
import algorithms.rate_constants as const
from operator import itemgetter
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator, ratio
# from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me # commented as adjusted in a specific module in the model
from algorithms.model_profiler.profiling_hxd_functions import time_me

from algorithms.model_profiler.profiling_hxd_functions import time_me

from scipy.optimize import fsolve
import math as math

@time_me
def rate_healthcare_cat_exposure_rating(hxd):

    ##############################
    ## Initialise variables
    ##############################

    cy_yoa = hxd.cds.risk_information.inception_year

    hc = hxd.cds.healthcare_cat

    trial_lst = hc.trial_history.trial
    trial_num_years = len(hc.trial_history.trial)
    trial_df = pd_df_from_hx_list(hc.trial_history.trial)

    trial_total = hc.trial_history.total
    uw_view = hc.trial_history.uw_view

    expo_terr = hc.exposure_territory
    type_of_business = expo_terr.type_of_business
    specialty = expo_terr.specialty
    expo_per_y_df = pd_df_from_hx_list(expo_terr.overall_exposure_per_year)
    expo_years = len(expo_terr.overall_exposure_per_year)

    expo_per_state_df = pd_df_from_hx_list(expo_terr.exposure_spit_by_state)

    hc_location_df = hx.params.table_hc_location
    hc_trial_history_df = hx.params.table_hc_trial_history
    hc_exp_base_df = hx.params.table_hc_exp_base
    hc_surgical_type_df = hx.params.table_hc_surgical_type
    hc_high_low_df = hx.params.table_hc_high_low
    hc_social_inflation_df = hx.params.table_hc_social_inflation
    hc_lr_assumptions_df = hx.params.table_hc_lr_assumptions
    hc_ld_summary_percentile_df = hx.params.table_hc_loss_distribution_summary_percentile

    hc_pricing = hc.pricing

    loss_distrib_summary_df = pd_df_from_hx_list(hc_pricing.loss_distribution_summary)

    layers = hxd.cds.layers

    ld_calcs = hxd.healthcare_cat.pricing_calc.loss_distribution_calculation
    

    ##############################
    ## Page Trial History: Assign Page Trial History
    ##############################    

    trial_df["uw_year"] = [(cy_yoa - trial_num_years + x) for x in range(1,trial_num_years +1)] 
    trial_df["display_yoa"] = trial_df.uw_year.astype(int).astype(str)
    trial_df["win_pct"] = ratio(trial_df["wins"], trial_df["taken_to_trial"] )

    ##############################
    ## Calculate Total and Uw view
    ############################## 

    trial_children=[
        "taken_to_trial",
        "wins",
        "losses",
        "mistrials",
    ]

    # Filter the DataFrame for rows where uw_year is between from_year and to_year (inclusive)
    filtered_df = trial_df[(trial_df["uw_year"] >= uw_view.from_year) & (trial_df["uw_year"] <= uw_view.to_year)]
    
    for child in trial_children:
        # calculated Total for Trial
        setattr(trial_total,child, trial_df[child].sum())
        
        # calculated Total for underwriting view
        setattr(uw_view, child, filtered_df[child].sum())
    
    trial_total.win_pct = trial_total_win_pct = ratio(trial_total.wins, trial_total.taken_to_trial)
    # uw_view.win_pct = uw_view_win_pct = ratio(uw_view.wins, uw_view.taken_to_trial)
    sum_taken_to_trials = uw_view.wins + uw_view.losses + uw_view.mistrials
    uw_view.win_pct = uw_view_win_pct = ratio(uw_view.wins, sum_taken_to_trials)


    ##############################
    ## Page Exposure Territory: Assign Exposure Per Year
    ############################## 

    expo_per_y_df["uw_year"] = [(cy_yoa - expo_years + x) for x in range(1,expo_years +1)] 
    expo_per_y_df["display_yoa"] = expo_per_y_df.uw_year.astype(int).astype(str)
    columns_to_sum = [
        "physicians",
        "professional_associations",
        "ambulatory_surgery_centres",
        "hospitals",
        "ltc_facilities",
        "other_facilities",
        "dentists",
        "others"
    ]

    expo_per_y_df["total_physicians_in_force"] = expo_per_y_df[columns_to_sum].sum(axis=1)

    ##############################
    ## Page Exposure Territory: Assign Exposure Split Per State
    ############################## 

    expo_per_state_df["venue"] = hc_location_df["Area"]
    
    if expo_terr.choose_split_by == "Premium":
        expo_per_state_df["split"] = ratio(expo_per_state_df["premium_written"],expo_per_state_df["premium_written"].fillna(0).sum())
    else:
        expo_per_state_df["split"] = ratio(expo_per_state_df["total_pif_current_year"],expo_per_state_df["total_pif_current_year"].fillna(0).sum())

    ##############################
    ## Page Pricing Specifics : Assign Pricing Specifics
    ############################## 

    # Merge the DataFrames on 'venue' and 'Area'
    merged_df = expo_per_state_df.merge(
        hc_location_df,
        left_on="venue",
        right_on="Area",
        how="inner"
    )


    # Calculate territory_adjustment and sum it
    hc_pricing.territory_adjustment.value = territory_adjustment = (merged_df["split"] * merged_df["Loading"] * merged_df["Adjustment"]).sum()

    ##############################
    ## Page Pricing Specifics : trial_history_adjustment without linear interpolation
    ############################## 

    # Filter rows where "Win %" <= trial_total_win_pct
    #filtered_df = hc_trial_history_df[hc_trial_history_df["Win %"] <= trial_total_win_pct]

    # Get the "Loading" value from the row with the highest "Win %"
    # hc_pricing.trial_history_adjustment.value = trial_history_adjustment #= filtered_df.loc[filtered_df["Win %"].idxmax(), "Loading"]

    ##############################
    ## Page Pricing Specifics : trial_history_adjustment with linear interpolation
    ############################## 

    # Sort the DataFrame by "Win %" to ensure correct ordering
    sorted_df = hc_trial_history_df.sort_values(by="Win %")

    # Find the row where "Win %" is immediately lower or equal to trial_total_win_pct
    low_row = sorted_df[sorted_df["Win %"] <= trial_total_win_pct].tail(1)
    low_win_pct = low_row["Win %"].values[0] if not low_row.empty else sorted_df["Win %"].head(1).values[0]
    low_loading = low_row["Loading"].values[0] if not low_row.empty else sorted_df["Loading"].head(1).values[0]

    # Find the row where "Win %" is immediately higher or equal to trial_total_win_pct
    high_row = sorted_df[sorted_df["Win %"] >= trial_total_win_pct].head(1)
    high_win_pct = high_row["Win %"].values[0] if not high_row.empty else sorted_df["Win %"].tail(1).values[0]
    high_loading = high_row["Loading"].values[0] if not high_row.empty else sorted_df["Loading"].tail(1).values[0]

    # # Linear interpolation
    m = ratio((uw_view_win_pct - low_win_pct) , (high_win_pct - low_win_pct))
    trial_history_adjustment = ((1 - m) * low_loading + m * high_loading or 0)

    # Get the "Loading" value from the row with the highest "Win %"
    hc_pricing.trial_history_adjustment.value = trial_history_adjustment #= filtered_df.loc[filtered_df["Win %"].idxmax(), "Loading"]
    
    ##############################
    ## Page Pricing Specifics : Other Adjustment
    ##############################     
    hc_pricing.type_of_business_adjustment.value = type_of_business_adjustment = hc_exp_base_df.loc[hc_exp_base_df["Exposure Base"] == type_of_business, "Relativity"].values[0]

    hc_pricing.specialty_adjustment.value = specialty_adjustment = hc_surgical_type_df.loc[hc_surgical_type_df["Specialty"] == specialty, "Relativity"].values[0]

    hc_pricing.high_low_adjustment.value = high_low_adjustment = hc_high_low_df.loc[hc_high_low_df["High low agreement"] == hc_pricing.high_low_adjustment.select, "Loading"].values[0]

    hc_pricing.social_inflation_impact.value = social_inflation_impact = hc_social_inflation_df.loc[hc_social_inflation_df["Level"] == hc_pricing.social_inflation_impact.select, "Loading"].values[0]

    hc_pricing.total_risk_adjustment.value = total_risk_adjustment = territory_adjustment * trial_history_adjustment * type_of_business_adjustment * specialty_adjustment * high_low_adjustment * social_inflation_impact

    ##############################
    ## Page Pricing Specifics : Assign additional Layer nodes
    ##############################  
    for layer in layers:
        layer.healthcare_cat.detachment = (layer.excess or 0) + (layer.limit or 0)

    ##############################
    ## Page Pricing Specifics : Assign distribution nodes
    ##############################  
    one_in_50_lr = hc_lr_assumptions_df.loc[hc_lr_assumptions_df["Category"] == "1 in 50 LR", "Assumption"].values[0]

    hc_pricing.loss_ratio_1_in_50 = loss_ratio_1_in_50 = one_in_50_lr * math.sqrt(total_risk_adjustment)

    mean_loss_ratio = hc_lr_assumptions_df.loc[hc_lr_assumptions_df["Category"] == "Cat LR", "Assumption"].values[0]

    def calculate_mean_loss_ratio(decay_factor, lr_1_in_50, loss_distribution_df):
        # Band sizes
        band_size_forward_low = const.hc_band_size_0_to_75 # 0-75%
        band_size_forward_mid = const.hc_band_size_75_to_90  # 75%-90%
        band_size_forward_high = const.hc_band_size_90_to_100  # 90%-98%
        band_size_backward = const.hc_band_size_90_to_100  # 98% - 100%
       

        # Number of bands
        n_forward = const.n_forward # 150 bands - 0% to 75%
        n_mid = const.n_mid # 150 bands 75% to 90%
        n_high = const.n_high # 800 bands -  90% 98%
        n_backward = const.n_backward # 200 bands -  98% to 100%

        # Loss ratios below 98% (forward)
        lr_forward = np.zeros(n_forward + n_mid + n_high)
        lr_forward[-1] = lr_1_in_50  # 98th percentile
        for i in range(n_forward + n_mid + n_high -1 -1, -1, -1):
            if i <= n_forward: 
                lr_forward[i] = lr_forward[i + 1] * np.exp(-decay_factor * band_size_forward_low)
            elif n_forward < i <= n_forward + n_mid :
                lr_forward[i] = lr_forward[i + 1] * np.exp(-decay_factor * band_size_forward_mid)
            else:
                lr_forward[i] = lr_forward[i + 1] * np.exp(-decay_factor * band_size_forward_high)

        # Loss ratios above 1 in 50 or 98% percentile (backward)
        lr_backward = np.zeros(n_backward + 1)
        lr_backward[0] = lr_1_in_50  # 98th percentile
        for i in range(1, n_backward +1):
            lr_backward[i] = lr_backward[i - 1] * np.exp(decay_factor * band_size_backward)

        # Combine all loss ratios
        all_lr = np.concatenate([lr_forward, lr_backward[1:]])

        # Band sizes for each segment
        band_sizes = np.concatenate([
            np.full(n_forward, band_size_forward_low),
            np.full(n_mid , band_size_forward_mid),
            np.full(n_high, band_size_forward_high),
            np.full(n_backward, band_size_backward)
        ])


        # Assign columns to the provided DataFrame
        loss_distribution_df['loss_ratio'] = all_lr
        loss_distribution_df['band_size'] = band_sizes
        loss_distribution_df['percentile'] = loss_distribution_df['band_size'].cumsum()

        # Calculate mean loss ratio
        mean_lr = (loss_distribution_df['loss_ratio'] * loss_distribution_df['band_size']).sum()
        hc_pricing.mean_cat_ulr = mean_lr
        return loss_distribution_df, mean_lr

    def mean_loss_equation(decay_factor, mean_loss_ratio, lr_1_in_50,loss_distribution_df):
        loss_distribution_df, mean_loss_ratio_calculated = calculate_mean_loss_ratio(decay_factor, lr_1_in_50, loss_distribution_df)
        return mean_loss_ratio_calculated - mean_loss_ratio

    # Create empty DataFrame
    loss_distribution_df = pd.DataFrame()

    # Solve for decay_factor
    decay_factor_initial_guess = 100
    decay_factor_solution = fsolve(
        mean_loss_equation,
        decay_factor_initial_guess,
        args=(mean_loss_ratio, loss_ratio_1_in_50,loss_distribution_df)
    )[0]

    print(f"Decay factor: {decay_factor_solution:.6f}")

    hc_pricing.decay_factor  = decay_factor_solution

    ##############################
    ## Page Pricing: Loss distribution Summary
    ##############################       
        
    loss_distrib_summary_df["loss_percentile"] =  hc_ld_summary_percentile_df["Loss Percentile"]

    loss_distrib_summary_df["loss_percentile_display"] = (
        (loss_distrib_summary_df["loss_percentile"] * 100).astype(int).astype(str) + "%"
    )

    # Ensure consistent precision (important for float joins)
    loss_distrib_summary_df["loss_percentile"] = loss_distrib_summary_df["loss_percentile"].round(6)
    loss_distribution_df["percentile"] = loss_distribution_df["percentile"].round(6)

    # Perform mapping
    loss_distrib_summary_df = loss_distrib_summary_df.merge(
        loss_distribution_df[["percentile", "loss_ratio"]],
        left_on="loss_percentile",
        right_on="percentile",
        how="left"
    )

    # Assign ulr
    loss_distrib_summary_df["ulr"] = loss_distrib_summary_df["loss_ratio"]

    # Optional: drop helper columns
    loss_distrib_summary_df.drop(columns=["percentile", "loss_ratio"], inplace=True)

    ##############################
    ## Page Pricing Calculation: Loss distribution calculation
    ##############################    
    ld_calcs_df = loss_distribution_df.copy().rename(
        columns={"percentile": "loss_percentile", "loss_ratio": "ulr"}
    )

    ld_layer_columns = [
        "fgu_expected_cat_loss",
        "expected_loss_in_layer",
        "expected_loss_x_prob_of_loss",

    ]
    for index, layer in enumerate(layers):
        suffix = f'{index+1:02d}'
        for col in ld_layer_columns:
            layer_col = col + "_" + suffix
            if col == "fgu_expected_cat_loss":
                ld_calcs_df[layer_col] = ld_calcs_df["ulr"] * (layer.epi_100 or 0)
            elif col == "expected_loss_in_layer":
                ld_calcs_df[layer_col] = (
                    (ld_calcs_df[f"fgu_expected_cat_loss"+"_"+suffix] - (layer.excess or 0))
                    .clip(lower=0, upper=(layer.limit or 0))
                )
            else:
                ld_calcs_df[layer_col] = ld_calcs_df[f"expected_loss_in_layer"+"_"+suffix] * ld_calcs_df["band_size"] 


        ##############################
        ## Page Pricing: Expected Losses Total and Beazley
        ##############################   

        layer.healthcare_cat.expected_cost_in_layer_total = expected_cost_in_layer_total = ld_calcs_df[f"expected_loss_x_prob_of_loss"+"_"+suffix].sum()
        layer.healthcare_cat.expected_cost_in_layer_beazley_share = expected_cost_in_layer_total * (layer.written_line or 0)


    ##############################
    ## Write Trial History to hxd
    ##############################       

    trial_history_output_columns_str = [
        "display_yoa"
    ]
    trial_history_output_columns_flt = [
        "uw_year",
        "win_pct",
    ]
    # clean data before writing it hxd
    trial_df[trial_history_output_columns_str ] = trial_df[trial_history_output_columns_str ].fillna('')
    trial_df[trial_history_output_columns_flt ] = trial_df[trial_history_output_columns_flt ].fillna(0)

    write_pd_to_hxd(trial_df,  trial_lst,  trial_history_output_columns_str + trial_history_output_columns_flt )
    
    ##############################
    ## Write overall_exposure_per_year to hxd
    ##############################   

    expo_p_y_output_columns_str = [
        "display_yoa"
    ]
    expo_p_y_output_columns_flt = [
        "uw_year",
        "total_physicians_in_force",
    ]
    # clean data before writing it hxd
    expo_per_y_df[expo_p_y_output_columns_str ] = expo_per_y_df[expo_p_y_output_columns_str ].fillna('')
    expo_per_y_df[expo_p_y_output_columns_flt ] = expo_per_y_df[expo_p_y_output_columns_flt ].fillna(0)

    write_pd_to_hxd(expo_per_y_df,  expo_terr.overall_exposure_per_year,  expo_p_y_output_columns_str + expo_p_y_output_columns_flt )

    ##############################
    ## Write Exposure Split Per State to hxd
    ##############################  
    expo_p_state_output_columns_str = [
        "venue"
    ]
    expo_p_state_output_columns_flt = [
        
        "split",
    ]

    # clean data before writing it hxd
    expo_per_state_df[expo_p_state_output_columns_str ] = expo_per_state_df[expo_p_state_output_columns_str ].fillna('')
    expo_per_state_df[expo_p_state_output_columns_flt ] = expo_per_state_df[expo_p_state_output_columns_flt ].fillna(0)

    write_pd_to_hxd(expo_per_state_df,  expo_terr.exposure_spit_by_state,  expo_p_state_output_columns_str + expo_p_state_output_columns_flt )

    ##############################
    ## Write Page Pricing Loss Distribution Summary to hxd
    ##############################  
    loss_distrib_summary_output_columns_str = [
        "loss_percentile_display"
    ]
    loss_distrib_summary_output_columns_flt = [
        
        "loss_percentile",
        "ulr"
    ]
    # clean data before writing it hxd
    loss_distrib_summary_df[loss_distrib_summary_output_columns_str ] = loss_distrib_summary_df[loss_distrib_summary_output_columns_str ].fillna('')
    loss_distrib_summary_df[loss_distrib_summary_output_columns_flt ] = loss_distrib_summary_df[loss_distrib_summary_output_columns_flt ].fillna(0)

    write_pd_to_hxd(loss_distrib_summary_df, hc_pricing.loss_distribution_summary,  loss_distrib_summary_output_columns_str + loss_distrib_summary_output_columns_flt )

    # ##############################
    # ## Write Page Pricing Calculation to hxd
    # ##############################  

    hxd.healthcare_cat.pricing_calc.loss_distribution_calculation = ld_calcs_df.to_dict(orient='records')

    return

