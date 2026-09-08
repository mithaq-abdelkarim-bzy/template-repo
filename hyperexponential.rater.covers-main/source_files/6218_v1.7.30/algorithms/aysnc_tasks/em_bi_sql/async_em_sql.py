import hx
import pyodbc
from datetime import datetime
import polars as pl
import pandas as pd
from algorithms.rate_common_rating_functions import join_param_table


def search_exposure_management_data(hxd, progress):
   
    
    hxd.cds.exposure_management_api.binder_reference_to_search =  hxd.cds.standard_fields.facility_reference

   
    
    binder_reference = hxd.cds.standard_fields.facility_reference[:6]
   
    filter_binder_reference = "" if binder_reference else "--"

    # KM - Code dependent on changes to the exposure management DB - if they sort the data duplication issue, code can go back to the below:
    # # Query location table first
    # query = f"""
    #     SELECT
    #         "YearMonth",
    #         "PORTNUM",
    #         "PORTNAME",
    #         COUNT(*) AS num_locs
    #     FROM Property_data.dbo.vw_covers_rater_data
    #         WHERE 1=1
    #         {filter_binder_name}  AND "PORTNAME" LIKE '%{str(binder_name).replace("'","''")}%'
    #         {filter_binder_reference} AND PORTNUM LIKE '%{str(binder_reference).replace("'","''")}%'
    #     GROUP BY
    #         "YearMonth",
    #         "PORTNUM",
    #         "PORTNAME"
    # """

    query = f"""
        WITH CTE AS (
            SELECT *,
                ROW_NUMBER() OVER (PARTITION BY PORTNUM,ACCGRPNUM , locid ORDER BY PORTNUM,ACCGRPNUM , locid) AS row_num
            FROM [Property_data].[dbo].[vw_covers_rater_data]
        )
        SELECT
            "YearMonth",
            "PORTNUM",
            "PORTNAME",
            COUNT(*) AS num_locs
        FROM CTE
            WHERE row_num = 1
          
            {filter_binder_reference} AND PORTNUM LIKE '%{str(binder_reference).replace("'","''")}%'
        GROUP BY
            "YearMonth",
            "PORTNUM",
            "PORTNAME"
    """


    search_db_pl, successful = query_exposure_management_database(hxd, progress, query, "search_fetch_status", limit=hxd.cds.exposure_management_api.limit_results)
    
    if successful:
        hxd.cds.exposure_management_api.search_results = search_db_pl.rename({
            "YearMonth": "binder_date",
            "PORTNUM": "binder_reference",
            "PORTNAME": "binder_name",
        })[[
                "binder_date",
                "binder_reference",
                "binder_name",
                "num_locs"
            ]].to_dicts()



def pull_in_exposure_management_data(hxd, progress):

    rows_selected = 0

    #---------------------for debugging only-----------------#  
    # rows_selected = 1  
    #------------------------------------------------------------#

    binder_names_agg = ""
    binder_reference_agg = ""
    
    search_results_df = hxd.cds.exposure_management_api.search_results

    
    for index , binder in enumerate(search_results_df, start =1):
        if binder.selected and not (binder.binder_name is None and binder.binder_reference is None and binder.num_locs is None):
            rows_selected += 1

            binder_reference = binder.binder_reference
            binder_name = binder.binder_name

            binder_reference_str = f"""'{str(binder_reference).replace("'","''")}'""" if binder_reference else "IS NULL"
            binder_name_str = f"""'{str(binder_name).replace("'","''")}'""" if binder_name else "IS NULL"

            if binder_names_agg and binder_reference_agg:
                binder_names_agg += ", "
                binder_reference_agg += ", "
            binder_names_agg += binder_name_str
            binder_reference_agg += binder_reference_str

    
            if binder_names_agg.endswith(", ") and binder_reference_agg.endswith(", "):
                binder_names_agg = binder_names_agg[:-2]
                binder_reference_agg = binder_reference_agg[:-2]
        
    #---------------------for debugging only-----------------#    
    # binder_names_agg = "('JOHNSON & JOHNSON INC')"
    # binder_reference_agg = "('B8220L24ANFT')"

    # binder_names_agg = "('BHI DIGITAL LLC Quake')"
    # binder_reference_agg = "('B8139Z24CNF4')"
    #------------------------------------------------------------#

            binder_names_agg = f"({binder_names_agg})"
            binder_reference_agg = f"({binder_reference_agg})"
        

    if rows_selected == 0:
        hxd.cds.exposure_management_api.location_fetch_status = "No policies selected"
    else:
        # KM - Code dependent on changes to the exposure management DB - if they sort the data duplication issue, code can go back to the below:
        # query = f"""
        #     SELECT
        #         *
        #     FROM property_data.dbo.vw_covers_rater_data vlp WITH (NOLOCK)
        #     WHERE 1=1
        #         AND PORTNUM IN {binder_reference_agg}
        #         AND PORTNAME IN {binder_names_agg}
        # """

        query = f"""
WITH cte AS (
    SELECT
        [PORTNUM],
        [ACCGRPNUM],
        locid,
        [PORTNAME],
        CASE
            WHEN [Policy Type] IN ('New', 'Renewal') THEN [Policy Type]
            ELSE 'New'
        END AS [Policy Type],
        ROW_NUMBER() OVER (
            PARTITION BY portnum, accgrpnum, locid
            ORDER BY portnum, accgrpnum, locid
        ) AS row_num
		,[YearMonth]
      ,[PORTINFOID]
      ,[ACCGRPNAME]
      ,[SignedLine Value used for calc]
      ,[INCEPTDATE]
      ,[EXPIREDATE]
      ,[LOCNUM]
      ,[Lineage]
      ,[Lineage Risk Number]
      ,[StreetAddress]
      ,[CityName]
      ,[PostalCode]
      ,[State]
      ,[County]
      ,[CountryCode]
      ,[latitude]
      ,[longitude]
      ,[Policy Wind Cover]
      ,[Policy Quake Cover]
      ,[Policy SCS Cover]
      ,[Policy AOP Cover]
      ,[Policy Flood Cover]
      ,[Policy Terror Cover]
      ,[Location Wind Cover]
      ,[Location Quake Cover]
      ,[Location SCS Cover]
      ,[Location AOP Cover]
      ,[Location Flood Cover]
      ,[Location Terror Cover]
      ,[Ceded Account Premium]
      ,[AFB Account Premium]
      ,[SignedLine]
      ,[AFB share/SignedLine]
      ,[Wind Limit]
      ,[Wind Excess]
      ,[Wind Account Deductible]
      ,[Wind Location Deductible]
      ,[Quake Limit]
      ,[Quake Excess]
      ,[Quake Account Deductible]
      ,[Quake Location Deductible]
      ,[SCS Limit]
      ,[SCS Excess]
      ,[SCS Account Deductible]
      ,[SCS Location Deductible]
      ,[AOP Limit]
      ,[AOP Excess]
      ,[AOP Account Deductible]
      ,[AOP Location Deductible]
      ,[Buildings]
      ,[Contents]
      ,[BI]
      ,[coverageid_max]
      ,[coverageid_min]
      ,[coverageid_count]
      ,[Buildings_eq]
      ,[Contents_eq]
      ,[BI_eq]
      ,[Buildings_ws]
      ,[Contents_ws]
      ,[BI_ws]
      ,[TIV_eq]
      ,[TIV_ws]
      ,[TIV_aop]
      ,[Beazley Gate]
      ,[Beazley Gate Description]
      ,[PPC]
      ,[Sprinkler]
      ,[Wind Beazley Location AAL Gross Loss]
      ,[Wind Beazley Location StdDev Gross Loss]
      ,[Quake Beazley Location AAL Gross Loss]
      ,[Quake Beazley Location StdDev Gross Loss]
      ,[All Perils Beazley Location StdDev Gross Loss]
      ,[Wind Beazley Account AAL Gross Loss]
      ,[Wind Beazley Account StdDev Gross Loss]
      ,[Quake Beazley Account AAL Gross Loss]
      ,[Quake Beazley Account StdDev Gross Loss]
      ,[All Perils Beazley Account StdDev Gross Loss]
      ,[Account Contribution to 1 in 250 for Property + Treaty All Perils]
      ,[Account Contribution to 1 in 10 for Property + Treaty All Perils]
      ,[California Earthquake - Los Angeles (15022534)]
      ,[California Earthquake - San Francisco (15006191)]
      ,[New Madrid Earthquake (15355285)]
      ,[New Madrid Extreme Stress Event (15387653)]
      ,[PNW Earthquake (15100131)]
      ,[Florida Windstorm #1 - Miami-Dade (2865409)]
      ,[Florida Windstorm #2 - Pinellas Hurricane (2869298)]
      ,[USA Windstorm Gulf of Mexico (2848918)]
      ,[Carolinas Windstorm immediately following NE Windstorm (2867710)]
      ,[North East Windstorm (2874165)]
      ,[BLDGSCHEME]
      ,[BLDGCLASS]
      ,[OCCSCHEME]
      ,[OCCTYPE]
      ,[YEARBUILT]
      ,[NUMSTORIES]
      ,[FLOORAREA]
      ,[DISTCOAST]
      ,[YEARUPGRAD]
      ,[ROOFAGE]
      ,[ROOFGEOM]
      ,[ROOFSYS]
      ,[zone1]
      ,[zone2]
    FROM Property_data.dbo.vw_covers_rater_data
)
SELECT *
FROM cte
WHERE row_num = 1
                AND PORTNUM IN {binder_reference_agg}
                AND PORTNAME IN {binder_names_agg}
        """


        location_db_pl, successful = query_exposure_management_database(hxd, progress, query, "location_fetch_status")

        if successful:

            location_db_pl = map_columns(location_db_pl, hxd)
            location_db_pl_dicts = location_db_pl
            location_dicts = location_db_pl_dicts.to_dicts()

            structured_location_dicts = []
            for ld in location_dicts:
                ld["address_dropdown"] = {"city": ld['address_dropdown/city'], "county": ld['address_dropdown/county'], "state": ld['address_dropdown/state'], "country": ld['address_dropdown/country']}
                ld["industry_occupancy_dropdown"] = {"industry": ld['industry_occupancy_dropdown/industry'], "occupancy": ld['industry_occupancy_dropdown/occupancy']}
                structured_location_dicts.append({key: ld[key] for key in ld if (('address_dropdown/' not in key) and ('industry_occupancy_dropdown/' not in key))})


            hxd.cds.exposure.granular.schedule_table = structured_location_dicts
            hxd.cds.exposure.granular.sov_total.num_locs = len(structured_location_dicts)



def query_exposure_management_database(hxd, progress, query, status_object=None, use_pandas=False, limit=None):

    # fetch_status = getattr(hxd.exposure_management_api, status_object)
    if status_object:
        setattr(hxd.cds.exposure_management_api, status_object, "Fetching from SQL...")# + "\n" + query
    progress.update(0)

    if "dev" in hx.secrets.environment_name.lower() or "tst" in hx.secrets.environment_name.lower(): 
        host = hx.secrets.exposuremanagement_host_uat
        user = hx.secrets.exposuremanagement_login_uat
        pwd = hx.secrets.exposuremanagement_password_uat
    else:
        host = hx.secrets.exposuremanagement_host_prd
        user = hx.secrets.exposuremanagement_login_prd
        pwd = hx.secrets.exposuremanagement_password_prd


    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER={' + host + '};DATABASE=Property_data;UID=' + user + ';PWD=' + pwd, timeout=30)


    # Setting up a cursor is the idiomatic way of maintaining the connection
    cursor = cnxn.cursor()

    # Fetch data
    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        if status_object:
            setattr(hxd.cds.exposure_management_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query
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
            setattr(hxd.cds.exposure_management_api, status_object, f"{len(rows)} rows fetched")# + "\n" + query

    return df, True


def map_columns(df, hxd):
    df = df.rename(columns_rename())
    df = bordereau_table_calc(df, hxd)
    df = set_lookup_columns(df)
    df = df.drop(extra_columns())
    df = clean_state_county(hxd, df)

    return df

def columns_rename():
    return {
        "YearMonth": "last_updated",
        "locid": "loc_id",
        "ACCGRPNAME": "acc_name",
        "ACCGRPNUM": "acc_number",
        "INCEPTDATE": "inception_date",
        "EXPIREDATE": "expiry_date",
        "Policy Type": "new_renewal", 
        "StreetAddress": "street_address",
        "CityName": "address_dropdown/city",
        "PostalCode": "zip",
        "State": "address_dropdown/state",
        "County": "address_dropdown/county",
        "CountryCode": "address_dropdown/country",
        "latitude": "latitude",
        "longitude": "longitude",
        "Location Wind Cover": "loc_ws_covered",
        "Location Quake Cover": "loc_eq_covered",
        "Location SCS Cover": "loc_scs_covered",
        "Location AOP Cover": "loc_aop_covered",
        "AFB share/SignedLine": "ceded_share",
        "All Perils Beazley Account StdDev Gross Loss": "acc_all_perils_gg_sd",
        "Wind Beazley Location AAL Gross Loss": "loc_ws_beazley_share_gg_aal",
        "Quake Beazley Location AAL Gross Loss": "loc_eq_beazley_share_gg_aal",
        "Buildings": "loc_tiv_buildings",
        "Contents": "loc_tiv_contents",
        "BI": "loc_tiv_bi",
        "Beazley Gate": "beazley_gate",
        "PPC": "ppc_code",
        "Sprinkler": "sprinkler",
        "California Earthquake - Los Angeles (15022534)": "rms_event_15022534",
        "California Earthquake - San Francisco (15006191)": "rms_event_15006191",
        "New Madrid Earthquake (15355285)": "rms_event_15355285",
        "New Madrid Extreme Stress Event (15387653)": "rms_event_15387653",
        "PNW Earthquake (15100131)": "rms_event_15100131",
        "Florida Windstorm #1 - Miami-Dade (2865409)": "rms_event_2865409",
        "Florida Windstorm #2 - Pinellas Hurricane (2869298)": "rms_event_2869298",
        "USA Windstorm Gulf of Mexico (2848918)": "rms_event_2848918",
        "Carolinas Windstorm immediately following NE Windstorm (2867710)": "rms_event_2867710",
        "North East Windstorm (2874165)": "rms_event_2874165",      
        "YEARBUILT": "year_built",
        "NUMSTORIES": "num_stories",
        "FLOORAREA": "floor_area",
        "DISTCOAST": "distance_to_coast"

    }

def extra_columns():
        return [
        "YearMonth",
        "PORTINFOID",
        "PORTNAME",
        "PORTNUM",
        "Lineage Risk Number",
        "LOCNUM",
        "SignedLine Value used for calc",
        "coverageid_count",
        "Buildings_eq",
        "Contents_eq",
        "BI_eq",
        "Buildings_ws",
        "Contents_ws",
        "BI_ws",
        "TIV_eq",
        "TIV_ws",
        "TIV_aop",
        "Wind Beazley Location StdDev Gross Loss",
        "Quake Beazley Location StdDev Gross Loss",
        "All Perils Beazley Location StdDev Gross Loss",
        "Wind Beazley Account AAL Gross Loss",
        "Wind Beazley Account StdDev Gross Loss",
        "Quake Beazley Account StdDev Gross Loss",
        "Beazley Gate Description",
        "Ceded Account Premium",
        "Policy Wind Cover",
        "Policy Quake Cover",
        "Policy SCS Cover",
        "Policy AOP Cover",
        "SignedLine",
        "YEARUPGRAD",
        "ROOFAGE", 
        "ROOFGEOM",
        "ROOFSYS",      
        "AOP Limit",   
        "Lineage",      
        "coverageid_max",
        "coverageid_min",

        #columns used in calcs (below) that are no longer nedded
        "AFB Account Premium",
        "Wind Limit",
        "Quake Limit",
        "SCS Limit",
        "Wind Excess",
        "Quake Excess",
        "SCS Excess",
        "AOP Excess",
        "Wind Account Deductible",
        "Wind Location Deductible",
        "Quake Account Deductible",
        "Quake Location Deductible",        
        "SCS Account Deductible",
        "SCS Location Deductible",
        "AOP Account Deductible",
        "AOP Location Deductible",
        "Account Contribution to 1 in 250 for Property + Treaty All Perils",
        "Account Contribution to 1 in 10 for Property + Treaty All Perils",
        "BLDGSCHEME",
        "BLDGCLASS",  
        "OCCSCHEME",
        "OCCTYPE",
        #columns that were created for calc below that are no longer needed
        "acc_tiv_total",
        "acc_beazley_share_gg_aal",
        # Test
        "Policy Flood Cover",
        "zone2",
        "Policy Terror Cover",
	    "Location Flood Cover",
        "Location Terror Cover",
        "zone1",
        "row_num"


        ]




def set_lookup_columns(df):
    df = join_param_table(df, hx.params.table_country, "Country", "address_dropdown/country", "Country Code", "address_dropdown/country")
    df = join_param_table(df, hx.params.table_atc_mapping, "BI Group", "industry_occupancy_dropdown/industry", "Orig Code", "OCCTYPE", drop=False)
    df = join_param_table(df, hx.params.table_atc_mapping, "Mapped ATC", "industry_occupancy_dropdown/occupancy", "Orig Code", "OCCTYPE", drop=True)
    df = join_param_table(df, hx.params.table_iso_construction_mapping, "ISO Class", "iso_constr", "Scheme Code", "construction_code_map_to_iso", drop=True)
    return df



def bordereau_table_calc(df, hxd):

    # changing data type of columns that we'll use in this function
    df = df.with_columns(
        pl.col("BLDGSCHEME").cast(pl.Utf8),
        # pl.col("BLDGCLASS").cast(pl.Int64),
        pl.col("loc_tiv_buildings").cast(pl.Float64),
        pl.col("loc_tiv_contents").cast(pl.Float64),
        pl.col("loc_tiv_bi").cast(pl.Float64),
        pl.col("loc_ws_beazley_share_gg_aal").cast(pl.Float64),
        pl.col("loc_eq_beazley_share_gg_aal").cast(pl.Float64),
        pl.col("acc_number").cast(pl.Utf8),
        pl.col("Account Contribution to 1 in 250 for Property + Treaty All Perils").cast(pl.Float64),
        pl.col("Account Contribution to 1 in 10 for Property + Treaty All Perils").cast(pl.Float64),

    )

    # change covered field to match dropdown
    df = df.with_columns(
        (pl.when(pl.col("loc_ws_covered")=="Y")).then(pl.lit("Yes")).otherwise(pl.lit("No")).alias("loc_ws_covered"),
        (pl.when(pl.col("loc_eq_covered")=="Y")).then(pl.lit("Yes")).otherwise(pl.lit("No")).alias("loc_eq_covered"),
        (pl.when(pl.col("loc_scs_covered")=="Y")).then(pl.lit("Yes")).otherwise(pl.lit("No")).alias("loc_scs_covered"),
        (pl.when(pl.col("loc_aop_covered")=="Y")).then(pl.lit("Yes")).otherwise(pl.lit("No")).alias("loc_aop_covered")
    )

    df = df.with_columns(
        pl.when(pl.col("new_renewal")=="").then(pl.lit("Unknown")).otherwise("new_renewal").alias("new_renewal")
    )

    # this column will be used for the ISO lookup. 
    df = df.with_columns(
        pl.concat_str(["BLDGSCHEME", "BLDGCLASS"], separator="-").alias("construction_code_map_to_iso")
    )

    # TIV for buildings and BI is 0 whern HO6 Coverage = Yes
    df = df.with_columns(
        pl.when(hxd.cds.layers[0].HO6_coverage == "Yes")
        .then(pl.lit(0))
        .otherwise( pl.col("loc_tiv_buildings").fill_nan(0).fill_null(0))
        .alias("loc_tiv_buildings"),

        pl.when(hxd.cds.layers[0].HO6_coverage == "Yes")
        .then(pl.lit(0))
        .otherwise( pl.col("loc_tiv_bi").fill_nan(0).fill_null(0))
        .alias("loc_tiv_bi"),
    
        pl.col("loc_tiv_contents").fill_nan(0).fill_null(0).alias("loc_tiv_contents"),
    )

    df = df.with_columns(
        (pl.col("loc_tiv_buildings") + pl.col("loc_tiv_contents") + pl.col("loc_tiv_bi")).alias("loc_tiv_total")
    )
     
    df = df.with_columns(
        pl.sum_horizontal("loc_ws_beazley_share_gg_aal", "loc_eq_beazley_share_gg_aal").sum().over("acc_number").alias("acc_beazley_share_gg_aal")
    )

    df = df.with_columns(
        (((pl.sum_horizontal("loc_ws_beazley_share_gg_aal", "loc_eq_beazley_share_gg_aal")) / pl.col("acc_beazley_share_gg_aal")) * pl.col("Account Contribution to 1 in 250 for Property + Treaty All Perils")).fill_nan(0).fill_null(0).alias("loc_1_in_250_oep"),
        (((pl.sum_horizontal("loc_ws_beazley_share_gg_aal", "loc_eq_beazley_share_gg_aal")) / pl.col("acc_beazley_share_gg_aal")) * pl.col("Account Contribution to 1 in 10 for Property + Treaty All Perils")).fill_nan(0).fill_null(0).alias("loc_1_in_10_aep")
    )

    # calculate AFB GGP
    inception_date = datetime(hxd.cds.standard_fields.inception_date.year, hxd.cds.standard_fields.inception_date.month, hxd.cds.standard_fields.inception_date.day)

    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        line_use = hxd.cds.layers[0].signed_line
    else:
        line_use = hxd.cds.layers[0].written_line

    if hxd.cds.layers[0].expiry_signed_line in [None, 0]:
        line_multiplier = line_use
    else:
        line_multiplier = hxd.cds.layers[0].expiry_signed_line

    df = df.with_columns(
        pl.when((pl.col("inception_date") < inception_date) & (pl.col("inception_date") != pl.col("expiry_date")))
        .then((pl.col("Ceded Account Premium") * line_multiplier) / ((pl.col("expiry_date") - pl.col("inception_date")).dt.days() / 366 ))
        .when((pl.col("inception_date") >= inception_date) & (pl.col("inception_date") != pl.col("expiry_date")))
        .then((pl.col("Ceded Account Premium") * line_use) / ((pl.col("expiry_date") - pl.col("inception_date")).dt.days() / 366 ))
        .otherwise(0)
        .alias("acc_beazley_received_gg_prem")

    )

    df = df.with_columns(
         pl.col("loc_tiv_total").sum().over("acc_number").alias("acc_tiv_total")
    )

    # allocate account level details to location level 
    df = df.with_columns(
        (pl.col("Wind Limit") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_ws_limit"),
        (pl.col("Quake Limit") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_eq_limit"),
        (pl.col("SCS Limit") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_scs_limit"),
        (pl.col("Wind Excess") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_ws_excess"),
        (pl.col("Quake Excess") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_eq_excess"),
        (pl.col("SCS Excess") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_scs_excess"),
        (pl.col("AOP Excess") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_aop_excess"),
        (pl.col("Wind Account Deductible") * (pl.col("loc_tiv_total") / pl.col("acc_tiv_total"))).fill_nan(0).alias("loc_ws_ded")
    )

    df = df.with_columns(
        (pl.when(pl.col("Wind Location Deductible") == 0))
        .then(((pl.col("loc_tiv_total") / pl.col("acc_tiv_total")) * pl.col("Wind Account Deductible")).fill_nan(0))
        .otherwise(pl.col("Wind Location Deductible"))
        .alias("loc_ws_ded"),
        (pl.when(pl.col("Quake Location Deductible") == 0))
        .then(((pl.col("loc_tiv_total") / pl.col("acc_tiv_total")) * pl.col("Quake Account Deductible")).fill_nan(0))
        .otherwise(pl.col("Quake Location Deductible"))
        .alias("loc_eq_ded"),
        (pl.when(pl.col("SCS Location Deductible") == 0))
        .then(((pl.col("loc_tiv_total") / pl.col("acc_tiv_total")) * pl.col("SCS Account Deductible")).fill_nan(0))
        .otherwise(pl.col("SCS Location Deductible"))
        .alias("loc_scs_ded"),
        (pl.when(pl.col("AOP Location Deductible") == 0))
        .then(pl.col("AOP Account Deductible"))
        .otherwise(pl.col("AOP Location Deductible"))
        .alias("loc_aop_ded"),   
    )
    
    #JK - I have no idea why this creates a new column rather than just renaming it. I have to drop it here but I wonder if it's just something wrong with HX and we could remove this line later? 
    df = df.drop("Quake Beazley Account AAL Gross Loss")  

    df = df.sort(pl.col("loc_tiv_total"), descending=True)

    # sets total column values 
    hxd.cds.exposure.granular.sov_total.loc_tiv_buildings = df.select(pl.col("loc_tiv_buildings")).sum().item()
    hxd.cds.exposure.granular.sov_total.loc_tiv_contents = df.select(pl.col("loc_tiv_contents")).sum().item()
    hxd.cds.exposure.granular.sov_total.loc_tiv_bi = df.select(pl.col("loc_tiv_bi")).sum().item()
    hxd.cds.exposure.granular.sov_total.loc_tiv_total = df.select(pl.col("loc_tiv_total")).sum().item()
    hxd.cds.exposure.granular.sov_total.floor_area = df.select(pl.col("floor_area")).sum().item()
    hxd.cds.exposure.granular.sov_total.loc_ws_beazley_share_gg_aal = df.select(pl.col("loc_ws_beazley_share_gg_aal")).sum().item()
    hxd.cds.exposure.granular.sov_total.loc_eq_beazley_share_gg_aal = df.select(pl.col("loc_eq_beazley_share_gg_aal")).sum().item()

    return df

def select_binders_for_em_pull(hxd, progress):

    # first if statment checks if the user selected the binder and if (when blank) it would overwrite the first instance of the agg results
    for binder in hxd.cds.exposure_management_api.search_results:
        if binder.selected and not any(
            binder.binder_name == item.binder_name and
            binder.binder_reference == item.binder_reference and
            binder.num_locs == item.num_locs for item in hxd.cds.exposure_management_api.agg_search_results):
                if hxd.cds.exposure_management_api.agg_search_results[0].binder_name == None:
                    hxd.cds.exposure_management_api.agg_search_results[0] =({
                        "binder_name": binder.binder_name,
                        "binder_reference": binder.binder_reference,
                        "num_locs": binder.num_locs
                    })
                else:
                    hxd.cds.exposure_management_api.agg_search_results.append({
                        "binder_name": binder.binder_name,
                        "binder_reference": binder.binder_reference,
                        "num_locs": binder.num_locs
                        })

def clear_binder_list(hxd, progress):

    clear_list =({
        "binder_name": "",
        "binder_reference": "",
        "num_locs": ""
    })
    
    for binder in hxd.cds.exposure_management_api.agg_search_results:
        binder = clear_list


def clean_state_county(hxd, df):
    rms_proxy_rate_df = pl.from_pandas(hx.params.table_rms_proxy_rate).select("Zip Code", "State Code", "County").rename({"Zip Code": "zip", "State Code": "state", "County": "county"})
    rms_proxy_rate_df = rms_proxy_rate_df.with_columns(pl.lit("United States").alias("country_titlecase"))

    df.with_columns(
        pl.col("address_dropdown/country").str.to_titlecase().alias("address_dropdown/country"),
        pl.col("zip").cast(pl.Utf8).alias('zip')
    )
    
    df = df.join(rms_proxy_rate_df, left_on=["zip", "address_dropdown/country"], right_on=["zip", "country_titlecase"], how="left")

    df = df.with_columns(
        pl.when(pl.col("state").is_null())
        .then(pl.col("address_dropdown/state"))
        .otherwise("state")
        .alias("address_dropdown/state"),

        pl.when(pl.col("county").is_null())
        .then(pl.col("address_dropdown/county").str.to_titlecase())
        .otherwise("county")
        .alias("address_dropdown/county")
    ).drop(["state", "county"])

    return df
