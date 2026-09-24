import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer

from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, query_bi_database

def generate_tags(hxd,progress):

    ## set dataframe variables for cleaner code
    cds = hxd.cds

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    deal_status = cds.deal_status or "EMPTY"
    programme = cds.programme or "EMPTY"
    calc_type = cds.calc_type or "EMPTY"
    territory = cds.territory or "EMPTY"
    tfg = cds.territorial_focus_group or "EMPTY"
    underwriter = cds.standard_fields.underwriter or "EMPTY"
    broker = cds.standard_fields.broker or "EMPTY"
    short_desc = cds.short_description or "EMPTY"
    risk_carrier = short_desc = cds.risk_carrier or "EMPTY"

    # 2) write back ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    tags = pd.Series([
    deal_status,
    programme,
    calc_type, 
    territory,
    tfg + "_tfg",
    underwriter,
    broker,
    short_desc,
    risk_carrier])

    tags = tags.str.replace(" ", "_")
    tags = tags.str.replace(",", "_")
    tags = tags.tolist()

    tags = list(dict.fromkeys(tags))

    hx.meta.policy_tags = tags

    cds.generate_tags_run = True
