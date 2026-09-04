import hx
import pandas as pd
import polars as pl
import numpy as np



def extract_deductible_option(opt, fx_rate):
    """Return a dict of deductible types and values. Blank values if option missing."""
    if opt is None:
        return {
            "region":   "NA",
            "state":    "NA",
            "tier":     "NA",
            "perc":     0.0,
            "amt":      0.0,
            "type":     "",
            "sub":      0.0,
        }

    return {
        "region":   opt.region_dropdown.region  or "NA",
        "state":    opt.region_dropdown.state   or "NA",
        "tier":     opt.region_dropdown.tier    or "NA",
        "perc":     opt.percent or 0.0,
        "amt":      (opt.location_min_max or 0.0) / fx_rate,
        "type":     opt.type or "",
        "sub":      (opt.sublimit or 0.0) / fx_rate,
    }




def gather_peril_deductibles(layer, fx_rate, peril_key, num_options):
    """
    Return three option dicts, but populate only the first
    `num_options` real entries.  The rest are blank placeholders.
    """
    perils   = getattr(layer.perils, peril_key)

    opt_1 = perils.location_ded.option_1 if num_options >= 1 else None
    opt_2 = perils.location_ded.option_2 if num_options >= 2 else None
    opt_3 = perils.location_ded.option_3 if num_options >= 3 else None

    return [
        extract_deductible_option(opt_1, fx_rate),
        extract_deductible_option(opt_2, fx_rate),
        extract_deductible_option(opt_3, fx_rate)
    ]





def map_tier_columns(df, out_field, region_type, in_field, peril):
    """If tier is selected this function maps the selected tier to a generic column for use downstream"""
    if out_field not in df:
        df[out_field] = 0

    if region_type == "Tier":
        # Define a mapping dictionary for Infield values to corresponding DataFrame columns
        if peril == "ws":
            tier_mapping = {
                "Tier 1: TX - VA (Inc Harris)": 'Tier_1_TX_VA_Inc_Harris',
                "Tier 1: TX - VA (Exc Harris)": 'Tier_1_TX_VA_Exc_Harris',
                "Tier 1: TX - NC (Inc Harris)": 'Tier_1_TX_NC_Inc_Harris',
                "Tier 1: TX - NC (Exc Harris)": 'Tier_1_TX_NC_Exc_Harris',
                "Tier 1: TX - ME": 'Tier_1_TX_ME',
                "Tier 1: NorthEast": 'Tier_1_NorthEast',
                "Tier 2: TX - VA": 'Tier_2_TX_VA',
                "FL": 'FL',
                "FL Tri County Only": 'FL_Tri_County',
                "FL Tri County and Keys Only": 'FL_Tri_County_Keys',
                "Tier 1: FL": 'Tier_1_FL',
                "Tier 2: FL": 'Tier_2_FL'
            }
        elif peril == "eq":
            tier_mapping = {
                "South East": 'SouthEast_Quake',
                "Great Basin": 'GreatBasin_Quake',
                "NM": 'NM_Quake',
                "PNW Counties": 'PNW_Counties_Quake',
                "PNW": 'PNW_States_Quake',
                "CA A and B": 'CA_AB_Quake',
                "CA All Other": 'CA_AllOther_Quake'
            }
        else:
            raise ValueError("peril must be ws or eq")

        # Assign the appropriate column if Infield matches
        if in_field in tier_mapping:
            df[out_field] = df[tier_mapping[in_field]]


def add_deductible_info(df, outfield, region_type, state, value, tier_field):
    """Add deductible info to location data dependent on selection.Updates the dataframe in place.
    This function combines the three options into one with later options taken precedent over earlier ones.
    """
    if outfield not in df:
        df[outfield] = 0

    if region_type == "State":
        mask = df['Statecode'] == state
    elif region_type == "Tier":
        mask = df[tier_field] >= 1
    elif region_type == "All":
        mask = pd.Series([True] * len(df))
    else:
        mask = pd.Series([False] * len(df))

    df.loc[mask, outfield] = value
    return df


def apply_deductibles(df, peril, tiv_col, da_col, dp_col, type_col, outfield):
    """Applies deductibles to each location depending on deductible type. Modifies df in place."""

    if outfield not in df:
        df[outfield] = 0
    
    # Create a mask for rows matching the peril
    mask = df['Peril'] == peril

    # Initialize a Series to hold the computed deductible values
    ded_values = df[outfield].copy()

    # Apply logic based on deductible type
    percentage_min = df[type_col] == "Percentage with a $ minimum"
    fixed_amount = df[type_col] == "Fixed $ amount"
    uncapped = df[type_col] == "Percentage uncapped"
    capped = df[type_col] == "Percentage capped by $ amount"

    # Compute values for each type
    ded_values[mask & percentage_min] = np.maximum(df[da_col], df[dp_col] * df[tiv_col])
    ded_values[mask & fixed_amount] = df[da_col]
    ded_values[mask & uncapped] = df[dp_col] * df[tiv_col]
    ded_values[mask & capped] = np.minimum(df[da_col], df[dp_col] * df[tiv_col])
    ded_values[mask & ~(percentage_min | fixed_amount | uncapped | capped)] = 0 # Catch all

    # Assign the result back to the DataFrame
    df.loc[mask, outfield] = ded_values[mask]
    return df



def apply_sublimits(df, peril, sublimit_col):
    # Ensure  columns exist
    for col in ["SubLimit", "NoSubs"]:
        if col not in df:
            df[col] = 0

    mask = df['Peril'] == peril
    has_sublimit = df[sublimit_col] > 0

    # Apply sublimit where applicable
    df.loc[mask & has_sublimit, 'SubLimit'] = df.loc[mask & has_sublimit, sublimit_col]
    df.loc[mask & (df['SubLimit'] > 0), 'NoSubs'] = 1

    return df


def apply_per_occurrence_deductible(df, per_occ_ded: dict):
    """ This function applies the per occurance deductible to each event. 
    Assumes the 'Deductible' column already exists. """

    adjusted_expr = (
        pl.concat_list([
            pl.col("Deductible"),
            pl.col("Peril").map_dict(per_occ_ded, default=0.0)
        ])
        .arr.max()
        .alias("Deductible")
    )

    return df.with_columns(adjusted_expr)



def loss_to_layer(df, excess, limit, peril_sublimits: dict, elt_basis):
    """ Calculates the expected loss to the layer """

    lim = pl.lit(limit)
    exc = pl.lit(excess)
    inf = pl.lit(np.inf)

    if elt_basis == "GR":
        net_loss = (pl.col("Loss") - exc).clip_min(0)
        
        layer_loss = (
            pl.concat_list([net_loss, lim])
            .arr.min()
            .alias("LayerLoss")
        )

    else: ## assumes GU ELT
        peril_sub = pl.col("Peril").map_dict(peril_sublimits, default=0)

        net_loss = (pl.col("Loss") - (pl.col("Deductible") + exc)).clip_min(0)

        sub_adj = (
            pl.when(pl.col("SubLimit") == 0)
            .then(inf)
            .otherwise(pl.col("SubLimit"))
            - exc
        ).clip_min(0)

        peril_adj = (
            pl.when(peril_sub == 0)
            .then(inf)
            .otherwise(peril_sub)
            - exc
        ).clip_min(0)

        # single row-wise minimum across all four possible caps
        layer_loss = (
            pl.concat_list([net_loss, sub_adj, peril_adj, lim])
            .arr.min()
            .alias("LayerLoss")
        )

    return df.with_columns(layer_loss)


