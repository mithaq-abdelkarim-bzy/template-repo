import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
import bisect


def map_dwt_bands(
    lower_band, upper_band, max_lower_band=50001, max_upper_band=999999999
):
    if lower_band == max_lower_band and upper_band == max_upper_band:
        return "50001+"
    return f"{lower_band} to {upper_band}"


def map_age_bands(lower_band, upper_band, max_lower_band=50, max_upper_band=999):
    if lower_band == max_lower_band and upper_band == max_upper_band:
        return "50+"
    return f"{lower_band} to {upper_band}"


def get_vessel_analysis_criteria_percentage(
    vessel_type, coverage_factor, vessels_percentile_table, achieved_rate, commission
):
    if commission == 1:
        return None, None, None, None

    filtered_df = vessels_percentile_table[
        vessels_percentile_table["vessel_type"] == vessel_type
    ]

    if filtered_df.empty:
        return None, None, None, None

    # Select the single row (assuming there is only one row for the given vessel_type)
    row = filtered_df.iloc[0]

    # List of columns to exclude
    exclude_columns = ["vessel_type", "count"]

    # Select columns to be analyzed
    columns_to_analyze = row.index.difference(exclude_columns)

    # Multiply the values in the selected columns by the multiplier
    row[columns_to_analyze] = (
        row[columns_to_analyze] * coverage_factor / (1 - commission)
    )

    # Calculate max and min values for the selected columns
    max_value = row[columns_to_analyze].max()
    min_value = row[columns_to_analyze].min()

    # Count values greater than achieved_rate
    count_greater_than_achieved_rate = (
        row[columns_to_analyze] > achieved_rate
    ).sum() / 100
    vessels_count = row["count"]

    return max_value, min_value, count_greater_than_achieved_rate, vessels_count


"""
3 behaviours:
1. If the achieved rate is less than the minimum rate, the pre list is set with the min. from the table and the max is empty
2. If the achieved rate is greater than the maximum rate, the post list is set with the max. from the table and the min is empty
3. If the achieved rate is between the min and max, the pre list is set with the min. from the table along with the achieved rate and the post list is set with the max. from the table
"""


def rate_vessel_analysis(hxd):
    if not hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        return
    vessels = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list
    drop_down_info_list = []
    const_y = 0.02
    criteria_list = ["type", "type_age", "type_age_dwt"]
    chosen_vessel = None
    # Filler values for a better UI
    for criteria in criteria_list:
        pre_list = [
            {
                f"vessel_analysis_pre_{criteria}": 0,
                "constant_pre_y": const_y,
            }
        ]
        post_list = [
            {
                f"vessel_analysis_post_{criteria}": 1,
                "constant_post_y": const_y,
            }
        ]
        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessel_pre_{criteria}_list",
            pre_list,
        )
        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessel_post_{criteria}_list",
            post_list,
        )
    for vessel in vessels:
        drop_down_info_list.append(
            {
                "drop_down_imo": vessel.vessel_details.imo,
                "drop_down_name": vessel.vessel_details.name,
            }
        )
        if (
            vessel.vessel_details.imo
            == hxd.cds.vessel_analysis.hull_rating.imo_and_name.vessel_analysis_imo
        ):
            chosen_vessel = vessel
    hxd.cds.vessel_analysis.hull_rating.drop_down_info = drop_down_info_list
    if chosen_vessel is None:
        return

    modelling_list = hxd.cds.exposure.granular.vessels.hull_rating.modelling_list
    coverage_factor = 0
    for vessel in modelling_list:
        if vessel.modelling_imo == chosen_vessel.vessel_details.imo:
            coverage_factor = vessel.static_coverage_factor
            break

    vessel_type = chosen_vessel.vessel_type
    if not vessel_type:
        return
    coverage_factor = coverage_factor
    achieved_rate = chosen_vessel.achieved_rate
    commission = hxd.cds.layers[0].coverages.hull.brokerage
    if (achieved_rate is None) or (commission is None) or (coverage_factor is None):
        return

    hxd.cds.vessel_analysis.hull_rating.vessel_analysis_achieved_rate = achieved_rate

    age_bands = hx.params.table_age_bands
    dwt_bands = hx.params.table_dwt_bands

    lower_age_bands = age_bands["lower_age_band"].tolist()
    upper_age_bands = age_bands["upper_age_band"].tolist()

    lower_dwt_bands = dwt_bands["lower_dwt_band"].tolist()
    upper_dwt_bands = dwt_bands["upper_dwt_band"].tolist()

    age_bands = None
    year_built = chosen_vessel.year_built
    inception_date = chosen_vessel.inception_date
    if year_built and inception_date:
        age = max(inception_date.year - year_built, 0)
        # Use binary search to find the insertion point
        idx = bisect.bisect_right(lower_age_bands, age) - 1
        if idx >= 0 and lower_age_bands[idx] <= age <= upper_age_bands[idx]:
            age_bands = map_age_bands(
                lower_age_bands[idx],
                upper_age_bands[idx],
                lower_age_bands[-1],
                upper_age_bands[-1],
            )

    dwt_bands = None
    dwt = chosen_vessel.dwt
    if dwt:
        # Use binary search to find the insertion point
        idx = bisect.bisect_right(lower_dwt_bands, dwt) - 1
        if idx >= 0 and lower_dwt_bands[idx] <= dwt <= upper_dwt_bands[idx]:
            dwt_bands = map_dwt_bands(
                lower_dwt_bands[idx],
                upper_dwt_bands[idx],
                lower_dwt_bands[-1],
                upper_dwt_bands[-1],
            )

    hxd.cds.vessel_analysis.hull_rating.vessel_analysis_vessel_type_age_dwt_table.vessel_analysis_vessel_type = (
        f"{vessel_type}"
    )

    hxd.cds.vessel_analysis.hull_rating.vessel_analysis_vessel_type_age_dwt_table.vessel_analysis_age_range = (
        f"{age_bands}"
    )

    hxd.cds.vessel_analysis.hull_rating.vessel_analysis_vessel_type_age_dwt_table.vessel_analysis_dwt_range = (
        f"{dwt_bands}"
    )

    for criteria in criteria_list:
        curr_vessel_type = vessel_type
        if criteria == "type_age":
            if not age_bands:
                continue
            curr_vessel_type = f"{vessel_type}{age_bands}"

        elif criteria == "type_age_dwt":
            if not age_bands or not dwt_bands:
                continue
            curr_vessel_type = f"{vessel_type}{age_bands}{dwt_bands}"

        vessels_percentile_table = getattr(
            hx.params, f"table_vessel_percentile_{criteria}"
        )
        max_value, min_value, count_greater_than_achieved_rate, vessels_count = (
            get_vessel_analysis_criteria_percentage(
                curr_vessel_type,
                coverage_factor,
                vessels_percentile_table,
                achieved_rate,
                commission,
            )
        )
        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessels_{criteria}_count",
            vessels_count if vessels_count and vessels_count > 0 else 0,
        )

        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessels_{criteria}_higher_rate",
            (
                count_greater_than_achieved_rate
                if count_greater_than_achieved_rate
                and count_greater_than_achieved_rate > 0
                else 0
            ),
        )
        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessels_{criteria}_lower_rate",
            (
                (1 - count_greater_than_achieved_rate)
                if count_greater_than_achieved_rate
                else 1
            ),
        )

        post_list = []
        pre_list = [
            {
                f"vessel_analysis_pre_{criteria}": 0,
                "constant_pre_y": const_y,
            }
        ]
        if achieved_rate <= (max_value or 0):
            post_list.append(
                {
                    f"vessel_analysis_post_{criteria}": max_value,
                    "constant_post_y": const_y,
                }
            )

        if achieved_rate >= (min_value or 0):
            pre_list = [
                {
                    f"vessel_analysis_pre_{criteria}": min_value,
                    "constant_pre_y": const_y,
                },
                {
                    f"vessel_analysis_pre_{criteria}": achieved_rate,
                    "constant_pre_y": const_y,
                },
            ]

        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessel_pre_{criteria}_list",
            pre_list,
        )
        setattr(
            hxd.cds.vessel_analysis.hull_rating,
            f"vessel_analysis_vessel_post_{criteria}_list",
            post_list,
        )
