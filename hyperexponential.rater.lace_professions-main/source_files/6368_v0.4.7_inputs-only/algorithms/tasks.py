# v0.5.0
import hx
import json
import math
import datetime
import os
import requests
import openpyxl
import copy

import pandas as pd
import numpy as np
import algorithms.rate_utilities as utils
from algorithms.task_start_renewal import task_start_renewal
from algorithms.rate_change.task_rarc_expiry_policy_fetch import task_expiring_policy_fetch, task_expiring_policy_fetch_coverage
from algorithms.rate_change.task_rarc import task_rarc_layer, task_rarc_coverage
from algorithms.rate_change.task_rarc_insured_asset import task_rarc_layer_insured_asset, task_rarc_coverage_insured_asset
from algorithms.task_policy_document import task_policy_to_excel
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report
from algorithms.rate_constants import (
    policy_structure_to_dataframe,
    policy_addl_structure_to_dataframe,
    retention_to_dataframe,
    territory_to_dataframe,
    client_details_lawyers_to_dataframe,
    client_details_aec_to_dataframe,
    get_fx_rate,
    get_fx_rate_base,
    get_base_params,
    get_tech_params,
    get_nmp_load,
    territory_labels,
    chart_revenue_steps,
)
from algorithms.year_frac import diffdays
from algorithms.rate_simulation import run_simulation

from algorithms.rate_simulation_inputs import get_model_params, get_ded_params, get_quotes_params, get_quotes_params_addl, validate_simulation_inputs, get_current_simulation_snapshot_json, _persist_simulation_snapshot





@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id


@hx.task
def start_renewal_task(hxd, progress):
    task_start_renewal(hxd, progress)


@hx.task
def expiring_policy_fetch_task(hxd, progress):
    task_expiring_policy_fetch(hxd, progress)


# Importing expiring policy info for rate change
@hx.task
def expiring_policy_fetch_coverages_task(hxd, progress):
    task_expiring_policy_fetch_coverage(hxd, progress)


@hx.task
def rarc_task(hxd, progress):
    task_rarc_layer(hxd, progress)


@hx.task
def rarc_task_coverages(hxd, progress):
    task_rarc_coverage(hxd, progress)


@hx.task
def rarc_task_insured_asset(hxd, progress):
    task_rarc_layer_insured_asset(hxd, progress)


@hx.task
def rarc_task_coverages_insured_asset(hxd, progress):
    task_rarc_coverage_insured_asset(hxd, progress)


# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):
    task_policy_to_excel(hxd, progress)


# Log new bug - add the following 5 methods for bug report section
@hx.task
def new_bug_report_task(hxd, progress):
    # Update rater name
    model_name = "Skeleton"
    new_bug_report(hxd, progress, model_name)


@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)


@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)


@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)


@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)


@hx.task
def import_claims_task(hxd, progress):
    pass


def run_simulation_charts_task(hxd, progress):
    results = {}
    results_addl = {}
    # validation
    validate_simulation_inputs(hxd, progress)

    profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"    
    bp = get_base_params(profession)
    df_quote_params = get_quotes_params(hxd)
    df_quote_params_addl = get_quotes_params_addl(hxd)
    df_ded_params = get_ded_params(hxd)

    for expected_exposure in chart_revenue_steps:
        df_ModelParamsFinal, df_ModelParamsUnadjustedFinal = get_model_params(hxd, profession, expected_exposure)
        # # Run the simulation
        df_modeloutputs, df_addmodeloutputs = run_simulation(
            ded_params = df_ded_params, 
            model_params = df_ModelParamsFinal, 
            quotes_params = df_quote_params, 
            add_quotes_params = df_quote_params_addl, 
            revenue = hxd.cds.exposure.granular.exposure_expected_current_year,
            r_scalar_input_odf = bp.odf,
            num_sims = 5000)
        results[expected_exposure] = df_modeloutputs["BookRate"].iloc[0]            # only first layer - needs to handle all
        results_addl[expected_exposure] = df_addmodeloutputs["BookRate"].iloc[0]

    df_results = pd.concat(results, names=["expected_exposure"]).reset_index(level=0)
    df_results.columns =["expected_exposure", "BookRate"]
    df_results["loss_cost"] = df_results["expected_exposure"] / 1e6 * df_results["BookRate"]
    df_results.rename(columns={"expected_exposure":"revenue"})
    df_results = df_results[["revenue", "loss_cost"]]

    df_results_addl = pd.concat(results_addl, names=["expected_exposure"]).reset_index(level=0)
    df_results_addl.columns =["expected_exposure", "BookRate"]
    df_results_addl["loss_cost"] = df_results_addl["expected_exposure"] / 1e6 * df_results_addl["BookRate"]
    df_results_addl.rename(columns={"expected_exposure":"revenue"})
    df_results_addl = df_results_addl[["revenue", "loss_cost"]]

    # write to relevant nodes


@hx.task
def run_simulation_task(hxd, progress):

    # validation
    validate_simulation_inputs(hxd, progress)

    # Get simulation input dataframes.
    expected_exposure = (hxd.cds.exposure.granular.exposure_expected_current_year or 0)
    profession = "lpl" if hxd.cds.profession == "Lawyers" else "aec"
    bp = get_base_params(profession)
    df_quote_params = get_quotes_params(hxd)
    df_quote_params_addl = get_quotes_params_addl(hxd)
    df_ded_params = get_ded_params(hxd)
    df_ModelParamsFinal, df_ModelParamsUnadjustedFinal = get_model_params(hxd, profession, expected_exposure)

    # Persist the input parameters that were used to drive the simulation.
    snapshot_json = get_current_simulation_snapshot_json(hxd)
    _persist_simulation_snapshot(hxd, snapshot_json)

    # Run the simulation
    df_modeloutputs, df_addmodeloutputs = run_simulation(
        ded_params = df_ded_params, 
        model_params = df_ModelParamsFinal, 
        quotes_params = df_quote_params, 
        add_quotes_params = df_quote_params_addl, 
        revenue = hxd.cds.exposure.granular.exposure_expected_current_year,
        r_scalar_input_odf = bp.odf,
        num_sims = 50000)

    counter = 0
    for idx, layer in enumerate(hxd.cds.layers):
        if layer.include:
            layer.sim_output_uw_adj.exposure_premium = df_modeloutputs["BookRate"].iloc[counter]
            layer.sim_output_uw_adj.average_freq = df_modeloutputs["FreqPer1000"].iloc[counter]
            layer.sim_output_uw_adj.average_defense_cost_freq = df_modeloutputs["DefFreqFGUPer1000"].iloc[counter]
            layer.sim_output_uw_adj.layer_exhaust_prob = df_modeloutputs["ExhaustionProb"].iloc[counter]
            layer.exposure_rate = df_modeloutputs["BookRate"].iloc[counter]
            counter += 1

    counter = 0
    for idx, layer in enumerate(hxd.cds.layers_addl):
        if layer.include:
            layer.sim_output_uw_adj.exposure_premium = df_addmodeloutputs["BookRate"].iloc[counter]
            layer.sim_output_uw_adj.average_freq = df_addmodeloutputs["FreqPer1000"].iloc[counter]
            layer.sim_output_uw_adj.average_defense_cost_freq = df_addmodeloutputs["DefFreqFGUPer1000"].iloc[counter]
            layer.sim_output_uw_adj.layer_exhaust_prob = df_addmodeloutputs["ExhaustionProb"].iloc[counter]
            layer.exposure_rate = df_addmodeloutputs["BookRate"].iloc[counter]
            counter += 1
            
    #run_simulation_charts_task(hxd, progress)