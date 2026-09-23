import hx, pyodbc
import pandas as pd


def bi_intelligence_fetch(hxd):
    cds = hxd.cds
    policy_reference = cds.standard_fields.policy_reference
    index_ref = policy_reference[:6] + policy_reference[8:]
    # index_ref = "JJX48CANYJ"
    threshold = cds.experience_detailed.ll_threshold
    # Query
    query1 = f"""
        SELECT 
            [PolicyReference],
            [SectionReference],
            [YOA],
            [CoverageName],
            [TriFocusName],
            [Division],
            (CASE WHEN [RateChangeDivisor] IS NULL THEN 1 Else RateChangeDivisor end) as 'RateChangeDivisor',
            [SettlementCurrency],
            ISNULL([WrittenOrEstimatedPremium],0) AS WrittenOrEstimatPrem,
            (CASE WHEN [TotalIncurred] IS NULL THEN 0 ELSE TotalIncurred end) as 'TotalIncurred', 
            'RateChangeReformat' = CASE 
                WHEN [RateChangeDivisor] IS NULL THEN 1 
                WHEN [RateChangeDivisor] < 10 THEN [RateChangeDivisor] 
                ELSE 10 END,
            (CASE 
                WHEN [RateChangeDivisor] IS NULL THEN 1 
                WHEN [RateChangeDivisor] < 10 THEN [RateChangeDivisor] 
                ELSE 10 END * 
                    ISNULL([WrittenOrEstimatedPremium],0)) AS WEPOnLevel,
            CONCAT(LEFT([PolicyReference],6),RIGHT([SectionReference],4)) AS 'Index',
            [TotalWrittenIfNotSignedMultiplier], 
            ([WrittenOrEstimatedPremium]/[TotalWrittenIfNotSignedMultiplier]) AS 'TotalWEP' 
        FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView] 
        WHERE 
            TrifocusName IN ('Jewellers', 'Fine Art and Specie') 
            AND CONCAT(LEFT([PolicyReference],6),RIGHT([SectionReference],4)) LIKE '{index_ref}' 
        ORDER BY [InceptionDate]
    """

    columns1 = [
        "PolicyReference",
        "SectionReference",
        "YOA",
        "CoverageName",
        "TriFocusName",
        "Division",
        "RateChangeDivisor",
        "SettlementCurrency",
        "WrittenOrEstimatPrem",
        "TotalIncurred", 
        "RateChangeReformat",
        "WEPOnLevel",
        "Index",
        "TotalWrittenIfNotSignedMultiplier", 
        "TotalWEP"
    ]

    query2 = f"""
        SELECT 
            [SectionReference],
            [ClaimReference],
            [TriFocusName],
            [Division],
            [PolicyYOA],
            [PolicyReference],
            [BeazleyCatCode],
            [BeazleyCat],
            [MarketCatCode],
            (CASE WHEN [MarketCat] IS NULL THEN '' ELSE MarketCat end) as 'MarketCat' ,
            [HasBeazleyCatCode],
            [BeazleyShareTotalIncurredInUSD],
            [BeazleyShareTotalOutstandingInUSD],
            [CauseOfLoss],
            'Large Loss Indicator' = CASE 
                WHEN [HasBeazleyCatCode]=0 AND [BeazleyShareTotalIncurredInUSD] > {threshold} THEN 1 
                ELSE 0 END,
            CONCAT(LEFT([SectionReference],6),RIGHT([SectionReference],4)) AS 'Index',
            [SignedLineMultiplier],
            ([BeazleyShareTotalIncurredInUSD]/[SignedLineMultiplier]) AS 'TotalIncurredInUSD' 
        FROM [BeazleyIntelligenceDataSets].[Report].[ClaimExposureSectionCombinedView] 
        WHERE 
            TrifocusName IN ('Jewellers', 'Fine Art and Specie') 
            AND CONCAT(LEFT([PolicyReference],6),RIGHT([SectionReference],4)) LIKE '{index_ref}' 
        ORDER BY [InceptionDate]
    """

    columns2 = [
        "SectionReference",
        "ClaimReference",
        "TriFocusName",
        "Division",
        "PolicyYOA",
        "PolicyReference",
        "BeazleyCatCode",
        "BeazleyCat",
        "MarketCatCode",
        "MarketCat",
        "HasBeazleyCatCode",
        "BeazleyShareTotalIncurredInUSD",
        "BeazleyShareTotalOutstandingInUSD",
        "CauseOfLoss",
        "LargeLossIndicator",
        "Index",
        "SignedLineMultiplier",
        "TotalIncurredInUSD" 
    ]
    
    # cds.bi_policy_data = query_beazley_intelligence_database(query1, columns1) 
    # cds.bi_claims_data = query_beazley_intelligence_database(query2, columns2) 


    policy_data = query_beazley_intelligence_database(hxd, query1, columns1) 
    claims_data = query_beazley_intelligence_database(hxd, query2, columns2) 

    if policy_data.shape[0] < 1:
        # do nothing
        cds.fetch_bi_task_status_policy = "Policy Information not found for selected Reference"
    else:
        setattr(cds,"bi_policy_data",policy_data.to_dict("records"))
        cds.fetch_bi_task_status_policy = "Policy Data successfully retrieved"

    if claims_data.shape[0] < 1:
        # do nothing
        cds.fetch_bi_task_status_claims = "Claims Information not found for selected Reference"
    else:
        setattr(cds,"bi_claims_data",claims_data.to_dict("records"))

        cds.fetch_bi_task_status_claims = "Claims Data successfully retrieved"

    pass


def query_beazley_intelligence_database(hxd, query, columns):
    # Set up connection details
    # if hxd.uat_prod_indicator == "uat":
    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower(): 
        host = hx.secrets.beazleyintelligencedatasets_host_uat
        database_name = "BeazleyIntelligenceDataSets"
        user = hx.secrets.beazleyintelligencedataSets_login_uat
        password = hx.secrets.beazleyintelligencedataSets_password_uat
    else:
        host = hx.secrets.beazleyintelligencedatasets_host_prd
        database_name = "BeazleyIntelligenceDataSets"
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