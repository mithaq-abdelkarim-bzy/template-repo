import hx
import polars as pl

def earthquake_us_base_rate_lookup(hxd, df, other_data):

    # Load parameter tables
    rms_proxy_rate_avg_df = hx.params.rms_proxy_rate_avg
    rms_proxy_rate_df = hx.params.rms_proxy_rate
    eq_base_rate_load_df = hx.params.eq_base_rate_load

    # US Earthquake building Base Rates (From lookup, before inflation and layer included check)
    rms_proxy_rate_avg_pl = pl.from_pandas(rms_proxy_rate_avg_df[["StateCounty", "EQ Base Rate"]]).rename(
                                {"StateCounty": "state_county", "EQ Base Rate": "eq_base_rate_avg"}
                            )
    rms_proxy_rate_avg_pl = rms_proxy_rate_avg_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")
    
    rms_proxy_rate_pl = pl.from_pandas(rms_proxy_rate_df[["Zip Code", "EQ Base Rate"]]).rename(
                            {"Zip Code": "zip", "EQ Base Rate": "eq_base_rate"}
                        )

    base_rate_pl = df[["row_nr", "zip", "state_county_lowercase", "country", "state"]]
    base_rate_pl = base_rate_pl.join(rms_proxy_rate_avg_pl, on="state_county_lowercase", how="left")
    base_rate_pl = base_rate_pl.join(rms_proxy_rate_pl, on="zip", how="left")
    
    base_rate_pl = base_rate_pl.with_columns(
        pl.when(pl.col("zip") == None)
            .then(pl.col("eq_base_rate_avg"))
            .otherwise(pl.col("eq_base_rate"))
            .fill_null(0)
            .alias("earthquake_us_buildings_base_rate")
    )

    eq_base_rate_load_pl = pl.from_pandas(eq_base_rate_load_df).rename({"StateCounty": "state_county"})
    eq_base_rate_load_pl = eq_base_rate_load_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")

    base_rate_pl = base_rate_pl.join(eq_base_rate_load_pl, on="state_county_lowercase", how="left")

    return df, base_rate_pl


def earthquake_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl):

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"eq_covered_rating_layer{index}")))
    
    df = df.with_columns(
        base_rate_pl.select(
                pl.when(pl.col("country") != "United States")
                    .then(0)
                    .otherwise(
                        pl.col("earthquake_us_buildings_base_rate") * 
                        pl.col(f"eq_covered_rating_layer{index}") * 
                        other_data['inflation'] *
                            (
                                pl.when((pl.col("state") == "CA") & (not layer.perils.quake.ca_quake_include))
                                    .then(0)
                                    .otherwise(1)
                            )
                        )
                    .alias(f"earthquake_us_buildings_base_rate_layer{index}"),
                
        )
    )

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"earthquake_us_buildings_base_rate_layer{index}")))

    df = df.with_columns(
        base_rate_pl.select(
            (pl.col(f"earthquake_us_buildings_base_rate_layer{index}") * (1 + pl.col("Contents")))
                .fill_null(0)
                .alias(f"earthquake_us_contents_base_rate_layer{index}"),
            (pl.col(f"earthquake_us_buildings_base_rate_layer{index}") * (1 + pl.col("BI")))
                .fill_null(0)
                .alias(f"earthquake_us_bi_base_rate_layer{index}")
        )
    )

    return df