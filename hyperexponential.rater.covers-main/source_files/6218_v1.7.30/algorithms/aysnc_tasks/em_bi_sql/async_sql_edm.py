##############################
######### TO DO #############
### add facility lookup on this data to RMS tab and have it default to facility where exact match
###########################################################


import hx, pyodbc
import pandas as pd


#############################################################################################################################
### BEGIN EDM Fetch - pull EDM data from SQL database and write to edm & edm_reference_lookup list nodes ###################
#############################################################################################################################

def edm_fetch(hxd,progress):
    cds = hxd.cds
    facility_reference = cds.standard_fields.facility_reference
    index_ref = facility_reference[:6] + facility_reference[8:12]
    #index_ref = facility_reference[:6]
    #index_ref = "B7134z"

    #edm_ref = cds.rms.edm_reference_selected

    # Query
    query1 = f"""
        SELECT DISTINCT [PORTNUM] as 'portnum' 
        FROM [Property_data].[dbo].[vw_covers_rater_EPcurve]
        WHERE SUBSTRING([PortNum],1,6) + SUBSTRING([PortNum],9,4) LIKE '{index_ref}' 
    """
    columns1 = ['portnum']

    




    query2 = f"""
        SELECT DISTINCT
            isnull(a.[Return Period],0)		as 'return_period'
            ,a.[Probability]					as 'probability'	
            ,a.[PortNum]						as 'portnum'
            ,isnull(b.[100% contract AEP],0)	as 'ws_loss_amount'
            ,isnull(b.[Premium],0)				as 'ws_premium'
            ,isnull(b.[Premium_currency],'')	as 'ws_currency'
            ,isnull(b.[Premium_fx],0)			as 'ws_fxrate'
            ,isnull(c.[100% contract AEP],0)	as 'eq_loss_amount'
            ,isnull(c.[Premium],0)				as 'eq_premium' 
            ,isnull(c.[Premium_currency],'')	as 'eq_currency'
            ,isnull(c.[Premium_fx],0)			as 'eq_fxrate'

        FROM [Property_data].[dbo].[vw_covers_rater_EPcurve] a
            LEFT JOIN  (SELECT * FROM [Property_data].[dbo].[vw_covers_rater_EPcurve] WHERE [Peril] = 'WS') b
                    ON b.[Return Period] = a.[Return Period] and b.[PortNum]=a.[PortNum]
            LEFT JOIN (SELECT * FROM [Property_data].[dbo].[vw_covers_rater_EPcurve] WHERE [Peril] = 'EQ') c
                    ON c.[Return Period] = a.[Return Period] and c.[PortNum]=a.[PortNum]
        WHERE SUBSTRING(a.[PortNum],1,6) + SUBSTRING(a.[PortNum],9,4) LIKE '{index_ref}' 
        ORDER BY a.[PortNum], a.[Probability]
    """

    columns2 = ['return_period'
                ,'probability'	
                ,'portnum'
                ,'ws_loss_amount'
                ,'ws_premium'
                ,'ws_currency'
                ,'ws_fxrate'
                ,'eq_loss_amount'
                ,'eq_premium' 
                ,'eq_currency'
                ,'eq_fxrate'
    ]
    




    #Total Premium of policy
    query3 = f"""
    SELECT SUM([AFB Account Premium]/[SignedLine Value used for calc]) AS bordereaux_total_prem
    FROM (
    SELECT DISTINCT accgrpnum, [AFB Account Premium],[SignedLine Value used for calc], [PortNum]
    FROM [Property_data].[dbo].[vw_covers_rater_data]
    WHERE SUBSTRING([PortNum],1,6) + SUBSTRING([PortNum],9,4) LIKE '{index_ref}'
    ) AS distinct_data
;
    """

    columns3 = ['bordereaux_total_prem']

    


    # pull edm portnum from sql based on query 1
    edm_data_reference_lookup  = query_edm_database(query1, columns1) 
    if edm_data_reference_lookup.shape[0] < 1:
        # do nothing
        cds.rms.fetch_edm_data_reference_lookup_task_status = "EDM Information not found for selected Reference"
    else:
        setattr(cds.rms,"edm_reference_lookup", edm_data_reference_lookup.to_dict("records"))
        cds.rms.fetch_edm_data_reference_lookup_task_status = "EDM Information successfully retrieved"



    # pull EDM data from sql based on query 2
    edm_data                = query_edm_database(query2, columns2) 
    if edm_data.shape[0] < 1:
        # do nothing
        cds.rms.fetch_edm_data_task_status = "EDM Information not found for selected Reference"
    else:
        setattr(cds.rms,"edm",edm_data.to_dict("records"))
        cds.rms.fetch_edm_data_task_status = "EDM Information successfully retrieved"


    # pull EDM data from sql based on query 3
    edm_prem = query_edm_database(query3, columns3) 
    if edm_prem.shape[0] < 1:
        # do nothing
        cds.rms.fetch_edm_prem_data_task_status = "EDM Information not found for selected Reference"
    else:
        setattr(cds.rms,"edm_prem",edm_prem.to_dict("records"))
        cds.rms.fetch_edm_prem_data_task_status = "EDM Prem Information successfully retrieved"
    
    pass

#############################################################################################################################
### END EDM Fetch - pull EDM data from SQL database and write to edm & edm_reference_lookup list nodes
#############################################################################################################################




#############################################################################################################################
### BEGIN QUERY EDM Database -
#############################################################################################################################
# similar query for BI arguably could be combined but would require lots of parameters passed...

def query_edm_database(query, columns):
    # Set up connection details

    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower(): 
        host = hx.secrets.exposuremanagement_host_uat
        user = hx.secrets.exposuremanagement_login_uat
        password = hx.secrets.exposuremanagement_password_uat
    else:
        host = hx.secrets.exposuremanagement_host_prd
        user = hx.secrets.exposuremanagement_login_prd
        password = hx.secrets.exposuremanagement_password_prd

    database_name = "Property_data"
    
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE={' + database_name + '};UID={' + user + '};PWD={' + password + '}', timeout=30)

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    return pd.DataFrame.from_records(rows, columns=columns)
    # return rows

#############################################################################################################################
### END QUERY EDM Database -
#############################################################################################################################
