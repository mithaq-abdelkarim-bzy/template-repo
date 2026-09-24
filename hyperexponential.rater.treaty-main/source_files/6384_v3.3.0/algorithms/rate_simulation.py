import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer
from algorithms.udf import generate_ymlt, list_to_numpy

def rate_simulation(hxd, common_data_dict):

    ## set dataframe variables for cleaner code
    cds = hxd.cds
    pml = cds.simulation.pml_comparison

    rp_list = [f"rp_{x}" for x in [2, 5, 10, 25, 50, 100, 200, 250, 500, 1000, 5000, 10000]]

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # oep
    simulation_gross = [getattr(pml.simulation_gross, x) for x in rp_list]
    simulation_net_inur = [getattr(pml.simulation_net_inur, x) for x in rp_list]

    model_gross = [getattr(pml.model_gross, x) for x in rp_list]
    model_net_inur = [getattr(pml.model_net_inur, x) for x in rp_list]

    simulation_gross = list_to_numpy(simulation_gross, float)
    simulation_net_inur = list_to_numpy(simulation_net_inur, float)
    model_gross = list_to_numpy(model_gross, float)
    model_net_inur = list_to_numpy(model_net_inur, float)

    # aep
    simulation_gross_aep = [getattr(pml.simulation_gross_aep, x) for x in rp_list]
    simulation_net_inur_aep = [getattr(pml.simulation_net_inur_aep, x) for x in rp_list]

    model_gross_aep = [getattr(pml.model_gross_aep, x) for x in rp_list]
    model_net_inur_aep = [getattr(pml.model_net_inur_aep, x) for x in rp_list]

    simulation_gross_aep = list_to_numpy(simulation_gross_aep, float)
    simulation_net_inur_aep = list_to_numpy(simulation_net_inur_aep, float)
    model_gross_aep = list_to_numpy(model_gross_aep, float)
    model_net_inur_aep = list_to_numpy(model_net_inur_aep, float)

    # 2) Calculate differences and write back ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # oep
    difference_gross = utils.ratio(simulation_gross - model_gross, model_gross)
    difference_net_inur = utils.ratio(simulation_net_inur - model_net_inur, model_net_inur)

    difference_gross = dict(zip(rp_list, difference_gross))
    difference_net_inur = dict(zip(rp_list, difference_net_inur))

    pml.difference_gross = difference_gross
    pml.difference_net_inur = difference_net_inur

    # aep
    difference_gross_aep = utils.ratio(simulation_gross_aep - model_gross_aep, model_gross_aep)
    difference_net_inur_aep = utils.ratio(simulation_net_inur_aep - model_net_inur_aep, model_net_inur_aep)

    difference_gross_aep = dict(zip(rp_list, difference_gross_aep))
    difference_net_inur_aep = dict(zip(rp_list, difference_net_inur_aep))

    pml.difference_gross_aep = difference_gross_aep
    pml.difference_net_inur_aep = difference_net_inur_aep

    # 3) Labels ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(8):
        setattr(cds.simulation.table_labels, f"gross_table_{i}", cds.simulation.file_list[i].description or f"Table {i + 1}")

