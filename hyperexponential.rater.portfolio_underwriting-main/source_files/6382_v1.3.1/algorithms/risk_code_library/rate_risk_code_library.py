import pandas as pd
import hx
import algorithms.rate_utilities as utils
import numpy as np
from algorithms.risk_code_library.risk_code_library_helpers import (
    set_do_we_model,
    latest_year_premium_vectorised,
    gn_ilr_vectorised
)
from algorithms import rate_constants as constants

def rate_risk_code_library(hxd, rater):

    # Pull year range settings from hxd config
    year_start  = hxd.cds.year_start
    year_end    = hxd.cds.year_end

    # Load static data
    lloyds_data         = hx.params.table_lloyds_risk_code_data
    lloyds_risk_codes   = hx.params.table_lloyds_risk_code
    beazley_data_new    = hx.params.table_beazley_data
    df                  = hx.params.table_lloyds_risk_code_desc

   
    # Define original column names as they appear in the raw Lloyd's risk codes table
    mapping = { 'RiskCode'                          : "risk_code",
                'High Level Class of Business'      : "high_level_cob",
                'Generic Class of Business'         : "generic_cob",
                'Type of Placement'                 : "type_of_placement",
                'Risk Code Description'             : "risk_code_description",
                'Risk Code Description - Expanded'  : "risk_code_explained",
                'OECD Class Mapping'                : "oecd_class_mapping",
                'Assigned Tracker'                  : "assigned_tracker",
                'Assigned BP Class'                 : "assigned_bp_class",    }

    # Apply renaming so downstream code uses standardized column names
    df = df.rename(columns=mapping)

    # ------------------------
    # Calculate Lloyd's metrics
    # ------------------------
    m = constants.risk_code_library_multiplying_factor
    df["gnpi_lloyds"]    = latest_year_premium_vectorised( df, lloyds_data, "lloyds_risk_code", "yoa", "gnpi",                      m,     year_start, year_end  )
    df["incured_lloyds"] = latest_year_premium_vectorised( df, lloyds_data, "lloyds_risk_code", "yoa", "latest_incurred_position",  m,     year_start, year_end  )
    df["gn_ilr_lloyds"]  = gn_ilr_vectorised(              df, lloyds_data, "lloyds_risk_code", "yoa", "latest_incurred_position", "gnpi", year_start, year_end    )

    # Add a "do_we_model" column based on whether the risk code exists in the Lloyd's list
    lloyds_risk_codes_list = lloyds_risk_codes['Lloyds Risk Code'].tolist()
    df                     = set_do_we_model(df, lloyds_risk_codes_list, lloyds_data)

    # -------------------------
    # Calculate Beazley metrics
    # -------------------------
    df["gnpi_beazley"]      = latest_year_premium_vectorised(       df, beazley_data_new, "risk_code", "yoa", "gn_written_premium", 1,                year_start, year_end    )
    df["incurred_beazley"]  = latest_year_premium_vectorised(       df, beazley_data_new, "risk_code", "yoa", "incurred_total",     1,                year_start, year_end    )
    df["gn_ilr_beazley"]    = gn_ilr_vectorised(                    df, beazley_data_new, "risk_code", "yoa", "incurred_total", "gn_written_premium", year_start, year_end    )


    # -------------------------
    # Persist results
    # -------------------------

    # Also save the DataFrame into the rater dictionary
    rater["risk_code_library_df"] = df