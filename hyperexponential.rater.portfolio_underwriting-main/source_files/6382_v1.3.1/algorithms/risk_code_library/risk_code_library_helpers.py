import numpy  as np
import pandas as pd
import algorithms.rate_utilities as utils


def set_do_we_model(df, lloyds_risk_codes_list, lloyds_data):
    min_num_yr_data = 4
    # Create a new column 'do_we_model' that is True if 'risk_code' exists in the provided list
    df["do_we_model"] = df["risk_code"].isin(lloyds_risk_codes_list)

    # Convert boolean values (True/False) into "Yes"/"No" 
    df["do_we_model"] = df["do_we_model"].map({True: "Yes", False: "No"}) 

    # inspect lloyds data for <4 years of data and set do_we_model to No where fails
    l_df                        = lloyds_data.rename(columns={'lloyds_risk_code':'risk_code'})
    l_df['gpi']                 = pd.to_numeric(l_df['gpi'], errors='coerce')
    l_df['lloyds_num_years']    = np.where( l_df['gpi'].fillna(0)!=0, 1, 0)
    lloyds_num_yr_df            = l_df.groupby('risk_code',as_index=False)['lloyds_num_years'].sum()
    df                          = utils.drop_and_merge(df, lloyds_num_yr_df, 'risk_code')
    mask                        = df['lloyds_num_years'].fillna(0) < min_num_yr_data
    df.loc[mask,"do_we_model"]  = "No"

    return df.drop(columns=["lloyds_num_years"])


def latest_year_premium_vectorised(df, data_table, code_column, year_column, value_column, multiplying_factor, year_start, year_end):
    # Filter rows from data_table where the year is between year_start and year_end (inclusive)
    filtered_data = data_table[
        (data_table[year_column] >= year_start) &
        (data_table[year_column] <= year_end)
    ]

    # Group filtered data by code_column, summing the values in value_column
    # Then scale the results by multiplying_factor
    grouped_data = filtered_data.groupby(code_column)[value_column].sum() * multiplying_factor

    # Map the grouped values back onto df using 'risk_code' as the key
    # Missing codes are filled with 0
    return df["risk_code"].map(grouped_data).fillna(0)


def gn_ilr_vectorised(df, data_table, code_column, year_column, numerator_column, denominator_column, year_start, year_end):
    # Filter rows from data_table where the year is between year_start and year_end (inclusive)
    filtered_data = data_table[
        (data_table[year_column] >= year_start) &
        (data_table[year_column] <= year_end)
    ]

    # Group filtered data by code_column, summing values in numerator_column
    grouped_numerator = filtered_data.groupby(code_column)[numerator_column].sum()

    # Group filtered data by code_column, summing values in denominator_column
    grouped_denominator = filtered_data.groupby(code_column)[denominator_column].sum()

    # Calculate the ratio of numerator / denominator per code, replacing NaNs with 0 
   
    grouped_ratio = (grouped_numerator / grouped_denominator).where(grouped_denominator != 0, 0)

    # Map the ratios back onto df using 'risk_code' as the key
    # Missing codes are filled with 0
    return df["risk_code"].map(grouped_ratio).fillna(0)