# v0.5.0
import hx, datetime, numpy as np, pandas as pd
import algorithms.rate_constants as const
from operator import itemgetter
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, remove_before_separator
# from libraries.model_profiler.algorithms.profiling_hxd_functions import time_me # commented as adjusted in a specific module in the model
from algorithms.model_profiler.profiling_hxd_functions import time_me


from algorithms.steer.rate_steer_experience_rating_triangle_projection import rate_steer_triangle_projection
from algorithms.steer.rate_steer_experience_rating_triangle_count_projection import rate_steer_triangle_count_projection

from scipy.interpolate import interp1d, PchipInterpolator

from algorithms.model_profiler.profiling_hxd_functions import time_me



@time_me
def rate_steer_experience_rating(hxd):

    ##############################
    ## Initialise variables
    ##############################

    layers = hxd.cds.layers
    er = hxd.cds.steer.experience_rating
    ol = hxd.cds.steer.experience_rating.on_levelling
    cy_yoa = hxd.cds.risk_information.inception_year
    future_inflation = hxd.cds.steer.experience_rating.on_levelling.future_inflation

    misc_params = hxd.cds.steer.experience_rating.misc_parameters
    data_map = hxd.cds.steer.experience_rating.data_mapping
    # raw_data_column_names = hxd.cds.steer.experience_rating.raw_data_column_names
    raw_data_column_names = hxd.steer.experience_rating.raw_data_column_names
    other_fields = hxd.cds.steer.experience_rating.other_fields
    coverage_basis = hxd.cds.steer.experience_rating.other_fields.coverage_basis.value
    data_as_at_date = hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value

    tbl_data_mapping = hx.params.table_steer_expe_data_mapping
    #  track the number of layers and burning cost year
    num_layers = len(hxd.cds.layers)
    num_years = len(ol.exposure_assumptions)

    expo_ass_df = pd_df_from_hx_list(ol.exposure_assumptions)
    raw_data_df = pd_df_from_hx_list(er.raw_data)

    inception_date = hxd.hx_core.inception_date

    # leap_day                = True if (hxd.hx_core.inception_date.month == 2 and hxd.hx_core.inception_date.day == 29) else False
    first_origin_month          = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.month or hxd.hx_core.inception_date.month)
    # first_origin_day            = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.day or hxd.hx_core.inception_date.day) - (1 if leap_day else 0)
    # first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)
    first_origin_year          = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.year or hxd.hx_core.inception_date.year)
    


    ############################################################
    ## Page On levelling
    ############################################################

    expo_ass_df = pd_df_from_hx_list(ol.exposure_assumptions)

    expo_ass_df["uw_year"] = [(cy_yoa - num_years + x) for x in range(1,num_years +1)] 
    expo_ass_df["display_yoa"] = expo_ass_df.uw_year.astype(int).astype(str)

    # Sort the DataFrame by uw_year in ascending order
    expo_ass_df = expo_ass_df.sort_values(by="uw_year", ascending=True)

    # clean data used in the calculation
    expo_ass_df["annual_rate_change"] = expo_ass_df["annual_rate_change"].fillna(0)
    expo_ass_df["claims_inflation"] = expo_ass_df["claims_inflation"].fillna(0)
    expo_ass_df["exposure"] = expo_ass_df["exposure"].fillna(0)

    # Set the last year's values
    expo_ass_df.loc[expo_ass_df.index[-1], "rate_change_index"] = 1
    # expo_ass_df.loc[expo_ass_df.index[-1], "inflation_index"] = 1 + (future_inflation or 0)
    expo_ass_df.loc[expo_ass_df.index[-1], "inflation_index"] = 1 

    # The loop starts from the second-to-last year and moves backward, multiplying by items from index i + 1
    for i in range(len(expo_ass_df) - 2, -1, -1):
        expo_ass_df.loc[expo_ass_df.index[i], "rate_change_index"] = (
                (expo_ass_df.loc[expo_ass_df.index[i + 1], "rate_change_index"]) *
                (1 + (expo_ass_df.loc[expo_ass_df.index[i + 1], "annual_rate_change"] or 0))
            )
        expo_ass_df.loc[expo_ass_df.index[i], "inflation_index"] = (
                (expo_ass_df.loc[expo_ass_df.index[i + 1], "inflation_index"]) *
                (1 + (expo_ass_df.loc[expo_ass_df.index[i ], "claims_inflation"] or 0))
            )

    expo_ass_df["exposure_on_level"] = expo_ass_df["exposure"] * expo_ass_df["rate_change_index"]
    
    #  Write to hxd
    expo_assump_output_columns_str = [
        "display_yoa"
    ]
    expo_assumnmp_output_columns_flt = [
        "uw_year"
        ,"exposure_on_level"
        ,"rate_change_index"
        ,"inflation_index"
    ]
    # clean data before writing it hxd
    expo_ass_df[expo_assump_output_columns_str ] = expo_ass_df[expo_assump_output_columns_str ].fillna('')
    expo_ass_df[expo_assumnmp_output_columns_flt ] = expo_ass_df[expo_assumnmp_output_columns_flt ].fillna(0)

    write_pd_to_hxd(expo_ass_df,  hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions,  expo_assump_output_columns_str + expo_assumnmp_output_columns_flt )

 
    ############################################################
    ## Page Data Format
    ############################################################

    # Misc Parameters: assign info nodes for 
    misc_params.target_year = inception_date.year
    misc_params.target_year_info = "Proposed year of cover. Must be one year after last year in data)"
    misc_params.closed_indicator_info = "Field name to indicate closed status"
    misc_params.data_layout_info = "Enter key to indicate structure (default 1, max 4)"

    # Data Mapping: assign field and field name and other column
    for index, item in enumerate(data_map):
        item[1].field = remove_before_separator(item[0],"_")
        item[1].field_name = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Field Name"].iloc[0]
        item[1].description = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Description"].iloc[0]
        # item[1].mandatory_column = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Mandatory Column"].iloc[0]
        item[1].mandatory_column = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]][f"Mandatory Column {coverage_basis}"].iloc[0]
        item[1].accept_missing = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Accept Missing Values"].iloc[0]
        item[1].field_type = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Field Type"].iloc[0]
        item[1].value_within_range = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Value Within Range"].iloc[0]
        item[1].replace_missing_with_default = tbl_data_mapping[tbl_data_mapping["node_name"]==item[0]]["Replace Missing with Default Value"].iloc[0]
    
    # Assign Raw Data column name for display
    for i in range(1, const.raw_data_max_column+1):  # Loop from 01 to 109, raw_data_max_column = 109
        column_name = f"column_{i:02d}"
        # setattr(hxd.cds.steer.experience_rating.raw_data_column_names, column_name, getattr(er.raw_data[0],column_name)) 
        setattr(hxd.steer.experience_rating.raw_data_column_names, column_name, getattr(er.raw_data[0],column_name))        

    # Other Fields: assign infoBy nodes
    other_fields.fvy.description = ""
    other_fields.lvy.description = ""
    other_fields.coverage_basis.description = "Default is costs inclusive"
    other_fields.bcost_measure.description = "Measure type Used for Bcost : Claim, Indemnity, Defense"
    

    # other_fields.coverage_basis.value = "Costs Inclusive"
    mapping_coverage_bcost_fields={
        "Costs Inclusive":"Claim",
        "Costs Exclusive":"Indemnity",
        "Costs Pro-Rata":"Indemnity, Expenses",
    }
    other_fields.bcost_measure.value = mapping_coverage_bcost_fields[coverage_basis]

    ############################################################
    ## Build triangles: page Triangle Projection, Triangle Projection per layer, Claim Count
    ############################################################

    # determine if using transient hxd
    live_hxd = False if "transient_hxd" in str(type(hxd)) else True
    if live_hxd:    
        rate_steer_triangle_projection(hxd) # page Triangle Projection, Triangle Projection per layer,
        rate_steer_triangle_count_projection(hxd)

    ############################################################
    ## Page Burning Cost - GET CLAIM INFO FROM PROCESSED DATA AND TRIANGLES (incurred claims, inflated claims, incurred_no_of_claims, dev pettern claim and count)
    ############################################################
    
    start_year = inception_date.year - const.experience_rating_max_years + 1
    end_year = inception_date.year

    ##############################
    ## START Helper functions ##
    ##############################
    def assign_yoa_labels(er_layers, inception_date, max_years,max_layers):
        """Assign policy_year and policy_year_label for all layers."""
        for yoa_index in range(max_years):
            policy_year = inception_date.year - max_years + yoa_index + 1
            policy_year_label = str(policy_year) if policy_year else ""

            # Assign to FGU layer
            er_layers.fgu.burning_cost[yoa_index].policy_year = policy_year
            er_layers.fgu.burning_cost[yoa_index].policy_year_label = policy_year_label

            # Assign to all RI layers
            for layer_index in range(max_layers):
                layer_name = f'layer_{layer_index+1:02d}'
                layer_bc = getattr(er_layers, layer_name).burning_cost[yoa_index]
                setattr(layer_bc, "policy_year", policy_year)
                setattr(layer_bc, "policy_year_label", policy_year_label)

    def create_bc_dataframes(er_layers, max_layers, pd_df_from_hx_list):
        """Create DataFrames for FGU and RI layers."""
        er_fgu_bc_df = pd_df_from_hx_list(er_layers.fgu.burning_cost)
        er_ri_layer_dfs = {}

        for layer_index in range(max_layers):
            layer_name = f'layer_{layer_index+1:02d}'
            df_name = f"er_ri_layer_{(layer_index+1):02d}_df"
            er_ri_layer_dfs[df_name] = pd_df_from_hx_list(getattr(er_layers, layer_name).burning_cost)

        return er_fgu_bc_df, er_ri_layer_dfs

    def get_claim_info_per_year(er, max_layers):
        """Prepare and aggregate experience data. Convert name from processed claims to Burning Cost"""
        # load the processed claims into a dataframe
        experience_data_df = pd_df_from_hx_list(er.processed_claims)

        # added for count
        experience_data_df["incurred_no_of_claims"] = 0
        experience_data_df.loc[experience_data_df["incurred_claims"]!=0,"incurred_no_of_claims"] = 1
        # adding count for inflated_claims
        experience_data_df["inflated_no_of_claims"] = 0
        experience_data_df.loc[experience_data_df["inflated_claims"]!=0,"inflated_no_of_claims"] = 1


        pc_claims_columns_list = [
            # "incurred_capped",
            # "trended_claim",
            "incurred_claims",
            "inflated_claims",
            "incurred_no_of_claims",
            "inflated_no_of_claims",

        ]

        for layer_index in range(max_layers):
            layer_suffix = f'{(layer_index+1):02d}'
            pc_claims_columns_list.extend([
                f"ri_claim_layer_{layer_suffix}",
                f"ri_claim_on_levelled_layer_{layer_suffix}",
                f"ri_claim_count_layer_{layer_suffix}",
                f"ri_claim_count_on_levelled_layer_{layer_suffix}",
                # f"inflated_ri_claim_count_layer_{layer_suffix}",
            ])
        
        agg_experience_data_df = experience_data_df.groupby("policy_year")[pc_claims_columns_list].sum().reset_index()
        
        # mapping processed claims to burning cost
        mapping_pc_to_bc ={
            # "incurred_capped":"incurred_claims",
            # "trended_claim":"inflated_claims",
            "incurred_claims":"incurred_claims",
            "inflated_claims":"inflated_claims",
            "incurred_no_of_claims":"incurred_no_of_claims",
            "inflated_no_of_claims":"inflated_no_of_claims",
        }
        mapping_pc_to_bc_for_layer ={
            "ri_claim_layer":"incurred_claims",
            "ri_claim_on_levelled_layer":"inflated_claims",
            "ri_claim_count_layer":"incurred_no_of_claims",
            "ri_claim_count_on_levelled_layer":"inflated_no_of_claims"
        }

        # Rename columns using mapping_pc_to_bc
        agg_experience_data_df = agg_experience_data_df.rename(columns=mapping_pc_to_bc)

        # Replace parts of column names using mapping_pc_to_bc_for_layer
        for old_part, new_part in mapping_pc_to_bc_for_layer.items():
            agg_experience_data_df.columns = [
                col.replace(old_part, new_part) if old_part in col else col
                for col in agg_experience_data_df.columns
            ]
        column_to_fill = list(mapping_pc_to_bc.values())
 
        return agg_experience_data_df, column_to_fill

    def ensure_all_years(filtered_df, start_year, end_year, columns_to_fill):
        """Ensure all years are present in the DataFrame, filling missing values with 0."""
        all_years = list(range(start_year, end_year + 1))
        all_years_df = pd.DataFrame({"policy_year": all_years})

        filtered_df = pd.merge(
            all_years_df,
            filtered_df,
            on="policy_year",
            how="left"
        )

        filtered_df[columns_to_fill] = filtered_df[columns_to_fill].fillna(0)
        filtered_df = filtered_df.sort_values(by="policy_year", ascending=True)

        return filtered_df

    def map_and_assign_data(filtered_df, er_fgu_bc_df, er_ri_layer_dfs, max_layers, output_columns):
        """Map and assign data to FGU and RI layer DataFrames."""
        # Assign to FGU
        for col in output_columns:
            er_fgu_bc_df[col] = filtered_df[col].fillna(0)

            # Assign to RI layers
            for layer_index in range(max_layers):
                df_name = f"er_ri_layer_{(layer_index+1):02d}_df"
                er_ri_layer_dfs[df_name][col] = filtered_df[f"{col}_{(layer_index+1):02d}"].fillna(0)

        return er_fgu_bc_df, er_ri_layer_dfs
    
    def get_adjusted_claims_dev_pattern(df,columns_to_fill, layer_name, triangulation_type, is_no_of_claim):
        """ 
        Get the pattern from the triangle, adjusted claims dev pattern, save to dataframe and add field to column_to_fill
        """
        
        # Determine column name for development percentage
        claim_dev_pct = (
            ("claim_count_dev_pct" if is_no_of_claim else "claim_dev_pct")
            + ("" if layer_name == "fgu" else f"_{layer_name[-2:]}")
        )

        triangulation = getattr(getattr(er_layers,layer_name),triangulation_type)
        pattern_type = getattr(er_layers,layer_name).pattern_type # for fgu defaulted to FGU and not available to change in the front end

        
        if "claim_count_dev_pct_" in claim_dev_pct:  # layer claim_count_dev
            # Pattern for layer, claim_count assign to fgu claim_count
            df[claim_dev_pct]=df["claim_count_dev_pct"]

        elif "claim_dev_pct_" in claim_dev_pct and pattern_type == "FGU": # layer claim_dev
            
            # Pattern for layer, claim_dev assign to fgu claim_count_dev
            df[claim_dev_pct]=df["claim_dev_pct"]     

        else:

            # dev_pattern_tri = triangulation.tri_3_selected

            # # Get the number of periods
            # number_of_period = dev_pattern_tri.origin_period_count
            # if number_of_period == 0:
            #     return df, columns_to_fill
            # # else get pattern and transform
            # tri_last_year = dev_pattern_tri.origin_periods[number_of_period - 1].year
            # tri_month = dev_pattern_tri.origin_periods[number_of_period - 1].month

            # Get the pattern
            # tri_pattern = dev_pattern_tri.pcts_developed_selected

            # from tasks.steer.py, steer_triangle_data()
            # last_origin_year            = int(aggregated_claims_tri["policy_year"].max())
            # first_origin_year           = int(aggregated_claims_tri["policy_year"].min())

            # leap_day                = True if (hxd.hx_core.inception_date.month == 2 and hxd.hx_core.inception_date.day == 29) else False
            # first_origin_month          = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.month or hxd.hx_core.inception_date.month)
            # first_origin_day            = (hxd.cds.steer.experience_rating.other_fields.data_as_at_date.value.day or hxd.hx_core.inception_date.day) - (1 if leap_day else 0)
            # first_origin_date           = datetime.date(first_origin_year,first_origin_month,first_origin_day)

            if triangulation.override_triangle == False: # use of overriden triangle
                number_of_period = triangulation.override_triangle_years
            else:
                # number_of_period = max(other_fields.lvy.value,last_origin_year)-min(other_fields.fvy.value,first_origin_year) + 1
                number_of_period = other_fields.lvy.value-min(other_fields.fvy.value,first_origin_year) + 1
            
            if number_of_period == 0:
                return df, columns_to_fill
            # else get pattern and transform

            if triangulation.override_triangle == True and triangulation.override_triangle_date_used:
                tri_last_year = triangulation.override_triangle_date_used.year or inception_date.year 
                tri_month = triangulation.override_triangle_date_used.month or inception_date.month
            else:
                tri_last_year = data_as_at_date.year
                tri_month = data_as_at_date.month or inception_date.month

            incremental_pattern = [factor.experience_selected for factor in triangulation.incremental_dev_factor]
            incremental_pattern_inc_tail = incremental_pattern.copy()
            incremental_pattern_inc_tail.pop(-1) # remove last item
            incremental_pattern_inc_tail.append(triangulation.tail_factor.experience_selected) # replace last item with Tail Factor
            #Reverse the incremental_pattern_inc_tail
            reversed_pattern = [1 if x is None else x for x in incremental_pattern_inc_tail[::-1]]

            # Calculate the cumulative product of the reversed pattern
            cumprod_reversed = np.cumprod(reversed_pattern)

            # Compute 1 / cumulative product
            cumulative_pattern = 1 / cumprod_reversed

            # Reverse back to the original order
            cumulative_pattern = cumulative_pattern[::-1]

            tri_pattern = cumulative_pattern
            
            # Assign the pattern to the DataFrame in reverse order
            pattern_df = pd.DataFrame({"end_of_year_pattern": tri_pattern})
            pattern_df["end_of_year_pattern"] = pattern_df["end_of_year_pattern"].values[::-1]

            # Assign policy years
            pattern_df["policy_year"] = tri_last_year - len(pattern_df) + pattern_df.index + 1

            # Merge with all years DataFrame and fill missing values with 0
            df = pd.merge(df, pattern_df, on="policy_year", how="left").fillna(0)

            # Find the index of the first non-zero value
            first_non_zero_idx = df["end_of_year_pattern"].ne(0).idxmax()

            # Set all values before the first non-zero value to 1
            if pd.notna(first_non_zero_idx) and first_non_zero_idx > 0:
                df.loc[:first_non_zero_idx - 1, "end_of_year_pattern"] = 1

            # Prepare data for interpolation
            df["month"] = const.experience_rating_max_years * 12 - (df.index + 1) * 12
            df["actual_month"] = (
                const.experience_rating_max_years * 12 - (df.index + 2) * 12 + tri_month
            )
            df["actual_month"] = np.where(df["actual_month"] < 0, 0, df["actual_month"])

            # Interpolate development patterns
            X = df["month"]
            y = df["end_of_year_pattern"]
            Z = df["actual_month"]

            interp_func = interp1d(X, y, kind="linear", fill_value="extrapolate")
            
            df[claim_dev_pct] = interp_func(Z)

            # Remove temporary columns
            df.drop(columns=["end_of_year_pattern", "month", "actual_month"], inplace=True)

        # add column name to list
        if claim_dev_pct in columns_to_fill:
            pass
        else:
            columns_to_fill.append(claim_dev_pct)

        return df, columns_to_fill

    def get_column_name(layer_name: str, hxd_col_name: str) -> str:
        """
        Returns the exposure column name based on the layer_name.

        Args:
            layer_name (str): The name of the layer (e.g., "fgu", "ri_claim_layer_01").
            hxd_col_name (str, optional): The base column name. Defaults to "exposure".

        Returns:
            str: The exposure column name.
        """
        return hxd_col_name if layer_name == "fgu" else f"{hxd_col_name}_{layer_name[-2:]}"
    ##############################
    ## END helper functions ##
    ##############################  


    ##############################
    ## Start Initialise Variables and lists
    ##############################
    er_layers = er.layers
    # Assign YOA labels columns in the burning cost node
    assign_yoa_labels(er_layers, inception_date, const.experience_rating_max_years,const.max_layers)

    # Create BC DataFrames - use for writing to hxd
    er_fgu_bc_df, er_ri_layer_dfs = create_bc_dataframes(er_layers, const.max_layers, pd_df_from_hx_list)

    # calculated node list to write to hxd to burning cost
    bc_output_columns = [
        "onlevelled_exposure",
        "incurred_claims",
        "incurred_no_of_claims",
        "inflated_claims",
        "inflated_no_of_claims",
        "claim_dev_pct",
        "claim_count_dev_pct",
        "ultimate_claims_developed",
        "ultimate_claims_developed_and_inflated",
        "ibnr",
        "ultimate_no_of_claims_developed",
        "frequency_per_m_exposure",
        "average_cost_per_claim",
        "loss_cost_per_m_exposure",
        "rate_pct",
        "expected_loss_cost",
        "ulr",
        "claim_dev_method",
        "claim_count_dev_method",
        "cl_incurred_claims_developed",
        "cl_inflated_claims_developed",
        "cl_claim_count_developed",
        "cl_freq",
        "cl_acpc",
        "cl_acpc_inflated",
        "bf_claim_amount",
        "bf_claim_amount_inflated",
        "bf_claim_count",

        "average_expected_loss_cost",
        "average_freq_per_m_exposure",
        "average_loss_cost_per_m_exposure",

        ] 

    # create dict - use for writing to hxd
    selected_wa_dict = {}
    all_y_wa_dict = {}
    ms_bc_dict = {}
    
    ms = hxd.model_state
    # selected_wa_dict and all_y_wa_dict keys
    agg_output = [
        "frequency_per_m_exposure",
        "average_cost_per_claim",
        "loss_cost_per_m_exposure",
        "rate_pct",
        "expected_loss_cost",
        "premium",
        "ulr",
    ]
    ##############################
    ## End Initialise Variables and lists
    ##############################

    if len(er.processed_claims)==0:
        return

    layer_list = ["fgu"]
    for layer_index in range(len(hxd.cds.layers)):

        layer_name=f"layer_{layer_index+1:02d}"
        layer_list.append(layer_name)
    
    is_pattern_updated = steer_validate_bc_patterns(hxd)
    
    if not is_pattern_updated:
        return

    for layer_name in layer_list:
        tri   = getattr(hxd.cds.steer.experience_rating.layers, layer_name).triangle_projection
        cc   = getattr(hxd.cds.steer.experience_rating.layers, layer_name).claim_count


        for index in range(len(tri.incremental_dev_factor)):
            tri.incremental_dev_factor[index].experience_selected = tri.incremental_dev_factor[index].experience_selected_set_in_task
            cc.incremental_dev_factor[index].experience_selected = cc.incremental_dev_factor[index].experience_selected_set_in_task
        if tri.tail_factor.experience_selected_set_in_task is not None:
            tri.tail_factor.experience_selected = tri.tail_factor.experience_selected_set_in_task
        if tri.tail_factor.experience_override is not None and tri.tail_factor.experience_override > 0:
            tri.tail_factor.experience_selected = tri.tail_factor.experience_override or 1
        else:
            tri.tail_factor.experience_selected = tri.tail_factor.experience_default or 1


    # Prepare and aggregate experience data
    agg_claim_data, columns_to_fill = get_claim_info_per_year(er, len(hxd.cds.layers))


    # Filter and ensure all years are present
    all_year_claims_data_df = agg_claim_data[
        (agg_claim_data["policy_year"] >= start_year) &
        (agg_claim_data["policy_year"] <= end_year) 
    ].copy()

    last_origin_year            = int(agg_claim_data["policy_year"].max())
    first_origin_year           = int(agg_claim_data["policy_year"].min())        

    all_year_claims_data_df = ensure_all_years(all_year_claims_data_df, start_year, end_year, columns_to_fill)
    
    layer_list=["fgu"]
    # add active layers
    for layer_index in range(len(layers)):

        layer_list.append(f"layer_{layer_index+1:02d}")

 
    for layer_name in layer_list:      
        # create list of triangulation     
        triangulations_list = ["triangle_projection", "claim_count"]

        for triangulation_type in triangulations_list:
            # set claim_count status
            is_claim_count = True if triangulation_type == "claim_count" else False

            # add claim pattern
            all_year_claims_data_df , columns_to_fill= get_adjusted_claims_dev_pattern(all_year_claims_data_df, columns_to_fill, layer_name, triangulation_type, is_claim_count)

    ##############################
    ## Burning Cost Page - CALCULATE BURNING COST RESULT COLUMMS
    ##############################

    # Get exposure from hxd into a dataframe
    er_on_levelling_assumptions_df = pd_df_from_hx_list(hxd.cds.steer.experience_rating.on_levelling.exposure_assumptions)
    
    # ensure all layer name are in the layer list
    for layer_index, layer in enumerate(layers):

        layer_name = f"layer_{layer_index+1:02d}"
        if layer_name in layer_list:
            pass
        else:
            layer_list.append(layer_name)

    # Loop through all layer an calculate columns
    for layer_name in layer_list:
        # exposure_column relate to Exposure assumtion naming convention
        if layer_name == "fgu":
            exposure_column = "exposure_on_level"
        else:
            exposure_column = f"exposure_adjusted_{layer_name}"

        # Initialise layer dependent column name
        # policy_year_label_column = get_column_name(layer_name, "policy_year_label")
        # policy_year_column = get_column_name(layer_name, "policy_year")
        weighting_column = get_column_name(layer_name, "weighting") # input
        onlevelled_exposure_column = get_column_name(layer_name, "onlevelled_exposure")
        incurred_claims_column = get_column_name(layer_name, "incurred_claims")
        inflated_claims_column = get_column_name(layer_name, "inflated_claims")
        incurred_no_of_claims_column = get_column_name(layer_name, "incurred_no_of_claims")
        inflated_no_of_claims_column = get_column_name(layer_name, "inflated_no_of_claims")

        ultimate_claims_developed_column = get_column_name(layer_name, "ultimate_claims_developed")
        ultimate_claims_developed_and_inflated_column = get_column_name(layer_name, "ultimate_claims_developed_and_inflated")
        ibnr_column = get_column_name(layer_name, "ibnr")
        ultimate_no_of_claims_developed_column = get_column_name(layer_name, "ultimate_no_of_claims_developed")
        frequency_per_m_exposure_column = get_column_name(layer_name, "frequency_per_m_exposure")
        average_cost_per_claim_column = get_column_name(layer_name, "average_cost_per_claim")
        loss_cost_per_m_exposure_column = get_column_name(layer_name, "loss_cost_per_m_exposure")
        rate_pct_column = get_column_name(layer_name, "rate_pct")
        expected_loss_cost_column = get_column_name(layer_name, "expected_loss_cost")
        
        premium_column = get_column_name(layer_name, "premium") # input
        ulr_column = get_column_name(layer_name, "ulr")

        ulr_as_if_expo_column = get_column_name(layer_name, "ulr_as_if_expo_only")
        ulr_as_if_prem_column = get_column_name(layer_name, "ulr_as_if_prem_only")
        bc_ulr_message_column = get_column_name(layer_name, "bc_ulr_message")

        claim_dev_pct_column = get_column_name(layer_name, "claim_dev_pct")
        claim_count_dev_pct_column = get_column_name(layer_name, "claim_count_dev_pct")
        claim_dev_method_column = get_column_name(layer_name, "claim_dev_method")
        claim_count_dev_method_column = get_column_name(layer_name, "claim_count_dev_method")
        cl_incurred_claims_developed_column = get_column_name(layer_name, "cl_incurred_claims_developed")
        cl_inflated_claims_developed_column = get_column_name(layer_name, "cl_inflated_claims_developed")
        cl_claim_count_developed_column = get_column_name(layer_name, "cl_claim_count_developed")
        cl_freq_column = get_column_name(layer_name, "cl_freq")
        cl_acpc_column = get_column_name(layer_name, "cl_acpc")
        cl_acpc_inflated_column = get_column_name(layer_name, "cl_acpc_inflated")
        bf_claim_amount_column = get_column_name(layer_name, "bf_claim_amount")
        bf_claim_amount_inflated_column = get_column_name(layer_name, "bf_claim_amount_inflated")
        bf_claim_count_column = get_column_name(layer_name, "bf_claim_count")

        average_expected_loss_cost_column = get_column_name(layer_name, "average_expected_loss_cost")
        average_freq_per_m_exposure_column = get_column_name(layer_name, "average_freq_per_m_exposure")
        average_loss_cost_per_m_exposure_column = get_column_name(layer_name, "average_loss_cost_per_m_exposure")
        
        
        # Assign on levelled exposure column
        exposure_values = er_on_levelling_assumptions_df[exposure_column].fillna(0)
        fallback_exposure = er_on_levelling_assumptions_df["exposure_on_level"].fillna(0) #fgu
        all_year_claims_data_df[onlevelled_exposure_column] = np.where(
            exposure_values != 0,
            exposure_values,
            fallback_exposure,
        )

        
        # Define method used for claims projection
        all_year_claims_data_df[claim_dev_method_column] = np.where(
            all_year_claims_data_df[claim_dev_pct_column].isna(),
            "",
            np.where(
                all_year_claims_data_df[claim_dev_pct_column] >= const.cl_dev_thres,
                # "Pure Chain-Ladder",
                # "Bornhuetter-Ferguson"
                "CL",
                "BF"
            )
        )

        # Define method used for claim count projection
        all_year_claims_data_df[claim_count_dev_method_column] = np.where(
            all_year_claims_data_df[claim_count_dev_pct_column].isna(),
            "",
            np.where(
                all_year_claims_data_df[claim_count_dev_pct_column] >= const.cl_dev_thres,
                # "Pure Chain-Ladder",
                # "Bornhuetter-Ferguson"
                "CL",
                "BF"
            )
        )

        # Project incurred claims
        condition_default_cl = (
            (all_year_claims_data_df[claim_dev_pct_column] == 0) |
            (all_year_claims_data_df["policy_year"] > other_fields.lvy.value)
        )
        all_year_claims_data_df[cl_incurred_claims_developed_column] = np.where(
            condition_default_cl,
            0,
            all_year_claims_data_df[incurred_claims_column] / all_year_claims_data_df[claim_dev_pct_column]
        )

        # Project inflated claims
        all_year_claims_data_df[cl_inflated_claims_developed_column] = np.where(
            condition_default_cl,
            0,
            all_year_claims_data_df[inflated_claims_column] / all_year_claims_data_df[claim_dev_pct_column]
        )

        # Project claim count
        all_year_claims_data_df[cl_claim_count_developed_column] = np.where(
            condition_default_cl,
            0,
            all_year_claims_data_df[inflated_no_of_claims_column] / all_year_claims_data_df[claim_count_dev_pct_column]
        )

        # Calculate claim frequency
        all_year_claims_data_df[cl_freq_column] = np.where(
            all_year_claims_data_df[onlevelled_exposure_column] == 0,
            0,
            (all_year_claims_data_df[cl_claim_count_developed_column] / (all_year_claims_data_df[onlevelled_exposure_column] / const.exposure_unit)) 
        )

        # Calculate claim Average Cost Per Claim based on incurred claims
        all_year_claims_data_df[cl_acpc_column] = np.where(
            all_year_claims_data_df[cl_claim_count_developed_column] == 0,
            0,
            all_year_claims_data_df[cl_incurred_claims_developed_column] / all_year_claims_data_df[cl_claim_count_developed_column]
        )

        # Calculate claim Average Cost Per Claim based on inflated claims
        all_year_claims_data_df[cl_acpc_inflated_column] = np.where(
            all_year_claims_data_df[cl_claim_count_developed_column] == 0,
            0,
            all_year_claims_data_df[cl_inflated_claims_developed_column] / all_year_claims_data_df[cl_claim_count_developed_column]
        )

        ##############################
        ## Burning Cost Page - CALCULATE EXPECTED ASSUMPTIONS USED BF
        ##############################
        # Get pattern type
        pattern_type = getattr(er.layers,layer_name).pattern_type
        
        if pattern_type == "FGU":
            claim_dev_pact_basis = f"claim_dev_pct_{layer_index+1:02d}"
        else:
            claim_dev_pact_basis = "claim_dev_pct"

        bf_expected = ["incurred_claim","inflated_claim"]

        # calculated the year to take into account
        no_of_mature_years = (all_year_claims_data_df[claim_dev_pact_basis] > const.cl_dev_thres).sum()
        
        for bf_basis in bf_expected:
            getattr(getattr(er.layers,layer_name).bf_expected,bf_basis).offset_rows = no_of_mature_years

            # Calculate the sum of onlevelled_exposure for mature years
            sum_onlevelled_exposure = all_year_claims_data_df[onlevelled_exposure_column][:no_of_mature_years].sum()

            # initialised variable
            frequency_per_m_exposure = 0
            acpc = 0

            if sum_onlevelled_exposure !=0:
                # calculate the frequency_per_m_exposure
                frequency_per_m_exposure =  float((all_year_claims_data_df[onlevelled_exposure_column][:no_of_mature_years] * all_year_claims_data_df[cl_freq_column][:no_of_mature_years]).sum() / sum_onlevelled_exposure)
                # calculate the acpc
                bf_basis_acpc_column = cl_acpc_inflated_column if bf_basis == "inflated_claim" else cl_acpc_column
                acpc = float((all_year_claims_data_df[onlevelled_exposure_column][:no_of_mature_years] * all_year_claims_data_df[bf_basis_acpc_column][:no_of_mature_years]).sum() / sum_onlevelled_exposure)
                # calculate the loss_cost_per_m_revenue

            # calculate the frequency_per_m_exposure
            getattr(getattr(er.layers,layer_name).bf_expected,bf_basis).frequency_per_m_exposure = frequency_per_m_exposure
            # calculate the acpc
            getattr(getattr(er.layers,layer_name).bf_expected,bf_basis).acpc = acpc
            # calculate the loss_cost_per_m_revenue
            getattr(getattr(er.layers,layer_name).bf_expected,bf_basis).loss_cost_per_m_revenue = frequency_per_m_exposure * acpc
                            
        ##############################
        ## Burning Cost Page - CALCULATE BF METHOD
        ##############################

        condition_bf = (
            (all_year_claims_data_df["policy_year"] > other_fields.lvy.value) |
            (all_year_claims_data_df[onlevelled_exposure_column] == 0)
        )

        all_year_claims_data_df[bf_claim_amount_column] = np.where(
            condition_bf,
            0,
            all_year_claims_data_df[incurred_claims_column] +
            (1 - all_year_claims_data_df[claim_dev_pct_column]) *
            getattr(er.layers, layer_name).bf_expected.incurred_claim.loss_cost_per_m_revenue *
            (all_year_claims_data_df[onlevelled_exposure_column] / const.exposure_unit)
        )
        all_year_claims_data_df[bf_claim_amount_inflated_column] = np.where(
            condition_bf,
            0,
            all_year_claims_data_df[inflated_claims_column] + (1-all_year_claims_data_df[claim_dev_pct_column]) * getattr(er.layers,layer_name).bf_expected.inflated_claim.loss_cost_per_m_revenue * (all_year_claims_data_df[onlevelled_exposure_column]/const.exposure_unit)
        )
        all_year_claims_data_df[bf_claim_count_column] = np.where(
            condition_bf,
            0,
            all_year_claims_data_df[inflated_no_of_claims_column] + (1-all_year_claims_data_df[claim_count_dev_pct_column]) * getattr(er.layers,layer_name).bf_expected.inflated_claim.frequency_per_m_exposure * (all_year_claims_data_df[onlevelled_exposure_column]/const.exposure_unit)
        )


        ##############################
        ## Burning Cost Page - RESULT COLUMNS
        ##############################

        all_year_claims_data_df[ultimate_claims_developed_column] = np.where(all_year_claims_data_df[claim_dev_pct_column]>=const.cl_dev_thres,
            all_year_claims_data_df[cl_incurred_claims_developed_column],
            all_year_claims_data_df[bf_claim_amount_column]
            )

        all_year_claims_data_df[ultimate_claims_developed_and_inflated_column] = np.where(all_year_claims_data_df[claim_dev_pct_column]>=const.cl_dev_thres,
            all_year_claims_data_df[cl_inflated_claims_developed_column],
            all_year_claims_data_df[bf_claim_amount_inflated_column]
            )

        all_year_claims_data_df[ibnr_column] = all_year_claims_data_df[ultimate_claims_developed_and_inflated_column] - all_year_claims_data_df[inflated_claims_column]

        all_year_claims_data_df[ultimate_no_of_claims_developed_column] = np.where(all_year_claims_data_df[claim_count_dev_pct_column]>=const.cl_dev_thres,
            all_year_claims_data_df[cl_claim_count_developed_column],
            all_year_claims_data_df[bf_claim_count_column]
            )


        all_year_claims_data_df[frequency_per_m_exposure_column] = np.where(all_year_claims_data_df[onlevelled_exposure_column]==0,
            0,
            all_year_claims_data_df[ultimate_no_of_claims_developed_column] / (all_year_claims_data_df[onlevelled_exposure_column]/const.exposure_unit)
        )

        all_year_claims_data_df[average_cost_per_claim_column] = np.where(all_year_claims_data_df[ultimate_no_of_claims_developed_column] ==0,
            0,
            all_year_claims_data_df[ultimate_claims_developed_and_inflated_column] / all_year_claims_data_df[ultimate_no_of_claims_developed_column]  
            )

        all_year_claims_data_df[loss_cost_per_m_exposure_column] = all_year_claims_data_df[frequency_per_m_exposure_column] * all_year_claims_data_df[average_cost_per_claim_column]

        all_year_claims_data_df[rate_pct_column] = all_year_claims_data_df[loss_cost_per_m_exposure_column]/const.exposure_unit

        all_year_claims_data_df[expected_loss_cost_column] = all_year_claims_data_df[rate_pct_column] * all_year_claims_data_df[onlevelled_exposure_column].iat[-1] 

        # get input values from hxd, necessary for calculation
        if layer_name == "fgu":
            all_year_claims_data_df[premium_column]  = er_fgu_bc_df["premium"].fillna(0)
            all_year_claims_data_df[weighting_column]  = er_fgu_bc_df["weighting"].fillna(0)

        else:
            df_name = f"er_ri_{layer_name}_df"
            all_year_claims_data_df[premium_column]  = er_ri_layer_dfs[df_name]["premium"].fillna(0)
            all_year_claims_data_df[weighting_column]  = er_ri_layer_dfs[df_name]["weighting"].fillna(0)


        all_year_claims_data_df[ulr_column] = np.where(all_year_claims_data_df[premium_column] ==0,
            np.where(all_year_claims_data_df[onlevelled_exposure_column]==0,
                0,
                all_year_claims_data_df[ultimate_claims_developed_and_inflated_column]/all_year_claims_data_df[onlevelled_exposure_column]
                ),
            all_year_claims_data_df[ultimate_claims_developed_and_inflated_column]/all_year_claims_data_df[premium_column] 
            )

        all_year_claims_data_df[ulr_as_if_expo_column] = np.where(all_year_claims_data_df[onlevelled_exposure_column]==0,
            0,
            all_year_claims_data_df[ultimate_claims_developed_and_inflated_column]/all_year_claims_data_df[onlevelled_exposure_column]
            )
        
        all_year_claims_data_df[ulr_as_if_prem_column] = np.where(all_year_claims_data_df[premium_column] ==0,
            0,
            all_year_claims_data_df[ultimate_claims_developed_and_inflated_column]/all_year_claims_data_df[premium_column] 
            )

        ##############################
        # Burning Cost Page - selected_years_wa and all_years_wa
        ##############################                  
        weighted_expo_df = all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1] * all_year_claims_data_df[weighting_column].iloc[:-1]
        expo_df = all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1]
        weighted_prem_df = all_year_claims_data_df[premium_column].iloc[:-1] * all_year_claims_data_df[weighting_column].iloc[:-1]
        prem_df = all_year_claims_data_df[premium_column].iloc[:-1]
        ulr_as_if_expo_df = all_year_claims_data_df[ulr_as_if_expo_column].iloc[:-1]
        ulr_as_if_prem_df = all_year_claims_data_df[ulr_as_if_prem_column].iloc[:-1]


        has_all_premium_provided = not (
            (all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1] != 0) &
            (all_year_claims_data_df[premium_column].iloc[:-1] == 0)
        ).any()
        
        for column in agg_output:
            # Get the column name for the current column
            column_name = get_column_name(layer_name, column)
            if column  == "premium":
                # Apply the formula for selected_wa_dict
                # selected_wa_dict[column_name] = np.where(weighted_expo_df==0,0,all_year_claims_data_df[column_name].iloc[:-1]).sum()
                
                selected_wa_dict[column_name] = np.where(weighted_expo_df==0,0,weighted_prem_df).sum()


                # Apply the formula for all_y_wa_dict
                all_y_wa_dict[column_name] = all_year_claims_data_df[column_name].iloc[:-1].sum() 
            elif column == "ulr":
                if has_all_premium_provided:
                    # Apply the formula for selected_wa_dict
                    selected_wa_dict[column_name] = (ulr_as_if_prem_df * weighted_prem_df).sum()  / weighted_prem_df.sum() if weighted_prem_df.sum() !=0 else 0

                    # Apply the formula for all_y_wa_dict
                    all_y_wa_dict[column_name] = (ulr_as_if_prem_df * prem_df).sum() / prem_df.sum() if prem_df.iloc[:-1].sum() != 0 else 0
                    ms_bc_dict[bc_ulr_message_column] = "The Selected Year WA and All Year WA ULRs are being calculated based on Manual Premium."
                else:
                    # Apply the formula for selected_wa_dict
                    selected_wa_dict[column_name] = (ulr_as_if_expo_df * weighted_expo_df).sum() / weighted_expo_df.sum() if weighted_expo_df.sum() !=0 else 0

                    # Apply the formula for all_y_wa_dict
                    # all_y_wa_dict[column_name] = ((all_year_claims_data_df[column_name].iloc[:-1] * all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1]).sum() / all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1].sum()) if all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1].sum()!=0 else 0
                    all_y_wa_dict[column_name] = (ulr_as_if_expo_df* expo_df).sum() / expo_df.sum() if expo_df.sum() !=0 else 0
                    if prem_df.sum() ==0:
                        ms_bc_dict[bc_ulr_message_column] = "The Selected Year WA and All Year WA ULRs are being calculated based on On-Levelled Exposure."
                    else:
                        ms_bc_dict[bc_ulr_message_column] = "Provide Premium for all years: the Selected Year WA and All Year WA ULRs are being calculated based on On-Levelled Exposure due to missing Premium"
            else:
                # Apply the formula for selected_wa_dict
                selected_wa_dict[column_name] = (all_year_claims_data_df[column_name].iloc[:-1] * weighted_expo_df).sum() / weighted_expo_df.sum() if weighted_expo_df.sum() !=0 else 0

                # Apply the formula for all_y_wa_dict
                # all_y_wa_dict[column_name] = ((all_year_claims_data_df[column_name].iloc[:-1] * all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1]).sum() / all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1].sum()) if all_year_claims_data_df[onlevelled_exposure_column].iloc[:-1].sum()!=0 else 0
                all_y_wa_dict[column_name] = (all_year_claims_data_df[column_name].iloc[:-1] * expo_df).sum() / expo_df.sum() if expo_df.sum() !=0 else 0

        ##############################
        ## Burning Cost Page - Assign data for Charts
        ##############################                  
        all_year_claims_data_df[average_expected_loss_cost_column] = selected_wa_dict[expected_loss_cost_column]
        all_year_claims_data_df[average_freq_per_m_exposure_column] = selected_wa_dict[frequency_per_m_exposure_column]
        all_year_claims_data_df[average_loss_cost_per_m_exposure_column] = selected_wa_dict[loss_cost_per_m_exposure_column]
        
        # For inception year, set all columns except "onlevelled_exposure" to None
        last_row_index = all_year_claims_data_df.index[-1]
        columns_to_clean = [col for col in all_year_claims_data_df.columns if not col.startswith("onlevelled_exposure")]

        all_year_claims_data_df.loc[last_row_index, columns_to_clean] = None

    # Map and assign data
    er_fgu_bc_df, er_ri_layer_dfs = map_and_assign_data(all_year_claims_data_df, er_fgu_bc_df, er_ri_layer_dfs, len(hxd.cds.layers),bc_output_columns)
    
    ##############################
    # Write data back to HXD
    ##############################

    # Write BC FGU data
    write_pd_to_hxd(er_fgu_bc_df, er_layers.fgu.burning_cost, bc_output_columns)
    
    # Write Selected_Y_WA and All_Y_WA years FGU data
    for col in agg_output:
        setattr(er_layers.fgu.selected_years_wa,col,selected_wa_dict[col])
        setattr(er_layers.fgu.all_years_wa,col, all_y_wa_dict[col])
    
    # Write FGU bc ulr message
    er_layers.fgu.bc_ulr_message = ms_bc_dict["bc_ulr_message"]

    # Assign summary values. Empty excess and limit for FGU
    er_layers.fgu.pure_rate = er_layers.fgu.selected_years_wa.rate_pct
    er_layers.fgu.ulr = er_layers.fgu.selected_years_wa.ulr
    

    # Write RI layer BC data
    for layer_index in range(len(hxd.cds.layers)):
        df_name = f"er_ri_layer_{(layer_index+1):02d}_df"
        layer_name = f'layer_{layer_index+1:02d}'

        er_layer_bc_df = er_ri_layer_dfs[df_name]
        hxd_layer_bc = getattr(er_layers, layer_name).burning_cost

        bc_ulr_mess_node = f"bc_ulr_message_{layer_index+1:02d}"

        write_pd_to_hxd(er_layer_bc_df, hxd_layer_bc, bc_output_columns) 

        # Write Selected_Y_WA and All_Y_WA years data
        for col in agg_output:
            setattr(getattr(er_layers,layer_name).selected_years_wa,col, selected_wa_dict[f"{col}_{(layer_index+1):02d}"])
            setattr(getattr(er_layers,layer_name).all_years_wa,col, all_y_wa_dict[f"{col}_{(layer_index+1):02d}"])
        # Write FGU bc ulr message in model state nodes
        # setattr(ms,bc_ulr_mess_node, ms_bc_dict[bc_ulr_mess_node])
        # Write FGU bc ulr message in children node (Use of selector)
        setattr(getattr(er_layers,layer_name),"bc_ulr_message", ms_bc_dict[bc_ulr_mess_node])


        getattr(er_layers, layer_name).excess = layers[layer_index].excess
        getattr(er_layers, layer_name).limit = layers[layer_index].limit
        getattr(er_layers, layer_name).pure_rate = getattr(er_layers, layer_name).selected_years_wa.rate_pct
        getattr(er_layers, layer_name).ulr = getattr(er_layers, layer_name).selected_years_wa.ulr
    

    
def steer_validate_bc_patterns(hxd):
    """
    Validate that experience_selected_set_in_task matches expected logic.
    If ANY mismatch is found, flag ALL layers (tri + cc).
    """

    def _expected_value(node):
        if node.experience_override is not None and node.experience_override > 0:
            return node.experience_override
        return node.experience_default or 1

    layer_list = ["fgu"] + [
        f"layer_{i+1:02d}" for i in range(len(hxd.cds.layers))
    ]

    mismatch_found = False
    layers_cache = []

    ##############################
    ## First pass: detect mismatch
    ##############################
    
    for layer_name in layer_list:
        layer = getattr(hxd.cds.steer.experience_rating.layers, layer_name)
        tri = layer.triangle_projection
        cc = layer.claim_count

        tri.update_pattern_message = ""
        cc.update_pattern_message = ""

        layers_cache.append((tri, cc))  # store for second pass
        ##############################
        ## Incremental dev factors
        ##############################
        for i in range(len(tri.incremental_dev_factor)):
            if tri.incremental_dev_factor[i].experience_selected_set_in_task != _expected_value(
                tri.incremental_dev_factor[i]
            ):
                mismatch_found = True
                break

            if cc.incremental_dev_factor[i].experience_selected_set_in_task != _expected_value(
                cc.incremental_dev_factor[i]
            ):
                mismatch_found = True
                break

        if mismatch_found:
            break

        ##############################
        ## Tail factors
        ##############################
        if tri.tail_factor.experience_selected_set_in_task != _expected_value(tri.tail_factor):
            mismatch_found = True
            break

        if cc.tail_factor.experience_selected_set_in_task != _expected_value(cc.tail_factor):
            mismatch_found = True
            break

    ##############################
    ## Second pass: apply or reset flags globally
    ##############################
    for tri, cc in layers_cache:
        if mismatch_found:
            tri.is_not_experience_selected_updated = True
            cc.is_not_experience_selected_updated = True

            tri.update_pattern_message = "⚠️Burning Cost Pattern and Experience Selected must be updated"
            cc.update_pattern_message = "⚠️Burning Cost Pattern and Experience Selected must be updated"

        else:
            tri.is_not_experience_selected_updated = False
            cc.is_not_experience_selected_updated = False

            # Clear message (use None or "" depending on your schema)
            tri.update_pattern_message = ""
            cc.update_pattern_message = ""

    if mismatch_found:
        hxd.cds.steer.experience_rating.is_not_experience_selected_updated = True
    else:
        hxd.cds.steer.experience_rating.is_not_experience_selected_updated = False

    return not mismatch_found
