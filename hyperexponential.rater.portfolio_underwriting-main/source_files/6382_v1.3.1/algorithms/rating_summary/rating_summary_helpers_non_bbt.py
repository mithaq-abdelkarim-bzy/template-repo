import hx
import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from algorithms                                           import parameter_tables_schema as params
from algorithms.anti_selection.anti_selection_helpers     import build_anti_selection_applied_charge
from algorithms.uncertainty.uncertainty_helpers           import build_uncertainty_applied_charge
from algorithms.risk_information.risk_information_helpers import import_inception_date
from algorithms                                           import parameter_tables_schema as params
import algorithms.validations.rating_summary_validations as validations
from algorithms.rating_summary.rating_summary_totals_helpers import (
    build_projected_gn_ulr_summary,
    build_model_weights_summary,
    build_cat_loadings_summary,
    build_additional_loadings_summary,
    build_tech_prem_build_up_summary,
    build_pricing_adequacy_metrics_summary,
    build_trifocus_summary_totals,
    build_cat_ulr_summary_totals
)

def set_tech_prem_dropdown_list(hxd):
    # Import the inception date for the current Hx dataset
    inception_date = import_inception_date(hxd)
    # Load TPI parameters from the Hx dataset
    tpi_params_df = params.tp_parameters.df()

    # Ensure all Years of Assessment (YoA) values are integers and sort them
    years_list = sorted(map(int, tpi_params_df["year"].unique()))

    # Set the TPI year dropdown options to the sorted list of YoA
    hxd.cds.rating_summary.technical_premium_build_up.tpi_year_dropdown = years_list

    # Set the initial TPI year to the smaller of the inception year or latest YoA
    hxd.cds.rating_summary.technical_premium_build_up.tpi_year.calculated = min(inception_date.year, years_list[-1])


def build_projected_gn_ulr_df(hxd,                  rating_summary_path,  prem_data_available, prem_limit_prof_df, 
                              own_exp_df,           bp_proj_df,           proj_lloyds_sum_df,  proj_bzly_sum_df,  rater):
    
    port_prof_summary_df = rater.get("portfolio_profile_summary", pd.DataFrame())
    proj_df              = rater.get("rat_sum_proj_gnulr", pd.DataFrame())

    # Aggregate premium and portfolio data by line of business (LOB)
    grouped_df = (prem_limit_prof_df.groupby("selected_lob", sort=False)
                                    .agg({
                                        "portfolio_composition" : "sum",
                                        "bst_net_premium"       : "sum",
                                        "assigned_trifocus"     : "first",
                                        "bst_deductions"        : "first"})
                                    .reset_index()    )

    # Assign aggregated values to the projected dataframe
    proj_df = proj_df.assign(   selected_lob     =grouped_df['selected_lob'         ],
                                tracker_class    =grouped_df['assigned_trifocus'    ],
                                gn_premium       =grouped_df['bst_net_premium'      ].fillna(0),
                                portfolio_percent=grouped_df['portfolio_composition'].fillna(0),
                                total_deductions =grouped_df['bst_deductions'       ].fillna(0))

    # Data Cleansing
    proj_df['is_row_visible']    = proj_df['selected_lob'].notna()          # Set row visibility based on presence of LOB
    proj_df['gn_premium']        = proj_df['gn_premium'].fillna(0)          # Fill any remaining NaNs with 0
    proj_df['portfolio_percent'] = proj_df['portfolio_percent'].fillna(0)   # Fill any remaining NaNs with 0

    # Filter out rows without a LOB
    proj_df = proj_df[proj_df["selected_lob"].notna()].reset_index(drop=True)

    # Handle own experience GN ULR depending on availability of premium data
    proj_df['own_exp_gn_ulr'] = own_exp_df['selected_total'].fillna(0) if prem_data_available else 0
    
    # map loss ratios based on lloyds and beazley
    cols_ulr = ['selected_lob','composition','weighted_ulr']
    for col, df in zip( ['beazley_gn_ulr','lloyds_gn_ulr'],  [proj_bzly_sum_df, proj_lloyds_sum_df]):
        df['weighted_ulr']  = df['composition'] * df['selected_final_gn_ulr']
        grp_df              = df[cols_ulr].groupby("selected_lob").sum().reset_index().fillna(0)
        # grp_df              = df.groupby('selected_lob', as_index=False).agg(
        #                             composition= ('composition',  'sum'),
        #                             col=         (col,            'sum'),
        #                             weighted_ulr=('weighted_ulr', 'sum')    )
        grp_df[col]         = utils.ratio( grp_df['weighted_ulr'],  grp_df['composition']   )
        cols_merge          = ['selected_lob'] + [col]
        proj_df             = utils.drop_and_merge(proj_df,    grp_df[cols_merge],   "selected_lob")


    # Map LOBs to BP projected GN ULR
    proj_df['bp_gn_ulr'] = proj_df['selected_lob'].map(     dict(zip(bp_proj_df['selected_lob'], bp_proj_df['adj_total_gn_ulr']))    ).fillna(0)

    # Get Hx path for projected GN ULR table
    projected_gn_ulr_path = rating_summary_path.model_gn_ulr.projected_gn_ulr.table

    # Write the processed dataframe back to the rater
    rater['rat_sum_proj_gnulr'] = proj_df[:grouped_df.shape[0]]
    
    return proj_df


def build_model_weights_df(rating_summary_path, proj_df, rater, warning_path):
    # Load model weights table from Hx
    model_weights_path = rating_summary_path.model_gn_ulr.model_weights.table
    model_weights_df = rater.get("rat_sum_mod_wgt", pd.DataFrame())

    # Assign LOBs and visibility flags
    model_weights_df['selected_lob'] = proj_df['selected_lob']
    model_weights_df['is_row_visible'] = model_weights_df['selected_lob'].notna()
    model_weights_df = model_weights_df[model_weights_df["selected_lob"].notna()].reset_index(drop=True)

    # Map GN ULR columns to corresponding weight columns
    gn_ulr_and_weight_map = {
        'own_exp_gn_ulr': 'own_experience',
        'lloyds_gn_ulr': 'lloyds_proj',
        'beazley_gn_ulr': 'beazley_proj',
        'bp_gn_ulr': 'bp_proj',
        'case_pricing': 'case_pricing'
    }

    # Fill missing weights with 0
    model_weights_df[list(gn_ulr_and_weight_map.values())] = \
        model_weights_df[list(gn_ulr_and_weight_map.values())].fillna(0)
        
    # Calculate sum of weights for validation
    weight_cols = gn_ulr_and_weight_map.values()
    model_weights_df['weighting_check'] = model_weights_df[weight_cols].sum(axis=1)

    # Mark rows where weights sum to 1 as TRUE, else FALSE
    # Use np.isclose for robust floating point comparison with tolerance
    model_weights_df['weighting_check'] = np.where(
        np.isclose(model_weights_df['weighting_check'], 1, atol=1e-9),
        "TRUE",
        "FALSE"
    )

    # Compute model estimate using weights and GN ULR values
    ulr_df = proj_df[list(gn_ulr_and_weight_map.keys())].copy()
    weight_df = model_weights_df[[gn_ulr_and_weight_map[col] for col in ulr_df.columns]].copy()
    weight_df.columns = ulr_df.columns
    model_weights_df['model_estimate'] = (ulr_df * weight_df).sum(axis=1)

    # Show warning when weighting given to own experience but the loss ratio is 0 (as a proxy for no data entered)
    validations.check_model_weightings_no_experience(warning_path, weight_df['own_exp_gn_ulr'], ulr_df['own_exp_gn_ulr'])

    # Write the processed dataframe back to the rater
    rater['rat_sum_mod_wgt'] = model_weights_df

    return model_weights_df


def build_cat_loadings(rating_summary_path, prem_data_available, own_exp_df, bp_proj_df, model_weights_df, rater):

    cat_loadings_df  = rater.get("rat_sum_cat_alloc", pd.DataFrame())

    # Assign LOBs and visibility flags
    cat_loadings_df['selected_lob']     = model_weights_df['selected_lob']
    cat_loadings_df['is_row_visible']   = cat_loadings_df['selected_lob'].notna()
    cat_loadings_df                     = cat_loadings_df[cat_loadings_df["selected_lob"].notna()].reset_index(drop=True)

    # Compute own experience catastrophe ratios if premium data is available
    if prem_data_available:
        own_exp_df['cat_exp']               = np.where(own_exp_df["selected_total"] == 0, 0,own_exp_df["selected_cat"] / own_exp_df["selected_total"]        )
        cat_loadings_df["cat_exp"]          = cat_loadings_df['selected_lob'].map(dict(zip(own_exp_df['selected_lob'], own_exp_df['cat_exp']))).fillna(0)
        cat_loadings_df["attr_and_lrg_exp"] = 1 - cat_loadings_df["cat_exp"]        # Complement for attritional and large losses
        lob_to_claim_basis_map = dict(zip(own_exp_df['selected_lob'], own_exp_df['claim_basis']))       # Map LOBs to claim basis from own experience
        cat_loadings_df['claim_basis'] = cat_loadings_df['selected_lob'].map(lob_to_claim_basis_map)
    else:
        cat_loadings_df["cat_exp"]          = 0
        cat_loadings_df["attr_and_lrg_exp"] = 0
        cat_loadings_df['claim_basis']      = "Total"

    # Compute BP attritional and large loss ratio
    bp_proj_df["attr_and_lrg_bp"]       = np.where(bp_proj_df['adj_total_gn_ulr'] == 0,0,bp_proj_df['adj_attr_gn_ulr'] / bp_proj_df['adj_total_gn_ulr'])
    cat_loadings_df["attr_and_lrg_bp"]  = cat_loadings_df["selected_lob"].map(dict(zip(bp_proj_df["selected_lob"], bp_proj_df["attr_and_lrg_bp"]))).fillna(0)
    cat_loadings_df["cat_bp"]           = 1 - cat_loadings_df["attr_and_lrg_bp"]    # Complement to get BP cat ratio



    # Compute final cat ratio based on claim basis and weights
    cat_loadings_df['cat'] = np.where(      cat_loadings_df['cat'].isna()
                                , np.where( cat_loadings_df['claim_basis'] == "Total"  ,  cat_loadings_df['cat_bp']
                                                                                       ,  cat_loadings_df['cat_exp'] * model_weights_df['own_experience'] 
                                                                                        + cat_loadings_df['cat_bp'] * (1 - model_weights_df['own_experience']))
                                , cat_loadings_df['cat'] )

    # Compute attritional and large loss ratio
    cat_loadings_df['attr_and_lrg'] = 1 - cat_loadings_df['cat']

    # Map climate change and NMP loads
    cat_loadings_df['climate_change_load'] = cat_loadings_df['selected_lob'].map(        dict(zip(bp_proj_df['selected_lob'], bp_proj_df['cat_climate_change']))    ).fillna(0)
    cat_loadings_df['nmp_load_general']    = cat_loadings_df['selected_lob'].map(        dict(zip(bp_proj_df['selected_lob'], bp_proj_df['cat_nmp_general']))       ).fillna(0)
    cat_loadings_df['nmp_load_weather']    = cat_loadings_df['selected_lob'].map(        dict(zip(bp_proj_df['selected_lob'], bp_proj_df['cat_nmp_all_other']))     ).fillna(0)

    # Write updated catastrophe loadings back to rater
    rater['rat_sum_cat_alloc']= cat_loadings_df
 
    return cat_loadings_df


def build_additional_loadings_df(rating_summary_path, proj_df, hxd, rater):
    # Load dataframes
    anti_selection_df        = rater.get("anti_sel_applied_charge", pd.DataFrame())
    uncertainty_df           = rater.get("uncertainty_applied_charge", pd.DataFrame())
    additional_loadings_df   = rater.get("rat_sum_add_load", pd.DataFrame())

    # build dicts
    dict_lob_as = dict(  zip( anti_selection_df['selected_lob'], anti_selection_df['anti_selection_charge'] )  ) 
    dict_lob_unc= dict(  zip( uncertainty_df[   'selected_lob'], uncertainty_df[   'load'                 ] )  )

    # assign values to df    
    additional_loadings_df['selected_lob']          = proj_df['selected_lob']                                                   # Add selected LOB column from project dataframe
    additional_loadings_df['is_row_visible']        = additional_loadings_df['selected_lob'].notna()                            # Flag rows as visible if selected_lob is not null
    additional_loadings_df                          =(additional_loadings_df[  additional_loadings_df['is_row_visible']  ]
                                                            .reset_index(drop=True)        )                                    # Filter out rows with missing LOB and reset index
    additional_loadings_df['anti_selection_charge'] = additional_loadings_df['selected_lob'].map(   dict_lob_as    ).fillna(0)  # Map anti-selection charges to the LOBs
    additional_loadings_df['uncertainty_charge']    = additional_loadings_df['selected_lob'].map(   dict_lob_unc  ).fillna(0)   # Map uncertainty charges to the LOBs  

   
    # Write updated additional loadings back to rater
    rater['rat_sum_add_load']= additional_loadings_df

    return additional_loadings_df


def calculate_profit_commission_impact_pre_adj(is_pc, pricing_adequacy_pre_adj_df, pricing_adequacy_act_basis_df):
    # If profit commission is applicable
    if is_pc:
        # Initialize factor column
        pricing_adequacy_pre_adj_df["factor"] = 0
        
        # Mask rows where pre-PC-adjusted estimate is non-zero
        mask = pricing_adequacy_pre_adj_df['best_estimate_pre_pc_adj'] != 0
        
        # Calculate adjustment factor
        pricing_adequacy_pre_adj_df.loc[mask, "factor"] = (            pricing_adequacy_act_basis_df.loc[mask, 'best_estimate_pre_pc_adj']            / pricing_adequacy_pre_adj_df.loc[mask, 'best_estimate_pre_pc_adj']        )

        # Scale profit commission impact by factor
        pricing_adequacy_pre_adj_df['pc_impact'] = (            pricing_adequacy_act_basis_df["pc_impact"]            * pricing_adequacy_pre_adj_df["factor"]        )
        
        # Fill any missing values with 0
        pricing_adequacy_pre_adj_df['pc_impact'] = pricing_adequacy_pre_adj_df['pc_impact'].fillna(0)
    else:
        # If no profit commission, set impact to 0
        pricing_adequacy_pre_adj_df['pc_impact'] = 0

    return pricing_adequacy_pre_adj_df['pc_impact']


def init_pricing_adequacy_act_basis_df(hxd, model_weights_df, cat_loading_df, additional_loadings_df, rater):
    # Load pricing adequacy actuarial basis table from HxD is unnecessary as all outputs
    pricing_adequacy_actuarial_basis_path = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis.table
    pricing_adequacy_act_basis_df = pd.DataFrame()

    # Add selected LOB column from model weights
    pricing_adequacy_act_basis_df['selected_lob'] = model_weights_df["selected_lob"]
    
    # Flag rows as visible if LOB is not null
    pricing_adequacy_act_basis_df['is_row_visible'] = pricing_adequacy_act_basis_df['selected_lob'].notna()
    
    # Filter out rows with missing LOBs
    pricing_adequacy_act_basis_df = pricing_adequacy_act_basis_df[pricing_adequacy_act_basis_df["selected_lob"].notna()].reset_index(drop=True)

    # Replace NaN additional charges with 0
    additional_loadings_df['additional_charge'] = np.where(   additional_loadings_df['additional_charge'].isna(),     0,     additional_loadings_df['additional_charge']    )

    # Compute total charges combining anti-selection, uncertainty, and additional charges
    additional_loadings_df["sum_charges"] = (additional_loadings_df['anti_selection_charge']    + additional_loadings_df['uncertainty_charge']     + additional_loadings_df['additional_charge'])

    # Compute best estimate pre-profit-commission-adjustment
    pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj"] = (   model_weights_df['model_estimate'] * (1 - cat_loading_df['cat'])
                                                                    + ( (model_weights_df['model_estimate'] * cat_loading_df['cat'] * (1 + cat_loading_df["climate_change_load"]))
                                                                         + cat_loading_df["nmp_load_general"]
                                                                         + cat_loading_df["nmp_load_weather"]        )
                                                                    + additional_loadings_df["sum_charges"]           ) 
                                                                

    # Calculate profit commission impact
    pricing_adequacy_act_basis_df["pc_impact"] = calculate_profit_commission_impact_act_basis(
        hxd, 
        pricing_adequacy_act_basis_df[["best_estimate_pre_pc_adj" , "selected_lob"]],
        rater
        )

    # Compute final best estimate including profit commission impact
    pricing_adequacy_act_basis_df['best_estimate'] = (     pricing_adequacy_act_basis_df['pc_impact']   + pricing_adequacy_act_basis_df['best_estimate_pre_pc_adj']   )

    # Initialize BPI (best pricing indicator)
    pricing_adequacy_act_basis_df["bpi"] = 0
    mask = pricing_adequacy_act_basis_df['best_estimate'] != 0
    pricing_adequacy_act_basis_df.loc[mask, "bpi"] = constants.BENCHMARK_LR /  pricing_adequacy_act_basis_df.loc[mask, 'best_estimate']

    return pricing_adequacy_act_basis_df


def init_pricing_adequacy_pre_adj_df(hxd, is_pc, pricing_adequacy_act_basis_df, proj_df, model_weights_df, cat_loading_df):
    # Load path to pre-adjusted pricing adequacy
    pre_adj_path = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj

    # Initialize empty dataframe with required number of rows
    pricing_adequacy_pre_adj_df = proj_df[['selected_lob']].copy()
    
    # Flag rows as visible
    pricing_adequacy_pre_adj_df['is_row_visible'] = pricing_adequacy_pre_adj_df['selected_lob'].notna()
    
    # Filter out rows with missing LOBs
    pricing_adequacy_pre_adj_df = pricing_adequacy_pre_adj_df[pricing_adequacy_pre_adj_df["selected_lob"].notna()].reset_index(drop=True)

    # Compute pre-profit-commission-adjusted best estimate
    pricing_adequacy_pre_adj_df["best_estimate_pre_pc_adj"] = model_weights_df['model_estimate'] \
        * (1 - cat_loading_df['cat']) \
        + ((model_weights_df['model_estimate'] * cat_loading_df['cat'] *
            (1 + cat_loading_df["climate_change_load"])) + cat_loading_df["nmp_load_general"]
           + cat_loading_df["nmp_load_weather"])

    # Calculate profit commission impact
    pricing_adequacy_pre_adj_df["pc_impact"] = calculate_profit_commission_impact_pre_adj(
        is_pc,
        pricing_adequacy_pre_adj_df[["best_estimate_pre_pc_adj"]],
        pricing_adequacy_act_basis_df[["best_estimate_pre_pc_adj", "pc_impact"]])

    # Compute final best estimate including profit commission impact
    pricing_adequacy_pre_adj_df['best_estimate'] = np.where(
        pricing_adequacy_pre_adj_df['best_estimate_pre_pc_adj'] == 0,
        0,
        pricing_adequacy_pre_adj_df['pc_impact']
        + pricing_adequacy_pre_adj_df['best_estimate_pre_pc_adj']
    )

    # Compute BPI
    pricing_adequacy_pre_adj_df['bpi'] = 0
    mask = pricing_adequacy_pre_adj_df['best_estimate'] != 0
    pricing_adequacy_pre_adj_df.loc[mask, "bpi"] = (
        constants.BENCHMARK_LR / pricing_adequacy_pre_adj_df.loc[mask, 'best_estimate']
    )

    return pricing_adequacy_pre_adj_df


def calculate_profit_commission_impact_act_basis(hxd, pricing_adequacy_act_basis_df, rater):
    # Check if profit commission is applicable
    is_there_profit_commission = hxd.cds.risk_information.is_profit_comission
    pc_path = hxd.cds.pc.profit_commission

    if is_there_profit_commission and len(pc_path.details):
        # Load profit commission details
        pc_df = rater.get("pc_details", pd.DataFrame())

        # setting up dicts
        dict_lob_pc_imp = dict(zip(pc_df["selected_lob"], pc_df["pc_impact"]))
        dict_lob_pc_adj = dict(zip(pc_df["selected_lob"], pc_df["best_estimate_pre_pc_adj"]))

        # mapping the columns
        pricing_adequacy_act_basis_df["pc_impact"]                    = ( pricing_adequacy_act_basis_df["selected_lob"]     # Map PC impact by LOB
                                                                            .map(  dict_lob_pc_imp  ).fillna(0)      )
        pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj_ref"] = ( pricing_adequacy_act_basis_df["selected_lob"]     # Store reference pre-PC-adjusted estimate
                                                                            .map(dict_lob_pc_adj).fillna(0)             )
        pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj"]     = pricing_adequacy_act_basis_df["best_estimate_pre_pc_adj"].fillna(0) # Ensure no missing values in pre-PC-adjusted best estimate

        # Perform validation on best estimate changes
        validations.check_best_estimate_pre_pc_adj_change(hxd, pricing_adequacy_act_basis_df[["best_estimate_pre_pc_adj", "best_estimate_pre_pc_adj_ref"]])

    elif is_there_profit_commission and not len(pc_path.details):
        # If no profit commission, set impact to 0
        pricing_adequacy_act_basis_df["pc_impact"] = 0
        # Pass empty df for validation
        validations.check_best_estimate_pre_pc_adj_change(hxd, pd.DataFrame())
    else:
        # If no profit commission, set impact to 0
        pricing_adequacy_act_basis_df["pc_impact"] = 0

    return pricing_adequacy_act_basis_df["pc_impact"]


def build_pricing_adequacy_final_df(path, proj_df, pricing_adequacy_act_basis_df, deductions_df, rater):
    # Load final pricing adequacy dataframe
    pricing_adequacy_final_df = rater.get("rat_sum_adeq_final", pd.DataFrame())

    # setting up the basic dataframe
    pricing_adequacy_final_df['selected_lob']   = proj_df["selected_lob"]                                           # Add selected LOBs
    pricing_adequacy_final_df['is_row_visible'] = pricing_adequacy_final_df['selected_lob'].notna()                 # Flag rows as visible
    row_filter                                  = pricing_adequacy_final_df['is_row_visible']
    pricing_adequacy_final_df                   = pricing_adequacy_final_df[ row_filter ].reset_index(drop=True)    # Filter out rows with missing LOBs

    # Validate underwriting adjustments
    validations.check_uw_adj_limits(pricing_adequacy_final_df["uw_adj"].fillna(0))

    # Compute gross best estimate
    pricing_adequacy_final_df['best_estimate_gn'] = (  pricing_adequacy_final_df["uw_adj"].fillna(0)
                                                     + pricing_adequacy_act_basis_df['best_estimate'])
    # Map effective deductions by LOB
    dict_lob_ded = dict(zip(deductions_df["selected_lob"],deductions_df["selected_effective_deductions"]))
    pricing_adequacy_final_df["effective_deductions"] = pricing_adequacy_final_df["selected_lob"].map( dict_lob_ded ).fillna(0)

    # Compute net best estimate after deductions
    pricing_adequacy_final_df['best_estimate_gg'] = (   pricing_adequacy_final_df['best_estimate_gn']
                                                      * (1 - pricing_adequacy_final_df['effective_deductions']) )
    # Compute BPI
    bench_lr                                    = constants.BENCHMARK_LR
    pricing_adequacy_final_df["bpi"]            = 0
    mask                                        = pricing_adequacy_final_df['best_estimate_gn'] != 0
    pricing_adequacy_final_df.loc[mask, "bpi"]  = bench_lr / pricing_adequacy_final_df.loc[mask, 'best_estimate_gn']

    return pricing_adequacy_final_df


def build_cat_ulr_summary_df(rating_summary_path, proj_df, model_weights_df, cat_loading_df, rater):
    
    # prep work - path & empty df
    cat_ulr_summary_path = rating_summary_path.cat_ulr_summary.details
    cat_ulr_summary_df   = pd.DataFrame()

    # calculate the necessary columns
    cat_ulr_summary_df['selected_lob']          = proj_df["selected_lob"]                                   # Copy selected line of business from project DataFrame
    cat_ulr_summary_df['is_row_visible']        = cat_ulr_summary_df['selected_lob'].notna()                # Boolean column indicating whether the row is visible (selected LOB exists)
    cat_ulr_summary_df['gn_cat_ulr_excl_loads'] = cat_loading_df["cat"] * model_weights_df["model_estimate"]# Calculate gross natural category ULR excluding additional loadings
    cat_ulr_summary_df['gn_cat_ulr_inc_loads']  = (   cat_ulr_summary_df["gn_cat_ulr_excl_loads"]
                                                    * (1 + cat_loading_df["climate_change_load"])
                                                    + cat_loading_df['nmp_load_general']
                                                    + cat_loading_df['nmp_load_weather']         )          # Calculate gross natural category ULR including additional loadings

    # Write the DataFrame to the designated path (custom utility function)
    rater['rat_sum_cat_ulr'] = cat_ulr_summary_df

    return cat_ulr_summary_df


def build_tech_prem_df(hxd, proj_df, pricing_adequacy_pre_adj_df, pricing_adequacy_act_basis_df, pricing_adequacy_final_df):
    # Retrieve TPI parameters table
    tpi_params_df   = params.tp_parameters.df()
    # Get the selected TPI year from the rating summary path
    incept_yr = hxd.hx_core.inception_date.year
    tpi_year  = hxd.cds.rating_summary.technical_premium_build_up.tpi_year.selected or incept_yr


    # Initialize technical premium DataFrame with relevant project columns
    tech_prem_df = proj_df[['selected_lob', "tracker_class", "is_row_visible"]]

    # Calculate expected loss for pre-adjustment, actuarial, and final basis
    tech_prem_df['el_pre_adj']  = pricing_adequacy_pre_adj_df['best_estimate'] * proj_df['gn_premium']
    tech_prem_df['el_actuarial']= pricing_adequacy_act_basis_df['best_estimate'] * proj_df['gn_premium']
    tech_prem_df['el_final']    = pricing_adequacy_final_df['best_estimate_gn'] * proj_df['gn_premium']
    # Fill missing final expected loss with zero
    tech_prem_df['el_final']    = tech_prem_df['el_final'].fillna(0)

    # Create mapping key for TPI parameters table
    tpi_params_df["map"]        = tpi_params_df["business_plan_class"] + tpi_params_df["year"].astype(int).astype(str)
    tech_prem_df["map"]         = tech_prem_df["tracker_class"] + str(tpi_year)

    # Map various ratios from TPI table to project DataFrame
    tech_prem_df["net_expense"]      = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["var_exp"]))).fillna(0)
    tech_prem_df["inv_income"]       = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["inv_inc"]))).fillna(0)
    tech_prem_df["ri_premium"]       = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["cost_of_ri"]))).fillna(0)
    tech_prem_df["ri_recoveries"]    = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["ri_rec"]))).fillna(0)
    tech_prem_df["capital_required"] = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["capital_req"]))).fillna(0)
    tech_prem_df["target_roc"]       = tech_prem_df["map"].map(dict(zip(tpi_params_df["map"], tpi_params_df["roc"]))).fillna(0)

    # Calculate the factor for technical premium adjustment
    if tpi_year < 2026:
        tech_prem_df["factor"] = ( 1 -  tech_prem_df['net_expense']
                                    - (tech_prem_df['ri_premium'] - tech_prem_df['ri_recoveries'])
                                    +  tech_prem_df['inv_income'] * (1 - tech_prem_df['ri_premium'])
                                    - (tech_prem_df['target_roc'] * tech_prem_df['capital_required'] * (1 - tech_prem_df['ri_premium']))    )
    else:
        tech_prem_df["factor"] = ( 1 -  tech_prem_df['net_expense']
                                    - (tech_prem_df['ri_premium'] - tech_prem_df['ri_recoveries'])
                                    +  tech_prem_df['inv_income'] 
                                    - (tech_prem_df['target_roc'] * tech_prem_df['capital_required'])    )


    # Calculate technical premium for each basis
    # Use mask for all three at once
    mask = tech_prem_df["factor"]  != 0
    tech_prem_df['tp_pre_adj']      = np.where(mask, tech_prem_df['el_pre_adj']   / tech_prem_df["factor"], 0)
    tech_prem_df['tp_actuarial']    = np.where(mask, tech_prem_df['el_actuarial'] / tech_prem_df["factor"], 0)
    tech_prem_df['tp_final']        = np.where(mask, tech_prem_df['el_final']     / tech_prem_df["factor"], 0)

    # Calculate gross/gross final technical premium including deductions
    brk = proj_df["total_deductions"].fillna(0)
    tech_prem_df['gg_tp_final'] = utils.ratio(tech_prem_df['tp_final'], 1 - brk)

    # Benchmark final expected loss (70% benchmark)
    tech_prem_df['gg_bm_final'] = utils.ratio(tech_prem_df['el_final'], constants.BENCHMARK_LR * (1 - brk))

    return tech_prem_df


def calculate_tpi_roc(df, tech_prem_df, proj_df, pricing_type, tpi_year):
    # Determine which technical premium column to use based on pricing type
    tp_col_name = ( "tp_pre_adj"    if pricing_type == "pre_adj"   else 
                    "tp_actuarial"  if pricing_type == "act_basis" else 
                    "tp_final"                                          )

    # Determine best estimate column based on pricing type
    best_estimate_col_name = ( "best_estimate" if       pricing_type == "pre_adj" or pricing_type == "act_basis"      else "best_estimate_gn"   )

    df["tpi"] = 0
    # Mask to avoid division by zero
    mask                = tech_prem_df[tp_col_name] != 0
    df.loc[mask, "tpi"] = proj_df.loc[mask, "gn_premium"] / tech_prem_df.loc[mask, tp_col_name]
    df['tpi']           = df['tpi'].fillna(0)

    # Calculate rate of capital (ROC)
    if tpi_year < 2026:
        df['roc'] = utils.ratio(  ( 1   - df[best_estimate_col_name]
                                        - (tech_prem_df['ri_premium']  - tech_prem_df['ri_recoveries']   )
                                        + (tech_prem_df['inv_income']  * (1 - tech_prem_df['ri_premium']))
                                        - (tech_prem_df['net_expense']                                   ))
                                 ,(tech_prem_df['capital_required']   * (1 - tech_prem_df['ri_premium']  )))
    else:
        df['roc'] = utils.ratio( ( 1   - df[best_estimate_col_name]
                                       - (tech_prem_df['ri_premium']  - tech_prem_df['ri_recoveries']    )
                                       + (tech_prem_df['inv_income']                                     )
                                       - (tech_prem_df['net_expense']                                    ))
                                ,(tech_prem_df['capital_required']                                        ))


    return df[["tpi", "roc"]]


def get_actual_tracker_class(hxd, curr_val):
    # Adjust tracker class based on insured name
    insured_name = hxd.cds.standard_fields.insured_name
    if insured_name == "AON CLIENT TREATY":     curr_val += " ACT"
    elif insured_name == "MARSH FAST TRACK":    curr_val += " MARSH"
    
    return curr_val


def build_trifocus_summary_pre_pc(hxd, proj_df, model_weights_df, additional_loadings_df):
    # Get the trifocus summary path from HXD
    trifocus_path = hxd.cds.rating_summary.trifocus_summary

    # Define the tracker class mapping
    tracker_classes = {
        "tracker_property": "Tracker Property",
        "tracker_sr":       "Tracker SR",
        "tracker_marine":   "Tracker Marine",
        "tracker_pac":      "Tracker PAC",
        "tracker_cyber":    "Tracker Cyber"    }

    # Loop through each tracker type
    for k, v in tracker_classes.items():
        # Adjust tracker name based on insured name
        v = get_actual_tracker_class(hxd, v)

        if v in proj_df['tracker_class'].values:
            setattr(trifocus_path, f"show_{k}", True)
            tracker_mask = proj_df["tracker_class"] == v

            # Extract relevant series for weighted calculation
            portfolio_percent_series = proj_df.loc[tracker_mask, "portfolio_percent"]
            model_estimate_series = model_weights_df.loc[tracker_mask, "model_estimate"]
            anti_selection_series = additional_loadings_df.loc[tracker_mask, "anti_selection_charge"]
            uncertainty_series = additional_loadings_df.loc[tracker_mask, "uncertainty_charge"]
            additional_series = additional_loadings_df.loc[tracker_mask, "additional_charge"]

            # Calculate total weight for normalization
            total_weight = portfolio_percent_series.sum()
            model_estimate_weighted_sum = (portfolio_percent_series * model_estimate_series).sum()
            anti_selection_weighted_sum = (portfolio_percent_series * anti_selection_series).sum()
            uncertainty_weighted_sum = (portfolio_percent_series * uncertainty_series).sum()
            additional_weighted_sum = (portfolio_percent_series * additional_series).sum()

            # Compute weighted averages, defaulting to 0 if no weight
            if total_weight != 0:
                model_estimate = model_estimate_weighted_sum / total_weight
                anti_selection = anti_selection_weighted_sum / total_weight
                uncertainty = uncertainty_weighted_sum / total_weight
                additional = additional_weighted_sum / total_weight
            else:
                model_estimate = 0
                anti_selection = 0
                uncertainty = 0
                additional = 0

            # Assign computed values to corresponding attributes in trifocus path
            model_estimate_node = getattr(trifocus_path, "model_estimate")
            setattr(model_estimate_node, k, model_estimate)

            anti_selection_node = getattr(trifocus_path, "anti_selection")
            setattr(anti_selection_node, k, anti_selection)

            uncertainty_node = getattr(trifocus_path, "uncertainty")
            setattr(uncertainty_node, k, uncertainty)

            additional_node = getattr(trifocus_path, "additional_charge")
            setattr(additional_node, k, additional)

        else:
            # If tracker class not in project DataFrame, mark as not visible
            setattr(trifocus_path, f"show_{k}", False)


def build_trifocus_summary_post_pc(hxd, proj_df, pricing_adequacy_act_basis_df, pricing_adequacy_final_df, tech_prem_df):
    trifocus_path = hxd.cds.rating_summary.trifocus_summary  # Access the trifocus summary path in HXD

    # Define tracker types with their corresponding labels
    tracker_classes = {
        "tracker_property": "Tracker Property",
        "tracker_sr":       "Tracker SR",
        "tracker_marine":   "Tracker Marine",
        "tracker_pac":      "Tracker PAC",
        "tracker_cyber":    "Tracker Cyber"    }

    # Iterate through each tracker type
    for k, v in tracker_classes.items():
        v = get_actual_tracker_class(hxd, v)  # Resolve actual tracker class
        if v in proj_df['tracker_class'].values:  # Check if tracker exists in projected dataframe

            # Initialize summary metrics
            summary = {
                'be_before_loads': 0,
                'pc_impact': 0,
                'be_after_pc': 0,
                'uw_adj': 0,
                'be_post_uw': 0,
                'bpi': 0,
                'tpi': 0,
                'roc': 0
            }

            tracker_mask = proj_df["tracker_class"] == v  # Boolean mask for the tracker type

            # Extract relevant series for calculations
            portfolio_percent_series = proj_df.loc[tracker_mask, "portfolio_percent"]
            pc_impcat_series         = pricing_adequacy_act_basis_df.loc[tracker_mask, "pc_impact"]
            best_estimate_series     = pricing_adequacy_act_basis_df.loc[tracker_mask, "best_estimate"]
            uw_adj_series            = pricing_adequacy_final_df.loc[tracker_mask, "uw_adj"]
            be_post_uw_series        = pricing_adequacy_final_df.loc[tracker_mask, "best_estimate_gn"]
            roc_series               = pricing_adequacy_final_df.loc[tracker_mask, "roc"]

            total_weight = portfolio_percent_series.sum()  # Total portfolio weight for tracker

            # Compute weighted sums for each metric
            pc_impact_weighted_sum      = (portfolio_percent_series * pc_impcat_series      ).sum()
            best_estimate_weighted_sum  = (portfolio_percent_series * best_estimate_series  ).sum()
            uw_adj_weighted_sum         = (portfolio_percent_series * uw_adj_series         ).sum()
            be_post_uw_weighted_sum     = (portfolio_percent_series * be_post_uw_series     ).sum()
            roc_weighted_sum            = (portfolio_percent_series * roc_series            ).sum()

            # Compute weighted averages if total weight is not zero
            if total_weight != 0:
                summary['pc_impact']    = pc_impact_weighted_sum / total_weight
                summary['be_after_pc']  = best_estimate_weighted_sum / total_weight
                summary['uw_adj']       = uw_adj_weighted_sum / total_weight
                summary['be_post_uw']   = be_post_uw_weighted_sum / total_weight
                summary['roc']          = roc_weighted_sum / total_weight

            gn_prem         = proj_df.loc[tracker_mask, "gn_premium"].sum()  # Gross premium for tracker
            el              = gn_prem * summary['be_post_uw']  # Expected loss
            benchmark_prem  = el / constants.BENCHMARK_LR  # Benchmark premium assuming 70% factor
            tech_prem       = tech_prem_df.loc[tracker_mask, "tp_final"].sum()  # Technical premium
            # Compute ratios safely to avoid division by zero
            summary['bpi']  = gn_prem / benchmark_prem if benchmark_prem != 0 else 0
            summary['tpi']  = gn_prem / tech_prem if tech_prem != 0 else 0

            # Access nodes in HXD trifocus summary for adjustments
            anti_selection_node = getattr(trifocus_path, "anti_selection")
            anti_selection      = getattr(anti_selection_node, k)

            uncertainty_node    = getattr(trifocus_path, "uncertainty")
            uncertainty         = getattr(uncertainty_node, k)

            additional_node     = getattr(trifocus_path, "additional_charge")
            additional          = getattr(additional_node, k)

            # Calculate be_before_loads by removing various charges
            summary['be_before_loads'] = summary['be_after_pc'] - anti_selection - uncertainty - additional

            # Write computed summary metrics back to the HXD trifocus summary
            for field, value in summary.items():
                node = getattr(trifocus_path, field)
                setattr(node, k, value)


def rate_rating_summary_non_bbt(hxd, rater):
    
    # set paths
    rating_summary_path                   = hxd.cds.rating_summary                                  # Root path for rating summary
    pc_path                               = hxd.cds.pc.profit_commission                            # Profit commission path
    pricing_adequacy_path                 = rating_summary_path.pricing_adequacy_metrics            # Pricing adequacy path
    tech_prem_path                        = rating_summary_path.technical_premium_build_up          # Technical premium path
    pricing_adequacy_actuarial_basis_path = pricing_adequacy_path.pricing_adequacy_actuarial_basis
    pricing_adequacy_pre_adj_path         = pricing_adequacy_path.pricing_adequacy_pre_adj
    pricing_adequacy_final_path           = pricing_adequacy_path.pricing_adequacy_final_pricing
    warning_path                          = hxd.non_cds.global_fields                               # Path for own experience weighting warning

    # load premium limit profile df and count unique selected lobs with non-null values
    prem_limit_prof_df = rater["prem_limit_data"]
    no_of_rows = len(prem_limit_prof_df.dropna(subset=["selected_lob"])
                                       .drop_duplicates(subset=["selected_lob"])
                                       .query('selected_lob != "0"')["selected_lob"]
                                       .unique())
    # Exit if no data
    if not no_of_rows:  
        return
    
    # Extract required rater dataframes
    deductions_df        = rater["deductions_df"       ]
    bp_summary_by_lob    = rater["bp_summary_by_lob"]
    own_exp_df           = rater["proj_own_exper_summary"     ]
    proj_lloyds_sum_df   = rater['proj_lloyds_summary' ]
    proj_bzly_sum_df     = rater['proj_beazley_summary']

    # set flags
    is_pc                = hxd.cds.risk_information.is_profit_comission  # Flag for profit commission
    prem_data_available  = hxd.cds.risk_information.prem_data_available  and (rater["policy_data"].shape[0] != 0) # Flag for available premium data

    # validate tpi year
    incept_yr            = hxd.hx_core.inception_date.year
    tpi_year             = hxd.cds.rating_summary.technical_premium_build_up.tpi_year.selected
    validations.check_tpi_year_value(tpi_year)
    tpi_year             = tpi_year or incept_yr


    # Build projected gross/net ultimate loss ratio dataframe
    proj_df = build_projected_gn_ulr_df(
        hxd, 
        rating_summary_path, 
        prem_data_available, 
        prem_limit_prof_df, 
        own_exp_df, 
        bp_summary_by_lob, 
        proj_lloyds_sum_df,
        proj_bzly_sum_df,
        rater)


    build_projected_gn_ulr_summary(proj_df, hxd)  # Summarize projected data

    # Build model weights for each projection
    model_weights_df   = build_model_weights_df(rating_summary_path, proj_df, rater, warning_path)
    model_weights_dict = build_model_weights_summary(model_weights_df, proj_df, rating_summary_path)

    # Build applied charges for anti-selection and uncertainty
    build_anti_selection_applied_charge(hxd,rater)
    build_uncertainty_applied_charge(hxd,rater)

    # Build catastrophe loadings and summaries
    cat_loading_df          = build_cat_loadings(rating_summary_path, prem_data_available, own_exp_df, bp_summary_by_lob, model_weights_df, rater)
    cat_summary_dict        = build_cat_loadings_summary(cat_loading_df, rating_summary_path, proj_df)

    # Build additional loadings
    additional_loadings_df  = build_additional_loadings_df(     rating_summary_path, proj_df, hxd, rater)
    add_load_summary_dict   = build_additional_loadings_summary(rating_summary_path, proj_df, additional_loadings_df)

    # Initialize pricing adequacy dataframes
    pricing_adequacy_act_basis_df = init_pricing_adequacy_act_basis_df( hxd, model_weights_df, cat_loading_df, additional_loadings_df, rater)
    pricing_adequacy_pre_adj_df = init_pricing_adequacy_pre_adj_df(     hxd,    is_pc,  pricing_adequacy_act_basis_df[["best_estimate_pre_pc_adj", "pc_impact"]],        proj_df,        model_weights_df,        cat_loading_df)
    pricing_adequacy_final_df = build_pricing_adequacy_final_df(        pricing_adequacy_final_path.table,        proj_df,        pricing_adequacy_act_basis_df,        deductions_df, rater)

    # Build technical premium dataframe
    tech_prem_df = build_tech_prem_df(        hxd,        proj_df,        pricing_adequacy_pre_adj_df[["best_estimate"]],        pricing_adequacy_act_basis_df[["best_estimate"]],        pricing_adequacy_final_df[["best_estimate_gn"]]    )

    # Build trifocus summary before profit commission adjustments
    build_trifocus_summary_pre_pc(hxd, proj_df, model_weights_df, additional_loadings_df)

    # Build catastrophe ULR summaries
    cat_ulr_summary_df      = build_cat_ulr_summary_df(     rating_summary_path, proj_df, model_weights_df, cat_loading_df, rater)
    cat_ulr_summary_dict    = build_cat_ulr_summary_totals( rating_summary_path, proj_df, cat_ulr_summary_df)

    # Compute TPI and ROC for different stages
    cols_std_tp = [ 'ri_premium', 'inv_income', 'ri_recoveries', 'net_expense', 'target_roc', 'capital_required']
    pricing_adequacy_act_basis_df[["tpi", "roc"]] = calculate_tpi_roc(        pricing_adequacy_act_basis_df[['best_estimate']]
                                                                            , tech_prem_df[['tp_actuarial'] + cols_std_tp]
                                                                            , proj_df[["gn_premium"]]
                                                                            , "act_basis"   , tpi_year)
    
    pricing_adequacy_pre_adj_df[["tpi", "roc"]]   = calculate_tpi_roc(        pricing_adequacy_pre_adj_df[['best_estimate']]
                                                                            , tech_prem_df[['tp_pre_adj'] + cols_std_tp]
                                                                            , proj_df[["gn_premium"]]
                                                                            , "pre_adj"     , tpi_year)
    
    pricing_adequacy_final_df[["tpi", "roc"]]     = calculate_tpi_roc(        pricing_adequacy_final_df[['best_estimate_gn']]
                                                                            , tech_prem_df[['tp_final'] + cols_std_tp]
                                                                            , proj_df[["gn_premium"]]
                                                                            , "final"       , tpi_year)

    # Filter columns for pricing adequacy tables

    cols_pricing_adequacy = [ 'selected_lob', 'best_estimate_pre_pc_adj', 'is_row_visible', 'pc_impact',
                                'best_estimate','bpi',                      'tpi',            'roc'    ]

    # Write pricing adequacy actuarial basis to rater & storing string ref
    pricing_adequacy_act_basis_df   = pricing_adequacy_act_basis_df[cols_pricing_adequacy]
    rater['rat_sum_adeq_act']       = pricing_adequacy_act_basis_df
    path_str                        = hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_actuarial_basis
    path_str.table_str              = pricing_adequacy_pre_adj_df.to_csv(index=False)  # SA: why are these saving csvs?!

    # Write pricing adequacy pre-adjustment to rater & storing string ref
    pricing_adequacy_pre_adj_df     = pricing_adequacy_pre_adj_df[cols_pricing_adequacy]
    rater['rat_sum_adeq_pre']       = pricing_adequacy_pre_adj_df
    path_str                        = hxd.non_cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_pre_adj
    path_str.table_str              = pricing_adequacy_pre_adj_df.to_csv(index=False)

    # Write final pricing adequacy to rater
    rater['rat_sum_adeq_final']     = pricing_adequacy_final_df

    # Write technical premium data to HXD
    rater['rat_sum_tech_prem']     = tech_prem_df

    # Build technical premium summary and overall pricing adequacy summary
    build_tech_prem_build_up_summary(hxd, tech_prem_df)
    build_pricing_adequacy_metrics_summary( hxd, pricing_adequacy_pre_adj_df, pricing_adequacy_act_basis_df,
                                                 pricing_adequacy_final_df,   proj_df                           )

    # Build trifocus summary after profit commission adjustments
    build_trifocus_summary_post_pc(hxd, proj_df, pricing_adequacy_act_basis_df, pricing_adequacy_final_df, tech_prem_df[['tp_final']] )

    # Build trifocus totals
    build_trifocus_summary_totals(hxd)