import hx
import pyodbc
from datetime import date
import polars as pl
import pandas as pd


def search_exposure_management_data(hxd, progress):
    accgrpid = hxd.exposure_management_api.inputs.accgrpid
    reference = hxd.exposure_management_api.inputs.reference
    team = hxd.exposure_management_api.inputs.team
    perspcode = hxd.exposure_management_api.inputs.perspcode
    account_name = hxd.exposure_management_api.inputs.account_name

    filter_accgrpid = "" if accgrpid else "--"
    filter_reference = "" if reference else "--"
    filter_team = "" if team else "--"
    filter_perspcode = "" if perspcode else "--"
    filter_account_name = "" if account_name else "--"

    # Query location table first
    query = f"""
        SELECT DISTINCT
            accgrpid,
            Reference,
            "Account Number",
            "Account Name",
            lastEdit,
            COUNT(*) AS num_locs
        FROM property_data.dbo.vw_location_policy vlp WITH (NOLOCK)
            WHERE 1=1
            {filter_account_name}  AND "Account Name" LIKE '%{str(account_name).replace("'","''")}%'
            {filter_accgrpid}   AND accgrpid LIKE '%{str(accgrpid).replace("'","''")}%'
            -- {filter_team}{filter_accgrpid}  AND accgrpid = '{str(team) + ' ' + str(accgrpid)}'
            {filter_reference}  AND reference = '{str(reference).replace("'","''")}'
        GROUP BY
            accgrpid,
            Reference,
            "Account Number",
            "Account Name",
            lastEdit
    """

    search_db_pl, successful = query_exposure_management_database(hxd, progress, query, "search_fetch_status", limit=hxd.exposure_management_api.limit_results)
    
    if successful:
        hxd.exposure_management_api.search_results = search_db_pl.rename({
            "Reference": "reference",
            "Account Number": "account_number",
            "Account Name": "account_name",
            "lastEdit": "last_edit",
        })[[
                "accgrpid",
                "reference",
                "account_number",
                "account_name",
                "last_edit",
                "num_locs"
            ]].to_dicts()

    # # Now query ELT table
    # query = f"""
    #     SELECT 
    #         anlsid, 
    #         Name, 
    #         EventID, 
    #         Rate, 
    #         perspvalue, 
    #         stddevi, 
    #         stddevc, 
    #         expvalue, 
    #         Peril,
    #         ROW_NUMBER() OVER (ORDER BY EventID) AS RowNumber
    #     FROM property_data.dbo.vw_elt_policy WITH (NOLOCK)
    #     WHERE 1=1
    #     {filter_team}{filter_accgrpid}    AND accgrpid = '{str(team) + ' ' + str(accgrpid)}' 
    #     {filter_perspcode}    AND perspcode = '{str(perspcode)}'
    # """

    # # elt_db_pl = query_exposure_management_database(hxd, progress, query)




def pull_in_exposure_management_data(hxd, progress):

    rows_selected = 0
    
    search_results_df = hxd.exposure_management_api.search_results

    for index, account in enumerate(search_results_df, start=1):
        if not account.selected:
        # if False:
            continue
        else:
            rows_selected += 1

            accgrpid = account.accgrpid
            reference = account.reference
            account_number = account.account_number
            account_name = account.account_name


    if rows_selected == 0:
        hxd.exposure_management_api.location_fetch_status = "No policies selected"
    elif rows_selected > 1:
        hxd.exposure_management_api.location_fetch_status = "Multiple policies selected. Please select only one policy"
    else:
        accgrpid_str = f"= '{str(accgrpid)}'" if accgrpid else "IS NULL"
        reference_str = f"""= '{str(reference).replace("'","''")}'""" if reference else "IS NULL"
        account_number_str = f"""= '{str(account_number).replace("'","''")}'""" if account_number else "IS NULL"
        account_name_str = f"""= '{str(account_name).replace("'","''")}'""" if account_name else "IS NULL"

        query = f"""
            SELECT
                *
            FROM property_data.dbo.vw_location_policy vlp WITH (NOLOCK)
            WHERE 1=1
                AND accgrpid {accgrpid_str}
                AND reference {reference_str}
                AND "Account Number" {account_number_str}
                AND "Account Name" {account_name_str}
        """

        location_db_pl, successful = query_exposure_management_database(hxd, progress, query, "location_fetch_status")

        if successful:

            hxd.policy_information.accgrpid = accgrpid
            hxd.policy_information.account_group_name = account_name
            location_db_pl = map_columns(location_db_pl)


            location_db_pl_dicts = location_db_pl.drop(["tiv_total"])  # We recalculate this

            location_dicts = location_db_pl_dicts.to_dicts()

            structured_location_dicts = []
            for ld in location_dicts:
                ld["address_dropdown"] = {"city": ld['address_dropdown/city'], "county": ld['address_dropdown/county'], "state": ld['address_dropdown/state'], "country": ld['address_dropdown/country']}
                ld["industry_occupancy_dropdown"] = {"industry": ld['industry_occupancy_dropdown/industry'], "occupancy": ld['industry_occupancy_dropdown/occupancy']}
                structured_location_dicts.append({key: ld[key] for key in ld if (('address_dropdown/' not in key) and ('industry_occupancy_dropdown/' not in key))})

            if hxd.policy_information.large_schedule_model:
                
                none_list = ['year_cov_last_replaced', 'ws_tier', 'wf_tier', 'ws_gate', 'eq_gate', 'cresta_zone', 'other_floodzone', 'katrisk_score_fl', 
                                'catnet_score_wf', 'riskmeter_score_wf', 'catnet_score_tn', 'catnet_score_ha', 'catnet_score_fl', 'catnet_score_eq', 
                                'catnet_score_ws', 'risk_level_eq', 'risk_level_ws', 'risk_level_fl', 'risk_level_scs', 'risk_level_wf']

                location_db_pl = location_db_pl.with_columns([
                    pl.lit(None).alias("fire_deductible"),
                    pl.lit(0).alias("tiv_other"),
                    *[pl.lit(None).alias(name) for name in none_list]
                ])

                with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
                    location_db_pl.write_csv(f)
            else:
                hxd.schedule.schedule_table = structured_location_dicts
            
            hxd.schedule.large_schedule_workflow.load_from_em_database = True
            hxd.schedule.large_schedule_workflow.num_of_locations = len(location_db_pl)


def query_exposure_management_database(hxd, progress, query, status_object=None, use_pandas=False, limit=None):
    # fetch_status = getattr(hxd.exposure_management_api, status_object)
    if status_object:
        setattr(hxd.exposure_management_api, status_object, "Fetching from SQL...")# + "\n" + query
    progress.update(0)

    # Connect to server
    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower():
        host = hx.secrets.exposuremanagement_host_uat
        user = hx.secrets.exposuremanagement_login_uat
        pwd = hx.secrets.exposuremanagement_password_uat
    else:
        host = hx.secrets.exposuremanagement_host_prd
        user = hx.secrets.exposuremanagement_login_prd
        pwd = hx.secrets.exposuremanagement_password_prd

    # Set up the connection
    # server=raptor-rater-extract.beazley.hxrenew.com
    # port=1433
    # database=RaptorRaterExtract
    # try:
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE=Property_data;UID=' + user + ';PWD=' + pwd, timeout=30)
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
        if status_object:
            setattr(hxd.exposure_management_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query
        return None, False
    else:
        column_names = [column[0] for column in cursor.description]

        if use_pandas:
            df = pd.DataFrame.from_records(data=rows, columns=column_names)
        else:
            df = pl.from_records(data=[[elem for elem in row] for row in rows], schema=column_names, infer_schema_length=None)

        if limit:
            df = df.head(limit)

        # If the task has not yet returned, the fetch has been successful
        if status_object:
            setattr(hxd.exposure_management_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query

    return df, True


def map_columns(df):
    df = df.rename(schedule_column_map())
    df = set_static_columns(df)
    df = adjust_columns(df)
    df = set_lookup_columns(df)
    df = df.drop(extra_columns())
    df = remap_dict(df)
    return df

def extra_columns():
    return [
        "structup", 
        "Account Number", 
        "fr", 
        "cladding", 
        "id_account", 
        "Reference", 
        "cladrate", 
        "accgrpid", 
        "buildingelevation",  
        "masintpart", 
        "wallsbracd", 
        "portinfoid", 
        "bldgscheme",
        "Occupancy Code", 
        "occtype", 
        "sitededamt_fl", 
        "occscheme", 
        "floodprot", 
        "sitededcur_ws", 
        "fl", 
        "lastEdit", 
        "sitededamt_cs_wt", 
        "deductamt_ws", 
        "urmprov", 
        "sitededcur_eq", 
        "cs_wt", 
        "wc", 
        "Landslide", 
        "Account Name", 
        "bldgclass", 
        "resistopen", 
        "locNum", 
        "tr", 
        "extorn", 
        "resistdoor", 
        "sitededcur_fl", 
        "shortcol", 
        "architect", 
        "windmissl", 
        "roofmaint", 
        "sitededamt_ws",  
        "eq", 
        "roofparapt", 
        "deductamt_scs", 
        "LANDMATCH", 
        "tiltupret", 
        "eqslsusceptibility", 
        "deductamt_eq", 
        "framebolt",
        "SOILMATCH", 
        "ws", 
        "spnklrtype", 
        "eqslins", 
        "floodmissl", 
        "mechground", 
        "broker_occupancy", 
        "policyid_ws", 
        "LIQUEMATCH",
        "BFE", 
        "sitededcur_cs_wt", 
        "engfound", 
        "mechside", 
        "policyid_eq", 
        "urmchimney", 
        "deductamt_fl", 
        "Liquefaction", 
        "Soil",
        "baseisol", 
        "sitededamt_eq", 
        "createDate", 
        "roofframe"
        ]

def adjust_columns(df):
    return df.with_columns(
        pl.col('year_built').dt.year().alias('year_built'),
        pl.col('year_updated').dt.year().alias('year_updated'),
        pl.col('floodzone').cast(pl.Utf8).str.strip().alias('floodzone')
    )

def set_static_columns(df):
    return df.with_columns(
        pl.lit("From Layer").alias("fire_covered"),
        pl.lit("From Layer").alias("eq_covered"),
        pl.lit("From Layer").alias("ws_covered"),
        pl.lit("From Layer").alias("fl_covered"),
        pl.lit("From Layer").alias("scs_covered"),
        pl.lit("From Layer").alias("wf_covered"),
    )

def schedule_column_map():
    return {
        "locid": "loc_id",
        "locname": "property_description",
        "Street": "street_name",
        "StateCode": "address_dropdown/state",
        "County": "address_dropdown/county",
        "City": "address_dropdown/city",
        "Zip": "zip",
        "Construction Narrative": "constr_description",
        "Year Built": "year_built",
        "Buildings": "tiv_buildings",
        "Contents": "tiv_contents",
        # "Other": "tiv_other",  # TODO: check this is ok to be commented out
        "BI": "tiv_bi",
        "TIV": "tiv_total",
        "Occupancy Narrative": "rms_occupancy",
        "Protection Class": "pc_code",
        "Floor Area": "floor_area",
        "Number of Floors": "num_stories",
        "basement": "basement",
        "Elevation": "building_elevation",
        "Number of Buildings": "num_buildings",
        "Flood Zone": "floodzone",
        "Soil Desc": "soil_type",
        "Liquefaction Desc": "liquefaction",
        "Landslide Desc": "landslide",
        "Year Upgraded": "year_updated",
        "Distance to Coast": "distance_from_coast",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Construction Code": "raw_constr_code",
        "TIVcur": "currency",
    }

    
def set_lookup_columns(df):
    df = join_param_table(df, hx.params.country, "Country", "address_dropdown/country", "Country Code", "Country")
    df = join_param_table(df, hx.params.ref_em_construction, "ISO", "constr_code", "EM Construction Code", "raw_constr_code", drop=False)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "sprinkler", "Code", "Sprinkler -Fire", filter_col="RMS Field", filter_val="Sprinkler -Fire")
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "roof_age", "Code", "roofage", filter_col="RMS Field", filter_val="ROOFAGE", force_int_df=True, int_col=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "roof_covering", "Code", "roofsys", filter_col="RMS Field", filter_val="ROOFSYS", force_int_df=True, int_col=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "roof_geometry", "Code", "roofgeom", filter_col="RMS Field", filter_val="ROOFGEOM", force_int_df=True, int_col=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "basement", "Code", "basement", filter_col="RMS Field", filter_val="BASEMENT", force_int_df=True, int_col=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "eq_construction_quality", "Code", "conqual", filter_col="RMS Field", filter_val="CONQUAL", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "plan_irregularity", "Code", "shapeconf", filter_col="RMS Field", filter_val="SHAPECONF", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "soft_story", "Code", "storyprof", filter_col="RMS Field", filter_val="STORYPROF", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "vertical_irregularity", "Code", "overprof", filter_col="RMS Field", filter_val="OVERPROF", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "ornamentation", "Code", "ornament", filter_col="RMS Field", filter_val="ORNAMENT", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "equipment_eq_bracing", "Code", "mechelec", filter_col="RMS Field", filter_val="MECHELEC", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "equipment_support_maintenance", "Code", "duress", filter_col="RMS Field", filter_val="DURESS", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "pounding", "Code", "pounding", filter_col="RMS Field", filter_val="POUNDING", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "ws_construction_quality", "Code", "constquali", filter_col="RMS Field", filter_val="CONQUAL", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "roof_anchor", "Code", "roofanch", filter_col="RMS Field", filter_val="ROOFANCH", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "roof_equipment_hurricane_bracing", "Code", "roofequip", filter_col="RMS Field", filter_val="ROOFEQUIP", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "cladding_type", "Code", "cladsys", filter_col="RMS Field", filter_val="CLADSYS", int_col=True, force_int_df=True)
    df = join_param_table(df, hx.params.ref_em_mapping, "Description", "frame_foundation_connection", "Code", "foundsys", filter_col="RMS Field", filter_val="FOUNDSYS", int_col=True, force_int_df=True)

    # Industry and Occupancy
    df = join_param_table(df, hx.params.ref_occupancy, "Industry", "industry_occupancy_dropdown/industry", "Broker", "broker_occupancy", upper=True, drop=False)
    df = join_param_table(df, hx.params.ref_occupancy, "Industry", "industry_temp_join_column", "Broker", "rms_occupancy", upper=True, drop=False)

    df = join_param_table(df, hx.params.ref_occupancy, "Rater", "industry_occupancy_dropdown/occupancy", "Broker", "broker_occupancy", upper=True, drop=False)
    df = join_param_table(df, hx.params.ref_occupancy, "Rater", "occupancy_temp_join_column", "Broker", "rms_occupancy", upper=True, drop=False)

    df = df.with_columns(
        pl.when(pl.col("industry_occupancy_dropdown/industry") == None)
            .then(pl.col("industry_temp_join_column"))
            .otherwise(pl.col("industry_occupancy_dropdown/industry"))
            .alias("industry_occupancy_dropdown/industry"),
        pl.when(pl.col("industry_occupancy_dropdown/occupancy") == None)
            .then(pl.col("occupancy_temp_join_column"))
            .otherwise(pl.col("industry_occupancy_dropdown/occupancy"))
            .alias("industry_occupancy_dropdown/occupancy"),
    )

    df = df.with_columns(
        pl.when(pl.col("industry_occupancy_dropdown/industry") == None)
            .then(pl.lit("Unknown"))
            .otherwise(pl.col("industry_occupancy_dropdown/industry"))
            .alias("industry_occupancy_dropdown/industry"),
        pl.when(pl.col("industry_occupancy_dropdown/occupancy") == None)
            .then(pl.lit("Unknown"))
            .otherwise(pl.col("industry_occupancy_dropdown/occupancy"))
            .alias("industry_occupancy_dropdown/occupancy"),
    )

    df = df.drop(["industry_temp_join_column", "occupancy_temp_join_column"])

    return df

def join_param_table(df, lookup_df, desired_column, desired_column_name, parameter_table_join_column, df_join_column, filter_col=None, filter_val=None, int_col=False, force_int_df=False, drop=True, upper=False):
    lookup_pl = pl.from_pandas(lookup_df)

    if filter_col and filter_val:
        lookup_pl = lookup_pl.filter(pl.col(filter_col) == filter_val)

    if int_col:
        lookup_pl = lookup_pl.with_columns(pl.col(parameter_table_join_column).cast(pl.Int64).alias(parameter_table_join_column))

    if desired_column_name == df_join_column:
        df = df.rename({df_join_column: "temp_join_column"})
        df_join_column = "temp_join_column"

    lookup_pl = lookup_pl[[desired_column, parameter_table_join_column]].rename({desired_column: desired_column_name, parameter_table_join_column: df_join_column})

    if force_int_df:
        df = df.with_columns(pl.col(df_join_column).cast(pl.Int64).alias(df_join_column))
    
    if upper:
        df = df.with_columns(pl.col(df_join_column).str.to_uppercase().alias(df_join_column))
        lookup_pl = lookup_pl.with_columns(pl.col(df_join_column).str.to_uppercase().alias(df_join_column))

    df = df.join(lookup_pl, on=df_join_column, how="left")
    if drop:
        df = df.drop(df_join_column)
    return df


def pull_exchange_rate_data(hxd, progress):
    if hxd.policy_information.slip_currency == None:
        hxd.policy_information.exchange_rate = 1.0
    else:
        ##### Commented out version of the today, year and month calculation is for automated testing 
        ##### and can be swapped in if a specific exchange rate date needs to be set rather than taking the most recent
        # creation_date = hxd.policy_information.created_date
        # if creation_date:
        #     year, month = creation_date.year, creation_date.month
        # else:
        #     today = date.today()
        #     year, month = today.year, today.month
        today = date.today()
        year, month = today.year, today.month

        quarter = ((month - 1) // 3) + 1

        successful_fetch = False
        while not successful_fetch:
            query = f"""
                SELECT *
                FROM property_data.dbo.vw_currency vlp WITH (NOLOCK)
                    WHERE 1=1
                    AND year = {year}
                    AND quarter = {quarter}
                    AND code = '{hxd.policy_information.slip_currency}'
            """

            search_db_pd, successful = query_exposure_management_database(hxd, progress, query, None, use_pandas=True)
            if search_db_pd is not None:
                successful_fetch = len(search_db_pd)
            if not successful_fetch:
                if quarter == 1:
                    year = year - 1
                    quarter = 4
                else:
                    quarter = quarter - 1
            if year == 2022:
                break
                
        if not successful or len(search_db_pd) == 0:
            hxd.policy_information.exchange_rate = 1
            hxd.policy_information.exchange_rate_date = "Fetch Error"
        else:
            result = search_db_pd.iloc[0]
            hxd.policy_information.exchange_rate = result['xfactor']
            hxd.policy_information.exchange_rate_date = f"{year} Q{quarter}"

def pull_general_exchange_rate_data(hxd, progress,currency):
    if currency == None:
        exchange_rate = 1.0
    else:
        ##### Commented out version of the today, year and month calculation is for automated testing 
        ##### and can be swapped in if a specific exchange rate date needs to be set rather than taking the most recent
        # creation_date = hxd.policy_information.created_date
        # if creation_date:
        #     year, month = creation_date.year, creation_date.month
        # else:
        #     today = date.today()
        #     year, month = today.year, today.month
        today = date.today()
        year, month = today.year, today.month

        quarter = ((month - 1) // 3) + 1

        successful_fetch = False
        while not successful_fetch:
            query = f"""
                SELECT *
                FROM property_data.dbo.vw_currency vlp WITH (NOLOCK)
                    WHERE 1=1
                    AND year = {year}
                    AND quarter = {quarter}
                    AND code = '{currency}'
            """

            search_db_pd, successful = query_exposure_management_database(hxd, progress, query, None, use_pandas=True)
            if search_db_pd is not None:
                successful_fetch = len(search_db_pd)
            if not successful_fetch:
                if quarter == 1:
                    year = year - 1
                    quarter = 4
                else:
                    quarter = quarter - 1
            if year == 2022:
                break
                
        if not successful or len(search_db_pd) == 0:
            exchange_rate = 1
            exchange_rate_date = "Fetch Error"
        else:
            result = search_db_pd.iloc[0]
            exchange_rate = result['xfactor']
            exchange_rate_date = f"{year} Q{quarter}"

    res = [exchange_rate,exchange_rate_date]
    return(res)
    
def remap_dict(df):
    df = df.with_columns(
            pl.col("ws_construction_quality")
                .map_dict({"Good": "Certified design & construction", "Poor": "Obvious signs of deterioration or distress"}),
            pl.col("floodzone")
                .map_dict({"N/A": ""}, default=pl.first())
        )
    
    return df