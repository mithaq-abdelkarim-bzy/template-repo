import hx
import pandas as pd
from algorithms import rate_constants as constants
from algorithms.rate_utilities import input_validation, interpolation_factor
from libraries.admitted_excess_premium.algorithms.parameter_tables.table_collections import (
    is_valid_date,
    filter_tables_by_date, 
    apply_schema_to_tables, 
    find_closest_date, 
    date_to_string,
    string_to_date,
    AdmittedExcessTables,
    get_all_tables)
from libraries.admitted_excess_premium.algorithms.rate_admitted_excess import load_and_prepare_data


##########################
#Admitted Excess additions
##########################

# admitted excess need to select tables by date
all_tables = get_all_tables('/workspace/editing/libraries/admitted_excess_premium/algorithms/parameter_tables')


def excess_attachement_factor_calculation(hxd):
    base_path = hxd.cds.admitted_excess
    
    primary_retention = base_path.primary_retention.value or 0
    excess_limit = base_path.excess_limit.value or 0
    excess_attachment = base_path.excess_attachment_point.value or 0

    admitted_excess_dataframes = load_and_prepare_data(hxd)

    df_ilf = admitted_excess_dataframes.excess_2_ilf

    df_singlelimit = admitted_excess_dataframes.excess_4_single_limit

    factor_table = df_ilf
    table_limit_interpolate = hx.params.table_limit_interpolate

    f_lower = "Average Lower"
    f_upper = "Average Upper"

    beazley_limit_attach_point_retention = primary_retention + excess_limit + excess_attachment
    beazley_attach_retention_interpolated_factor = interpolation_factor(beazley_limit_attach_point_retention, df_ilf, "Attachment Point Lower", "Attachment Point Upper", f_lower, factor_table, "Attachment Point Lower")
    
    attach_point_retention = primary_retention + excess_attachment
    attach_point_retention_interpolated_factor = interpolation_factor(attach_point_retention, df_ilf, "Attachment Point Lower", "Attachment Point Upper", f_lower, factor_table, "Attachment Point Lower")

    # (Beazley Limit + Attachment Point + Retention Interpolated Factor) - (Attachment Point plus Retention Interpolated Factor)
    excess_attachement_factor = beazley_attach_retention_interpolated_factor - attach_point_retention_interpolated_factor

    return excess_attachement_factor


def single_limit_factor_calculation(hxd):
    base_path = hxd.cds.admitted_excess
    policy_sharing_single_limit = 1 if base_path.no_of_policies_sharing_single_limit.value is None else base_path.no_of_policies_sharing_single_limit.value

    admitted_excess_dataframes = load_and_prepare_data(hxd)

    df_singlelimit = admitted_excess_dataframes.excess_4_single_limit

    table = df_singlelimit
    single_limit_factor = table.loc[table["Number of"] == policy_sharing_single_limit, "Single Limit Factor"].iloc[0]
    
    return single_limit_factor

def pro_rata_factor_calculation(hxd):

    # Date calculations
    inception_date = hxd.hx_core.inception_date or pd.Timestamp.now().date()  # Dummy date if no inception date
    one_year_from_inception = (inception_date + pd.DateOffset(years=1)).date()
    expiry_date = hxd.hx_core.expiry_date or one_year_from_inception
    pro_rata_factor = 1 + (
        (expiry_date - one_year_from_inception) / pd.Timedelta(days=365)
    )
    return pro_rata_factor    

def one_plus(node_value, default=0):
    return (node_value if node_value is not None else default) + 1 