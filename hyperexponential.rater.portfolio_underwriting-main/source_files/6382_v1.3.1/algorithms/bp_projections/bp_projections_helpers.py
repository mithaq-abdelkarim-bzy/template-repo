import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms.risk_information.risk_information_helpers import import_inception_date


def set_is_tab_shown(hxd):
    # Get flag for whether main syndicate is not followed
    not_follow_main_syndicate = hxd.non_cds.risk_information.not_follow_main_syndicate  

    # Get the pricing source
    priced_by = hxd.cds.risk_information.priced_by  

    # Show BP projections tab only if priced by Actuarial and not following main syndicate
    if priced_by == "Actuarial" and not_follow_main_syndicate:
        hxd.non_cds.bp_projections.is_shown = True  


def init_bp_summary_by_lob(hxd, bp_details_df,rater):
    # Initialize empty DataFrame for Table 2 summary
    bp_summary_by_lob_df = pd.DataFrame({})

    # Extract unique LOBs and align summary DataFrame length  
    unique_selected_lob = bp_details_df['selected_lob'].unique()
    bp_summary_by_lob_df = pd.DataFrame({'selected_lob': unique_selected_lob})

    # Mark rows as visible if LOB is not null
    bp_summary_by_lob_df["is_row_visible"] = bp_summary_by_lob_df["selected_lob"].notna()

    # Map tracker_class values from details to summary
    bp_summary_by_lob_df['tracker_class'] = bp_summary_by_lob_df['selected_lob'].map(
        dict(zip(bp_details_df['selected_lob'], bp_details_df['tracker_class']))
    ).fillna('')

    # Aggregate composition sums per LOB
    composition_sums = bp_details_df.groupby('selected_lob')['composition'].sum()
    bp_summary_by_lob_df['composition'] = bp_summary_by_lob_df['selected_lob'].map(composition_sums).fillna(0)

    # Define columns that require weighted average calculation
    columns_to_process = [
        'acc_aquisition_costs', 'attr_base_gn_ulr', 'attr_inflation_1_year',
        'attr_rate_change', 'attr_rarc_margin', 'attr_portfolio_change',
        'cat_base_gn_ulr', 'cat_inflation_1_year', 'cat_rate_change',
        'cat_rarc_margin', 'cat_climate_change', 'cat_nmp_general',
        'cat_nmp_all_other'
    ]

    # Compute weighted averages for each selected column
    for col in columns_to_process:
        # Multiply composition by column value
        bp_details_df["product"] = bp_details_df["composition"] * bp_details_df[col].fillna(0)

        # Aggregate product sums per LOB
        product_sums = bp_details_df.groupby('selected_lob')['product'].sum()

        # Map aggregated product back to summary DataFrame
        bp_summary_by_lob_df['product'] = bp_summary_by_lob_df['selected_lob'].map(product_sums).fillna(0)

        # Compute weighted average = product sum / composition sum        
        bp_summary_by_lob_df[col] = (
            bp_summary_by_lob_df["product"] / bp_summary_by_lob_df["composition"]
        ).where(bp_summary_by_lob_df["composition"] != 0, 0)
        
    return bp_summary_by_lob_df


def init_bp_details(hxd,  rater):
    # Load Table 3 details DataFrame
    risk_code_final_composition_df = rater["risk_composition_final"]
    deductions_final_df            = rater["deductions_df"]
    bp_details_df                  = rater["bp_details"]

    # Load business plan parameters
    business_plan_df = import_business_plan_df(hxd)    

    # Initialize Table 3 from final composition data
    bp_details_df = init_bp_details_from_final_composition(bp_details_df, risk_code_final_composition_df)

    # Map acquisition costs from deductions data
    bp_details_df['acc_aquisition_costs'] = bp_details_df['selected_lob'].map(
        dict(zip(deductions_final_df['selected_lob'], deductions_final_df['selected_effective_deductions']))
    )

    # Map business plan attributes into Table 3
    bp_details_df = map_data_from_business_plan(bp_details_df, business_plan_df)
  
    return bp_details_df


def import_business_plan_df(hxd):
    business_plan_df = hx.params.table_business_plan

    min_year = business_plan_df["year"].min()
    max_year = business_plan_df["year"].max()
    
    inception_date = import_inception_date(hxd)
    inception_year = inception_date.year

    selected_year = pd.Series([min_year, max_year, inception_year]).median()

    filtered_bp_df = business_plan_df.loc[business_plan_df["year"] == int(selected_year)]

    return filtered_bp_df


def build_bp_summary_by_lob(hxd, bp_details_df, bp_summary_by_lob_df):
    # BP Summary by LoB: Aggregates data at the selected LOB level

    # Columns requiring weighted aggregation
    columns_to_process = [
        'selected_attr_gn_ulr', 
        'selected_cat_gn_ulr', 
        'total_gn_ulr', 
        'bp_acquisition_costs', 
        'adj_attr_gn_ulr', 
        'adj_cat_gn_ulr',
        'adj_total_gn_ulr'
    ]

    # Compute weighted averages for each column at LOB level
    for col in columns_to_process + ['rate_change_override', 'adj_attr_gn_ulr', 'adj_cat_gn_ulr']:
        product = (bp_details_df.groupby('selected_lob')
                                .apply(lambda row: (row[col] * row['composition'])
                                .sum()                                            ).to_dict())
        
        # Divide by total composition per LOB to get weighted average
        bp_summary_by_lob_df[col] = bp_summary_by_lob_df.apply(
            lambda row: product.get(row['selected_lob'], 0) / row['composition'] if row['composition'] != 0 else 0, axis=1
        )

    return bp_summary_by_lob_df


def build_bp_details(hxd, bp_details, rate_change_df):
    # BP Details: Core table for BP projections calculations

    # Apply rate change and ULR calculations in sequence
    bp_details = calculate_rate_change_override(bp_details, rate_change_df)
    bp_details = calculate_selected_attr_gn_ulr(bp_details)
    bp_details = calculate_selected_cat_gn_ulr(bp_details)
    bp_details = calculate_total_gn_ulr(bp_details)
    bp_details = calculate_adj_gn_ulr(bp_details, is_attr=True)
    bp_details = calculate_adj_gn_ulr(bp_details, is_attr=False)
    bp_details = calculate_adj_total_gn_ulr(bp_details)

    return bp_details


def calculate_adj_total_gn_ulr(bp_details_df):
    # Sum adjusted attr and cat GN ULR to calculate total adjusted GN ULR
    bp_details_df['adj_total_gn_ulr'] = bp_details_df['adj_attr_gn_ulr'] + bp_details_df['adj_cat_gn_ulr']

    # Replace NaN values with 0
    bp_details_df['adj_total_gn_ulr'] = bp_details_df['adj_total_gn_ulr'].fillna(0)
    return bp_details_df


def calculate_adj_gn_ulr(bp_details_df, is_attr=True):
    # Select appropriate column names depending on attr or cat
    selected_col_name = 'selected_attr_gn_ulr' if is_attr else 'selected_cat_gn_ulr'
    adj_col_name = 'adj_attr_gn_ulr' if is_attr else 'adj_cat_gn_ulr'
    
    # Calculate adjusted GN ULR where required values are present
    bp_details_df[f"{adj_col_name}/calculated"] = 0

    valid_denominator_mask =  (1 - bp_details_df['acc_aquisition_costs']) != 0

    bp_details_df.loc[valid_denominator_mask, f"{adj_col_name}/calculated"] = (
        bp_details_df.loc[valid_denominator_mask, selected_col_name] 
        * (1 - bp_details_df.loc[valid_denominator_mask, 'bp_acquisition_costs']) 
        / (1 - bp_details_df.loc[valid_denominator_mask, 'acc_aquisition_costs'])
    )
    
    # Apply overrides if flagged, otherwise use calculated values
    bp_details_df[f"{adj_col_name}"] = np.where(
        bp_details_df[f"{adj_col_name}/is_overridden"],
        bp_details_df[f"{adj_col_name}"].fillna(0),
        bp_details_df[f"{adj_col_name}/calculated"],
    )
    
    # Ensure numeric type and replace NaN with None
    bp_details_df[adj_col_name] = pd.to_numeric(bp_details_df[adj_col_name], errors='coerce')
    bp_details_df[adj_col_name] = np.where(np.isnan(bp_details_df[adj_col_name]), None, bp_details_df[adj_col_name])
    
    return bp_details_df


def calculate_total_gn_ulr(bp_details_df):
    # Calculate total GN ULR by summing attr and cat GN ULR
    bp_details_df['total_gn_ulr'] = np.where(
        bp_details_df[['selected_attr_gn_ulr', 'selected_cat_gn_ulr']].isnull().all(axis=1),
        None,
        bp_details_df['selected_attr_gn_ulr'].fillna(0) + bp_details_df['selected_cat_gn_ulr'].fillna(0)
    )
    return bp_details_df


def calculate_selected_cat_gn_ulr(bp_details_df):
    # Compute denominators for rate change handling
    override_denom = (1 + bp_details_df['rate_change_override']).replace(0, np.nan)
    cat_rate_change_denom = (1 + bp_details_df['cat_rate_change']) / (1 + bp_details_df['cat_rarc_margin'])
    cat_rate_change_denom = cat_rate_change_denom.replace(0, np.nan)
    
    # Compute selected_cat_gn_ulr using inflation, rate changes, and overrides
    bp_details_df['selected_cat_gn_ulr'] = np.where(
        bp_details_df['rate_change_override'] == -1,
        None,
        bp_details_df['cat_base_gn_ulr'] * (1 + bp_details_df['cat_inflation_1_year']) /
        np.where(bp_details_df['rate_change_override'].isnull(), cat_rate_change_denom, override_denom)
    )
    return bp_details_df


def calculate_selected_attr_gn_ulr(bp_details_df):
    # Compute denominators for attr GN ULR
    override_denom = (1 + bp_details_df['rate_change_override']).replace(0, np.nan)
    rate_change_denom = (1 + bp_details_df['attr_rate_change']).replace(0, np.nan) / \
        (1 + bp_details_df['attr_rarc_margin']).replace(0, np.nan)
    
    # Compute selected_attr_gn_ulr using inflation, rate changes, portfolio changes, and overrides
    bp_details_df['selected_attr_gn_ulr'] = np.where(
        bp_details_df['rate_change_override'] == -1,
        None,
        bp_details_df['attr_base_gn_ulr'] * (1 + bp_details_df['attr_inflation_1_year']) /
        np.where(bp_details_df['rate_change_override'].isnull(), rate_change_denom, override_denom) *
        (1 + bp_details_df['attr_portfolio_change'])
    )
    return bp_details_df


def calculate_rate_change_override(bp_details_df, rate_change_df):
    # Map rate change source by LOB
    bp_details_df['rate_change_source_by_lob'] = bp_details_df['selected_lob'].map(
        dict(zip(rate_change_df['selected_lob'], rate_change_df['year_0/source']))).fillna('')
    
    # Build mapping of LOB to selected rate change
    rate_change_mapping = dict(zip(rate_change_df['selected_lob'], rate_change_df['year_0/selected']))
    
    # Calculate rate_change_override only for Facility/Blend sources
    bp_details_df['rate_change_override/calculated'] = np.where(
        bp_details_df['rate_change_source_by_lob'].isin(["Facility", "Blend"]),
        bp_details_df['selected_lob'].map(rate_change_mapping) - 1,
        None
    )
    
    # Apply override flag or use calculated values
    bp_details_df['rate_change_override'] = np.where(
        bp_details_df['rate_change_override/is_overridden'],
        bp_details_df['rate_change_override'],
        bp_details_df['rate_change_override/calculated']
    )
    
    # Convert to numeric, replace NaN with None
    bp_details_df['rate_change_override'] = pd.to_numeric(bp_details_df['rate_change_override'], errors='coerce')
    bp_details_df['rate_change_override'] = np.where(np.isnan(bp_details_df['rate_change_override']), None, bp_details_df['rate_change_override'])

    # Drop rows with missing acquisition costs since table is reloaded
    bp_details_df = bp_details_df.dropna(subset=['acc_aquisition_costs'])
    return bp_details_df


def map_data_from_business_plan(bp_details_df, business_plan_df):
    # Mapping between business_plan_df columns and bp_details_df columns
    business_plan_to_bp_details_cols_map = {
        'attr_base': 'attr_base_gn_ulr',
        'attr_inflation': 'attr_inflation_1_year',
        'attr_rate_change': 'attr_rate_change',
        'attr_rarc_margin': 'attr_rarc_margin',
        'attr_portfolio_change': 'attr_portfolio_change',
        'cat_base': 'cat_base_gn_ulr',
        'cat_inflation': 'cat_inflation_1_year',
        'cat_rate_change': 'cat_rate_change',
        'cat_rarc_margin': 'cat_rarc_margin',
        'cat_climate_change': 'cat_climate_change',
        'cat_non_modelled_perils_general': 'cat_nmp_general',
        'cat_non_modelled_perils_all_other': 'cat_nmp_all_other',
        'bp_expenses': 'bp_acquisition_costs'
    }
    
    # For each mapped column, pull values from business_plan_df and assign to bp_details_df
    for bp_col, table_col in business_plan_to_bp_details_cols_map.items():
        bp_details_df[table_col] = bp_details_df['bp_class'].map(
            dict(zip(business_plan_df['business_plan_class'], business_plan_df[bp_col]))
        ).fillna(0)
    
    return bp_details_df


def init_bp_details_from_final_composition(bp_details_df, risk_code_final_composition_df):
    # Align number of rows in bp_details_df with final composition - resetting index to cater for filtered rows
    # bp_details_df = bp_details_df[:risk_code_final_composition_df.shape[0]]
    
    bp_details_df                  = bp_details_df.reset_index(drop=True)
    risk_code_final_composition_df = risk_code_final_composition_df.reset_index(drop=True)
    bp_details_df                  = bp_details_df.reindex(range(len(risk_code_final_composition_df)))
    
    # Assign core attributes from risk_code_final_composition_df
    bp_details_df = bp_details_df.assign(
        tracker_class=risk_code_final_composition_df["selected_trifocus"],
        selected_lob=risk_code_final_composition_df["selected_lob"],
        risk_code=risk_code_final_composition_df["risk_code"],
        composition=risk_code_final_composition_df["composition"],
        is_row_visible=risk_code_final_composition_df["selected_trifocus"].notna()
    )
        
    # Calculate bp_class, applying overrides if present
    bp_details_df["bp_class/calculated"] = risk_code_final_composition_df["selected_bp_class"]
    bp_details_df["bp_class"] = np.where(
        bp_details_df["bp_class/is_overridden"],
        bp_details_df["bp_class"],
        bp_details_df["bp_class/calculated"]
    )

    # Handle missing values in rate_change_override by temporarily filling and resetting
    bp_details_df["rate_change_override/calculated"] = bp_details_df["rate_change_override"].fillna("TEMP")
    bp_details_df.loc[bp_details_df["rate_change_override/calculated"] == "TEMP", "rate_change_override"] = None
    
    return bp_details_df

