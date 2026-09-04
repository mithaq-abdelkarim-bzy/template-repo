import hx, pyodbc
import pandas as pd

def bi_policy_fetch(hxd, progress):
    hxd_er = hxd.cds.experience_rating
    pol_ref = hxd.cds.standard_fields.policy_reference
    index_ref = pol_ref[:6] if pol_ref else ""
    query = f"""
        SELECT
            [PolicyReference]
            ,[SectionReference]
            ,[TriFocusName]
            ,[ClassOfBusinessCode]
            ,ISNULL([StatsCode], '') AS [StatsCode]
            ,[YOA]
            ,[SettlementCurrency]
            ,[ExternalAcquisitionCostMultiplier]
            ,[WrittenOrEstimatedPremium]
            ,ISNULL([RateChangeDivisor], 0) AS 'RateChangeDivisor'
            ,[BenchmarkPremium]
            ,[TotalWrittenIfNotSignedMultiplier]
        FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
        WHERE TriFocusName = 'Stand Alone Terrorism'
        AND [WrittenOrEstimatedPremium] IS NOT NULL
        AND [WrittenOrEstimatedPremium] > 0
        AND (([Product] = 'Deadly Weapons Protection' AND Substring(PolicyReference,2,5) = Substring('{index_ref}',2,5))
        OR ([TrifocusName] = ('Stand Alone Terrorism') AND [StatsCode] = 'DW' AND LEFT(PolicyReference,6) = LEFT('{index_ref}',6)))
        AND [YOA] > 2015
        ORDER BY [InceptionDate]
    """ 
    columns = [
        "PolicyReference",
        "SectionReference",
        "TriFocusName",
        "ClassOfBusinessCode",
        "StatsCode",
        "YOA",
        "SettlementCurrency",
        "ExternalAcquisitionCostMultiplier",
        "WrittenOrEstimatedPremium",
        "RateChangeDivisor", 
        "BenchmarkPremium",
        "TotalWrittenIfNotSignedMultiplier"
    ]
    
    policy_data = pd.DataFrame(query_beazley_intelligence_database(query, columns))
    
    if policy_data.shape[0] == 0:
        hxd.messages.fetch_bi_task_status = "Policy information not found for selected reference"
    else:
        hxd.messages.fetch_bi_task_status = "✅ Policy data successfully retrieved."
        hxd_er.bi_policy_data = policy_data.to_dict(orient="records")
    pass


def bi_claim_fetch(hxd, progress):
    hxd_er = hxd.cds.experience_rating
    pol_ref = hxd.cds.standard_fields.policy_reference
    index_ref = pol_ref[:6] if pol_ref else ""
    query = f"""
        SELECT
            [PolicyReference]
            ,[SectionReference]
            ,[TriFocusName]
            ,[PolicyYOA] as [YOA]
            ,[ClaimReference]
            ,ISNULL([MarketCatCode], '') AS [MarketCatCode] 
            ,[BeazleyShareTotalPaidInUSD]
            ,[BeazleyShareTotalOutstandingInUSD]
            ,[BeazleyShareTotalIncurredInUSD]
            ,[SettlementCurrency]
            ,[SlipOrderTotalIncurred]
            ,[SignedLineMultiplier]
        FROM [BeazleyIntelligenceDataSets].[Report].[ClaimExposureSectionCombinedView]
        WHERE (([Product] = 'Deadly Weapons Protection' AND Substring(PolicyReference,2,5) = Substring('{index_ref}',2,5))
        OR ([TrifocusName] = ('Stand Alone Terrorism') AND LEFT(PolicyReference,6) = LEFT('{index_ref}',6)))
        AND LEFT([PolicyReference],6) = '{index_ref}'
        ORDER BY [PolicyYOA]
    """
    columns = [
        "PolicyReference",
        "SectionReference",
        "TriFocusName",
        "YOA",
        "ClaimReference",
        "MarketCatCode",
        "BeazleyShareTotalPaidInUSD",
        "BeazleyShareTotalOutstandingInUSD",
        "BeazleyShareTotalIncurredInUSD",
        "SettlementCurrency",
        "SlipOrderTotalIncurred",
        "SignedLineMultiplier"
    ]

    claim_data = pd.DataFrame(query_beazley_intelligence_database(query, columns))

    if claim_data.shape[0] > 0:
        hxd_er.bi_claim_data = claim_data.to_dict(orient="records")     
    pass


def query_beazley_intelligence_database(query, columns):
    
    database_name = "BeazleyIntelligenceDataSets"
    
    # Set up connection details
    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower():
        host = hx.secrets.beazleyintelligencedatasets_host_uat
        user = hx.secrets.beazleyintelligencedataSets_login_uat
        password = hx.secrets.beazleyintelligencedataSets_password_uat
    else:
        host = hx.secrets.beazleyintelligencedatasets_host_prd
        user = hx.secrets.beazleyintelligencedataSets_login_prd
        password = hx.secrets.beazleyintelligencedataSets_password_prd

    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows