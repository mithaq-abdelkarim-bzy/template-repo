import hx
import polars as pl

def tria_calc(hxd, df, other_data):
    '''
    Calculate TRIA premium
    '''
    
    rms_proxy_rate_df = hx.params.rms_proxy_rate
    rms_proxy_rate_pl = pl.from_pandas(rms_proxy_rate_df[["Zip Code", "TRIA Rate"]])

    max_zip_pl = df.select(pl.col("zip").take(pl.col("tiv_total_usd").arg_max()))
    max_zip = max_zip_pl['zip'][0]

    filtered_rate_pl = (rms_proxy_rate_pl.filter(pl.col("Zip Code") == max_zip))
    tria_rate = filtered_rate_pl["TRIA Rate"][0] if len(filtered_rate_pl) else 0

    for index, layer in enumerate(hxd.layers, start=1):
        layer.perils.tria.tria_premium = (layer.perils.tria.include *
                                            tria_rate * (layer.achieved_premium_100_gg or 0))
            