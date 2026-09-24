# Note - uncertainty_helpers and anti_selection_helpers follow very similar formats - when updating, consider the other
import hx
import pandas as pd
import algorithms.rate_utilities as utils
import algorithms.anti_selection.anti_selection_notes as notes
from algorithms import rate_constants as constants


# Build the anti-selection matrix by evaluating each section's guideline and selected values
def build_anti_selection_matrix(hxd):
    # Map matrix section names to reference tables in HX
    refs_map = {
        'baseline':               hx.params.table_antiselection_1,
        'competing_portfolio':    hx.params.table_antiselection_2,
        'delegation_scope':       hx.params.table_antiselection_3,
        'quantity_quality':       hx.params.table_antiselection_4,
        'cover_holder_alignment': hx.params.table_antiselection_5,
        'participation':          hx.params.table_antiselection_6,
    }

    path_as     = hxd.cds.anti_selection
    path_mtx    = path_as.matrix
    requirement = path_as.charge_required

    # Initialize total sums for guideline and final values
    totals = {'min': 0, 'max': 0, 'suggested': 0, 'final': 0}

    # Process each section and compute guideline and selected values
    for name, df in refs_map.items():
        path_mtx_section = getattr(path_mtx, name)

        # Set section guideline min/max
        path_mtx_section.guideline_min = df["Charge"].min()
        path_mtx_section.guideline_max = df["Charge"].max()

        # Determine selected and suggested charge
        selection_value            = path_mtx_section.selection
        suggested                  = df.loc[df["Grade"] == selection_value, "Charge"].values[0]
        path_mtx_section.suggested = suggested

        # Compute final selected charge based on requirement
        path_mtx_section.final_selected.calculated = suggested if requirement else 0
        final_selected                             = path_mtx_section.final_selected.selected

        # Aggregate totals across sections
        totals['min']       += path_mtx_section.guideline_min
        totals['max']       += path_mtx_section.guideline_max
        totals['suggested'] += suggested
        totals['final']     += final_selected

    # force final total to be nil if uncertainty loading not required - YZ req 9-Feb
    totals['final'] = totals['final'] if requirement else 0

    # Assign overall totals to matrix
    overall = path_mtx.overall_selected
    overall.guideline_min             = totals['min']
    overall.guideline_max             = totals['max']
    overall.suggested                 = totals['suggested']
    overall.final_selected.calculated = totals['final']

    return totals['final']


# Add explanatory notes for UI
def add_charge_details(hxd):

    path_mtx    = hxd.cds.anti_selection.matrix

    # Map notes to each category
    notes_dict = {
        'baseline':                 notes.baseline_note,
        'competing_portfolio':      notes.competing_portfolio_note,
        'delegation_scope':         notes.delegation_scope_note,
        'quantity_quality':         notes.quantity_quality_note,
        'cover_holder_alignment':   notes.cover_holder_alignment_note,
        'participation':            notes.cover_holder_alignment_note,  # reused
        'overall_selected':         notes.overall_note
    }

    # Populate the details section with notes
    for name, note in notes_dict.items():
        path            = getattr(path_mtx, name)
        path.guidelines = note
    
    return


# Build the applied anti-selection charge based on weights and selections
def build_anti_selection_applied_charge(hxd, rater):
    applied_charge_path = hxd.cds.anti_selection.applied_charge
    applied_charge_df   = rater.get("anti_sel_applied_charge", pd.DataFrame())

    risk_code_composition_list = hxd.non_cds.risk_code_composition.final_composition

    # Skip if no composition data
    if len(risk_code_composition_list) == 0:
        return

    risk_code_composition_df = rater.get('risk_composition_final', pd.DataFrame())


    # Map unique LOBs to applied charge DataFrame
    unique_lobs = risk_code_composition_df["selected_lob"].unique()
    applied_charge_df.loc[:len(unique_lobs)-1, "selected_lob"] = unique_lobs
    applied_charge_df["is_row_visible"] = applied_charge_df["selected_lob"].notna()

    # Load model weight table
    model_weight_path = hxd.cds.rating_summary.model_gn_ulr.model_weights.table
    model_weights_df  = rater.get('rat_sum_mod_wgt', pd.DataFrame())

    follow_main_syndicate = hxd.cds.risk_information.follow_main_syndicate

    # Define projection column mappings
    projection_columns = {
        'own_performance': 'own_experience',
        'lloyds_performance': 'lloyds_proj',
        'beazley_performance': 'beazley_proj',
        'business_plan': 'bp_proj',
        'case_pricing': 'case_pricing',
    }

    if not follow_main_syndicate:
        # Map model weight projections for each LOB
        for target_col, source_col in projection_columns.items():
            lob_to_values_dict = dict(zip(model_weights_df['selected_lob'], model_weights_df[source_col]))
            applied_charge_df[target_col] = applied_charge_df['selected_lob'].map(lob_to_values_dict).fillna(0)
        applied_charge_df['pricing_2623_623'] = 0
    else:
        # Zero projections if following main syndicate; set pricing column
        for col in projection_columns.keys():
            applied_charge_df[col] = 0
        applied_charge_df['pricing_2623_623'] = 1

    # Compute weighted anti-selection charge
    model_weighting_values  = build_model_weighting(applied_charge_path)
    applied_charge_df       = calculate_anti_selection_charge(hxd, applied_charge_df, model_weighting_values)

    # Save updated DataFrame back to Hx
    cols_output =  ['selected_lob', 'is_row_visible', 'own_performance', 'lloyds_performance',
                    'beazley_performance', 'business_plan', 'case_pricing', 'pricing_2623_623']
    cols_override =['anti_selection_charge']
      
    rater['anti_sel_applied_charge'] = applied_charge_df[cols_output + cols_override]

    return

# Create a dictionary of model weighting factors
def build_model_weighting(applied_charge_path):
    model_weighting_path = applied_charge_path.model_weighting
   
    # Assign weights to Hx structure
    for col, value in constants.cols_to_value_dict.items():
        setattr(model_weighting_path, col, value)

    return constants.cols_to_value_dict


# Calculate the final anti-selection charge using weights and final selected charge
def calculate_anti_selection_charge(hxd, applied_charge_df, model_weighting_values):
    # Retrieve the overall final selected charge
    final_selected_charge = hxd.cds.anti_selection.matrix.overall_selected.final_selected.selected
    final_selected_charge = 0 if final_selected_charge is None else final_selected_charge

    # Multiply projection columns by weights and scale by final selected charge
    weights                                     = pd.Series(model_weighting_values)[model_weighting_values.keys()]
    calc_charge                                 = applied_charge_df[model_weighting_values.keys()].dot(weights) * final_selected_charge
    applied_charge_df['anti_selection_charge']  = applied_charge_df['anti_selection_charge'].fillna(calc_charge) # since when NOT overrriden it is NAN

    return applied_charge_df



