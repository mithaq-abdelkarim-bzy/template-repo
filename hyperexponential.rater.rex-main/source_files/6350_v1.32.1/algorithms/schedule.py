import hx
from operator import itemgetter
import polars as pl
import pandas as pd
import numpy as np
from email import policy
from email.generator import BytesGenerator
from datetime import date
from algorithms.exposure_management_task import query_exposure_management_database
from algorithms.schedule_clean_state_county import clean_state_county
from algorithms.remodelling_check.email_generation import generate_email


def schedule_table_calc(hxd, df, other_data):
    '''
    Caluclates the output fields for schedule table
    '''

    # Calculate the sum for schedule table
    slip_currency_exchange_rate = hxd.policy_information.exchange_rate or 1
    df = df.with_columns(
        df.select(
            pl.col('tiv_buildings', 'tiv_contents', 'tiv_other', 'tiv_bi').fill_null(0)
        ).sum(axis=1).alias("tiv_total"),
        df.select(
            pl.col('tiv_contents', 'tiv_other').fill_null(0)
        ).sum(axis=1).alias("tiv_contents_total"),
    )

    # We convert each row's value first to USD then to the slip currency. Floor area needs no conversion
    tiv_sum = df.select(
        [
            *[
                (pl.col(col).fill_null(0) / pl.col('exchange_rate') * slip_currency_exchange_rate)
                for col in ['tiv_buildings', 'tiv_contents', 'tiv_other', 'tiv_bi', 'tiv_total']
            ],
            pl.col('floor_area').fill_null(0)
        ]
    ).sum().row(0)

    other_data["total_tiv_buildings"], other_data["total_tiv_contents"], other_data["total_tiv_other"], other_data["total_tiv_bi"], other_data["total_tiv_total"], other_data["total_floor_area"] = tiv_sum

    other_data["total_num_locs"] = df.shape[0]

    # Calculate WS Tier, WF Tier, WS Gate, EQ Gate, EQ Cresta Zone
    rms_proxy_rate = hx.params.rms_proxy_rate
    rms_proxy_rate_avg = hx.params.rms_proxy_rate_avg
    us_state_code = hx.params.us_state_code
    ceded_profit = hx.params.ceded_profit

    df = df.drop(["ws_tier", "wf_tier", "ws_gate", "eq_gate", "cresta_zone"])

    df = df.with_columns(
        (
            pl.col("state") + pl.col("county")
        ).fill_null("").alias("state_county"),
        pl.col("zip").str.zfill(5).alias("zip")  # zero-pad zip codes for joins below
    )

    # Lowercase state and country names to avoid errors later
    df = df.with_columns(
        pl.col("state").str.to_uppercase().alias("state"),
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase"),
        pl.col("country").str.to_lowercase().alias("country_lowercase"),
    )

    rms_proxy_rate_pl = pl.from_pandas(rms_proxy_rate)[["Zip Code", "WS Gate", "EQ Gate", "Cresta Zone"]]
    rms_proxy_rate_pl = rms_proxy_rate_pl.rename({"Zip Code": "zip", "WS Gate": "ws_gate_num_proxy", "EQ Gate": "eq_gate_num_proxy", "Cresta Zone": "cresta_zone_proxy"})

    rms_proxy_rate_avg_pl = pl.from_pandas(rms_proxy_rate_avg)[["StateCounty", "WS Gate", "EQ Gate", "Cresta Zone"]]
    rms_proxy_rate_avg_pl = rms_proxy_rate_avg_pl.rename({"StateCounty": "state_county", "WS Gate": "ws_gate_num_proxy_avg", "EQ Gate": "eq_gate_num_proxy_avg", "Cresta Zone": "cresta_zone_proxy_avg"})
    rms_proxy_rate_avg_pl = rms_proxy_rate_avg_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    us_state_code_pl = pl.from_pandas(us_state_code)[["US State Code", "WF Tier"]]
    us_state_code_pl = us_state_code_pl.rename({"US State Code": "state", "WF Tier": "wf_tier_us"})

    ceded_profit_pl = pl.from_pandas(ceded_profit)[["Gate Number", "Gate"]]

    gate_pl = df[["zip", "state_county_lowercase", "state", "country"]]
    gate_pl = gate_pl.join(rms_proxy_rate_pl, on="zip", how="left")
    gate_pl = gate_pl.join(rms_proxy_rate_avg_pl, on="state_county_lowercase", how="left")
    gate_pl = gate_pl.join(us_state_code_pl, on="state", how="left")

    df = df.with_columns(gate_pl.select(
        [
            pl.when(pl.col("country") != "United States")
                .then("N/A")
                .when((pl.col("zip") == None) | (pl.col("zip") == ""))
                .then(pl.col("cresta_zone_proxy_avg"))
                .otherwise(pl.col("cresta_zone_proxy"))
                .alias("cresta_zone"),
            pl.when(pl.col("country") != "United States")
                .then(999)
                .when((pl.col("zip") == None) | (pl.col("zip") == ""))
                .then(pl.col("eq_gate_num_proxy_avg"))
                .otherwise(pl.col("eq_gate_num_proxy"))
                .fill_null(161)
                .alias("eq_gate_no"),
            pl.when(pl.col("country") != "United States")
                .then(99.9)
                .when((pl.col("zip") == None) | (pl.col("zip") == ""))
                .then(pl.col("ws_gate_num_proxy_avg"))
                .otherwise(pl.col("ws_gate_num_proxy"))
                .fill_null(0)
                .alias("ws_gate_no"),
            pl.when(pl.col("country") == "United States")
                .then(pl.col("wf_tier_us"))
                .otherwise(3)
                .alias("wf_tier")
        ]
    ))

    df = df.with_columns(
        pl.col("ws_gate_no").str.slice(-1).alias("ws_tier")
    )

    del gate_pl

    ceded_profit_pl = ceded_profit_pl.rename({"Gate Number": "eq_gate_no", "Gate": "eq_gate"})
    df = df.join(ceded_profit_pl, on="eq_gate_no", how="left")
    ceded_profit_pl = ceded_profit_pl.rename({"eq_gate_no": "ws_gate_no", "eq_gate": "ws_gate"})
    df = df.join(ceded_profit_pl, on="ws_gate_no", how="left")

    if hxd.policy_information.small_schedule_model:
        other_data["cresta_zone"] = df["cresta_zone"].to_list()
        other_data["ws_tier"] = df["ws_tier"].to_list()
        other_data["wf_tier"] = df["wf_tier"].to_list()
        other_data["eq_gate"] = df["eq_gate"].to_list()
        other_data["ws_gate"] = df["ws_gate"].to_list()


    # Calculate Risk Level - EQ, WS, FL, SCS, WF
    eq_catnet_score = hx.params.eq_catnet_score
    fl_catnet_score = hx.params.fl_catnet_score
    fl_katrisk_score = hx.params.fl_katrisk_score
    ha_catnet_score = hx.params.ha_catnet_score
    tn_catnet_score = hx.params.tn_catnet_score
    wf_catnet_score = hx.params.wf_catnet_score
    wf_riskmeter_score = hx.params.wf_riskmeter_score
    ws_catnet_score = hx.params.ws_catnet_score
    scs_category = hx.params.scs_category

    df = df.drop(["risk_level_eq", "risk_level_ws", "risk_level_fl", "risk_level_wf"])

    # Earthquake Risk Level
    eq_catnet_score_pl = pl.from_pandas(eq_catnet_score)[["Score Band", "Category"]]
    eq_catnet_score_pl = eq_catnet_score_pl.rename({"Score Band": "catnet_score_eq", "Category": "risk_level_eq"})
    df = df.join(eq_catnet_score_pl, on="catnet_score_eq", how="left")

    # Windstorm Risk Level
    ws_catnet_score_pl = pl.from_pandas(ws_catnet_score)[["Score Band", "Category"]]
    ws_catnet_score_pl = ws_catnet_score_pl.rename({"Score Band": "catnet_score_ws", "Category": "risk_level_ws"})
    df = df.join(ws_catnet_score_pl, on="catnet_score_ws", how="left")

    # Flood Risk Level
    fl_catnet_score_pl = pl.from_pandas(fl_catnet_score)[["Score Band", "Category"]]
    fl_catnet_score_pl = fl_catnet_score_pl.rename({"Score Band": "catnet_score_fl", "Category": "category_catnet"})

    fl_katrisk_score_pl = pl.from_pandas(fl_katrisk_score)[["KatRisk Score", "KatRisk Category"]]
    fl_katrisk_score_pl = fl_katrisk_score_pl.rename({"KatRisk Score": "katrisk_score_fl", "KatRisk Category": "category_katrisk"})

    df_fl = df[["country", "catnet_score_fl", "katrisk_score_fl"]].join(fl_catnet_score_pl, on="catnet_score_fl", how="left")
    df_fl = df_fl.join(fl_katrisk_score_pl, on="katrisk_score_fl", how="left")
    df = df.with_columns(
        df_fl.select(
            pl.when(pl.col("country") == "United States")
            .then(pl.col("category_katrisk"))
            .otherwise(pl.col("category_catnet"))
            .alias("risk_level_fl")
        )
    )

    # SCS Risk Level
    tn_catnet_score_pl = pl.from_pandas(tn_catnet_score)[["Score Band", "Points"]]
    tn_catnet_score_pl = tn_catnet_score_pl.rename({"Score Band": "catnet_score_tn", "Points": "points_tn"})
    ha_catnet_score_pl = pl.from_pandas(ha_catnet_score)[["Score Band", "Points"]]
    ha_catnet_score_pl = ha_catnet_score_pl.rename({"Score Band": "catnet_score_ha", "Points": "points_ha"})
    scs_category_pl = pl.from_pandas(scs_category).rename({"Points": "points", "Category": "risk_level_scs"})

    df_scs = df[["catnet_score_tn", "catnet_score_ha"]].join(tn_catnet_score_pl, on="catnet_score_tn", how="left")
    df_scs = df_scs.join(ha_catnet_score_pl, on="catnet_score_ha", how="left")
    df_scs = df_scs.with_columns(
        pl.max("points_tn", "points_ha").alias("points")
    )
    df = df.with_columns(df_scs.join(scs_category_pl, on="points", how="left")["risk_level_scs"])

    # WF Risk Level
    wf_catnet_score_pl = pl.from_pandas(wf_catnet_score)[["Intensity", "Category"]]
    wf_catnet_score_pl = wf_catnet_score_pl.rename({"Intensity": "catnet_score_wf", "Category": "category_catnet"})
    wf_riskmeter_score_pl = pl.from_pandas(wf_riskmeter_score)[["Score", "Category"]]
    wf_riskmeter_score_pl = wf_riskmeter_score_pl.rename({"Score": "riskmeter_score_wf", "Category": "category_riskmeter"})

    catnet_score_wf_list = list(map(int, df.select("catnet_score_wf").to_series().fill_null(0).ceil().to_list()))
    df.replace("catnet_score_wf", pl.Series(name="catnet_score_wf", values=catnet_score_wf_list))

    riskmeter_score_wf_list = list(map(int, ((df.select("riskmeter_score_wf").to_series().fill_null(0) / 10).ceil() * 10).to_list()))
    df.replace("riskmeter_score_wf", pl.Series(name="riskmeter_score_wf", values=riskmeter_score_wf_list))

    df_wf = df[["catnet_score_wf", "riskmeter_score_wf"]].join(wf_catnet_score_pl, on="catnet_score_wf", how="left")
    df_wf = df_wf.join(wf_riskmeter_score_pl, on="riskmeter_score_wf", how="left")
    df = df.with_columns(
        df_wf.select(
            pl.when((pl.col("riskmeter_score_wf") == None) | (pl.col("riskmeter_score_wf") == 0))
            .then(pl.col("category_catnet"))
            .otherwise(pl.col("category_riskmeter"))
            .alias("risk_level_wf")
        )
    )

    if hxd.policy_information.small_schedule_model:
        other_data["tiv_total"] = df["tiv_total"].to_list()
        for peril in ["eq", "ws", "fl", "scs", "wf"]:
            other_data[f"risk_level_{peril}"] = df[f"risk_level_{peril}"].to_list()


    del df_fl, df_scs, df_wf

    # Calculate ceded profit ratio
    ceded_profit_pl = pl.from_pandas(ceded_profit)[["Gate Number", "Gate", "NACP", "Open Market", "European Commercial Property", "Renewables"]]

    ceded_profit_pl = ceded_profit_pl.rename({"Gate Number": "eq_gate_no"})
    eq_gate_joined_pl = df[["eq_gate_no"]].join(ceded_profit_pl, on="eq_gate_no", how="left")
    df = df.with_columns(
        eq_gate_joined_pl.select(
            pl.when(hxd.policy_information.team == None)
                .then(0)
                .when(hxd.policy_information.team == "NACP")
                .then(pl.col("NACP"))
                .when(hxd.policy_information.team == "Open Market")
                .then(pl.col("Open Market"))
                .when(hxd.policy_information.team == "European Commercial Property")
                .then(pl.col("European Commercial Property"))
                .otherwise(pl.col("Renewables"))
                .alias("earthquake_us_profit_ceded_ratio")
        )
    )

    ceded_profit_pl = ceded_profit_pl.rename({"eq_gate_no": "ws_gate_no"})
    ws_gate_joined_pl = df[["ws_gate_no"]].join(ceded_profit_pl, on="ws_gate_no", how="left")
    df = df.with_columns(
        ws_gate_joined_pl.select(
            pl.when(hxd.policy_information.team == None)
                .then(0)
                .when(hxd.policy_information.team == "NACP")
                .then(pl.col("NACP"))
                .when(hxd.policy_information.team == "Open Market")
                .then(pl.col("Open Market"))
                .when(hxd.policy_information.team == "European Commercial Property")
                .then(pl.col("European Commercial Property"))
                .otherwise(pl.col("Renewables"))
                .alias("windstorm_us_profit_ceded_ratio")
        )
    )

    # For quote doc - set the key location
    key_location = df[["tiv_total", "street_name", "state", "county", "city", "zip", "country"]]
    max_tiv_total = key_location['tiv_total'].max()
    key_location = key_location.filter(pl.col('tiv_total') == max_tiv_total).limit(1)



    hxd.quote_documents.key_location = \
        str(key_location['street_name'].item() or "") + (", " if key_location['street_name'].item() else "") + \
        str(key_location['city'].item() or "") + (", " if key_location['city'].item() else "")  + \
        str(key_location['county'].item() or "") + (", " if key_location['county'].item() else "")  + \
        str(key_location['state'].item() or "") + (", " if key_location['state'].item() else "")  + \
        str(key_location['country'].item() or "") + (", " if key_location['country'].item() else "")  + \
        str(key_location['zip'].item() or "")
        
    del eq_gate_joined_pl, ws_gate_joined_pl

    # Join on WS and EQ Zones for account segmentation tab
    ws_zones = pl.DataFrame(hx.params.ws_zones)
    df = df.join(ws_zones, on="ws_gate", how="left")
    eq_zones = pl.DataFrame(hx.params.eq_zones)
    df = df.join(eq_zones, on="eq_gate", how="left")

    # Create grouped dtc and year_built columns
    dtc_bands = pl.DataFrame(hx.params.dtc_bands)[['dtc_band', 'min_dtc']].rename({"min_dtc": "distance_from_coast"})
    df = df.with_columns(pl.col("distance_from_coast").fill_null(strategy="zero"))  # TODO: check null preferred action
    df = df.sort("distance_from_coast")
    df = df.join_asof(dtc_bands, on="distance_from_coast", strategy="backward")

    year_built_bands = pl.DataFrame(hx.params.year_built_bands)[['year_built_band', 'max_year_built']].rename({"max_year_built": "year_built"})
    df = df.with_columns(pl.col("year_built").fill_null(9999)) 
    df = df.sort("year_built")
    df = df.join_asof(year_built_bands, on="year_built", strategy="forward")
    df = df.with_columns(pl.col('year_built_band').fill_null("Unknown"))

    df = df.sort("row_nr")
    return df

        
def read_schedule_table(hxd):
    '''
    Read the schedule table as polars format
    '''

    columns = [
        "loc_id",
        "fire_deductible", "currency", "fire_covered", "street_name",
        "eq_covered", "ws_covered", "fl_covered", "scs_covered", "wf_covered",
        "zip", "tiv_buildings", "tiv_contents", "tiv_other", "tiv_bi", "tiv_total", "constr_code",
        "num_buildings", "num_stories", "year_built", "year_updated", "pc_code", "sprinkler",
        "year_cov_last_replaced", "roof_age", "floor_area", "distance_from_coast", "roof_covering",
        "roof_geometry", "ws_tier", "wf_tier", "ws_gate", "eq_gate", "eq_crit_cat_zone", "ws_crit_cat_zone", "cresta_zone", "soil_type",
        "liquefaction", "landslide", "floodzone", "other_floodzone", "basement", "building_elevation",
        "eq_construction_quality", "plan_irregularity", "soft_story",
        "vertical_irregularity", "ornamentation", "equipment_eq_bracing", "equipment_support_maintenance",
        "pounding", "ws_construction_quality", "roof_anchor", "roof_equipment_hurricane_bracing",
        "cladding_type", "frame_foundation_connection", "katrisk_score_fl", "catnet_score_wf",
        "riskmeter_score_wf", "catnet_score_tn", "catnet_score_ha", "catnet_score_fl", "catnet_score_eq",
        "catnet_score_ws", "risk_level_eq", "risk_level_ws", "risk_level_fl", "risk_level_scs", "risk_level_wf",
        "longitude", "latitude", "property_description", "constr_description"
        ]

    if hxd.policy_information.small_schedule_model:
        df = pd.DataFrame([{column: getattr(row, column) for column in columns} for row in hxd.schedule.schedule_table])

        df["industry"] = [row.industry_occupancy_dropdown.industry for row in hxd.schedule.schedule_table]
        df["occupancy"] = [row.industry_occupancy_dropdown.occupancy for row in hxd.schedule.schedule_table]
        df["country"] = [row.address_dropdown.country for row in hxd.schedule.schedule_table]
        df["city"] = [row.address_dropdown.city for row in hxd.schedule.schedule_table]
    else:
        if hxd.schedule.large_schedule_workflow.load_from_schedule_file:
            with hxd.schedule.large_schedule_workflow.schedule_file.open("b") as f:
                df = pd.read_csv(f)
        elif hxd.schedule.large_schedule_workflow.load_from_em_database:
            with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
                df = pd.read_csv(f)
        else:
            hx.errors.fatal("Error: Please upload/import schedule file")
        # with hxd.schedule.large_schedule_workflow.large_schedule_em_file.open("b") as f:
        #     df = pd.read_csv(f)

        # Error just in case the input file is missing columns
        for col in columns:
            if col not in df.columns:
                df[col] = None

        df = df[columns + 
                    ["industry_occupancy_dropdown/industry", "industry_occupancy_dropdown/occupancy", "address_dropdown/country", "address_dropdown/city"]
                ]

        df.rename(columns={"industry_occupancy_dropdown/industry": "industry", "industry_occupancy_dropdown/occupancy": "occupancy",
                    "address_dropdown/country": "country", "address_dropdown/city": "city"}, inplace=True)
        
        df["fema_flood_zone"] = None
        
        if hxd.schedule.spatial_key_file.exists and hxd.schedule.large_schedule_workflow.spatial_key_updated:
            columns_to_overwrite = ["catnet_score_tn", "catnet_score_ha", "catnet_score_fl", 
                                    "catnet_score_eq", "catnet_score_ws", "catnet_score_wf", "katrisk_score_fl", "fema_flood_zone",
                                    "zip", "latitude", "longitude", "eq_crit_cat_zone", "ws_crit_cat_zone"]
            
            with hxd.schedule.spatial_key_file.open(mode="b") as f:
                spatial_key_df = pd.read_csv(f)
            
            for column in columns_to_overwrite:
                if column in spatial_key_df.columns:
                    df.drop(labels=column, axis="columns", inplace=True)
                    df[column] = spatial_key_df[column]

    # Replace blank construction codes with 0 (unknown)
    df["constr_code"] = df["constr_code"].fillna(0)
    
    # Clean state and county values based on ZIP code
    df = clean_state_county(hxd, df)

    # Get default type for polars joining
    df['zip'] = df['zip'].astype('string')
    df['state'] = df['state'].astype('string')

    # Force into strings as occasionally these columns (particuarly catnet_score_fl) can be incorrectly interpreted as floats 
    # which can cause errors when converting to polars, which doesn't support mixed-type columns.
    for col in [
        "catnet_score_tn", "catnet_score_ha", "catnet_score_fl", "catnet_score_eq", 
        "catnet_score_ws", "catnet_score_wf", "katrisk_score_fl", "fema_flood_zone", "property_description"
        ]:
        if col in df.columns:
            df[col] = df[col].astype("string")

    df = pl.from_pandas(df)
    df = df.with_columns(
        pl.col("tiv_buildings").cast(pl.Float64), 
        pl.col("tiv_contents").cast(pl.Float64),
        pl.col("tiv_other").cast(pl.Float64),
        pl.col("tiv_bi").cast(pl.Float64),
        pl.col("tiv_total").cast(pl.Float64),
        pl.col("catnet_score_wf").cast(pl.Float64),
        pl.col("riskmeter_score_wf").cast(pl.Float64),
        pl.col("constr_code").cast(pl.Int64),
        pl.col("pc_code").cast(pl.Int64),
        pl.col("fire_deductible").cast(pl.Float64),
        pl.col("year_built").cast(pl.Int64),
        pl.col("year_cov_last_replaced").cast(pl.Int64),
        pl.col("distance_from_coast").cast(pl.Float64),
        pl.col("num_stories").cast(pl.Int64),
        pl.col("floor_area").cast(pl.Int64),
        pl.col("zip").cast(pl.Utf8),
        pl.col("ws_construction_quality").cast(pl.Utf8),
        pl.col("liquefaction").cast(pl.Utf8),
        pl.col("landslide").cast(pl.Utf8),
        pl.col("soil_type").cast(pl.Utf8),
        pl.col("floodzone").cast(pl.Utf8),
        pl.col("other_floodzone").cast(pl.Utf8),
        pl.col("katrisk_score_fl").cast(pl.Utf8),
        pl.col("catnet_score_tn").cast(pl.Utf8), 
        pl.col("catnet_score_ha").cast(pl.Utf8), 
        pl.col("catnet_score_fl").cast(pl.Utf8), 
        pl.col("catnet_score_eq").cast(pl.Utf8), 
        pl.col("catnet_score_ws").cast(pl.Utf8),
        # Large Policy Model requires additional cohersing
        pl.col("county").cast(pl.Utf8), 
        pl.col("roof_covering").cast(pl.Utf8), 
        pl.col("roof_geometry").cast(pl.Utf8), 
        pl.col("roof_anchor").cast(pl.Utf8), 
        pl.col("roof_equipment_hurricane_bracing").cast(pl.Utf8), 
        pl.col("cladding_type").cast(pl.Utf8), 
        pl.col("frame_foundation_connection").cast(pl.Utf8), 
        pl.col("eq_construction_quality").cast(pl.Utf8)
    )
    data_types_dict = data_types()
    for col in data_types_dict:
        if col in df.columns:
            df = df.with_columns(
                pl.col(col).cast(data_types_dict[col])
            )

    if "fema_flood_zone" in df.columns:
        df = df.with_columns(
            pl.col("fema_flood_zone").cast(pl.Utf8)
        )
    df = df.with_row_count()

    return df


def get_currency_exchange(hxd, df, progress):
    '''
    Get each row's exchange rate from the row's currency to USD
    '''
    # Maps exchange rate from currency column

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

    currency_set = set(df['currency'].to_list())
    currency_query_string = "("
    for currency in currency_set:
        currency_query_string += f"'{currency}',"
    currency_query_string = currency_query_string[:-1] + ")"

    successful_fetch = False
    while not successful_fetch:

        query = f"""
            SELECT *
            FROM property_data.dbo.vw_currency vlp WITH (NOLOCK)
                WHERE 1=1
                AND year = {year}
                AND quarter = {quarter}
                AND code IN {currency_query_string}
        """

        search_db_df, successful = query_exposure_management_database(hxd, progress, query, None, use_pandas=True)
        if search_db_df is not None:
            successful_fetch = len(search_db_df)
        if not successful_fetch:
            if quarter == 1:
                year = year - 1
                quarter = 4
            else:
                quarter = quarter - 1
        if year == 2022:
            break
    
    if search_db_df is not None:
        exchange_rate_pl = pl.from_pandas(search_db_df[['code', 'xfactor']])
        exchange_rate_pl = exchange_rate_pl.rename({'code': 'currency', 'xfactor': 'exchange_rate'})

        df = df.join(exchange_rate_pl, on="currency", how="left")
        df = df.with_columns(pl.col('exchange_rate').fill_null(1.0))
    else:
        df = df.with_columns(pl.lit(1).alias("exchange_rate"))

    return df


def map_tiv_usd(hxd, df, other_data, progress):
    '''
    Map TIV related fields from risk currency to USD
    '''

    df = df.with_columns(
        [
            (pl.col('tiv_buildings').fill_null(0) / pl.col('exchange_rate')).fill_null(0).alias('tiv_buildings_usd'),
            (pl.col('tiv_contents').fill_null(0) / pl.col('exchange_rate')).fill_null(0).alias('tiv_contents_usd'),
            (pl.col('tiv_other').fill_null(0) / pl.col('exchange_rate')).fill_null(0).alias('tiv_other_usd'),
            ((pl.col('tiv_contents').fill_null(0) + pl.col('tiv_other').fill_null(0)) / pl.col('exchange_rate')).fill_null(0).alias('tiv_contents_total_usd'),
            (pl.col('tiv_bi').fill_null(0) / pl.col('exchange_rate')).fill_null(0).alias('tiv_bi_usd'),
            (pl.col('tiv_total').fill_null(0) / pl.col('exchange_rate')).fill_null(0).alias('tiv_total_usd'),
        ]
    )

    other_data["total_tiv_total_usd"] = df['tiv_total_usd'].sum()

    # Assign to schedule table
    if hxd.policy_information.small_schedule_model:

        tiv_building_usd_list = df['tiv_buildings_usd'].to_list()
        tiv_contents_usd_list = df['tiv_contents_usd'].to_list()
        tiv_other_usd_list = df['tiv_other_usd'].to_list()
        tiv_contents_total_usd_list = df['tiv_contents_total_usd'].to_list()
        tiv_bi_usd_list = df['tiv_bi_usd'].to_list()
        tiv_total_usd_list = df['tiv_total_usd'].to_list()

        for index, row in enumerate(hxd.schedule.schedule_table):
            row.tiv_building_usd = tiv_building_usd_list[index]
            row.tiv_contents1_usd = 0  # TODO: Why?
            row.tiv_other_usd = tiv_other_usd_list[index]
            row.tiv_contents_usd = tiv_contents_total_usd_list[index]
            row.tiv_bi_usd = tiv_bi_usd_list[index]
            row.tiv_total_usd = tiv_total_usd_list[index]
            row.tiv_contents_only_usd = tiv_contents_usd_list[index]

    elif other_data["large_model_assign"]:

        ex_rate_list = df['exchange_rate'].to_list()

        for index, row in enumerate(hxd.schedule.large_schedule_output):
            row.ex_rate = ex_rate_list[index]


    # Calculates US County TIV and international TIV for each location
    other_data['sum_tiv_total_usd'] = df['tiv_total_usd'].sum()
    other_data['sum_tiv_us_total_usd'] = df.filter(pl.col("country") == "United States")['tiv_total_usd'].sum()
    other_data['sum_tiv_intr_total_usd'] = df.filter(pl.col("country") != "United States")['tiv_total_usd'].sum()

        
    # Calculates US County, International, EQ Gate and WS Gate counts and tiv sums
    for column, column_name in zip(["state_county_lowercase", "country_lowercase", "eq_gate", "ws_gate"], ["state_county", "country", "eq_gate", "ws_gate"]):
        column_sums = df.groupby([column]).sum()[[column, "tiv_total_usd"]].rename({'tiv_total_usd': f'tiv_{column_name}'})
        df = df.join(column_sums, on=column, how="left")

        count_df = df.groupby(column).count().rename({"count": f"count_{column_name}"})
        df = df.join(count_df, on=column, how="left")

    df = df.with_columns(pl.when(pl.col("country") == "United States").then(pl.col("tiv_state_county")).otherwise(pl.col("tiv_country")).alias("tiv_region"))
    df = df.with_columns(pl.when(pl.col("country") == "United States").then(pl.col("count_state_county")).otherwise(pl.col("count_country")).alias("count_region"))
    
    return df


def schedule_tiv_rater_calc(hxd):
    '''
    Calculates tiv values in the rater and show in frontend schedule
    '''
    for row in hxd.schedule.schedule_table:
        row.tiv_total = (row.tiv_buildings or 0) + (row.tiv_contents or 0) + (row.tiv_other or 0) + (row.tiv_bi or 0)

    # The logic here is that before the rater is run, there is no indication of values being converted to any currency,
    # so users are free to change any values and they'll get the updates immediately
    # Once the rater is run once, we have a currency and an exchange rate so any value change needs a rater re-run to update
    if hxd.policy_information.small_schedule_model:
        exchange_rate = hxd.policy_information.exchange_rate or 1
        tiv_buildings_sum = tiv_contents_sum = tiv_other_sum = tiv_bi_sum = tiv_total_sum = floor_area_sum = 0

        if not hxd.experience_rating.run_rater_run:
            for row in hxd.schedule.schedule_table:
                tiv_buildings_sum += row.tiv_buildings if row.tiv_buildings else 0
                tiv_contents_sum += row.tiv_contents if row.tiv_contents else 0
                tiv_other_sum += row.tiv_other if row.tiv_other else 0
                tiv_bi_sum += row.tiv_bi if row.tiv_bi else 0
                floor_area_sum += row.floor_area if ((row.tiv_buildings or 0) and (row.floor_area or 0)) > 0 else 0
        else:
            for row in hxd.schedule.schedule_table:
                tiv_buildings_sum += (row.tiv_building_usd * exchange_rate) if row.tiv_building_usd else 0
                tiv_contents_sum += (row.tiv_contents_only_usd * exchange_rate) if row.tiv_contents_only_usd else 0
                tiv_other_sum += (row.tiv_other_usd * exchange_rate) if row.tiv_other_usd else 0
                tiv_bi_sum += (row.tiv_bi_usd * exchange_rate) if row.tiv_bi_usd else 0
                floor_area_sum += row.floor_area if ((row.tiv_buildings or 0) and (row.floor_area or 0)) > 0 else 0

        hxd.schedule.schedule_total.tiv_buildings = tiv_buildings_sum
        hxd.schedule.schedule_total.tiv_contents = tiv_contents_sum
        hxd.schedule.schedule_total.tiv_other = tiv_other_sum
        hxd.schedule.schedule_total.tiv_bi = tiv_bi_sum
        hxd.schedule.schedule_total.tiv_total = tiv_buildings_sum + tiv_contents_sum + tiv_other_sum + tiv_bi_sum
        hxd.schedule.schedule_total.floor_area = floor_area_sum


def schedule_table_hxd_assignment(hxd, df, other_data):
    '''
    Assign schedule table related calculation to backend nodes for reporting purpose
    '''

    # When the model is large
    if other_data["large_model_assign"]:

        zip_list = df["zip"].to_list()
        state_list = df["state"].to_list()
        county_list = df["county"].to_list()
        country_list = df["country"].to_list()
        occupancy_list = df["occupancy"].to_list()
        gate_no_eq_list = df["eq_gate_no"].to_list()
        gate_no_ws_list = df["ws_gate_no"].to_list()
        tiv_buildings_list = df["tiv_buildings"].to_list()
        tiv_contents_list = df["tiv_contents"].to_list()
        tiv_other_list = df["tiv_other"].to_list()
        tiv_bi_list = df["tiv_bi"].to_list()
        cresta_zone_list = df["cresta_zone"].to_list()
        ws_tier_list = df["ws_tier"].to_list()
        catnet_score_tn_list = df["catnet_score_tn"].to_list()
        catnet_score_ha_list = df["catnet_score_ha"].to_list()
        catnet_score_fl_list = df["catnet_score_fl"].to_list()
        catnet_score_wf_list = df["catnet_score_wf"].to_list()
        catnet_score_ws_list = df["catnet_score_ws"].to_list()
        catnet_score_eq_list = df["catnet_score_eq"].to_list()

        hxd.schedule.large_schedule_output = [{"zip": zip_} for zip_ in zip_list]

        for index, row in enumerate(hxd.schedule.large_schedule_output):
            row.zip = zip_list[index]
            row.state = state_list[index]
            row.county = county_list[index]
            row.country = country_list[index]
            row.occupancy = occupancy_list[index]
            row.gate_no_eq = gate_no_eq_list[index]
            row.gate_no_ws = gate_no_ws_list[index]
            row.tiv_buildings = tiv_buildings_list[index]
            row.tiv_contents = tiv_contents_list[index]
            row.tiv_other = tiv_other_list[index]
            row.tiv_bi = tiv_bi_list[index]
            row.cresta_zone = cresta_zone_list[index]
            row.ws_tier = ws_tier_list[index]
            row.catnet_score_tn = catnet_score_tn_list[index]
            row.catnet_score_ha = catnet_score_ha_list[index]
            row.catnet_score_fl = catnet_score_fl_list[index]
            row.catnet_score_wf = catnet_score_wf_list[index]
            row.catnet_score_ws = catnet_score_ws_list[index]
            row.catnet_score_eq = catnet_score_eq_list[index]

            for layer_index, layer in enumerate(hxd.layers, start=1):
                row.output_by_layer.append({"layer_index": layer_index})

    else:
        for index, row in enumerate(hxd.schedule.schedule_table):
            for layer_index, layer in enumerate(hxd.layers, start=1):
                row.output_by_layer.append({"layer_index": layer_index})
            


def update_schedule_field_labels(hxd):
    '''
    Update schedule related field labels based on the slip currency
    '''

    currency = hxd.policy_information.slip_currency
    hxd.schedule.tiv_buildings_label = f"Buildings - {currency}"
    hxd.schedule.tiv_contents_label = f"Contents - {currency}"
    hxd.schedule.tiv_other_label = f"Other - {currency}"
    hxd.schedule.tiv_bi_label = f"BI - {currency}"
    hxd.schedule.tiv_total_label = f"Total - {currency}"
    hxd.schedule.tiv_total_outside_table_label = f"Total TIV in Schedule - {currency}"


def data_types():
    return {
        "id": pl.Utf8,
        "broker_loc_id": pl.Utf8,
        "broker_subloc_id": pl.Utf8,
        "fire_deductible": pl.Float64,
        "currency": pl.Utf8,
        "fire_covered": pl.Utf8,
        "eq_covered": pl.Utf8,
        "ws_covered": pl.Utf8,
        "fl_covered": pl.Utf8,
        "scs_covered": pl.Utf8,
        "wf_covered": pl.Utf8,
        "address_dropdown/country": pl.Utf8,
        "address_dropdown/state": pl.Utf8,
        "address_dropdown/county": pl.Utf8,
        "address_dropdown/city": pl.Utf8,
        "property_description": pl.Utf8,
        "street_name": pl.Utf8,
        "zip": pl.Utf8,
        "latitude": pl.Float64,
        "longitude": pl.Float64,
        "tiv_buildings": pl.Float64,
        "tiv_contents": pl.Float64,
        "tiv_other": pl.Float64,
        "tiv_bi": pl.Float64,
        "tiv_total": pl.Float64,
        "constr_code": pl.Int64,
        "raw_constr_code": pl.Utf8,
        "constr_description": pl.Utf8,
        "num_buildings": pl.Int64,
        "num_stories": pl.Int64,
        "year_built": pl.Int64,
        "year_updated": pl.Int64,
        "industry_occupancy_dropdown/industry": pl.Utf8,
        "industry_occupancy_dropdown/occupancy": pl.Utf8,
        "broker_occu_desc": pl.Utf8,
        "rms_occupancy": pl.Utf8,
        "pc_code": pl.Int64,
        "sprinkler": pl.Utf8,
        "year_cov_last_replaced": pl.Int64,
        "roof_age": pl.Utf8,
        "floor_area": pl.Float64,
        "distance_from_coast": pl.Float64,
        "roof_covering": pl.Utf8,
        "roof_geometry": pl.Utf8,
        "ws_tier": pl.Int64,
        "wf_tier": pl.Int64,
        "ws_gate": pl.Utf8,
        "eq_gate": pl.Utf8,
        "cresta_zone": pl.Utf8,
        "soil_type": pl.Utf8,
        "liquefaction": pl.Utf8,
        "landslide": pl.Utf8,
        "floodzone": pl.Utf8,
        "other_floodzone": pl.Utf8,
        "basement": pl.Utf8,
        "building_elevation": pl.Float64,
        "katrisk_fl_1_in_10": pl.Float64,
        "eq_construction_quality": pl.Utf8,
        "plan_irregularity": pl.Utf8,
        "soft_story": pl.Utf8,
        "vertical_irregularity": pl.Utf8,
        "ornamentation": pl.Utf8,
        "equipment_eq_bracing": pl.Utf8,
        "equipment_support_maintenance": pl.Utf8,
        "pounding": pl.Utf8,
        "ws_construction_quality": pl.Utf8,
        "roof_anchor": pl.Utf8,
        "roof_equipment_hurricane_bracing": pl.Utf8,
        "cladding_type": pl.Utf8,
        "frame_foundation_connection": pl.Utf8,
        "katrisk_score_fl": pl.Utf8,
        "catnet_score_wf": pl.Float64,
        "riskmeter_score_wf": pl.Int64,
        **{
            f"catnet_score_{peril}": pl.Utf8
            for peril in ["tn", "ha", "fl", "eq", "ws"]
        },
        **{
            f"risk_level_{peril}": pl.Utf8
            for peril in ["eq", "ws", "fl", "scs", "wf"]
        },
        "fema_flood": pl.Int64,
        "fema_flood_risk": pl.Utf8,
        "fema_flood_zone": pl.Utf8,
        "fema_flood_subzone": pl.Utf8,
        "fema_flood_combined_zone": pl.Utf8,
        "tiv_building_usd": pl.Float64,
        "tiv_contents_usd": pl.Float64,
        "tiv_contents1_usd": pl.Float64,
        "tiv_other_usd": pl.Float64,
        "tiv_bi_usd": pl.Float64,
        "tiv_total_usd": pl.Float64,
        **{
            f"score_category_{peril}": pl.Float64
            for peril in ["eq", "ws", "fl", "scs", "wf"]
        },
        # "output_by_layer": hx.List                                                  (mode="output", async_output=["run_schedule_rater_task", "load_into_schedule_task"], children={
        #     "layer_index": pl.Int64,
        #     **{
        #         f"deductible_usd_{peril}": pl.Float64
        #         for peril in ["fire", "eq", "ws", "fl", "scs"] 
        #     },
        #     **{
        #         f"sublimit_usd_{peril}": pl.Float64
        #         for peril in ["eq", "ws", "fl", "scs"]
        #     },
        #     "aal_post_uw_eq_us_usd_100": pl.Float64,
        #     "aal_post_uw_ws_us_usd_100": pl.Float64,
        #     "aal_pre_uw_eq_us_usd_100": pl.Float64,
        #     "aal_pre_uw_ws_us_usd_100": pl.Float64,
        #     **{
        #         f"coc_post_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
        #     },
        #     **{
        #         f"coc_pre_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
        #     },
        #     **{
        #         f"el_post_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fire_total", "fl", "ha", "tn", "total", "wf", "ws"]
        #     },
        #     **{
        #         f"el_pre_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fire_total", "fl", "ha", "tn", "total", "wf", "ws"]    
        #     },
        #     **{
        #         f"flc_entry_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
        #     },
        #     **{
        #         f"flc_exit_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
        #     },
        #     **{
        #         f"flc_worth_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]    
        #     },
        #     "lae_post_uw_eq_usd100": pl.Float64,
        #     "lae_post_uw_ws_usd100": pl.Float64,
        #     "lae_pre_uw_eq_usd100": pl.Float64,
        #     "lae_pre_uw_ws_usd100": pl.Float64,
        #     **{
        #         f"premtp_gn_max_post_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws", "total"]    
        #     },
        #     **{
        #         f"premtp_gn_max_pre_uw_usd_100_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws", "total"]    
        #     },
        #     **{
        #         f"rate_base_total_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]    
        #     },
        #     **{
        #         f"rate_gu_total_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]    
        #     },
        #     "ri_cost_post_uw_eq_usd100": pl.Float64,
        #     "ri_cost_post_uw_ws_usd100": pl.Float64,
        #     "ri_cost_pre_uw_eq_usd100": pl.Float64,
        #     "ri_cost_pre_uw_ws_usd100": pl.Float64,
        #     "sd_post_uw_eq_usd100": pl.Float64,
        #     "sd_post_uw_ws_usd100": pl.Float64,
        #     "sd_pre_uw_eq_usd100": pl.Float64,
        #     "sd_pre_uw_ws_usd100": pl.Float64,
        #     **{
        #         f"tivexposed_total_usd_{peril}": pl.Float64
        #         for peril in ["eq", "fire", "fl", "scs", "wf", "ws"]
        #     }
        # }),
        "cgear_score_total": pl.Float64,
        "rfr_basement_fl": pl.Float64,
        "rfr_bi_cbi": pl.Float64,
        "rfr_bi_indemnityperiod": pl.Float64,
        "rfr_bi_waitingperiod": pl.Float64,
        **{
            f"rfr_construction_{peril}": pl.Float64
            for peril in ["eq", "fire", "fl", "ha", "tn", "wf", "ws"]
        },
        "rfr_elevation_fl": pl.Float64,
        "rfr_floorarea_ha": pl.Float64,
        "rfr_floorarea_ws": pl.Float64,
        **{
            f"rfr_hazardscore_{peril}": pl.Float64
            for peril in ["eq", "fl", "ha", "tn", "wf", "ws"]
        },
        "rfr_hazardscoreriskmeter_wf": pl.Float64,
        "rfr_katriskscore_fl": pl.Float64,
        "rfr_mexicanfonden_fire": pl.Float64,
        "rfr_nofloors_eq": pl.Float64,
        "rfr_nofloors_fl": pl.Float64,
        "rfr_nofloors_ws": pl.Float64,
        **{
            f"rfr_occ_{peril}": pl.Float64
            for peril in ["eq", "ha", "tn", "wf", "ws"]
        },
        "rfr_ppc_fire": pl.Float64,
        "rfr_ppc_wf": pl.Float64,
        "rfr_riskquality_fire": pl.Float64,
        "rfr_roofage_ha": pl.Float64,
        "rfr_roofage_ws": pl.Float64,
        "rfr_roofcovering_ha": pl.Float64,
        "rfr_roofcovering_ws": pl.Float64,
        "rfr_roofgeometry_ha": pl.Float64,
        "rfr_roofgeometry_ws": pl.Float64,        
        **{
            f"rfr_sizedisc_{peril}": pl.Float64
            for peril in ["eq", "ha", "tn", "wf", "ws", "fl", "fire"]
        },        
        "rfr_sprinkler_fire": pl.Float64,
        "rfr_ss_ws": pl.Float64,
        **{
            f"rfr_yearbuilt_{peril}": pl.Float64
            for peril in ["eq", "ha", "tn", "ws"]
        },
}



def check_remodel(hxd):

    occ_df = (
        pl.DataFrame(hx.params.non_cat_base_rates)
        .filter(pl.col('Industry') != "")
        .rename({'Industry': 'industry', 'Occupancy': 'occupancy', 'ATC Occupancy Group': 'atc_occupancy'})
        .select(['industry', 'occupancy', 'atc_occupancy'])
    )

    em_map = pl.DataFrame(hx.params.ref_occupancy).rename({
        'Broker': 'rms_occupancy', 
        'Rater': 'occupancy',
        'Industry': 'industry'
    }).with_columns(pl.col("rms_occupancy").str.to_lowercase())

    if hxd.policy_information.small_schedule_model:    
        
        # Pull schedule
        columns = ['loc_id', 'rms_occupancy', 'tiv_total']
        df = pl.DataFrame([
            {"row_number": i} |
            {column: getattr(row, column) for column in columns} |
            {
                "rater_industry": row.industry_occupancy_dropdown.industry,
                "rater_occupancy": row.industry_occupancy_dropdown.occupancy,
            }
            for i, row in enumerate(hxd.schedule.schedule_table, start=1)
        ])
        
        if df.height == 1 and df['tiv_total'].sum() == 0:
            hxd.info.remodel_msg = "Schedule is empty"
            return

        df = df.with_columns([df["rms_occupancy"].cast(pl.Utf8)]).select(['row_number', 'loc_id', 'rater_industry', 'rater_occupancy', 'rms_occupancy'])

        # Remap EM column ATC code (same process as EM task)
        df = df.with_columns(pl.col("rms_occupancy").str.to_lowercase())
        df = df.join(em_map, on='rms_occupancy', how='left')
        df = df.join(occ_df, on=['industry', 'occupancy'], how='left')

        # Map rater industry occupancy to ATC code
        df = df.join(occ_df, left_on=['rater_industry', 'rater_occupancy'], right_on=['industry', 'occupancy'], how='left', suffix='_rater')

        # Check if ATC code changed
        df = df.with_columns((pl.col('atc_occupancy_rater') != pl.col('atc_occupancy')).alias('cols_not_equal'))
        
        remodel_flag = any(df.select('cols_not_equal').to_series().to_list())
        if remodel_flag:
            hxd.info.remodelling_needed = True
            hxd.info.remodelling_not_needed = False

            insured = hxd.policy_information.insured
            sender = ""
            recipient =""
            underwriter = hxd.policy_information.underwriter

            if underwriter:
                formatted_underwriter = underwriter.replace(" ", ".").lower()
                underwriter_email = formatted_underwriter + "@beazley.com"
                sender = underwriter_email
                recipient = underwriter_email
                hxd.email.sender = underwriter_email
                hxd.email.recipient = underwriter_email

            changed_df = df.filter(pl.col('cols_not_equal'))

            # Update cols order
            changed_df = changed_df.select(['row_number','loc_id','industry','occupancy','atc_occupancy','rater_industry','rater_occupancy','atc_occupancy_rater'])
            
            changed_df = changed_df.rename({
                "row_number": "Row #",
                "loc_id": "LocID",
                "industry": "Original NAICS Industry",
                "occupancy": "Original NAICS Occupancy",
                "atc_occupancy": "Modelled ATC Occupancy",
                "rater_industry": "Amended NAICS Industry",
                "rater_occupancy": "Amended NAICS Occupancy",
                "atc_occupancy_rater": "New Implied ATC Occupancy"
            })

            hxd.info.remodel_msg = "⚠️ Remodelling may be required. See *infobox* for details."
            email_msg = generate_email(data=changed_df, hxd=hxd, insured_name=insured, sender=sender, recipient=recipient)
            with hxd.email.remodelling_check_file.open("b") as file:
                gen = BytesGenerator(file, policy=policy.default)
                gen.flatten(email_msg)

        else:
            hxd.info.remodelling_needed = False
            hxd.info.remodelling_not_needed = True
            hxd.info.remodel_msg = "✅ No remodelling required"
        
def ind_occ_map(hxd, df):
    
    ind_occ_map = pl.from_pandas(hx.params.ind_occ_mapping)
    
    all_ind_occ_set = set(hx.params.non_cat_base_rates["Industry"] + " - " + hx.params.non_cat_base_rates["Occupancy"])
    live_ind_occ_set = set(hx.params.non_cat_base_rates_live_dropdown["Industry"] + " - " + hx.params.non_cat_base_rates_live_dropdown["Occupancy"])
    df_ind_occ_set = set((df["industry"] + " - " + df["occupancy"]).to_list())

    missing_live = df_ind_occ_set - live_ind_occ_set
    missing_all = df_ind_occ_set - all_ind_occ_set

    if missing_all:             # if the schedule ind-occs are not in the full base rate table (including old occupancies), return a fatal error 
        hx.errors.fatal(f"Please review the schedule. The following industry/occupancy pair(s) are not valid: {missing_all}")
    elif missing_live:          # if the schedule ind-occs are in the full base rate table, but not in the live-only base rate table, then remap them to live occupancies
        df = df.join(ind_occ_map, on=["industry", "occupancy"], how="left")
        df = df.with_columns([
            pl.when(( pl.col("industry_live").is_null() & pl.col("occupancy_live").is_null() ))
                .then(pl.col("industry"))
                .otherwise(pl.col("industry_live"))
                .alias("industry"),
            pl.when(( pl.col("industry_live").is_null() & pl.col("occupancy_live").is_null() ))
                .then(pl.col("occupancy"))
                .otherwise(pl.col("occupancy_live"))
                .alias("occupancy")
        ])
        df = df.drop(["industry_live", "occupancy_live"])
        
        # write to hxd
        industry_list = df["industry"].to_list()
        occupancy_list = df["occupancy"].to_list()
        for i, row in enumerate(hxd.schedule.schedule_table):
            row.industry_occupancy_dropdown.industry = industry_list[i]
            row.industry_occupancy_dropdown.occupancy = occupancy_list[i]

        url = r'https://beazley.sharepoint.com/:f:/r/sites/ActuarialPricing/Shared%20Documents/Property/Property%20User%20Guides/1.%20REX%20-%20Commercial%20Property/Occupancy%20Guide?csf=1&web=1&e=JJyHgZ'
        hxd.schedule.schedule_warnings = f"""The following occupancies are no longer used and have been remapped during the rating calculation. 
        *{"   |   ".join(missing_live)}*
        
        Please refer to the [occupancy guide]({url}) for more information.
        """
    else:                       # if the schedule ind-occs are all live
        pass
    
    return df



