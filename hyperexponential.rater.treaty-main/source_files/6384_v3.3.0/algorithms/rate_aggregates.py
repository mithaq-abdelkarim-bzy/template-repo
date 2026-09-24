import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.udf import create_index, layer_loss, ccy_conversion
from hx import params as hx_params
from algorithms.udf import agg_std_dev, reins_approx, ccy_conversion, list_to_numpy
from algorithms.timer import timer


def rate_aggregates(hxd, common_data_dict):

    # set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    granular = cds.exposure.granular.exposures
    aggregates = cds.exposure.aggregate

    # table
    ly_aggregate = [x.ly_aggregate for x in granular]
    ty_aggregate = [x.ty_aggregate for x in granular]
    key_zone_selector = [x.key_zone_selector for x in granular]

    ly_aggregate = list_to_numpy(ly_aggregate, float)
    ty_aggregate = list_to_numpy(ty_aggregate, float)
    key_zone_selector = list_to_numpy(key_zone_selector, float)

    value_change = ty_aggregate - ly_aggregate
    perc_change = utils.ratio(value_change, ly_aggregate)

    for i, agg in enumerate(granular):
        agg.value_change = value_change[i]
        agg.perc_change = perc_change[i]
        
    # summary

    ## exposure_total
    ly_aggregate_total = ly_aggregate.sum()
    ty_aggregate_total = ty_aggregate.sum()

    exposure_total_value_change =  ty_aggregate_total - ly_aggregate_total
    exposure_total_perc_change = utils.ratio(exposure_total_value_change, ly_aggregate_total)

    ## write back to hxd
    aggregates.value_change.exposure_total = exposure_total_value_change
    aggregates.perc_change.exposure_total = exposure_total_perc_change

    aggregates.ly_aggregates.exposure_total = ly_aggregate_total
    aggregates.ty_aggregates.exposure_total = ty_aggregate_total

    ## bespoke total
    ly_bespoke_total = aggregates.ly_aggregates.bespoke_total or 0
    ty_bespoke_total = aggregates.ty_aggregates.bespoke_total or 0

    bespoke_total_value_change =  ty_bespoke_total - ly_bespoke_total
    bespoke_total_perc_change = utils.ratio(bespoke_total_value_change, ly_bespoke_total)

    ## write back to hxd
    aggregates.value_change.bespoke_total = bespoke_total_value_change
    aggregates.perc_change.bespoke_total = bespoke_total_perc_change

    ## key zone total
    ly_key_zone_total = np.sum(ly_aggregate * key_zone_selector)
    ty_key_zone_total = np.sum(ty_aggregate * key_zone_selector)

    key_zone_total_value_change =  ty_key_zone_total - ly_key_zone_total
    key_zone_total_perc_change = utils.ratio(key_zone_total_value_change, ly_key_zone_total)

    ## write back to hxd
    aggregates.ly_aggregates.key_zone_total = ly_key_zone_total
    aggregates.ty_aggregates.key_zone_total = ty_key_zone_total

    aggregates.value_change.key_zone_total = key_zone_total_value_change
    aggregates.perc_change.key_zone_total = key_zone_total_perc_change
