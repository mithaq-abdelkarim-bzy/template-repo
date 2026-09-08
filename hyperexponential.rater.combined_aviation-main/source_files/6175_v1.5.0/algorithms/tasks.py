import hx
import json
import copy
import os
import pyodbc
import pandas as pd
import numpy as np
import openpyxl
import datetime
import sys
import importlib
import algorithms.rate_constants as c
from algorithms.rate_utilities import ratio, title_rc, one_layer, look_up, rsetattr, rgetattr, rgetkey, date_to_string, policy_term
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, sanitize_and_sort_expiring_list_by_renewal, split_renewal_list_by_expiring
from algorithms.rate_rate_change import rate_change_buckets
from algorithms.data_schema.sch_rater_defined import airlines_dict, airlines_inputs, ga_inputs, coverages_dict
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report


### --- UX --- ###

@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

def fill_additional_fields(hxd):
    expe = hxd.cds.experience_rating
    claims = expe.claims
    inception_date = hxd.hx_core.inception_date
    pol = hxd.cds.policy_info    
    today = datetime.date.today()

 
    # Calculate term
    pol.term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)

    # Save inception date
    pol.inception_date_temp = inception_date

    # Add today's date to application date
    if not pol.application_date:
        pol.application_date = today

    # Add cut-off date
    expe.as_at_date = pol.application_date if pol.application_date else today

    # Calculate YOA
    for idx, claim in enumerate(claims):
        claim.yoa = inception_date.year - idx - 1
        claim.years_to_inception = inception_date.year - claim.yoa

    # Import expiring claims and match to YOA
    if hxd.expiring_claims:
        try:
            # raise ValueError("test") # NOTE: for testing in dev
            expiring_claims_dict = json.loads(hxd.expiring_claims)
            expiring_claims_df = pd.DataFrame(expiring_claims_dict)
            input_columns = [
                "hull_attr_claims",
                "hull_large_losses",
                "hull_gross_premium",
                # "hull_exposure_adj",
                "hull_rate_change",
                "liab_attr_claims",
                "liab_large_losses",
                "liab_gross_premium",
                # "liab_exposure_adj",
                "liab_rate_change",
            ]
            filtered_expiring_claims_df = expiring_claims_df[["yoa"] + input_columns]

            # Merge the expiring and current claims_df and pushed to hxd
            claims_df = pd.DataFrame([{"yoa": claim.yoa} for claim in claims])
            merged_df = claims_df.merge(filtered_expiring_claims_df, on="yoa", how="left")
            if not merged_df.empty:
                write_pd_to_hxd(merged_df, claims, input_columns, replace_nan=True)

                expe.expiring_claims_msg = "✅ Claims from expiring policy imported successfully."

        except Exception as e:
            expe.expiring_claims_msg = f"❗❗ Failed to import expiring claims. Please proceed and enter data manually. ❗❗\n\nError for dev team:\n{e}"
            expe.show_expiring_claims_msg = True

@hx.task
def show_airlines_task(hxd, progress):
    ms = hxd.model_state
    claims = hxd.cds.experience_rating.claims

    # Allow user to proceed even if SQL connection fails
    try:
        # raise ValueError("test") # NOTE: for testing in dev
        get_sql_inputs_task(hxd, progress)
    except:
        ms.has_sql_conn_failed = True

    ms.pressed_airlines_task = True
    ms.pressed_ga_task = False

    fill_additional_fields(hxd)

    #Add default values for the airlines
    exp_details = hxd.cds.exposure.granular.airlines_default[0]
    layer_hull = hxd.cds.layers[0].coverages.hull
    layer_liab = hxd.cds.layers[0].coverages.liability


    exp_details.no_of_aircraft = 1
    exp_details.attachment_date = hxd.hx_core.inception_date
    exp_details.expiry_date = hxd.hx_core.expiry_date
    if layer_hull.coverage == "Total Loss":
        exp_details.coverage = "TLO"
    else:
        exp_details.coverage = layer_hull.coverage
    exp_details.hull_limit = layer_hull.limit
    exp_details.hull_excess = layer_hull.excess
    exp_details.hull_ccy = layer_hull.currency.selected
    exp_details.liability_limit = layer_liab.limit
    exp_details.liability_excess = layer_liab.excess
    exp_details.liability_ccy = layer_liab.currency.selected

    # add the Policy Reference to PAS
    hx.meta.pas_references.clear()
    hull_section_ref = hxd.cds.layers[0].coverages.hull.section_reference
    liab_section_ref = hxd.cds.layers[0].coverages.liability.section_reference
    if hull_section_ref is not None:
        hx.meta.pas_references.append(hull_section_ref[:8])
    elif liab_section_ref is not None:
        hx.meta.pas_references.append(liab_section_ref[:8])

@hx.task
def show_ga_task(hxd, progress):
    ms = hxd.model_state

    # Allow user to proceed even if SQL connection fails
    try:
        get_sql_inputs_task(hxd, progress)
    except:
        ms.has_sql_conn_failed = True

    ms.pressed_ga_task = True
    ms.pressed_airlines_task = False

    fill_additional_fields(hxd)

    # Add default values for the aircrafts
    exp_details = hxd.cds.exposure.granular.aircrafts_default[0]
    layer_hull = hxd.cds.layers[0].coverages.hull
    layer_liab = hxd.cds.layers[0].coverages.liability


    exp_details.no_of_aircraft = 1
    exp_details.attachment_date = hxd.hx_core.inception_date
    exp_details.expiry_date = hxd.hx_core.expiry_date
    exp_details.hull_ccy = layer_hull.currency.selected
    exp_details.combined_single_limit = layer_liab.limit
    exp_details.liability_ccy = layer_liab.currency.selected  

    # add the Policy Reference to PAS
    hx.meta.pas_references.clear()
    hull_section_ref = hxd.cds.layers[0].coverages.hull.section_reference
    liab_section_ref = hxd.cds.layers[0].coverages.liability.section_reference
    if hull_section_ref is not None:
        hx.meta.pas_references.append(hull_section_ref[:8])
    elif liab_section_ref is not None:
        hx.meta.pas_references.append(liab_section_ref[:8])


### --- AIRLINES DETAILS --- ###

def clean_airlines_dict(airlines_dict):

    airlines_dict.pop("pll_award")
    airlines_dict.pop("tpl_limit_exposed")
    airlines_dict.pop("achieved_hull_rate")
    
    return airlines_dict

def get_common_query(product="Airlines", table="[Marine].[dbo].[aviation_fleet_live_data]"):

    if product == "General Aviation":
        common_query = f"""
        SELECT 
            [aircraft_class],
            [operator],                          -- Operator Name
            [aircraft_master_series],            -- Master Series
            [registration],                      -- Registration
            [operator_country],                  -- Operator Country
            -- [operator_region],                   -- Operator Region
            [primary_usage],
            [total_seats],                       -- Seats
            [number_of_engines],
            [build_country],
            [build_year]                         -- FS 02/09/2025: build_year
        FROM {table}
        """
    else:
        # Extract the list of Russian manufacturers
        russian_df = hx.params.RussianManufacturer
        russian_manufacturers = russian_df["Russian Manufacturer"].dropna().unique().tolist()
        escaped_manufacturers = [manufacturer.replace("'", "''") for manufacturer in russian_manufacturers]
        manufacturers_list = ", ".join(f"'{manufacturer}'" for manufacturer in escaped_manufacturers)

        common_query = f"""
        SELECT 
            [operator],                          -- Operator Name
            [aircraft_master_series],            -- Master Series
            [registration],                      -- Registration
            [aircraft_status],                   -- Status
            [build_year],                        -- Build Year
            [primary_usage],                     -- Primary Usage
            [market_class],                      -- Market Class
            [operator_country],                  -- Operator Country
            -- [operator_region],                   -- Operator Region
            [total_seats],                       -- Seats
            [previous12_months_hours],           -- Utilisation (Annual hours)
            [operating_mtow_lb],                 -- MTOW (if using Operating MTOW)
            --[certified_mtow_lb],                  -- MTOW (if using Certified MTOW)
            CASE 
                WHEN [aircraft_manufacturer] IN ({manufacturers_list}) THEN 1
                ELSE 0
            END AS [russian_built]              -- Logic for Russian Built (Airlines)
        FROM {table}
        """

    return common_query

def enrich_airlines_table(hxd, airlines_df):
    sf = hxd.cds.standard_fields
    layer, cvg = one_layer(hxd)
    UsageMapping = hx.params.al_UsageMapping
    StatusMapping = hx.params.al_StatusMapping
    OperatorCountryList = hx.params.OperatorCountryList

    airlines_df["no_of_aircraft"] = 1
    airlines_df["attachment_date"] = sf.inception_date
    airlines_df["expiry_date"] = sf.expiry_date
    airlines_df["time_in_service"] = 1
    airlines_df["usage"] = look_up(airlines_df["primary_usage"], "AircraftUsage", "AircraftUsageMapped", UsageMapping, if_not_found="Other")
    airlines_df["aircraft_status"] = look_up(airlines_df["aircraft_status"], "Cirium Field Name", "Airlines Rater Mapped Name", StatusMapping, if_not_found="Other")
    # airlines_df["operator_region"] = look_up(airlines_df["operator_country"], "Country", "Region Airlines", OperatorCountryList, if_not_found=np.nan) # Moved to rating
    
    airlines_df["hull_limit"] = cvg.hull.limit
    airlines_df["hull_excess"] = cvg.hull.excess
    airlines_df["hull_ccy"] = cvg.hull.currency.selected
    airlines_df["liability_limit"] = cvg.liability.limit
    airlines_df["liability_excess"] = cvg.liability.excess
    airlines_df["liability_ccy"] = cvg.liability.currency.selected

    # Avoid errors if entry doesn't exist in dropdown
    airlines_df["primary_usage"] = airlines_df["primary_usage"].apply(lambda x: x if x in c.primary_usage_options else None) 
    airlines_df["market_class"] = airlines_df["market_class"].apply(lambda x: x if x in c.market_class_options else None)
    # airlines_df["operator_region"] = airlines_df["operator_region"].apply(lambda x: x if x in c.region_options else None)

    return airlines_df

### --- AIRCRAFT DETAILS --- ###

def clean_ga_dict(ga_dict):
    ga_dict.pop("per_occ_deductible")
    ga_dict.pop("achieved_hull_rate")
    # ga_dict.pop("countries")
    return ga_dict

def enrich_aircrafts_table(hxd, aircrafts_df):
    sf = hxd.cds.standard_fields
    layer, cvg = one_layer(hxd)
    CiriumClassMapping = hx.params.CiriumClassMapping
    OperatorCountryList = hx.params.OperatorCountryList
    MappedUsageType = hx.params.ga_MappedUsageType

    aircrafts_df["no_of_aircraft"] = 1
    aircrafts_df["hull_ccy"] = cvg.hull.currency.selected
    aircrafts_df["attachment_date"] = sf.inception_date
    aircrafts_df["expiry_date"] = sf.expiry_date
    aircrafts_df["time_in_service"] = 1
    aircrafts_df["pax_net_worth"] = "Unknown"
    aircrafts_df["combined_single_limit"] = cvg.liability.limit
    aircrafts_df["liability_ccy"] = cvg.liability.currency.selected
    aircrafts_df["tpl_limit_exposed"] = 1

    aircrafts_df["aircraft_class_group"] = look_up(aircrafts_df["aircraft_class"], "Cirium Aircraft Class", "Mapped Rater Class", CiriumClassMapping, if_not_found="empty")
    aircrafts_df["number_of_engines_group"] = np.where(aircrafts_df["number_of_engines"] > 1, "Multi", "Single")
    aircrafts_df["class_engine_split"] = look_up(aircrafts_df["aircraft_class"], "Cirium Aircraft Class", "Class Split by Number of Engines", CiriumClassMapping, if_not_found="N")
    aircrafts_df["aircraft_class"] = np.where(aircrafts_df["class_engine_split"] == "N", aircrafts_df["aircraft_class_group"], np.where(
        aircrafts_df["number_of_engines_group"] == "Single", aircrafts_df["aircraft_class_group"] + "1", aircrafts_df["aircraft_class_group"] + "2"
    ))

    aircrafts_df["build_location"] = aircrafts_df["build_country"].map(
        lambda x: "Russian Built" if x == "Russia" else None if pd.isna(x) else "Non-Russian Built"
    )
    # aircrafts_df["operator_region"] = look_up(aircrafts_df["operator_country"], "Country", "Region GA", OperatorCountryList)
    aircrafts_df["use"] = look_up(aircrafts_df["primary_usage"], "Cirium Primary Usage", "GA Mapped Primary Usage", MappedUsageType, if_not_found="Other")

    # Avoid errors if entry doesn't exist in dropdown
    aircrafts_df["aircraft_class"] = aircrafts_df["aircraft_class"].apply(lambda x: x if x in c.aircraft_class_options else None)
    # aircrafts_df["operator_region"] = aircrafts_df["operator_region"].apply(lambda x: x if x in c.ga_region_options else None)
    aircrafts_df["use"] = aircrafts_df["use"].apply(lambda x: x if x in c.ga_use_options else None)

    # Remove helper columns
    aircrafts_df = aircrafts_df.drop(columns=["primary_usage", "build_country", "number_of_engines", "aircraft_class_group", "number_of_engines_group", "class_engine_split"])

    return aircrafts_df

### --- USEFUL COMMON FUNCTIONS --- ###

def sql_query(query):
    # Get login details
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
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + host + ';'
        'UID=' + user + ';'
        'PWD=' + pwd,
        timeout=30
    )

    # Run a new query and close connection
    result = pd.read_sql_query(query, conn)
    conn.close()

    return result


def order_by_reg(hxd, df, df_col="registration", input_regs=None):
    expo = hxd.cds.exposure.granular

    if not input_regs:
        # input_regs = [reg.registration for reg in expo.registrations if reg.registration is not None]
        input_regs = [ac.registration for ac in expo.airlines if ac.registration is not None]

    if input_regs:
        try: # Avoid error when input registrations have been deleted accidentally
            df[df_col] = pd.Categorical(df[df_col], categories=input_regs, ordered=True)
            df = df.sort_values(df_col)
        except:
            return df

    return df

def assign_to_hxd_from_reg(hxd, df, dict_):
    if hxd.cds.is_ga:
        inputs_dict = clean_ga_dict(dict_)
        ac_list = hxd.cds.exposure.granular.aircrafts
    else:
        inputs_dict = clean_airlines_dict(dict_)
        ac_list = hxd.cds.exposure.granular.airlines

    for ac in ac_list:
        ac_df = df[df["registration"] == ac.registration]
        if ac_df.empty: # Allow for registrations not present in SQL DB
            continue

        for node in inputs_dict.keys():
            if node not in ac_df.columns: # Skip nodes not present in df
                continue

            df_value = ac_df[node].iloc[0]
            current_value = getattr(ac, node)
            setattr(ac, node, df_value if not current_value else current_value)

### --- TASKS --- ###

# Fetch available inputs from SQL databse
@hx.task
def get_sql_inputs_task(hxd, progress):
    
    table = "[Marine].[dbo].[aviation_fleet_live_data]"

    # Operators NOTE: removed dropdown - inconsistent behaviour leading to slow model in TST
    # query = f"SELECT DISTINCT [operator] FROM {table} ORDER BY [operator]"
    # df = sql_query(query)
    # hxd.sql_db.operators = df.to_dict("records")

    # Registrations NOTE: removed dropdown - too many regs were making model freeze when searching for one
    # query = f"SELECT DISTINCT [registration] FROM {table} ORDER BY [registration]"
    # df = sql_query(query)
    # hxd.sql_db.registrations = df.to_dict("records")

    # Master series
    query = f"SELECT DISTINCT [aircraft_master_series] FROM {table} ORDER BY [aircraft_master_series]"
    df = sql_query(query)
    hxd.sql_db.master_series = df.to_dict("records")

# --- Fetch Cirium data from SQL
@hx.task
def search_for_operator_task(hxd, progress):
    expo = hxd.cds.exposure.granular

    operator = expo.operator_search

    # Run operator search
    try:
        table = "[Marine].[dbo].[aviation_fleet_live_data]"
        query = f"SELECT DISTINCT [operator] FROM {table} WHERE [operator] LIKE '%{operator}%' ORDER BY [operator]"
        df = sql_query(query)

        if df.shape[0] > 0:
            hxd.sql_db.operators = df.to_dict("records")

        # Provide confirmation message
        expo.operators_msg = f"✅ {df.shape[0]} operator(s) found."
        expo.are_operators_fetched = True
    
    except Exception as e:
        expo.operators_msg = f"❗❗ Failed to connect to database. ❗❗\n\nError for dev team:\n{e}"
        expo.are_operators_fetched = True


@hx.task
def fetch_by_operator_task(hxd, progress):
    expo = hxd.cds.exposure.granular

    if all(op.operator is None for op in expo.operators):
        hx.errors.fatal("List of Operators cannot be empty.")

    # Concatenate operators
    operators = ', '.join(f"'{op.operator}'" for op in expo.operators if op.operator is not None)

    # Build query
    query = f"""
    {get_common_query(product=hxd.cds.rater)}
    WHERE [operator] IN ({operators})
    ORDER BY [operator], [registration]
    """

    df = sql_query(query)

    # Enrich with additional fields
    if hxd.cds.is_ga:
        # Add GA-specific fields
        aircrafts_df = enrich_aircrafts_table(hxd, aircrafts_df=df)
        
        # Fill NaN with None and push to hxd
        aircrafts_df = aircrafts_df.fillna(np.nan).replace([np.nan], [None])
        expo.aircrafts = aircrafts_df.to_dict("records")
    else:
        # Add Airlines-specific fields
        airlines_df = enrich_airlines_table(hxd, airlines_df=df)
        
        # Fill NaN with None and push to hxd
        airlines_df = airlines_df.fillna(np.nan).replace([np.nan], [None])
        expo.airlines = airlines_df.to_dict("records")


def check_missing_registrations(reg_list, df):
    # Convert input list and DataFrame column to sets
    input_regs = set(reg_list)
    found_regs = set(df["registration"])

    # Find missing registrations
    missing_regs = input_regs - found_regs
    has_missing = bool(missing_regs)  # True if there are missing registrations

    # Create a user-friendly message
    if has_missing:
        message = f"⚠️ The following registrations were not found: {', '.join(missing_regs)}"
    else:
        message = "✅ All registrations were found."

    return has_missing, message

@hx.task
def fetch_by_registration_task(hxd, progress):
    expo = hxd.cds.exposure.granular
    airlines = expo.airlines
    aircrafts = expo.aircrafts
    sql = hxd.sql_db

    # Concatenate registrations
    if hxd.cds.is_ga:
        reg_list = [ac.registration for ac in aircrafts]
    else:
        reg_list = [ac.registration for ac in airlines]

    if all(reg is None for reg in reg_list):
        hx.errors.fatal("List of Registrations cannot be blank.")

    registrations = ', '.join(f"'{reg}'" for reg in reg_list if reg is not None)

    # Check duplicate registrations
    table = "[Marine].[dbo].[aviation_fleet_live_data]"
    regs_query = f"""
    SELECT [registration]
    FROM {table}
    WHERE [registration] IN ({registrations})
    GROUP BY [registration]
    HAVING COUNT(*) > 1;
    """
    regs_df = sql_query(regs_query)

    if not regs_df.empty:
        duplicate_regs = ', '.join(f"'{reg}'" for reg in regs_df["registration"] if reg is not None)
        duplicate_regs_query = f"""
        SELECT
            [registration],
            [aircraft_family],
            [operator],
            [serial_number]
        FROM {table}
        WHERE [registration] IN ({duplicate_regs})
        ORDER BY [registration]
        """

        duplicate_regs_df = sql_query(duplicate_regs_query)
        duplicate_regs_df = order_by_reg(hxd, duplicate_regs_df)
        sql.duplicate_regs = duplicate_regs_df.to_dict("records")
        sql.has_duplicate_regs = True
        sql.are_regs_selected = False

        return # Don't proceed if there are duplicates

    # Build query
    query = f"""
    {get_common_query(product=hxd.cds.rater)}
    WHERE [registration] IN ({registrations})
    ORDER BY [operator], [registration]
    """

    df = sql_query(query)

    # Enrich with additional fields
    if hxd.cds.is_ga:
        # Add GA-specific fields
        aircrafts_df = enrich_aircrafts_table(hxd, aircrafts_df=df)
        
        # Fill NaN with None and push to hxd
        aircrafts_df = aircrafts_df.fillna(np.nan).replace([np.nan], [None])
        assign_to_hxd_from_reg(hxd, aircrafts_df, ga_inputs)
    else:
        # Add Airlines-specific fields
        airlines_df = enrich_airlines_table(hxd, airlines_df=df)
        
        # Fill NaN with None and push to hxd
        airlines_df = airlines_df.fillna(np.nan).replace([np.nan], [None])
        assign_to_hxd_from_reg(hxd, airlines_df, airlines_dict)

    # Return message for missing regs
    expo.has_missing_regs, expo.has_missing_regs_msg = check_missing_registrations(reg_list, df)

@hx.task
def get_selected_regs_task(hxd, progress):
    expo = hxd.cds.exposure.granular
    airlines = expo.airlines
    aircrafts = expo.aircrafts
    sql = hxd.sql_db
    
    # Get unique registrations
    duplicate_regs = {reg.registration for reg in sql.duplicate_regs}

    if hxd.cds.is_ga:
        all_regs = {ac.registration for ac in aircrafts}
    else:
        all_regs = {ac.registration for ac in airlines}

    unique_regs = all_regs - duplicate_regs
    unique_regs_str = ', '.join(f"'{reg}'" for reg in unique_regs)

    # Don't run if there are no registrations
    if all(reg.is_selected is False for reg in sql.duplicate_regs) and (not unique_regs_str):
        sql.has_duplicate_regs = False
        sql.are_regs_selected = True
        return

    # Build query
    where_condition = f"WHERE [registration] IN ({unique_regs_str})\nOR " if unique_regs_str else "WHERE "
    query = f"{get_common_query(product=hxd.cds.rater)}\n" + where_condition

    # Dynamically add conditions for the selected registrations
    conditions = []

    for reg in sql.duplicate_regs:
        if reg.is_selected:
            # Construct the condition for each selected registration
            condition = f"([registration] = '{reg.registration}' AND [aircraft_family] = '{reg.aircraft_family}' AND [operator] = '{reg.operator}' AND [serial_number] = '{reg.serial_number}')"
            # Append the condition to the list
            conditions.append(condition)

    query += " OR \n".join(conditions)
    # hxd.debug_str = query NOTE: for debugging
    df = sql_query(query)

    # Enrich with additional fields
    if hxd.cds.is_ga:
        # Add GA-specific fields
        aircrafts_df = enrich_aircrafts_table(hxd, aircrafts_df=df)
        
        # Fill NaN with None and push to hxd
        aircrafts_df = aircrafts_df.fillna(np.nan).replace([np.nan], [None])
        assign_to_hxd_from_reg(hxd, aircrafts_df, ga_inputs)
    else:
        # Add Airlines-specific fields
        airlines_df = enrich_airlines_table(hxd, airlines_df=df)
        
        # Fill NaN with None and push to hxd
        airlines_df = airlines_df.fillna(np.nan).replace([np.nan], [None])
        assign_to_hxd_from_reg(hxd, airlines_df, airlines_inputs)

    sql.has_duplicate_regs = False
    sql.are_regs_selected = True

    # Return message for missing regs
    expo.has_missing_regs, expo.has_missing_regs_msg = check_missing_registrations(list(all_regs), df)

@hx.task
def clear_table_task(hxd, progress):
    pass # No need to do anything as task will clear inputs upon running

# FS 25/09/2025: Additional async task added to fill in PAX limit as 0 when the time in service is 0%
@hx.task
def fill_pax_limit_implied(hxd, progress):
    # Retrieve current inputs for time in service and pax liability limit
    aircrafts = hxd.cds.exposure.granular.aircrafts
    time_in_service = np.array([ac.time_in_service for ac in aircrafts])
    pax_liab = np.array([ac.per_pax_liab_limit for ac in aircrafts])

    # Set pax liability limit to 0 where time in service is 0%
    alt_pax_liab = np.where(time_in_service == 0, 0, pax_liab)
    for ac, alt_value in zip(aircrafts, alt_pax_liab):
        setattr(ac, "per_pax_liab_limit", alt_value)
    

@hx.task
def fill_with_defaults_task(hxd, progress):
    expo = hxd.cds.exposure.granular

    if hxd.cds.is_ga:
        inputs_dict = clean_ga_dict(ga_inputs)
        ac_list = expo.aircrafts
        ac_list_default = expo.aircrafts_default
    else:
        inputs_dict = clean_airlines_dict(airlines_inputs)
        ac_list = expo.airlines
        ac_list_default = expo.airlines_default

    # Fill in empty values with defaults
    for ac in ac_list:
        for node in inputs_dict.keys():
            default_value = getattr(ac_list_default[0], node)
            current_value = getattr(ac, node)
            setattr(ac, node, default_value if not current_value else current_value)
        

### --- EXPERIENCE RATING --- ###
@hx.task
def fill_historic_premium_task(hxd, progress):
    _, cvg = one_layer(hxd)
    expe = hxd.cds.experience_rating
    years = expe.no_of_years_history

    if years > len(expe.claims):
        hx.errors.fatal(f"Number of years of history ({years} years) cannot be greater than the number of rows in the claims table ({len(expe.claims)} rows).")

    claims_length = len(expe.claims)
    for idx in range(0, claims_length):        
        c = expe.claims[idx]
        c.hull_gross_premium = None if idx >= years else cvg.hull.quoted_premium 
        c.liab_gross_premium = None if idx >= years else cvg.liability.quoted_premium 
        c.hull_attr_claims = None if idx >= years else 0 if not c.hull_attr_claims else c.hull_attr_claims
        c.liab_attr_claims = None if idx >= years else 0 if not c.liab_attr_claims else c.liab_attr_claims
        c.hull_large_losses = None if idx >= years else 0 if not c.hull_large_losses else c.hull_large_losses
        c.liab_large_losses = None if idx >= years else 0 if not c.liab_large_losses else c.liab_large_losses


### --- RATE CHANGE --- ###
def get_expiring_data(hxd):
    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: id used for testing
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
    expiring_data = expiring_response["data"]

    return expiring_data

def clean_expiring_data(hxd, fillna=False, remove_bulk_pricing=False, remove_duplicates=False):
    """
    Sorts the expiring aircrafts in the same order as the renewing aircrafts.
    Renewal may have additional aircrafts which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of aircrafts that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional aircrafts that are present in renewal but not in expiring.
    """

    expo = hxd.cds.exposure.granular

    # Get expiring data but remove bloating from dynamic dropdown data
    expiring_data = get_expiring_data(hxd)
    expiring_data = {
        "cds": expiring_data["cds"],
        "model_state": expiring_data["model_state"],
        "hx_core": expiring_data["hx_core"],
        "expiring_claims": expiring_data["expiring_claims"],
        "rate_change": expiring_data["rate_change"]
    }

    # Map structures
    hxd_structures = {
        "aircrafts": hxd.rate_change.aircrafts,
        "airlines": hxd.rate_change.airlines
    }

    # Ensure expiring list of aircrafts follows the same order as renewal
    list_name = "aircrafts" if hxd.cds.is_ga else "airlines"
    expiring_list = expiring_data["cds"]["exposure"]["granular"][list_name]
    renewal_list = json.loads(hxd_structures[list_name])

    sorted_expiring_list, warnings = sanitize_and_sort_expiring_list_by_renewal(
        expiring_list, 
        renewal_list, 
        sorting_key="registration", 
        fillna=fillna, 
        remove_bulk_pricing=remove_bulk_pricing, 
        remove_duplicates=remove_duplicates
    )

    expiring_data_sorted = copy.deepcopy(expiring_data)

    # Return split data
    expiring_list_common, renewal_list_others, expiring_list_dropped = split_renewal_list_by_expiring(sorted_expiring_list, renewal_list, sorting_key="registration")
    expiring_data_common = copy.deepcopy(expiring_data)
    expiring_data_others = copy.deepcopy(expiring_data) # Calling this expiring_data even though the specified list will contain renewal elements
    expiring_data_dropped = copy.deepcopy(expiring_data)
    
    # FS 27/08/2025: RC additions for aircrafts

    if list_name == "aircrafts":
        # Items retrieved from renewal and fed into expiry data
        renewal_list_common = [row for row in renewal_list if row not in renewal_list_others]
        items_from_renewal = ["aircraft_class", "build_year"]
        for i in range(0,len(renewal_list_common)):
            for item in items_from_renewal:
                expiring_list_common[i][item] = renewal_list_common[i].get(item)

        # Default item values assigned to laspsed expiry policies to calculate partial loss
        expiry_default = {"build_year":1985} 
        for j in range(0, len(expiring_list_dropped)):
            # Find build year and number of engines within cirium database using registration
            reg = expiring_list_dropped[j]["registration"]
            query = f"""
            {get_common_query(product="General Aviation")}
            WHERE [registration] = '{reg}'
            """
            cirium_aircraft = sql_query(query) 

            # Add cirium information to lapsed policies if available
            if not cirium_aircraft.empty:
                expiring_list_dropped[j]["build_year"] = cirium_aircraft["build_year"].iloc[0]
                aircraft_class = expiring_list_dropped[j]["aircraft_class"]
                if aircraft_class in ["BusinessJet", "PistonHeli"]:
                    expiring_list_dropped[j]["aircraft_class"] = aircraft_class + "2" if cirium_aircraft["number_of_engines"].iloc[0] > 1 else aircraft_class + "1"
            else:
                # Otherwise add default values to lapsed policies
                expiring_list_dropped[j]["build_year"] = expiry_default["build_year"]
                if expiring_list_dropped[j]["aircraft_class"] == "BusinessJet":
                    expiring_list_dropped[j]["aircraft_class"] = expiring_list_dropped[j]["aircraft_class"] + "2"
                elif expiring_list_dropped[j]["aircraft_class"] == "PistonHeli":
                    expiring_list_dropped[j]["aircraft_class"] = expiring_list_dropped[j]["aircraft_class"] + "1"

        # New adjusted expiry data
        adjusted_expiry_list = expiring_list_common + expiring_list_dropped
        expiring_data_sorted["cds"]["exposure"]["granular"][list_name] = adjusted_expiry_list
    else:
        # No changes to expiry for airlines
        expiring_data_sorted["cds"]["exposure"]["granular"][list_name] = sorted_expiring_list

    expiring_data_common["cds"]["exposure"]["granular"][list_name] = expiring_list_common
    expiring_data_others["cds"]["exposure"]["granular"][list_name] = renewal_list_others
    expiring_data_dropped["cds"]["exposure"]["granular"][list_name] = expiring_list_dropped

    # Check for term changes
    expiring_term = expiring_data_sorted["cds"]["policy_info"]["term"]
    renewal_term = hxd.cds.policy_info.term
    term_warning = ""

    if expiring_term != renewal_term:
        term_warning = f"Policy term has changed from {expiring_term} to {renewal_term} years."

    return expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped, warnings, term_warning



# Import expiring policy for rate change
@hx.task
def expiring_policy_fetch_task(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    expiring_data = get_expiring_data(hxd)

    # Get fields from json response and push to hxd
    coverages = ["hull", "liability"]
    for idx, layer in enumerate(hxd.cds.layers):
        hxd_coverages = [layer.rate_change.hull, layer.rate_change.liability]

        # Overall
        layer.rate_change.expiring_policy_info.expiring_premium = expiring_data["cds"]["layers"][idx]["quoted_premium"]
        layer.rate_change.expiring_policy_info.expiring_premium_annualised = expiring_data["cds"]["layers"][idx]["quoted_premium_annualised"]
        layer.rate_change.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["written_line"]

        # By coverage
        for cvg, hxd_cvg in zip(coverages, hxd_coverages):
            hxd_cvg.expiring_policy_info.expiring_premium = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["quoted_premium"]
            hxd_cvg.expiring_policy_info.expiring_premium_annualised = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["quoted_premium_annualised"]
            hxd_cvg.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["written_line"]
            hxd_cvg.expiring_policy_info.expiring_benchmark_premium_post_uw_adj = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["benchmark_premium_post_uw_adj"]
            hxd_cvg.expiring_policy_info.expiring_benchmark_premium = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["benchmark_premium"]
            hxd_cvg.expiring_policy_info.expiring_bpi = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["bpi"]
            hxd_cvg.expiring_policy_info.expiring_written_line = expiring_data["cds"]["layers"][idx]["coverages"][cvg]["written_line"]


@hx.task
def rarc_task(hxd, progress):
    layer, cvg = one_layer(hxd)
    rc = hxd.cds.rate_change
    
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected

    if not expiring_policy_option_id:
       hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get correct buckets based on coverage
    hull_buckets, liab_buckets = rate_change_buckets(hxd)

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)
    # expiring_policy_option_id = 243035 # NOTE: for debugging

    # Get expiring data split between common and other aircrafts
    expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped, warnings, term_warning = clean_expiring_data(
        hxd, fillna=True, remove_bulk_pricing=True, remove_duplicates=True
    )

    # Prepare arguments for calculate_repriced_values() function
    kw_args = {
        "custom_expiring_data": [expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped],
        "split_list_path": "cds/exposure/granular/" + ("aircrafts" if hxd.cds.is_ga else "airlines"),
        "matching_key": "registration",
        "additional_items_bucket": "exposure"
    }

    # --- Rate Change for Hull --- #
    hull_rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=hull_buckets,
        layers_path="cds/layers",
        expiring_actual_prem="coverages/hull/quoted_premium_annualised",
        expiring_technical_prem="coverages/hull/benchmark_premium_annualised",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    hull_rc_hxds = hull_rc.calculate_repriced_values(**kw_args)

    # Use the repriced values to calculate the changes for each bucket
    hull_rarc_df, hull_rarc_list = hull_rc.calculate_rarc_by_layer()

    # Push to hxd
    for rarc_layer, hxd_layer in zip(hull_rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.hull = rarc_layer

    # --- Rate Change for Liability --- #
    liab_rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=liab_buckets,
        layers_path="cds/layers",
        expiring_actual_prem="coverages/liability/quoted_premium_annualised",
        expiring_technical_prem="coverages/liability/benchmark_premium_annualised",
        async_tasks=[],  # Pass the actual tasks, not strings
        data_schema_static_path=data_schema_static_path
    )

    liab_rc_hxds = liab_rc.calculate_repriced_values(**kw_args)

    # Use the repriced values to calculate the changes for each bucket
    liab_rarc_df, liab_rarc_list = liab_rc.calculate_rarc_by_layer()

    # Push to hxd
    for rarc_layer, hxd_layer in zip(liab_rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.liability = rarc_layer

    # NOTE: for debugging
    # pd.set_option('display.max_columns', None)
    # print(hull_rarc_df)

    # Add warning messages
    warning_messages = []
    
    if warnings:  # Aircraft-related warnings
        bullet_list = "\n".join([f"- {w}" for w in warnings])
        warning_messages.append(f"""⚠️ Caution:\n
        {bullet_list}\n\n
        These expiry aircrafts have been removed from the RARC calculation as there is no exact match to the renewing fleet exposures.
        Please contact the Actuarial team to more accurately reflect these risks in the RARC.""")
    
    if term_warning:  # Term change warning
        warning_messages.append(f"⚠️ Note:\n- {term_warning}\n\nThis may affect the RARC calculation.")
    
    if warning_messages:
        rc.reg_warning = "\n\n".join(warning_messages)


def filter_data_schema(data_schema_csv, filters):
    df = pd.read_csv(data_schema_csv)
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
    ignored_fields = ["insured_country",
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
]
    def traverse_and_filter(current_obj, current_path):
        if isinstance(current_obj, dict):
            # Check if the dictionary contains the specific fields
            if all(key in current_obj for key in ["selected", "calculated", "is_overridden"]):
                # Compute the value based on the logic
                computed_value = current_obj["selected"] if current_obj["is_overridden"] else current_obj["calculated"]
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
                new_path = f"{current_path}/{key}" if current_path and key != "calculated" else key
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
    data_schema_csv = "./model/algorithms/data_schema/exported_data_schema.csv"
    # data_schema_csv = "/workspace/editing/algorithms/data_schema/exported_data_schema.csv"
    filters = [
        {"column": "Mode", "operator": "eq", "value": "input"},
        # {"column": "Mode", "operator": "eq", "value": "override"},
    ]
    filtered_data_schema = filter_data_schema(data_schema_csv,filters)    

    ms = hxd.model_state    

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hx.meta.expiring_policy_option_id # or 743948 # NOTE: For testing in dev mode
    # expiring_policy_option_id = 775776

    try: 
        expiring_nodes = filtered_data_schema["Path"].tolist()
        expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
        expiring_data = expiring_response["data"]
        # Save expiring claims
        hxd.expiring_claims = json.dumps(expiring_data["cds"]["experience_rating"]["claims"])        
        # Save expiring aircrafts by registration
        hxd.rate_change.expiring_aircrafts = json.dumps([a["registration"] for a in expiring_data["cds"]["exposure"]["granular"]["aircrafts"]])
        is_ga = expiring_data["cds"]["rater"] == "General Aviation"
        is_airline = expiring_data["cds"]["rater"] == "Airlines"
        filtered_expiring_data = filter_and_replace_json(expiring_nodes, expiring_data)        

        #Update Attachment and Expiry dates in expiring data
        expiring_list_path = "aircrafts" if is_ga else "airlines" if is_airline else ""

        #FS 23/09/2025: Additional expiry manipulation for aircrafts
        if expiring_list_path == "aircrafts":
            expiring_aircraft_details = filtered_expiring_data["cds"]["exposure"]["granular"][expiring_list_path]
            for j in range(0, len(expiring_aircraft_details)):
                aircraft_class = expiring_aircraft_details[j]["aircraft_class"]
                
                # Find aircraft class and number of engines within cirium database using registration
                if aircraft_class in ("BusinessJet", "PistonHeli"):
                    reg = expiring_aircraft_details[j]["registration"]

                    query = f"""
                    {get_common_query(product="General Aviation")}
                    WHERE [registration] = '{reg}'
                    """
                    cirium_aircraft = sql_query(query) 

                    # Add cirium information to expiry if available
                    if not cirium_aircraft.empty:
                        expiring_aircraft_details[j]["aircraft_class"] = aircraft_class + "2" if cirium_aircraft["number_of_engines"].iloc[0] > 1 else aircraft_class + "1"
                    else:
                        if expiring_aircraft_details[j]["aircraft_class"] == "BusinessJet":
                            expiring_aircraft_details[j]["aircraft_class"] = expiring_aircraft_details[j]["aircraft_class"] + "2"
                        elif expiring_aircraft_details[j]["aircraft_class"] == "PistonHeli":
                            expiring_aircraft_details[j]["aircraft_class"] = expiring_aircraft_details[j]["aircraft_class"] + "1"
            filtered_expiring_data["cds"]["exposure"]["granular"][expiring_list_path] = expiring_aircraft_details

        filtered_expiring_list = filtered_expiring_data["cds"]["exposure"]["granular"][expiring_list_path]
        for d in filtered_expiring_list:
            d["attachment_date"] = date_to_string(hxd.hx_core.inception_date)
            d["expiry_date"] = date_to_string(hxd.hx_core.expiry_date)        

        hxd.cds = filtered_expiring_data["cds"]          
        hxd.model_state = filtered_expiring_data["model_state"]          

        ms.pressed_start_renewal_task = True
        ms.pressed_airlines_task = False             
        ms.pressed_ga_task = False    
        ms.expiring_policy_option_id = expiring_policy_option_id         
        if is_ga:
            ms.pressed_ga_task = True
            fill_additional_fields(hxd)
            # Add default values for the aircrafts
            exp_details = hxd.cds.exposure.granular.aircrafts_default[0]
            layer_hull = hxd.cds.layers[0].coverages.hull
            layer_liab = hxd.cds.layers[0].coverages.liability
            exp_details.no_of_aircraft = 1
            exp_details.attachment_date = hxd.hx_core.inception_date
            exp_details.expiry_date = hxd.hx_core.expiry_date
            exp_details.hull_ccy = layer_hull.currency.selected
            exp_details.combined_single_limit = layer_liab.limit
            exp_details.liability_ccy = layer_liab.currency.selected  
        elif is_airline:
            ms.pressed_airlines_task = True
            fill_additional_fields(hxd)
            #Add default values for the airlines
            exp_details = hxd.cds.exposure.granular.airlines_default[0]
            layer_hull = hxd.cds.layers[0].coverages.hull
            layer_liab = hxd.cds.layers[0].coverages.liability
            exp_details.no_of_aircraft = 1
            exp_details.attachment_date = hxd.hx_core.inception_date
            exp_details.expiry_date = hxd.hx_core.expiry_date
            if layer_hull.coverage == "Total Loss":
                exp_details.coverage = "TLO"
            else:
                exp_details.coverage  = layer_hull.coverage 
                
            exp_details.hull_limit = layer_hull.limit
            exp_details.hull_excess = layer_hull.excess
            exp_details.hull_ccy = layer_hull.currency.selected
            exp_details.liability_limit = layer_liab.limit
            exp_details.liability_excess = layer_liab.excess
            exp_details.liability_ccy = layer_liab.currency.selected          

        
        # Add status and application date
        hxd.cds.layers[0].status = "Rating"
        hxd.cds.policy_info.application_date = datetime.date.today()

        for layer in hxd.cds.layers:
            for coverage in layer.coverages:
                if coverage[1].section_reference is not None:                                 
                    coverage[1].section_reference = replace_year_in_policy_reference(coverage[1].section_reference, hxd.hx_core.inception_date)



        hxd.cds.standard_fields.is_renewal = True
        # add the Policy Reference to PAS
        hx.meta.pas_references.clear()
        hull_section_ref = hxd.cds.layers[0].coverages.hull.section_reference
        liab_section_ref = hxd.cds.layers[0].coverages.liability.section_reference
        if hull_section_ref is not None:
            hx.meta.pas_references.append(hull_section_ref[:8])
        elif liab_section_ref is not None:
            hx.meta.pas_references.append(liab_section_ref[:8])


        # Force user to press Start Airlines/GA task for UX flow to work        

    except Exception as e:
        ms.landing_page_info = f"❗❗ Failed to fetch expiring data. Please proceed and enter data manually. ❗❗\n\nError for dev team:\n{e}"
        ms.has_import_failed = True
        print(e)
       

@hx.task
def quote_to_excel_task(hxd, progress):

    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/policy_doc_template/combined_aviation_template.xlsx"

    # Load the workbook and select the active worksheet
    workbook = openpyxl.load_workbook(template_path)
    sheet = workbook.active

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for title, coord in cells:
                if title == sheet.title:  # Ensure the named range is in the correct sheet
                    sheet[coord] = value

    # Protect the sheet to prevent changes
    sheet.protection.enable()
    sheet.protection.set_password(c.excel_password)

    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict

def replace_year_in_policy_reference(policy_reference, date):
    """
    Replace the two digits in the policy reference corresponding to the year with the last two digits of the year.

    :param policy_reference: The policy reference string (e.g., "JGM43G25ANVQ").
    :param date: A date object or string in 'YYYY-MM-DD' format.
    :return: The modified policy reference with the year digits replaced.
    """
    # Extract the year from the date
    if isinstance(date, str):
        # Parse the date string
        year = datetime.strptime(date, "%Y-%m-%d").year
    elif hasattr(date, "year"):
        # If it's a date object, extract the year
        year = date.year
    else:
        raise ValueError("Invalid date format. Provide a date object or a string in 'YYYY-MM-DD' format.")

    # Get the last two digits of the year
    year_last_two_digits = str(year)[-2:]

    # Replace the 6th and 7th characters in the policy reference
    modified_reference = policy_reference[:6] + year_last_two_digits + policy_reference[8:]

    return modified_reference

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Marine - Combined Aviation"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)      