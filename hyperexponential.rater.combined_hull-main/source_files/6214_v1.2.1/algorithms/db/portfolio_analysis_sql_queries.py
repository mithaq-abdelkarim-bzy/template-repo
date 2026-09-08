import os
import sqlite3
import pandas as pd


def portfolio_analysis_query_builder(filter_options):
    query = """
    SELECT a.[ApplicationID], b.[IMO], a.[FirmName], b.[VesselsTablePolicyReference],
    strftime('%Y-%m-%d', substr(b.[InceptionDate], 7, 4) || '-' || substr(b.[InceptionDate], 4, 2) || '-' || substr(b.[InceptionDate], 1, 2)) AS InceptionDate,
    strftime('%Y-%m-%d', substr(b.[ExpiryDate], 7, 4) || '-' || substr(b.[ExpiryDate], 4, 2) || '-' || substr(b.[ExpiryDate], 1, 2)) AS ExpiryDate, 
    b.[Coverage], b.[AgreedValue],
    c.[Value] AS Currency, NULL AS AgreedValCurr, b.[Type], b.[GrossTonnage], b.[DWT], b.[YearBuilt],
    b.[Flag], b.[Class], b.[AchievedRate], b.OrderPercentage, b.VesselsTableWrittenLine,
    d.[Value] AS Domicile, a.[Broker], b.[VesselsTableLeadFollow] AS FollowLead, b.[name],
    substr(b.[Type], -3) AS [Type Abrv]
    FROM Application a
    INNER JOIN Vessel b ON a.[ApplicationID] = b.[ApplicationID] AND b.[IncludeVessel] = 1
    LEFT JOIN RaterKVData c ON a.[ApplicationID] = c.[ApplicationID] AND c.[Key] = 'RiskInfo.CCY'
    LEFT JOIN RaterKVData d ON a.[ApplicationID] = d.[ApplicationID] AND d.[Key] = 'Vessels.OperatorDomicile'
    WHERE a.RaterIndicator = 'MarineHull_Rater'
"""

    conditions = {
        "date(replace(b.[InceptionDate], '/', '-')) >= ?": filter_options.get(
            "effective_date_from"
        ),
        "date(replace(b.[ExpiryDate], '/', '-')) <= ?": filter_options.get(
            "effective_date_to"
        ),
        "a.FirmName LIKE ?": (
            f"%{filter_options.get('insured_name')}%"
            if filter_options.get("insured_name")
            else None
        ),
        "a.Broker LIKE ?": (
            f"%filter_options.get('broker')" if filter_options.get("broker") else None
        ),
        "d.Value = ?": filter_options.get("operator_domicile"),
        "b.VesselsTableLeadFollow = ?": filter_options.get("follow_lead"),
        "b.IMO LIKE ?": (
            f"%{filter_options.get('imo')}%" if filter_options.get("imo") else None
        ),
        "b.Coverage = ?": filter_options.get("coverage"),
        "b.Type = ?": filter_options.get("vessel_type"),
        "b.Flag = ?": filter_options.get("flag"),
        "b.Class = ?": filter_options.get("vessel_class"),
        "b.AgreedValue >= ?": filter_options.get("agreed_value_from"),
        "b.AgreedValue <= ?": filter_options.get("agreed_value_to"),
        "b.GrossTonnage >= ?": filter_options.get("gross_tonnage_from"),
        "b.GrossTonnage <= ?": filter_options.get("gross_tonnage_to"),
        "b.DWT >= ?": filter_options.get("dwt_from"),
        "b.DWT <= ?": filter_options.get("dwt_to"),
        "b.YearBuilt >= ?": filter_options.get("year_built_from"),
        "b.YearBuilt <= ?": filter_options.get("year_built_to"),
        "b.ExpiryDate >= ?": filter_options.get("live_risk_entry"),
        "b.VesselsTablePolicyReference = ?": filter_options.get("policy_reference"),
        "a.DealStatus = ?": filter_options.get("status"),
    }

    column_mapping = {
        "ApplicationID": "id",
        "IMO": "imo",
        "FirmName": "insured",
        "VesselsTablePolicyReference": "policy_reference",
        "InceptionDate": "effective_date",
        "ExpiryDate": "expiry_date",
        "Coverage": "coverage",
        "AgreedValue": "original_agreed_value",
        "Currency": "original_currency",
        "Type": "vessel_type",
        "GrossTonnage": "gross_tonnage",
        "DWT": "dwt",
        "YearBuilt": "year_built",
        "Flag": "flag",
        "Class": "classification",
        "AchievedRate": "achieved_rate",
        "OrderPercentage": "order_percent",
        "VesselsTableWrittenLine": "written_line_percent",
        "Domicile": "operator_domicile",
        "Broker": "broker",
        "FollowLead": "follow_lead",
        "Name": "vessel_name",
        "Type Abrv": "type_abrv",
    }

    params = []
    for condition, value in conditions.items():
        if value is not None:
            query += f" AND {condition}"
            params.append(value)

    if filter_options.get("has_policy_reference") is not None:
        if filter_options.get("has_policy_reference"):
            query += "AND b.VesselsTablePolicyReference IS NOT NULL"
        else:
            query += "AND b.VesselsTablePolicyReference IS NULL"

    db_file_path = os.path.join(os.path.dirname(__file__), "portfolio_analysis.db")
    conn = sqlite3.connect(f"file:{db_file_path}?mode=ro", uri=True)

    # Run a new query and close connection
    result_df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    result_df.rename(columns=column_mapping, inplace=True)
    return result_df
