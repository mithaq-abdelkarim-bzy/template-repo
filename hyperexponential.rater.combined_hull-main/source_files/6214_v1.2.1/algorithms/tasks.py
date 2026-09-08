import openpyxl.utils
import hx
import os
import json
import copy
import numpy as np
import pandas as pd
from datetime import date
import openpyxl
import pyodbc
# from copy import copy, deepcopy
from openpyxl.utils import get_column_letter

from algorithms.rate_utilities import is_hx_class, pd_df_from_hx_list
from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.db.sql_queries import get_vessels_by_imo
from algorithms.db.portfolio_analysis_sql_queries import (
    portfolio_analysis_query_builder,
)
from algorithms import parameter_tables_schema as params
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
import algorithms.rate_constants as constants
from algorithms.db.bi_db_sql_queries import (
    get_policies_by_policy_references,
    get_policies_by_class_of_business,
)


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id


def calculate_avg_yoa_rate_change():
    all_policies_columns = [
        "yoa",
        "current_premium",
        "expiring_premium",
    ]
    all_policies = get_policies_by_class_of_business()
    all_policies_df = pd.DataFrame.from_records(
        all_policies, columns=all_policies_columns
    )
    all_policies_df["current_premium"].fillna(0, inplace=True)
    all_policies_df["expiring_premium"].fillna(0, inplace=True)

    # Group by 'yoa' and calculate the sum of current_premium and expiring_premium
    all_policies_grouped_by_yoa = all_policies_df.groupby("yoa")[
        ["current_premium", "expiring_premium"]
    ].sum()

    # Calculate the ratio for each YOA
    all_policies_grouped_by_yoa["rate_change"] = (
        all_policies_grouped_by_yoa["current_premium"]
        / all_policies_grouped_by_yoa["expiring_premium"]
    )

    all_policies_grouped_by_yoa["rate_change"].replace(
        {np.nan: 1, np.inf: 1}, inplace=True
    )

    return all_policies_grouped_by_yoa


@hx.task
# Place Holder logic of assignment until an access to the database is provided
def populate_bi_data(hxd, progress):

    if not hxd.cds.experience_rating.ship_building.claims_date:
        hxd.cds.experience_rating.ship_building.claims_date = date.today()
    ship_building_policy_reference = hxd.cds.layers[
        0
    ].coverages.ship_building.section_reference
    current_year = (
        hxd.cds.standard_fields.inception_date.year
        if hxd.cds.standard_fields.inception_date
        else None
    )
    if not current_year:
        return

    all_policies_grouped_by_yoa = calculate_avg_yoa_rate_change()

    start_year = current_year - 1
    policy_reference_substring_length = 6
    rate_year_substring_length = 2
    yoas = [(start_year - i) for i in range(10 - 1, -1, -1)]

    if (
        ship_building_policy_reference
        and ship_building_policy_reference != ""
        and len(ship_building_policy_reference) >= policy_reference_substring_length
    ):

        policy_reference_prefix = ship_building_policy_reference[
            :policy_reference_substring_length
        ]
        policy_reference_yoas = [
            (
                policy_reference_prefix
                + str((start_year - i))[rate_year_substring_length:]
            )
            for i in range(10 - 1, -1, -1)
        ]
        policies = get_policies_by_policy_references(
            policy_references=policy_reference_yoas
        )

        policies_df = pd.DataFrame()
        policies_df["yoa"] = yoas

        if len(policies) == 0:
            policies_df["rate_change"] = np.nan
            # Map the calculated rate_change to the corresponding rows in policies_df
            policies_df["rate_change"] = policies_df["yoa"].map(
                all_policies_grouped_by_yoa["rate_change"]
            )
            policies_df["rate_change"].fillna(1, inplace=True)
            hxd.cds.experience_rating.ship_building.extracted_policies = (
                policies_df.to_dict(orient="records")
            )
            return

        columns = [
            "policy_reference",
            "written_or_estimated_premium",
            "total_incurred_shared_line",
            "rate_change",
            "external_acquisition_cost",
            "internal_acquisition_cost",
            "signed_line",
            "yoa",
        ]

        imported_policies_df = pd.DataFrame.from_records(policies, columns=columns)
        policies_df = (
            policies_df.set_index("yoa")
            .combine_first(imported_policies_df.set_index("yoa"))
            .reset_index()
        )
        policies_df["external_acquisition_cost"].fillna(0, inplace=True)
        policies_df["acquisition_cost"] = policies_df[["external_acquisition_cost"]]
        policies_df["is_include_year"] = True

        policies_df.drop(
            columns=[
                "external_acquisition_cost",
                "internal_acquisition_cost",
            ],
            inplace=True,
        )

        if (all_policies_grouped_by_yoa is not None) and (
            not all_policies_grouped_by_yoa.empty
        ):
            rate_change_mask = policies_df["rate_change"].isna()
            # Map the calculated rate_change to the corresponding rows in policies_df
            policies_df.loc[rate_change_mask, "rate_change"] = policies_df.loc[
                rate_change_mask, "yoa"
            ].map(all_policies_grouped_by_yoa["rate_change"])

        # Fill NaN values in the rate_change column with 1
        policies_df["rate_change"].fillna(1, inplace=True)

        policies_df.replace({np.nan: None}, inplace=True)
        hxd.cds.experience_rating.ship_building.extracted_policies = (
            policies_df.to_dict(orient="records")
        )


def lookup_imos(vessels):
    imos_set = set()
    for vessel in vessels:
        imo = vessel.vessel_details.imo
        if imo is not None:
            imos_set.add(imo)

    imos = list(imos_set)
    if len(imos) == 0:
        return

    db_vessels = get_vessels_by_imo(imos)
    # Retrieve columns from db_vessels
    columns = db_vessels.columns

    # Filter out the 'imo' column
    vessels_table_schema = [column for column in columns if column != "imo"]
    non_behavioural_columns = [
        "dwt",
        "gross_tonnage",
        "name",
        "vessel_type",
        "flag",
        "year_built",
    ]

    for vessel in vessels:
        imo = str(vessel.vessel_details.imo or "")
        if imo not in db_vessels["imo"].values:
            continue
        for key in vessels_table_schema:
            db_vessesl = db_vessels[db_vessels["imo"] == imo]
            try:
                if (getattr(vessel.vessel_details, key) is None) or (
                    key not in non_behavioural_columns
                ):
                    setattr(vessel.vessel_details, key, db_vessesl[key].values[0])
            except Exception as e:
                try:
                    if (getattr(vessel, key) is None) or (
                        key not in non_behavioural_columns
                    ):
                        setattr(vessel, key, db_vessesl[key].values[0])
                except Exception as e:
                    continue


@hx.task
def lookup_imos_task(hxd, progress):
    vessels = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list
    lookup_imos(vessels)


def flatten_dict(d):
    def recursive_flatten(d):
        items = []
        for key, value in d.items():
            if is_hx_class(value):
                children = dict(value)
                items.extend(recursive_flatten(children).items())
            else:
                items.append((key, value))
        return dict(items)

    return recursive_flatten(d)


@hx.task
def generate_portfolio_analysis_excel(hxd, progress):
    portfolio_analysis_vessels_list = (
        hxd.cds.portfolio_analysis.hull_rating.portfolio_metrics.vessels
    )
    if len(portfolio_analysis_vessels_list) == 0:
        return
    vessels_df = pd_df_from_hx_list(portfolio_analysis_vessels_list)

    # Write the dictionary values to the Excel template
    template_path = (
        f"./model/algorithms/templates/combined_hull_portfolio_analysis_template.xlsx"
    )

    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook.active

    # Start filling data from row 10
    start_row = 10

    # Get the maximum length of the data lists to determine the number of rows to add
    max_length = len(vessels_df)

    # Add rows to the sheet as needed
    for _ in range(max_length):
        sheet.append([])

    portfolio_metrics = hxd.cds.portfolio_analysis.hull_rating.portfolio_metrics
    sheet.cell(row=6, column=4, value=portfolio_metrics.vessels_count)
    sheet.cell(row=6, column=8, value=portfolio_metrics.average_agreed_value)
    sheet.cell(row=6, column=13, value=portfolio_metrics.average_achieved_rate)

    vessels_df = vessels_df.replace({np.nan: None})

    for idx, vessel in enumerate(vessels_df.itertuples(index=False), start=0):
        sheet.cell(row=start_row + idx, column=2, value=vessel.id)
        sheet.cell(row=start_row + idx, column=3, value=vessel.imo)
        sheet.cell(row=start_row + idx, column=4, value=vessel.insured)
        sheet.cell(row=start_row + idx, column=5, value=vessel.policy_reference)
        sheet.cell(row=start_row + idx, column=6, value=vessel.effective_date)
        sheet.cell(row=start_row + idx, column=7, value=vessel.expiry_date)
        sheet.cell(row=start_row + idx, column=8, value=vessel.coverage)
        sheet.cell(
            row=start_row + idx,
            column=9,
            value=(
                int(round(vessel.original_agreed_value, 0))
                if vessel.original_agreed_value
                else None
            ),
        )
        sheet.cell(row=start_row + idx, column=10, value=vessel.original_currency)
        sheet.cell(
            row=start_row + idx,
            column=11,
            value=(
                int(round(vessel.agreed_value_converted, 0))
                if vessel.agreed_value_converted
                else None
            ),
        )
        sheet.cell(row=start_row + idx, column=12, value=vessel.vessel_type)
        sheet.cell(
            row=start_row + idx,
            column=13,
            value=int(round(vessel.gross_tonnage, 0)) if vessel.gross_tonnage else None,
        )
        sheet.cell(row=start_row + idx, column=14, value=vessel.dwt)
        sheet.cell(row=start_row + idx, column=15, value=vessel.year_built)
        sheet.cell(row=start_row + idx, column=16, value=vessel.flag)
        sheet.cell(row=start_row + idx, column=17, value=vessel.classification)
        sheet.cell(
            row=start_row + idx,
            column=18,
            value=vessel.achieved_rate * 100 if vessel.achieved_rate else None,
        )
        sheet.cell(
            row=start_row + idx,
            column=19,
            value=vessel.order_percent * 100 if vessel.order_percent else None,
        )
        sheet.cell(
            row=start_row + idx,
            column=20,
            value=(
                vessel.written_line_percent * 100
                if vessel.written_line_percent
                else None
            ),
        )
        sheet.cell(row=start_row + idx, column=21, value=vessel.operator_domicile)
        sheet.cell(row=start_row + idx, column=22, value=vessel.broker)
        sheet.cell(row=start_row + idx, column=23, value=vessel.follow_lead)
        sheet.cell(row=start_row + idx, column=24, value=vessel.vessel_name)
        sheet.cell(row=start_row + idx, column=25, value=vessel.type_abrv)

    # Protect the sheet to prevent changes
    sheet.protection.enable()
    sheet.protection.set_password(constants.excel_password)

    # Save the filled template to a new file
    with hxd.cds.portfolio_analysis.hull_rating.exported_data.open("b") as f:
        workbook.save(f)
        hxd.non_cds.show_hide_toggles.hull.show_generated_portfolio_analysis_excel = (
            True
        )


def generate_rate_change_sheet(hxd, sheet, coverage):

    buckets = [
        "exposure_change",
        "risk_characteristics_change",
        "limit_change",
        "deductible_change",
        "terms_conditions_change",
        "other_change",
        "brokerage_change",
        "rate_change",
    ]

    buckets_children = ["model_calculated", "uw_selected", "comments"]

    premiums_children = [
        "premium_policy_term_100pct",
        "premium_policy_term_beazley_share",
        "written_line",
        "benchmark_premium",
        "bpi",
    ]

    start_row = 6
    start_column = 3
    current_index = 0
    current_coverage = getattr(hxd.cds.layers[0].rate_change, coverage)

    for premium in premiums_children:
        for i, status in enumerate(["renewal", "expiring"]):
            current_value = getattr(getattr(current_coverage, premium), status)
            if current_value is None:
                continue
            sheet.cell(
                row=start_row + current_index,
                column=start_column + i,
                value=current_value,
            )
        current_index += 1

    # Adjust for cosmetic gaps in the template
    current_index += 3

    for bucket in buckets:
        current_bucket = getattr(current_coverage, bucket)
        for i, field in enumerate(buckets_children):
            current_value = (
                getattr(current_bucket, field).selected
                if field == "uw_selected" and bucket != "rate_change"
                else getattr(current_bucket, field)
            )
            if current_value is None:
                continue
            sheet.cell(
                row=start_row + current_index,
                column=start_column + i,
                value=current_value,
            )
        if bucket in ["rate_change", "brokerage_change"]:
            # Adjust for cosmetic gaps in the template
            current_index += 2
        else:
            # Adjust for cosmetic gaps in the template
            current_index += 1

    risk_adjusted_rate_change_uw_selected = (
        current_coverage.risk_adjusted_rate_change_uw_selected.uw_selected
    )
    if risk_adjusted_rate_change_uw_selected:
        sheet.cell(
            row=start_row + current_index,
            column=start_column,
            value=risk_adjusted_rate_change_uw_selected,
        )

    # Populate_rate_change_premiums
    # Protect the sheet
    sheet.protection.set_password(constants.excel_password)
    sheet.protection.enable()


def generate_vessels_sheet(hxd, sheet):
    # Extract frequently used attributes
    hull_rating = hxd.cds.exposure.granular.vessels.hull_rating
    vessels_list = hull_rating.vessels_list
    if not vessels_list:
        return sheet

    layer = hxd.cds.layers[0]
    currency = hxd.cds.currencies.source_currency

    # Extract layer-level attributes
    policy_reference = layer.coverages.hull.section_reference or ""
    brokerage = layer.coverages.hull.brokerage or ""
    written_line = layer.coverages.hull.written_line or ""
    lead_follow = layer.coverages.hull.hull_lead_follow or ""
    operator_domicile = hull_rating.operator_domicile or ""
    fleet_casualty_history = hull_rating.fleet_soft_factors.fleet_casualty_history or ""
    owner_manager_quality = hull_rating.fleet_soft_factors.owner_quality or ""

    # Helper function for conditional values
    def safe_value(value):
        return value if value else ""

    # Write static data to the sheet
    policy_reference_cell = sheet.cell(row=4, column=3, value=policy_reference)
    set_excel_cell_style(policy_reference_cell, None)
    lead_follow_cell = sheet.cell(row=4, column=6, value=lead_follow)
    set_excel_cell_style(lead_follow_cell, None)
    brokerage_cell = sheet.cell(row=7, column=3, value=brokerage)
    set_excel_cell_style(brokerage_cell, None)
    written_line_cell = sheet.cell(row=7, column=6, value=written_line)
    set_excel_cell_style(written_line_cell, None)
    operator_domicile_cell = sheet.cell(row=7, column=10, value=operator_domicile)
    set_excel_cell_style(operator_domicile_cell, None)
    fleet_casualty_history_cell = sheet.cell(
        row=11, column=3, value=fleet_casualty_history
    )
    set_excel_cell_style(fleet_casualty_history_cell, None)
    owner_manager_quality_cell = sheet.cell(
        row=11, column=6, value=owner_manager_quality
    )
    set_excel_cell_style(owner_manager_quality_cell, None)

    # Write vessel data
    start_row = 15
    # Add currency to specific cells
    currency_columns = [8, 20, 22]
    for col in currency_columns:
        cell = sheet.cell(
            row=start_row - 1,
            column=col,
            value=f"{sheet.cell(row=start_row - 1, column=col).value} ({currency})",
        )
        set_excel_cell_style(cell, None)

    for idx, vessel in enumerate(vessels_list):
        row = start_row + idx
        vessel_details = vessel.vessel_details

        # Batch update row data
        row_data = [
            vessel_details.imo,
            vessel_details.name,
            vessel.inception_date,
            vessel.expiry_date,
            vessel.coverage,
            vessel.vessel_type,
            safe_value(vessel.agreed_value),
            safe_value(vessel_details.gross_tonnage),
            safe_value(vessel.dwt),
            safe_value(vessel.year_built),
            vessel.flag,
            vessel_details.vessel_class,
            safe_value(vessel.deductible),
            safe_value(vessel_details.order_percent),
            vessel_details.freight_conditions,
            vessel_details.vessel_quality,
            vessel_details.area_of_operation,
            safe_value(vessel.behavioural_model_rate),
            safe_value(vessel.behavioural_benchmark_premium),
            safe_value(vessel.static_model_rate),
            safe_value(vessel.static_benchmark_premium),
            safe_value(vessel.achieved_rate),
            safe_value(vessel.achieved_premium),
            vessel.average_achieved_rate,
            safe_value(vessel.uw_adjustment),
            vessel.percent_of_similar_vessel_that_achieved_lower_rate,
        ]

        for col, value in enumerate(row_data, start=2):
            cell = sheet.cell(row=row, column=col, value=value)
            set_excel_cell_style(cell, None)

    # Protect the sheet
    sheet.protection.set_password(constants.excel_password)
    sheet.protection.enable()
    return sheet


@hx.task
def generate_vessels_xlsx_task(hxd, progress):
    # Extract frequently used attributes
    hull_rating = hxd.cds.exposure.granular.vessels.hull_rating
    vessels_list = hull_rating.vessels_list
    if not vessels_list:
        return

    layer = hxd.cds.layers[0]
    currency = hxd.cds.currencies.source_currency

    # Extract layer-level attributes
    policy_reference = layer.coverages.hull.section_reference or ""
    brokerage = layer.coverages.hull.brokerage or ""
    written_line = layer.coverages.hull.written_line or ""
    lead_follow = layer.coverages.hull.hull_lead_follow or ""
    operator_domicile = hull_rating.operator_domicile or ""
    fleet_casualty_history = hull_rating.fleet_soft_factors.fleet_casualty_history or ""
    owner_manager_quality = hull_rating.fleet_soft_factors.owner_quality or ""

    # Load the workbook and select the active worksheet
    template_path = "./model/algorithms/templates/vessels_template.xlsx"
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook.active

    # Helper function for conditional values
    def safe_value(value):
        return value if value else ""

    # Write static data to the sheet
    policy_reference_cell = sheet.cell(row=4, column=3, value=policy_reference)
    set_excel_cell_style(policy_reference_cell, None)
    lead_follow_cell = sheet.cell(row=4, column=6, value=lead_follow)
    set_excel_cell_style(lead_follow_cell, None)
    brokerage_cell = sheet.cell(row=7, column=3, value=brokerage)
    set_excel_cell_style(brokerage_cell, None)
    written_line_cell = sheet.cell(row=7, column=6, value=written_line)
    set_excel_cell_style(written_line_cell, None)
    operator_domicile_cell = sheet.cell(row=7, column=10, value=operator_domicile)
    set_excel_cell_style(operator_domicile_cell, None)
    fleet_casualty_history_cell = sheet.cell(
        row=11, column=3, value=fleet_casualty_history
    )
    set_excel_cell_style(fleet_casualty_history_cell, None)
    owner_manager_quality_cell = sheet.cell(
        row=11, column=6, value=owner_manager_quality
    )
    set_excel_cell_style(owner_manager_quality_cell, None)

    # Write vessel data
    start_row = 15
    # Add currency to specific cells
    currency_columns = [8, 20, 22]
    for col in currency_columns:
        # col_letter = get_column_letter(col)
        # sheet.column_dimensions[col_letter].width = 25   # adjust width as needed
        cell = sheet.cell(
            row=start_row - 1,
            column=col,
            value=f"{sheet.cell(row=start_row - 1, column=col).value} ({currency})",
        )
        set_excel_cell_style(cell, None)

    vessels_formatting = []
    for idx, vessel in enumerate(vessels_list):
        row = start_row + idx
        vessel_details = vessel.vessel_details

        # Batch update row data
        row_data = [
            vessel_details.imo,
            vessel_details.name,
            vessel.inception_date,
            vessel.expiry_date,
            vessel.coverage,
            vessel.vessel_type,
            safe_value(vessel.agreed_value),
            safe_value(vessel_details.gross_tonnage),
            safe_value(vessel.dwt),
            safe_value(vessel.year_built),
            vessel.flag,
            vessel_details.vessel_class,
            safe_value(vessel.deductible),
            safe_value(vessel_details.order_percent),
            vessel_details.freight_conditions,
            vessel_details.vessel_quality,
            vessel_details.area_of_operation,
            safe_value(vessel.behavioural_model_rate),
            safe_value(vessel.behavioural_benchmark_premium),
            safe_value(vessel.static_model_rate),
            safe_value(vessel.static_benchmark_premium),
            safe_value(vessel.achieved_rate),
            safe_value(vessel.achieved_premium),
            vessel.average_achieved_rate,
            safe_value(vessel.uw_adjustment),
            vessel.percent_of_similar_vessel_that_achieved_lower_rate,
        ]

        for col, value in enumerate(row_data, start=2):
            cell = sheet.cell(row=row, column=col, value=value)
            if idx == 0:
                vessels_formatting.append({
                    "number_format": cell.number_format,
                    "font": copy.copy(cell.font),
                    "border": copy.copy(cell.border),
                    "fill": copy.copy(cell.fill),
                    "alignment": copy.copy(cell.alignment)
                })
            else:
                fmt = vessels_formatting[col-2]
                cell.number_format = fmt["number_format"]
                cell.font = fmt["font"]
                cell.border = fmt["border"]
                cell.fill = fmt["fill"]
                cell.alignment = fmt["alignment"]

    # Protect the sheet
    sheet.protection.set_password(constants.excel_password)
    sheet.protection.enable()

    # Save the workbook
    with hull_rating.vessels_xlsx.open("b") as f:
        workbook.save(f)
        hxd.non_cds.show_hide_toggles.hull.show_generated_vessels_xlsx = True


@hx.task
def generate_rating_summary_xlsx_task(hxd, progress):

    vessels_list = []
    template_path = ""

    is_hull_coverage = hxd.non_cds.show_hide_toggles.hull.show_hull_coverage
    is_loh_coverage = hxd.non_cds.show_hide_toggles.loh.show_loh_coverage
    is_ship_building_coverage = (
        hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage
    )

    if is_hull_coverage:
        vessels_list = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list
        template_path = "./model/algorithms/templates/rating_summary_hull_template.xlsx"
    elif is_loh_coverage:
        vessels_list = hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
        template_path = "./model/algorithms/templates/rating_summary_loh_template.xlsx"
    elif is_ship_building_coverage:
        vessels_list = (
            hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list
        )
        template_path = (
            "./model/algorithms/templates/rating_summary_shipbuilders_template.xlsx"
        )

    if len(vessels_list) == 0:
        return

    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook[workbook.sheetnames[0]]
    workbook.active = workbook.sheetnames.index(sheet.title)
    uw_comment = hxd.cds.uw_comment
    risk_info = hxd.cds.standard_fields
    insured_name = risk_info.insured_name
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    underwriter = risk_info.underwriter
    currency = hxd.cds.currencies.source_currency
    broker = risk_info.broker
    broker_contact = hxd.cds.broker_contact
    is_renewal = hxd.cds.standard_fields.is_renewal

    coverages = (
        ["hull", "iv", "war"]
        if hxd.non_cds.show_hide_toggles.hull.show_hull_coverage
        else (
            ["loh"]
            if hxd.non_cds.show_hide_toggles.loh.show_loh_coverage
            else ["ship_building"]
        )
    )
    fields = [
        "status",
        "section_reference",
        "rating_summary_brokerage",
        "other_deductions",
        "rating_summary_written_line",
        "quoted_premium_pro_rated_100pct",
        "technical_premium_pro_rated_100pct",
        "technical_premium_pre_uw_adj_pro_rated_100pct",
        "benchmark_premium_pro_rated_100pct",
        "tpi",
        "tpi_pre_uw_adj",
        "bpi",
        "pflr",
        "roc",
        "uw_adj_impact",
    ]
    rating_summary_starting_column = 3
    rating_summary_starting_row = 16

    # Output the risk information
    set_excel_cell_style(sheet.cell(row=4, column=3, value=insured_name), None)
    set_excel_cell_style(sheet.cell(row=4, column=6, value=underwriter), None)
    set_excel_cell_style(sheet.cell(row=5, column=6, value=currency), None)
    set_excel_cell_style(sheet.cell(row=6, column=3, value=inception_date), None)
    set_excel_cell_style(sheet.cell(row=6, column=6, value=broker_contact), None)
    set_excel_cell_style(sheet.cell(row=7, column=6, value=broker), None)
    set_excel_cell_style(sheet.cell(row=7, column=3, value=expiry_date), None)
    set_excel_cell_style(
        sheet.cell(row=8, column=3, value=("Yes" if is_renewal else "No")), None
    )
    set_excel_cell_style(sheet.cell(row=10, column=2, value=uw_comment), None)

    is_iv = hxd.non_cds.show_hide_toggles.iv.show_iv_coverage
    is_war = hxd.non_cds.show_hide_toggles.war.show_war_coverage

    # Populate rating summary
    for i, coverage in enumerate(coverages):
        if len(coverages) == 1:
            cell = sheet.cell(
                row=rating_summary_starting_row - 1,
                column=rating_summary_starting_column,
            )
            set_excel_cell_style(cell, None)
        secondary_index = 0
        for field in fields:
            # Don't populate Rating Summary Table if coverage is iv and is_war is false
            if (coverage == "iv" and (not is_iv)) or (
                coverage == "war" and (not is_war)
            ):
                continue
            if coverage != "ship_building" and field == "other_deductions":
                continue
            value = getattr(getattr(hxd.cds.layers[0].coverages, coverage), field)
            cell = sheet.cell(
                row=rating_summary_starting_row + secondary_index,
                column=rating_summary_starting_column + i,
                value=value,
            )
            secondary_index += 1

            set_excel_cell_style(cell, None)

    if hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        # Define a mapping of vessel attributes to columns
        start_row = 34
        vessel_columns = [
            ("vessel_details.imo",),
            ("vessel_details.name",),
            ("coverage",),
            ("agreed_value",),
            ("deductible",),
            ("achieved_rate",),
            ("achieved_premium",),
            ("iv.iv_output_summary_coverage", "is_iv", "iv.iv_is_include_vessel"),
            (
                "iv.iv_output_summary_agreed_value",
                "is_iv",
                "iv.iv_is_include_vessel",
            ),
            (
                "iv.iv_output_summary_deductible",
                "is_iv",
                "iv.iv_is_include_vessel",
            ),
            (
                "iv.iv_achieved_rate",
                "is_iv",
                "iv.iv_is_include_vessel",
            ),
            (
                "iv.iv_achieved_premium",
                "is_iv",
                "iv.iv_is_include_vessel",
            ),
            (
                "war.war_output_summary_coverage",
                "is_war",
                "war.war_is_include_vessel",
            ),
            (
                "war.war_output_summary_agreed_value",
                "is_war",
                "war.war_is_include_vessel",
            ),
            (
                "war.war_achieved_rate",
                "is_war",
                "war.war_is_include_vessel",
            ),
            (
                "war.war_achieved_premium",
                "is_war",
                "war.war_is_include_vessel",
            ),
        ]

        # Populate vessel data
        vessels_formatting = []
        for i, vessel in enumerate(vessels_list):
            first_column_cell = sheet.cell(row=start_row + i, column=1)
            set_excel_cell_style(
                first_column_cell,
                "ShtBack",
            )
            last_column_cell = sheet.cell(
                row=start_row + i,
                column=len(vessel_columns) + 2,
            )
            set_excel_cell_style(
                last_column_cell,
                "ShtBack",
            )
            for col, (attr, *conditions) in enumerate(vessel_columns):
                # Check conditions if any
                if conditions:
                    # Handle global conditions like is_iv and is_war
                    condition_values = []
                    for cond in conditions:
                        if cond == "is_iv":
                            condition_values.append(is_iv)
                        elif cond == "is_war":
                            condition_values.append(is_war)
                        else:
                            condition_values.append(getattr(vessel, cond.split(".")[0]))

                    if not all(condition_values):
                        vessels_formatting.append("ShtBack")
                        continue

                # Get the value of the attribute
                value = getattr(vessel, attr.split(".")[0])
                for sub_attr in attr.split(".")[1:]:
                    value = getattr(value, sub_attr, "")

                # Set the cell value
                cell = sheet.cell(
                    row=start_row + i,
                    column=col + 2,
                    value=value if value else "",
                )
                if i == 0:
                    vessels_formatting.append(cell.style)
                else:
                    set_excel_cell_style(
                        cell,
                        vessels_formatting[col],
                    )

    elif hxd.non_cds.show_hide_toggles.loh.show_loh_coverage:
        start_row = 33
        # Define a mapping of vessel attributes to columns
        vessel_columns = [
            ("loh_number_of_vessels"),
            ("loh_vessel_details.loh_name"),
            ("loh_vessel_details.loh_imo"),
            ("loh_vessel_details.loh_vessel_type"),
            ("loh_vessel_details.loh_year_built"),
            ("loh_vessel_details.loh_gross_tonnage"),
            ("loh_vessel_details.loh_dwt"),
            ("loh_daily_rate"),
            ("loh_xs_days"),
            ("loh_cover"),
            ("loh_vessel_achieved_rate"),
        ]

        # Populate vessel data
        vessels_formatting = []
        for i, vessel in enumerate(vessels_list):
            first_column_cell = sheet.cell(row=start_row + i, column=1)
            set_excel_cell_style(
                first_column_cell,
                "ShtBack",
            )
            last_column_cell = sheet.cell(
                row=start_row + i,
                column=len(vessel_columns) + 2,
            )
            set_excel_cell_style(
                last_column_cell,
                "ShtBack",
            )
            for col, attr in enumerate(vessel_columns):
                # Get the value of the attribute
                value = getattr(vessel, attr.split(".")[0])
                for sub_attr in attr.split(".")[1:]:
                    value = getattr(value, sub_attr, "")

                # Set the cell value
                cell = sheet.cell(
                    row=start_row + i,
                    column=col + 2,
                    value=value if value else "",
                )
                if i == 0:
                    vessels_formatting.append(cell.style)
                else:
                    cell = set_excel_cell_style(
                        cell,
                        vessels_formatting[col],
                    )

    elif hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage:
        start_row = 34
        sheet.cell(
            row=start_row - 2,
            column=3,
            value=hxd.cds.layers[
                0
            ].coverages.ship_building.ship_building_policy_details,
        )

        is_war_cover = hxd.cds.layers[
            0
        ].coverages.ship_building.ship_building_is_war_cover

        sheet.cell(
            row=start_row - 2, column=7, value=("Yes" if is_war_cover else "No")
        ), None
        # Define a mapping of vessel attributes to columns
        show_production_stages_time = hxd.cds.layers[
            0
        ].coverages.ship_building.ship_building_show_production_stages_time

        vessel_columns = [
            ("ship_building_vessel_type"),
            ("ship_building_number_of_vessels"),
            ("ship_building_vessel_name"),
            ("ship_building_attachment_date"),
            ("ship_building_delivery_date"),
            ("ship_building_total_months_all_stages"),
            ("ship_building_total_months_steel_cutting_keel_laying"),
            ("ship_building_total_months_keel_laying_launch"),
            ("ship_building_total_months_launch_delivery"),
            ("ship_building_country"),
            ("ship_building_survey_grade"),
            ("ship_building_deductible"),
            ("ship_building_sum_insured"),
            ("ship_building_benchmark_rate"),
        ]

        # Populate vessel data
        vessels_formatting = []
        if show_production_stages_time:
            first_cell = sheet.cell(
                row=start_row,
                column=8,
            )
            set_excel_cell_style(
                first_cell,
                "InNum3dp",
            )
            second_cell = sheet.cell(
                row=start_row,
                column=9,
            )
            set_excel_cell_style(
                second_cell,
                "InNum3dp",
            )
            third_cell = sheet.cell(
                row=start_row,
                column=10,
            )
            set_excel_cell_style(
                third_cell,
                "InNum3dp",
            )
        else:
            first_cell = sheet.cell(
                row=start_row,
                column=7,
            )
            set_excel_cell_style(
                first_cell,
                "InNum3dp",
            )

        production_stages = [
            "ship_building_total_months_steel_cutting_keel_laying",
            "ship_building_total_months_keel_laying_launch",
            "ship_building_total_months_launch_delivery",
        ]
        for i, vessel in enumerate(vessels_list):
            first_column_cell = sheet.cell(row=start_row + i, column=1)
            first_column_cell = set_excel_cell_style(
                first_column_cell,
                "ShtBack",
            )
            last_column_cell = sheet.cell(
                row=start_row + i,
                column=len(vessel_columns) + 2,
            )
            last_column_cell = set_excel_cell_style(
                last_column_cell,
                "ShtBack",
            )
            for col, attr in enumerate(vessel_columns):
                # Get the value of the attribute
                if (
                    attr == "ship_building_total_months_all_stages"
                    and show_production_stages_time
                ) or (
                    (attr in production_stages) and (not show_production_stages_time)
                ):
                    if i == 0:
                        vessels_formatting.append(cell.style)
                    else:
                        cell = sheet.cell(
                            row=start_row + i,
                            column=col + 2,
                        )
                        set_excel_cell_style(
                            cell,
                            "ShtBack",
                        )
                    continue
                value = getattr(vessel, attr.split(".")[0])
                for sub_attr in attr.split(".")[1:]:
                    value = getattr(value, sub_attr, "")

                # Set the cell value
                cell = sheet.cell(
                    row=start_row + i,
                    column=col + 2,
                    value=value if value else "",
                )
                if i == 0:
                    vessels_formatting.append(cell.style)
                else:
                    cell = set_excel_cell_style(
                        cell,
                        vessels_formatting[col],
                    )

        benchmark_summary_position = len(vessels_list) + start_row + 1
        benchmark_summary_fields = [
            ("achieved_premium", "achieved_premium", "OutNum0dp"),
            (
                "exposure_benchmark_premium",
                "net_benchmark_premium_pre_uw_adj",
                "OutNum0dp",
            ),
            ("experience_benchmark_premium", "experience_premium", "OutNum0dp"),
            ("weight_to_experience", "experience_weighting", "OutPerc0dp"),
            (
                "blended_premium_pre_adj",
                "blended_benchmark_premium_pre_uw_adj",
                "OutNum0dp",
            ),
            (None, "uw_adjustment", "OutPerc0dp"),
            (
                "blended_premium_post_adj",
                "blended_benchmark_premium_post_uw_adj",
                "OutNum0dp",
            ),
        ]

        non_hidden_columns = [
            col_letter
            for col_letter, col_dim in sheet.column_dimensions.items()
            if not col_dim.hidden
        ]

        # Get the count of non-hidden columns
        non_hidden_count = len(non_hidden_columns)

        # Create an empty row and apply the ShtBack style
        empty_row = benchmark_summary_position - 1
        sheet.insert_rows(empty_row)
        for col in range(1, non_hidden_count + 2):
            cell = sheet.cell(row=empty_row, column=col)
            set_excel_cell_style(cell, "ShtBack")

        for i, (field_name, value_node, format) in enumerate(benchmark_summary_fields):
            if field_name is None:
                field_name_cell = sheet.cell(
                    row=benchmark_summary_position + i,
                    column=2,
                    value="Underwriter Adjustment",
                )
                field_name_cell = set_excel_cell_style(
                    field_name_cell,
                    "ShtBack",
                )
            else:
                field_name_cell = sheet.cell(
                    row=benchmark_summary_position + i,
                    column=2,
                    value=getattr(
                        hxd.non_cds.labels.ship_building,
                        field_name,
                    ),
                )
                field_name_cell = set_excel_cell_style(
                    field_name_cell,
                    "ShtBack",
                )
            field_name_cell.font = openpyxl.styles.Font(bold=True, size=11)
            field_name_cell.alignment = openpyxl.styles.Alignment(
                horizontal="right"
            )  # Set right alignment

            set_excel_cell_style(
                sheet.cell(
                    row=benchmark_summary_position + i,
                    column=3,
                    value=getattr(
                        hxd.cds.layers[0].coverages.ship_building,
                        f"ship_building_{value_node}",
                    ),
                ),
                format,
            ).alignment = openpyxl.styles.Alignment(
                horizontal="right"
            )  # Set right alignment

            # Turn all other columns in this row to ShtBack style
            for col in range(1, non_hidden_count + 2):
                if (col == 2) or (col == 3):
                    continue
                set_excel_cell_style(
                    sheet.cell(
                        row=benchmark_summary_position + i,
                        column=col,
                    ),
                    "ShtBack",
                )

    if not is_renewal:
        for sheet_name in workbook.sheetnames[1:]:  # Skip the first sheet
            sheet = workbook[sheet_name]
            sheet.sheet_state = "hidden"
    else:
        if is_hull_coverage:
            generate_rate_change_sheet(hxd, workbook["Rate Change (Hull)"], "hull")
            if not is_iv:
                workbook["Rate Change (IV)"].sheet_state = "hidden"
            else:
                generate_rate_change_sheet(hxd, workbook["Rate Change (IV)"], "iv")
            if not is_war:
                workbook["Rate Change (War)"].sheet_state = "hidden"
            else:
                generate_rate_change_sheet(hxd, workbook["Rate Change (War)"], "war")
        elif is_loh_coverage:
            generate_rate_change_sheet(hxd, workbook["Rate Change (LOH)"], "loh")
        elif is_ship_building_coverage:
            generate_rate_change_sheet(
                hxd, workbook["Rate Change (Shipbuilders)"], "ship_building"
            )

    # Protect the sheet to prevent changes
    sheet.protection.enable()
    sheet.protection.set_password(constants.excel_password)

    # Write to file
    hull_rating = hxd.cds.exposure.granular.vessels.hull_rating
    with hull_rating.output_summary_xlsx.open("b") as f:
        workbook.save(f)
        hxd.non_cds.show_hide_toggles.hull.show_generated_output_summary_xlsx = True


def set_excel_cell_style(cell, style):
    if style:
        cell.style = style  # Set the new style

    # Apply the border to the cell
    if style == "ShtBack":
        cell.border = None
    else:
        # Define the border style
        thin_border = openpyxl.styles.Border(
            left=openpyxl.styles.Side(style="thin"),
            right=openpyxl.styles.Side(style="thin"),
            top=openpyxl.styles.Side(style="thin"),
            bottom=openpyxl.styles.Side(style="thin"),
        )
        cell.border = thin_border

    # Adjust the column width dynamically
    column_letter = openpyxl.utils.get_column_letter(cell.column)
    sheet = cell.parent
    if is_numeric(cell.value):
        multiplier = 2  # Larger multiplier for numbers
    else:
        multiplier = 1.2  # Smaller multiplier for text

    max_length = max(
        len(str(cell.value or "")) * multiplier,
        sheet.column_dimensions[column_letter].width or 0,
    )
    sheet.column_dimensions[column_letter].width = max_length
    cell.protection = openpyxl.styles.Protection(locked=True)
    return cell


def is_numeric(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


@hx.task
def portfolio_analysis_search_task(hxd, progress):
    filter_options = hxd.cds.portfolio_analysis.hull_rating.filter_options
    portfolio_metrics = hxd.cds.portfolio_analysis.hull_rating.portfolio_metrics
    filters = flatten_dict(dict(filter_options))

    db_vessels = portfolio_analysis_query_builder(filters)
    progress.update(0.7)

    if db_vessels is None or db_vessels.empty:
        return
    hxd.cds.portfolio_analysis.hull_rating.portfolio_metrics.vessels_count = len(
        db_vessels
    )
    portfolio_metrics.vessels = [{}] * len(db_vessels)
    fx_rates_df = params.fx_rates.df()
    currency = filter_options.currency
    fx_rate = (
        1
        if currency is None
        else (
            fx_rates_df[(fx_rates_df["ccy"] == currency)]["fx_rate"].iloc[0]
            if ((currency in list(fx_rates_df["ccy"])))
            else 1
        )
    )
    agreed_value_mask = db_vessels["original_agreed_value"].notnull()
    db_vessels.loc[agreed_value_mask, "agreed_value_converted"] = (
        db_vessels.loc[agreed_value_mask, "original_agreed_value"] * fx_rate
    )

    agreed_value_mask = db_vessels["agreed_value_converted"].notnull()
    portfolio_metrics.average_agreed_value = db_vessels.loc[
        agreed_value_mask, "agreed_value_converted"
    ].mean()

    achieved_premium_mask = (
        db_vessels["achieved_rate"].notnull()
        & db_vessels["agreed_value_converted"].notnull()
    )
    db_vessels.loc[achieved_premium_mask, "achieved_premium"] = (
        db_vessels.loc[achieved_premium_mask, "achieved_rate"]
        * db_vessels.loc[achieved_premium_mask, "agreed_value_converted"]
    )

    portfolio_metrics.average_achieved_rate = (
        db_vessels["achieved_premium"].sum()
        / db_vessels["agreed_value_converted"].fillna(0).sum()
    )

    columns_to_drop = [
        "achieved_premium",
        "AgreedValCurr",
    ]
    db_vessels.drop(columns=columns_to_drop, inplace=True)

    db_vessels = db_vessels.replace({np.nan: None})

    portfolio_metrics.vessels = db_vessels.to_dict(orient="records")
    progress.update(1)


@hx.task
def clear_portfolio_analysis_search_task(hxd, progress):
    pass


@hx.task
def lookup_loh_imos_task(hxd, progress):
    loh_prefix = "loh_"
    vessels = hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
    imos_set = set()
    for vessel in vessels:
        imo = vessel.loh_vessel_details.loh_imo
        if imo is not None:
            imos_set.add(imo)

    imos = list(imos_set)
    if len(imos) == 0:
        return

    db_vessels = get_vessels_by_imo(imos)
    # Retrieve columns from db_vessels
    columns = db_vessels.columns

    # Filter out the 'imo' column
    vessels_table_schema = [column for column in columns if column != "imo"]
    for vessel in vessels:
        imo = str(vessel.loh_vessel_details.loh_imo or "")
        if imo not in db_vessels["imo"].values:
            continue
        # add ModelYearOfBuild exception
        for key in vessels_table_schema:
            db_vessesl = db_vessels[db_vessels["imo"] == imo]
            try:
                setattr(
                    vessel.loh_vessel_details,
                    loh_prefix + key,
                    db_vessesl[key].values[0],
                )
            except Exception as e:
                try:
                    setattr(vessel, key, db_vessesl[key].values[0])
                except Exception as e:
                    hx.errors.validation(
                        f"Error setting attribute {key} for vessel {imo}: {e}"
                    )


@hx.task
def clear_vessels_task(hxd, progress):
    pass


@hx.task
def clear_loh_vessels_task(hxd, progress):
    pass


@hx.task
def set_vessels_defaults_task(hxd, progress):
    """
    This code sets default values for vessels based on the vessels_defaults structure.
    It iterates through each vessel in the vessels list and checks if any of its attributes have a value of None.
    If an attribute has a value of None, it sets the attribute to the corresponding value from the vessels_defaults structure.
    This ensures that only the attributes specified in vessels_defaults are set to default values, and only if they are currently None.
    """
    vessels = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list
    vessels_defaults = dict(hxd.cds.exposure.granular.vessels.vessels_defaults.hull)
    for vessel in vessels:
        for key, value in vessels_defaults.items():
            if key in [
                "coverage",
                "deductible",
                "uw_adjustment",
                "agreed_value",
                "inception_date",
                "expiry_date",
            ]:
                if key in ["inception_date", "expiry_date"]:
                    if getattr(vessel, key) is None:
                        setattr(
                            vessel,
                            key,
                            value.selected if value.selected else value.calculated,
                        )

                elif getattr(vessel, key) is None:
                    setattr(vessel, key, value)
            elif getattr(vessel.vessel_details, key) is None:
                setattr(vessel.vessel_details, key, value)


@hx.task
def set_loh_vessels_defaults_task(hxd, progress):
    """
    This code sets default values for vessels based on the vessels_defaults structure.
    It iterates through each vessel in the vessels list and checks if any of its attributes have a value of None.
    If an attribute has a value of None, it sets the attribute to the corresponding value from the vessels_defaults structure.
    This ensures that only the attributes specified in vessels_defaults are set to default values, and only if they are currently None.
    """
    vessels = hxd.cds.exposure.granular.vessels.loh_rating.loh_vessels_list
    vessels_defaults = dict(hxd.cds.exposure.granular.vessels.vessels_defaults.loh)
    prefix = "loh_"

    vessel_details_fields = [
        prefix + "imo",
        prefix + "vessel_name",
        prefix + "vessel_type",
        prefix + "year_built",
        prefix + "gross_tonnage",
    ]

    for vessel in vessels:
        for key, value in vessels_defaults.items():
            parent = (
                vessel.loh_vessel_details if key in vessel_details_fields else vessel
            )
            if getattr(parent, key) is None:
                setattr(parent, key, value)


# Importing expiring policy for rate change
"""
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
"""


@hx.task
def ship_building_number_of_vessels_task(hxd, progress):
    ship_building_vessels_list = (
        hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list
    )

    number_of_vessels = hxd.cds.layers[
        0
    ].coverages.ship_building.ship_building_number_of_vessels

    if number_of_vessels is None or number_of_vessels == 0:
        return

    if len(ship_building_vessels_list) >= number_of_vessels:
        hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list = list(
            hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list
        )[
            :number_of_vessels
        ]
        new_list = [
            hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list[
                i
            ]
            for i in range(number_of_vessels)
        ]
        hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list = list(
            new_list
        )
    elif len(ship_building_vessels_list) < number_of_vessels:
        hxd.cds.exposure.granular.vessels.ship_building_rating.ship_building_vessels_list.extend(
            [{} for _ in range(len(ship_building_vessels_list), number_of_vessels)]
        )


@hx.task
def policy_json_download_task(hxd, progress):
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    expiring_data = get_expiring_data(hxd)
    with hxd.cds.rate_change.output_json_example_data.open("t") as json_file:
        json.dump(expiring_data, json_file, indent=4)


# Import expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    expiring_data = get_expiring_data(hxd)

    # Get fields from json response and push to hxd
    coverages = ["hull", "iv", "war", "loh", "ship_building"]
    for idx, layer in enumerate(hxd.cds.layers):
        hxd_coverages = [
            layer.rate_change.hull,
            layer.rate_change.iv,
            layer.rate_change.war,
            layer.rate_change.loh,
            layer.rate_change.ship_building,
        ]

        # By coverage
        for cvg, hxd_cvg in zip(coverages, hxd_coverages):
            is_override = cvg in ["iv", "war"]
            written_line = expiring_data["cds"]["layers"][idx]["coverages"][cvg][
                "written_line"
            ]
            hxd_cvg.expiring_policy_info.expiring_written_line = (
                written_line.get("selected") if is_override else written_line
            ) or 0

            hxd_cvg.expiring_policy_info.expiring_premium_annualised = (
                hxd_cvg.expiring_policy_info.expiring_premium
            ) = (expiring_data["cds"]["layers"][idx]["coverages"][cvg][
                "quoted_premium_pro_rated_100pct"
            ]) or 0

            hxd_cvg.expiring_policy_info.expiring_benchmark_premium = (expiring_data[
                "cds"
            ]["layers"][idx]["coverages"][cvg]["benchmark_premium_pro_rated_100pct"]) or 0

            hxd_cvg.expiring_policy_info.expiring_bpi = (expiring_data["cds"]["layers"][
                idx
            ]["coverages"][cvg]["bpi"]) or 0


### --- RATE CHANGE --- ###
def get_expiring_data(hxd):
    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = (
        hxd.cds.rate_change.expiring_policy_option_id.selected
    )  # or 85244 # NOTE: id used for testing
    expiring_response = hx_renew.snapshots.get_snapshot(
        policy_option_id=expiring_policy_option_id, stream=False
    ).json()
    expiring_data = expiring_response["data"]

    return expiring_data


# Use map to apply the transformation to all items in the list
def flatten_vessel_details(item):
    if "vessel_details" in item:
        # Extract fields from 'vessel_details' and merge them with the parent
        vessel_details = item.pop("vessel_details")
        item.update(vessel_details)
    return item


def clean_hull_vessels_expiring_data(hxd, expiring_data):
    """
    Sorts the expiring aircrafts in the same order as the renewing aircrafts.
    Renewal may have additional aircrafts which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of aircrafts that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional aircrafts that are present in renewal but not in expiring.
    """

    # Map structures
    hxd_structures = {
        "vessels_list": hxd.rate_change.hull_vessels,
    }

    # Ensure expiring list of vessels follows the same order as renewal
    list_name = "vessels_list"
    expiring_list = expiring_data["cds"]["exposure"]["granular"]["vessels"][
        "hull_rating"
    ][list_name]

    renewal_list = json.loads(hxd_structures[list_name])
    # # Use enumerate properly to loop over the vessels list
    # for i, vessel in enumerate(renewal_list):
    #     if "imo" in vessel:
    #         # Move "imo" under "vessel_details"
    #         renewal_list[i]["vessel_details"] = {"imo": vessel.pop("imo")}
    #     if "iv_agreed_value" in vessel:
    #         # Ensure "iv" exists before adding "iv_agreed_value"
    #         renewal_list[i]["iv"] = vessel.get("iv", {})
    #         renewal_list[i]["iv"]["iv_agreed_value"] = vessel.pop("iv_agreed_value")

    # Create a lookup for the order of keys from the renewal list
    renewal_order = {d["unique_imo"]: idx for idx, d in enumerate(renewal_list)}

    # Partition expiring_list into items with keys in renewal_order and those without.
    # YZ: Others here are in the Dropped
    common = [d for d in expiring_list if d["unique_imo"] in renewal_order]
    others = [d for d in expiring_list if d["unique_imo"] not in renewal_order]

    # Sort items present in the renewal_order
    common.sort(key=lambda d: renewal_order[d["unique_imo"]])
    sorted_expiring_list = common + others

    expiring_data_sorted = copy.deepcopy(expiring_data)
    expiring_data_sorted["cds"]["exposure"]["granular"]["vessels"]["hull_rating"][
        list_name
    ] = sorted_expiring_list

    # Build a set of keys from the expiring list and renewal list
    expiring_keys = {item["unique_imo"] for item in sorted_expiring_list}
    renewal_keys = {item["unique_imo"] for item in renewal_list}

    # Partition the renewal list based on renewal_keys and expiring_keys
    expiring_list_common = [
        item for item in sorted_expiring_list if item["unique_imo"] in renewal_keys
    ]
    renewal_list_others = [
        item for item in renewal_list if item["unique_imo"] not in expiring_keys
    ]
    expiring_list_dropped = [
        item for item in sorted_expiring_list if item["unique_imo"] not in renewal_keys
    ]

    # YZ: What are the following steps doing? To set up initial values for the data frame?
    expiring_data_common = copy.deepcopy(expiring_data)
    expiring_data_others = copy.deepcopy(
        expiring_data
    )  # Calling this expiring_data even though the specified list will contain renewal elements
    expiring_data_dropped = copy.deepcopy(expiring_data)

    # YZ: to update the three dataframe
    expiring_data_common["cds"]["exposure"]["granular"]["vessels"]["hull_rating"][
        list_name
    ] = expiring_list_common
    expiring_data_others["cds"]["exposure"]["granular"]["vessels"]["hull_rating"][
        list_name
    ] = renewal_list_others
    expiring_data_dropped["cds"]["exposure"]["granular"]["vessels"]["hull_rating"][
        list_name
    ] = expiring_list_dropped

    return (
        expiring_data_sorted,
        expiring_data_common,
        expiring_data_others,
        expiring_data_dropped,
    )


def clean_shipbuilders_vessels_data(hxd, expiring_data):
    """
    Sorts the expiring aircrafts in the same order as the renewing aircrafts.
    Renewal may have additional aircrafts which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of aircrafts that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional aircrafts that are present in renewal but not in expiring.
    """

    # Ensure expiring list of vessels follows the same order as renewal
    expiring_list = expiring_data["cds"]["exposure"]["granular"]["vessels"][
        "ship_building_rating"
    ]["ship_building_vessels_list"]

    renewal_list = json.loads(hxd.rate_change.shipbuilders_vessels)

    # Create a lookup for the order of keys from the renewal list
    renewal_order = {
        d["ship_building_index"]: idx for idx, d in enumerate(renewal_list)
    }

    # Partition expiring_list into items with keys in renewal_order and those without
    common = [d for d in expiring_list if d["ship_building_index"] in renewal_order]
    others = [d for d in expiring_list if d["ship_building_index"] not in renewal_order]

    # Sort items present in the renewal_order
    common.sort(key=lambda d: renewal_order[d["ship_building_index"]])
    sorted_expiring_list = common + others

    expiring_data_sorted = copy.deepcopy(expiring_data)
    expiring_data_sorted["cds"]["exposure"]["granular"]["vessels"][
        "ship_building_rating"
    ]["ship_building_vessels_list"] = sorted_expiring_list

    # Build a set of keys from the expiring list and renewal list
    expiring_keys = {item["ship_building_index"] for item in sorted_expiring_list}
    renewal_keys = {item["ship_building_index"] for item in renewal_list}

    # Partition the renewal list based on renewal_keys and expiring_keys
    expiring_list_common = [
        item
        for item in sorted_expiring_list
        if item["ship_building_index"] in renewal_keys
    ]
    renewal_list_others = [
        item
        for item in renewal_list
        if item["ship_building_index"] not in expiring_keys
    ]
    expiring_list_dropped = [
        item
        for item in sorted_expiring_list
        if item["ship_building_index"] not in renewal_keys
    ]

    expiring_data_common = copy.deepcopy(expiring_data)
    expiring_data_others = copy.deepcopy(
        expiring_data
    )  # Calling this expiring_data even though the specified list will contain renewal elements
    expiring_data_dropped = copy.deepcopy(expiring_data)

    expiring_data_common["cds"]["exposure"]["granular"]["vessels"][
        "ship_building_rating"
    ]["ship_building_vessels_list"] = expiring_list_common
    expiring_data_others["cds"]["exposure"]["granular"]["vessels"][
        "ship_building_rating"
    ]["ship_building_vessels_list"] = renewal_list_others
    expiring_data_dropped["cds"]["exposure"]["granular"]["vessels"][
        "ship_building_rating"
    ]["ship_building_vessels_list"] = expiring_list_dropped

    return (
        expiring_data_sorted,
        expiring_data_common,
        expiring_data_others,
        expiring_data_dropped,
    )


def clean_loh_vessels_data(hxd, expiring_data):
    """
    Sorts the expiring aircrafts in the same order as the renewing aircrafts.
    Renewal may have additional aircrafts which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of aircrafts that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional aircrafts that are present in renewal but not in expiring.
    """

    # Ensure expiring list of vessels follows the same order as renewal
    expiring_list = expiring_data["cds"]["exposure"]["granular"]["vessels"][
        "loh_rating"
    ]["loh_vessels_list"]

    renewal_list = json.loads(hxd.rate_change.loh_vessels)

    # Create a lookup for the order of keys from the renewal list
    renewal_order = {
        d["loh_unique_identifier"]: idx for idx, d in enumerate(renewal_list)
    }

    # Partition expiring_list into items with keys in renewal_order and those without
    common = [d for d in expiring_list if d["loh_unique_identifier"] in renewal_order]
    others = [
        d for d in expiring_list if d["loh_unique_identifier"] not in renewal_order
    ]

    # Sort items present in the renewal_order
    common.sort(key=lambda d: renewal_order[d["loh_unique_identifier"]])
    sorted_expiring_list = common + others

    expiring_data_sorted = copy.deepcopy(expiring_data)
    expiring_data_sorted["cds"]["exposure"]["granular"]["vessels"]["loh_rating"][
        "loh_vessels_list"
    ] = sorted_expiring_list

    # Build a set of keys from the expiring list and renewal list
    expiring_keys = {item["loh_unique_identifier"] for item in sorted_expiring_list}
    renewal_keys = {item["loh_unique_identifier"] for item in renewal_list}

    # Partition the renewal list based on renewal_keys and expiring_keys
    expiring_list_common = [
        item
        for item in sorted_expiring_list
        if item["loh_unique_identifier"] in renewal_keys
    ]
    renewal_list_others = [
        item
        for item in renewal_list
        if item["loh_unique_identifier"] not in expiring_keys
    ]
    expiring_list_dropped = [
        item
        for item in sorted_expiring_list
        if item["loh_unique_identifier"] not in renewal_keys
    ]

    expiring_data_common = copy.deepcopy(expiring_data)
    expiring_data_others = copy.deepcopy(
        expiring_data
    )  # Calling this expiring_data even though the specified list will contain renewal elements
    expiring_data_dropped = copy.deepcopy(expiring_data)

    expiring_data_common["cds"]["exposure"]["granular"]["vessels"]["loh_rating"][
        "loh_vessels_list"
    ] = expiring_list_common
    expiring_data_others["cds"]["exposure"]["granular"]["vessels"]["loh_rating"][
        "loh_vessels_list"
    ] = renewal_list_others
    expiring_data_dropped["cds"]["exposure"]["granular"]["vessels"]["loh_rating"][
        "loh_vessels_list"
    ] = expiring_list_dropped

    return (
        expiring_data_sorted,
        expiring_data_common,
        expiring_data_others,
        expiring_data_dropped,
    )


@hx.task
def rarc_task(hxd, progress):

    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected

    if not expiring_policy_option_id:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get correct buckets based on coverage
    hull_buckets, iv_buckets, war_buckets, loh_buckets, ship_builders_buckets = (
        rate_change_buckets(hxd)
    )

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(
        os.path.dirname(__file__), data_schema_static_filename
    )
    # expiring_policy_option_id = 243035 # NOTE: for debugging

    # Prepare arguments for calculate_repriced_values() function
    rating_type = ""
    vessels_list_name = ""
    expiring_data = get_expiring_data(hxd)
    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = {
        "cds": expiring_data["cds"],
        "model_state": expiring_data["model_state"],
        "hx_core": expiring_data["hx_core"],
        "rate_change": expiring_data["rate_change"],
    }
    if hxd.non_cds.show_hide_toggles.hull.show_hull_coverage:
        # Get expiring data split between common and other aircrafts
        (
            expiring_data_sorted,
            expiring_data_common,
            expiring_data_others,
            expiring_data_dropped,
        ) = clean_hull_vessels_expiring_data(hxd, expiring_data)
        rating_type = "hull_rating"
        vessels_list_name = "vessels_list"
        kw_args = {
            "custom_expiring_data": [
                dict(expiring_data_sorted),
                dict(expiring_data_common),
                dict(expiring_data_others),
                dict(expiring_data_dropped),
            ],
            "split_list_path": f"cds/exposure/granular/vessels/{rating_type}/{vessels_list_name}",
            "matching_key": "unique_imo",
            "additional_items_bucket": "exposure",
        }

        # Create RateChangeLib instances
        hull_rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=hull_buckets,
            layers_path="cds/layers",
            expiring_actual_prem="coverages/hull/quoted_premium_policy_term_100pct",
            expiring_technical_prem="coverages/hull/benchmark_premium_policy_term_100pct",
            async_tasks=[],  # Pass the actual tasks, not strings
            data_schema_static_path=data_schema_static_path,
        )

        future_hull = calculate_rate_change(hull_rc, kw_args)
        # Wait for all tasks to complete and retrieve results
        for (
            hxd_layer,
            hull_rarc,
        ) in zip(hxd.cds.layers, future_hull):
            if hull_rarc and (len(hull_rarc) > 0):
                hxd_layer.rate_change.hull = replace_nan_with_none(hull_rarc)

        if hxd.non_cds.show_hide_toggles.iv.show_iv_coverage:
            iv_rc = RateChangeLib(
                hxd=hxd,
                progress=progress,
                buckets=iv_buckets,
                layers_path="cds/layers",
                expiring_actual_prem="coverages/iv/quoted_premium_policy_term_100pct",
                expiring_technical_prem="coverages/iv/benchmark_premium_policy_term_100pct",
                async_tasks=[],  # Pass the actual tasks, not strings
                data_schema_static_path=data_schema_static_path,
            )

            future_iv = calculate_rate_change(iv_rc, kw_args)
            if future_iv:
                for hxd_layer, iv_rarc in zip(hxd.cds.layers, future_iv):
                    if iv_rarc and (len(iv_rarc) > 0):
                        hxd_layer.rate_change.iv = replace_nan_with_none(iv_rarc)

        if hxd.non_cds.show_hide_toggles.war.show_war_coverage:
            war_rc = RateChangeLib(
                hxd=hxd,
                progress=progress,
                buckets=war_buckets,
                layers_path="cds/layers",
                expiring_actual_prem="coverages/war/quoted_premium_policy_term_100pct",
                expiring_technical_prem="coverages/war/benchmark_premium_policy_term_100pct",
                async_tasks=[],  # Pass the actual tasks, not strings
                data_schema_static_path=data_schema_static_path,
            )
            future_war = calculate_rate_change(war_rc, kw_args)
            if future_war:
                for hxd_layer, war_rarc in zip(hxd.cds.layers, future_war):
                    if war_rarc and (len(war_rarc) > 0):
                        hxd_layer.rate_change.war = replace_nan_with_none(war_rarc)

    elif hxd.non_cds.show_hide_toggles.loh.show_loh_coverage:
        rating_type = "loh_rating"
        vessels_list_name = "loh_vessels_list"

        (
            expiring_data_sorted,
            expiring_data_common,
            expiring_data_others,
            expiring_data_dropped,
        ) = clean_loh_vessels_data(hxd, expiring_data)
        kw_args = {
            "custom_expiring_data": [
                dict(expiring_data_sorted),
                dict(expiring_data_common),
                dict(expiring_data_others),
                dict(expiring_data_dropped),
            ],
            "split_list_path": f"cds/exposure/granular/vessels/{rating_type}/{vessels_list_name}",
            "matching_key": "loh_unique_identifier",
            "additional_items_bucket": "exposure",
        }

        # Create RateChangeLib instances
        loh_rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=loh_buckets,
            layers_path="cds/layers",
            expiring_actual_prem="coverages/loh/quoted_premium_policy_term_100pct",
            expiring_technical_prem="coverages/loh/benchmark_premium_policy_term_100pct",
            async_tasks=[],  # Pass the actual tasks, not strings
            data_schema_static_path=data_schema_static_path,
        )

        loh_rarc_list = calculate_rate_change(loh_rc, kw_args)
        if loh_rarc_list:
            for hxd_layer, loh_rarc in zip(hxd.cds.layers, loh_rarc_list):
                if loh_rarc and (len(loh_rarc) > 0):
                    hxd_layer.rate_change.loh = replace_nan_with_none(loh_rarc)

    elif hxd.non_cds.show_hide_toggles.ship_building.show_ship_building_coverage:
        rating_type = "ship_building_rating"
        vessels_list_name = "ship_building_vessels_list"

        (
            expiring_data_sorted,
            expiring_data_common,
            expiring_data_others,
            expiring_data_dropped,
        ) = clean_shipbuilders_vessels_data(hxd, expiring_data)
        kw_args = {
            "custom_expiring_data": [
                dict(expiring_data_sorted),
                dict(expiring_data_common),
                dict(expiring_data_others),
                dict(expiring_data_dropped),
            ],
            "split_list_path": f"cds/exposure/granular/vessels/{rating_type}/{vessels_list_name}",
            "matching_key": "ship_building_index",
            "additional_items_bucket": "exposure",
        }

        # Create RateChangeLib instances
        ship_building_rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=ship_builders_buckets,
            layers_path="cds/layers",
            expiring_actual_prem="coverages/ship_building/quoted_premium_policy_term_100pct",
            expiring_technical_prem="coverages/ship_building/benchmark_premium_policy_term_100pct",
            async_tasks=[],  # Pass the actual tasks, not strings
            data_schema_static_path=data_schema_static_path,
        )

        ship_building_rarc_list = calculate_rate_change(ship_building_rc, kw_args)
        if ship_building_rarc_list:
            for hxd_layer, ship_building_rarc in zip(
                hxd.cds.layers, ship_building_rarc_list
            ):
                if ship_building_rarc and (len(ship_building_rarc) > 0):
                    hxd_layer.rate_change.ship_building = replace_nan_with_none(
                        ship_building_rarc
                    )


def replace_nan_with_none(data):
    if isinstance(data, list):
        return [replace_nan_with_none(item) for item in data]
    elif isinstance(data, dict):
        return {key: replace_nan_with_none(value) for key, value in data.items()}
    elif data is np.nan:
        return None
    else:
        return data


# --- Rate Change for Hull, IV, and War --- #
def calculate_rate_change(rate_change_lib, kw_args):
    rate_change_lib.calculate_repriced_values(**kw_args)
    _, rarc_list = rate_change_lib.calculate_rarc_by_layer()
    return rarc_list


def filter_data_schema(data_schema_csv, filters):
    df = pd.read_csv(data_schema_csv, error_bad_lines=False, warn_bad_lines=True)
    filtered_dfs = []  # List to store filtered DataFrames

    # Apply filtering based on filter objects
    for filter_obj in filters:
        if callable(filter_obj):  # If the filter is a callable function
            filtered_dfs.append(df[filter_obj(df)])
        elif isinstance(filter_obj, dict):  # If the filter is a dictionary
            column = filter_obj.get("column")
            operator = filter_obj.get("operator")
            value = filter_obj.get("value")

            if operator == "gt":  # Greater than
                filtered_dfs.append(df[df[column] > value])
            elif operator == "lt":  # Less than
                filtered_dfs.append(df[df[column] < value])
            elif operator == "eq":  # Equal to
                filtered_dfs.append(df[df[column] == value])
            elif operator == "neq":  # Not equal to
                filtered_dfs.append(df[df[column] != value])
            elif operator == "contains":  # Contains (for strings)
                filtered_dfs.append(df[df[column].str.contains(value, na=False)])
            # Add more operators as needed

    # Combine all filtered DataFrames using pd.concat and drop duplicates
    if filtered_dfs:
        df = pd.concat(filtered_dfs).drop_duplicates()

    return df


def filter_and_replace_json(paths, expiring_json):
    ignored_fields = [
        "insured_country",
        "insured_postal_code",
        "insured_state_or_province",
        "is_admitted_or_surplus",
        "is_free_trade_zone",
        "facility_reference",
        "uw_rationale",
        "trifocus",
        "claims",
        "application_date",
        "import_expiry_prompt",
        "landing_page_info",
        "inconsistent_product_msg",
        "has_sql_conn_failed",
        "sql_failure_msg",
        "data_input_experience_table",
    ]

    def traverse_and_filter(current_obj, current_path):
        if isinstance(current_obj, dict):
            # Check if the dictionary contains the specific fields
            if all(
                key in current_obj
                for key in ["selected", "calculated", "is_overridden"]
            ):
                # Compute the value based on the logic
                computed_value = (
                    current_obj["selected"]
                    if current_obj["is_overridden"]
                    else current_obj["calculated"]
                )
                # Assign the computed value to the "calculated" field
                current_obj["calculated"] = computed_value
                # Remove all other fields except "calculated"
                current_obj = {"calculated": current_obj["calculated"]}

            # Traverse each key in the dictionary
            keys_to_remove = []
            for key, value in current_obj.items():
                # Remove specific fields if they exist
                if key in ignored_fields:
                    keys_to_remove.append(key)
                    continue
                # Exclude "calculated" from the path
                new_path = (
                    f"{current_path}/{key}"
                    if current_path and key != "calculated"
                    else key
                )
                filtered_value = traverse_and_filter(value, new_path)
                if filtered_value is None:
                    keys_to_remove.append(key)
                else:
                    current_obj[key] = filtered_value
            for key in keys_to_remove:
                del current_obj[key]
            return current_obj if current_obj else None
        elif isinstance(current_obj, list):
            # Traverse each item in the list
            filtered_list = []
            # Remove specific fields if they exist
            if current_obj in ignored_fields:
                return None
            for item in current_obj:
                filtered_item = traverse_and_filter(item, current_path)
                if filtered_item is not None:
                    filtered_list.append(filtered_item)
            return filtered_list if filtered_list else None
        else:
            # Leaf node, check if the path exists in paths
            return current_obj if current_path in paths else None

    # Start traversal from the root
    return traverse_and_filter(expiring_json, "")


@hx.task
def start_renewal_task(hxd, progress):

    model_state = hxd.model_state
    model_state.pressed_start_renewal_task = True
    model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = (
        hx.meta.expiring_policy_option_id
    )  # or 831405 # NOTE: For testing in dev mode

    data_schema_csv = "./model/algorithms/data_schema/exported_data_schema.csv"
    # data_schema_csv = (
    #     "/workspace/editing/algorithms/data_schema/exported_data_schema.csv"
    # )
    filters = [
        {"column": "Mode", "operator": "eq", "value": "input"},
        # {"column": "Mode", "operator": "eq", "value": "override"},
    ]
    filtered_data_schema = filter_data_schema(data_schema_csv, filters)
    show_hull_coverage = False

    try:
        expiring_nodes = filtered_data_schema["Path"].tolist()
        expiring_response = hx_renew.snapshots.get_snapshot(
            policy_option_id=expiring_policy_option_id, stream=False
        ).json()
        expiring_data = expiring_response["data"]
        expiring_show_hide_toggles = expiring_data["non_cds"]["show_hide_toggles"]
        expiring_shipbuilders_experience_data_input = copy.deepcopy(
            expiring_data["cds"]["experience_rating"]["ship_building"][
                "data_input_experience_table"
            ]
        )

        show_hull_coverage = (
            expiring_show_hide_toggles["hull"]["show_hull_coverage"]
            if "hull" in expiring_show_hide_toggles
            else False
        )

        show_iv_coverage = (
            expiring_show_hide_toggles["iv"]["show_iv_coverage"]
            if "iv" in expiring_show_hide_toggles
            else False
        )

        show_war_coverage = (
            expiring_show_hide_toggles["war"]["show_war_coverage"]
            if "war" in expiring_show_hide_toggles
            else False
        )

        show_loh_coverage = (
            expiring_show_hide_toggles["loh"]["show_loh_coverage"]
            if "loh" in expiring_show_hide_toggles
            else False
        )

        show_ship_building_coverage = (
            expiring_show_hide_toggles["ship_building"]["show_ship_building_coverage"]
            if "ship_building" in expiring_show_hide_toggles
            else False
        )

        filtered_expiring_data = filter_and_replace_json(expiring_nodes, expiring_data)
        hxd.cds = filtered_expiring_data["cds"]

        hull_vessels = hxd.cds.exposure.granular.vessels.hull_rating.vessels_list
        if len(hull_vessels) > 0:
            for vessel in hull_vessels:
                vessel.inception_date = hxd.hx_core.inception_date
                vessel.expiry_date = hxd.hx_core.expiry_date

        coverages = hxd.cds.layers[0].coverages

        for coverage in coverages:
            coverage_name, coverage_data = coverage
            if coverage_name not in expiring_data["cds"]["layers"][0]["coverages"] or (
                "section_reference"
                not in expiring_data["cds"]["layers"][0]["coverages"][coverage_name]
            ):
                continue
            expiring_section_reference = expiring_data["cds"]["layers"][0]["coverages"][
                coverage_name
            ]["section_reference"]

            # Automatically update the 7th and 8th positions as an integer
            if expiring_section_reference and len(expiring_section_reference) >= 7:
                # Extract the 7th and 8th characters, convert to integer, and increment
                prefix = expiring_section_reference[:6]
                numeric_part = int(expiring_section_reference[6:8]) + 1
                suffix = expiring_section_reference[8:]

                # Reconstruct the updated section reference
                section_reference = f"{prefix}{numeric_part:02d}{suffix}"
            else:
                section_reference = expiring_section_reference

            # Set the updated section reference in the coverage object
            setattr(coverage_data, "section_reference", section_reference)

        yoa_map = {}
        for experience_row in expiring_shipbuilders_experience_data_input:
            yoa_map[experience_row["yoa"]] = {
                "previous_insurer": experience_row["previous_insurer"],
                "number_of_vessels": experience_row["number_of_vessels"],
                "acquisition_cost": experience_row["acquisition_cost"],
                "premium": experience_row["premium"],
                "total_incurred_shared_line": experience_row[
                    "total_incurred_shared_line"
                ],
                "large_incurred_shared_line": experience_row[
                    "large_incurred_shared_line"
                ],
                "signed_line": experience_row["signed_line"],
                "rate_change": experience_row["rate_change"],
                "is_include_year": experience_row["is_include_year"],
            }

        hxd.cds.experience_rating.ship_building.claims_date = hxd.hx_core.inception_date
        data_experience_table = (
            hxd.cds.experience_rating.ship_building.data_input_experience_table
        )

        hxd.cds.experience_rating.ship_building.extracted_policies = [{}] * len(
            data_experience_table
        )
        imported_policies_table = (
            hxd.cds.experience_rating.ship_building.extracted_policies
        )

        ship_building_policy_reference = hxd.cds.layers[
            0
        ].coverages.ship_building.section_reference

        current_year = int(hxd.hx_core.inception_date.year)

        start_year = current_year - 1
        policy_reference_substring_length = 6
        rate_year_substring_length = 2
        policies_df = pd.DataFrame()

        if (
            ship_building_policy_reference
            and ship_building_policy_reference != ""
            and len(ship_building_policy_reference) >= policy_reference_substring_length
        ):
            policy_reference_prefix = ship_building_policy_reference[
                :policy_reference_substring_length
            ]
            policy_reference_yoas = [
                (
                    policy_reference_prefix
                    + str((start_year - i))[rate_year_substring_length:]
                )
                for i in range(10 - 2, -1, -1)
            ]
            ship_building_policy_reference
            policies = get_policies_by_policy_references(
                policy_references=policy_reference_yoas
            )
            if len(policies) > 1:
                columns = [
                    "policy_reference",
                    "written_or_estimated_premium",
                    "total_incurred_shared_line",
                    "rate_change",
                    "external_acquisition_cost",
                    "internal_acquisition_cost",
                    "signed_line",
                    "yoa",
                ]
                policies_df = pd.DataFrame.from_records(policies, columns=columns)

            all_policies_grouped_by_yoa = calculate_avg_yoa_rate_change()
            for i in range(len(data_experience_table)):
                yoa = data_experience_table[i].yoa
                if yoa in yoa_map:
                    imported_policies_table[i].previous_insurer = yoa_map[yoa][
                        "previous_insurer"
                    ]["selected"]
                    data_experience_table[i].number_of_vessels = yoa_map[yoa][
                        "number_of_vessels"
                    ]

                    imported_policies_table[i].acquisition_cost = yoa_map[yoa][
                        "acquisition_cost"
                    ]["selected"]

                    imported_policies_table[i].written_or_estimated_premium = (
                        yoa_map[yoa]["premium"]["selected"] or 0
                    ) * (1 - (yoa_map[yoa]["acquisition_cost"]["selected"] or 0))

                    imported_policies_table[i].total_incurred_shared_line = yoa_map[
                        yoa
                    ]["total_incurred_shared_line"]["selected"]

                    data_experience_table[i].large_incurred_shared_line = yoa_map[yoa][
                        "large_incurred_shared_line"
                    ]

                    imported_policies_table[i].signed_line = yoa_map[yoa][
                        "signed_line"
                    ]["selected"]

                    rate_change_expiring = yoa_map[yoa]["rate_change"]["selected"]
                    rate_change_value = (
                        rate_change_expiring
                        if rate_change_expiring
                        else (
                            all_policies_grouped_by_yoa.loc[yoa, "rate_change"]
                            if yoa in all_policies_grouped_by_yoa.index
                            else 1
                        )
                    )
                    imported_policies_table[i].rate_change = rate_change_value

                    imported_policies_table[i].is_include_year = yoa_map[yoa][
                        "is_include_year"
                    ]["selected"]

                    imported_policies_table[i].yoa = yoa
                    if not imported_policies_table[i].previous_insurer:
                        if not policies_df.empty:
                            # Check if the policy reference is in the DataFrame
                            matching_row = policies_df[policies_df["yoa"] == yoa]
                            imported_policies_table[i].previous_insurer = (
                                "Non-Beazley" if matching_row.empty else "Beazley"
                            )
                        else:
                            imported_policies_table[i].previous_insurer = "Non-Beazley"

        hxd.cds.standard_fields.is_renewal = True
        upsert_hx_meta_policy_references(
            hxd.cds.layers[0].coverages,
            show_hull_coverage,
            show_iv_coverage,
            show_war_coverage,
            show_loh_coverage,
            show_ship_building_coverage,
        )

        if show_hull_coverage:
            lookup_imos(hxd.cds.exposure.granular.vessels.hull_rating.vessels_list)
            hxd.cds.exposure.granular.vessels.hull_rating.is_modelling = False

    except Exception as e:
        model_state.landing_page_info = f"❗❗ Failed to fetch expiring data. Please proceed and enter data manually. ❗❗\n\nError for dev team:\n{e}"
        print(e)

    finally:
        hxd.cds.standard_fields.is_renewal = True
        if show_hull_coverage:
            lookup_imos(hxd.cds.exposure.granular.vessels.hull_rating.vessels_list)
            hxd.cds.exposure.granular.vessels.hull_rating.is_modelling = False


def upsert_hx_meta_policy_references(
    coverages,
    show_hull_coverage,
    show_iv_coverage,
    show_war_coverage,
    show_loh_coverage,
    show_ship_building_coverage,
):
    # add the Policy Reference to PAS
    hx.meta.pas_references.clear()
    pas_references_set = set()

    if show_hull_coverage:
        if (
            coverages.hull.section_reference
            and len(coverages.hull.section_reference) >= 8
        ):
            pas_references_set.add(coverages.hull.section_reference[:8])

        if show_iv_coverage and (
            coverages.iv.section_reference and len(coverages.iv.section_reference) >= 8
        ):
            pas_references_set.add(coverages.iv.section_reference[:8])

        if show_war_coverage and (
            coverages.war.section_reference
            and len(coverages.war.section_reference) >= 8
        ):
            pas_references_set.add(coverages.war.section_reference[:8])

    elif show_loh_coverage and (
        coverages.loh.section_reference and len(coverages.loh.section_reference) >= 8
    ):
        pas_references_set.add(coverages.loh.section_reference[:8])

    elif (show_ship_building_coverage) and (
        coverages.ship_building.section_reference
        and len(coverages.ship_building.section_reference) >= 8
    ):
        pas_references_set.add(coverages.ship_building.section_reference[:8])

    hx.meta.pas_references.extend(list(pas_references_set))


@hx.task
def upsert_hx_meta_policy_references_task(hxd, progress):
    """
    Task to update hx.meta.pas_references with the policy references from the coverages.
    """
    coverages = hxd.cds.layers[0].coverages
    show_hide_toggles = hxd.non_cds.show_hide_toggles
    show_hull_coverage = show_hide_toggles.hull.show_hull_coverage
    show_iv_coverage = show_hide_toggles.iv.show_iv_coverage
    show_war_coverage = show_hide_toggles.war.show_war_coverage
    show_loh_coverage = show_hide_toggles.loh.show_loh_coverage
    show_ship_building_coverage = (
        show_hide_toggles.ship_building.show_ship_building_coverage
    )
    upsert_hx_meta_policy_references(
        coverages,
        show_hull_coverage,
        show_iv_coverage,
        show_war_coverage,
        show_loh_coverage,
        show_ship_building_coverage,
    )


def push_loh_vessels_to_datamart(hxd):
    """
    Pushes the LOH vessels data to the datamart.
    """
    # Extract root and layer-level attributes
    is_renewal = 1 if hxd.cds.standard_fields.is_renewal else 0
    currency = str(hxd.cds.currencies.source_currency or "")
    inception_date = hxd.cds.standard_fields.inception_date or date(1900, 1, 1)
    expiry_date = hxd.cds.standard_fields.expiry_date or date(1900, 1, 1)
    layer = hxd.cds.layers[0]
    policy_reference = str(layer.coverages.loh.section_reference or "")
    written_line = float(layer.coverages.loh.written_line or 0)

    if policy_reference == "":
        return

    # Collect tvp data
    tvp_data = []
    loh_rating = hxd.cds.exposure.granular.vessels.loh_rating
    loh_vessels_list = loh_rating.loh_vessels_list
    data_mart_temp_vessels_list = []
    for vessel in loh_vessels_list:
        if vessel.loh_unique_identifier is None:
            continue
        imo = 0
        try:
            if vessel.loh_vessel_details.loh_imo:
                imo = int(
                    vessel.loh_vessel_details.loh_imo
                )  # Attempt to parse the string to an integer
        except (ValueError, TypeError):
            imo = 0

        data_mart_vessel_dict = {
            "loh_imo": vessel.loh_vessel_details.loh_imo,
            "loh_name": vessel.loh_vessel_details.loh_name,
            "loh_vessel_type": vessel.loh_vessel_details.loh_vessel_type,
            "loh_year_built": vessel.loh_vessel_details.loh_year_built,
            "loh_dwt": vessel.loh_vessel_details.loh_dwt,
            "loh_xs_days": vessel.loh_xs_days,
            "loh_sum_insured": vessel.loh_sum_insured,
            "loh_vessel_achieved_rate": vessel.loh_vessel_achieved_rate,
            "loh_policy_reference": policy_reference,
            "loh_written_line": written_line,
            "loh_currency": currency,
            # "loh_is_renewal": is_renewal,
            "loh_expiry_date": expiry_date,
            "loh_inception_date": inception_date,
        }
        # LOH
        row_data_loh = {
            "policy reference": str(policy_reference or ""),
            "vessel": str(vessel.loh_vessel_details.loh_name or ""),
            "value": float(vessel.loh_sum_insured or 0),
            "rate": float((vessel.loh_vessel_achieved_rate or 0) * 100),
            "deductible": float(vessel.loh_xs_days or 0),
            "inception": inception_date,
            "expiry": expiry_date,
            "lr no": 0,
            "orders": 100,
            "Currency": currency,
            "VesselType": str(vessel.loh_vessel_details.loh_vessel_type or "")[-3:]
            or "",
            "DWT": int(vessel.loh_vessel_details.loh_dwt or 0),
            "YOB": int(vessel.loh_vessel_details.loh_year_built or 0),
            "IMONumber": imo,
            "RenewedPolicy": is_renewal,
            "WrittenLine": written_line * 100,
        }

        tvp_data.append(list(row_data_loh.values()))
        data_mart_temp_vessels_list.append(data_mart_vessel_dict)

    push_to_powersearch_db(
        tvp_data,
        hxd.cds.exposure.granular.vessels.loh_rating,
        data_mart_temp_vessels_list,
    )


def push_to_powersearch_db(tvp_data, coverage_rating, data_mart_temp_vessels_list):
    if len(tvp_data) > 0:
        if "dev" in hx.secrets.environment_name.lower():
            host = hx.secrets.Datamart_host_dev
            user = hx.secrets.Datamart_login_dev
            pwd = hx.secrets.Datamart_password_dev
        elif "tst" in hx.secrets.environment_name.lower():
            host = hx.secrets.Datamart_host_uat
            user = hx.secrets.Datamart_login_uat
            pwd = hx.secrets.Datamart_password_uat
        else:
            host = hx.secrets.Datamart_host_prd
            user = hx.secrets.Datamart_login_prd
            pwd = hx.secrets.Datamart_password_prd

        database_name = "Datamart"

        cnxn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER={"
            + host
            + "};DATABASE={"
            + database_name
            + "};UID={"
            + user
            + "};PWD={"
            + pwd
            + "}",
            timeout=60,
        )
        cursor = cnxn.cursor()

        cmd = "exec [dbo].[usp_Vessel_Bulk_Upsert] @marine_tvp=?"
        cursor.execute(cmd, [tvp_data])
        cnxn.commit()
    coverage_rating.data_mart_temp_vessels_list = data_mart_temp_vessels_list


@hx.task
def push_vessels_to_datamart_task(hxd, progress):

    if hxd.non_cds.show_hide_toggles.loh.show_loh_coverage:
        push_loh_vessels_to_datamart(hxd)
        return
    # Extract root and layer-level attributes
    is_renewal = 1 if hxd.cds.standard_fields.is_renewal else 0
    currency = hxd.cds.currencies.source_currency
    layer = hxd.cds.layers[0]
    policy_reference_hull = layer.coverages.hull.section_reference
    policy_reference_iv = layer.coverages.iv.section_reference
    policy_reference_war = layer.coverages.war.section_reference
    written_line_hull = layer.coverages.hull.written_line
    written_line_iv = layer.coverages.iv.written_line.selected
    written_line_war = layer.coverages.war.written_line.selected
    show_iv_coverage = hxd.non_cds.show_hide_toggles.iv.show_iv_coverage
    show_war_coverage = hxd.non_cds.show_hide_toggles.war.show_war_coverage

    # Collect tvp data
    tvp_data = []
    hull_rating = hxd.cds.exposure.granular.vessels.hull_rating
    vessels_list = hull_rating.vessels_list
    data_mart_temp_vessels_list = []
    for vessel in vessels_list:
        if vessel.vessel_details.imo is None:
            continue
        imo = None
        try:
            if vessel.vessel_details.imo:
                imo = int(
                    vessel.vessel_details.imo
                )  # Attempt to parse the string to an integer
        except (ValueError, TypeError):
            # If parsing fails, skip this vessel
            continue
        data_mart_vessel_dict = {
            "imo": vessel.vessel_details.imo,
            "name": vessel.vessel_details.name,
            "vessel_type": vessel.vessel_type,
            "year_built": vessel.year_built,
            "dwt": vessel.dwt,
            "order_percent": vessel.vessel_details.order_percent,
            "inception_date": vessel.inception_date,
            "expiry_date": vessel.expiry_date,
            "deductible": vessel.deductible,
            "agreed_value": vessel.agreed_value,
            "achieved_rate": vessel.achieved_rate,
            "hull_policy_reference": policy_reference_hull,
            "hull_written_line": written_line_hull,
            "currency": currency,
            # "is_renewal": is_renewal,
        }
        # Hull
        row_data_hull = {
            "policy reference": str(policy_reference_hull or ""),
            "vessel": str(vessel.vessel_details.name or ""),
            "value": float(vessel.agreed_value or 0),
            "rate": float((vessel.achieved_rate or 0) * 100),
            "deductible": float(vessel.deductible or 0),
            "inception": vessel.inception_date or date(1900, 1, 1),
            "expiry": vessel.expiry_date or date(1900, 1, 1),
            "lr no": 0,
            "orders": int((vessel.vessel_details.order_percent or 0) * 100),
            "Currency": str(currency or ""),
            "VesselType": str(vessel.vessel_type or "")[-3:] or "",
            "DWT": int(vessel.dwt or 0),
            "YOB": int(vessel.year_built or 0),
            "IMONumber": int(imo or 0),
            "RenewedPolicy": is_renewal,
            "WrittenLine": float(written_line_hull or 0) * 100,
        }
        if policy_reference_hull is not None:
            tvp_data.append(list(row_data_hull.values()))

        # IV
        if (
            show_iv_coverage
            and policy_reference_iv is not None
            and vessel.iv.iv_is_include_vessel
        ):
            row_data_iv = row_data_hull.copy()
            row_data_iv["policy reference"] = str(policy_reference_iv or "")
            row_data_iv["value"] = float(vessel.iv.iv_agreed_value.selected or 0)
            row_data_iv["rate"] = float(vessel.iv.iv_achieved_rate or 0) * 100
            row_data_iv["deductible"] = float(
                vessel.iv.iv_deductible.selected or 0,
            )
            row_data_iv["WrittenLine"] = float(written_line_iv or 0) * 100
            tvp_data.append(list(row_data_iv.values()))
            data_mart_vessel_dict = {
                **data_mart_vessel_dict,
                "iv_agreed_value": vessel.iv.iv_agreed_value.selected,
                "iv_deductible": vessel.iv.iv_deductible.selected,
                "iv_achieved_rate": vessel.iv.iv_achieved_rate,
                "iv_policy_reference": policy_reference_iv,
                "iv_written_line": written_line_iv
            }

        # WAR
        if (
            show_war_coverage
            and policy_reference_war is not None
            and vessel.war.war_is_include_vessel
        ):
            row_data_war = row_data_hull.copy()
            row_data_war["policy reference"] = str(policy_reference_war or "")
            row_data_war["value"] = float(vessel.war.war_agreed_value.selected or 0)
            row_data_war["rate"] = float(vessel.war.war_achieved_rate or 0) * 100
            row_data_war["WrittenLine"] = float(written_line_war or 0) * 100
            row_data_war["deductible"] = None
            tvp_data.append(list(row_data_war.values()))
            data_mart_vessel_dict = {
                **data_mart_vessel_dict,
                "war_agreed_value": vessel.war.war_agreed_value.selected,
                "war_achieved_rate": vessel.war.war_achieved_rate,
                "war_policy_reference": policy_reference_war,
                "war_written_line": written_line_war
            }
        data_mart_temp_vessels_list.append(data_mart_vessel_dict)

    # Execute stored procedure
    if len(tvp_data) > 0:

        if "dev" in hx.secrets.environment_name.lower():
            host = hx.secrets.Datamart_host_dev
            user = hx.secrets.Datamart_login_dev
            pwd = hx.secrets.Datamart_password_dev
        elif "tst" in hx.secrets.environment_name.lower():
            host = hx.secrets.Datamart_host_uat
            user = hx.secrets.Datamart_login_uat
            pwd = hx.secrets.Datamart_password_uat
        else:
            host = hx.secrets.Datamart_host_prd
            user = hx.secrets.Datamart_login_prd
            pwd = hx.secrets.Datamart_password_prd

        database_name = "Datamart"

        cnxn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};SERVER={"
            + host
            + "};DATABASE={"
            + database_name
            + "};UID={"
            + user
            + "};PWD={"
            + pwd
            + "}",
            timeout=60,
        )
        cursor = cnxn.cursor()

        cmd = "exec [dbo].[usp_Vessel_Bulk_Upsert] @marine_tvp=?"
        cursor.execute(cmd, [tvp_data])
        cnxn.commit()
    
    hull_rating.data_mart_temp_vessels_list = copy.deepcopy(data_mart_temp_vessels_list)
