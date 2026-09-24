# Note - 
# uncertainty_helpers and anti_selection_helpers follow very similar formats - when updating, consider the other
# Could move hardcoded values in process_manual_sections to constants page

import hx
import pandas as pd
import algorithms.rate_utilities as utils
import algorithms.uncertainty.uncertainty_notes as notes


# Build the uncertainty matrix by computing guideline, suggested, and final loads
def build_uncertainty_matrix(hxd):
    # Map matrix section names to reference tables in HX
    refs_map = {
        'quantity':                 hx.params.table_uncertainty_1,
        'quality':                  hx.params.table_uncertainty_2,
        'new_or_existing_facility': hx.params.table_uncertainty_3,
        'perf_volatility':          hx.params.table_uncertainty_4,
        'reliance_on_ext_modelling':hx.params.table_uncertainty_5,
    }

    path_unc    = hxd.cds.uncertainty
    path_mtx    = path_unc.matrix
    requirement = path_unc.charge_required

    # Initialize total sums for guideline and final values
    totals = {'min': 0, 'max': 0, 'suggested': 0, 'final': 0}

    # Iterate through each uncertainty factor and compute section values
    for name, df in refs_map.items():
        path_mtx_section = getattr(path_mtx, name)
     
        # Set section guideline min/max
        path_mtx_section.guideline_min = guideline_min = df["Charge"].min()
        path_mtx_section.guideline_max = guideline_max = df["Charge"].max()

        # Determine selected and suggested charge
        selection_value                        = path_mtx_section.selection
        path_mtx_section.suggested = suggested = df.loc[  df["Grade"] == selection_value  , "Charge"].values[0]

        # Compute final selected charge based on requirement
        path_mtx_section.final_selected.calculated = suggested if requirement else 0
        final_selected                             = path_mtx_section.final_selected.selected

        # Aggregate totals across sections
        totals['min']       += guideline_min
        totals['max']       += guideline_max
        totals['suggested'] += suggested
        totals['final']     += final_selected

    # Apply manual adjustments such as subjectivity and performance discount
    totals  = process_manual_sections(path_mtx, totals)

    # force final total to be nil if uncertainty loading not required - YZ req 9-Feb
    totals['final'] = totals['final'] if requirement else 0

    # Update overall matrix totals
    overall = path_mtx.overall_selected
    overall.guideline_min   = totals['min']
    overall.guideline_max   = totals['max']
    overall.suggested       = totals['suggested']
    
    overall.final_selected.calculated = totals['final']

    return totals


# Add explanatory notes for UI
def add_load_details(hxd):
    path_mtx    = hxd.cds.uncertainty.matrix

    notes_dict = {
        'quantity':                 notes.quantity_notes,
        'quality':                  notes.quality_notes,
        'new_or_existing_facility': notes.new_or_existing_facility_notes,
        'perf_volatility':          notes.perf_volatility_notes,
        'reliance_on_ext_modelling':notes.reliance_on_ext_modelling_notes
    }

    # Populate the details section with notes
    for name, note in notes_dict.items():
        path            = getattr(path_mtx, name)
        path.guidelines = note

    # Add notes for requirement and manual adjustments
    path_mtx.overall_selected.guidelines   = notes.requirement_notes
    path_mtx.add_subjectivity.guidelines   = notes.add_subjectivity_notes
    path_mtx.perf_discount.guidelines      = notes.perf_discount_notes
    
    return


# Populate and adjust manual sections like subjectivity and performance discount
def process_manual_sections(path_mtx, totals):
    manual_sections = {
        'add_subjectivity': {'guideline_min':     0, 'guideline_max':  0.05, 'suggested': 0, 'final_selected': 0},
        'perf_discount':    {'guideline_min': -0.05, 'guideline_max':     0, 'suggested': 0, 'final_selected': 0}
    }

    for name, vals in manual_sections.items():
        s = getattr(path_mtx, name)

        s.guideline_min             = vals['guideline_min']
        totals['min']              += vals['guideline_min']        
        
        s.guideline_max             = vals['guideline_max']
        totals['max']              += vals['guideline_max']

        s.suggested                 = vals['suggested']
        totals['suggested']        += vals['suggested']

        s.final_selected.calculated = vals['final_selected']
        final_selected              = s.final_selected.override if s.final_selected.is_overridden else s.final_selected.calculated
        totals['final']            += final_selected

    return totals


# Build the applied uncertainty charge using projections and model weights
def build_uncertainty_applied_charge(hxd,rater):
    applied_charge_path = hxd.cds.uncertainty.applied_charge
    applied_charge_df   = rater.get("uncertainty_applied_charge", pd.DataFrame())

    # Return early if no risk code composition exists
    risk_code_composition_list = hxd.non_cds.risk_code_composition.final_composition
    if len(risk_code_composition_list) == 0:
        return

    risk_code_composition_df = rater.get('risk_composition_final', pd.DataFrame())

    # Assign selected lines of business to the applied charge table
    unique_lobs = risk_code_composition_df["selected_lob"].unique()
    applied_charge_df.loc[:len(unique_lobs)-1, "selected_lob"] = unique_lobs
    applied_charge_df["is_row_visible"] = applied_charge_df["selected_lob"].notna()

    model_weight_path = hxd.cds.rating_summary.model_gn_ulr.model_weights.table
    model_weights_df  = rater.get('rat_sum_mod_wgt', pd.DataFrame())
    follow_main_syndicate = hxd.cds.risk_information.follow_main_syndicate

    # Map projection values depending on whether following main syndicate
    projection_columns = {
        'own_performance': 'own_experience',
        'lloyds_performance': 'lloyds_proj',
        'beazley_performance': 'beazley_proj',
        'business_plan': 'bp_proj',
        'case_pricing': 'case_pricing',
    }

    if not follow_main_syndicate:
        for target_col, source_col in projection_columns.items():
            lob_to_values_dict = dict(zip(model_weights_df['selected_lob'], model_weights_df[source_col]))
            applied_charge_df[target_col] = applied_charge_df['selected_lob'].map(lob_to_values_dict).fillna(0)
        applied_charge_df['pricing_2623_623'] = 0
    else:
        for col in projection_columns.keys():
            applied_charge_df[col] = 0
        applied_charge_df['pricing_2623_623'] = 1

    # Apply model weights and calculate final uncertainty load
    model_weighting_values = build_model_weighting(applied_charge_path)
    applied_charge_df = calculate_uncertainty_charge(hxd, applied_charge_df, model_weighting_values)

    # Save results to rater
    rater["uncertainty_applied_charge"] = applied_charge_df


# Assign default weights for each projection column
def build_model_weighting(applied_charge_path):
    model_weighting_path = applied_charge_path.model_weighting
    cols_to_value_dict = {col: 1 for col in [
        'own_performance', 'lloyds_performance', 'beazley_performance',
        'business_plan', 'case_pricing', 'pricing_2623_623']}
    
    for col, value in cols_to_value_dict.items():
        setattr(model_weighting_path, col, value)

    return cols_to_value_dict


# Calculate final uncertainty load using weighted projections and final selected matrix value
def calculate_uncertainty_charge(hxd, applied_charge_df, model_weighting_values):
    # Retrieve the overall final selected charge
    final_selected_charge     = hxd.cds.uncertainty.matrix.overall_selected.final_selected.selected
    final_selected_charge     = 0 if final_selected_charge is None else final_selected_charge
    
    # Multiply projection columns by weights and scale by final selected charge
    weights                   = pd.Series(model_weighting_values)[model_weighting_values.keys()]
    calc_charge               = applied_charge_df[model_weighting_values.keys()].dot(weights) * final_selected_charge
    applied_charge_df['load'] = applied_charge_df['load'].fillna(calc_charge) # since when NOT overrriden it is NAN

    return applied_charge_df


