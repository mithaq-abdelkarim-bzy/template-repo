import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import policy_term
from operator import itemgetter
from algorithms.rate_constants import max_curves
import algorithms.rate_utilities as utils
from algorithms.timer import timer
from hx import params as hx_params

from algorithms.udf import agg_std_dev, list_to_numpy


def rate_calculator(hxd, common_data_dict):

    cds = hxd.cds
    calculator = cds.calculator

    calc_df = utils.pd_df_from_hx_list(calculator.input_list)

    calculator.results.el = calc_df["el"].sum()
    calculator.results.sd = agg_std_dev(calc_df["sd"])
