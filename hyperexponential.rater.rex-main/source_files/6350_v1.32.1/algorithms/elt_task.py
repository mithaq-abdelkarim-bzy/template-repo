import hx
import pyodbc
from datetime import datetime
import polars as pl
import pandas as pd


def pull_elt_data(hxd, progress):
    portinfoid = hxd.elt_api.inputs.portinfoid
    accgrpid = hxd.elt_api.inputs.accgrpid

    filter_portinfoid = "" if portinfoid else "--"
    filter_accgrpid = "" if accgrpid else "--"
    filter_team = "" if team else "--"

    # Query ELT table
    query = f"""
        SELECT 
            anlsid, 
            Name as name, 
            EventID as event_id, 
            Rate as rate, 
            perspvalue, 
            stddevi, 
            stddevc, 
            expvalue, 
            Peril as peril
        FROM property_data.dbo.vw_elt_policy WITH (NOLOCK)
        WHERE 1=1
        {filter_team}{filter_accgrpid}    AND accgrpid = '{str(team) + ' ' + str(accgrpid)}' 
        {filter_perspcode}    AND perspcode = '{str(perspcode)}'
    """

    elt_db_pl, successful = query_exposure_management_database(hxd, progress, query)

    if successful:
        hxd.elt_api.elt_results = elt_db_pl.to_dicts()


def query_exposure_management_database(hxd, progress, query, status_object):
    # fetch_status = getattr(hxd.elt_api, status_object)
    setattr(hxd.elt_api, status_object, "Fetching from SQL...")# + "\n" + query
    progress.update(0)

    # Connect to server
    # The developer should insert their own credentials here
    user = "hx"
    pwd = "xpecYH3qEQhGHhcbn-LqCMqfC"

    # Set up the connection
    # server=raptor-rater-extract.beazley.hxrenew.com
    # port=1433
    # database=RaptorRaterExtract
    # try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=raptor-rater-extract.beazley.hxrenew.com;DATABASE=property_data;UID=' + user + ';PWD=' + pwd, timeout=30)
    # except pyodbc.Error as err:
    #     # hxd.policy.fetch_status = "Unable to connect to Policy Admin System database"
    #     hxd.policy.fetch_status = err.args[0]
    #     return

    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        setattr(hxd.elt_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query
        return None, False
    else:
        column_names = [column[0] for column in cursor.description]

        pandas_df = pd.DataFrame.from_records(data=rows, columns=column_names)
        # polars_df = pl.from_records(data=[[elem for elem in row] for row in rows], schema=column_names)

        # If the task has not yet returned, the fetch has been successful
        setattr(hxd.elt_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query

    return pandas_df, True
