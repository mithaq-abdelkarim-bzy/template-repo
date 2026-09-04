import hx
import polars as pl
import gc
from algorithms.analytical_curves import size_discount

def flood_rating_factor(hxd, df, other_data):

    df = flood_katrisk_score_rating_factor(hxd, df)
    df = flood_construction_rating_factor(hxd, df)
    df = flood_num_floors_rating_factor(hxd, df)
    df = flood_basement_rating_factor(hxd, df)
    df = flood_elevation_rating_factor(hxd, df)
    df = flood_catnet_score_intl_rating_factor(hxd, df)
    df = flood_size_discount_rating_factor(hxd, df, other_data)

    return df


def flood_katrisk_score_rating_factor(hxd, df):

    # Load parameter tables
    fl_katrisk_score_df = hx.params.fl_katrisk_score
    
    fl_katrisk_score_pl = pl.from_pandas(fl_katrisk_score_df[["KatRisk Score", "Load"]])
    fl_katrisk_score_pl = fl_katrisk_score_pl.rename(
                            {"KatRisk Score": "katrisk_score_fl", "Load": "fl_katrisk_risk_rating_factor"}
                        )

    fl_katrisk_score_pl = fl_katrisk_score_pl.with_columns(pl.col("katrisk_score_fl").cast(pl.Int64, strict=False).alias("katrisk_score_fl"))
    df = df.with_columns(pl.col("katrisk_score_fl").cast(pl.Float64, strict=False).cast(pl.Int64).alias("katrisk_score_fl"))

    df = df.join(fl_katrisk_score_pl, on="katrisk_score_fl", how="left")
        
    df = df.with_columns(
        (1 + pl.col("fl_katrisk_risk_rating_factor"))
            .fill_null(1)
            .alias("fl_katrisk_risk_rating_factor")
    )

    return df


def flood_construction_rating_factor(hxd, df):

    # Load parameter table
    construction_load_df = hx.params.construction_load

    construction_load_pl = pl.from_pandas(construction_load_df[["ISO", "Flood"]]).rename({"ISO": "constr_code", "Flood": "fl_construction_rating_factor"})
    df = df.join(construction_load_pl, on="constr_code", how="left").fill_null(0)

    df = df.with_columns(
        (1 + pl.col("fl_construction_rating_factor"))
            .fill_null(1)
            .alias("fl_construction_rating_factor")
    )

    return df


def flood_num_floors_rating_factor(hxd, df):

    # Load parameter table
    floors_df = hx.params.floors

    floors_pl = pl.from_pandas(floors_df).rename({"No. Floors": "num_stories", "Weight": "fl_num_floors_rating_factor"})
    df = df.sort("num_stories")
    df = df.join_asof(floors_pl, on="num_stories")
    df = df.sort("row_nr")
    df = df.with_columns(pl.col("fl_num_floors_rating_factor").fill_null(1))

    return df


def flood_basement_rating_factor(hxd, df):

    # Load parameter table
    basement_df = hx.params.basement

    basement_pl = pl.from_pandas(basement_df).rename({"Basement": "basement", "Load": "fl_basement_rating_factor"})
    df = df.join(basement_pl, on="basement", how="left")
    df = df.with_columns(
        (1 + pl.col("fl_basement_rating_factor"))
            .fill_null(1)
            .alias("fl_basement_rating_factor")
        )

    return df


def flood_elevation_rating_factor(hxd, df):

    df = df.with_columns(
        pl.lit(1)
            .alias("fl_elevation_rating_factor")
    )

    return df


def flood_catnet_score_intl_rating_factor(hxd, df):

    # Load parameter table
    fl_catnet_score_df = hx.params.fl_catnet_score

    # Windstorm Risk Level
    fl_catnet_score_pl = pl.from_pandas(fl_catnet_score_df)[["Score Band", "Load"]]
    fl_catnet_score_pl = fl_catnet_score_pl.rename({"Score Band": "catnet_score_fl", "Load": "fl_catnet_load"})

    fl_catnet_score_pl = df[["country", "catnet_score_fl"]].join(fl_catnet_score_pl, on="catnet_score_fl", how="left")

    df = df.with_columns(
        fl_catnet_score_pl.select(
            pl.when(pl.col("country") == "United States")
                .then(1)
                .otherwise(1 + pl.col("fl_catnet_load"))
                .fill_null(1)
                .alias("fl_catnet_rating_factor")
        )
    )

    return df

def flood_size_discount_rating_factor(hxd, df, other_data): 

    # Load parameter tables
    loc_discount_df = hx.params.location_level_tiv
    acc_discount_df = hx.params.account_level_tiv
    # assign Discount Factors 
    total_acc_tiv = other_data["total_tiv_total_usd"]
    total_loc_tiv_df = df["tiv_total_usd"]

    flood_size_discount_rating_factor = size_discount(loc_discount_df, acc_discount_df, total_acc_tiv, total_loc_tiv_df, "flood")

    df = df.with_columns(pl.Series(name="fl_size_discount_rating_factor", values = flood_size_discount_rating_factor))

    return df


def flood_us_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        (
            pl.col("fl_katrisk_risk_rating_factor") * pl.col("fl_construction_rating_factor") * pl.col("fl_num_floors_rating_factor") *
            pl.col("fl_basement_rating_factor") * pl.col("fl_elevation_rating_factor") * pl.col("fl_size_discount_rating_factor")
        ).alias("flood_us_buildings_total_adjustment")
    )
    
    df = df.with_columns(
        [
            pl.col("flood_us_buildings_total_adjustment").alias("flood_us_contents_total_adjustment"),
            (pl.col("flood_us_buildings_total_adjustment") * pl.col('bi_waiting_period_factor') * 
                other_data['bi_indemnity_period_factor'] * other_data['cbi_load'])
                .alias("flood_us_bi_total_adjustment")
        ]
    )

    return df


def flood_intl_total_adjustment(hxd, df, other_data):

    df = df.with_columns(
        (
            pl.col("fl_catnet_rating_factor") * pl.col("fl_construction_rating_factor") * pl.col("fl_num_floors_rating_factor") *
            pl.col("fl_basement_rating_factor") * pl.col("fl_elevation_rating_factor") * pl.col("fl_size_discount_rating_factor")
        ).alias("flood_intl_buildings_total_adjustment")
    )
    
    df = df.with_columns(
        [
            pl.col("flood_intl_buildings_total_adjustment").alias("flood_intl_contents_total_adjustment"),
            (pl.col("flood_intl_buildings_total_adjustment") * pl.col('bi_waiting_period_factor') * 
                other_data['bi_indemnity_period_factor'] * other_data['cbi_load'])
                .alias("flood_intl_bi_total_adjustment")
        ]
    )
    
    return df
