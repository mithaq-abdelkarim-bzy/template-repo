import hx
import polars as pl

def flood_us_base_rate_lookup(hxd, df, other_data):

    # Load parameter tables
    fl_us_cat_base_rate_df = hx.params.fl_us_cat_base_rate

    fl_us_cat_base_rate_pl = pl.from_pandas(fl_us_cat_base_rate_df).rename(
                                    {
                                        "StateCounty": "state_county", "FL Buildings": "fl_buildings_rate",
                                        "FL Contents": "fl_contents_rate", "FL BI": "fl_bi_rate"
                                    }
                                )

    fl_us_cat_base_rate_pl = fl_us_cat_base_rate_pl.with_columns(
        pl.col("state_county").str.to_lowercase().alias("state_county_lowercase")
    ).drop("state_county")
    
    base_rate_pl = df[["row_nr", "state_county_lowercase"]].join(fl_us_cat_base_rate_pl, on="state_county_lowercase", how="left")
    
    return df, base_rate_pl


def flood_us_base_rate(hxd, df, other_data, layer, index, base_rate_pl):

    base_rate_pl = base_rate_pl.with_columns(df.select(pl.col(f"fl_covered_rating_layer{index}")))

    df = df.with_columns(
        base_rate_pl.select(
            [
                (pl.col("fl_buildings_rate") * pl.col(f"fl_covered_rating_layer{index}") * other_data['inflation'])
                    .fill_null(0)
                    .alias(f"flood_us_buildings_base_rate_layer{index}"),
                (pl.col("fl_contents_rate") * pl.col(f"fl_covered_rating_layer{index}") * other_data['inflation'])
                    .fill_null(0)
                    .alias(f"flood_us_contents_base_rate_layer{index}"),    
                (pl.col("fl_bi_rate") * pl.col(f"fl_covered_rating_layer{index}") * other_data['inflation'])
                    .fill_null(0)
                    .alias(f"flood_us_bi_base_rate_layer{index}"),
            ]
        )
    )

    return df