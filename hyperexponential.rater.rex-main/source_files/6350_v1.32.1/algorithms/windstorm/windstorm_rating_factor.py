import hx
import polars as pl


def windstorm_rating_factor(hxd, df, other_data):

    df = windstorm_occupancy_rating_factor(hxd, df)
    df = windstorm_construction_rating_factor(hxd, df)
    df = windstorm_year_built_rating_factor(hxd, df)
    df = windstorm_floor_area_rating_factor(hxd, df)
    df = windstorm_num_floors_rating_factor(hxd, df)
    df = windstorm_roof_age_rating_factor(hxd, df)
    df = windstorm_roof_covering_rating_factor(hxd, df)
    df = windstorm_roof_geometry_rating_factor(hxd, df)
    df = windstorm_construction_quality_rating_factor(hxd, df)
    df = windstorm_roof_anchor_rating_factor(hxd, df)
    df = windstorm_roof_bracing_rating_factor(hxd, df)
    df = windstorm_cladding_type_rating_factor(hxd, df)
    df = windstorm_frame_connection_rating_factor(hxd, df)
    df = windstorm_storm_surge_rating_factor(hxd, df)
    df = windstorm_catnet_score_intl_rating_factor(hxd, df)

    return df


def windstorm_occupancy_rating_factor(hxd, df):

    # Load parameter tables
    ws_occupancy_rating_factor_df = hx.params.ws_occupancy_rating_factor
    intl_occupancy_rating_factor_df = hx.params.intl_occupancy_rating_factor
    non_cat_base_rates_df = hx.params.non_cat_base_rates

    # Calculate occupancy rating factor
    non_cat_base_rates_pl = pl.from_pandas(non_cat_base_rates_df[["Key", "ATC Code"]]).rename({
                                "Key": "industry_occupancy",
                                "ATC Code": "atc_code"
                            })
    
    df = df.join(non_cat_base_rates_pl, on="industry_occupancy", how="left")
    
    value_vars = [str(index) for index in range(0, 55) if index != 45 and index != 46]

    ws_occupancy_rating_factor_pl = pl.from_pandas(ws_occupancy_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=value_vars, variable_name="atc_code", value_name="load"
    )

    ws_occupancy_rating_factor_pl.replace("atc_code", ws_occupancy_rating_factor_pl.select("atc_code").to_series().cast(pl.Int64))
    ws_occupancy_rating_factor_pl = ws_occupancy_rating_factor_pl.rename({"StateCounty": "state_county"})
    ws_occupancy_rating_factor_pl = ws_occupancy_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    occupancy_pl = df[["country", "state_county_lowercase", "atc_code"]].join(ws_occupancy_rating_factor_pl, on=["state_county_lowercase", "atc_code"], how="left")
    occupancy_pl = occupancy_pl.rename({"load": "us_load"}).fill_null(0)

    intl_occupancy_rating_factor_pl = pl.from_pandas(intl_occupancy_rating_factor_df[["Occupancy", "WS"]]).rename({"Occupancy": "atc_code", "WS": "intl_load"})
    occupancy_pl = occupancy_pl.join(intl_occupancy_rating_factor_pl, on="atc_code", how="left").fill_null(0)

    df = df.with_columns(
        occupancy_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("ws_occupancy_factor")
        )
    )

    return df


def windstorm_construction_rating_factor(hxd, df):

    # Load parameter tables
    ws_construction_rating_factor_df = hx.params.ws_construction_rating_factor
    construction_load_df = hx.params.construction_load
  
    # Calculate construction rating factor
    ws_construction_rating_factor_pl = pl.from_pandas(ws_construction_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=[str(index) for index in range(1, 7)], variable_name="constr_code", value_name="us_load"
    )

    ws_construction_rating_factor_pl.replace("constr_code", ws_construction_rating_factor_pl.select("constr_code").to_series().cast(pl.Int64))
    ws_construction_rating_factor_pl = ws_construction_rating_factor_pl.rename({"StateCounty": "state_county"})
    ws_construction_rating_factor_pl = ws_construction_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    construction_pl = df[["country", "state_county_lowercase", "constr_code"]].join(ws_construction_rating_factor_pl, on=["state_county_lowercase", "constr_code"], how="left").fill_null(0)

    intl_construction_rating_factor_pl = pl.from_pandas(construction_load_df[["ISO", "Int WS"]]).rename({"ISO": "constr_code", "Int WS": "intl_load"})
    construction_pl = construction_pl.join(intl_construction_rating_factor_pl, on="constr_code", how="left").fill_null(0)

    df = df.with_columns(
        construction_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("ws_construction_factor")
        )
    )

    return df


def windstorm_year_built_rating_factor(hxd, df):
    
    # Load parameter tables
    ws_year_built_rating_factor_df = hx.params.ws_year_built_rating_factor
    intl_year_built_rating_factor_df = hx.params.intl_year_built_rating_factor

    # Calculate year built rating factor
    ws_year_built_rating_factor_pl = pl.from_pandas(ws_year_built_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=["1900","1995","2002","2009"],  variable_name="year_built_us_lookup", value_name="us_load"
    )

    ws_year_built_rating_factor_pl.replace("year_built_us_lookup", ws_year_built_rating_factor_pl.select("year_built_us_lookup").to_series().cast(pl.Int64))
    ws_year_built_rating_factor_pl = ws_year_built_rating_factor_pl.rename({"StateCounty": "state_county"})
    ws_year_built_rating_factor_pl = ws_year_built_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    year_built_pl = df[["row_nr", "country", "state_county_lowercase", "year_built"]].join(ws_year_built_rating_factor_pl, on="state_county_lowercase", how="left")
    year_built_pl = year_built_pl.filter((pl.col("year_built") == None) | (pl.col("year_built_us_lookup") <= pl.col("year_built")))
    year_built_pl = year_built_pl.groupby("row_nr", maintain_order=True).last()
    year_built_pl = df[["row_nr", "country"]].join(year_built_pl, on=["row_nr", "country"], how="left").fill_null(0)

    intl_year_built_rating_factor_pl = pl.from_pandas(intl_year_built_rating_factor_df[["Year", "WS"]]).rename({"Year": "year_built", "WS": "intl_load"})
    year_built_pl = year_built_pl.replace("year_built", df["year_built"].fill_null(9999))
    year_built_pl = year_built_pl.sort("year_built")
    year_built_pl = year_built_pl.join_asof(intl_year_built_rating_factor_pl, on="year_built")

    year_built_pl = year_built_pl.sort("row_nr")
    df = df.sort("row_nr")

    df = df.with_columns(
        year_built_pl.select(
            pl.when(pl.col("year_built") == 9999)
                .then(1)
                .when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .fill_nan(1)
                .alias("ws_year_built_factor")
        )        
    )    

    return df


def windstorm_floor_area_rating_factor(hxd, df):

    # Load parameter tables
    ws_floor_area_rating_factor_df = hx.params.ws_floor_area_rating_factor
    intl_floor_area_rating_factor_df = hx.params.intl_floor_area_rating_factor

    # Create temp table
    floor_area_pl = df[["row_nr", "country", "state_county_lowercase", "num_stories", "floor_area"]]
    floor_area_pl = floor_area_pl.with_columns(
        (
            pl.when(pl.col("num_stories") == 0)
                .then(0)
                .otherwise(pl.col("floor_area") / pl.col("num_stories"))
                .fill_null(0)
                .cast(pl.Float64)
                .alias("area_per_floor")
        )
    )

    # Calculate floor area rating factor
    ws_floor_area_rating_factor_pl = pl.from_pandas(ws_floor_area_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=[x for x in ws_floor_area_rating_factor_df.columns if x != "StateCounty"], variable_name="area_per_floor", value_name="us_load"
    )

    ws_floor_area_rating_factor_pl = ws_floor_area_rating_factor_pl.with_columns(pl.col("area_per_floor").cast(pl.Float64).alias("area_per_floor"))
    ws_floor_area_rating_factor_pl = ws_floor_area_rating_factor_pl.rename({"StateCounty": "state_county"})
    ws_floor_area_rating_factor_pl = ws_floor_area_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    floor_area_pl = floor_area_pl.sort("area_per_floor")
    floor_area_pl = floor_area_pl.join_asof(ws_floor_area_rating_factor_pl, on="area_per_floor", by="state_county_lowercase", strategy="backward")  # TODO Check this is less than

    intl_floor_area_rating_factor_pl = pl.from_pandas(intl_floor_area_rating_factor_df[["Area", "WS"]]).rename({"Area": "area_per_floor", "WS": "intl_load"})

    # already sorted above so don't need to sort again for asof
    floor_area_pl = floor_area_pl.join_asof(intl_floor_area_rating_factor_pl, on="area_per_floor")

    floor_area_pl = floor_area_pl.sort("row_nr").fill_null(0)
    df = df.sort("row_nr")

    df = df.with_columns(
        floor_area_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("ws_floor_area_factor")
        )
    )

    return df


def windstorm_num_floors_rating_factor(hxd, df):

    # Load parameter tables
    ws_num_floors_rating_factor_df = hx.params.ws_num_floors_rating_factor
    intl_num_floors_rating_factor_df = hx.params.intl_num_floors_rating_factor

    # Calculate num floors rating factor
    ws_num_floors_rating_factor_pl = pl.from_pandas(ws_num_floors_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=["1", "2", "3", "4", "5", "6", "8", "12", "20", "40", "80"], variable_name="num_stories", value_name="us_load"
    )

    ws_num_floors_rating_factor_pl.replace("num_stories", ws_num_floors_rating_factor_pl.select("num_stories").to_series().cast(pl.Int64))
    ws_num_floors_rating_factor_pl = ws_num_floors_rating_factor_pl.rename({"StateCounty": "state_county"})
    ws_num_floors_rating_factor_pl = ws_num_floors_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    num_floors_pl = df[["row_nr", "country", "state_county_lowercase", "num_stories"]].fill_null(0)

    num_floors_pl = num_floors_pl.sort("num_stories")
    ws_num_floors_rating_factor_pl = ws_num_floors_rating_factor_pl.sort("num_stories")
    num_floors_pl = num_floors_pl.join_asof(ws_num_floors_rating_factor_pl, on="num_stories", by="state_county_lowercase")

    intl_num_floors_rating_factor_pl = pl.from_pandas(intl_num_floors_rating_factor_df[["Floors", "WS"]]).rename({"Floors": "num_stories", "WS": "intl_load"})
    num_floors_pl = num_floors_pl.join_asof(intl_num_floors_rating_factor_pl, on="num_stories")

    num_floors_pl = num_floors_pl.sort("row_nr").fill_null(0)
    df = df.sort("row_nr")

    df = df.with_columns(
        num_floors_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("ws_num_floors_factor")
        )
    )

    return df


def windstorm_roof_age_rating_factor(hxd, df):

    # Load parameter tables
    ws_roof_age_description_mapping_df = hx.params.ws_roof_age_description_mapping
    ws_roof_age_rating_factor_df = hx.params.ws_roof_age_rating_factor

    # Calculate roof age rating factor
    ws_roof_age_description_mapping_pl = pl.from_pandas(ws_roof_age_description_mapping_df).rename({"Lower Bound": "update_year_diff", "Age": "update_year_age_desc"})

    roof_age_pl = df[["row_nr", "state_county_lowercase", "year_built", "year_cov_last_replaced", "roof_age"]]

    roof_age_pl = roof_age_pl.with_columns(
        pl.when((pl.col("year_cov_last_replaced") == None) | (pl.col("year_cov_last_replaced") == 9999))
            .then(pl.col("year_built"))
            .otherwise(pl.col("year_cov_last_replaced"))
            .fill_null(9999)
            .alias("year_cov_last_replaced")
    )

    roof_age_pl = roof_age_pl.with_columns(
        (hxd.hx_core.inception_date.year - pl.col("year_cov_last_replaced")).alias("update_year_diff")
    )

    roof_age_pl = roof_age_pl.sort("update_year_diff")
    roof_age_pl = roof_age_pl.join_asof(ws_roof_age_description_mapping_pl, on="update_year_diff")
    roof_age_pl = roof_age_pl.sort("row_nr").fill_null("Unknown")

    roof_age_pl = roof_age_pl.with_columns(
        pl.when(pl.col("roof_age") != None)
            .then(pl.col("roof_age"))
            .when((pl.col("year_built") == None) | pl.col("year_built") == 0)
            .then("Unknown")
            .otherwise("update_year_age_desc")
            .alias("age_description")
    )

    ws_roof_age_rating_factor_pl = pl.from_pandas(ws_roof_age_rating_factor_df).melt(
        id_vars="StateCounty", 
        value_vars=["Unknown", "0-5 years", "6-10 years", "11+ years", "Obvious signs of deterioration or distress"], 
        variable_name="age_description", value_name="roof_age_load"
    ).rename({"StateCounty": "state_county"})
    ws_roof_age_rating_factor_pl = ws_roof_age_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    roof_age_pl = roof_age_pl.join(ws_roof_age_rating_factor_pl, on=["state_county_lowercase", "age_description"], how="left").fill_null(0)

    roof_age_pl = roof_age_pl.sort("row_nr")
    df = df.sort("row_nr")

    df = df.with_columns(
        roof_age_pl.select(
            (1 + pl.col("roof_age_load"))
                .alias("ws_roof_age_factor")
        )
    )

    return df


def windstorm_roof_covering_rating_factor(hxd, df):

    ws_roof_covering_rating_factor_df = hx.params.ws_roof_covering_rating_factor
    ws_roof_covering_rating_factor_pl = pl.from_pandas(ws_roof_covering_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Metal sheathing", "Built-up or single ply membrane", "Concrete/clay tiles",
                        "Wood shakes", "Normal shingle", "Shingle rated for high wind speeds"],
        variable_name="roof_covering", value_name="roof_covering_load"
    ).rename({"StateCounty": "state_county"})
    ws_roof_covering_rating_factor_pl = ws_roof_covering_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    roof_covering_pl = df[["state_county_lowercase", "roof_covering"]].join(ws_roof_covering_rating_factor_pl, on=["state_county_lowercase", "roof_covering"], how="left")

    df = df.with_columns(
        roof_covering_pl.select(
            (1 + pl.col("roof_covering_load"))
                .fill_null(1)
                .alias("ws_roof_covering_factor")
        )
    )

    return df


def windstorm_roof_geometry_rating_factor(hxd, df):

    ws_roof_geometry_rating_factor_df = hx.params.ws_roof_geometry_rating_factor
    ws_roof_geometry_rating_factor_pl = pl.from_pandas(ws_roof_geometry_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Flat roof with Parapets", "Flat roof without Parapets",
                        "Hip roof", "Gable roof", "Braced gable roof"],
        variable_name="roof_geometry", value_name="roof_geometry_load"
    ).rename({"StateCounty": "state_county"})
    ws_roof_geometry_rating_factor_pl = ws_roof_geometry_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    roof_geometry_pl = df[["state_county_lowercase", "roof_geometry"]].join(ws_roof_geometry_rating_factor_pl, on=["state_county_lowercase", "roof_geometry"], how="left")

    df = df.with_columns(
        roof_geometry_pl.select(
            (1 + pl.col("roof_geometry_load"))
                .fill_null(1)
                .alias("ws_roof_geometry_factor")
        )
    )

    return df


def windstorm_construction_quality_rating_factor(hxd, df):

    ws_construction_quality_rating_factor_df = hx.params.ws_construction_quality_rating_factor
    ws_construction_quality_rating_factor_pl = pl.from_pandas(ws_construction_quality_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Obvious signs of deterioration or distress", "Certified design & construction"],
        variable_name="ws_construction_quality", value_name="construction_quality_load"
    ).rename({"StateCounty": "state_county"})
    ws_construction_quality_rating_factor_pl = ws_construction_quality_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    construction_quality_pl = df[["state_county_lowercase", "ws_construction_quality"]].join(ws_construction_quality_rating_factor_pl, on=["state_county_lowercase", "ws_construction_quality"], how="left")

    df = df.with_columns(
        construction_quality_pl.select(
            (1 + pl.col("construction_quality_load"))
                .fill_null(1)
                .alias("ws_construction_quality_factor")
        )
    )

    return df


def windstorm_roof_anchor_rating_factor(hxd, df):

    ws_roof_anchor_rating_factor_df = hx.params.ws_roof_anchor_rating_factor
    ws_roof_anchor_rating_factor_pl = pl.from_pandas(ws_roof_anchor_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Toe nailing or no anchorage", "Clips", "Single wraps", "Double wraps", "Structural"],
        variable_name="roof_anchor", value_name="roof_anchor_load"
    ).rename({"StateCounty": "state_county"})
    ws_roof_anchor_rating_factor_pl = ws_roof_anchor_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    roof_anchor_pl = df[["state_county_lowercase", "roof_anchor"]].join(ws_roof_anchor_rating_factor_pl, on=["state_county_lowercase", "roof_anchor"], how="left")

    df = df.with_columns(
        roof_anchor_pl.select(
            (1 + pl.col("roof_anchor_load"))
                .fill_null(1)
                .alias("ws_roof_anchor_factor")
        )
    )

    return df


def windstorm_roof_bracing_rating_factor(hxd, df):

    ws_roof_bracing_rating_factor_df = hx.params.ws_roof_bracing_rating_factor
    ws_roof_bracing_rating_factor_pl = pl.from_pandas(ws_roof_bracing_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Properly installed with adequate anchorage", "Obvious signs of deficiencies in the installation", "No equipment present"],
        variable_name="roof_equipment_hurricane_bracing", value_name="roof_bracing_load"
    ).rename({"StateCounty": "state_county"})
    ws_roof_bracing_rating_factor_pl = ws_roof_bracing_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    roof_bracing_pl = df[["state_county_lowercase", "roof_equipment_hurricane_bracing"]].join(ws_roof_bracing_rating_factor_pl, on=["state_county_lowercase", "roof_equipment_hurricane_bracing"], how="left")

    df = df.with_columns(
        roof_bracing_pl.select(
            (1 + pl.col("roof_bracing_load"))
                .fill_null(1)
                .alias("ws_roof_bracing_factor")
        )
    )

    return df


def windstorm_cladding_type_rating_factor(hxd, df):

    ws_cladding_type_rating_factor_df = hx.params.ws_cladding_type_rating_factor
    ws_cladding_type_rating_factor_pl = pl.from_pandas(ws_cladding_type_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Brick Veneer", "Metal Sheathing", "Wood", "EIFS", "Impact rated glazing", "Glazing not designed for impact WITH gravel rooftop within 1,000 ft",
                        "Glazing not designed for impact without gravel rooftop within 1,000 ft", "Vinyl siding", "Stucco", "None"],
        variable_name="cladding_type", value_name="cladding_type_load"
    ).rename({"StateCounty": "state_county"})
    ws_cladding_type_rating_factor_pl = ws_cladding_type_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    cladding_type_pl = df[["state_county_lowercase", "cladding_type"]].join(ws_cladding_type_rating_factor_pl, on=["state_county_lowercase", "cladding_type"], how="left")

    df = df.with_columns(
        cladding_type_pl.select(
            (1 + pl.col("cladding_type_load"))
                .fill_null(1)
                .alias("ws_cladding_type_factor")
        )
    )

    return df


def windstorm_frame_connection_rating_factor(hxd, df):

    ws_frame_connection_rating_factor_df = hx.params.ws_frame_connection_rating_factor
    ws_frame_connection_rating_factor_pl = pl.from_pandas(ws_frame_connection_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Bolted", "Unbolted", "Engineered"],
        variable_name="frame_foundation_connection", value_name="frame_connection_load"
    ).rename({"StateCounty": "state_county"})
    ws_frame_connection_rating_factor_pl = ws_frame_connection_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    frame_connection_pl = df[["state_county_lowercase", "frame_foundation_connection"]].join(ws_frame_connection_rating_factor_pl, on=["state_county_lowercase", "frame_foundation_connection"], how="left")

    df = df.with_columns(
        frame_connection_pl.select(
            (1 + pl.col("frame_connection_load"))
                .fill_null(1)
                .alias("ws_frame_connection_factor")
        )
    )

    return df


def windstorm_storm_surge_rating_factor(hxd, df):

    ws_storm_surge_rating_factor_df = hx.params.ws_storm_surge_rating_factor
    ws_storm_surge_rating_factor_pl = pl.from_pandas(ws_storm_surge_rating_factor_df).rename({"StateCounty": "state_county", "Storm Surge": "storm_surge_load"})
    ws_storm_surge_rating_factor_pl = ws_storm_surge_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    storm_surge_pl = df[["state_county_lowercase", "distance_from_coast"]].join(ws_storm_surge_rating_factor_pl, on="state_county_lowercase", how="left").fill_null(0)

    df = df.with_columns(
        storm_surge_pl.select(
            pl.when(pl.col("distance_from_coast") > 1)
                .then(1 + pl.col("storm_surge_load"))
                .otherwise(1)
                .alias("ws_storm_surge_factor")
        )
    )

    return df


def windstorm_catnet_score_intl_rating_factor(hxd, df):

    ws_catnet_score_df = hx.params.ws_catnet_score

    # Windstorm Risk Level
    ws_catnet_score_pl = pl.from_pandas(ws_catnet_score_df)[["Score Band", "Load"]]
    ws_catnet_score_pl = ws_catnet_score_pl.rename({"Score Band": "catnet_score_ws", "Load": "ws_catnet_load"})

    catnet_pl = df[["country", "catnet_score_ws"]].join(ws_catnet_score_pl, on="catnet_score_ws", how="left")

    df = df.with_columns(
        catnet_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1)
                .otherwise(1 + pl.col("ws_catnet_load"))
                .fill_null(1)
                .alias("ws_catnet_intl_factor")
        )
    )

    return df


def windstorm_us_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        (
            pl.col("ws_occupancy_factor") * pl.col("ws_construction_factor") * pl.col("ws_year_built_factor") * pl.col("ws_floor_area_factor") *
            pl.col("ws_num_floors_factor") * pl.col("ws_roof_age_factor") * pl.col("ws_roof_covering_factor") * pl.col("ws_roof_geometry_factor") *
            pl.col("ws_construction_quality_factor") * pl.col("ws_roof_anchor_factor") * pl.col("ws_roof_bracing_factor") * pl.col("ws_cladding_type_factor") *
            pl.col("ws_frame_connection_factor") * pl.col("ws_storm_surge_factor")
        ).alias("windstorm_us_buildings_total_adjustment")
    )

    df = df.with_columns(
        [
            pl.col("windstorm_us_buildings_total_adjustment").alias("windstorm_us_contents_total_adjustment"),
            (pl.col("windstorm_us_buildings_total_adjustment") * pl.col('bi_waiting_period_factor') * 
                other_data['bi_indemnity_period_factor'] * other_data['cbi_load'])
                .alias("windstorm_us_bi_total_adjustment")
        ]
    )

    return df


def windstorm_intl_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        [
            (pl.col("windstorm_us_buildings_total_adjustment") * pl.col("ws_catnet_intl_factor")).alias("windstorm_intl_buildings_total_adjustment"),
            (pl.col("windstorm_us_contents_total_adjustment") * pl.col("ws_catnet_intl_factor")).alias("windstorm_intl_contents_total_adjustment"),
            (pl.col("windstorm_us_bi_total_adjustment") * pl.col("ws_catnet_intl_factor")).alias("windstorm_intl_bi_total_adjustment")
        ]
    )

    return df