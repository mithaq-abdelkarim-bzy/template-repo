import hx
import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils


def copy_composition_selection_table_to_manual(hxd):
    # Access the risk code composition object
    rcc = hxd.cds.risk_code_composition

    # Convert the "composition_selection" table (data-driven) into a pandas DataFrame
    composition_selection_df = utils.pd_df_from_hx_list(rcc.data_driven_composition.composition_selection.table)

    # removing "[blank]", replace didnt work as not the right "sentinel"
    cs_risk_code_ss = composition_selection_df['cs_risk_code']
    composition_selection_df['cs_risk_code'] = np.where(cs_risk_code_ss=='[blank]',None,cs_risk_code_ss)

    # Define which columns to copy into the manual composition table
    cs_output_cols_to_write = [
        "cs_risk_code",
        "cs_composition",
        "selected_lob",
        "model"
    ]

    # Drop any rows where the risk code is missing (avoid writing blank rows)
    filtered_df = composition_selection_df.dropna(subset=["cs_risk_code"])

    # Write the filtered data into the manual composition table
    # (this overwrites whatever is currently in the manual table)
    utils.write_pd_to_hxd(
        filtered_df[cs_output_cols_to_write],
        rcc.composition_manual.table,
        cs_output_cols_to_write
    )


def clear_manual_composition_table(hxd):
    """Clears all data from the manual composition table in risk code composition."""
    # Define which columns should be cleared
    cols = ['cs_risk_code', 'cs_composition', 'selected_lob']

    # Iterate over all attributes in the first row of the manual table
    for attr_name in dir(hxd.cds.risk_code_composition.composition_manual.table[0]):
        # If the attribute is one of the target columns
        if attr_name in cols:
            # Reset its value to None (effectively "clearing" it)
            setattr(
                hxd.cds.risk_code_composition.composition_manual.table[0],
                attr_name,
                None
            )