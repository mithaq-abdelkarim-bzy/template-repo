import hx
import datetime
from algorithms.rate_utilities import pd_df_from_hx_list, hxd_node_setter
import algorithms.rate_constants as constants
from algorithms import parameter_tables_schema as params
import pandas as pd
import numpy as np


def set_dynamic_labels(
    non_cds_labels, risk_information_currency, experience_rating_currency, current_year
):
    ship_building_experience_rating = non_cds_labels.ship_building.experience_rating
    ship_building_experience_rating.currency_experience_rating_data_input_gross_premium_label = (
        f"Gross Premium - Shared Line ({experience_rating_currency})"
        if experience_rating_currency
        else "Gross Premium - Shared Line"
    )
    ship_building_experience_rating.currency_experience_rating_data_input_total_incurred_label = (
        f"Total Incurred - Shared Line ({experience_rating_currency})"
        if experience_rating_currency
        else "Total Incurred - Shared Line"
    )
    ship_building_experience_rating.currency_experience_rating_data_input_att_incurred_label = (
        f"Attritional Incurred  - Shared Line ({experience_rating_currency})"
        if experience_rating_currency
        else "Attritional Incurred  - Shared Line"
    )
    ship_building_experience_rating.currency_experience_rating_data_input_large_incurred_label = (
        f"Large Incurred - Shared Line ({experience_rating_currency})"
        if experience_rating_currency
        else "Large Incurred - Shared Line"
    )
    ship_building_experience_rating.currency_experience_rating_projection_net_premium_label = (
        f"Net Premium ({experience_rating_currency})"
        if experience_rating_currency
        else "Net Premium "
    )
    ship_building_experience_rating.currency_experience_rating_projection_att_incurred_label = (
        f"Attritional Incurred ({experience_rating_currency})"
        if experience_rating_currency
        else "Attritional Incurred"
    )
    ship_building_experience_rating.currency_experience_rating_projection_large_incurred_label = (
        f"Large Incurred ({experience_rating_currency})"
        if experience_rating_currency
        else "Large Incurred"
    )
    ship_building_experience_rating.currency_experience_rating_projection_on_levelled_net_premium_label = (
        f"On-Levelled Net Premium ({experience_rating_currency})"
        if experience_rating_currency
        else "On-Levelled Net Premium"
    )
    ship_building_experience_rating.currency_experience_rating_projection_on_levelled_att_incurred_label = (
        f"On-Levelled Attritional Claims ({experience_rating_currency})"
        if experience_rating_currency
        else "On-Levelled Attritional Claims"
    )
    ship_building_experience_rating.currency_experience_rating_projection_on_levelled_large_claims_label = (
        f"On-Levelled Large Claims ({experience_rating_currency})"
        if experience_rating_currency
        else "On-Levelled Large Claims"
    )
    ship_building_experience_rating.current_year_experience_rating_rate_change_label = (
        f"Rate Change for current year ({current_year})"
        if current_year
        else "Rate Change for current year"
    )
    ship_building_experience_rating.currency_experience_claims_cost_label = (
        f"Experience Claims Cost ({risk_information_currency})"
        if risk_information_currency
        else "Experience Claims Cost"
    )

    ship_building_experience_rating.currency_experience_claims_net_benchmark_premium_pure_experience = (
        f"Net Benchmark Premium - Pure Experience ({risk_information_currency})"
        if risk_information_currency
        else "Net Benchmark Premium - Pure Experience"
    )

    ship_building_experience_rating.currency_experience_rating_data_input_net_premium_shared_line_label = (
        f"Net Premium - Shared Line ({experience_rating_currency})"
        if experience_rating_currency
        else "Net Premium - Shared Line"
    )

    ship_building_experience_rating.currency_experience_exchange_rate_label = (
        f"Exchange Rate: 1 USD = ? {experience_rating_currency}"
        if experience_rating_currency
        else "Exchange Rate: 1 USD"
    )


def rate_experience_rating(hxd):
    if not hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage:
        return
    experience_rating = hxd.cds.experience_rating.ship_building
    experience_rating_currency = experience_rating.claims_currency
    risk_information_currency = hxd.cds.currencies.source_currency
    non_cds_labels = hxd.non_cds.labels
    claims_date = experience_rating.claims_date
    inception_date = hxd.cds.standard_fields.inception_date
    current_year = claims_date.year if claims_date else None
    inception_year = inception_date.year if inception_date else None
    current_year_rate_change = experience_rating.current_year_rate_change
    experience_rating_currency = experience_rating.claims_currency

    is_dev = False
    bp_class = "Shipbuilders" if is_dev else "Hull"
    if not bp_class:
        return
    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = (
        hx.params.table_original_rater_params if is_dev else params.tp_parameters.df()
    )
    tp_year = inception_date.year
    if tp_year in list(tp_params_df["year"]):
        tp_year = tp_year
    else:
        tp_year = tp_params_df[tp_params_df["business_plan_class"] == bp_class][
            "year"
        ].max()
    fx_rates_df = params.fx_rates.df()
    experience_rating.claims_fx_rate.calculated = (
        None
        if experience_rating_currency is None
        else (
            fx_rates_df[(fx_rates_df["ccy"] == experience_rating_currency)][
                "fx_rate"
            ].iloc[0]
            if ((experience_rating_currency in list(fx_rates_df["ccy"])))
            else 1
        )
    )

    set_dynamic_labels(
        non_cds_labels,
        risk_information_currency,
        experience_rating_currency,
        current_year,
    )
    data_input_experience_table = experience_rating.data_input_experience_table
    extracted_policies = experience_rating.extracted_policies
    data_input_df, data_input_columns_to_write, data_input_override_column_fields = (
        process_data_input_experience_rating(
            pd_df_from_hx_list(data_input_experience_table),
            inception_year,
            (
                pd.DataFrame()
                if len(extracted_policies) == 0
                else pd_df_from_hx_list(extracted_policies)
            ),
            experience_rating.claims_fx_rate.selected,
        )
    )

    if not data_input_df.empty:
        hxd.non_cds.show_hide_toggles.ship_building.show_experience_number_of_vessels_warning = (
            data_input_df["number_of_vessels"].fillna(0).sum() == 0
        )

        is_signed_line_warning = (
            (data_input_df["signed_line"].isna() | (data_input_df["signed_line"] == 0))
            & (data_input_df["premium"].notna() & (data_input_df["premium"] != 0))
        ).any()
        hxd.non_cds.show_hide_toggles.ship_building.show_experience_signed_line_warning = (
            is_signed_line_warning
        )
        is_number_of_vessels_warning = (
            data_input_df["number_of_vessels"].fillna(0).sum() == 0
        )
        hxd.non_cds.show_hide_toggles.ship_building.show_experience_number_of_vessels_warning = (
            is_number_of_vessels_warning
        )
        hxd.non_cds.show_hide_toggles.ship_building.show_experience_rating_warning = (
            is_signed_line_warning or is_number_of_vessels_warning
        )

    ulr_projection_experience_table = experience_rating.ulr_projection_experience_table
    (
        ulr_projection_df,
        ulr_projection_columns_to_write,
    ) = process_ulr_projection_table(
        data_input_df,
        pd_df_from_hx_list(ulr_projection_experience_table),
        claims_date,
        current_year_rate_change,
        inception_date,
    )

    for i in range(len(data_input_experience_table)):
        for col in data_input_columns_to_write:
            if col in data_input_override_column_fields:
                hxd_node_setter(
                    getattr(data_input_experience_table[i], col),
                    "calculated",
                    data_input_df[f"{col}"].iloc[i],
                )
            else:
                hxd_node_setter(
                    data_input_experience_table[i],
                    col,
                    data_input_df[f"{col}"].iloc[i],
                )

    for i in range(len(ulr_projection_experience_table)):
        for col in ulr_projection_columns_to_write:
            hxd_node_setter(
                ulr_projection_experience_table[i],
                col,
                ulr_projection_df[f"{col}"].iloc[i],
            )

    ulr_projection_df = pd_df_from_hx_list(ulr_projection_experience_table)
    on_levelled_premium_sum = np.dot(
        ulr_projection_df["on_levelled_premium"].fillna(0),
        ulr_projection_df["is_include_year"].fillna(0),
    )

    on_levelled_large_incurred_lr_on_levelled_premium_product_sum = np.sum(
        ulr_projection_df["on_levelled_large_incurred_lr"].fillna(0)
        * ulr_projection_df["on_levelled_premium"].fillna(0)
        * ulr_projection_df["is_include_year"].fillna(0)
    )

    try:
        hxd_node_setter(
            experience_rating.large_load_selection,
            "average_on_levelled_net_large_lr",
            (
                0
                if on_levelled_premium_sum == 0
                else (
                    on_levelled_large_incurred_lr_on_levelled_premium_product_sum
                    / on_levelled_premium_sum
                )
            ),
        )
    except Exception as e:
        experience_rating.large_load_selection.average_on_levelled_net_large_lr = 0

    user_number_of_years_expected_large_loss = (
        experience_rating.large_load_selection.user_selected.user_number_of_years_expected_large_loss
    )

    user_average_net_lr_of_large_loss = (
        experience_rating.large_load_selection.user_selected.user_average_net_lr_of_large_loss
    )

    experience_rating.large_load_selection.user_selected.selected_large_load = (
        None
        if (
            (user_number_of_years_expected_large_loss == 0)
            or (user_number_of_years_expected_large_loss is None)
            or (user_average_net_lr_of_large_loss is None)
        )
        else (
            user_average_net_lr_of_large_loss / user_number_of_years_expected_large_loss
        )
    )

    table_ulr_projection = hx.params.table_ulr_projection
    parameters_dict = table_ulr_projection.set_index("parameter")["value"].to_dict()
    large_return_period_portfolio = parameters_dict["large_return_period_portfolio"]
    avg_large_lr_portfolio = parameters_dict["avg_large_lr_portfolio"]

    experience_rating.large_load_selection.portfolio_load_guidance.guidance_number_of_years_expected_large_loss = (
        large_return_period_portfolio
    )

    experience_rating.large_load_selection.portfolio_load_guidance.guidance_average_net_lr_of_large_loss = (
        avg_large_lr_portfolio
    )

    experience_rating.large_load_selection.portfolio_load_guidance.portfolio_large_load = (
        None
        if (
            (
                experience_rating.large_load_selection.portfolio_load_guidance.guidance_number_of_years_expected_large_loss
                == 0
            )
            or (
                experience_rating.large_load_selection.portfolio_load_guidance.guidance_number_of_years_expected_large_loss
                is None
            )
            or (
                experience_rating.large_load_selection.portfolio_load_guidance.guidance_average_net_lr_of_large_loss
                is None
            )
        )
        else (
            experience_rating.large_load_selection.portfolio_load_guidance.guidance_average_net_lr_of_large_loss
            / experience_rating.large_load_selection.portfolio_load_guidance.guidance_number_of_years_expected_large_loss
        )
    )

    att_ulr_on_levelled_premium_product_sum = np.sum(
        ulr_projection_df["attritional_ulr"].fillna(0)
        * ulr_projection_df["on_levelled_premium"].fillna(0)
        * ulr_projection_df["is_include_year"].fillna(0)
    )

    try:
        hxd_node_setter(
            experience_rating.experience_pricing_results,
            "average_attritional_ulr",
            (
                0
                if on_levelled_premium_sum == 0
                else (att_ulr_on_levelled_premium_product_sum / on_levelled_premium_sum)
            ),
        )
    except:
        experience_rating.experience_pricing_results.average_attritional_ulr = 0

    experience_rating.experience_pricing_results.large_load = (
        experience_rating.large_load_selection.user_selected.selected_large_load
        or experience_rating.large_load_selection.portfolio_load_guidance.portfolio_large_load
    )

    experience_rating.experience_pricing_results.total_ulr = (
        experience_rating.experience_pricing_results.average_attritional_ulr
        + experience_rating.experience_pricing_results.large_load
    )

    achieved_premium = hxd.cds.layers[
        0
    ].coverages.ship_building.ship_building_achieved_premium

    nmp_load = tp_params_df[
        (tp_params_df["business_plan_class"] == bp_class)
        & (tp_params_df["year"] == tp_year)
    ]["nmp_load"].iloc[0]

    experience_rating.experience_pricing_results.experience_claims_cost = (
        None
        if ((achieved_premium is None) or (achieved_premium == 0))
        else (1 + nmp_load)
        * achieved_premium
        * experience_rating.experience_pricing_results.total_ulr
    )

    if ulr_projection_df["premium"].any():
        hxd.cds.layers[0].coverages.ship_building.ship_building_experience_premium = (
            experience_rating.experience_pricing_results.net_benchmark_premium_pure_experience
        ) = (
            None
            if not experience_rating.experience_pricing_results.experience_claims_cost
            else (
                (
                    experience_rating.experience_pricing_results.experience_claims_cost
                    or 0
                )
                / constants.benchmark_lr
            )
        )

    if data_input_df["yoa"].notna().all() and ulr_projection_df["yoa"].notna().all():
        # Merge the dataframes on the 'yoa' column
        merged_df = data_input_df.merge(
            ulr_projection_df,
            left_on="yoa",
            right_on="yoa",
            how="left",
            suffixes=("", "_proj"),
        )

        # Filter the merged dataframe to include only rows where 'is_include_year' is 1
        filtered_df = merged_df[merged_df["is_include_year_proj"] == 1]

        experience_rating.experience_weighting_calculation.total_number_of_vessels = (
            filtered_df["number_of_vessels"].sum()
        )

    table_vessels_experience_weighting = hx.params.table_vessels_experience_weighting
    vessels = table_vessels_experience_weighting["number_of_vessels"]
    weights = table_vessels_experience_weighting["weight"]

    if (
        experience_rating.experience_weighting_calculation.total_number_of_vessels
        is None
    ) or (
        experience_rating.experience_weighting_calculation.total_number_of_vessels == 0
    ):
        return

    experience_wighting_interpolated_value = np.interp(
        experience_rating.experience_weighting_calculation.total_number_of_vessels,
        vessels,
        weights,
    )

    # Clip the result to the range [0, 0.25]
    experience_weighting_clipped_value = np.clip(
        experience_wighting_interpolated_value, 0, 0.25
    )

    hxd.cds.layers[0].coverages.ship_building.ship_building_experience_weighting = (
        experience_rating.experience_weighting_calculation.experience_weighting
    ) = experience_weighting_clipped_value

    """
    Processes the data input for experience rating.

    This function processes the data input DataFrame for experience rating by performing
    various calculations and updates based on the provided parameters. It ensures that
    certain columns are updated and written back to the DataFrame, even if the function
    needs to end early.

    The reason for splitting the logic into a function is to allow for early termination of the function while still ensuring that the necessary columns are written back to the DataFrame. 
    This is achieved by maintaining lists of columns to write (columns_to_write) and columns that were overridden (override_column_fields), 
    which are returned along with the updated DataFrame. 
    This approach ensures that the data integrity is maintained and the necessary updates are applied, 
    even if the function does not complete all its intended operations.

    Parameters:
    - data_input_df: The input DataFrame containing the data to be processed.
    - current_year: The current year to be used for calculations.

    Returns:
    - data_input_df: The updated DataFrame with processed data.
    - columns_to_write: A list of columns that were updated and need to be written back.
    - override_column_fields: A list of columns that were overridden and need to be written back.
    """


def process_data_input_experience_rating(
    data_input_df, current_year, extracted_policies_df, currency_exchange_rate
):
    data_input_columns_to_write = []
    data_input_override_column_fields = []
    if current_year:
        start_year = current_year - 1
        years = [
            start_year - i
            for i in range(constants.ship_building_experience_rating_years - 1, -1, -1)
        ]

        data_input_df["yoa"] = years
        data_input_columns_to_write.append("yoa")

        if len(extracted_policies_df) > 0:
            extracted_policies_df["yoa"] = (
                extracted_policies_df["yoa"].fillna(0).astype(int)
            )
            data_input_df = data_input_df.merge(
                extracted_policies_df,
                left_on="yoa",
                right_on="yoa",
                how="left",
                suffixes=("", "_populated"),
            )

            neglected_columns = [
                "yoa",
                "policy_reference",
                "written_or_estimated_premium",
            ]
            for column in extracted_policies_df.columns:
                if column not in neglected_columns:
                    data_input_df.loc[
                        data_input_df[column + "_selected"].isna(), column
                    ] = data_input_df.loc[
                        data_input_df[column + "_selected"].isna(),
                        column + "_populated",
                    ].combine_first(
                        data_input_df.loc[
                            data_input_df[column + "_selected"].isna(), column
                        ]
                    )
                    data_input_columns_to_write.append(column)
                    data_input_override_column_fields.append(column)

            previous_insurer_mask = data_input_df["previous_insurer"].isna() | (
                ~data_input_df["previous_insurer"].isin(
                    [
                        "Beazley",
                        "Non-Beazley",
                    ]
                )
            )
            data_input_df.loc[previous_insurer_mask, "previous_insurer"] = np.where(
                data_input_df.loc[previous_insurer_mask, "policy_reference"].isna(),
                "Non-Beazley",
                "Beazley",
            )

            shared_gross_premium_mask = (
                data_input_df["written_or_estimated_premium"].notna()
                & data_input_df["premium_selected"].isna()
            )
            data_input_df.loc[shared_gross_premium_mask, "premium"] = (
                data_input_df.loc[
                    shared_gross_premium_mask, "written_or_estimated_premium"
                ]
                .div(
                    1
                    - data_input_df.loc[
                        shared_gross_premium_mask, "acquisition_cost"
                    ].fillna(0)
                )
                .mul(currency_exchange_rate)
            )

            data_input_columns_to_write.append("premium")
            data_input_override_column_fields.append("premium")

        else:
            data_input_df["previous_insurer"].fillna("Non-Beazley", inplace=True)

        data_input_columns_to_write.append("previous_insurer")
        data_input_override_column_fields.append("previous_insurer")

        net_premium_shared_line_mask = data_input_df["premium"].notna() & (
            data_input_df["acquisition_cost"].notna()
        )

        data_input_df.loc[net_premium_shared_line_mask, "net_premium_shared_line"] = (
            data_input_df.loc[net_premium_shared_line_mask, "premium"].mul(
                1 - data_input_df.loc[net_premium_shared_line_mask, "acquisition_cost"]
            )
        )
        data_input_columns_to_write.append("net_premium_shared_line")

        att_incurred_shared_line_mask = (
            data_input_df["total_incurred_shared_line"].notna()
            | data_input_df["large_incurred_shared_line"].notna()
        )

        data_input_df.loc[
            att_incurred_shared_line_mask, "att_incurred_shared_line"
        ] = data_input_df.loc[
            att_incurred_shared_line_mask, "total_incurred_shared_line"
        ].fillna(
            0
        ) - data_input_df.loc[
            att_incurred_shared_line_mask, "large_incurred_shared_line"
        ].fillna(
            0
        )
        data_input_columns_to_write.append("att_incurred_shared_line")

        is_include_year_mask = data_input_df["is_include_year_selected"].isna()
        data_input_df.loc[is_include_year_mask, "is_include_year"] = data_input_df.loc[
            is_include_year_mask, "net_premium_shared_line"
        ].notna() & (
            data_input_df.loc[is_include_year_mask, "net_premium_shared_line"] != 0
        )
        data_input_columns_to_write.append("is_include_year")
        data_input_override_column_fields.append("is_include_year")

    return data_input_df, data_input_columns_to_write, data_input_override_column_fields


def process_ulr_projection_table(
    data_input_df,
    ulr_projection_df,
    claims_date,
    current_year_rate_change,
    inception_date,
):
    ulr_projection_columns_to_write = []

    current_year = inception_date.year if inception_date else None
    if (not current_year) or (not claims_date):
        return data_input_df, ulr_projection_columns_to_write

    # Rename columns to avoid conflicts
    data_input_df = data_input_df.rename(columns=lambda x: f"{x}_input")
    ulr_projection_df = ulr_projection_df.rename(columns=lambda x: f"{x}_proj")

    start_year = current_year
    years = [
        start_year - i
        for i in range(constants.ship_building_experience_rating_years, -1, -1)
    ]

    ulr_projection_df["yoa_proj"] = years
    ulr_projection_columns_to_write.append("yoa")

    merged_df = ulr_projection_df.merge(
        data_input_df, left_on="yoa_proj", right_on="yoa_input", how="left"
    )

    premium_mask = (
        (merged_df["signed_line_input"].notna())
        & (merged_df["signed_line_input"] != 0)
        & (merged_df["net_premium_shared_line_input"].notna())
        & (merged_df["net_premium_shared_line_input"] != 0)
    )

    merged_df.loc[premium_mask, "premium_proj"] = merged_df.loc[
        premium_mask, "net_premium_shared_line_input"
    ].div(merged_df.loc[premium_mask, "signed_line_input"])
    ulr_projection_columns_to_write.append("premium")

    attritional_incurred_mask = (merged_df["premium_proj"].notna()) & (
        merged_df["premium_proj"] != 0
    ) & merged_df["att_incurred_shared_line_input"].notna() & merged_df[
        "signed_line_input"
    ].notna() & merged_df[
        "signed_line_input"
    ] != 0

    merged_df.loc[attritional_incurred_mask, "att_incurred_shared_line_proj"] = (
        merged_df.loc[attritional_incurred_mask, "att_incurred_shared_line_input"].div(
            merged_df.loc[attritional_incurred_mask, "signed_line_input"]
        )
    )
    ulr_projection_columns_to_write.append("att_incurred_shared_line")

    large_incurred_mask = (merged_df["premium_proj"].notna()) & (
        merged_df["premium_proj"] != 0
    ) & merged_df["large_incurred_shared_line_input"].notna() & merged_df[
        "signed_line_input"
    ].notna() & merged_df[
        "signed_line_input"
    ] != 0

    merged_df.loc[large_incurred_mask, "large_incurred_shared_line_proj"] = (
        merged_df.loc[large_incurred_mask, "large_incurred_shared_line_input"].div(
            merged_df.loc[large_incurred_mask, "signed_line_input"]
        )
    )
    ulr_projection_columns_to_write.append("large_incurred_shared_line")

    merged_df["rate_change_proj"] = merged_df["rate_change_input"].fillna(0)
    merged_df.at[merged_df.index[-1], "rate_change_proj"] = (
        current_year_rate_change or 0
    )
    ulr_projection_columns_to_write.append("rate_change")

    table_claims_inflation = hx.params.table_claims_inflation
    claims_inflation_dict = dict(
        zip(table_claims_inflation["year"], table_claims_inflation["claims_inflation"])
    )
    merged_df["claims_inflation_yoy_proj"] = (
        merged_df["yoa_proj"].map(claims_inflation_dict).fillna(0)
    )
    ulr_projection_columns_to_write.append("claims_inflation_yoy")

    # Loop through each row in reverse order
    for i in range(len(merged_df) - 2, -1, -1):
        if i == len(merged_df) - 2:
            # Edge case: for the first item in the reversed loop, set the cumulative rate change to the current year's rate change
            merged_df.at[i, "rate_change_cumulative_proj"] = merged_df.at[
                i + 1, "rate_change_proj"
            ]

            merged_df.at[i, "claims_inflation_cumulative_proj"] = merged_df.at[
                i + 1, "claims_inflation_yoy_proj"
            ]

            merged_df.at[i, "claims_inflation_cumulative_proj"] = merged_df.at[
                i + 1, "claims_inflation_yoy_proj"
            ]

            merged_df.at[i, "development_month_proj"] = round(
                (
                    (
                        pd.to_datetime(claims_date)
                        - pd.to_datetime(
                            f"{claims_date.year - 1}-{inception_date.month}-{inception_date.day}"
                        )
                    ).days
                    / 365.25
                )
                * 12
            )
        else:
            # Normal case: multiply the value of the cumulative rate change at the previous index by the rate change of the previous index
            merged_df.at[i, "rate_change_cumulative_proj"] = (
                merged_df.at[i + 1, "rate_change_cumulative_proj"]
                * merged_df.at[i + 1, "rate_change_proj"]
            )

            merged_df.at[i, "claims_inflation_cumulative_proj"] = merged_df.at[
                i + 1, "claims_inflation_cumulative_proj"
            ] * (merged_df.at[i + 1, "claims_inflation_yoy_proj"])

            merged_df.at[i, "development_month_proj"] = (
                merged_df.at[i + 1, "development_month_proj"] + 12
            )
    ulr_projection_columns_to_write.append("rate_change_cumulative")
    ulr_projection_columns_to_write.append("claims_inflation_cumulative")
    ulr_projection_columns_to_write.append("development_month")

    on_levelled_premium_mask = (
        (merged_df["premium_proj"].notna())
        & (merged_df["premium_proj"] != 0)
        & merged_df["rate_change_cumulative_proj"].notna()
    )
    merged_df.loc[on_levelled_premium_mask, "on_levelled_premium_proj"] = merged_df.loc[
        on_levelled_premium_mask, "premium_proj"
    ].mul(merged_df.loc[on_levelled_premium_mask, "rate_change_cumulative_proj"])
    ulr_projection_columns_to_write.append("on_levelled_premium")

    on_levelled_att_incurred_mask = (
        (merged_df["premium_proj"].notna())
        & (merged_df["premium_proj"] != 0)
        & merged_df["att_incurred_shared_line_proj"].notna()
        & merged_df["claims_inflation_cumulative_proj"].notna()
    )
    merged_df.loc[
        on_levelled_att_incurred_mask, "on_levelled_att_incurred_shared_line_proj"
    ] = merged_df.loc[
        on_levelled_att_incurred_mask, "att_incurred_shared_line_proj"
    ].mul(
        merged_df.loc[on_levelled_att_incurred_mask, "claims_inflation_cumulative_proj"]
    )
    ulr_projection_columns_to_write.append("on_levelled_att_incurred_shared_line")

    on_levelled_att_incurred_mask = (merged_df["premium_proj"].notna()) & (
        merged_df["premium_proj"] != 0
    ) & merged_df["on_levelled_att_incurred_shared_line_proj"].notna() & merged_df[
        "on_levelled_premium_proj"
    ].notna() & merged_df[
        "on_levelled_premium_proj"
    ] != 0

    merged_df.loc[on_levelled_att_incurred_mask, "on_levelled_att_incurred_lr_proj"] = (
        merged_df.loc[
            on_levelled_att_incurred_mask, "on_levelled_att_incurred_shared_line_proj"
        ].div(merged_df.loc[on_levelled_att_incurred_mask, "on_levelled_premium_proj"])
    )
    ulr_projection_columns_to_write.append("on_levelled_att_incurred_lr")

    on_levelled_large_incurred_mask = (
        (merged_df["premium_proj"].notna())
        & (merged_df["premium_proj"] != 0)
        & merged_df["large_incurred_shared_line_proj"].notna()
        & merged_df["claims_inflation_cumulative_proj"].notna()
    )
    merged_df.loc[
        on_levelled_large_incurred_mask, "on_levelled_large_incurred_shared_line_proj"
    ] = merged_df.loc[
        on_levelled_large_incurred_mask, "large_incurred_shared_line_proj"
    ].mul(
        merged_df.loc[
            on_levelled_large_incurred_mask, "claims_inflation_cumulative_proj"
        ]
    )
    ulr_projection_columns_to_write.append("on_levelled_large_incurred_shared_line")

    on_levelled_large_incurred_lr_mask = (merged_df["premium_proj"].notna()) & (
        merged_df["premium_proj"] != 0
    ) & merged_df["on_levelled_large_incurred_shared_line_proj"].notna() & merged_df[
        "on_levelled_premium_proj"
    ].notna() & merged_df[
        "on_levelled_premium_proj"
    ] != 0
    merged_df.loc[
        on_levelled_large_incurred_lr_mask, "on_levelled_large_incurred_lr_proj"
    ] = merged_df.loc[
        on_levelled_large_incurred_lr_mask,
        "on_levelled_large_incurred_shared_line_proj",
    ].div(
        merged_df.loc[on_levelled_large_incurred_lr_mask, "on_levelled_premium_proj"]
    )
    ulr_projection_columns_to_write.append("on_levelled_large_incurred_lr")

    table_hull_development_pattern = hx.params.table_hull_development_pattern
    hull_development_pattern_dict = dict(
        zip(
            table_hull_development_pattern["months"],
            table_hull_development_pattern["dev"],
        )
    )

    development_percent_mask = (
        merged_df["development_month_proj"]
        >= 0 & merged_df["development_month_proj"].notna()
    )
    merged_df.loc[development_percent_mask, "development_percent_proj"] = (
        merged_df.loc[development_percent_mask, "development_month_proj"]
        .map(hull_development_pattern_dict)
        .fillna(1)
    )
    ulr_projection_columns_to_write.append("development_percent")

    table_ulr_projection = hx.params.table_ulr_projection
    parameters_dict = table_ulr_projection.set_index("parameter")["value"].to_dict()
    cl_dev_threshold = parameters_dict["cl_dev_threshold"]
    attritional_ielr_portfolio = parameters_dict["attritional_ielr_portfolio"]

    attritional_ulr_mask = (
        (merged_df["on_levelled_att_incurred_shared_line_proj"] != 0)
        & merged_df["on_levelled_att_incurred_shared_line_proj"].notna()
        & merged_df["development_percent_proj"].notna()
    )
    merged_df.loc[attritional_ulr_mask, "attritional_ulr_proj"] = np.where(
        merged_df.loc[attritional_ulr_mask, "development_percent_proj"]
        > cl_dev_threshold,
        merged_df.loc[attritional_ulr_mask, "on_levelled_att_incurred_lr_proj"]
        .fillna(0)
        .div(merged_df.loc[attritional_ulr_mask, "development_percent_proj"]),
        merged_df.loc[attritional_ulr_mask, "on_levelled_att_incurred_lr_proj"]
        .fillna(0)
        .add(
            attritional_ielr_portfolio
            * (1 - merged_df.loc[attritional_ulr_mask, "development_percent_proj"])
        ),
    )
    ulr_projection_columns_to_write.append("attritional_ulr")

    merged_df["is_include_year_proj"] = (
        merged_df["is_include_year_input"].fillna(False).astype(int)
    )
    merged_df.iloc[-2, merged_df.columns.get_loc("is_include_year_proj")] = 0

    ulr_projection_columns_to_write.append("is_include_year")

    merged_df.columns = [col.replace("_proj", "") for col in merged_df.columns]
    return (
        merged_df,
        ulr_projection_columns_to_write,
    )
