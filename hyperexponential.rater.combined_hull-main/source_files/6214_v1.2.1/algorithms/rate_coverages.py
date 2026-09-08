import hx
import pandas as pd
import math as math
import re
import numpy as np
from datetime import date
from algorithms.rate_utilities import (
    pd_df_from_hx_list,
    hxd_node_setter,
    ratio,
)
from algorithms.helpers.rate_common import MBBEFDG3
import algorithms.rate_constants as constants
from algorithms import parameter_tables_schema as params
from algorithms.rate_utilities import ratio


def get_cover_value(cover):
    match = re.match(r"^(\d+)", cover)
    if match:
        return int(match.group(1))
    else:
        return 0


def populate_coverages_inputs(coverages, rating_summary):
    hull_rating_summary = rating_summary.coverages.hull

    for coverage in coverages:
        coverage_data = getattr(rating_summary.coverages, coverage)
        written_line = getattr(coverage_data, "written_line")
        written_line.calculated = hull_rating_summary.written_line
        brokerage = getattr(coverage_data, "brokerage")
        brokerage.calculated = hull_rating_summary.brokerage
        lead_follow = getattr(coverage_data, f"{coverage}_lead_follow")
        lead_follow.calculated = hull_rating_summary.hull_lead_follow


def calculate_loh_values(hxd):
    vessels = hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
    loh_rating_summary = hxd.cds.layers[0].coverages.loh
    inception_date = hxd.cds.standard_fields.inception_date
    expiry_date = hxd.cds.standard_fields.expiry_date
    non_cds_fields = hxd.non_cds
    base_rate_table = hx.params.table_loh_base_rate
    daily_rate_table = hx.params.table_loh_daily_rate
    modelling_parameters_table = hx.params.table_modelling_parameters
    base_rate_brokerage = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "LOHBaseRateBrokerage", "value"
    ].iloc[0]
    prefix = "loh_"
    commission = loh_rating_summary.brokerage or 0
    # Join the DataFrame with base_rate_table on 'loh_xs_days' and 'loh_cover'
    vessels_df = pd_df_from_hx_list(vessels)
    # Create a mask to filter out rows where both IMO and Name are None/NaN
    empty_name_and_imo_mask = ~(
        vessels_df[f"{prefix}vessel_details/{prefix}name"].isnull()
        & vessels_df[f"{prefix}vessel_details/{prefix}imo"].isnull()
    )

    # Apply the mask to filter the DataFrame
    vessels_df = vessels_df[empty_name_and_imo_mask]

    # Generate the unique identifier
    vessels_df[f"{prefix}unique_identifier"] = (
        vessels_df[f"{prefix}vessel_details/{prefix}name"].fillna("")
        + "_"
        + vessels_df[f"{prefix}vessel_details/{prefix}imo"].fillna("")
    )

    # Add a unique identifier to each vessel
    vessels_df[f"{prefix}unique_identifier"] = (
        vessels_df[f"{prefix}unique_identifier"]
        + "_"
        + (vessels_df.groupby(f"{prefix}unique_identifier").cumcount() + 1).astype(str)
    )

    number_of_vessels_mask = vessels_df[f"{prefix}number_of_vessels"].notna()
    non_cds_fields.show_hide_toggles.loh.show_number_of_vessels_warning = (
        True
        if (
            vessels_df.loc[number_of_vessels_mask, f"{prefix}number_of_vessels"] > 1
        ).any()
        else False
    )
    non_cds_fields.labels.loh.loh_vessels_number_greater_than_one_warning = 'Warning: "Bulked" vessels are identified with Number of Vessels > 1. Please make sure the entering is correct for Bulk Rating'
    vessels_df[f"{prefix}xs_days"] = (
        vessels_df[f"{prefix}xs_days"]
        .fillna(0)
        .astype(int)
        .astype(str)
        .replace("0", "")
    )
    vessels_df[f"{prefix}cover"] = vessels_df[f"{prefix}cover"].fillna("").astype(str)
    base_rate_table["xs_days"] = base_rate_table["xs_days"].astype(str)
    daily_rate_table["xs_days"] = daily_rate_table["xs_days"].astype(str)

    vessels_df = vessels_df.merge(
        base_rate_table,
        left_on=[f"{prefix}xs_days", f"{prefix}cover"],
        right_on=["xs_days", "cover"],
        how="left",
    ).rename(columns={"rate": "base_rate"})

    vessels_df = vessels_df.merge(
        daily_rate_table,
        left_on=[f"{prefix}xs_days", f"{prefix}cover"],
        right_on=["xs_days", "cover"],
        how="left",
    ).rename(columns={"rate": "daily_rate"})

    vessels_df[f"{prefix}conditions"] = (
        vessels_df[f"{prefix}xs_days"].astype(str).fillna("")
        + "/"
        + vessels_df[f"{prefix}cover"].fillna("")
    )

    vessels_df[f"{prefix}sum_insured"] = vessels_df[f"{prefix}cover"].apply(
        get_cover_value
    ) * vessels_df[f"{prefix}daily_rate"].fillna(0)

    is_dev = False
    bp_class = "Loss of Hire (LOH)" if is_dev else "Hull"
    if not bp_class:
        return
    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = (
        hx.params.table_original_rater_params if is_dev else params.tp_parameters.df()
    )
    tp_year = inception_date.year
    if tp_year not in list(
        tp_params_df[tp_params_df["business_plan_class"] == bp_class]["year"]
    ):
        tp_year = tp_params_df[tp_params_df["business_plan_class"] == bp_class][
            "year"
        ].max()

    nmp_load = tp_params_df[
        (tp_params_df["business_plan_class"] == bp_class)
        & (tp_params_df["year"] == tp_year)
    ]["nmp_load"].iloc[0]

    vessels_df[f"{prefix}vessel_base_rate"] = (
        vessels_df[f"base_rate"].fillna(0)
        * (1 + vessels_df[f"{prefix}uw_adjustment"].fillna(0))
        * (1 - base_rate_brokerage)
        * (1 + nmp_load)
    ) / (1 - commission)

    vessels_df[f"{prefix}vessel_daily_rate"] = (
        vessels_df[f"daily_rate"].fillna(0)
        * (1 + vessels_df[f"{prefix}uw_adjustment"].fillna(0))
        * (1 - base_rate_brokerage)
        * (1 + nmp_load)
    ) / (1 - commission)

    term_year = ((expiry_date - inception_date).days + 1) / 365
    vessels_df[f"{prefix}benchmark_premium"] = vessels_df[
        f"{prefix}vessel_base_rate"
    ].fillna(0) * vessels_df[f"{prefix}sum_insured"].fillna(0) * term_year

    coverage_benchmark_premium = vessels_df[f"{prefix}benchmark_premium"].sum()

    coverage_total_sum_insured = vessels_df[f"{prefix}sum_insured"].sum()

    hxd_node_setter(
        loh_rating_summary,
        prefix + "total_premium",
        coverage_benchmark_premium,
    )

    hxd_node_setter(
        loh_rating_summary,
        prefix + "total_sum_insured",
        coverage_total_sum_insured,
    )

    hxd_node_setter(
        loh_rating_summary,
        prefix + "fleet_level",
        ratio(coverage_benchmark_premium, coverage_total_sum_insured),
    )

    columns_to_write = [
        "unique_identifier",
        "conditions",
        "sum_insured",
        "vessel_daily_rate",
        "vessel_base_rate",
        "benchmark_premium",
    ]
    for i in range(vessels_df.shape[0]):
        for col in columns_to_write:
            hxd_node_setter(
                vessels[i],
                f"{prefix}{col}",
                vessels_df[f"{prefix}{col}"][i],
            )

    if loh_rating_summary.section_reference is None:
        return
    data_mart_vessels = (
        hxd.cds.exposure.granular.vessels.loh_rating.data_mart_temp_vessels_list
    )

    vessels_df = vessels_df.loc[vessels_df[f"{prefix}unique_identifier"].notna()]
    if (not data_mart_vessels) or (len(data_mart_vessels) != len(vessels_df)):
        hxd.non_cds.show_hide_toggles.loh.show_data_mart_warning = True
        hx.errors.validation(f"{hxd.non_cds.labels.loh.data_mart_warning_message}")
        return
    data_mart_vessels_df = pd_df_from_hx_list(data_mart_vessels)

    vessels_df = vessels_df.drop(
        columns=[f"{prefix}unique_identifier"], errors="ignore"
    )
    data_mart_vessels_df = data_mart_vessels_df.drop(
        columns=[f"{prefix}unique_identifier"], errors="ignore"
    )

    data_mart_columns = data_mart_vessels_df.columns.tolist()
    vessels_details_prefix = "loh_vessel_details/loh_"
    vessels_df = vessels_df.rename(
        columns={
            f"{vessels_details_prefix}imo": "loh_imo",
            f"{vessels_details_prefix}name": "loh_name",
            f"{vessels_details_prefix}gross_tonnage": "loh_gross_tonnage",
            f"{vessels_details_prefix}dwt": "loh_dwt",
            f"{vessels_details_prefix}vessel_type": "loh_vessel_type",
            f"{vessels_details_prefix}year_built": "loh_year_built",
        }
    )

    vessels_df["loh_policy_reference"] = loh_rating_summary.section_reference or ""
    vessels_df["loh_written_line"] = loh_rating_summary.written_line or 0
    vessels_df["loh_is_renewal"] = 1 if hxd.cds.standard_fields.is_renewal else 0
    vessels_df["loh_currency"] = hxd.cds.currencies.source_currency or ""
    vessels_df["loh_inception_date"] = hxd.cds.standard_fields.inception_date or date(
        1900, 1, 1
    )
    vessels_df["loh_expiry_date"] = hxd.cds.standard_fields.expiry_date or date(
        1900, 1, 1
    )
    vessels_df = vessels_df.filter(items=data_mart_columns).replace({np.nan: None})

    # Dynamically align data types for merge columns
    for col in data_mart_columns:
        # Check if both columns are entirely None/NaN
        if vessels_df[col].isnull().all() and data_mart_vessels_df[col].isnull().all():
            # Convert both to string if all values are None/NaN
            vessels_df[col] = vessels_df[col].astype(str)
            data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)
        else:
            left_dtype = vessels_df[col].dtype
            right_dtype = data_mart_vessels_df[col].dtype

            # If both columns are floats, round to 6 decimal places
            if pd.api.types.is_float_dtype(left_dtype) and pd.api.types.is_float_dtype(
                right_dtype
            ):
                vessels_df[col] = vessels_df[col].round(6)
                data_mart_vessels_df[col] = data_mart_vessels_df[col].round(6)
            # If data types are mismatched
            elif left_dtype != right_dtype:
                if pd.api.types.is_numeric_dtype(
                    left_dtype
                ) or pd.api.types.is_numeric_dtype(right_dtype):
                    # Convert both to float if either is numeric
                    vessels_df[col] = vessels_df[col].replace("", np.nan).astype(float)
                    data_mart_vessels_df[col] = (
                        data_mart_vessels_df[col].replace("", np.nan).astype(float)
                    )
                elif pd.api.types.is_bool_dtype(
                    left_dtype
                ) or pd.api.types.is_bool_dtype(right_dtype):
                    # Convert both to bool if either is boolean
                    vessels_df[col] = (
                        vessels_df[col].astype(bool).replace("", np.nan).astype(float)
                    )
                    data_mart_vessels_df[col] = (
                        data_mart_vessels_df[col]
                        .astype(bool)
                        .replace("", np.nan)
                        .astype(float)
                    )
                else:
                    # Convert both to string for mixed or object types
                    vessels_df[col] = vessels_df[col].astype(str)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)

    merged_df = vessels_df.merge(data_mart_vessels_df, how="left", indicator=True)
    non_cds_fields.show_hide_toggles.loh.show_data_mart_warning = not (
        merged_df["_merge"].eq("both").all()
    )
    if non_cds_fields.show_hide_toggles.loh.show_data_mart_warning:
        hx.errors.validation(f"{hxd.non_cds.labels.loh.data_mart_warning_message}")


def calculate_ship_building_values(hxd):
    inception_date = hxd.cds.standard_fields.inception_date
    vessels = hxd.cds.exposure.granular.vessels
    ship_building_rating_summary = hxd.cds.layers[0].coverages.ship_building
    inception_date,
    is_actuarial_pricing = (
        hxd.non_cds.show_hide_toggles.ship_building.show_ship_builders_actuarial_pricing,
    )
    prefix = "ship_building_"
    base_rate_table = hx.params.ship_building_base_rate
    is_production_stages_time = (
        ship_building_rating_summary.ship_building_show_production_stages_time
    )

    vessels_df = pd_df_from_hx_list(
        vessels.ship_building_rating.ship_building_vessels_list
    )
    vessels_df
    base_rate_table_dict = dict(zip(base_rate_table["stage"], base_rate_table["rate"]))
    base_rate_table_dict = {
        **base_rate_table_dict,
        "all_stages": (base_rate_table_dict["keel_laying_launch"] / 3)
        + (base_rate_table_dict["launch_delivery"] / 3)
        + (base_rate_table_dict["steel_cutting_keel_laying"] / 3),
    }

    if (
        vessels_df[f"{prefix}number_of_vessels"].isna().all()
        or vessels_df[f"{prefix}sum_insured"].isna().all()
    ):
        return

    number_of_vessels_mask = vessels_df[f"{prefix}number_of_vessels"].notna()
    hxd.non_cds.show_hide_toggles.ship_building.show_number_of_vessels_warning = (
        True
        if (
            vessels_df.loc[number_of_vessels_mask, f"{prefix}number_of_vessels"] > 1
        ).any()
        else False
    )
    hxd.non_cds.labels.shipbuilders.shipbuilders_vessels_number_greater_than_one_warning = 'Warning: "Bulked" vessels are identified with Number of Vessels > 1. Please make sure the entering is correct for Bulk Rating'

    vessels_df["base_rate_steel_cutting"] = (
        vessels_df[f"{prefix}total_months_steel_cutting_keel_laying"]
        .fillna(0)
        .astype(float)
        * base_rate_table_dict["steel_cutting_keel_laying"]
    )
    vessels_df["base_rate_keel_laying"] = (
        vessels_df[f"{prefix}total_months_keel_laying_launch"].fillna(0).astype(float)
    ) * base_rate_table_dict["keel_laying_launch"]
    vessels_df["base_rate_launch_delivery"] = (
        vessels_df[f"{prefix}total_months_launch_delivery"].fillna(0).astype(float)
    ) * base_rate_table_dict["launch_delivery"]
    vessels_df["base_rate_all_stages"] = (
        vessels_df[f"{prefix}total_months_all_stages"].fillna(0).astype(float)
        * base_rate_table_dict["all_stages"]
    )

    vessels_df[f"{prefix}base_rate_non_war"] = (
        (
            vessels_df["base_rate_steel_cutting"]
            + vessels_df["base_rate_keel_laying"]
            + vessels_df["base_rate_launch_delivery"]
        )
        if is_production_stages_time
        else vessels_df["base_rate_all_stages"]
    )

    vessel_types_table = hx.params.ship_building_vessel_types
    vessels_df[f"{prefix}vessel_type_rate"] = (
        vessels_df[f"{prefix}vessel_type"]
        .map(vessel_types_table.set_index("vessel_type")["factor"])
        .fillna(0)
    )

    countries_table = hx.params.ship_building_countries
    countries_table["total_discount"] = (
        (1 + countries_table["cat_load"])
        * (1 + countries_table["shipyard_and_typhoon_plans_sophistication"])
    ) - 1
    vessels_df[f"{prefix}country_rate"] = (
        vessels_df[f"{prefix}country"]
        .map(countries_table.set_index("country")["total_discount"])
        .fillna(0)
    )

    survey_grade_table = hx.params.ship_building_survey_grade
    vessels_df[f"{prefix}survey_grade_rate"] = (
        vessels_df[f"{prefix}survey_grade"]
        .map(survey_grade_table.set_index("grade")["factor"])
        .fillna(0)
    )

    vessels_df[f"{prefix}deductible"] = vessels_df[f"{prefix}deductible"].fillna(0)
    # Calculate intermediate values
    intermediate_deductible_rate_values = vessels_df[f"{prefix}deductible"] / (
        vessels_df[f"{prefix}sum_insured"] / vessels_df[f"{prefix}number_of_vessels"]
    )

    # Apply the MBBEFDG3 function to each intermediate value using a list comprehension
    modelling_parameters_table = hx.params.table_modelling_parameters
    MBBEFDG3_param = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "MBBDFDShipbuildingParam", "value"
    ].iloc[0]
    vessels_df[f"{prefix}deductible_rate"] = [
        1 - MBBEFDG3(MBBEFDG3_param, value)
        for value in intermediate_deductible_rate_values
    ]

    vessels_df[f"{prefix}non_war_net_premium_rate"] = (
        vessels_df[f"{prefix}base_rate_non_war"]
        * (1 + vessels_df[f"{prefix}vessel_type_rate"])
        * (1 + vessels_df[f"{prefix}country_rate"])
        * (1 + vessels_df[f"{prefix}survey_grade_rate"])
        * vessels_df[f"{prefix}deductible_rate"]
    )

    vessels_df[f"{prefix}war_rate"] = (
        constants.ship_building_war_factor * vessels_df[f"{prefix}number_of_vessels"]
    )

    vessels_df[f"{prefix}war_premium_net_rate"] = (
        vessels_df[f"{prefix}non_war_net_premium_rate"]
        + vessels_df[f"{prefix}war_rate"]
    )

    vessels_df[f"{prefix}total_pre_fleet_exposure_net_rate"] = (
        vessels_df[f"{prefix}war_premium_net_rate"]
        if ship_building_rating_summary.ship_building_is_war_cover
        else vessels_df[f"{prefix}non_war_net_premium_rate"]
    )

    table_vessels_discounts = hx.params.ship_building_vessels_discount
    total_number_of_vessels = vessels_df[f"{prefix}number_of_vessels"].sum()
    max_vessels = table_vessels_discounts["number_of_vessels"].max()
    max_discount = table_vessels_discounts.loc[
        table_vessels_discounts["number_of_vessels"] == max_vessels, "discount"
    ].values[0]

    discount = (
        max_discount
        if total_number_of_vessels >= max_vessels
        else (
            (
                table_vessels_discounts.loc[
                    table_vessels_discounts["number_of_vessels"]
                    == total_number_of_vessels,
                    "discount",
                ].values[0]
            )
            if total_number_of_vessels
            in list(
                table_vessels_discounts[
                    table_vessels_discounts["number_of_vessels"]
                    == total_number_of_vessels
                ]["number_of_vessels"]
            )
            else 0
        )
    )
    vessels_df[f"{prefix}fleet_discount"] = discount

    vessels_df[f"{prefix}total_exposure_net_rate"] = vessels_df[
        f"{prefix}total_pre_fleet_exposure_net_rate"
    ] * (1 - vessels_df[f"{prefix}fleet_discount"])

    vessels_df[f"{prefix}total_exposure_net_premium"] = (
        vessels_df[f"{prefix}total_exposure_net_rate"]
        * vessels_df[f"{prefix}sum_insured"]
        / vessels_df[f"{prefix}number_of_vessels"]
    )

    is_dev = False
    bp_class = "Shipbuilders" if is_dev else "Hull"
    if not bp_class:
        return
    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = (
        hx.params.table_original_rater_params if is_dev else params.tp_parameters.df()
    )
    tp_year = inception_date.year
    if tp_year not in list(
        tp_params_df[tp_params_df["business_plan_class"] == bp_class]["year"]
    ):
        tp_year = tp_params_df[tp_params_df["business_plan_class"] == bp_class][
            "year"
        ].max()

    nmp_load = tp_params_df[
        (tp_params_df["business_plan_class"] == bp_class)
        & (tp_params_df["year"] == tp_year)
    ]["nmp_load"].iloc[0]

    uw_adjustment = ship_building_rating_summary.ship_building_uw_adjustment or 0
    implied_claim_pre_uw_adj = (
        vessels_df[f"{prefix}total_exposure_net_premium"].fillna(0).sum()
        * (1 + nmp_load)
        * constants.benchmark_lr
    )
    implied_claim_post_uw_adj = implied_claim_pre_uw_adj * (1 + uw_adjustment)
    benchmark_net_premium_exposure_rated = (
        implied_claim_pre_uw_adj / constants.benchmark_lr
    )

    ship_building_rating_summary.ship_building_net_benchmark_premium_pre_uw_adj = (
        benchmark_net_premium_exposure_rated
    )
    ship_building_rating_summary.expected_loss_cost_pro_rated_100pct = (
        implied_claim_post_uw_adj
    )
    ship_building_rating_summary.expected_loss_cost_pre_uw_adj = (
        implied_claim_pre_uw_adj
    )

    vessels_df[f"{prefix}benchmark_rate"] = vessels_df[
        f"{prefix}total_exposure_net_rate"
    ] * (1 + uw_adjustment)

    vessels_df["ship_building_index"] = vessels_df.index

    columns_to_write = ["benchmark_rate", "index"]
    for i in range(vessels_df.shape[0]):
        for col in columns_to_write:
            value = vessels_df[f"{prefix}{col}"][i]
            if (
                (value is not None)
                and (isinstance(value, float) or isinstance(value, np.int64))
                and (not math.isinf(value))
                and (not math.isnan(value))
            ):
                hxd_node_setter(
                    vessels.ship_building_rating.ship_building_vessels_list[i],
                    f"{prefix}{col}",
                    value,
                )

    if is_actuarial_pricing:
        pricing_prefix = "ship_building_pricing_"
        columns_mapping = {
            "base_rate_all_stages": "overall_process_base_rate",
            "base_rate_steel_cutting": "base_rate_steel_cutting_keel_laying",
            "base_rate_keel_laying": "base_rate_keel_laying_launch",
            "base_rate_launch_delivery": "base_rate_launch_delivery",
            f"{prefix}base_rate_non_war": "base_rate_non_war",
            f"{prefix}vessel_type_rate": "vessel_type",
            f"{prefix}country_rate": "country",
            f"{prefix}survey_grade_rate": "survey_grade",
            f"{prefix}deductible_rate": "deductible",
            f"{prefix}non_war_net_premium_rate": "non_war_premium_net_rate",
            f"{prefix}war_rate": "war_premium_net_rate",
            f"{prefix}total_pre_fleet_exposure_net_rate": "total_exposure_net_rate_pre_fleet",
            f"{prefix}fleet_discount": "fleet_discount",
            f"{prefix}total_exposure_net_rate": "total_exposure_net_rate",
            f"{prefix}total_exposure_net_premium": "exposure_net_premium",
        }

        columns_mapping = {
            key: f"{pricing_prefix}{value}" for key, value in columns_mapping.items()
        }
        # Select and rename the columns
        pricing_df = vessels_df[list(columns_mapping.keys())].rename(
            columns=columns_mapping
        )
        if pricing_df.empty:
            return
        pricing_df[f"{pricing_prefix}vessel_type"] = pricing_df[
            f"{pricing_prefix}vessel_type"
        ].mul(100)
        pricing_df[f"{pricing_prefix}country"] = pricing_df[
            f"{pricing_prefix}country"
        ].mul(100)
        pricing_df = pricing_df.replace({np.nan: None, "": None})
        vessels.ship_building_rating.ship_building_pricing_vessels_list = (
            pricing_df.to_dict(orient="records")
        )


def calculate_iv_values(hxd):
    rating_summary = hxd.cds.layers[0]
    hull_rating_summary = rating_summary.coverages.hull
    vessels = hxd.cds.exposure.granular.vessels
    iv_rating_summary = rating_summary.coverages.iv
    show_hide_toggles = hxd.non_cds.show_hide_toggles
    iv_labels = hxd.non_cds.labels.iv
    coverage_prefix = "iv/iv_"
    vessels_details_prefix = "vessel_details/"
    modelling_static_prefix = "static_"
    validation_columns_prefix = "validation_iv_"
    columns_to_write = []
    iv_agreed_value_perc = iv_rating_summary.iv_perc_of_h_and_m_value
    iv_brokerage = iv_rating_summary.brokerage.selected or 0

    if len(vessels.hull_rating.modelling_list) == 0:
        return

    vessels_df = pd_df_from_hx_list(vessels.hull_rating.vessels_list)
    modelling_df = pd_df_from_hx_list(vessels.hull_rating.modelling_list)
    vessels_df = vessels_df.merge(
        modelling_df,
        left_on="unique_imo",
        right_on="modelling_unique_imo",
        how="left",
    )
    imo_not_empty_mask = vessels_df[f"{vessels_details_prefix}imo"].notna()

    vessels_deductible_mask = vessels_df["deductible"].isna()

    vessels_df[f"{coverage_prefix}deductible"] = vessels_df[
        f"{coverage_prefix}deductible"
    ].where(
        ~vessels_df[
            f"{coverage_prefix}deductible"
        ].isna(),  # Keep existing values if not NaN
        np.where(vessels_deductible_mask, None, 0),
    )
    columns_to_write.append("iv_deductible")

    if iv_agreed_value_perc is not None:
        agreed_value_mask = vessels_df["agreed_value"].notna()
        vessels_df.loc[
            agreed_value_mask, f"{coverage_prefix}agreed_value"
        ] = vessels_df.loc[
            agreed_value_mask, f"{coverage_prefix}agreed_value_selected"
        ].where(
            (
                vessels_df.loc[
                    agreed_value_mask, f"{coverage_prefix}agreed_value_selected"
                ].notna()
            ),
            vessels_df.loc[agreed_value_mask, "agreed_value"] * (iv_agreed_value_perc / (1 - iv_agreed_value_perc)),
        )
        columns_to_write.append("iv_agreed_value")

    vessels_df["expiry_date"] = pd.to_datetime(
        vessels_df["expiry_date"], errors="coerce"
    )
    vessels_df["inception_date"] = pd.to_datetime(
        vessels_df["inception_date"], errors="coerce"
    )

    pro_rata_mask = (
        vessels_df[f"inception_date"].notna()
        & vessels_df[f"expiry_date"].notna()
        & (vessels_df[f"expiry_date"] > vessels_df[f"inception_date"])
        & (vessels_df[f"expiry_date"] > pd.Timestamp("1900-01-01"))
        & (vessels_df[f"inception_date"] > pd.Timestamp("1900-01-01"))
    )

    vessels_df[f"{coverage_prefix}pro_rata"] = (
        (
            vessels_df.loc[pro_rata_mask, "expiry_date"]
            - vessels_df.loc[pro_rata_mask, "inception_date"]
        ).dt.days
        + 1
    ) / 365

    coverage_table = hx.params.table_coverage_factor
    vessels_df[f"{coverage_prefix}coverage_factor"] = vessels_df[
        f"{coverage_prefix}coverage"
    ].map(coverage_table.set_index("coverage")["factor"])

    intermediate_coverage_deductible_rate_values = (
        vessels_df[f"{coverage_prefix}deductible"]
        .fillna(0)
        .div(vessels_df[f"{coverage_prefix}agreed_value"].fillna(0))
    )

    modelling_parameters_table = hx.params.table_modelling_parameters
    MBBEFDG3_param = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "MBBDFDHullParam", "value"
    ].iloc[0]
    vessels_df[f"{coverage_prefix}mbbefdg"] = [
        1 - MBBEFDG3(MBBEFDG3_param, value)
        for value in intermediate_coverage_deductible_rate_values
    ]

    vessels_commission = hull_rating_summary.brokerage or 0
    for model_type in constants.model_types:
        # Filter out rows where model_rate is None
        filtered_vessels_df = vessels_df[
            vessels_df[f"{model_type}_model_rate"].notna()
            & vessels_df[f"{coverage_prefix}agreed_value"].notna()
        ]

        # Perform the calculations on the filtered DataFrame
        filtered_vessels_df[f"{coverage_prefix}{model_type}_model_rate"] = (
            filtered_vessels_df[f"{model_type}_model_rate"]
            .div(filtered_vessels_df[f"{modelling_static_prefix}mbbefdg"])
            .mul(filtered_vessels_df[f"{coverage_prefix}mbbefdg"])
            .mul(
                1 + filtered_vessels_df[f"{coverage_prefix}uw_adjustment"], fill_value=1
            )
            .mul(1 - vessels_commission)
            .mul(filtered_vessels_df[f"{coverage_prefix}coverage_factor"])
            .div(1 - iv_brokerage)
        )

        filtered_vessels_df[f"{coverage_prefix}{model_type}_benchmark_premium"] = (
            filtered_vessels_df[f"{coverage_prefix}{model_type}_model_rate"].mul(
                filtered_vessels_df[f"{coverage_prefix}agreed_value"]
            )
        )

        columns_to_write.append(f"iv_{model_type}_model_rate")
        columns_to_write.append(f"iv_{model_type}_benchmark_premium")

        # Assign the results back to the original DataFrame
        vessels_df.loc[
            filtered_vessels_df.index, f"{coverage_prefix}{model_type}_model_rate"
        ] = filtered_vessels_df[f"{coverage_prefix}{model_type}_model_rate"]

        vessels_df.loc[
            filtered_vessels_df.index,
            f"{coverage_prefix}{model_type}_benchmark_premium",
        ] = filtered_vessels_df[f"{coverage_prefix}{model_type}_benchmark_premium"]

    # Filter out rows where agreed values is None
    achieved_premium_mask = (
        vessels_df[f"{coverage_prefix}agreed_value"].notna()
        & vessels_df[f"{coverage_prefix}achieved_rate"].notna()
        & vessels_df[f"{coverage_prefix}pro_rata"].notna()
    )

    vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}achieved_premium"] = (
        vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}agreed_value"]
        .mul(
            vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}achieved_rate"],
            fill_value=0,
        )
        .mul(vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}pro_rata"])
    )

    columns_to_write.append("iv_achieved_premium")

    vessels_df[f"{coverage_prefix}benchmark_premium"] = vessels_df[
        f"{coverage_prefix}behavioural_benchmark_premium"
    ].fillna(vessels_df[f"{coverage_prefix}static_benchmark_premium"])
    columns_to_write.append("iv_benchmark_premium")

    # Filter out rows where benchmark_premium is None
    filtered_vessels_df = vessels_df[
        vessels_df[f"{coverage_prefix}benchmark_premium"].notna()
    ]

    # Perform the calculations on the filtered DataFrame
    filtered_vessels_df[
        f"{coverage_prefix}benchmark_premium_pre_uw_adj"
    ] = filtered_vessels_df[f"{coverage_prefix}benchmark_premium"].div(
        (1 + filtered_vessels_df[f"{coverage_prefix}uw_adjustment"])
        * (1 + filtered_vessels_df["uw_adjustment"]),
        fill_value=1,
    )

    # Assign the results back to the original DataFrame
    vessels_df.loc[
        filtered_vessels_df.index, f"{coverage_prefix}benchmark_premium_pre_uw_adj"
    ] = filtered_vessels_df[f"{coverage_prefix}benchmark_premium_pre_uw_adj"]

    override_column_fields = ["iv_agreed_value", "iv_deductible"]

    vessels_df[f"{validation_columns_prefix}coverage"] = np.where(
        vessels_df[f"{coverage_prefix}coverage"].isna(),
        f"{constants.incomplete_column} Coverage must have a value",
        "",
    )
    vessels_df[f"{validation_columns_prefix}agreed_value"] = np.where(
        vessels_df[f"{coverage_prefix}agreed_value"].isna(),
        f"{constants.incomplete_column} Agreed Value must have a value",
        "",
    )
    vessels_df[f"{validation_columns_prefix}achieved_rate"] = np.where(
        vessels_df[f"{coverage_prefix}achieved_rate"].isna(),
        f"{constants.incomplete_column} Achieved Rate must have a value",
        np.where(
            (vessels_df["achieved_rate"] < 0),
            f"{constants.incomplete_column} Achieved Rate Must be greater than 0",
            "",
        ),
    )
    validation_columns = [
        f"{validation_columns_prefix}coverage",
        f"{validation_columns_prefix}agreed_value",
        f"{validation_columns_prefix}achieved_rate",
    ]
    has_error = vessels_df[validation_columns].notna() & (
        vessels_df[validation_columns] != ""
    )

    # Set the has_error column in vessels_df to True if any column has a non-null and non-empty value
    vessels_df[f"{coverage_prefix}has_error"] = has_error.any(axis=1)
    iv_labels.validation_iv_error_message = (
        f"{constants.incomplete_column} Fix the invalid entries"
        if vessels_df[f"{coverage_prefix}has_error"].any()
        else f"{constants.complete_column} All entries are valid."
    )

    columns_to_write.append("iv_has_error")
    is_include_vessel_mask = vessels_df[
        f"{coverage_prefix}is_include_vessel"
    ].notna() & (vessels_df[f"{coverage_prefix}is_include_vessel"] == True)
    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_coverage"
    ] = vessels_df[f"{coverage_prefix}coverage"]

    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_agreed_value"
    ] = vessels_df[f"{coverage_prefix}agreed_value"]

    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_deductible"
    ] = vessels_df[f"{coverage_prefix}deductible"]

    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_achieved_rate"
    ] = vessels_df[f"{coverage_prefix}achieved_rate"]

    columns_to_write.extend(
        [
            "iv_output_summary_coverage",
            "iv_output_summary_agreed_value",
            "iv_output_summary_deductible",
            "iv_output_summary_achieved_rate",
        ]
    )
    if vessels_df.empty:
        return
    vessels_df_dict = (
        vessels_df.loc[imo_not_empty_mask]
        .set_index("unique_imo")
        .to_dict(orient="index")
    )
    ok_validation = f"Ok {constants.complete_column}"
    for i in range(len(vessels.hull_rating.vessels_list)):
        unique_imo = vessels.hull_rating.vessels_list[i].unique_imo
        if unique_imo in vessels_df_dict:
            for col in columns_to_write:
                if col in override_column_fields:
                    hxd_node_setter(
                        getattr(vessels.hull_rating.vessels_list[i].iv, col),
                        "calculated",
                        vessels_df_dict[unique_imo][f"iv/{col}"],
                    )
                else:
                    hxd_node_setter(
                        vessels.hull_rating.vessels_list[i].iv,
                        col,
                        vessels_df_dict[unique_imo][f"iv/{col}"],
                    )

            for col in validation_columns:
                current_validation_value = getattr(iv_labels, col)
                hxd_node_setter(
                    vessels.hull_rating.vessels_list[i].iv.iv_error_validation_columns,
                    col,
                    vessels_df_dict[unique_imo][f"{col}"],
                )

                hxd_node_setter(
                    iv_labels,
                    col,
                    (
                        ok_validation
                        if (
                            (vessels_df_dict[unique_imo][f"{col}"] == "")
                            and (
                                (current_validation_value is None)
                                or (current_validation_value == ok_validation)
                            )
                        )
                        else f"Error {constants.incomplete_column}"
                    ),
                )

    if show_hide_toggles.hull.show_data_mart_warning or (
        hxd.cds.layers[0].coverages.iv.section_reference is None
    ):
        return
    data_mart_vessels = (
        hxd.cds.exposure.granular.vessels.hull_rating.data_mart_temp_vessels_list
    )
    if not data_mart_vessels:
        show_hide_toggles.hull.show_data_mart_warning = True
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")
        return
    data_mart_vessels_df = pd_df_from_hx_list(data_mart_vessels)
    data_mart_vessels_df = data_mart_vessels_df.filter(regex="^iv_", axis=1)

    data_mart_columns = data_mart_vessels_df.columns.tolist()
    vessels_df = vessels_df[vessels_df[f"{coverage_prefix}is_include_vessel"] == True]
    vessels_df = vessels_df.loc[imo_not_empty_mask]
    vessels_df = vessels_df.rename(
        columns={
            f"{vessels_details_prefix}imo": "imo",
            f"{vessels_details_prefix}name": "name",
            f"{vessels_details_prefix}gross_tonnage": "gross_tonnage",
            f"{vessels_details_prefix}order_percent": "order_percent",
            f"{coverage_prefix}agreed_value": "iv_agreed_value",
            f"{coverage_prefix}deductible": "iv_deductible",
            f"{coverage_prefix}achieved_rate": "iv_achieved_rate",
        }
    )
    vessels_df["iv_policy_reference"] = iv_rating_summary.section_reference
    vessels_df["iv_written_line"] = iv_rating_summary.written_line.selected or 0
    vessels_df["is_renewal"] = 1 if hxd.cds.standard_fields.is_renewal else 0
    vessels_df["currency"] = hxd.cds.currencies.source_currency or ""
    vessels_df = vessels_df.filter(items=data_mart_columns).replace({np.nan: None})

    # Dynamically align data types for merge columns
    for col in data_mart_columns:
        # Check if both columns are entirely None/NaN
        if vessels_df[col].isnull().all() and data_mart_vessels_df[col].isnull().all():
            # Convert both to string if all values are None/NaN
            vessels_df[col] = vessels_df[col].astype(str)
            data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)
        else:
            left_dtype = vessels_df[col].dtype
            right_dtype = data_mart_vessels_df[col].dtype

            # If data types are mismatched
            if left_dtype != right_dtype:
                if pd.api.types.is_numeric_dtype(
                    left_dtype
                ) or pd.api.types.is_numeric_dtype(right_dtype):
                    # Convert both to float if either is numeric
                    vessels_df[col] = vessels_df[col].astype(float)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(float)
                elif pd.api.types.is_bool_dtype(
                    left_dtype
                ) or pd.api.types.is_bool_dtype(right_dtype):
                    # Convert both to bool if either is boolean
                    vessels_df[col] = vessels_df[col].astype(bool)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(bool)
                else:
                    # Convert both to string for mixed or object types
                    vessels_df[col] = vessels_df[col].astype(str)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)

    merged_df = vessels_df.merge(data_mart_vessels_df, how="left", indicator=True)
    show_hide_toggles.hull.show_data_mart_warning = not (
        merged_df["_merge"].eq("both").all()
    )
    if show_hide_toggles.hull.show_data_mart_warning:
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")


def calculate_war_values(hxd):
    rating_summary = hxd.cds.layers[0]
    hull_rating_summary = rating_summary.coverages.hull
    vessels = hxd.cds.exposure.granular.vessels
    war_rating_summary = rating_summary.coverages.war
    show_hide_toggles = hxd.non_cds.show_hide_toggles
    war_labels = hxd.non_cds.labels.war
    coverage_prefix = "war/war_"
    iv_coverage_prefix = "iv/iv_"
    vessels_details_prefix = "vessel_details/"
    validation_columns_prefix = "validation_war_"
    columns_to_write = []
    vessels_df = pd_df_from_hx_list(vessels.hull_rating.vessels_list)
    imo_not_empty_mask = vessels_df[f"{vessels_details_prefix}imo"].notna()

    war_rating_summary.brokerage.calculated = hull_rating_summary.brokerage
    war_rating_summary.written_line.calculated = hull_rating_summary.written_line

    war_commission = war_rating_summary.brokerage.selected or 0

    agreed_value_mask = (
        vessels_df["agreed_value"].notna()
        & vessels_df[f"{coverage_prefix}agreed_value_selected"].isna()
    )

    vessels_df.loc[agreed_value_mask, f"{coverage_prefix}agreed_value"] = vessels_df[
        "agreed_value"
    ] + vessels_df.loc[agreed_value_mask, f"{iv_coverage_prefix}agreed_value"].fillna(0)
    columns_to_write.append("war_agreed_value")

    vessels_df["expiry_date"] = pd.to_datetime(
        vessels_df["expiry_date"], errors="coerce"
    )
    vessels_df["inception_date"] = pd.to_datetime(
        vessels_df["inception_date"], errors="coerce"
    )

    pro_rata_mask = (
        vessels_df[f"inception_date"].notna()
        & vessels_df[f"expiry_date"].notna()
        & (vessels_df[f"expiry_date"] > vessels_df[f"inception_date"])
        & (vessels_df[f"expiry_date"] > pd.Timestamp("1900-01-01"))
        & (vessels_df[f"inception_date"] > pd.Timestamp("1900-01-01"))
    )

    vessels_df[f"{coverage_prefix}pro_rata"] = (
        (
            vessels_df.loc[pro_rata_mask, "expiry_date"]
            - vessels_df.loc[pro_rata_mask, "inception_date"]
        ).dt.days
        + 1
    ) / 365

    vessels_df[f"inception_year"] = pd.to_datetime(
        vessels_df[f"inception_date"]
    ).dt.year

    achieved_premium_mask = (
        vessels_df[f"{coverage_prefix}agreed_value"].notna()
        & vessels_df[f"{coverage_prefix}achieved_rate"].notna()
        & vessels_df[f"{coverage_prefix}pro_rata"].notna()
    )

    vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}achieved_premium"] = (
        vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}agreed_value"]
        .mul(
            vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}achieved_rate"],
            fill_value=0,
        )
        .mul(vessels_df.loc[achieved_premium_mask, f"{coverage_prefix}pro_rata"])
    )

    columns_to_write.append("war_achieved_premium")

    table_war_bplr = hx.params.table_war_bplr
    vessels_df[f"{coverage_prefix}bplr"] = (
        vessels_df[f"inception_year"]
        .map(table_war_bplr.set_index("year")["factor"])
        .fillna(0)
    )

    static_benchmark_mask = vessels_df[f"{coverage_prefix}achieved_premium"].notna()

    vessels_df.loc[
        static_benchmark_mask, f"{coverage_prefix}static_benchmark_premium"
    ] = (
        vessels_df.loc[static_benchmark_mask, f"{coverage_prefix}achieved_premium"]
        .mul(
            1
            + vessels_df.loc[
                static_benchmark_mask, f"{coverage_prefix}uw_adjustment"
            ].fillna(0)
        )
        .mul(1 - war_commission)
        .div(
            constants.benchmark_lr
            / vessels_df.loc[static_benchmark_mask, f"{coverage_prefix}bplr"].replace(
                0, float("nan")
            )
        )
        .div(1 - war_commission)
    )

    vessels_df[f"{coverage_prefix}behavioural_benchmark_premium"] = vessels_df[
        f"{coverage_prefix}static_benchmark_premium"
    ]

    for model_type in constants.model_types:
        # Create a mask for rows where both benchmark_premium and agreed_value are not NaN
        benchmark_premium_agreed_value_mask = (
            vessels_df[f"{coverage_prefix}{model_type}_benchmark_premium"].notna()
            & vessels_df[f"{coverage_prefix}agreed_value"].notna()
            & vessels_df[f"{coverage_prefix}agreed_value"]
            > 0
        )

        # Perform the calculations only on the rows where the mask is True
        vessels_df.loc[
            benchmark_premium_agreed_value_mask,
            f"{coverage_prefix}{model_type}_model_rate",
        ] = vessels_df.loc[
            benchmark_premium_agreed_value_mask,
            f"{coverage_prefix}{model_type}_benchmark_premium",
        ].div(
            vessels_df.loc[
                benchmark_premium_agreed_value_mask, f"{coverage_prefix}agreed_value"
            ]
        )

        columns_to_write.append(f"war_{model_type}_model_rate")
        columns_to_write.append(f"war_{model_type}_benchmark_premium")

    vessels_df[f"{coverage_prefix}benchmark_premium"] = vessels_df[
        f"{coverage_prefix}static_benchmark_premium"
    ]
    columns_to_write.append("war_benchmark_premium")

    # Create a mask for rows where benchmark_premium is not NaN
    mask_benchmark_premium = ~vessels_df[f"{coverage_prefix}benchmark_premium"].isna()

    # Perform the calculation only on the rows where the mask is True
    vessels_df.loc[
        mask_benchmark_premium, f"{coverage_prefix}benchmark_premium_pre_uw_adj"
    ] = vessels_df.loc[
        mask_benchmark_premium, f"{coverage_prefix}benchmark_premium"
    ].div(
        1
        + vessels_df.loc[
            mask_benchmark_premium, f"{coverage_prefix}uw_adjustment"
        ].fillna(0)
    )

    vessels_df[f"{validation_columns_prefix}coverage"] = np.where(
        vessels_df[f"{coverage_prefix}coverage"].isna(),
        f"{constants.incomplete_column} Coverage must have a value",
        "",
    )
    vessels_df[f"{validation_columns_prefix}agreed_value"] = np.where(
        vessels_df[f"{coverage_prefix}agreed_value"].isna(),
        f"{constants.incomplete_column} Agreed Value must have a value",
        "",
    )
    vessels_df[f"{validation_columns_prefix}achieved_rate"] = np.where(
        vessels_df[f"{coverage_prefix}achieved_rate"].isna(),
        f"{constants.incomplete_column} Achieved Rate must have a value",
        np.where(
            (vessels_df["achieved_rate"] < 0),
            f"{constants.incomplete_column} Achieved Rate Must be greater than 0",
            "",
        ),
    )
    validation_columns = [
        f"{validation_columns_prefix}coverage",
        f"{validation_columns_prefix}agreed_value",
        f"{validation_columns_prefix}achieved_rate",
    ]
    has_error = vessels_df[validation_columns].notna() & (
        vessels_df[validation_columns] != ""
    )

    # Set the has_error column in vessels_df to True if any column has a non-null and non-empty value
    vessels_df[f"{coverage_prefix}has_error"] = has_error.any(axis=1)
    war_labels.validation_war_error_message = (
        f"{constants.incomplete_column} Fix the invalid entries"
        if vessels_df[f"{coverage_prefix}has_error"].any()
        else f"{constants.complete_column} All entries are valid."
    )

    columns_to_write.append("war_has_error")

    override_column_fields = ["war_agreed_value", "war_coverage"]

    is_include_vessel_mask = vessels_df[
        f"{coverage_prefix}is_include_vessel"
    ].notna() & (vessels_df[f"{coverage_prefix}is_include_vessel"] == True)
    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_coverage"
    ] = vessels_df[f"{coverage_prefix}coverage"]

    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_agreed_value"
    ] = vessels_df[f"{coverage_prefix}agreed_value"]

    vessels_df.loc[
        is_include_vessel_mask, f"{coverage_prefix}output_summary_achieved_rate"
    ] = vessels_df[f"{coverage_prefix}achieved_rate"]

    columns_to_write.extend(
        [
            "war_output_summary_coverage",
            "war_output_summary_agreed_value",
            "war_output_summary_achieved_rate",
        ]
    )

    if (
        vessels_df.loc[imo_not_empty_mask].empty
        or vessels_df.loc[imo_not_empty_mask, "unique_imo"].isna().any()
    ):
        return
    vessels_df_dict = (
        vessels_df.loc[imo_not_empty_mask]
        .set_index("unique_imo")
        .to_dict(orient="index")
    )
    ok_validation = f"Ok {constants.complete_column}"
    for i in range(len(vessels.hull_rating.vessels_list)):
        unique_imo = vessels.hull_rating.vessels_list[i].unique_imo
        if unique_imo in vessels_df_dict:
            for col in columns_to_write:
                value = vessels_df_dict[unique_imo][f"war/{col}"]
                if value is not None:
                    if col in override_column_fields:
                        hxd_node_setter(
                            getattr(vessels.hull_rating.vessels_list[i].war, col),
                            "calculated",
                            value,
                        )
                    else:
                        hxd_node_setter(
                            vessels.hull_rating.vessels_list[i].war,
                            col,
                            value,
                        )
            for col in validation_columns:
                current_validation_value = getattr(war_labels, col)
                hxd_node_setter(
                    vessels.hull_rating.vessels_list[
                        i
                    ].war.war_error_validation_columns,
                    col,
                    vessels_df_dict[unique_imo][f"{col}"],
                )

                hxd_node_setter(
                    war_labels,
                    col,
                    (
                        ok_validation
                        if (
                            (vessels_df_dict[unique_imo][f"{col}"] == "")
                            and (
                                (current_validation_value is None)
                                or (current_validation_value == ok_validation)
                            )
                        )
                        else f"Error {constants.incomplete_column}"
                    ),
                )

    if show_hide_toggles.hull.show_data_mart_warning or (
        hxd.cds.layers[0].coverages.war.section_reference is None
    ):
        return

    data_mart_vessels = (
        hxd.cds.exposure.granular.vessels.hull_rating.data_mart_temp_vessels_list
    )
    if not data_mart_vessels:
        show_hide_toggles.hull.show_data_mart_warning = True
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")
        return
    data_mart_vessels_df = pd_df_from_hx_list(data_mart_vessels)
    data_mart_vessels_df = data_mart_vessels_df.filter(regex="^war_", axis=1)

    data_mart_columns = data_mart_vessels_df.columns.tolist()
    vessels_df = vessels_df[vessels_df[f"{coverage_prefix}is_include_vessel"] == True]
    vessels_df = vessels_df.loc[imo_not_empty_mask]
    vessels_df = vessels_df.rename(
        columns={
            f"{vessels_details_prefix}imo": "imo",
            f"{vessels_details_prefix}name": "name",
            f"{vessels_details_prefix}gross_tonnage": "gross_tonnage",
            f"{vessels_details_prefix}order_percent": "order_percent",
            f"{coverage_prefix}agreed_value": "war_agreed_value",
            f"{coverage_prefix}achieved_rate": "war_achieved_rate",
        }
    )
    vessels_df["war_policy_reference"] = war_rating_summary.section_reference
    vessels_df["war_written_line"] = war_rating_summary.written_line.selected or 0
    vessels_df["is_renewal"] = 1 if hxd.cds.standard_fields.is_renewal else 0
    vessels_df["currency"] = hxd.cds.currencies.source_currency or ""
    vessels_df = vessels_df.filter(items=data_mart_columns).replace({np.nan: None})

    # Dynamically align data types for merge columns
    for col in data_mart_columns:
        # Check if both columns are entirely None/NaN
        if vessels_df[col].isnull().all() and data_mart_vessels_df[col].isnull().all():
            # Convert both to string if all values are None/NaN
            vessels_df[col] = vessels_df[col].astype(str)
            data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)
        else:
            left_dtype = vessels_df[col].dtype
            right_dtype = data_mart_vessels_df[col].dtype

            # If data types are mismatched
            if left_dtype != right_dtype:
                if pd.api.types.is_numeric_dtype(
                    left_dtype
                ) or pd.api.types.is_numeric_dtype(right_dtype):
                    # Convert both to float if either is numeric
                    vessels_df[col] = vessels_df[col].astype(float)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(float)
                elif pd.api.types.is_bool_dtype(
                    left_dtype
                ) or pd.api.types.is_bool_dtype(right_dtype):
                    # Convert both to bool if either is boolean
                    vessels_df[col] = vessels_df[col].astype(bool)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(bool)
                else:
                    # Convert both to string for mixed or object types
                    vessels_df[col] = vessels_df[col].astype(str)
                    data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)

    merged_df = vessels_df.merge(data_mart_vessels_df, how="left", indicator=True)
    show_hide_toggles.hull.show_data_mart_warning = not (
        merged_df["_merge"].eq("both").all()
    )
    if show_hide_toggles.hull.show_data_mart_warning:
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")


def rate_coverages(hxd):
    rating_summary = hxd.cds.layers[0]
    currency = hxd.cds.currencies.source_currency
    show_hide_toggles = hxd.non_cds.show_hide_toggles

    coverages = []
    if show_hide_toggles.hull.show_hull_coverage:
        if hxd.cds.is_iv_coverage:
            coverages = ["iv"]
            if hxd.cds.is_war_coverage:
                coverages.append("war")
        elif hxd.cds.is_war_coverage:
            coverages = ["war"]
    elif show_hide_toggles.loh.show_loh_coverage:
        coverages = ["loh"]
    elif show_hide_toggles.ship_building.show_ship_building_coverage:
        coverages = ["ship_building"]

    if not show_hide_toggles.ship_building.show_ship_building_coverage:
        if show_hide_toggles.loh.show_loh_coverage:
            hxd.non_cds.labels.loh.achieved_premium_label = (
                (f"Gross Achieved Premium 100% - ({currency})")
                if currency
                else "Gross Achieved Premium 100%"
            )

            hxd.non_cds.labels.loh.total_benchmark_premium_label = (
                (f"Total Gross Benchmark Premium - ({currency})")
                if currency
                else "Total Gross Benchmark Premium"
            )
            calculate_loh_values(hxd)
        else:
            populate_coverages_inputs(coverages, rating_summary)
            if hxd.cds.is_iv_coverage:
                hxd.non_cds.show_hide_toggles.iv.iv_not_filter_by_errors = (
                    not hxd.non_cds.show_hide_toggles.iv.iv_filter_by_errors
                )
                calculate_iv_values(hxd)
            if hxd.cds.is_war_coverage:
                hxd.non_cds.show_hide_toggles.war.war_not_filter_by_errors = (
                    not hxd.non_cds.show_hide_toggles.war.war_filter_by_errors
                )
                calculate_war_values(hxd)
    else:
        coverage_rating_summary = rating_summary.coverages.ship_building
        other_deductions = coverage_rating_summary.other_deductions or 0
        coverage_rating_summary.ship_building_show_production_stages_time = (
            True
            if coverage_rating_summary.ship_building_policy_details
            == "Enter the time spent at each production stage"
            else False
        )

        coverage_rating_summary.ship_building_show_overall_time = (
            not coverage_rating_summary.ship_building_show_production_stages_time
        )
        calculate_ship_building_values(hxd)
        brokerage = coverage_rating_summary.brokerage or 0
        coverage_rating_summary.quoted_premium_pro_rated_100pct = (
            coverage_rating_summary.ship_building_achieved_premium or 0
        ) / (1 - brokerage - other_deductions)
