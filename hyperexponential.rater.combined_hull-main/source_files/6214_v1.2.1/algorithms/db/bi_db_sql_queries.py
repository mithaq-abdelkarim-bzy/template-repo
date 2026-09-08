import pyodbc
import pandas as pd
import datetime
import hx


def query_bi_database(query, columns=None):
    # Set up connection details
    print("starting " + str(datetime.datetime.now()))
    print(str(query))

    is_dev = (
        hx.secrets.environment_name == "beazley-dev"
        or hx.secrets.environment_name == "beazley-tst"
    )

    database_name = "BeazleyIntelligenceDataSets"

    host = (
        hx.secrets.beazleyintelligencedatasets_host_uat
        if is_dev
        else hx.secrets.beazleyintelligencedatasets_host_prd
    )

    user = (
        hx.secrets.beazleyintelligencedataSets_login_uat
        if is_dev
        else hx.secrets.beazleyintelligencedataSets_login_prd
    )

    password = (
        hx.secrets.beazleyintelligencedataSets_password_uat
        if is_dev
        else hx.secrets.beazleyintelligencedataSets_password_prd
    )

    cnxn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER={"
        + host
        + "};DATABASE={"
        + database_name
        + "};UID={"
        + user
        + "};PWD={"
        + password
        + "}",
        timeout=30,
    )

    cursor = cnxn.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()

    print("ending " + str(datetime.datetime.now()))
    if columns:
        return pd.DataFrame.from_records(rows, columns=columns)
    else:
        return rows


def get_all_table_schemas():
    query = """
    SELECT TABLE_SCHEMA, TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE IN ('VIEW')
    """
    tables = query_bi_database(query)
    return [(table[0], table[1]) for table in tables]


def get_table_schema(schema_name, table_name):
    query = f"""
    SELECT COLUMN_NAME, DATA_TYPE
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'
    """
    columns = ["COLUMN_NAME", "DATA_TYPE"]
    return query_bi_database(query, columns)


def get_policies_by_class_of_business(
    class_of_business_code="WH",
    stats_code=73,
):
    query = f"""
    SELECT 
        [current].YOA AS YOA,
        [current].WrittenOrEstimatedPremium AS CurrentPremium,
        [expiring].WrittenOrEstimatedPremium AS ExpiringPremium
    FROM 
        Report.SectionCombinedView AS [current]
    LEFT JOIN 
        Report.SectionCombinedView AS [expiring]
    ON 
        [current].ExpiringSection = [expiring].SectionReference
        AND [current].ExpiringPolicy = [expiring].PolicyReference
    WHERE 
        [current].ClassOfBusinessCode = '{class_of_business_code}'
        AND [current].StatsCode = '{stats_code}'
    """
    return query_bi_database(query)


def get_policies_by_policy_references(
    policy_references=[],
    class_of_business_code="WH",
    stats_code=73,
):

    formatted_policy_references = ", ".join(f"'{ref}'" for ref in policy_references)
    query = f"""
    SELECT PolicyReference,WrittenOrEstimatedPremium,TotalIncurred,RateChangeDivisor,ExternalAcquisitionCostMultiplier,InternalAcquisitionCostMultiplier,TotalWrittenIfNotSignedMultiplier,YOA
    FROM Report.SectionCombinedView 
    WHERE ClassOfBusinessCode = '{class_of_business_code}'
    AND StatsCode = '{stats_code}'
    AND PolicyReference IN ({formatted_policy_references})
    """
    return query_bi_database(query)
