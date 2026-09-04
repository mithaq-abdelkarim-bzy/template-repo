import hx
import polars as pl

def earthquake_rating_factor(hxd, df, other_data):

    df = earthquake_occupancy_rating_factor(hxd, df)
    df = earthquake_construction_rating_factor(hxd, df)
    df = earthquake_year_built_rating_factor(hxd, df)
    df = earthquake_num_floors_rating_factor(hxd, df)
    df = earthquake_construction_quality_rating_factor(hxd, df)
    df = earthquake_plan_irregularity_rating_factor(hxd, df)
    df = earthquake_soft_story_rating_factor(hxd, df)
    df = earthquake_vertical_irregularity_rating_factor(hxd, df)
    df = earthquake_ornamentation_rating_factor(hxd, df)
    df = earthquake_equipment_bracing_rating_factor(hxd, df)
    df = earthquake_equipment_maintenance_rating_factor(hxd, df)
    df = earthquake_pounding_rating_factor(hxd, df)
    df = earthquake_catnet_score_intl_rating_factor(hxd, df)

    return df


def earthquake_occupancy_rating_factor(hxd, df):

    # Load parameter tables
    eq_occupancy_rating_factor_df = hx.params.eq_occupancy_rating_factor
    intl_occupancy_rating_factor_df = hx.params.intl_occupancy_rating_factor

    value_vars = [str(index) for index in range(0, 55) if index != 45 and index != 46]

    eq_occupancy_rating_factor_pl = pl.from_pandas(eq_occupancy_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=value_vars, variable_name="atc_code", value_name="load"
    )

    eq_occupancy_rating_factor_pl.replace("atc_code", eq_occupancy_rating_factor_pl.select("atc_code").to_series().cast(pl.Int64))
    eq_occupancy_rating_factor_pl = eq_occupancy_rating_factor_pl.rename({"StateCounty": "state_county"})
    eq_occupancy_rating_factor_pl = eq_occupancy_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    )   

    occupancy_pl = df[["country", "state_county_lowercase", "atc_code"]].join(eq_occupancy_rating_factor_pl, on=["state_county_lowercase", "atc_code"], how="left")
    occupancy_pl = occupancy_pl.rename({"load": "us_load"}).fill_null(0)

    intl_occupancy_rating_factor_pl = pl.from_pandas(intl_occupancy_rating_factor_df[["Occupancy", "EQ"]]).rename({"Occupancy": "atc_code", "EQ": "intl_load"})
    occupancy_pl = occupancy_pl.join(intl_occupancy_rating_factor_pl, on="atc_code", how="left").fill_null(0)

    df = df.with_columns(
        occupancy_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("eq_occupancy_factor")
        )
    )

    return df


def earthquake_construction_rating_factor(hxd, df):

    # Load parameter tables
    eq_construction_rating_factor_df = hx.params.eq_construction_rating_factor
    construction_load_df = hx.params.construction_load

    # Calculate construction rating factor
    eq_construction_rating_factor_pl = pl.from_pandas(eq_construction_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=[str(index) for index in range(1, 7)], variable_name="constr_code", value_name="us_load"
    )

    eq_construction_rating_factor_pl.replace("constr_code", eq_construction_rating_factor_pl.select("constr_code").to_series().cast(pl.Int64))
    eq_construction_rating_factor_pl = eq_construction_rating_factor_pl.rename({"StateCounty": "state_county"})
    eq_construction_rating_factor_pl = eq_construction_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    construction_pl = df[["country", "state_county_lowercase", "constr_code"]].join(eq_construction_rating_factor_pl, on=["state_county_lowercase", "constr_code"], how="left").fill_null(0)

    intl_construction_rating_factor_pl = pl.from_pandas(construction_load_df[["ISO", "Int EQ"]]).rename({"ISO": "constr_code", "Int EQ": "intl_load"})
    construction_pl = construction_pl.join(intl_construction_rating_factor_pl, on="constr_code", how="left").fill_null(0)

    df = df.with_columns(
        construction_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("eq_construction_factor")
        )
    )

    return df


def earthquake_year_built_rating_factor(hxd, df):

    # Load parameter tables
    eq_year_built_rating_factor_df = hx.params.eq_year_built_rating_factor
    intl_year_built_rating_factor_df = hx.params.intl_year_built_rating_factor

    # Calculate year built rating factor
    eq_year_built_rating_factor_pl = pl.from_pandas(eq_year_built_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=["1900","1937","1974","1989", "2000"],  variable_name="year_built", value_name="us_load"
    )

    eq_year_built_rating_factor_pl.replace("year_built", eq_year_built_rating_factor_pl.select("year_built").to_series().cast(pl.Int64))
    eq_year_built_rating_factor_pl = eq_year_built_rating_factor_pl.rename({"StateCounty": "state_county"})
    eq_year_built_rating_factor_pl = eq_year_built_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    year_built_pl = df[["row_nr", "country", "state_county_lowercase", "year_built"]]

    year_built_pl = year_built_pl.with_columns(
        pl.col("year_built").fill_null(9999)
    )

    year_built_pl = year_built_pl.sort("year_built")
    eq_year_built_rating_factor_pl = eq_year_built_rating_factor_pl.sort("year_built")
    year_built_pl = year_built_pl.join_asof(eq_year_built_rating_factor_pl, on="year_built", by="state_county_lowercase")

    intl_year_built_rating_factor_pl = pl.from_pandas(intl_year_built_rating_factor_df[["Year", "EQ"]]).rename({"Year": "year_built", "EQ": "intl_load"})
    year_built_pl = year_built_pl.join_asof(intl_year_built_rating_factor_pl, on="year_built")

    year_built_pl = year_built_pl.sort("row_nr").fill_null(0)
    df = df.sort("row_nr")

    df = df.with_columns(
        year_built_pl.select(
            pl.when(pl.col("year_built") == 9999)
                .then(1)
                .when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("eq_year_built_factor")
        )        
    )

    return df


def earthquake_num_floors_rating_factor(hxd, df):

    # Load parameter tables
    eq_num_floors_rating_factor_df = hx.params.eq_num_floors_rating_factor
    intl_num_floors_rating_factor_df = hx.params.intl_num_floors_rating_factor

    # Calculate num floors rating factor
    eq_num_floors_rating_factor_pl = pl.from_pandas(eq_num_floors_rating_factor_df).melt(
        id_vars="StateCounty", value_vars=["1", "3", "4", "8", "16", "40", "80"], variable_name="num_stories", value_name="us_load"
    )

    eq_num_floors_rating_factor_pl.replace("num_stories", eq_num_floors_rating_factor_pl.select("num_stories").to_series().cast(pl.Int64))
    eq_num_floors_rating_factor_pl = eq_num_floors_rating_factor_pl.rename({"StateCounty": "state_county"})
    eq_num_floors_rating_factor_pl = eq_num_floors_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    num_floors_pl = df[["row_nr", "country", "state_county_lowercase", "num_stories"]].fill_null(0)

    num_floors_pl = num_floors_pl.sort("num_stories")
    eq_num_floors_rating_factor_pl = eq_num_floors_rating_factor_pl.sort("num_stories")
    num_floors_pl = num_floors_pl.join_asof(eq_num_floors_rating_factor_pl, on="num_stories", by="state_county_lowercase")

    intl_num_floors_rating_factor_pl = pl.from_pandas(intl_num_floors_rating_factor_df[["Floors", "EQ"]]).rename({"Floors": "num_stories", "EQ": "intl_load"})
    num_floors_pl = num_floors_pl.join_asof(intl_num_floors_rating_factor_pl, on="num_stories")

    num_floors_pl = num_floors_pl.sort("row_nr").fill_null(0)
    df = df.sort("row_nr")

    df = df.with_columns(
        num_floors_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1 + pl.col("us_load"))
                .otherwise(1 + pl.col("intl_load"))
                .alias("eq_num_floors_factor")
        )
    )

    return df


def earthquake_construction_quality_rating_factor(hxd, df):

    eq_construction_quality_rating_factor_df = hx.params.eq_construction_quality_rating_factor
    eq_construction_quality_rating_factor_pl = pl.from_pandas(eq_construction_quality_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Good", "Average", "Poor"],
        variable_name="eq_construction_quality", value_name="construction_quality_load"
    ).rename({"StateCounty": "state_county"})
    eq_construction_quality_rating_factor_pl = eq_construction_quality_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    construction_quality_pl = df[["state_county_lowercase", "eq_construction_quality"]].join(eq_construction_quality_rating_factor_pl, on=["state_county_lowercase", "eq_construction_quality"], how="left")

    df = df.with_columns(
        construction_quality_pl.select(
            (1 + pl.col("construction_quality_load"))
                .fill_null(1)
                .alias("eq_construction_quality_factor")
        )
    )

    return df


def earthquake_plan_irregularity_rating_factor(hxd, df):

    eq_plan_irregularity_rating_factor_df = hx.params.eq_plan_irregularity_rating_factor
    eq_plan_irregularity_rating_factor_pl = pl.from_pandas(eq_plan_irregularity_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Regular", "Irregular"],
        variable_name="plan_irregularity", value_name="plan_irregularity_load"
    ).rename({"StateCounty": "state_county"})
    eq_plan_irregularity_rating_factor_pl = eq_plan_irregularity_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    plan_irregularity_pl = df[["state_county_lowercase", "plan_irregularity"]].join(eq_plan_irregularity_rating_factor_pl, on=["state_county_lowercase", "plan_irregularity"], how="left")

    df = df.with_columns(
        plan_irregularity_pl.select(
            (1 + pl.col("plan_irregularity_load"))
                .fill_null(1)
                .alias("eq_plan_irregularity_factor")
        )
    )

    return df


def earthquake_soft_story_rating_factor(hxd, df):

    eq_soft_story_rating_factor_df = hx.params.eq_soft_story_rating_factor
    eq_soft_story_rating_factor_pl = pl.from_pandas(eq_soft_story_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "No", "Yes"],
        variable_name="soft_story", value_name="soft_story_load"
    ).rename({"StateCounty": "state_county"})
    eq_soft_story_rating_factor_pl = eq_soft_story_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    soft_story_pl = df[["state_county_lowercase", "soft_story"]].join(eq_soft_story_rating_factor_pl, on=["state_county_lowercase", "soft_story"], how="left")

    df = df.with_columns(
        soft_story_pl.select(
            (1 + pl.col("soft_story_load"))
                .fill_null(1)
                .alias("eq_soft_story_factor")
        )
    )


    return df


def earthquake_vertical_irregularity_rating_factor(hxd, df):
    
    eq_vertical_irregularity_rating_factor_df = hx.params.eq_vertical_irregularity_rating_factor
    eq_vertical_irregularity_rating_factor_pl = pl.from_pandas(eq_vertical_irregularity_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "No", "Yes"],
        variable_name="vertical_irregularity", value_name="vertical_irregularity_load"
    ).rename({"StateCounty": "state_county"})
    eq_vertical_irregularity_rating_factor_pl = eq_vertical_irregularity_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    vertical_irregularity_pl = df[["state_county_lowercase", "vertical_irregularity"]].join(eq_vertical_irregularity_rating_factor_pl, on=["state_county_lowercase", "vertical_irregularity"], how="left")

    df = df.with_columns(
        vertical_irregularity_pl.select(
            (1 + pl.col("vertical_irregularity_load"))
                .fill_null(1)
                .alias("eq_vertical_irregularity_factor")
        )
    )

    return df


def earthquake_ornamentation_rating_factor(hxd, df):

    eq_ornamentation_rating_factor_df = hx.params.eq_ornamentation_rating_factor
    eq_ornamentation_rating_factor_pl = pl.from_pandas(eq_ornamentation_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Little or None", "Average", "Extensive"],
        variable_name="ornamentation", value_name="ornamentation_load"
    ).rename({"StateCounty": "state_county"})
    eq_ornamentation_rating_factor_pl = eq_ornamentation_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    ornamentation_pl = df[["state_county_lowercase", "ornamentation"]].join(eq_ornamentation_rating_factor_pl, on=["state_county_lowercase", "ornamentation"], how="left")

    df = df.with_columns(
        ornamentation_pl.select(
            (1 + pl.col("ornamentation_load"))
                .fill_null(1)
                .alias("eq_ornamentation_factor")
        )
    )

    return df


def earthquake_equipment_bracing_rating_factor(hxd, df):

    eq_equipment_bracing_rating_factor_df = hx.params.eq_equipment_bracing_rating_factor
    eq_equipment_bracing_rating_factor_pl = pl.from_pandas(eq_equipment_bracing_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "Generally Well-Braced", "Somewhat Braced", "Generally Unbraced"],
        variable_name="equipment_eq_bracing", value_name="equipment_bracing_load"
    ).rename({"StateCounty": "state_county"})
    eq_equipment_bracing_rating_factor_pl = eq_equipment_bracing_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    equipment_bracing_pl = df[["state_county_lowercase", "equipment_eq_bracing"]].join(eq_equipment_bracing_rating_factor_pl, on=["state_county_lowercase", "equipment_eq_bracing"], how="left")

    df = df.with_columns(
        equipment_bracing_pl.select(
            (1 + pl.col("equipment_bracing_load"))
                .fill_null(1)
                .alias("eq_equipment_bracing_factor")
        )
    )

    return df


def earthquake_equipment_maintenance_rating_factor(hxd, df):

    eq_equipment_maintenance_rating_factor_df = hx.params.eq_equipment_maintenance_rating_factor
    eq_equipment_maintenance_rating_factor_pl = pl.from_pandas(eq_equipment_maintenance_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "No Signs of Fatigue / Good Maintenance", "Few Signs of Fatigue / Average Maintenance", "Obvious Signs of Fatigue / Poor Maintenance"],
        variable_name="equipment_support_maintenance", value_name="equipment_maintenance_load"
    ).rename({"StateCounty": "state_county"})
    eq_equipment_maintenance_rating_factor_pl = eq_equipment_maintenance_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    equipment_maintenance_pl = df[["state_county_lowercase", "equipment_support_maintenance"]].join(eq_equipment_maintenance_rating_factor_pl, on=["state_county_lowercase", "equipment_support_maintenance"], how="left")

    df = df.with_columns(
        equipment_maintenance_pl.select(
            (1 + pl.col("equipment_maintenance_load"))
                .fill_null(1)
                .alias("eq_equipment_maintenance_factor")
        )
    )

    return df


def earthquake_pounding_rating_factor(hxd, df):

    eq_pounding_rating_factor_df = hx.params.eq_pounding_rating_factor
    eq_pounding_rating_factor_pl = pl.from_pandas(eq_pounding_rating_factor_df).melt(
        id_vars="StateCounty",
        value_vars=["Unknown", "No", "Yes"],
        variable_name="pounding", value_name="pounding_load"
    ).rename({"StateCounty": "state_county"})
    eq_pounding_rating_factor_pl = eq_pounding_rating_factor_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    pounding_pl = df[["state_county_lowercase", "pounding"]].join(eq_pounding_rating_factor_pl, on=["state_county_lowercase", "pounding"], how="left")

    df = df.with_columns(
        pounding_pl.select(
            (1 + pl.col("pounding_load"))
                .fill_null(1)
                .alias("eq_pounding_factor")
        )
    )

    return df


def earthquake_catnet_score_intl_rating_factor(hxd, df):

    eq_catnet_score_df = hx.params.eq_catnet_score

    # Windstorm Risk Level
    eq_catnet_score_pl = pl.from_pandas(eq_catnet_score_df)[["Score Band", "Load"]]
    eq_catnet_score_pl = eq_catnet_score_pl.rename({"Score Band": "catnet_score_eq", "Load": "eq_catnet_load"})

    catnet_pl = df[["country", "catnet_score_eq"]].join(eq_catnet_score_pl, on="catnet_score_eq", how="left")

    df = df.with_columns(
        catnet_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1)
                .otherwise(1 + pl.col("eq_catnet_load"))
                .fill_null(1)
                .alias("eq_catnet_intl_factor")
        )
    )


    return df


def earthquake_us_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        (
            pl.col("eq_occupancy_factor") * pl.col("eq_construction_factor") * pl.col("eq_year_built_factor") * pl.col("eq_num_floors_factor") *
            pl.col("eq_construction_quality_factor") * pl.col("eq_plan_irregularity_factor") * pl.col("eq_soft_story_factor") * pl.col("eq_vertical_irregularity_factor") *
            pl.col("eq_ornamentation_factor") * pl.col("eq_equipment_bracing_factor") * pl.col("eq_equipment_maintenance_factor") * pl.col("eq_pounding_factor")
        ).alias("earthquake_us_buildings_total_adjustment")
    )

    df = df.with_columns(
        [
            pl.col("earthquake_us_buildings_total_adjustment").alias("earthquake_us_contents_total_adjustment"),
            (pl.col("earthquake_us_buildings_total_adjustment") * pl.col('bi_waiting_period_factor') * 
                other_data['bi_indemnity_period_factor'] * other_data['cbi_load'])
                .alias("earthquake_us_bi_total_adjustment")
        ]
    )

    return df


def earthquake_intl_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        [
            (pl.col("earthquake_us_buildings_total_adjustment") * pl.col("eq_catnet_intl_factor")).alias("earthquake_intl_buildings_total_adjustment"),
            (pl.col("earthquake_us_contents_total_adjustment") * pl.col("eq_catnet_intl_factor")).alias("earthquake_intl_contents_total_adjustment"),
            (pl.col("earthquake_us_bi_total_adjustment") * pl.col("eq_catnet_intl_factor")).alias("earthquake_intl_bi_total_adjustment")
        ]
    )

    return df