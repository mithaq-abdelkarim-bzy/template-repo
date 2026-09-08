import hx
import polars as pl
import algorithms.rate_constants as const
from algorithms.json_parameter_files.parameters import get_parameters 

def report_summary(hxd, df):

    tiv_summary(hxd, df)
    summary_by_stat(hxd, df, col_name="iso_constr", summary_name="construction")
    summary_by_stat(hxd, df, col_name="occupancy", summary_name="occupancy")
    summary_by_stat(hxd, df, col_name="year_built", summary_name="year_built", bins=const.year_built_bins)
    summary_by_stat(hxd, df, col_name="num_floors", summary_name="num_floors", bins=const.num_floors_bins)
    summary_by_stat(hxd, df, col_name="state", summary_name="state")

def tiv_summary(hxd, df):
    
    buildings_sum = df.select(pl.sum("loc_tiv_buildings")).item()
    contents_sum = df.select(pl.sum("loc_tiv_contents")).item()
    bi_sum = df.select(pl.sum("loc_tiv_bi")).item()
    total_sum = df.select(pl.sum("loc_tiv_total")).item()

    tiv_summary = pl.DataFrame({
        "coverage": ["Buildings", "Contents", "BI", "Total"],
        "value": [buildings_sum, contents_sum, bi_sum, total_sum],
        "percentage":[
            (buildings_sum / total_sum),
            (contents_sum / total_sum),
            (bi_sum / total_sum),
            1 #set total % to None 
        ],
        "show_row": [True, True, True, False] # Add show_row for displaying purposes 
    })

    tiv_summary =  tiv_summary.to_dicts()
    hxd.cds.exposure.aggregate.tiv_summary = tiv_summary

    # Total Row for TIV summary assign to the separate structure, for displaying purposes
    total_structure = hxd.cds.exposure.aggregate.tiv_summary_total
    total_structure.coverage = tiv_summary[-1]["coverage"]
    total_structure.value =tiv_summary[-1]["value"]
    total_structure.percentage = tiv_summary[-1]["percentage"]


def summary_by_stat(hxd, df, col_name, summary_name, bins=None):

    if df[col_name].dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.Float32, pl.Float64]:
        df = df.with_columns(
            pl.when(pl.col(col_name).is_null())
            .then(pl.lit("Unknown"))
            .otherwise(pl.col(col_name))
            .alias(col_name)
        )
    else:
        df = df.with_columns(
            pl.when(pl.col(col_name).is_null() | (pl.col(col_name) == ""))
            .then(pl.lit("Unknown"))
            .otherwise(pl.col(col_name))
            .alias(col_name)
        )

    if bins:
        breaks = list(bins[0])
        labels = list(bins[1])

        df_with_bins = df.with_columns(
            pl.col(col_name).cut(breaks=breaks, labels=labels).alias(col_name)
        )

    else:
        df_with_bins = df

    df_with_bins = df_with_bins.with_columns((pl.col("loc_tiv_total") * pl.col("ceded_share")).alias("share_lim"))
    share_lim_total = df_with_bins.select(pl.col("share_lim").sum()).item()

    df_with_bins = df_with_bins.with_columns((pl.col("acc_beazley_received_gg_prem") * (pl.col("loc_all_perils_beazley_share_aal_and_el") / pl.col("acc_all_perils_beazley_share_aal_and_el"))).fill_nan(0).alias("loc_beazley_share_received_gg_prem"))
    df_with_bins = df_with_bins.with_columns((pl.col("loc_beazley_share_received_gg_prem") * (1 - hxd.cds.layers[0].total_deductions)).alias("loc_beazley_share_received_gn_prem"))
    
    df_with_bins = df_with_bins.with_columns(
        (pl.col("loc_beazley_share_received_gn_prem"))
        .alias("loc_beazley_share_gn_prem_allocated")
    )    
    summary_df = df_with_bins.groupby(col_name).agg([
        pl.sum("loc_tiv_total").alias("tiv"),                                                                                                                                                                                                                                                                                                                                                                                                                 
        pl.sum("share_lim").alias("share_lim"),

        pl.when(share_lim_total != 0)
        .then(pl.sum("share_lim") / share_lim_total)
        .otherwise(0)
        .alias("perc_share_limit"),

        pl.sum("loc_beazley_share_gn_prem_allocated").alias("gn_prem"),
        pl.sum("loc_ws_beazley_share_aal").alias("ws_aal"),
        pl.sum("loc_eq_beazley_share_aal").alias("eq_aal"),
        pl.sum("loc_all_perils_beazley_share_el").alias("aop_el"), # should we add NMP to the ws, eq, and other peril losses here?
       
        pl.when(pl.sum("share_lim") != 0)
        .then((pl.sum("loc_beazley_share_gn_prem_allocated") / pl.sum("share_lim")) * 100)
        .otherwise(0)
        .alias("rate_received"),

        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_ws_beazley_share_aal") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("ws_aal_rate"),

        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_eq_beazley_share_aal") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("eq_aal_rate"),

        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_all_perils_beazley_share_el") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("aop_el_rate"),

        pl.when((pl.sum("loc_ws_beazley_share_aal") != 0) | (pl.sum("loc_eq_beazley_share_aal") != 0))
        .then(pl.sum("loc_beazley_share_gn_prem_allocated") / (pl.sum("loc_ws_beazley_share_aal") + pl.sum("loc_eq_beazley_share_aal")))
        .otherwise(0)
        .alias("prem_as_perc_of_aal")
    ])

    # Add show_row for displaying purposes
    summary_df = summary_df.with_columns(
    pl.lit(True).alias("show_row")
    )

    totals = df_with_bins.select([
        pl.lit("Total").alias(col_name),
        pl.sum("loc_tiv_total").alias("tiv"),
        pl.sum("share_lim").alias("share_lim"),

        pl.when(share_lim_total != 0)
        .then(pl.sum("share_lim") / share_lim_total)
        .otherwise(0)
        .alias("perc_share_limit"),

        pl.sum("loc_beazley_share_gn_prem_allocated").alias("gn_prem"),
        pl.sum("loc_ws_beazley_share_aal").alias("ws_aal"),
        pl.sum("loc_eq_beazley_share_aal").alias("eq_aal"),
        pl.sum("loc_all_perils_beazley_share_el").alias("aop_el"),
        
        pl.when(pl.sum("share_lim") != 0)
        .then((pl.sum("loc_beazley_share_gn_prem_allocated") / pl.sum("share_lim")) * 100)
        .otherwise(0)
        .alias("rate_received"),
        
        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_ws_beazley_share_aal") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("ws_aal_rate"),

        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_eq_beazley_share_aal") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("eq_aal_rate"),
        
        pl.when(pl.sum("loc_beazley_share_gn_prem_allocated") != 0)
        .then(pl.sum("loc_all_perils_beazley_share_el") / pl.sum("loc_beazley_share_gn_prem_allocated"))
        .otherwise(0)
        .alias("aop_el_rate"),
        
        pl.when((pl.sum("loc_ws_beazley_share_aal") != 0) | (pl.sum("loc_eq_beazley_share_aal") != 0))
        .then(pl.sum("loc_beazley_share_gn_prem_allocated") / (pl.sum("loc_ws_beazley_share_aal") + pl.sum("loc_eq_beazley_share_aal")))
        .otherwise(0)
        .alias("prem_as_perc_of_aal"),

        pl.lit(False).alias("show_row") # Add show_row for displaying purposes
    ])

    summary_df = summary_df.with_columns(pl.col(col_name).cast(pl.Utf8))
    summary_df = summary_df.sort(col_name)

    # move row with < to the first row
    if 'labels' in locals():
        first_row = summary_df.filter(pl.col(col_name) == labels[0])
        other_rows = summary_df.filter(pl.col(col_name) != labels[0])
        summary_df = pl.concat([first_row, other_rows])         

    summary_dict = pl.concat([summary_df, totals]).to_dicts()

    setattr(hxd.cds.exposure.aggregate, f"{summary_name}_summary", summary_dict)

    # Total Row for each summary assign to the separate structure
    path = hxd.cds.exposure.aggregate
    total_structure = getattr(path, f"{summary_name}_summary_total")
    for col_name, value in zip(totals.columns, totals.row(0)):
        if col_name != "show_row":
            setattr(total_structure, col_name, value)


#### bins ####
year_built_breaks = [1919, 1939, 1959, 1979, 1995, 2001]
year_built_labels = ["<1920", "1920-1939", "1940-1959", "1960-1979", "1980-1995", "1996-2001", ">2002"]
year_built_bins = [year_built_breaks, year_built_labels]

num_floors_breaks = [1, 3, 7, 14]
num_floors_labels = ["1", "2-3", "4-7", "8-14", "15+"]
num_floors_bins = [num_floors_breaks, num_floors_labels]


#### Region Summary #####

def region_summary(hxd, df):


    df = df.with_columns((pl.col("acc_beazley_received_gg_prem") * (pl.col("loc_all_perils_beazley_share_aal_and_el") / pl.col("acc_all_perils_beazley_share_aal_and_el"))).fill_nan(0).alias("loc_beazley_share_received_gg_prem"))
    df = df.with_columns((pl.col("loc_beazley_share_received_gg_prem") * (1 - hxd.cds.layers[0].total_deductions)).alias("loc_beazley_share_received_gn_prem"))
    
    
    df = df.with_columns(
        (pl.col("loc_beazley_share_received_gn_prem")
        .alias("loc_beazley_share_gn_prem_allocated")),

        (pl.col("loc_tiv_total") * pl.col("ceded_share"))
        .alias("share_lim")
    )

    share_lim_total = df.select(pl.col("share_lim").sum()).item()

    summary_df = df.groupby(["state", "county"]).agg([
        pl.sum("loc_tiv_total").alias("tiv"),
        pl.sum("share_lim").alias("share_lim"),
        (pl.sum("share_lim") / share_lim_total).alias("perc_share_limit"),
        pl.sum("loc_beazley_share_gn_prem_allocated").alias("beazley_share_gn_prem"),
        pl.sum("loc_1_in_250_oep").alias("one_in_250_oep"),
        pl.sum("loc_1_in_10_aep").alias("one_in_10_aep")
    ])

    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        line_use = hxd.cds.layers[0].signed_line
    else:
        line_use = hxd.cds.layers[0].written_line
        
    summary_df = summary_df.with_columns(
        pl.when(line_use is not None)
        .then(pl.col("share_lim") * pl.lit(line_use))
        .otherwise(None)
        .alias("beazley_share_lim")
        )

    # Add show_row for displaying purposes
    summary_df = summary_df.with_columns(
    pl.lit(True).alias("show_row")
    )

    totals = summary_df.select([
        pl.lit("Total").alias("state"),
        pl.lit(None).alias("county"),
        pl.sum("tiv").alias("tiv"),
        pl.sum("share_lim").alias("share_lim"),
        (pl.sum("share_lim") / share_lim_total).alias("perc_share_limit"),
        pl.sum("beazley_share_gn_prem").alias("beazley_share_gn_prem"),
        pl.sum("one_in_250_oep").alias("one_in_250_oep"),
        pl.sum("one_in_10_aep").alias("one_in_10_aep"),
        pl.sum("beazley_share_lim").alias("beazley_share_lim"),
        pl.lit(False).alias("show_row")
    ])

    summary_df = summary_df.sort("tiv",  descending=True)

    # Total row
    total_structure = hxd.cds.exposure.aggregate.region_summary_total
    for col_name, value in zip(totals.columns, totals.row(0)):
        if col_name != "show_row":
            setattr(total_structure, col_name, value)

    summary_df = pl.concat([summary_df, totals])

    # Add county FIPS code - for County level choropleth
    fips_codes = get_parameters('fips_codes.json')
    fips_df = pl.DataFrame(fips_codes).select([
        pl.col("fips").cast(pl.Utf8),  
        pl.col("county"), 
        pl.col("state").alias("state").cast(pl.Utf8),  
    ])

    summary_df = summary_df.join(
            fips_df, 
            left_on=["state", "county"], 
            right_on=["state", "county"], 
            how="left"
        ).select([
            pl.col("state"),
            pl.col("county"),
            pl.col("fips").alias("fips"),
            pl.col("tiv").alias("tiv"),
            pl.col("share_lim").alias("share_lim"),
            pl.col("perc_share_limit").alias("perc_share_limit"),
            pl.col("beazley_share_lim").alias("beazley_share_lim"),
            pl.col("beazley_share_gn_prem").alias("beazley_share_gn_prem"),
            pl.col("one_in_250_oep").alias("one_in_250_oep"),
            pl.col("one_in_10_aep").alias("one_in_10_aep"),
            pl.col("show_row").alias("show_row"), # Add show_row for displaying purposes

        ])
 
    hxd.cds.exposure.aggregate.region_summary = summary_df.to_dicts()

    # State level table - for State level choropleth
    states_df = summary_df.groupby(["state"]).agg([
        pl.sum("tiv").alias("tiv"),
        pl.sum("share_lim").alias("share_lim"),
        pl.sum("perc_share_limit").alias("perc_share_limit"),
        pl.sum("beazley_share_lim").alias("beazley_share_lim"),
        pl.sum("beazley_share_gn_prem").alias("beazley_share_gn_prem"),
        pl.sum("one_in_250_oep").alias("one_in_250_oep"),
        pl.sum("one_in_10_aep").alias("one_in_10_aep")
        
    ])

    # Remove Total row
    states_df = states_df.filter(pl.col("state") != "Total")

    states_df = states_df.with_columns(
        pl.col("state").alias("label")
    )
    
    hxd.cds.exposure.aggregate.region_summary_state = states_df.to_dicts()