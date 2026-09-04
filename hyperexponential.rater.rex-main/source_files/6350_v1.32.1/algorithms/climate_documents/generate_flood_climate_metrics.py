import hx
import pandas as pd
import polars as pl
import numpy as np
from algorithms.climate_documents.gc_flood_api_requests import main 
import os

def generate_flood_climate_metrics(hxd, progress):
    # Global Constants
    climate_change_year = 2055
    current_yoa = hxd.hx_core.inception_date.year

    # Flood Climate Metric Algorithms
    flood_df = prepare_data(hxd, progress)
    flood_df = call_gc_api(flood_df, progress)
    flood_df = calculate_risk_scores(flood_df, hxd, progress)
    summaries = generate_summaries(flood_df, climate_change_year,current_yoa, hxd, progress)
    assign_to_hxd(hxd, summaries, progress)


def prepare_data(hxd, progress):
    '''Prepare flood data from schedule.'''

    # CONSTANTS Required 
    max_rows = 999  # API call fails at 1,000 locs, but then seems to work for 999
    countries = ['United States']
    columns = ['loc_id', 'street_name', 'latitude', 'longitude', 'constr_code', 'num_stories', 'tiv_total', 'tiv_total_usd', 'risk_level_fl']  # select descriptive construction field.

    if hxd.policy_information.small_schedule_model:
        ## Data preparation from hxd:
        flood_df = pl.DataFrame([{col: getattr(row, col) for col in columns} for row in hxd.schedule.schedule_table])

        
        flood_df = flood_df.with_columns([
            pl.Series([row.industry_occupancy_dropdown.industry for row in hxd.schedule.schedule_table]).alias('industry'),
            pl.Series([row.industry_occupancy_dropdown.occupancy for row in hxd.schedule.schedule_table]).alias('occupancy'),
            pl.Series([row.address_dropdown.country for row in hxd.schedule.schedule_table]).alias('country'),
            pl.Series([row.address_dropdown.state for row in hxd.schedule.schedule_table]).alias('state')
            ])

        
        # bring in flood expected loss cost for each location and layer 
        num_layers = len(hxd.schedule.schedule_table[0].output_by_layer)

        for i in range(num_layers):
            flood_df = flood_df.with_columns(
                pl.Series([row.output_by_layer[i].el_post_uw_usd_100_fl for row in hxd.schedule.schedule_table]).alias(f'el_post_uw_usd_100_fl_layer_{i}'))

        
        # sum flood EL over layers
        layer_cols = [f'el_post_uw_usd_100_fl_layer_{i}' for i in range(num_layers)]
        if layer_cols:
            flood_df = flood_df.with_columns(
                flood_df.select(pl.col(layer_cols).fill_null(0))
                        .sum(axis=1)
                        .cast(pl.Float64)
                        .alias("el_post_uw_usd_100_fl_total")
            )
        else:
            flood_df = flood_df.with_columns(
                pl.lit(0).alias('el_post_uw_usd_100_fl_total'))

        # filter data on US only and take top 1000 locations by flood EL
        flood_df = flood_df.filter(pl.col('country').is_in(countries))
        flood_df = flood_df.sort('el_post_uw_usd_100_fl_total', descending=True).head(max_rows)

    return flood_df 


def call_gc_api(flood_df, progress):

    # GC API Call
    ## Establish API connection and complete authentication 
    ## take flood_df, convert each row to JSON, pass to API, return results and tabulate 
    # set missing values to 0
    flood_df = flood_df.to_pandas()
    flood_df = main(flood_df, workers = 16)

    # Rename new columns of flood_df
    flood_df.rename(columns={
        'label_1': 'current_ind',
        'label_2': 'current_com',
        'label_3': 'current_res',
        'label_4': 'future_com',
        'label_5': 'future_res',
        'label_6': 'future_ind'
    }, inplace=True)

    return flood_df


def calculate_risk_scores(flood_df, hxd, progress):
    flood_df = pl.from_pandas(flood_df)
    # PARAMS
    fl_ind_map = pl.from_pandas(hx.params.climate_fl_ind_map)
    fl_gc_rs_aadr = pl.from_pandas(hx.params.climate_fl_gc_rs_aadr)
    fl_loc_scores = pl.from_pandas(hx.params.climate_fl_loc_scores)

    # Scores based on industry mapping to residential, commercial, industrial 
    flood_df = flood_df.join(fl_ind_map, on = 'industry', how = 'left')
    flood_df = flood_df.with_columns(
        pl.col('ind_map').str.to_lowercase())

    # Determine current and future score based on occupancy mapping
    # Note need to expand this if add new industries, to keep it vectorised.
    flood_df = flood_df.with_columns(
        pl.when(pl.col('ind_map') == 'com').then(pl.col('current_com'))
        .when(pl.col('ind_map') == 'ind').then(pl.col('current_ind'))
        .when(pl.col('ind_map') == 'res').then(pl.col('current_res'))
        .otherwise(pl.lit(0))
        .alias('current_risk_score')
    )

    flood_df = flood_df.with_columns(
        pl.when(pl.col('ind_map') == 'com').then(pl.col('future_com'))
        .when(pl.col('ind_map') == 'ind').then(pl.col('future_ind'))
        .when(pl.col('ind_map') == 'res').then(pl.col('future_res'))
        .otherwise(pl.lit(0))
        .alias('future_risk_score')
    )

    # Lookup Beazley location flood risk score, which is based on how the expected increase in EL derived from the GC risk scores. 
    # e.g. if a location observes a 0% increase by 2055, then it is scored a 1; for 100% a score of 2; for 1000% a score of 5
    flood_df = flood_df.join(
        fl_loc_scores,
        on = ['current_risk_score', 'future_risk_score'],
        how = 'left'
    )

    # Calculate policy-level Beazley risk score
    flood_df = flood_df.with_columns(
        pl.when(pl.col('bzly_loc_score') == 0).then(pl.lit(0))
        .otherwise(pl.col('el_post_uw_usd_100_fl_total'))
        .alias('current_fl_el_with_score')
    )

    flood_df = flood_df.with_columns(
        (pl.col('current_fl_el_with_score') * pl.col('bzly_loc_score'))
        .alias('current_fl_el_weighted_by_score'))


    ## Continue calculations to give the expected change in EL. 
    # Determine resulting AADRs from the parameter table 
    # Current risk scores
    flood_df = flood_df.join(
        fl_gc_rs_aadr.select(['risk_score', 'aadr']),
        left_on='current_risk_score',
        right_on='risk_score',
        how='left'
    )

    flood_df = flood_df.rename({'aadr': 'current_aadr'})

    # Future risk scores
    flood_df = flood_df.join(
        fl_gc_rs_aadr.select(['risk_score', 'aadr']),
        left_on = 'future_risk_score',
        right_on = 'risk_score',
        how = 'left'
    )
    flood_df = flood_df.rename({'aadr': 'future_aadr'})

    # Calculate current and future AALs and the change   
    flood_df = flood_df.with_columns(
        (pl.col('tiv_total_usd') * pl.col('current_aadr')).alias('current_aal'),
        (pl.col('tiv_total_usd') * pl.col('future_aadr')).alias('future_aal')
    )
    
    flood_df = flood_df.with_columns(
        pl.when(pl.col('current_aal')==0)
        .then(pl.lit(0))
        .otherwise((pl.col('future_aal') / pl.col('current_aal')) - 1 )
        .alias('change')
    )

    # Calculate current and future ELs based on Rex calc 
    flood_df = flood_df.with_columns(
        (pl.col('el_post_uw_usd_100_fl_total')).alias('current_fl_el'),
    )
    flood_df = flood_df.with_columns(
        (pl.col('current_fl_el') * (1 + pl.col('change'))).alias('future_fl_el'),
    )

    return flood_df


    
def generate_summaries(flood_df,climate_change_year, current_yoa, hxd, progress):

    # Calculate total policy change and annualised change
    el = flood_df.select(
        pl.col('current_fl_el').sum().alias('pol_current_fl_el'),
        pl.col('future_fl_el').sum().alias('pol_future_fl_el')
    )
    pol_current_fl_el, pol_future_fl_el = el.row(0)

    pol_change_all_years = 0 if pol_current_fl_el == 0 else (pol_future_fl_el / pol_current_fl_el) - 1

    pol_change_one_year = ((1 + pol_change_all_years) ** (1 / (climate_change_year - current_yoa))) - 1
    pol_change_five_years = ((1 + pol_change_one_year) ** 5) - 1

    # Calculate the flood_climate_risk score summary
    el_with_score = flood_df.select(
        pl.col('current_fl_el_with_score').sum().alias('pol_fl_el_with_score'),
        pl.col('current_fl_el_weighted_by_score').sum().alias('pol_fl_el_weighted_by_score')
    )
    pol_fl_el_with_score, pol_fl_el_weighted_by_score = el_with_score.row(0)

    flood_climate_risk_score = 1 if pol_fl_el_with_score == 0 else (pol_fl_el_weighted_by_score / pol_fl_el_with_score)
    
    flood_climate_risk_score = np.round(flood_climate_risk_score)

    # Flood climate metrics - note
    degree_sign = u'\N{DEGREE SIGN}'
    direction = 'rise by' if pol_change_all_years >= 0 else 'fall by'
    flood_el_projection = f'Flood expected loss cost is projected to {direction} {abs(int(pol_change_all_years * 100))}% by 2055, assuming a 2{degree_sign}C increase in global temperatures compared to pre-industrial levels.'

    # Score summary
    score_summary_temp = pl.DataFrame({
        'bzly_loc_score': range(6),
        'loc_count': 0.0,
        'tiv_total_usd': 0.0,
        'current_fl_el': 0.0
    })

    score_summary = (
        flood_df.groupby('bzly_loc_score')
        .agg([
            pl.count().cast(pl.Float64).alias("loc_count"),
            pl.col("tiv_total_usd").sum().cast(pl.Float64).alias("tiv_total_usd"),
            pl.col("current_fl_el").sum().cast(pl.Float64).alias("current_fl_el")
            ])
    )

    score_summary = (
        pl.concat([score_summary_temp, score_summary])
        .groupby("bzly_loc_score")
        .agg([
            pl.col("loc_count").sum(),
            pl.col("tiv_total_usd").sum(),
            pl.col("current_fl_el").sum()
        ])
        .sort("bzly_loc_score") 
    )

    score_summary = (
        score_summary
        .with_columns([
            (pl.col("loc_count") / pl.col("loc_count").sum()).alias("loc_prop"),
            (pl.col("tiv_total_usd") / 1_000_000).alias("tiv_total_usd_chart")
        ])
    )

    # Construction summary
    constr_summary = (
        flood_df
        .groupby("constr_code")
        .agg([
            pl.count().cast(pl.Float64).alias("locations"),
            pl.col("tiv_total_usd").sum().cast(pl.Float64).alias("tiv_total_usd"),
            pl.col("current_fl_el").sum().cast(pl.Float64).alias("current_fl_el"),
            pl.col("future_fl_el").sum().cast(pl.Float64).alias("future_fl_el"),
            pl.col("current_fl_el_with_score").sum().cast(pl.Float64).alias("current_fl_el_with_score"),
            pl.col("current_fl_el_weighted_by_score").sum().cast(pl.Float64).alias("current_fl_el_weighted_by_score"),
            pl.col("bzly_loc_score").mean().cast(pl.Float64).alias("bzly_loc_score")
        ])
        .with_columns([
            pl.when(pl.col("current_fl_el") == 0)
            .then(0)
            .otherwise(((pl.col("future_fl_el") / pl.col("current_fl_el")) ** (5 / (climate_change_year - current_yoa))) - 1)
            .alias("change_five_years")
        ])
    )
    constr_summary = constr_summary.sort("constr_code", descending = False)

    # Num Stories summary
    num_stories_summary = (
        flood_df
        .groupby("num_stories")
        .agg([
            pl.count().cast(pl.Float64).alias("locations"),
            pl.col("tiv_total_usd").sum().cast(pl.Float64).alias("tiv_total_usd"),
            pl.col("current_fl_el").sum().cast(pl.Float64).alias("current_fl_el"),
            pl.col("future_fl_el").sum().cast(pl.Float64).alias("future_fl_el"),
            pl.col("current_fl_el_with_score").sum().cast(pl.Float64).alias("current_fl_el_with_score"),
            pl.col("current_fl_el_weighted_by_score").sum().cast(pl.Float64).alias("current_fl_el_weighted_by_score"),
            pl.col("bzly_loc_score").mean().cast(pl.Float64).alias("bzly_loc_score")
        ])
        .with_columns([
            pl.when(pl.col("current_fl_el") == 0)
            .then(0)
            .otherwise(((pl.col("future_fl_el") / pl.col("current_fl_el")) ** (5 / (climate_change_year - current_yoa))) - 1)
            .alias("change_five_years")
        ])
    )
    num_stories_summary = num_stories_summary.sort("num_stories", descending = False)

    # Flood Risk summary 
    flood_risk_summary = (
        flood_df
        .groupby("risk_level_fl")
        .agg([
            pl.count().cast(pl.Float64).alias("locations"),
            pl.col("tiv_total_usd").sum().cast(pl.Float64).alias("tiv_total_usd"),
            pl.col("current_fl_el").sum().cast(pl.Float64).alias("current_fl_el"),
            pl.col("future_fl_el").sum().cast(pl.Float64).alias("future_fl_el"),
            pl.col("current_fl_el_with_score").sum().cast(pl.Float64).alias("current_fl_el_with_score"),
            pl.col("current_fl_el_weighted_by_score").sum().cast(pl.Float64).alias("current_fl_el_weighted_by_score"),
            pl.col("bzly_loc_score").mean().cast(pl.Float64).alias("bzly_loc_score")
        ])
        .with_columns([
            pl.when(pl.col("current_fl_el") == 0)
            .then(0)
            .otherwise(((pl.col("future_fl_el") / pl.col("current_fl_el")) ** (5 / (climate_change_year - current_yoa))) - 1)
            .alias("change_five_years")
        ])
    )

    if flood_risk_summary.height > 0:
        risk_order_df = pl.DataFrame({
            "risk_level_fl": ["None", "Low", "Medium", "High"],
            "sort_index": [0, 1, 2, 3]
        })

        flood_risk_summary = (
            flood_risk_summary
            .join(risk_order_df, on="risk_level_fl", how="left")
        )
        flood_risk_summary = flood_risk_summary.sort("sort_index").drop("sort_index")


    # Top 10 locations
    top_10_locations_summary = (
        flood_df.select([
            "tiv_total_usd", "current_fl_el", "future_fl_el", "bzly_loc_score",
            "constr_code", "industry", "occupancy", "num_stories"])
        .sort("tiv_total_usd", descending=True)
        .head(10)
    )
    top_10_locations_summary = top_10_locations_summary.with_columns(
        pl.when(pl.col('current_fl_el')==0)
        .then(pl.lit(0))
        .otherwise(((pl.col('future_fl_el')/pl.col('current_fl_el'))** (5 / (climate_change_year - current_yoa)))-1)
        .alias('change_five_years')
    )

    
    summaries = {
        'flood_climate_risk_score': flood_climate_risk_score,
        'pol_current_fl_el': pol_current_fl_el, 
        'pol_future_fl_el': pol_future_fl_el,
        'pol_change_all_years': pol_change_all_years,
        'pol_change_one_year': pol_change_one_year,
        'pol_change_five_years': pol_change_five_years,
        'flood_el_projection': flood_el_projection, 
        'score_summary': score_summary.to_dicts(),
        'constr_summary': constr_summary.to_dicts(),
        'num_stories_summary': num_stories_summary.to_dicts(),
        'flood_risk_summary': flood_risk_summary.to_dicts(),
        'top_10_locations_summary': top_10_locations_summary.to_dicts(),
        'flood_df': flood_df
        }

    return summaries

def assign_to_hxd(hxd, summaries, progress):

    # Assign back to hxd
    hxd.non_layer_summary.climate_metrics.flood.flood_climate_risk_score = summaries['flood_climate_risk_score']
    hxd.non_layer_summary.climate_metrics.flood.pol_current_fl_el = summaries['pol_current_fl_el']
    hxd.non_layer_summary.climate_metrics.flood.pol_future_fl_el = summaries['pol_future_fl_el']
    hxd.non_layer_summary.climate_metrics.flood.pol_change_all_years = summaries['pol_change_all_years']
    hxd.non_layer_summary.climate_metrics.flood.pol_change_one_year = summaries['pol_change_one_year']
    hxd.non_layer_summary.climate_metrics.flood.pol_change_five_years = summaries['pol_change_five_years']
    hxd.non_layer_summary.climate_metrics.flood.flood_el_projection = summaries['flood_el_projection']

    hxd.non_layer_summary.climate_metrics.flood.score_summary = summaries['score_summary']
    hxd.non_layer_summary.climate_metrics.flood.constr_summary = summaries['constr_summary']
    hxd.non_layer_summary.climate_metrics.flood.num_stories_summary = summaries['num_stories_summary']
    hxd.non_layer_summary.climate_metrics.flood.flood_risk_summary = summaries['flood_risk_summary']
    hxd.non_layer_summary.climate_metrics.flood.top_10_locations_summary = summaries['top_10_locations_summary']

    # table of all locations. This is used in the climate doc generation task.
    flood_df = summaries['flood_df']
    table_data = flood_df.select([
        'loc_id', 'street_name', 'state', 'latitude', 'longitude', 
        'industry', 'occupancy', 'constr_code', 'num_stories',
        'tiv_total', 'tiv_total_usd', 'el_post_uw_usd_100_fl_total', 
        'status', 'ind_map',
        'current_risk_score', 'future_risk_score', 
        'bzly_loc_score', 'current_fl_el_with_score', 'current_fl_el_weighted_by_score', 
        'current_aadr', 'future_aadr', 
        'current_aal', 'future_aal', 'change', 'current_fl_el', 'future_fl_el'
    ])

    hxd.non_layer_summary.climate_metrics.flood.flood_climate_table = table_data.to_dicts()
        

