# v0.5.0
import hx, datetime, numpy as np, pandas as pd
import algorithms.rate_constants as const
from operator import itemgetter
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator, clean_string_columns
# from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me # commented as adjusted in a specific module in the model
from algorithms.model_profiler.profiling_hxd_functions import time_me

from scipy.interpolate import interp1d, PchipInterpolator

from algorithms.model_profiler.profiling_hxd_functions import time_me

from algorithms.steer.rate_steer_exposure_rating_ilf_function import ilfa, ilftab2

from typing import Callable


@time_me
def rate_steer_exposure_curve_descriptions(hxd):
    """Populate Curve Description information from params"""

    ##############################
    ## Initialise variables
    ##############################

    cd_all_curves_df = hx.params.table_curve_desc_all_curves
    cd_commercial_auto_state_df = hx.params.table_curve_desc_commercial_auto_state
    cd_cyber_df = hx.params.table_curve_desc_cyber
    cd_healthcare_df = hx.params.table_curve_desc_healthcare
    cd_private_d_o_df = hx.params.table_curve_desc_private_d_o

    ##############################
    ## Populate all curves
    ##############################
    mapping_params_to_schema_all_curves = {
        'Description':"description", 
        'Parametric':"parametric", 
        'Curve Description':"curve_description", 
        'Source':"source"
    }
    # get output
    all_curves_desc_outputs = list(mapping_params_to_schema_all_curves.values())
    # rename dataframe in line with Data Schema
    cd_all_curves_df = cd_all_curves_df.rename(columns=mapping_params_to_schema_all_curves)
    # clean missing with default value
    cd_all_curves_df[all_curves_desc_outputs] = cd_all_curves_df[all_curves_desc_outputs].fillna("")
    # write to HXD
    hxd.steer.exposure_rating.curve_descriptions.all_curves = cd_all_curves_df.to_dict(orient='records')

    ##############################
    ## Populate Commercial Auto State
    ##############################
    mapping_params_to_schema_com_auto_state = {
        "Group 1": "group_1",
        "Group 2": "group_2",
        "Group 3": "group_3",
        "Group 4": "group_4",
        "Group 5": "group_5",
        "Group 6": "group_6",
        "Group 7": "group_7",
        "Group 8": "group_8"
    }
    # get output
    com_auto_state_desc_outputs = list(mapping_params_to_schema_com_auto_state.values())
    # rename dataframe in line with Data Schema
    cd_commercial_auto_state_df = cd_commercial_auto_state_df.rename(columns=mapping_params_to_schema_com_auto_state)
    # clean missing with default value
    cd_commercial_auto_state_df[com_auto_state_desc_outputs] = cd_commercial_auto_state_df[com_auto_state_desc_outputs].fillna("")
    # write to HXD
    hxd.steer.exposure_rating.curve_descriptions.commercial_auto_state = cd_commercial_auto_state_df.to_dict(orient='records')

    ##############################
    ## Populate Cyber
    ##############################
    mapping_params_to_schema_cyber = {
        "Low": "low",
        "High": "high"
    }
    # get output
    cyber_desc_outputs = list(mapping_params_to_schema_cyber.values())
    # rename dataframe in line with Data Schema
    cd_cyber_df = cd_cyber_df.rename(columns=mapping_params_to_schema_cyber)
    # clean missing with default value
    cd_cyber_df[cyber_desc_outputs] = cd_cyber_df[cyber_desc_outputs].fillna("")
    # write to HXD
    hxd.steer.exposure_rating.curve_descriptions.cyber = cd_cyber_df.to_dict(orient='records')

    ##############################
    ## Populate Healthcare
    ##############################
    mapping_params_to_schema_healthcare = {
        "Low": "low",
        "Medium": "medium",
        "Medium/High": "medium_high",
        "High": "high",
        "Very High": "very_high"
    }
    # get output
    healthcare_desc_outputs = list(mapping_params_to_schema_healthcare.values())
    # rename dataframe in line with Data Schema
    cd_healthcare_df = cd_healthcare_df.rename(columns=mapping_params_to_schema_healthcare)
    # clean missing with default value
    cd_healthcare_df[healthcare_desc_outputs] = cd_healthcare_df[healthcare_desc_outputs].fillna("")
    # write to HXD
    hxd.steer.exposure_rating.curve_descriptions.healthcare = cd_healthcare_df.to_dict(orient='records')

    ##############################
    # Populate Private D&O
    ##############################
    mapping_params_to_schema_private_d_o = {
        "Low": "low",
        "Medium": "medium",
        "High": "high",
        "Very High": "very_high"
    }
    # get output
    private_d_o_desc_outputs = list(mapping_params_to_schema_private_d_o.values())
    # rename dataframe in line with Data Schema
    cd_private_d_o_df = cd_private_d_o_df.rename(columns=mapping_params_to_schema_private_d_o)
    # clean missing with default value
    cd_private_d_o_df[private_d_o_desc_outputs] = cd_private_d_o_df[private_d_o_desc_outputs].fillna("")
    # write to HXD
    hxd.steer.exposure_rating.curve_descriptions.private_d_o = cd_private_d_o_df.to_dict(orient='records')

    return 

@time_me
def rate_steer_exposure_rating_risk_profil_bdx(hxd):

    ##############################
    ## Initialise variables
    ##############################

    cds_layers = hxd.cds.layers
    sc_ccy = hxd.cds.currencies.source_currency
    expo_r = hxd.cds.steer.exposure_rating
    expe_r = hxd.cds.steer.experience_rating
    expe_r_layers = expe_r.layers
    rp_bdx = expo_r.risk_profile_bdx
    rp = expo_r.risk_profile_bdx.risk_profiles

    rp_df = pd_df_from_hx_list(rp)

    # Load and prepare FX data
    fx_df = hx.params.table_currency
    curve_list_df = hx.params.table_ilf_curve_list
    curves_df = hx.params.table_ilf_curve
    cob_df = hx.params.table_cob_code_assumptions
    table_ilf_tabular_df = hx.params.table_ilf_tabular 

    # Create FX to USD DataFrame
    fx_to_usd_df = fx_df.copy()
    fx_to_usd_df["fx_rate_to_usd"] = 0  # Initialise column
    fx_to_usd_df.loc[fx_to_usd_df["fx_rate"] != 0, "fx_rate_to_usd"] = 1 / fx_to_usd_df["fx_rate"]

    # Create FX to Source Currency DataFrame
    fx_to_sc_ccy_df = fx_df.copy()
    factor_to_sc_ccy = fx_df.loc[fx_df["ccy"] == sc_ccy, "fx_rate"].iloc[0]
    fx_to_sc_ccy_df["fx_rate_to_sc_ccy"] = 0  # Initialise column
    fx_to_sc_ccy_df.loc[fx_to_sc_ccy_df["fx_rate"] != 0, "fx_rate_to_sc_ccy"] = factor_to_sc_ccy / fx_to_sc_ccy_df["fx_rate"]


    ##############################
    ## Assign Risk profiles summary nodes: exposure_profile_gross_premium, no_risk, curve 
    ##############################

    # assign currency to source currency
    rp_df["currency"]=sc_ccy

    # Create a dictionary mapping currency to fx_rate_to_usd from fx_to_usd_df
    fx_rate_to_usd_mapping = fx_to_usd_df.set_index("ccy")["fx_rate_to_usd"].to_dict()
    fx_rate_to_sc_ccy_mapping = fx_to_sc_ccy_df.set_index("ccy")["fx_rate_to_sc_ccy"].to_dict()

    # Assign FX rates to rp_df
    rp_df["fx_rate_to_usd"] = rp_df["currency"].map(fx_rate_to_usd_mapping)
    rp_df["fx_rate_to_sc_ccy"] = rp_df["currency"].map(fx_rate_to_sc_ccy_mapping)

    # Calculate and assign summary nodes
    rp_bdx.exposure_profile_gross_premium = (rp_df["net_premium"]).sum()
    rp_bdx.no_of_risk = len(rp_df)

    # Assign curve in display
    unique_curves_list = rp_df["curve"].unique().tolist()
    rp_bdx.curve = unique_curves_list[0] if len(unique_curves_list) == 1 else "Various"

    # Clean string before grouping
    rp_df = clean_string_columns(
            rp_df,
            columns=["linkage", "insured"],
            to_lower=True,
            strip_whitespace=True,
            replace_multiple_spaces=True,
            replace_empty_with="",
            remove_special_chars=False
        )

    # Exposure contribution of each row
    # rp_df["_expo_contribution"] = rp_df["limit"] * rp_df["share"]
    rp_df["_expo_contribution"] = (
        rp_df["limit"] * rp_df["share"]
    ).where(
        ~((rp_df["linkage"] == "") | (rp_df["linkage"].isna())),
        0
    )

    # Exposure = cumulative sum of previous rows with the same insured + linkage
    rp_df["exposure"] = (
        rp_df.groupby(["insured", "linkage"])["_expo_contribution"]
        .cumsum()
        .sub(rp_df["_expo_contribution"])
    )

    # Remove the temporary column
    rp_df.drop(columns="_expo_contribution", inplace=True)

    curve_to_parametric_mapping = curve_list_df.set_index("Description")["Parametric"].to_dict()
    rp_df["parametric"] = rp_df["curve"].map(curve_to_parametric_mapping)

    # Define the columns to map from curves_df to rp_df
    columns_to_map = {
        "curve_type": "Curve Type",
        "first_loss": "FirstLoss_Ind",
        "param_1": "P1",
        "param_2": "P2",
        "param_3": "P3",
        "param_4": "P4"
    }

    # Create mapping dictionaries for each column
    mapping_dicts = {
        new_col: curves_df.set_index("Description")[src_col].to_dict()
        for new_col, src_col in columns_to_map.items()
    }
    
    # Capitalize the first letter of each value in the dictionary
    mapping_dicts["first_loss"] = {
        key: value.capitalize() if isinstance(value, str) else value
        for key, value in mapping_dicts["first_loss"].items()
    }

    # Populate rp_df with mapped values, filling missing values with an empty string
    for new_col, mapping in mapping_dicts.items():
        rp_df[new_col] = rp_df["curve"].map(mapping)

    # Calculate the sum of limit and excess
    rp_df["limit_plus_excess"] = rp_df["limit"] + rp_df["excess"]

    # Define the conditions and corresponding values for "first_loss_factor"
    conditions = [
        (rp_df["first_loss"] == "False"),
        (rp_df["first_loss"] != "False") & (rp_df["limit_plus_excess"] != 0)
    ]

    calculations = [
        1,
        1 / rp_df["limit_plus_excess"]
    ]

    # Use numpy.select to apply the conditions and choices
    rp_df["first_loss_factor"] = np.select(conditions, calculations, default=0)

    # Drop the temporary column 
    rp_df.drop(columns=["limit_plus_excess"], inplace=True)

    # get max limit for tabular ILF in USD
    max_limit = table_ilf_tabular_df["LimitLow"].max()

    ##############################
    ## Build error message
    ##############################

    bdx_error_message = ""
    # Find rows where 'limit' exceeds max_limit
    exceeding_rows = rp_df[(rp_df['limit']*rp_df['fx_rate_to_usd'] > max_limit) & (rp_df['parametric'] == "No")]

    # Print a message for each row where limit in usd exceeds max limit in USD
    over_limit_list = []
    is_bdx_input_issue=False
    for index, row in exceeding_rows.iterrows():
        over_limit_list.append(f"{index+1}")
    if len(over_limit_list)!=0:
        is_bdx_input_issue=True
        bdx_error_message = bdx_error_message + (f" Limit entered exceeding the tabular ILF max limit USD {int(max_limit):,} in row(s): {', '.join(over_limit_list)}\n")
    
    limit_issues_list = []
    # Find rows where 'limit' are negative
    limit_issues_rows = rp_df[( rp_df['limit'] <=0 )]
    for index, row in limit_issues_rows.iterrows():
        limit_issues_list.append(f"{index+1}")
    if len(limit_issues_list)!=0:
        is_bdx_input_issue=True
        bdx_error_message = bdx_error_message + (f" * Limit entered cannot be negative or 0. Please review limit of the following row(s): {', '.join(limit_issues_list)}\n")
    
    missing_curve_list = []
    # Find rows where 'curve' are missing
    missing_curve_rows = rp_df[(rp_df['curve'].isna()) | (rp_df['curve']==None)]
    for index, row in missing_curve_rows.iterrows():
        missing_curve_list.append(f"{index+1}")
    if len(missing_curve_list)!=0:
        is_bdx_input_issue=True
        bdx_error_message = bdx_error_message + (f" * Missing Curve. Please review curve of the following row(s): {', '.join(missing_curve_list)}\n")
    
    missing_cob_list = []
    # Find rows where 'cob' are missing
    missing_cob_rows = rp_df[(rp_df['cob'].isna()) | (rp_df['cob']==None)]
    for index, row in missing_cob_rows.iterrows():
        missing_cob_list.append(f"{index+1}")
    if len(missing_cob_list)!=0:
        is_bdx_input_issue=True
        bdx_error_message = bdx_error_message + (f" * Missing COB. Please review COB of the following row(s): {', '.join(missing_cob_list)}\n")
    
    rp_bdx.message = bdx_error_message
    # define str outputs
    rp_outputs_str = [
        "currency", # str
        "parametric", # str
        "fx_rate_to_usd", #str
        "curve_type", #str
        "first_loss", #str
    ]

    # define numeric output
    rp_outputs_flt = [
        "first_loss_factor", # float
        "param_1",# float
        "param_2",# float
        "param_3",# float
        "param_4",# float
        "exposure",# float,
    ]
    
    layer_rp_outputs = [
            "expo_pct",
            "expo_premium",
            "excess",
            "sum_insured",
            "ilf_xs_and_xm",
            "ilf_xs_and_xl",
            "ilf_xs_and_lmt",
            "ilf_xs",
            "pr_pct",
            "pr_net_premium"
        ]  

        # assign limit and excess for display
    for layer_num in range(len(cds_layers)):

        layer_name = f"layer_{layer_num+1:02d}"

        ##############################
        ## Assign Pure Rate summany per layer
        ##############################

        layer_limit = cds_layers[layer_num].limit or 0

        ##############################
        ## Assign Risk profiles layer nodes
        ##############################

        # assign excess
        rp_layer_excess = layer_name+"/excess"
        rp_df[rp_layer_excess] = cds_layers[layer_num].excess

        # assign sum insured
        rp_layer_sum_insured = layer_name+"/sum_insured"
        rp_df[rp_layer_sum_insured] = np.minimum(
            rp_df[rp_layer_excess] + layer_limit,
            rp_df["exposure"] + rp_df["share"] * rp_df["limit"]
        )

        # Assign pr_pct
        rp_layer_pr_pct = f"{layer_name}/pr_pct"
        rp_df[rp_layer_pr_pct] = 0  # Initialise column

        # Create masks
        zero_limit_mask = rp_df["limit"] == 0
        zero_share_mask = rp_df["share"] == 0
        denominator = rp_df["share"] * rp_df["limit"]
        zero_denominator_mask = denominator == 0

        # Valid mask: limit != 0, share != 0, and denominator != 0
        valid_mask = ~zero_limit_mask & ~zero_share_mask & ~zero_denominator_mask

        # Debug prints (optional)
        # print("Zero values in denominator:", zero_denominator_mask.sum())
        # print("Indices with zero denominator:", rp_df.index[zero_denominator_mask])

        # Apply logic using masks
        rp_df.loc[valid_mask, rp_layer_pr_pct] = np.maximum(
            0,
            (rp_df[rp_layer_sum_insured] - rp_df[rp_layer_excess]) / denominator[valid_mask]
        )

        # Assign pr_net_premium
        rp_layer_pr_net_premium = f"{layer_name}/pr_net_premium"
        rp_df[rp_layer_pr_net_premium] = 0  # Initialise column

        # Create mask for non-zero pr_pct
        non_zero_pr_pct_mask = rp_df[rp_layer_pr_pct] != 0

        # Apply logic using mask
        rp_df.loc[non_zero_pr_pct_mask, rp_layer_pr_net_premium] = (
            rp_df[rp_layer_pr_pct] * rp_df["net_premium"]
        )

        def calculate_ilf(
            rp_df: pd.DataFrame,
            layer_name: str,
            rp_layer_excess: str,
            rp_layer_sum_insured: str,
            ilf_column: str,
            ilfa_func: Callable,
            ilftab2_func: Callable,
            ilf_table: pd.DataFrame,
            x_calculation_func_parametric: Callable,
            x_calculation_func_tabular: Callable,
        ) -> pd.DataFrame:
            """
            Calculate ILF values for parametric and tabular curves.

            Args:
                rp_df: DataFrame containing the input data.
                layer_name: Name of the layer.
                rp_layer_excess: Column name for risk excess.
                rp_layer_sum_insured: Column name for sum insured.
                ilf_column: Column name for ILF results (e.g., "ilf_xs_and_xm").
                ilfa_func: Function to calculate ILF for parametric curves.
                ilftab2_func: Function to calculate ILF for tabular curves.
                ilf_table: DataFrame containing the ILF table for tabular curves.
                x_calculation_func_parametric: Function to calculate the input value for parametric ILF functions.
                    Signature: x_calculation_func_parametric(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series
                x_calculation_func_tabular: Function to calculate the input value for tabular ILF functions.
                    Signature: x_calculation_func_tabular(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series

            Returns:
                Updated DataFrame with ILF values in the specified column.
            """
            rp_layer_ilf = f"{layer_name}/{ilf_column}"

            # Initialise or reset the ILF column
            rp_df[rp_layer_ilf] = 0

            # Only proceed if curve is not empty
            curve_mask = rp_df["curve"] != ""
            if not curve_mask.any():
                return rp_df

            # Create a mask for rows where share is 0
            zero_share_mask = rp_df["share"] == 0

            # Initialise the result Series
            x = rp_df[rp_layer_excess].copy()

            # Apply the mask: where share is 0, set to 0.01
            x[zero_share_mask] = 0.01

            # Split by parametric/tabular
            parametric_mask = (rp_df["parametric"] == "Yes") & curve_mask
            tabular_mask = (rp_df["parametric"] == "No") & curve_mask

            if parametric_mask.any():
                parametric_non_zero_share_mask = parametric_mask & (~zero_share_mask)

                if parametric_non_zero_share_mask.any():
                    x.loc[parametric_non_zero_share_mask] = x_calculation_func_parametric(rp_df, parametric_non_zero_share_mask)

                    valid_indices = parametric_mask[parametric_non_zero_share_mask].index

                    # Compute ILFA for the valid subset
                    ilfa_values = ilfa_func(
                        x=x.loc[parametric_non_zero_share_mask],
                        c_type=rp_df.loc[valid_indices, "curve_type"],
                        p1=rp_df.loc[valid_indices, "param_1"],
                        p2=rp_df.loc[valid_indices, "param_2"],
                        p3=rp_df.loc[valid_indices, "param_3"],
                        p4=rp_df.loc[valid_indices, "param_4"],
                    )

                    # Assign the computed ILFA values
                    rp_df.loc[valid_indices, rp_layer_ilf] = ilfa_values

            if tabular_mask.any():
                tabular_non_zero_share_mask = tabular_mask & (~zero_share_mask)

                if tabular_non_zero_share_mask.any():
                    x.loc[tabular_non_zero_share_mask] = x_calculation_func_tabular(rp_df, tabular_non_zero_share_mask)

                    valid_indices = tabular_mask[tabular_mask].index

                    # Compute ILF for tabular curves
                    ilf_values = ilftab2_func(
                        x=x.loc[tabular_non_zero_share_mask],
                        curve=rp_df.loc[tabular_non_zero_share_mask, "curve"],
                        ilf_table=ilf_table,
                    )

                    # Assign the computed ILF values
                    rp_df.loc[valid_indices, rp_layer_ilf] = ilf_values

            return rp_df

        def x_calculation_parametric_xs_xm(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            # return (
            #     (rp_df["excess"][mask] +
            #     (rp_df[rp_layer_sum_insured][mask] - rp_df["exposure"][mask]) /
            #     rp_df["share"][mask]) *
            #     rp_df["fx_rate_to_usd"][mask] *
            #     rp_df["first_loss_factor"][mask]
            # )
            return (
                (rp_df["excess"][mask] +
                (np.maximum(rp_df[rp_layer_sum_insured][mask], rp_df["exposure"][mask]) - rp_df["exposure"][mask]) /
                rp_df["share"][mask]) *
                rp_df["fx_rate_to_usd"][mask] *
                rp_df["first_loss_factor"][mask]
            )

        def x_calculation_tabular_xs_xm(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            # as per DEV v0.29
            # return (
            #     (rp_df["excess"][mask] +
            #     (rp_df[rp_layer_sum_insured][mask] - rp_df["exposure"][mask]) /
            #     rp_df["share"][mask]) *
            #     rp_df["fx_rate_to_usd"][mask]
            # )
            return (
                (rp_df["excess"][mask] +
                (np.maximum(rp_df[rp_layer_sum_insured][mask], rp_df["exposure"][mask]) - rp_df["exposure"][mask]) /
                rp_df["share"][mask]) *
                rp_df["fx_rate_to_usd"][mask]
            )

        def x_calculation_parametric_xs_xl(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                (rp_df["excess"][mask] +
                (np.maximum(rp_df[rp_layer_excess][mask], rp_df["exposure"][mask]) - rp_df["exposure"][mask]) /
                rp_df["share"][mask]) *
                rp_df["fx_rate_to_usd"][mask] *
                rp_df["first_loss_factor"][mask]
            )

        def x_calculation_tabular_xs_xl(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                (rp_df["excess"][mask] +
                (np.maximum(rp_df[rp_layer_excess][mask], rp_df["exposure"][mask]) - rp_df["exposure"][mask]) /
                rp_df["share"][mask]) *
                rp_df["fx_rate_to_usd"][mask]
            )

        def x_calculation_parametric_xs(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                rp_df["excess"][mask] *
                rp_df["fx_rate_to_usd"][mask] *
                rp_df["first_loss_factor"][mask]
            )

        def x_calculation_tabular_xs(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                (rp_df["excess"][mask]) *
                rp_df["fx_rate_to_usd"][mask]
            )
        
        def x_calculation_parametric_xs_lmt(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                (rp_df["excess"][mask] + rp_df["limit"][mask]) *
                rp_df["fx_rate_to_usd"][mask] *
                rp_df["first_loss_factor"][mask]
            )

        def x_calculation_tabular_xs_lmt(rp_df: pd.DataFrame, mask: pd.Series) -> pd.Series:
            return (
                (rp_df["excess"][mask] + rp_df["limit"][mask]) *
                rp_df["fx_rate_to_usd"][mask]
            )

        rp_df = calculate_ilf(
            rp_df=rp_df,
            layer_name=layer_name,
            rp_layer_excess=f"{layer_name}/excess",
            rp_layer_sum_insured="sum_insured",
            ilf_column="ilf_xs_and_xm",
            ilfa_func=ilfa,
            ilftab2_func=ilftab2,
            ilf_table=hx.params.table_ilf_tabular,
            x_calculation_func_parametric=x_calculation_parametric_xs_xm,
            x_calculation_func_tabular=x_calculation_tabular_xs_xm,
        )

        rp_df = calculate_ilf(
            rp_df=rp_df,
            layer_name=layer_name,
            rp_layer_excess=f"{layer_name}/excess",
            rp_layer_sum_insured="sum_insured",
            ilf_column="ilf_xs_and_xl",
            ilfa_func=ilfa,
            ilftab2_func=ilftab2,
            ilf_table=hx.params.table_ilf_tabular,
            x_calculation_func_parametric=x_calculation_parametric_xs_xl,
            x_calculation_func_tabular=x_calculation_tabular_xs_xl,
        )

        rp_df = calculate_ilf(
            rp_df=rp_df,
            layer_name=layer_name,
            rp_layer_excess=f"{layer_name}/excess",
            rp_layer_sum_insured="sum_insured",
            ilf_column="ilf_xs",
            ilfa_func=ilfa,
            ilftab2_func=ilftab2,
            ilf_table=hx.params.table_ilf_tabular,
            x_calculation_func_parametric=x_calculation_parametric_xs,
            x_calculation_func_tabular=x_calculation_tabular_xs,
        )

        rp_df = calculate_ilf(
            rp_df=rp_df,
            layer_name=layer_name,
            rp_layer_excess=f"{layer_name}/excess",
            rp_layer_sum_insured="sum_insured",
            ilf_column="ilf_xs_and_lmt",
            ilfa_func=ilfa,
            ilftab2_func=ilftab2,
            ilf_table=hx.params.table_ilf_tabular,
            x_calculation_func_parametric=x_calculation_parametric_xs_lmt,
            x_calculation_func_tabular=x_calculation_tabular_xs_lmt,
        )

        rp_layer_ilf_xs_and_xm = f"{layer_name}/ilf_xs_and_xm"
        rp_layer_ilf_xs_and_xl = f"{layer_name}/ilf_xs_and_xl"
        rp_layer_ilf_xs_and_lmt = f"{layer_name}/ilf_xs_and_lmt"
        rp_layer_ilf_xs = f"{layer_name}/ilf_xs"

        # Assign layer_expo_pct
        rp_layer_expo_pct = f"{layer_name}/expo_pct"
        rp_df[rp_layer_expo_pct] = 0  # Initialise column

        # Create masks
        zero_net_prem_mask = rp_df["net_premium"] == 0
        si_smaller_pol_excess_mask = rp_df[rp_layer_sum_insured] <= rp_df[rp_layer_excess]
        denominator_expo = rp_df[rp_layer_ilf_xs_and_lmt] - rp_df[rp_layer_ilf_xs]
        zero_denominator_expo_mask = denominator_expo == 0

        # Valid mask: limit != 0, share != 0, and denominator != 0
        valid_expo_mask = ~zero_net_prem_mask & ~si_smaller_pol_excess_mask & ~zero_denominator_expo_mask
        # valid_expo_mask = ~zero_net_prem_mask | ~si_smaller_pol_excess_mask | ~zero_denominator_expo_mask

        # Define the columns to check for equality
        cols = [
            rp_layer_ilf_xs_and_xm,
            rp_layer_ilf_xs_and_xl,
            rp_layer_ilf_xs_and_lmt,
            rp_layer_ilf_xs
        ]

        # Create a mask where all specified columns have the same value
        all_equal_mask = (rp_df[cols[0]] == rp_df[cols[1]]) & \
                        (rp_df[cols[1]] == rp_df[cols[2]]) & \
                        (rp_df[cols[2]] == rp_df[cols[3]])

        # Assign 1 where all columns are equal and the valid mask is True
        rp_df.loc[zero_denominator_expo_mask & all_equal_mask, rp_layer_expo_pct] = 1
        rp_df.loc[zero_denominator_expo_mask & ~all_equal_mask, rp_layer_expo_pct] = 0
        
        # Assign 0 where SI < Excess and net prem equal zero
        rp_df.loc[zero_net_prem_mask | si_smaller_pol_excess_mask, rp_layer_expo_pct] = 0

        # # Apply logic using masks
        rp_df.loc[valid_expo_mask, rp_layer_expo_pct] = (rp_df[rp_layer_ilf_xs_and_xm] - rp_df[rp_layer_ilf_xs_and_xl]) / denominator_expo[valid_mask]

        # Assign layer_expo_pct
        rp_layer_expo_premium = f"{layer_name}/expo_premium"
        rp_df[rp_layer_expo_premium] = 0  # Initialise column

        # Create mask for non-zero pr_pct
        non_zero_expo_pct_mask = rp_df[rp_layer_expo_pct] != 0

        # Apply logic using mask
        rp_df.loc[non_zero_expo_pct_mask, rp_layer_expo_premium] = (rp_df[rp_layer_expo_pct] * rp_df["net_premium"])

        ##############################
        ## Assign Summary field per layer
        ##############################

        risk_bdx_summary = cds_layers[layer_num].risk_profile_bdx

        exposure_lr = (
            rp_bdx.exposure_lr
            if risk_bdx_summary.glr_pick == "Cedant LR"
            else (getattr(expe_r.layers,layer_name).selected_years_wa.ulr or 0)
        )
        risk_bdx_summary.exposure_lr = exposure_lr or 0

        # risk_bdx_summary.pro_rata_premium = rp_df[rp_layer_pr_net_premium].sum() or 0
        # risk_bdx_summary.exposure_premium = rbdx_expo_prem = max(0,rp_df[rp_layer_expo_premium].sum() or 0)

        if cds_layers[layer_num].limit ==1 and cds_layers[layer_num].excess ==0:
            risk_bdx_summary.pro_rata_premium =  0
            risk_bdx_summary.exposure_premium = rbdx_expo_prem = 0
        else:
            risk_bdx_summary.pro_rata_premium = rp_df[rp_layer_pr_net_premium].sum() or 0
            risk_bdx_summary.exposure_premium = rbdx_expo_prem = max(0,rp_df[rp_layer_expo_premium].sum() or 0)
        


        # Calculate layer_el_at_loss_ratio (faster, reusing exposure_lr)
        layer_el_at_loss_ratio = rbdx_expo_prem * exposure_lr

        risk_bdx_summary.el_at_loss_ratio = layer_el_at_loss_ratio
        
        bdx_epi = getattr(rp_bdx,"exposure_profile_gross_premium")
        
        if bdx_epi == 0:
            risk_bdx_summary.rate_on_npi = 0 
            risk_bdx_summary.loss_premium = 0 
            risk_bdx_summary.pure_rate = 0
        else:
            risk_bdx_summary.rate_on_npi = layer_el_at_loss_ratio / bdx_epi 
            risk_bdx_summary.loss_premium = layer_el_at_loss_ratio / bdx_epi * (cds_layers[layer_num].epi_100 or 0)
            risk_bdx_summary.pure_rate = layer_el_at_loss_ratio / bdx_epi 
        
        # adding layer nodes to the rp_outputs_flt list
        for item in layer_rp_outputs:
            rp_outputs_flt.append(f"{layer_name}/{item}")

    # clean data before writing it hxd
    rp_df[rp_outputs_str ] = rp_df[rp_outputs_str ].fillna('')
    rp_df[rp_outputs_flt ] = rp_df[rp_outputs_flt ].fillna(0)

    # Combine output lists
    rp_outputs = rp_outputs_flt + rp_outputs_str

    # Assign bdx_limit_exceeding_message
    hxd.model_state.is_bdx_input_issue = is_bdx_input_issue

    # write to HXD
    write_pd_to_hxd(rp_df, rp,  rp_outputs )

    return

@time_me
def rate_steer_exposure_rating_las_bdx(hxd):
    ##############################
    ## Initialise variables
    ##############################
    cds_layers = hxd.cds.layers
    
    expo_r = hxd.cds.steer.exposure_rating
    rp_bdx = expo_r.risk_profile_bdx
    rp = rp_bdx.risk_profiles
    # total_las = rp_bdx.total_las
    pc = hxd.cds.steer.experience_rating.processed_claims
    las_layers = hxd.cds.steer.exposure_rating.limit_average_severity.layers
    
    
    # check is there is any risk profiles
    if len(rp)==0:
        return # Exit function
    # Check if claims have been processed
    if len(pc)==0:
        return # Exit function

    rp_df = pd_df_from_hx_list(rp)
    pc_df = pd_df_from_hx_list(pc)
    
    ##############################
    # calculate FGU LAS
    ##############################

    # get the unique list of Limit from Risk Profiles Bdx
    las_fgu_rp_df = pd.DataFrame()

    ##############################
    # Write information box for LAS limitation
    ##############################
    

    if len(rp_df["limit"].dropna().unique()) > const.las_limit_number:
        # Assign bdx_limit_exceeding_message
        hxd.model_state.is_bdx_input_issue = True
        current_bdx_message = rp_bdx.message
        current_bdx_message = current_bdx_message + "Limit Average Severity - the LAS method only applies the 30 lowest limit from Risk bdx!"
        rp_bdx.message = current_bdx_message

    # las_fgu_rp_df["upper"] = sorted(rp_df["limit"].dropna().unique())
    las_fgu_rp_df["upper"] = sorted(rp_df["limit"].dropna().unique())[:const.las_limit_number]
    las_fgu_rp_df["lower"] = las_fgu_rp_df["upper"].shift(1) + 1
    las_fgu_rp_df["lower"] = las_fgu_rp_df["lower"].fillna(0)

    
    
    def calculate_bin_stats(row, pc_df):
        """Calculate sum of losses, count of occurrences, and average for a given row/bin."""
        lower, upper = row["lower"], row["upper"]
        mask = (pc_df["trended_claim"] > lower) & (pc_df["trended_claim"] <= upper)
        bin_values = pc_df.loc[mask, "trended_claim"]
        losses = bin_values.sum()
        occurrences = (bin_values > 0).sum()
        average = losses / occurrences if occurrences > 0 else 0
        return losses, occurrences, average

    # Apply the calculation to each row in rp_df
    results = las_fgu_rp_df.apply(
        lambda row: calculate_bin_stats(row, pc_df),
        axis=1,
        result_type="expand"  # Returns a DataFrame with three columns
    )

    # Assign results to the appropriate columns
    las_fgu_rp_df[["losses", "occurrences", "average"]] = results

    # calculate Total
    total_las_fgu_losses = las_fgu_rp_df["losses"].sum()
    total_las_fgu_occurrences = las_fgu_rp_df["occurrences"].sum()
    total_las_fgu_average = (total_las_fgu_losses / total_las_fgu_occurrences) if total_las_fgu_occurrences != 0 else 0.0

    hxd.cds.steer.exposure_rating.limit_average_severity.layers.fgu.total.losses = total_las_fgu_losses
    hxd.cds.steer.exposure_rating.limit_average_severity.layers.fgu.total.occurrences = total_las_fgu_occurrences
    hxd.cds.steer.exposure_rating.limit_average_severity.layers.fgu.total.average = total_las_fgu_average


    # Initialise value
    las_fgu_rp_df["las"] = 0

    mask_upper_zero = las_fgu_rp_df["upper"] == 0
    mask_upper_non_zero = ~mask_upper_zero

    if total_las_fgu_average != 0 and total_las_fgu_occurrences != 0:
        # Create a subset for non-zero upper values
        las_fgu_rp_df_upper_non_zero = las_fgu_rp_df.loc[mask_upper_non_zero].copy()

        # Calculate current occurrence losses (cumulative sum)
        current_occurrence_losses = las_fgu_rp_df_upper_non_zero["losses"].cumsum()

        future_occurrence_losses = las_fgu_rp_df_upper_non_zero["upper"] * las_fgu_rp_df_upper_non_zero["occurrences"][::-1].cumsum()[::-1].shift(-1)
        # Calculate LAS for non-zero upper rows
        las_fgu_rp_df_upper_non_zero["las"] = (current_occurrence_losses + future_occurrence_losses.fillna(0) )/ total_las_fgu_occurrences

        # Update the original DataFrame with the calculated values
        las_fgu_rp_df.loc[mask_upper_non_zero, "las"] = las_fgu_rp_df_upper_non_zero["las"]
    
    # initialise value
    las_fgu_rp_df["ilf_empirical"] = 0

    # Calculate ILF empirical only if the first value of LAS is not zero
    first_las_value = las_fgu_rp_df["las"].iat[0]
    if first_las_value != 0:
        # Set to 0 where LAS is 0, otherwise divide by the first LAS value
        las_fgu_rp_df["ilf_empirical"] = np.where(
            las_fgu_rp_df["las"] == 0,
            0,
            las_fgu_rp_df["las"] / first_las_value
        )
    
    
    if len(las_fgu_rp_df) < const.las_limit_number:
        missing_rows = const.las_limit_number - len(las_fgu_rp_df)
        new_rows = pd.DataFrame(0, index=range(missing_rows), columns=las_fgu_rp_df.columns)
        las_fgu_rp_df = pd.concat([las_fgu_rp_df, new_rows], ignore_index=True)

    ##############################
    ## Calculate Layer LAS
    ##############################

    rp_layer_las_cy_outputs =[
        "lower",
        "upper",
        "ilf_selected",
        "pct_of_claims_to_layer",
        "premium",
        "loss_to_layer",
    ]
    # get upper columns
    las_limit_rp_df = pd.DataFrame()
    las_limit_rp_df["upper"] = las_fgu_rp_df[["upper"]].copy()
    las_limit_rp_df["lower"] = las_fgu_rp_df[["lower"]].copy()

    for layer_index in range(len(cds_layers)):
        layer_name = f"layer_{layer_index+1:02d}"

        # rp_bdx_layer = getattr(rp_bdx.layers,f"{layer_name}")    
        layer_limit = cds_layers[layer_index].limit

        ##############################
        ## Calculate Layer LAS current Year
        ##############################

        las_rp_df = pd_df_from_hx_list(getattr(expo_r.limit_average_severity.layers,layer_name).risk_profiles)
        
        las_all_rp_df = las_fgu_rp_df.copy()

        prefix_cy = f"{layer_name}/risk_profiles/current_year/"


        # Define the items we need to create variables for
        items = [
            "lower",
            "upper",
            "ilf_user_input",
            "ilf_selected",
            "pct_of_claims_to_layer",
            "premium",
            "loss_to_layer"
        ]

        # Create variables directly without dictionary
        las_layer_cy_lower = f"{prefix_cy}lower"
        las_layer_cy_upper = f"{prefix_cy}upper"
        las_layer_cy_ilf_user_input = f"{prefix_cy}ilf_user_input"
        las_layer_cy_ilf_selected = f"{prefix_cy}ilf_selected"
        las_layer_cy_pct_of_claims_to_layer = f"{prefix_cy}pct_of_claims_to_layer"
        las_layer_cy_premium = f"{prefix_cy}premium"
        las_layer_cy_loss_to_layer = f"{prefix_cy}loss_to_layer"

        las_all_rp_df[las_layer_cy_lower] = las_limit_rp_df['lower']
        las_all_rp_df[las_layer_cy_upper] = las_limit_rp_df['upper']
        las_all_rp_df[las_layer_cy_ilf_user_input] = las_rp_df['current_year/ilf_user_input']
        # las_all_rp_df[las_layer_cy_ilf_user_input] = las_rp_df['current_year/ilf_user_input']

        las_all_rp_df[las_layer_cy_ilf_selected] = np.where(
            las_all_rp_df[las_layer_cy_ilf_user_input]!=0,
            las_all_rp_df[las_layer_cy_ilf_user_input],
            las_all_rp_df["ilf_empirical"])


        layer_xs = cds_layers[layer_index].excess or 0
        layer_xs_and_xl = layer_xs + (cds_layers[layer_index].limit or 0)

        
        def get_interpolated_ilf(rp_df, layer_tower, las_layer_cy_lower, las_layer_cy_upper, las_layer_cy_ilf_selected):
            """
            Find the interval containing layer_tower and interpolate the ilf_selected value.

            Args:
                rp_df: DataFrame containing the layer information
                layer_tower: The excess value to find the interval for
                las_layer_cy_lower: path to lower limit
                las_layer_cy_upper: path to higher limit
                las_layer_cy_ilf_selected: path to ilf selected
            Returns:
                The interpolated ilf_selected value for layer_tower
            """
            # Find the row where las_layer_cy_lower <= layer_tower <= las_layer_cy_upper
            mask = (rp_df[las_layer_cy_lower] <= layer_tower) & (rp_df[las_layer_cy_upper] >= layer_tower)
            row = rp_df[mask]

            if row.empty:
                # raise ValueError(f"No interval found containing layer_tower = {layer_tower}")
                return 1

            # Get the lower and upper values
            las_layer_cy_lower_value = row[las_layer_cy_lower].values[0]
            las_layer_cy_upper_value = row[las_layer_cy_upper].values[0]

            # Get the ilf_selected values for the lower and upper bounds
            
            ilf_candidates_lower = rp_df.loc[
                (rp_df[las_layer_cy_lower] <= las_layer_cy_lower_value)
                & (rp_df[las_layer_cy_upper] != 0),
                las_layer_cy_ilf_selected,
            ]
            
            if not ilf_candidates_lower.empty:
                ilf_lower = ilf_candidates_lower.iloc[-1]
            else:
                ilf_lower = row[las_layer_cy_ilf_selected].values[0]
                            
            ilf_candidates_upper = rp_df.loc[
                (rp_df[las_layer_cy_lower] <= las_layer_cy_upper_value)
                & (rp_df[las_layer_cy_upper] != 0),
                las_layer_cy_ilf_selected,
            ]

            if not ilf_candidates_upper.empty:
                ilf_upper = ilf_candidates_upper.iloc[-1]
            else:
                ilf_upper = row[las_layer_cy_ilf_selected].values[0]

            # Linear interpolation
            if las_layer_cy_upper_value == las_layer_cy_lower_value:
                # Avoid division by zero if bounds are equal
                return ilf_lower

            # Calculate the interpolation weight
            weight = (layer_tower - las_layer_cy_lower_value) / (las_layer_cy_upper_value - las_layer_cy_lower_value)

            # Interpolate between the two ilf_selected values
            interpolated_ilf = ilf_lower + weight * (ilf_upper - ilf_lower)

            return interpolated_ilf
        
        ilf_layer_xs = get_interpolated_ilf(las_all_rp_df, layer_xs, las_layer_cy_lower, las_layer_cy_upper, las_layer_cy_ilf_selected)
        ilf_layer_xs_and_xl = get_interpolated_ilf(las_all_rp_df, layer_xs_and_xl, las_layer_cy_lower, las_layer_cy_upper, las_layer_cy_ilf_selected)

        # Initialise the column
        las_all_rp_df[las_layer_cy_pct_of_claims_to_layer] = 0

        # Create masks
        mask_default = (
            (las_all_rp_df[las_layer_cy_upper] < layer_xs) |
            (las_all_rp_df[las_layer_cy_upper] == 0) |
            (las_all_rp_df[las_layer_cy_ilf_selected] == 0)
        )

        mask_tower_above_upper = (layer_xs_and_xl >= las_all_rp_df[las_layer_cy_upper]) & ~mask_default
        mask_tower_below_upper = (layer_xs_and_xl < las_all_rp_df[las_layer_cy_upper]) & ~mask_default

        # Apply calculations directly to the original DataFrame
        las_all_rp_df.loc[mask_tower_below_upper, las_layer_cy_pct_of_claims_to_layer] = (
            (ilf_layer_xs_and_xl - ilf_layer_xs) / las_all_rp_df.loc[mask_tower_below_upper, las_layer_cy_ilf_selected]
        )

        las_all_rp_df.loc[mask_tower_above_upper, las_layer_cy_pct_of_claims_to_layer] = (
            (las_all_rp_df.loc[mask_tower_above_upper, las_layer_cy_ilf_selected] - ilf_layer_xs) /
            las_all_rp_df.loc[mask_tower_above_upper, las_layer_cy_ilf_selected]
        )


        # Calculate cumulative sum where limit <= las_layer_cy_upper for each row
        las_all_rp_df["net_premium_cumsum"] = las_all_rp_df[las_layer_cy_upper].apply(
            lambda upper: rp_df.loc[rp_df["limit"] <= upper, "net_premium"].sum()
        )

        # Then calculate net_premium_sum where each row deducts the previous row's value
        las_all_rp_df[las_layer_cy_premium] = (las_all_rp_df["net_premium_cumsum"] - las_all_rp_df["net_premium_cumsum"].shift(1).fillna(0)).clip(lower=0)

        las_all_rp_df[las_layer_cy_loss_to_layer] = 0

        las_all_rp_df[las_layer_cy_loss_to_layer] = las_all_rp_df[las_layer_cy_premium]  * las_all_rp_df[las_layer_cy_pct_of_claims_to_layer] 

        # ##### 
        # calculate Layer LAS Movements
        # #####
        mvt_items = [
            "pct_of_claims_to_layer",
            "premium",
            "loss_to_layer"
        ]
        
        prefix_mvt = f"{layer_name}/risk_profiles/movement/"

    
        las_layer_mvt_pct_of_claims_to_layer = f"{prefix_mvt}pct_of_claims_to_layer"
        las_layer_mvt_premium = f"{prefix_mvt}premium"
        las_layer_mvt_loss_to_layer = f"{prefix_mvt}loss_to_layer"

        prefix_prev = f"{layer_name}/risk_profiles/previous_year/"

        las_layer_prev_pct_of_claims_to_layer = f"{prefix_prev}pct_of_claims_to_layer"
        las_layer_prev_premium = f"{prefix_prev}premium"
        las_layer_prev_loss_to_layer = f"{prefix_prev}loss_to_layer"

        las_all_rp_df[las_layer_prev_pct_of_claims_to_layer]=0 # set by default to 0
        las_all_rp_df[las_layer_prev_premium]=0 # set by default to 0
        las_all_rp_df[las_layer_prev_loss_to_layer]=0 # set by default to 0

        las_all_rp_df[las_layer_mvt_pct_of_claims_to_layer] = las_all_rp_df[las_layer_cy_pct_of_claims_to_layer].fillna(0) - las_all_rp_df[las_layer_prev_pct_of_claims_to_layer].fillna(0)
        las_all_rp_df[las_layer_mvt_premium] = las_all_rp_df[las_layer_cy_premium].fillna(0) - las_all_rp_df[las_layer_prev_premium].fillna(0)
        las_all_rp_df[las_layer_mvt_loss_to_layer] = las_all_rp_df[las_layer_cy_loss_to_layer].fillna(0) - las_all_rp_df[las_layer_prev_loss_to_layer].fillna(0)

        ##############################
        ## Assign Layer LAS Chart
        ##############################

        chart_items = [
            "limit",
            "this_year",
            "last_year",
            "ilf_selected",
        ]
        
        prefix_chart = f"{layer_name}/risk_profiles/chart/"

        # rp_layer_las_chart_outputs_flt = [f"{prefix_chart}{item}" for item in chart_items]
        
        las_layer_chart_limit = f"{prefix_chart}limit"
        las_layer_chart_this_year = f"{prefix_chart}this_year"
        las_layer_chart_last_year = f"{prefix_chart}last_year"
        las_layer_chart_ilf_selected = f"{prefix_chart}ilf_selected"

        def forward_fill_zero_or_na(df, source_col, target_col):
            """Helper function to forward-fill 0 or NaN values in target_col from source_col."""
            df[target_col] = df[source_col]
            mask = (df[source_col] == 0) | (df[source_col].isna())
            df.loc[mask, target_col] = df.loc[mask, target_col].shift(1).fillna(0)

        # Apply the helper function to each column pair
        forward_fill_zero_or_na(las_all_rp_df, las_layer_cy_upper, las_layer_chart_limit)
        forward_fill_zero_or_na(las_all_rp_df, las_layer_cy_loss_to_layer, las_layer_chart_this_year)
        forward_fill_zero_or_na(las_all_rp_df, las_layer_prev_loss_to_layer, las_layer_chart_last_year)
        forward_fill_zero_or_na(las_all_rp_df, las_layer_cy_ilf_selected, las_layer_chart_ilf_selected)

        ##############################
        ## Total LAS per layer
        ##############################       
        total_las_layer = getattr(las_layers,layer_name).total
        las_layer = getattr(las_layers,layer_name)

        total_las_layer_cy_prem_sum = las_all_rp_df[las_layer_cy_premium].sum()
        total_las_layer_cy_layer_to_loss_sum = las_all_rp_df[las_layer_cy_loss_to_layer].sum()

        total_las_layer_cy_prem_sum = (las_all_rp_df[las_layer_cy_premium].sum() if not las_all_rp_df[las_layer_cy_premium].isna().all() else 0.0)
        total_las_layer_cy_layer_to_loss_sum = (las_all_rp_df[las_layer_cy_loss_to_layer].sum() if not las_all_rp_df[las_layer_cy_loss_to_layer].isna().all() else 0.0)

        total_las_layer.current_year.premium = total_las_layer_cy_prem_sum
        total_las_layer.current_year.loss_to_layer = total_las_layer_cy_layer_to_loss_sum

        risk_bdx_summary = cds_layers[layer_index].risk_profile_bdx
        exposure_lr = risk_bdx_summary.exposure_lr or 0


        las_layer.glr =  exposure_lr
        las_layer.expected_loss = (exposure_lr * total_las_layer_cy_layer_to_loss_sum) or 0
        las_layer.pure_rate = (las_layer.expected_loss / total_las_layer_cy_prem_sum) if total_las_layer_cy_prem_sum !=0 else 0
        las_layer.rol = (total_las_layer_cy_layer_to_loss_sum / layer_limit) if layer_limit!=0 and layer_limit is not None else 0

        ##############################
        ## Write in Hxd
        ##############################

        # clean FGU data before writing it hxd
        hxd.cds.steer.exposure_rating.limit_average_severity.layers.fgu.risk_profiles = las_fgu_rp_df.to_dict(orient='records')

        # Create list of prefixed outputs
        rp_layer_las_cy_outputs_flt = [f"current_year/{item}" for item in rp_layer_las_cy_outputs]
        rp_layer_las_mvt_outputs_flt = [f"movement/{item}" for item in mvt_items]
        rp_layer_las_chart_outputs_flt = [f"chart/{item}" for item in chart_items]


        prefix = f"{layer_name}/risk_profiles/"
        las_layer_rp_df = las_all_rp_df.loc[:, las_all_rp_df.columns.str.startswith(prefix)]
        las_layer_rp_df.columns = las_layer_rp_df.columns.str.replace(prefix, "", regex=False)
                
        # clean layer data before writing it hxd
        # rp_fgu_las_df[rp_layer_las_cy_outputs_str ] = rp_fgu_las_df[rp_layer_las_cy_outputs_str ].fillna('')
        las_layer_rp_df[rp_layer_las_cy_outputs_flt ] = las_layer_rp_df[rp_layer_las_cy_outputs_flt ].fillna(0)
        las_layer_rp_df[rp_layer_las_mvt_outputs_flt ] = las_layer_rp_df[rp_layer_las_mvt_outputs_flt ].fillna(0)
        las_layer_rp_df[rp_layer_las_chart_outputs_flt ] = las_layer_rp_df[rp_layer_las_chart_outputs_flt ].fillna(0)

        # Combine output lists
        # rp_las_outputs = rp_las_outputs_flt + rp_las_outputs_str
        rp_layer_las_outputs = rp_layer_las_cy_outputs_flt + rp_layer_las_mvt_outputs_flt + rp_layer_las_chart_outputs_flt

        # las_layer_rp_df = las_layer_rp_df.drop(columns=["current_year/ilf_user_input"])
        # las_layer_rp_df = las_layer_rp_df.drop(columns=["current_year/ilf_user_input","previous_year/premium","previous_year/loss_to_layer",])

        # write to HXD
        write_pd_to_hxd(las_layer_rp_df, getattr(hxd.cds.steer.exposure_rating.limit_average_severity.layers,layer_name).risk_profiles,  rp_layer_las_outputs )

    return
