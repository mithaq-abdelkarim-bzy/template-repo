import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer

from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, query_bi_database

def bi_data_fetch(hxd,progress):

    ## set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    
    sec_refs = [layer.section_reference for layer in layers]
    # sec_refs = ["T1857V25APCC", "T7417Q25APCC"]
    sec_refs = [x[:6] for x in sec_refs if x is not None]
    sec_refs = ', '.join(f"'{x}'" for x in sec_refs)
     
    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    query1 = f"""
                SELECT [SectionReference],
                        [InsuredParty],
                        [SectionIsRenewal],
                        [TriFocusName],
                        [YOA],
                        [WrittenOrEstimatedPremium],
                        [RateChangeDivisor],
                        [BenchmarkDivisor],
                        [Exposure],
                        [TotalIncurred]


                FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
                WHERE TriFocusName = 'Cat' 
                and InsuredParty IN (
                    SELECT DISTINCT InsuredParty 
                    FROM [BeazleyIntelligenceDataSets].[Report].[SectionCombinedView]
                    WHERE Left(SectionReference,6) IN ({sec_refs})
                )
                Order by [YOA] Desc
            """

    columns1 =  [
        'section_reference',
        "insured_party",
        "section_is_renewal",
        "tri_focus_name",
        "yoa",
        "wep",
        "rate_change_divisor",
        "benchmark_divisor",
        "exposure",
        "incurred"
    ]

    bi_data_df = query_bi_database(query1, columns1)

    # 2) Calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    bi_data_df = bi_data_df.loc[:, ["yoa", "exposure", "wep", "rate_change_divisor", "benchmark_divisor", "incurred"]]
    bi_data_df = bi_data_df.fillna(0)
    bi_data_df["el"] = utils.ratio(bi_data_df["wep"], bi_data_df["benchmark_divisor"]) * 0.7
    bi_data_df["expiring_premium"] = np.where(bi_data_df["rate_change_divisor"] > 0,
                                              utils.ratio(bi_data_df["wep"], bi_data_df["rate_change_divisor"]),
                                              0)
    bi_data_df["renewed_premium"] = np.where(bi_data_df["expiring_premium"] > 0, bi_data_df["wep"], 0)

    bi_data_df = bi_data_df.groupby(["yoa"], as_index = False).agg(
        exposure = ("exposure", "sum"),
        wep = ("wep", "sum"),
        el = ("el", "sum"),
        expiring_premium = ("expiring_premium", "sum"),
        renewed_premium = ("renewed_premium", "sum"),
        incurred = ("incurred", "sum")
    )

    profit = bi_data_df["wep"].sum() - bi_data_df["incurred"].sum()
    ilr = utils.ratio(bi_data_df["incurred"].sum(), bi_data_df["wep"].sum())

    bi_data_df["elr"] = utils.ratio(bi_data_df["el"], bi_data_df["wep"])
    bi_data_df["rate_change"] = utils.ratio(bi_data_df["renewed_premium"], bi_data_df["expiring_premium"])
    bi_data_df["rate_change"] = np.where(bi_data_df["rate_change"] == 0, 1, bi_data_df["rate_change"])
    bi_data_df["cumulative_rate_change"] = bi_data_df["rate_change"].cumprod()
    bi_data_df = bi_data_df.loc[:, ["yoa", "exposure", "wep", "incurred", "elr", "cumulative_rate_change"]]
    bi_data_df = bi_data_df.to_dict(orient = "records")

    # 3) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.bi_data.graph_list = bi_data_df
    cds.bi_data.profit = profit
    cds.bi_data.ilr = ilr


