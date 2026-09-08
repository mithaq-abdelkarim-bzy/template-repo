import hx
import numpy as np
import pandas as pd
import math as math
import calendar
from algorithms.rate_utilities import (
    pd_df_from_hx_list,
    hxd_node_setter,
    retrieve_range_values,
    safe_get_and_fillna,
)

from algorithms.helpers.rate_common import (
    MBBEFDG3,
    calculate_final_achieved_net_rate,
)
import algorithms.rate_constants as constants


modelling_prefix = "modelling_"
modelling_static_prefix = "static_"
modelling_behavioural_prefix = "behavioural_"
vessels_details_prefix = "vessel_details/"
validation_columns_prefix = "validation_"


def set_labels(column_labels, label_node, label):
    setattr(column_labels, label_node, label)


def rate_vessels(hxd):
    """
    Rates the vessels based on various factors such as coverage, agreed value, age, and type.

    Args:
        hxd (object): The input object containing vessel data.

    Returns:
        None: If any of the required data is missing or if the commission is equal to 1.

    Steps:
        1. Extract the vessel data from the input object.
        2. Filter the vessel data based on the required fields being not null.
        3. Calculate the benchmark premium and model rate for each vessel using static and behavioural models.
        4. Calculate the pro-rata factor for each vessel based on the inception and expiry dates.
        5. Calculate the achieved premium for each vessel.
        6. Merge the vessel data with a table containing average achieved rates based on vessel type, age, and dwt.
        7. Filter the merged data based on age and dwt bounds.
        8. Remove duplicate vessels based on IMO number, keeping the last occurrence.
        9. Identify rows with missing average achieved rate values and merge them with another table.
        10. Repeat the filtering and duplicate handling for the missing values.
        11. Identify remaining rows with missing values and merge them with a third table.
        12. Combine all the results into a final DataFrame.
        13. Calculate the final net achieved rate and average achieved rate for each vessel.
        14. Update the vessel objects with the calculated rates.
    """
    hxd.cds.exposure.granular.vessels.vessels_defaults.hull.inception_date.calculated = (
        hxd.hx_core.inception_date
    )
    hxd.cds.exposure.granular.vessels.vessels_defaults.hull.expiry_date.calculated = (
        hxd.hx_core.expiry_date
    )
    hxd.non_cds.show_hide_toggles.hull.not_filter_by_errors = (
        not hxd.non_cds.show_hide_toggles.hull.filter_by_errors
    )
    hxd.non_cds.show_hide_toggles.hull.show_data_mart_warning = False
    vessels = hxd.cds.exposure.granular.vessels
    column_labels = hxd.non_cds.labels.required_vessels_columns_labels
    currency = hxd.cds.currencies.source_currency
    if not hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        return
    rating_summary = hxd.cds.layers[0].coverages.hull
    vessels_df = pd_df_from_hx_list(vessels.hull_rating.vessels_list)
    modelling_df = pd_df_from_hx_list(
        hxd.cds.exposure.granular.vessels.hull_rating.modelling_list
    )

    vessels_df = vessels_df.merge(
        modelling_df,
        left_on=[f"unique_imo"],
        right_on=[f"{modelling_prefix}unique_imo"],
        how="left",
    )
    vessels_df = vessels_df[vessels_df[f"{vessels_details_prefix}imo"].notna()]
    converted_imos = pd.to_numeric(
        vessels_df[f"{vessels_details_prefix}imo"], errors="coerce"
    )

    if converted_imos.isna().any():
        hx.errors.validation("Vessel IMO must be numeric")

    # List of tuples containing parameters for set_labels function
    labels = [
        ("name", "Name"),
        ("inception_date", "Inception"),
        ("expiry_date", "Expiry"),
        ("vessel_type", "Type"),
        ("gross_tonnage", "Gross Tonnage"),
        ("dwt", "DWT"),
        ("year_built", "Year Built"),
        ("flag", "Flag"),
        ("vessel_class", "Class"),
        ("order_percent", "Order (%) ie % Beazley"),
        ("freight_conditions", "Freight Conditions"),
        ("vessel_quality", "Vessel/ Machinery Quality"),
        ("area_of_operation", "Area(s) of Operation"),
        ("coverage", "Coverage"),
        ("agreed_value", f"Agreed Value ({currency})"),
        ("deductible", f"Deductible ({currency})"),
        ("achieved_rate", "Achieved Rate (%)"),
        ("achieved_premium", f"Achieved Premium ({currency})"),
        ("static_benchmark_premium", f"Static Benchmark Premium ({currency})"),
        (
            "behavioural_benchmark_premium",
            f"Behavioural Benchmark Premium ({currency})",
        ),
        ("iv_benchmark_premium", f"Benchmark Premium ({currency})"),
        ("war_benchmark_premium", f"Benchmark Premium ({currency})"),
    ]

    for label in labels:
        set_labels(column_labels, *label)

    commission = rating_summary.brokerage or 0

    if vessels_df.empty:
        return

    agreed_value_mask = vessels_df["agreed_value"].notna() & (
        vessels_df["agreed_value"] > 0
    )
    columns_to_write = []
    for model_type in constants.model_types:
        prefix = f"{model_type}_"
        vessels_df[f"{model_type}_benchmark_premium"] = (
            vessels_df[f"{prefix}el_post_uw_adj"] / constants.benchmark_lr
        ) / (1 - commission)

        vessels_df.loc[agreed_value_mask, f"{model_type}_model_rate"] = (
            vessels_df.loc[agreed_value_mask, f"{model_type}_benchmark_premium"]
            / vessels_df.loc[agreed_value_mask, "agreed_value"]
        )

        columns_to_write += [
            (f"{model_type}_benchmark_premium"),
            (f"{model_type}_model_rate"),
        ]

    # Use the behavioural benchmark premium if it exists, otherwise use the static benchmark premium
    vessels_df["premium_to_use"] = vessels_df["behavioural_benchmark_premium"].fillna(
        vessels_df["static_benchmark_premium"]
    )

    vessels_df.loc[agreed_value_mask, "final_model_rate"] = vessels_df.loc[
        agreed_value_mask, "premium_to_use"
    ].div(vessels_df.loc[agreed_value_mask, "agreed_value"])

    vessels_df["premium_to_use_pre_uw_adj"] = vessels_df["premium_to_use"] / (
        1 + vessels_df["uw_adjustment"].fillna(0)
    )

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
    days_in_period = (
        None
        if vessels_df.loc[pro_rata_mask].empty
        else (
            vessels_df.loc[pro_rata_mask, "expiry_date"]
            - vessels_df.loc[pro_rata_mask, "inception_date"]
        ).dt.days
        + 1.0
    )
    days_in_year = vessels_df.loc[pro_rata_mask, "inception_date"].apply(
        lambda x: (366 if calendar.isleap(x.year) else 365)
    )
    vessels_df.loc[pro_rata_mask, "pro_rata"] = (
        float("nan")
        if (days_in_period is None) or (days_in_year is None)
        else (days_in_period / days_in_year)
    )

    vessels_df["achieved_premium"] = (
        vessels_df["agreed_value"]
        * vessels_df["achieved_rate"].fillna(0)
        * vessels_df["pro_rata"]
    )
    columns_to_write.append("achieved_premium")

    table_avg_achieved_rate_filters_type_age_dwt = (
        hx.params.table_avg_achieved_rate_type_age_dwt.rename(
            columns={"achieved_rate": "avg_achieved_rate_type_age_dwt"}
        )
    )

    vessels_df[f"policy_to_built_year_diff"] = (
        pd.to_datetime(vessels_df[f"inception_date"]).dt.year
        - (vessels_df[f"year_built"])
    ).clip(lower=0)

    # Merge the DataFrames on vessel_type
    criteria_3_vessels_df = vessels_df.merge(
        table_avg_achieved_rate_filters_type_age_dwt,
        left_on=[f"vessel_type"],
        right_on=["vessel_type"],
        how="left",
    )

    if len(criteria_3_vessels_df) > 0:

        criteria_3_vessels_df[["dwt", "year_built"]] = criteria_3_vessels_df[
            ["dwt", "year_built"]
        ].fillna(1)

        criteria_3_vessels_df = criteria_3_vessels_df[
            (
                criteria_3_vessels_df["age_lower_bound"]
                <= criteria_3_vessels_df["policy_to_built_year_diff"]
            )
            & (
                criteria_3_vessels_df["age_upper_bound"]
                >= criteria_3_vessels_df["policy_to_built_year_diff"]
            )
            & (
                criteria_3_vessels_df["dwt_lower_bound"]
                <= criteria_3_vessels_df[f"dwt"]
            )
            & (
                criteria_3_vessels_df["dwt_upper_bound"]
                >= criteria_3_vessels_df[f"dwt"]
            )
        ]

        """
        In some cases there are multiple return values for the same vessel_type, age_range and dwt_range. 
        In this case we take the first sorted value.
    
        Example of the table:
        IMO = 5212696
        DWT = 282
        Year Built = 1959
    
        With any inception_date that will make the vessel policy_to_built_year_diff greater than 30 years old
        It will keep those two rows after the filteration:
        Fishing (General) - FFS,30,999,0,1000,484704.9667056260,10849719.557132,12,0.044674423532634800000000
        Fishing (General) - FFS,50,999,0,1000,86805.9575856970,2576810.424057,3,0.033687366666666700000000
    
        The last row will be taken as the achieved_rate for the vessel as it matches the criteria more accuratley.
        """
        criteria_3_vessels_df = criteria_3_vessels_df.drop_duplicates(
            subset=f"unique_imo", keep="last"
        )

    vessels_df = vessels_df.merge(
        criteria_3_vessels_df[[f"unique_imo", "avg_achieved_rate_type_age_dwt"]],
        on=f"unique_imo",
        how="left",
    )

    vessels_df["final_achieved_net_rate"] = calculate_final_achieved_net_rate(
        df=vessels_df,
        criteria_column="avg_achieved_rate_type_age_dwt",
        coverage_factor_column=f"{modelling_static_prefix}coverage_factor",
    )

    # Step 4: Identify rows with missing avg_achieved_rate_type_age_dwt values
    criteria_2_vessels_df = vessels_df[
        vessels_df["avg_achieved_rate_type_age_dwt"].isna()
    ]
    if not criteria_2_vessels_df.empty:
        table_avg_achieved_rate_filters_type_age = (
            hx.params.table_avg_achieved_rate_type_age.rename(
                columns={"achieved_rate": "avg_achieved_rate_type_age"}
            )
        )
        # Step 5: Merge these rows with the second table
        filtered_criteria_2_vessels_df = criteria_2_vessels_df.merge(
            table_avg_achieved_rate_filters_type_age,
            left_on=[f"vessel_type"],
            right_on=["vessel_type"],
            how="left",
        )

        if len(filtered_criteria_2_vessels_df) > 0:

            filtered_criteria_2_vessels_df["year_built"] = (
                filtered_criteria_2_vessels_df["year_built"].fillna(1)
            )

            # Step 6: Repeat the filtering and duplicate handling
            filtered_criteria_2_vessels_df = filtered_criteria_2_vessels_df[
                (
                    filtered_criteria_2_vessels_df["age_lower_bound"]
                    <= filtered_criteria_2_vessels_df["policy_to_built_year_diff"]
                )
                & (
                    filtered_criteria_2_vessels_df["age_upper_bound"]
                    >= filtered_criteria_2_vessels_df["policy_to_built_year_diff"]
                )
            ]
            filtered_criteria_2_vessels_df = (
                filtered_criteria_2_vessels_df.drop_duplicates(
                    subset=f"unique_imo", keep="last"
                )
            )

        vessels_df = vessels_df.merge(
            filtered_criteria_2_vessels_df[
                [f"unique_imo", "avg_achieved_rate_type_age"]
            ],
            on=f"unique_imo",
            how="left",
        )

        vessels_df["final_achieved_net_rate"] = vessels_df[
            "final_achieved_net_rate"
        ].fillna(
            calculate_final_achieved_net_rate(
                df=vessels_df,
                criteria_column="avg_achieved_rate_type_age",
                coverage_factor_column=f"{modelling_static_prefix}coverage_factor",
            )
        )

        criteria_1_vessels_df = vessels_df[
            vessels_df["avg_achieved_rate_type_age"].isna()
        ]

        if not criteria_1_vessels_df.empty:

            table_avg_achieved_rate_filters_type = (
                hx.params.table_avg_achieved_rate_type.rename(
                    columns={"achieved_rate": "avg_achieved_rate_type"}
                )
            )

            criteria_1_vessels_df = criteria_1_vessels_df.merge(
                table_avg_achieved_rate_filters_type,
                left_on=[f"vessel_type"],
                right_on=["vessel_type"],
                how="left",
            )

            vessels_df = vessels_df.merge(
                criteria_1_vessels_df[[f"unique_imo", "avg_achieved_rate_type"]],
                on=f"unique_imo",
                how="left",
            )

            vessels_df["final_achieved_net_rate"] = vessels_df[
                "final_achieved_net_rate"
            ].fillna(
                calculate_final_achieved_net_rate(
                    df=vessels_df,
                    criteria_column="avg_achieved_rate_type",
                    coverage_factor_column=f"{modelling_static_prefix}coverage_factor",
                )
            )

    vessels_df["average_achieved_rate"] = vessels_df["final_achieved_net_rate"] / (1 - commission)
    columns_to_write.append("average_achieved_rate")

    coverage_table = hx.params.table_coverage_factor
    vessels_df["coverage_factor"] = vessels_df["coverage"].map(
        coverage_table.set_index("coverage")["factor"]
    )

    vessel_types_table = hx.params.table_vessel_types
    vessels_df["vessel_type_factor"] = vessels_df[f"vessel_type"].map(
        vessel_types_table.set_index("vessel_type")["factor"]
    )

    dwt_mask = vessels_df[f"dwt"].notna()

    dwt_table = hx.params.table_dwt_factor
    min_dwt = min(vessels_df[f"dwt"].min(), 0)
    max_dwt = max(vessels_df[f"dwt"].max(), 500)
    if not (math.isnan(min_dwt) or math.isnan(max_dwt) or min_dwt < 0):
        dwt_values = retrieve_range_values(
            table=dwt_table,
            lower_bound=min_dwt,
            upper_bound=max_dwt,
            lower_search_key="lower_bound",
            upper_search_key="upper_bound",
        )
        # Create bins and labels
        bins = dwt_values["lower_bound"].tolist() + [dwt_values["upper_bound"].iloc[-1]]
        labels = dwt_values["factor"]

        # Bin the dwt values and map to factors
        vessels_df.loc[dwt_mask, "dwt_factor"] = pd.cut(
            vessels_df.loc[dwt_mask, f"dwt"],
            bins=bins,
            labels=labels,
            right=False,  # Make the bins left-inclusive
        ).astype(float)

    age_table = hx.params.table_age_factor
    max_age = age_table["age"].max()
    max_age_factor = age_table["factor"].max()
    # Difference between inception and built date in years, with a minimum of 0
    if not (math.isnan(max_age) or math.isnan(max_age_factor)):
        vessels_df["inception_and_year_built_diff"] = (
            pd.to_datetime(vessels_df[f"inception_date"]).dt.year
            - vessels_df[f"year_built"]
        ).clip(lower=0)

        # Rename 'age' column in age_table
        age_table = age_table.rename(columns={"age": "age_renamed"})

        vessels_df = vessels_df.merge(
            age_table,
            left_on=["inception_and_year_built_diff"],
            right_on=["age_renamed"],
            how="left",
        ).rename(columns={"factor": "age_factor"})

        vessels_df["age_factor"] = np.where(
            vessels_df["inception_and_year_built_diff"] > max_age,
            max_age_factor,
            vessels_df["age_factor"],
        )

    flag_table = hx.params.table_flags
    vessels_df["flag_factor"] = vessels_df[f"flag"].map(
        flag_table.set_index("vessel_flag")["factor"]
    )

    class_table = hx.params.table_vessel_classifications
    vessels_df["vessel_class_factor"] = vessels_df[
        f"{vessels_details_prefix}vessel_class"
    ].map(class_table.set_index("classification_society")["factor"])

    # Apply the MBBEFDG3 function to each row
    mbbedfg3_mask = (
        vessels_df["deductible"].notna()
        & vessels_df["agreed_value"].notna()
        & vessels_df["agreed_value"]
        > 0
    )
    modelling_parameters_table = hx.params.table_modelling_parameters
    MBBEFDG3_param = modelling_parameters_table.loc[
        modelling_parameters_table["parameter"] == "MBBDFDHullParam", "value"
    ].iloc[0]
    vessels_df.loc[mbbedfg3_mask, "mbbefdg"] = vessels_df.loc[mbbedfg3_mask].apply(
        lambda row: 1
        - MBBEFDG3(MBBEFDG3_param, row["deductible"] / row["agreed_value"]),
        axis=1,
    )

    base = (constants.iv_base_rate * 4) * (
        ((constants.iv_plan_ulr) * (1 - constants.iv_plan_commission))
        / constants.benchmark_lr
    )

    # Calculate rate_pre_uw_adj
    vessels_df["rate_pre_uw_adj"] = (
        safe_get_and_fillna(vessels_df, "pro_rata", 1)
        * safe_get_and_fillna(vessels_df, "coverage_factor", 1)
        * safe_get_and_fillna(vessels_df, "vessel_type_factor", 1)
        * safe_get_and_fillna(vessels_df, "dwt_factor", 1)
        * safe_get_and_fillna(vessels_df, "age_factor", 1)
        * safe_get_and_fillna(vessels_df, "flag_factor", 1)
        * safe_get_and_fillna(vessels_df, "vessel_class_factor", 1)
        * safe_get_and_fillna(vessels_df, "mbbefdg", 1)
    )

    vessels_df["rate_post_uw_adj"] = (
        vessels_df["rate_pre_uw_adj"]
        * vessels_df[f"{modelling_prefix}freight_conditions"]
        * vessels_df[f"{modelling_prefix}area_of_operation"]
        * vessels_df[f"{modelling_prefix}vessel_quality"]
        * vessels_df[f"{modelling_prefix}owner_quality"]
        * vessels_df[f"{modelling_prefix}fleet_casualty_history"]
    )

    vessels_df["first_rate_model_rate"] = vessels_df["rate_post_uw_adj"] / (
        1 - commission
    )
    columns_to_write.append("first_rate_model_rate")

    is_behvaoural_data_mask = vessels_df["age"].notna() & (vessels_df["age"] > 0)
    vessels_df.loc[is_behvaoural_data_mask, "is_behavioural_data"] = vessels_df.loc[
        is_behvaoural_data_mask, "age"
    ].notna()

    vessels_df["is_behavioural_data"] = vessels_df["is_behavioural_data"].fillna(False)
    columns_to_write.append("is_behavioural_data")

    vessels_df[f"{validation_columns_prefix}name"] = np.where(
        vessels_df[f"{vessels_details_prefix}name"].isna(),
        f"{constants.incomplete_column} Name must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}inception_date"] = np.where(
        vessels_df[f"inception_date"].isna(),
        f"{constants.incomplete_column} Inception Date must have a value",
        np.where(
            vessels_df[f"inception_date"] < pd.Timestamp(hxd.hx_core.inception_date),
            f"{constants.incomplete_column} Inception Date must be greater than or equal to the Policy inception date ({hxd.hx_core.inception_date})",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}expiry_date"] = np.where(
        vessels_df[f"expiry_date"].isna(),
        f"{constants.incomplete_column} Expiry Date must have a value",
        np.where(
            vessels_df[f"expiry_date"] > pd.Timestamp(hxd.hx_core.expiry_date),
            f"{constants.incomplete_column} Expiry Date must be less than or equal to the Policy expiry date ({hxd.hx_core.expiry_date})",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}vessel_type"] = np.where(
        vessels_df[f"vessel_type"].isna(),
        f"{constants.incomplete_column} Vessel Type must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}gross_tonnage"] = np.where(
        vessels_df[f"{vessels_details_prefix}gross_tonnage"].isna(),
        f"{constants.incomplete_column} Gross Tonnage must have a value",
        np.where(
            vessels_df[f"{vessels_details_prefix}gross_tonnage"] < 0,
            f"{constants.incomplete_column} Gross Tonnage Must be greater than 0",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}dwt"] = np.where(
        vessels_df[f"dwt"].isna(),
        f"{constants.incomplete_column} DWT must have a value",
        np.where(
            vessels_df[f"dwt"] < 0,
            f"{constants.incomplete_column} DWT Must be greater than 0",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}year_built"] = np.where(
        vessels_df[f"year_built"].isna(),
        f"{constants.incomplete_column} Year Built must have a value",
        np.where(
            vessels_df[f"year_built"] < 0,
            f"{constants.incomplete_column} Year Built Must be greater than 0",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}flag"] = np.where(
        vessels_df[f"flag"].isna(),
        f"{constants.incomplete_column} Flag must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}vessel_class"] = np.where(
        vessels_df[f"{vessels_details_prefix}vessel_class"].isna(),
        f"{constants.incomplete_column} Vessel Class must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}order_percent"] = np.where(
        vessels_df[f"{vessels_details_prefix}order_percent"].isna(),
        f"{constants.incomplete_column} Order (%) ie % Beazley must have a value",
        np.where(
            (vessels_df[f"{vessels_details_prefix}order_percent"] < 0)
            | (vessels_df[f"{vessels_details_prefix}order_percent"] > 1),
            f"{constants.incomplete_column} Order (%) ie % Beazley Must be between 0 and 100",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}freight_conditions"] = np.where(
        vessels_df[f"{vessels_details_prefix}freight_conditions"].isna(),
        f"{constants.incomplete_column} Freight Conditions must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}vessel_quality"] = np.where(
        vessels_df[f"{vessels_details_prefix}vessel_quality"].isna(),
        f"{constants.incomplete_column} Vessel/ Machinery Quality must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}area_of_operation"] = np.where(
        vessels_df[f"{vessels_details_prefix}area_of_operation"].isna(),
        f"{constants.incomplete_column} Area(s) of Operation must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}coverage"] = np.where(
        vessels_df["coverage"].isna(),
        f"{constants.incomplete_column} Coverage must have a value",
        "",
    )

    vessels_df[f"{validation_columns_prefix}agreed_value"] = np.where(
        vessels_df["agreed_value"].isna(),
        f"{constants.incomplete_column} Agreed Value must have a value",
        np.where(
            vessels_df["agreed_value"] < 0,
            f"{constants.incomplete_column} Agreed Value Must be greater than 0",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}deductible"] = np.where(
        vessels_df["deductible"].isna(),
        f"{constants.incomplete_column} Deductible must have a value",
        np.where(
            vessels_df["deductible"] < 0,
            f"{constants.incomplete_column} Deductible Must be greater than 0",
            "",
        ),
    )

    vessels_df[f"{validation_columns_prefix}achieved_rate"] = np.where(
        vessels_df["achieved_rate"].isna(),
        f"{constants.incomplete_column} Achieved Rate must have a value",
        np.where(
            (vessels_df["achieved_rate"] < 0),
            f"{constants.incomplete_column} Achieved Rate Must be greater than 0",
            "",
        ),
    )

    validation_columns = [
        f"{validation_columns_prefix}name",
        f"{validation_columns_prefix}inception_date",
        f"{validation_columns_prefix}expiry_date",
        f"{validation_columns_prefix}vessel_type",
        f"{validation_columns_prefix}gross_tonnage",
        f"{validation_columns_prefix}dwt",
        f"{validation_columns_prefix}year_built",
        f"{validation_columns_prefix}flag",
        f"{validation_columns_prefix}vessel_class",
        f"{validation_columns_prefix}order_percent",
        f"{validation_columns_prefix}freight_conditions",
        f"{validation_columns_prefix}vessel_quality",
        f"{validation_columns_prefix}area_of_operation",
        f"{validation_columns_prefix}coverage",
        f"{validation_columns_prefix}agreed_value",
        f"{validation_columns_prefix}deductible",
        f"{validation_columns_prefix}achieved_rate",
    ]

    has_error = vessels_df[validation_columns].notna() & (
        vessels_df[validation_columns] != ""
    )

    # Set the has_error column in vessels_df to True if any column has a non-null and non-empty value
    vessels_df["has_error"] = has_error.any(axis=1)
    hxd.non_cds.labels.hull.validation_error_message = (
        f"{constants.incomplete_column} Fix the invalid entries"
        if vessels_df["has_error"].any()
        else f"{constants.complete_column} All entries are valid."
    )

    columns_to_write.append("has_error")

    vessels_df_dict = vessels_df.set_index("unique_imo").to_dict(orient="index")
    ok_validation = f"Ok {constants.complete_column}"
    for i in range(len(vessels.hull_rating.vessels_list)):
        unique_imo = vessels.hull_rating.vessels_list[i].unique_imo
        if unique_imo in vessels_df_dict:
            for col in columns_to_write:
                hxd_node_setter(
                    vessels.hull_rating.vessels_list[i],
                    col,
                    vessels_df_dict[unique_imo][f"{col}"],
                )
            for col in validation_columns:
                current_validation_value = getattr(hxd.non_cds.labels.hull, col)
                hxd_node_setter(
                    vessels.hull_rating.vessels_list[i].error_validation_columns,
                    col,
                    vessels_df_dict[unique_imo][f"{col}"],
                )

                hxd_node_setter(
                    hxd.non_cds.labels.hull,
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

    if hxd.cds.layers[0].coverages.hull.section_reference is None:
        return
    data_mart_vessels = (
        hxd.cds.exposure.granular.vessels.hull_rating.data_mart_temp_vessels_list
    )
    if (not data_mart_vessels) or (len(data_mart_vessels) != len(vessels_df)):
        hxd.non_cds.show_hide_toggles.hull.show_data_mart_warning = True
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")
        return
    data_mart_vessels_df = pd_df_from_hx_list(data_mart_vessels)
    data_mart_vessels_df["inception_date"] = pd.to_datetime(
        data_mart_vessels_df["inception_date"]
    )
    data_mart_vessels_df["expiry_date"] = pd.to_datetime(
        data_mart_vessels_df["expiry_date"]
    )
    data_mart_vessels_df = data_mart_vessels_df.drop(
        data_mart_vessels_df.filter(regex="^(iv_|war_)").columns, axis=1
    )

    data_mart_columns = data_mart_vessels_df.columns.tolist()
    vessels_df = vessels_df.rename(
        columns={
            f"{vessels_details_prefix}imo": "imo",
            f"{vessels_details_prefix}name": "name",
            f"{vessels_details_prefix}gross_tonnage": "gross_tonnage",
            f"{vessels_details_prefix}order_percent": "order_percent",
        }
    )

    vessels_df["hull_policy_reference"] = hxd.cds.layers[
        0
    ].coverages.hull.section_reference
    vessels_df["hull_written_line"] = rating_summary.written_line or 0
    vessels_df["is_renewal"] = 1 if hxd.cds.standard_fields.is_renewal else 0
    vessels_df["currency"] = hxd.cds.currencies.source_currency or ""
    vessels_df = vessels_df.filter(items=data_mart_columns)

    # Dynamically align data types for merge columns
    for col in data_mart_columns:
        left_dtype = vessels_df[col].dtype
        right_dtype = data_mart_vessels_df[col].dtype

        # If data types are mismatched
        if left_dtype != right_dtype:
            if pd.api.types.is_numeric_dtype(
                left_dtype
            ) or pd.api.types.is_numeric_dtype(right_dtype):
                # Convert both to float if both are numeric
                vessels_df[col] = vessels_df[col].astype(float)
                data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(float)
            elif pd.api.types.is_bool_dtype(left_dtype) or pd.api.types.is_bool_dtype(
                right_dtype
            ):
                # Convert both to bool if both are boolean
                vessels_df[col] = vessels_df[col].astype(bool)
                data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(bool)
            else:
                # Convert both to string for mixed or object types
                vessels_df[col] = vessels_df[col].astype(str)
                data_mart_vessels_df[col] = data_mart_vessels_df[col].astype(str)

    hxd.non_cds.show_hide_toggles.hull.show_data_mart_warning = not (
        vessels_df.merge(data_mart_vessels_df, how="left", indicator=True)["_merge"]
        .eq("both")
        .all()
    )
    if hxd.non_cds.show_hide_toggles.hull.show_data_mart_warning:
        hx.errors.validation(f"{hxd.non_cds.labels.hull.data_mart_warning_message}")
