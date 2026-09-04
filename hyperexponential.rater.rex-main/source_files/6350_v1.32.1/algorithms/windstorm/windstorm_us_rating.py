import hx
import polars as pl

def windstorm_us_base_rate_lookup(hxd, df, other_data):

    # Load parameter tables
    rms_proxy_rate_avg_df = hx.params.rms_proxy_rate_avg
    rms_proxy_rate_df = hx.params.rms_proxy_rate
    ws_base_rate_load_df = hx.params.ws_base_rate_load

    # US Windstorm building Base Rates (From lookup, before inflation and layer included check)
    rms_proxy_rate_avg_pl = pl.from_pandas(rms_proxy_rate_avg_df[["StateCounty", "WS Base Rate"]]).rename(
                                {"StateCounty": "state_county", "WS Base Rate": "ws_base_rate_avg"}
                            )
    rms_proxy_rate_avg_pl = rms_proxy_rate_avg_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county") 
    rms_proxy_rate_pl = pl.from_pandas(rms_proxy_rate_df[["Zip Code", "WS Base Rate"]]).rename(
                            {"Zip Code": "zip", "WS Base Rate": "ws_base_rate"}
                        )

    base_rate_pl = df[["row_nr", "zip", "state_county_lowercase", "country"]]
    base_rate_pl = base_rate_pl.join(rms_proxy_rate_avg_pl, on="state_county_lowercase", how="left")
    base_rate_pl = base_rate_pl.join(rms_proxy_rate_pl, on="zip", how="left")
    
    base_rate_pl = base_rate_pl.with_columns(
        pl.when(pl.col("zip") == None)
            .then(pl.col("ws_base_rate_avg"))
            .otherwise(pl.col("ws_base_rate"))
            .fill_null(0)
            .alias("windstorm_us_buildings_base_rate")
    )

    ws_base_rate_load_pl = pl.from_pandas(ws_base_rate_load_df).rename({"StateCounty": "state_county"})
    ws_base_rate_load_pl = ws_base_rate_load_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")
    base_rate_pl = base_rate_pl.join(ws_base_rate_load_pl, on="state_county_lowercase", how="left")

    return df, base_rate_pl
    

def windstorm_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl):

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"ws_covered_rating_layer{index}")))
    
    df = df.with_columns(
        base_rate_pl.select(
                pl.when(pl.col("country") != "United States")
                    .then(0)
                    .otherwise(pl.col("windstorm_us_buildings_base_rate") * pl.col(f"ws_covered_rating_layer{index}") * other_data['inflation'])
                    .alias(f"windstorm_us_buildings_base_rate_layer{index}"),
                
        )
    )

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"windstorm_us_buildings_base_rate_layer{index}")))

    df = df.with_columns(
        base_rate_pl.select(
            (pl.col(f"windstorm_us_buildings_base_rate_layer{index}") * (1 + pl.col("Contents")))
                .fill_null(0)
                .alias(f"windstorm_us_contents_base_rate_layer{index}"),
            (pl.col(f"windstorm_us_buildings_base_rate_layer{index}") * (1 + pl.col("BI")))
                .fill_null(0)
                .alias(f"windstorm_us_bi_base_rate_layer{index}")
        )
    )

    return df
