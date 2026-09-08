import os
import sqlite3
import pandas as pd
import hx
import pyodbc

import re

vessels_table_schema = [
    "imo",
    "NumberOfportVisits",
    "NumberOfUniquePortVisits",
    "ModelAge",
    "ModelShipName",
    "ModelAthsAntarctica",
    "ModelAthsAustraliaAndNewZealand",
    "ModelAthsEasternAsia",
    "ModelAthsEasternEurope",
    "ModelAthsHighSeas",
    "ModelAthsLatinAmericaAndCaribbean",
    "ModelAthsMelanesia",
    "ModelAthsMicronesia",
    "ModelAthsNorthernAfrica",
    "ModelAthsNorthernAmerica",
    "ModelAthsNorthernEurope",
    "ModelAthsPolynesia",
    "ModelAthsSouthEasternAsia",
    "ModelAthsSouthernAsia",
    "ModelAthsSouthernEurope",
    "ModelAthsSubSaharanAfrica",
    "ModelAthsWesternAsia",
    "ModelAthsWesternEurope",
    "ModelChangeInFleet",
    "ModelClassChanges5yr",
    "ModelDWT",
    "ModelFlag",
    "ModelGrossTonnage",
    "ModelMaxDistanceRatio",
    "ModelNetSumInsured",
    "ModelNumJourneysCut",
    "ModelNumPortVisitsCut",
    "ModelPercTimeEEZ",
    "ModelPercTimeHRZ",
    "ModelPercTimeSECA",
    "Modelpowerkwmax",
    "ModelRatioAnchored",
    "ModelRatioMoored",
    "ModelRatioMoving",
    "ModelTotalUniqueIMOsOwnerBins",
    "ModelUniqueJourneyRatio",
    "ModelUniquePortRatio",
    "ModelShipType",
    "ModelMappedFlag",
    "ModelRawDWT",
    "ModelYearOfBuild",
    "ModelRawGrossTonnage",
    "ModelGranularShipType",
]

replacements = {
    r"Model": "",
    r"NumberOfportVisits": "number_of_port_visits",
    r"Aths": "is_aths",
    r"ShipName": "name",
    r"GranularShipType": "vessel_type",
    r"ClassChanges5yr": "is_class_changes_5yr",
    r"MappedFlag": "flag",
    r"Flag": "model_flag",
    r"TotalUniqueIMOsOwnerBins": "total_unique_imos_owner",
    r"YearOfBuild": "year_built",
    r"RawGrossTonnage": "gross_tonnage",
    r"GrossTonnage": "model_gross_tonnage",
    r"RawDWT": "dwt",
    r"DWT": "model_dwt",
    r"ShipType": "ship_type",
}


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


def multiple_replace(text, replacements):
    pattern = re.compile("|".join(re.escape(key) for key in replacements.keys()))
    return pattern.sub(lambda m: replacements.get(m.group(0), m.group(0)), text)


def get_vessels_by_imo(imos):
    query_columns = ", ".join(vessels_table_schema)
    # Create a query to fetch vessels by IMO
    query = f"SELECT {query_columns} FROM [Marine].[dbo].[USP_MODEL_TABLE] WHERE imo IN ({', '.join(str(imo) for imo in imos)})"
    if "dev" in hx.secrets.environment_name.lower():
        host = hx.secrets.marine_host_dev
        user = hx.secrets.marine_login_dev
        pwd = hx.secrets.marine_password_dev
    elif "tst" in hx.secrets.environment_name.lower():
        host = hx.secrets.marine_host_tst
        user = hx.secrets.marine_login_tst
        pwd = hx.secrets.marine_password_tst
    else:
        host = hx.secrets.marine_host_prd
        user = hx.secrets.marine_login_prd
        pwd = hx.secrets.marine_password_prd

    # Create connection
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=" + host + ";"
        "UID=" + user + ";"
        "PWD=" + pwd,
        timeout=30,
    )

    # Run a new query and close connection
    result_df = pd.read_sql_query(query, conn)
    conn.close()
    schema_dict = {}
    # Rename columns to match the schema, removing "Model" prefix and converting to snake case (e.g. ModelFlag -> flag)
    for column in vessels_table_schema:
        new_name = multiple_replace(column, replacements)
        new_name_snake_case = camel_to_snake(new_name)

        # Check if the new snake case name starts with 'is_'
        if new_name_snake_case.startswith("is_"):
            # Convert the column values from 0/1 to True/False
            result_df[column] = result_df[column].apply(
                lambda x: bool(int(x)) if str(x).isdigit() else x.lower() == "true"
            )

        # elif new_name_snake_case.startswith("perc_"):
        #     # Divide the column values by 100 to convert them to Float percentages
        #     result_df[column] = result_df[column] / 100

        schema_dict[column] = new_name_snake_case

    result_df.rename(columns=schema_dict, inplace=True)

    if not result_df.empty:
        column_mapping = {
            "name": "model_ship_name",
            "vessel_type": "raw_ship_type",
            "flag": "current_flag",
            "year_built": "year_of_build",
            "gross_tonnage": "raw_grosstonnage",
            "dwt": "raw_deadweight",
        }

        for original, copy in column_mapping.items():
            if original in result_df.columns:
                result_df[copy] = result_df[original]

    return result_df
