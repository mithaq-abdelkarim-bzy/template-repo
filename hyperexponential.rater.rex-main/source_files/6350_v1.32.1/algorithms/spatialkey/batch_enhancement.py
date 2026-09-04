import hx
import requests
import json
import time
import re
import os
import math
import hashlib
import ast
import pandas as pd
import numpy as np
from io import StringIO
from datetime import datetime
import copy
from algorithms.spatialkey.authentication import get_0auth_token
from algorithms.spatialkey.xml_string_generation import get_xml_string
from algorithms.spatialkey.utils import UploadSpatialKeyProgress
from algorithms.spatialkey.geojson_fetch import geojsonLoader
from algorithms.spatialkey.allocate_geojson_region import allocate_to_regions


def strip_data_from_sov(hxd):
    '''
    Extract the wanted columns from the SoV table and convert it into a DataFrame.
    '''
    input_data = [{
        "LocID": row.loc_id,
        "BI TIV": row.tiv_bi,
        "Building TIV": row.tiv_buildings,
        "Contents TIV": row.tiv_contents,
        "Other TIV": row.tiv_other,
        "Total TIV": (row.tiv_bi or 0) + (row.tiv_buildings or 0) + (row.tiv_contents or 0) + (row.tiv_other or 0),
        "City": row.address_dropdown.city,
        "Country": row.address_dropdown.country,
        # "County": row.address_dropdown.county,
        # "StateCode": row.address_dropdown.state,
        "Constr Code": row.constr_code,
        # "Latitude": row.latitude,
        # "Longitude": row.longitude,
        "Sprinklered": row.sprinkler,
        "StreetName": row.street_name,
        "Occupancy": row.industry_occupancy_dropdown.occupancy
    } for row in hxd.schedule.schedule_table]

    df = pd.DataFrame(input_data)

    # Write the hash for status check
    hxd.schedule.small_schedule_workflow.spatial_key_hash = hashlib.sha256(pd.util.hash_pandas_object(df, index=True).values).hexdigest()

    # append zips after status check hash to prevent status change issues when different zips come back from a successful spatial key run    
    county_statecode_df = pd.DataFrame([{"Zip": row.zip, "County": row.address_dropdown.county, "StateCode": row.address_dropdown.state} for row in hxd.schedule.schedule_table])
    df = df.join(county_statecode_df)

    col_names = {"latitude": "Latitude", "longitude": "Longitude"}
    try:
        spatialkey_saved_cols = pd.read_csv("spatialkey_saved_cols.csv")
        spatialkey_saved_cols = spatialkey_saved_cols.rename(col_names, axis=1)
        df = df.join(spatialkey_saved_cols)
    except OSError:
        hxd.spatialkey.fetch_status = f"OSError while reading from spatialkey_saved_cols.csv"
        pass  # columns will be created below anyway
    except FileNotFoundError:
        hxd.spatialkey.fetch_status = f"spatialkey_saved_cols.csv not found"
        pass  # columns will be created below anyway

    for key, val in col_names.items():
        if val not in df.columns:
            df[val] = None

    return df

def strip_data_from_csv(hxd):
    '''
    Extract the wanted columns from the CSV file and convert it into a DataFrame.
    '''

    if hxd.schedule.large_schedule_workflow.load_from_schedule_file:
        with hxd.schedule.large_schedule_workflow.schedule_file.open("b") as f:
            df = pd.read_csv(f)
    elif hxd.schedule.large_schedule_workflow.load_from_em_database:
        with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
            df = pd.read_csv(f)
    else:
        hx.errors.fatal("Please upload the csv file before running spatial key task.")

    if "tiv_other" not in df.columns:
        df["tiv_other"] = 0

    if "tiv_total" not in df.columns:
        df["tiv_total"] = df[["tiv_bi", "tiv_buildings", "tiv_contents", "tiv_other"]].sum(axis=1)

    df = df[["loc_id", "tiv_bi", "tiv_buildings", "tiv_contents", "tiv_other", "tiv_total", "address_dropdown/city",
            "address_dropdown/country", "address_dropdown/county", "address_dropdown/state", "constr_code", "latitude",
            "longitude", "sprinkler", "street_name", "zip", "industry_occupancy_dropdown/occupancy"]]
    

    df.rename(columns={
        "loc_id": "LocID", "tiv_bi": "BI TIV", "tiv_buildings": "Building TIV", "tiv_contents": "Contents TIV", "tiv_other": "Other TIV",
        "tiv_total": "Total TIV", "address_dropdown/city": "City", "address_dropdown/country": "Country", "address_dropdown/county": "County",
        "address_dropdown/state": "StateCode", "constr_code": "Constr Code", "latitude": "Latitude", "longitude": "Longitude", "sprinkler": "Sprinklered",
        "street_name": "StreetName", "zip": "Zip", "industry_occupancy_dropdown/occupancy": "Occupancy"
        }, inplace=True)
    
    return df


def upload_csv_to_sk(hxd, bearer_token, df):
    '''
    Uploads the csv file that stores the dataset into SpatialKey Database
    '''

    # 'upload.json' indicates that the results will be sent back in a JSON format
    url = "https://beazleyuw.spatialkey.com/SpatialKeyFramework/api/v2/upload.json"
    params = {
        "token": bearer_token
    }
    
    f = df.to_csv(index=False)

    # with open("converted_data.csv", "r") as f:
    files = {
        "file": ("converted_data.csv", f, "text/csv")
    }
    response = requests.post(url, params=params, files=files)

    result = response.json()
    return result

def get_models_to_run(countries):
    '''
    Get the model set for analysis based on the countries found inside the data
    '''
    us_models = ["katriskusflood*", "catnetglobalwildfireuw_2024_v1", "femausflood*", "catnetglobalhailuw_2025_v1", "catnetglobaltornadouw_2024_v1"]
    non_us_models = ["catnetglobalhailuw_2025_v1", "catnetglobalwildfireuw_2024_v1", "catnetglobalriverflooduw_2024_v1", "catnetglobalearthquakebedrockuw_2024_v1", "catnetglobaltornadouw_2024_v1", "catnetglobalwinduw_2024_v1"]

    have_us = any(country == "United States" for country in countries)
    have_non_us = any(country != "United States" for country in countries if country != "")

    if have_us and have_non_us:
        models = us_models + non_us_models
    elif have_us:
        models = us_models
    elif have_non_us:
        models = non_us_models
    else:
        models = []
    
    return models

def upload_xml(bearer_token, upload_id):
    '''
    Uses the XML file stored in Renew to describe the dataset structure.
    '''
    url = f"https://beazleyuw.spatialkey.com/SpatialKeyFramework/api/v2/upload/{upload_id}/dataset.json"

    params = {
        "token": bearer_token
    }

    headers = {
        "Content-Type": "application/xml"
        }
    
    # Get the XML string 
    content = get_xml_string()

    # Upload it into SK
    response = requests.post(url, params=params, headers=headers, data=content)
    return response
    
def check_upload_status(bearer_token, upload_id):
    '''
    Gives an update on the upload status for the file.
    '''
    url = f"https://beazleyuw.spatialkey.com/SpatialKeyFramework/api/v2/upload/{upload_id}.json"

    params = {
        "token": bearer_token
    }

    response = requests.get(url, params)

    return response

def run_analysis(bearer_token, upload_id, models_to_run):
    '''
    Runs the Hazard analysis on the dataset. Max 5000 locations (SK Limit)
    The 5K limit is going to be upgraded soon.
    '''
    url = f"https://beazleyuw.spatialkey.com/api/analytics/v3/uw/analysis/{upload_id}.json"

    params = {
        "token": bearer_token
    }

    analysis_json = {
        "exportType" : "CSV",
        "includeEnhancementColumns" : "true",
        "exportShortenColumnNames" : "true",
        "exportColumns" : ["locid"],
        "formattedColumns" : ["sk_country_code"],
        "modelsToRun" : models_to_run,
        }

    headers = {
        "Content-Type": "application/json"
        }
    
    response = requests.post(url, params=params, headers=headers, data=str(analysis_json))
    return response

def check_analysis_status(bearer_token, job_id):
    '''
    Gets the analysis status
    '''
    url = f"https://beazleyuw.spatialkey.com/api/analytics/v3/job/{job_id}/status"

    params = {
        "token": bearer_token
    }

    response = requests.get(url, params=params)
    return response

def get_sk_output_data(bearer_token, url):
    '''
    Get the raw CSV output data from SpatialKey
    '''
    params = {
        "token": bearer_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.text
    else:
        hx.errors.fatal(f"Download error ({response.status_code})")

def extract_numbers(sentence):
    '''
    Returns a list of numbers found inside a string
    '''
    list_of_numbers = re.findall(r'\d+\.\d+|\d+', sentence)
    return list_of_numbers

def assign_sk_data(hxd, df, models_to_run, has_timed_out):
    '''
    Set the SK output data back to the SoV using setattr.
    '''
    # Column name mapping to schedule data schema
    columns_to_hxd_names = {
        "locid": "loc_id",
        "sk_postal_code": "zip",
        "point_latitude": "latitude",
        "point_longitude": "longitude",
        "global_catnet_wildfire_intensity": "catnet_score_wf",
        "global_catnet_tornado_frequency_range": "catnet_score_tn",
        "us_katrisk_flood_score": "katrisk_score_fl", 
        "us_fema_flood": "fema_flood",  
        "us_fema_flood_risk": "fema_flood_risk", 
        "us_fema_flood_zone": "fema_flood_zone", 
        "us_fema_flood_subzone": "fema_flood_subzone", 
        "us_fema_flood_combinedzone": "fema_flood_combined_zone",
        "global_catnet_hail_description": "catnet_score_ha", 
        "global_catnet_wind_peak_gust_range": "catnet_score_ws",
        "global_catnet_river_return_period": "catnet_score_fl", 
        # "global_catnet_river_flood_intensity": "river_flood_intensity", 
        "global_catnet_seismic_hazard_psa_range": "catnet_score_eq",
        "eq_crit_cat_zone": "eq_crit_cat_zone",
        "ws_crit_cat_zone": "ws_crit_cat_zone"
    }

    # Expected columns within output data for respective models
    # Removed any columns that we don't want to get data from
    model_outputs = {
        "catnetglobalwildfireuw_2024_v1": ["global_catnet_wildfire_intensity"],
        "catnetglobaltornadouw_2024_v1": ["global_catnet_tornado_frequency_range"],
        "katriskusflood*": ["us_katrisk_flood_score"],
        "femausflood*": ["us_fema_flood", "us_fema_flood_risk", "us_fema_flood_zone","us_fema_flood_subzone", "us_fema_flood_combinedzone"],
        "catnetglobalhailuw_2025_v1": ["global_catnet_hail_description"],
        "catnetglobalwinduw_2024_v1": ["global_catnet_wind_peak_gust_range"],
        "catnetglobalriverflooduw_2024_v1": ["global_catnet_river_return_period"],
        "catnetglobalearthquakebedrockuw_2024_v1": ["global_catnet_seismic_hazard_psa_range"],
    }

    # Get the columns we need to extract from the data
    column_names = ["locid", "sk_postal_code", "point_latitude", "point_longitude", "eq_crit_cat_zone", "ws_crit_cat_zone"] # Always keep locid for referencing back to the hxd
    for model in models_to_run:
        column_names += model_outputs[model]
    
    # Get the subset we are interested in
    output_df = df[df.columns[df.columns.isin(column_names)]]
    
    # Change all the NaN values into None
    output_df = output_df.where(pd.notnull(output_df), None)
    output_df = output_df.replace({np.nan: None})  #IR changed , to :

    # Change locid column into a string
    output_df["locid"] = output_df["locid"].astype('str')

    # Rejoin lat/long and zip cols if they were null in spatialkey
    output_df = rejoin_saved_cols(hxd, output_df)


    if hxd.policy_information.large_schedule_model:
        df.rename(columns=columns_to_hxd_names, inplace=True)
        if not has_timed_out:
            df["zip"] = df["zip"].astype('Int64').astype("str").str.zfill(5)  # Ensure zip strings are read in correctly
        
        with hxd.schedule.spatial_key_file.open("b") as f:
            df.to_csv(f)
        hxd.schedule.large_schedule_workflow.spatial_key_updated = True
    else:
        output_dict = output_df.to_dict("records")
        for index, layer in enumerate(hxd.schedule.schedule_table):
            row = output_dict[index]
                # Only write back the longitude and latitude, keep the zip as entered...
            for column in column_names[2:]:
                # column refers to the sk output original column name
                hxd_node_name = columns_to_hxd_names[column]
                value = row[column]

                if type(value) == str or value is None or not math.isnan(value):

                    # Edge case for katrisk_score_fl
                    if hxd_node_name in {"katrisk_score_fl", "catnet_score_fl", "zip"}:
                        try:
                            value = int(float(row[column]))
                        except:
                            value = row[column]
                    
                    # Remapping for zip
                    if hxd_node_name == "zip" and value and not isinstance(value, str):
                        value = "{:05d}".format(value)

                    if hxd_node_name == "zip" and value and isinstance(value, str):
                        zero_padding = max(5-len(value), 0) * "0"
                        value = zero_padding + value

                    if hxd_node_name == "zip" and not value:
                        value = "00000"

                    # Map floodzone alongside fema_flood_zone
                    if hxd_node_name == "fema_flood_zone":
                        setattr(layer, "floodzone", value)
                            
                    setattr(layer, hxd_node_name, value)


def step_2(hxd, bearer_token, input_df):
    '''
    Running through the Step 2 workflow for SpatialKey with error catching
    If upload succesful, returns the upload_id for the csv upload
    Otherwise, sends an error message
    '''
    # Try MAX 3 times to upload the file
    for i in range(3):
        if not input_df.empty:
            results = upload_csv_to_sk(hxd, bearer_token, input_df)
        else:
            hx.errors.fatal("Input CSV file was not found.")

        # Get the upload ID for the file
        upload_id = results.get('upload', {}).get('uploadId', "")
        errors = results.get('upload', {}).get('errors', None)

        # We want it to exit if we get a functional upload ID and with no errors.
        if errors == None and upload_id != "":
            return upload_id
        
    # Throw an error message after max attempts
    hx.errors.fatal(f"Upload fail - Error: {errors}")

def step_4(bearer_token, upload_id, time_end):
    '''
    Runs through the Step 4 workflow for SpatialKey with error catching.
    Returns the status of the upload.
    '''
    # Check the status for the first time
    response = check_upload_status(bearer_token, upload_id)
    result = response.json()
    status = result.get("status", "")

    # It is expected that status == "IMPORT_PROCESSING" if no error is found during upload
    while status == "IMPORT_PROCESSING" or status == "IMPORT_VALIDATING":
        if time.time() >= time_end:
            return "timed_out"
        time.sleep(5)

        response = check_upload_status(bearer_token, upload_id)
        result = response.json()
        status = result.get("status", "")
    
    return result

def step_6(bearer_token, job_id, time_end):
    '''
    Run the Step 6 workflow for SpatialKey with error catching
    If successful, return file download url
    Otherwise, throw an error after 3 tries
    '''
    for i in range(3):
        if time.time() >= time_end:
            return "timed_out"

        # Poll for the first time
        response = check_analysis_status(bearer_token, job_id)
        result = json.loads(response.text)
        status = result.get("status", "")

        while status == "PROCESSING" or status == "WAITING":
            if time.time() >= time_end:
                return "timed_out"
            time.sleep(5) # Wait for 5 seconds

            response = check_analysis_status(bearer_token, job_id)
            result = json.loads(response.text)
            status = result.get("status", "")

        if status == "COMPLETED": # Exit condition
            file_download_url = result.get("file", "")
            return file_download_url
        elif i == 3: # Error catch
            errors = result.get("errors", None)
            hx.errors.fatal(f"Analysis Error ({status}): {errors}")

def time_out(current_time, time_end):
    '''
    Checks if the code has reached the time limit. 
    If TRUE, return an error and stop async task.
    '''
    if current_time >= time_end:
        hx.errors.fatal("TIME OUT")

def run_batch_enhancement(hxd, progress):
    '''
    Runs through the entire workflow to get SpatialKey to work in hx Renew.
    '''

    # CAT Zone Load parameter tables
    us_cat_limit_zones = copy.deepcopy(hx.params.us_cat_limit_zones)
    intl_cat_limit_zones = copy.deepcopy(hx.params.intl_cat_limit_zones)

    # Step 0 - Create progress object, number of dfs to loop through currently unknown
    progress_status = UploadSpatialKeyProgress(hxd, progress, num_stages=7)
    progress_status.update() # call update so we get placeholder text

    # Step 1 - Authentication
    bearer_token = get_0auth_token()

    # Get the SoV data
    if hxd.policy_information.small_schedule_model:
        df = strip_data_from_sov(hxd)
    else:
        df = strip_data_from_csv(hxd)

    # Check for type of models
    unique_countries = df["Country"].unique()
    models_to_run = get_models_to_run(unique_countries)

    if models_to_run == []:
        hx.errors.fatal("No country data found")

    table_spatialkey_hazard_scores = hx.params.spatialkey_hazard_scores

    # Load your dataframe into a pandas dataframe named df
    MAX_ROW_LIMIT = 5000
    num_of_groups = math.ceil(len(df) / MAX_ROW_LIMIT)
    num_of_rows = math.ceil(len(df) / num_of_groups)
    input_dfs = [df[i:i+num_of_rows] for i in range(0, len(df), num_of_rows)]
    
    # set the number of dfs since we know it and update the progress
    progress_status.set_num_dfs(len(input_dfs))
    progress_status.set_num_rows(len(df))
    progress_status.update()

    output_dfs = []
    for index, input_df in enumerate(input_dfs):
        # Timeout limit for 5 minutes (Step 2 - 4)
        time_end = time.time() + (60 * 5)
        
        # initialise variable to test if Step 6 times out at any point.
        has_timed_out = False
        
        progress_status.update()
        # Restart process from Step 2 if Step 4 fails - MAX 3 ATTEMPTS
        for i in range(3):
            # Step 2 - Upload the Schedule data

            upload_id = step_2(hxd, bearer_token, input_df)

            # Step 3 - Upload XML file
            response = upload_xml(bearer_token, upload_id)

            progress_status.update()
            # Step 4 - Check import status until it's complete
            if has_timed_out:
                results = "timed_out"
            else:
                results = step_4(bearer_token, upload_id, time_end)

                #keep track of how many records have gone to SK already
                if results == "timed_out":
                    sk_records = index * 5000
                    proxy_score_records = len(df) - sk_records

            progress_status.update()
            if results == "timed_out":
                # once process has timed out once, use the hazard scores replacement for all subsequent input_df
                has_timed_out = True
            else:
                status = results.get("status", "")
                errors = results.get("errors", None)

                if status == "IMPORT_COMPLETE_CLEAN": # Exit condition - Success
                    hxd.spatialkey.dataset_id = results["createdResources"][0]["id"]
                    break
                elif i == 3: # Error condition
                    hx.errors.fatal(f"IMPORT ERROR ({status}): {errors}")
        
        progress_status.update()
        # this step will fall over if SK has already timed out
        if has_timed_out == False:
            # Step 5 - Running the analysis
            response = run_analysis(bearer_token, upload_id, models_to_run)
            analysis_result = json.loads(response.text)
            job_id = analysis_result.get("job", {}).get("jobId", "")
            hxd.spatialkey.job_id = job_id

        # Step 6 - Poll the analysis status
        # Timeout limit for 20 minutes (Step 6 only)
        progress_status.update()
        time_end = time.time() + (60 * 20)

        if has_timed_out:
            file_download_url = "timed_out"
        else:
            file_download_url = step_6(bearer_token, job_id, time_end)

            # calculate variables to be used for status message
            if file_download_url == "timed_out":
                sk_records = index * 5000
                proxy_score_records = len(df) - sk_records

        if not file_download_url:
            hxd.spatialkey.fetch_status = "No data points applied to SpatialKey"
            return

        # Step 7 - Download the SK data or use proxy scores for US locations when SK taking too long
        progress_status.update()
        if file_download_url == "timed_out":
            # once process has timed out once, use the hazard scores replacement for all subsequent input_df
            has_timed_out = True

            column_names = {
                "locid",
                "sk_postal_code",
                "point_latitude",
                "point_longitude",
                "global_catnet_wildfire_intensity",
                "global_catnet_tornado_frequency_range",
                "us_katrisk_flood_score",
                "us_fema_flood", 
                "us_fema_flood_risk",
                "us_fema_flood_zone",
                "us_fema_flood_subzone",
                "us_fema_flood_combinedzone",
                "global_catnet_hail_description",
                "global_catnet_wind_peak_gust_range",
                "global_catnet_river_return_period",
                # "global_catnet_river_flood_intensity",
                "global_catnet_seismic_hazard_psa_range"
                }

            output_df = pd.DataFrame(columns=column_names)

            # add a country column to ensure only US zips are mapped and not any other countries with equivalent zips
            table_spatialkey_hazard_scores["Country"] = "United States"
            temp_df = input_df.merge(table_spatialkey_hazard_scores, how = "left", left_on = ["Country","Zip"], right_on = ["Country","Zip"])

            output_df["sk_postal_code"] = temp_df["Zip"]
            output_df["us_katrisk_flood_score"] = temp_df["Flood"]
            output_df["global_catnet_hail_description"] = temp_df["Hail"]
            output_df["global_catnet_wildfire_intensity"] = temp_df["Wildfire"]
            output_df["global_catnet_tornado_frequency_range"] = temp_df["Tornado"]

            if hxd.policy_information.large_schedule_model:
                hxd.spatialkey.fetch_status = f"SpatialKey timed out after {sk_records} data points, applied proxy scores to {proxy_score_records} data points in csv file"
            else:    
                hxd.spatialkey.fetch_status = f"SpatialKey timed out after {sk_records} data points, applied proxy scores to {proxy_score_records} data points in schedule table"

        else:
            output_data = get_sk_output_data(bearer_token, file_download_url)
            output_df = pd.read_csv(StringIO(output_data))

            output_df = remap_sk_output(output_df)

            if hxd.policy_information.large_schedule_model:
                hxd.spatialkey.fetch_status = f"Applied SpatialKey to {len(df)} data points in csv file"
            else:    
                hxd.spatialkey.fetch_status = f"Applied SpatialKey to {len(df)} data points in schedule table"

        output_dfs.append(output_df)
        progress_status.update()

    final_df = pd.concat(output_dfs).reset_index(drop=True)

    # Step 8 - Assign CAT Zones
    final_df = assign_cat_zone(hxd, df, final_df, us_cat_limit_zones, intl_cat_limit_zones)

    # Step 9 - Assign data back to hxd
    assign_sk_data(hxd, final_df, models_to_run, has_timed_out)
    progress_status.finish()  # progress ends

def remap_sk_output(final_df):
    # Remapping EQ scoring (PGA -> PSA bands)
    if "global_catnet_seismic_hazard_pga" in final_df.columns:
        eq_mapping = hx.params.eq_catnet_mapping_table
        breaks = eq_mapping["low_pga"].append(pd.Series([float("inf")]), ignore_index = True)
        bin_labels = eq_mapping["label_psa"][0:len(eq_mapping["label_psa"])]
        final_df["global_catnet_seismic_hazard_psa_range"] = pd.cut(x = pd.to_numeric(final_df["global_catnet_seismic_hazard_pga"], errors="coerce"), bins = breaks, labels = bin_labels, include_lowest = True).astype("object")

    if "global_catnet_tornado_frequency_range" in final_df.columns:
        final_df["global_catnet_tornado_frequency_range"] = final_df["global_catnet_tornado_frequency_range"].fillna("No Data")

    if "global_catnet_river_return_period" in final_df.columns:
        fl_mapping = hx.params.fl_catnet_mapping_table
        final_df.rename(columns={"global_catnet_river_return_period": "sk_fl_catnet_level"}, inplace = True)
        final_df["sk_fl_catnet_level"] = np.where(pd.isnull(final_df["sk_fl_catnet_level"]), final_df["sk_fl_catnet_level"], final_df["sk_fl_catnet_level"].astype("str"))
        final_df = final_df.merge(fl_mapping, how = "left", on = "sk_fl_catnet_level")
        final_df.rename(columns={"rater_fl_catnet_level": "global_catnet_river_return_period"}, inplace = True)
        final_df["global_catnet_river_return_period"] = final_df["global_catnet_river_return_period"].fillna(final_df["sk_fl_catnet_level"])

    if "global_catnet_wind_peak_gust_range" in final_df.columns:
        ws_mapping = hx.params.ws_catnet_mapping_table
        final_df.rename(columns={"global_catnet_wind_peak_gust_range": "sk_ws_catnet_level"}, inplace = True)
        final_df["sk_ws_catnet_level"] = np.where(pd.isnull(final_df["sk_ws_catnet_level"]), final_df["sk_ws_catnet_level"], final_df["sk_ws_catnet_level"].astype("str"))
        final_df = final_df.merge(ws_mapping, how = "left", on = "sk_ws_catnet_level")
        final_df.rename(columns={"rater_ws_catnet_level": "global_catnet_wind_peak_gust_range"}, inplace = True)
        final_df["global_catnet_wind_peak_gust_range"] = final_df["global_catnet_wind_peak_gust_range"].fillna(final_df["sk_ws_catnet_level"])

    return final_df

def check_dataset_valid(hxd, bearer_token, dataset_id):
    '''
    Check whether Dataset is available/valid within SpatialKey
    '''
    url = f"https://beazleyuw.spatialkey.com/api/dataset/v1/{dataset_id}.json"

    headers = {
        "x-sktoken": bearer_token
    }

    response = requests.get(url, headers=headers)
    
    
    if response.status_code == 200: 
        result = response.json()
        expired_date_object = datetime.strptime(result["dateExpired"], "%Y-%m-%d %H:%M:%S:%f %Z")
        return expired_date_object > datetime.now()
    else:
        hx.errors.fatal(f"Error validating dataset id - {dataset_id}")
    

def open_spatialkey_dashboard(hxd, progress):

    #Obtain authorisation
    bearer_token = get_0auth_token()

    #Check required job_id available and dataset_id still valid
    if not hxd.spatialkey.job_id:
        hxd.spatialkey.dashboard_note = "No valid SpatialKey data found - please upload data to SpatialKey"
        return
    elif not check_dataset_valid(hxd, bearer_token, hxd.spatialkey.dataset_id):
        hxd.spatialkey.dashboard_note = "SpatialKey Dataset Expired - please reupload data to SpatialKey"
        return

    #Create URL for embedding
    url = f"https://beazleyuw.spatialkey.com?appID=underwriting3&allowHome=false&processingID={hxd.spatialkey.job_id}&oAuthToken={bearer_token}"

    #Set note with url
    hxd.spatialkey.dashboard_note = f"[SpatialKey dashboard link]({url})\n(Refresh link before each use)"


def rejoin_saved_cols(hxd, df):
    if hxd.policy_information.small_schedule_model:
        col_names = {"latitude": "original_latitude", "longitude": "original_longitude"}
        
        try:
            spatialkey_saved_cols = pd.read_csv("spatialkey_saved_cols.csv")
            spatialkey_saved_cols = spatialkey_saved_cols.rename(col_names, axis=1)
            df = df.join(spatialkey_saved_cols)
        except OSError:
            hxd.spatialkey.fetch_status = f"OSError while reading from spatialkey_saved_cols.csv"
            pass  # columns will be created below anyway
        except FileNotFoundError:
            hxd.spatialkey.fetch_status = f"spatialkey_saved_cols.csv not found"
            pass  # columns will be created below anyway

        for key, val in col_names.items():
            if val not in df.columns:
                df[val] = None


        df["point_latitude"] = df["point_latitude"].fillna(df["original_latitude"])
        df = df.drop("original_latitude", axis=1)

        df["point_longitude"] = df["point_longitude"].fillna(df["original_longitude"])
        df = df.drop("original_longitude", axis=1)
        
    else:
        if hxd.schedule.large_schedule_workflow.load_from_schedule_file:
            with hxd.schedule.large_schedule_workflow.schedule_file.open("b") as f:
                original_df = pd.read_csv(f)
        elif hxd.schedule.large_schedule_workflow.load_from_em_database:
            with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
                original_df = pd.read_csv(f)

        original_df = original_df[['zip', 'latitude', 'longitude']]
        df["sk_postal_code"] = df["sk_postal_code"].fillna(original_df["zip"])
        df["point_latitude"] = df["point_latitude"].fillna(original_df["latitude"])
        df["point_longitude"] = df["point_longitude"].fillna(original_df["longitude"])

    return df


def assign_cat_zone(hxd, df, final_df, us_cat_limit_zones, intl_cat_limit_zones):

    # Attach Latitudes And Longitudes
    df = df[["Country", "StateCode", "County"]].assign(
        Latitude=final_df["point_latitude"],
        Longitude=final_df["point_longitude"]
    )

    # Attach Intl CAT Zone - Single Countries
    df = df.merge(intl_cat_limit_zones, left_on="Country", right_on = "country", how="left")
    df["is_eq_multi"] = df["is_eq_multi"].fillna(False)
    df["is_ws_multi"] = df["is_ws_multi"].fillna(False)
    df["intl_eq_cat_limit_zone"] = df["intl_eq_cat_limit_zone"].fillna(0)
    df["intl_ws_cat_limit_zone"] = df["intl_ws_cat_limit_zone"].fillna(0)

    # Load in the geojsons for Intl-Multi Regions
    load_geojson = geojsonLoader()
    eq_multi_cat_limit_zones = load_geojson.download_geojson_from_sharepoint("eq_multi_cat_limit_zones.geojson")
    ws_multi_cat_limit_zones = load_geojson.download_geojson_from_sharepoint("ws_multi_cat_limit_zones.geojson")

    # Apply multi zones based on lat longs 
    df['intl_eq_multi_eq_cat_limit_zone'] = allocate_to_regions(df['Longitude'], df['Latitude'], eq_multi_cat_limit_zones, region_property='cat_zone', process= df['is_eq_multi']) 
    df['intl_ws_multi_eq_cat_limit_zone'] = allocate_to_regions(df['Longitude'], df['Latitude'], ws_multi_cat_limit_zones, region_property='cat_zone', process= df['is_ws_multi']) 

    # Convert US counties to lower case for better matching
    us_cat_limit_zones["state_county_lowercase"] = us_cat_limit_zones["state_county"].str.lower()
    df["state_county_lowercase"] = df["StateCode"].str.lower() + df["County"].str.lower()

    # Attach US CAT Zones
    df = df.merge(us_cat_limit_zones, on="state_county_lowercase", how="left")
    df["us_eq_cat_limit_zone"] = df["us_eq_cat_limit_zone"].fillna(0)
    df["us_ws_cat_limit_zone"] = df["us_ws_cat_limit_zone"].fillna(0)

    # Assign final Cat Zones
    df['eq_crit_cat_zone_final'] = np.where(
        df['Country'] == 'United States',
        df["us_eq_cat_limit_zone"],
        np.where(
            ~df["is_eq_multi"],
            df["intl_eq_cat_limit_zone"],
            df['intl_eq_multi_eq_cat_limit_zone']
        )
    )

    df['ws_crit_cat_zone_final'] = np.where(
        df['Country'] == 'United States',
        df["us_ws_cat_limit_zone"],
        np.where(
            ~df["is_ws_multi"],
            df["intl_ws_cat_limit_zone"],
            df['intl_ws_multi_eq_cat_limit_zone']
        )
    )
    # Fill Nones (where no crit limit defined) as 3s
    df['eq_crit_cat_zone_final'] = (pd.to_numeric(df['eq_crit_cat_zone_final'], errors='coerce').fillna(3).astype(int))
    df['ws_crit_cat_zone_final'] = (pd.to_numeric(df['ws_crit_cat_zone_final'], errors='coerce').fillna(3).astype(int))

    # Assign Appropriate CAT Zone
    # US - by state by zone
    # Intl - by country by zone
    mask_us = df["Country"] == "United States"

    df["eq_crit_cat_zone"] = (df["StateCode"] + " - CAT Zone " + df["eq_crit_cat_zone_final"].astype(str)).where(
        mask_us, df["Country"] + " - CAT Zone " + df["eq_crit_cat_zone_final"].astype(str)
    )

    df["ws_crit_cat_zone"] = (df["StateCode"] + " - CAT Zone " + df["ws_crit_cat_zone_final"].astype(str)).where(
        mask_us, df["Country"] + " - CAT Zone " + df["ws_crit_cat_zone_final"].astype(str)
    )

    final_df = final_df.assign(
        eq_crit_cat_zone = df["eq_crit_cat_zone"],
        ws_crit_cat_zone = df["ws_crit_cat_zone"]
    )

    return final_df
