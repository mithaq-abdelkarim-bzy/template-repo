import hx
import polars as pl
from datetime import datetime


def el_calcs(hxd, df):

    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        line_use = hxd.cds.layers[0].signed_line
    else:
        line_use = hxd.cds.layers[0].written_line

    inception_date = datetime(hxd.cds.standard_fields.inception_date.year, hxd.cds.standard_fields.inception_date.month, hxd.cds.standard_fields.inception_date.day)

    # calculate net ELs by peril
    df = df.with_columns(
        pl.sum_horizontal(["bg1_buildings_market_share_el", "bg2_buildings_market_share_el", "scl_buildings_market_share_el", "bg1_contents_market_share_el", "bg2_contents_market_share_el", "scl_contents_market_share_el", "fire_bi_market_share_el"]).alias("loc_fire_market_share_el")
    )

    for peril in ("fl", "tn", "ha", "wf", "wts"):
        df = df.with_columns(
            pl.sum_horizontal([f"{peril}_buildings_market_share_el", f"{peril}_contents_market_share_el", f"{peril}_bi_market_share_el"]).alias(f"loc_{peril}_market_share_el")
        )
    
    df = df.with_columns(
        pl.sum_horizontal("loc_fire_market_share_el", "loc_fl_market_share_el", "loc_tn_market_share_el", "loc_ha_market_share_el", "loc_wf_market_share_el", "loc_wts_market_share_el").alias("loc_all_perils_market_share_el")
    )

    # calculate afb net EL by peril and total
    for peril in ("fire", "fl", "tn", "ha", "wf", "wts"):
        df = df.with_columns(
            pl.when((pl.col("inception_date") <inception_date) &  (hxd.cds.layers[0].expiry_signed_line not in[None, 0]))
            .then(pl.col(f"loc_{peril}_market_share_el") * pl.col("ceded_share") * hxd.cds.layers[0].expiry_signed_line)
            .otherwise(pl.col(f"loc_{peril}_market_share_el") * pl.col("ceded_share") * line_use)
            .alias(f"loc_{peril}_beazley_share_el")
        )
    
    df = df.with_columns(pl.sum_horizontal((f"loc_{peril}_beazley_share_el" for peril in ("fire", "fl", "tn", "ha", "wf", "wts"))).alias("loc_all_perils_beazley_share_el"))

    df = df.with_columns(
        pl.col("loc_all_perils_beazley_share_el").sum().over("acc_number").alias("acc_beazley_share_total_el"),
        ((pl.sum_horizontal("loc_ws_beazley_share_aal", "loc_eq_beazley_share_aal")).sum().over("acc_number").alias("acc_all_perils_beazley_share_aal"))
    )

    df = df.with_columns(
        (pl.col("loc_all_perils_beazley_share_el")  + pl.col("loc_ws_beazley_share_aal")  + pl.col("loc_eq_beazley_share_aal")).alias("loc_all_perils_beazley_share_aal_and_el"),
        (pl.col("acc_beazley_share_total_el")  + pl.col("acc_all_perils_beazley_share_aal")).alias("acc_all_perils_beazley_share_aal_and_el")
    )
    
    nmp_uplift = pl.from_pandas(hx.params.table_uplift)["nmp_el_uplift"].item()

    df = df.with_columns(((pl.col("loc_all_perils_market_share_el") + pl.col("loc_ws_market_share_aal")  + pl.col("loc_eq_market_share_aal")) * pl.lit(nmp_uplift)).alias("loc_nmp_market_share_el"))

    df = df.with_columns(
        pl.when((pl.col("inception_date") < inception_date) & (hxd.cds.layers[0].expiry_signed_line not in [None, 0]))
        .then(pl.col("loc_nmp_market_share_el") * (pl.col("ceded_share") * hxd.cds.layers[0].expiry_signed_line))
        .otherwise(pl.col("loc_nmp_market_share_el") * (pl.col("ceded_share") * line_use))
        .alias("loc_nmp_beazley_share_el")
    )

    for peril, loss_type in zip(["fire", "fl", "tn", "ha", "wf", "wts", "eq", "ws"], ["el", "el", "el", "el", "el", "el", "aal", "aal"]):
        df = df.with_columns(((pl.col(f"loc_{peril}_beazley_share_{loss_type}") / pl.col("loc_all_perils_beazley_share_aal_and_el")) * pl.col("loc_nmp_beazley_share_el")).fill_nan(0).alias(f"loc_{peril}_nmp_beazley_share_el"))

    return df