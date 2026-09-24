import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer
from scipy.stats import percentileofscore
from hx import params as hx_params
import csv
from scipy.optimize import brentq

from algorithms.udf import list_to_numpy, sim_elt_calc, sim_elt_all, fhcf_recoveries, layer_loss, kpi_calc, reins_calc, generate_oep, duplicate_ylt, mbbefd_inverse, mbbefd_pdf

def run_exposure_simulation(hxd, progress):

    # set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    exp_list = cds.risk_xl_exposure_rating.exposure_listing


    # 1) Load layer info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit_cnv = [layer.limit_cnv for layer in layers]
    occ_limit_cnv = [layer.risk_xl_occurrence_limit_cnv for layer in layers]
    excess_cnv = [layer.excess_cnv for layer in layers]
    aad_cnv = [layer.aggregate_deductible_cnv for layer in layers]
    number_reins = [layer.number_reins for layer in layers]
    perc_reins_1 = [layer.perc_reins_1 for layer in layers]
    perc_reins_2 = [layer.perc_reins_2 for layer in layers]
    perc_reins_3 = [layer.perc_reins_3 for layer in layers]

    limit_cnv = list_to_numpy(limit_cnv, float)
    occ_limit_cnv = list_to_numpy(occ_limit_cnv, float)
    excess_cnv = list_to_numpy(excess_cnv, float)
    aad_cnv = list_to_numpy(aad_cnv, float)
    number_reins = list_to_numpy(number_reins, int)
    perc_reins_1 = list_to_numpy(perc_reins_1, float)
    perc_reins_2 = list_to_numpy(perc_reins_2, float)
    perc_reins_3 = list_to_numpy(perc_reins_3, float)

    # 2) Load ex-cat simulation info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    location_count = [exp_item.location_count for exp_item in exp_list]
    avg_tiv = [exp_item.avg_tiv for exp_item in exp_list]
    expected_frequency = [exp_item.expected_frequency for exp_item in exp_list]
    swiss_re_c = [exp_item.swiss_re_c for exp_item in exp_list]
    avg_cedant_participation = [exp_item.avg_cedant_participation for exp_item in exp_list]
    avg_attachment = [exp_item.avg_attachment for exp_item in exp_list]

    location_count = list_to_numpy(location_count, int)
    avg_tiv = list_to_numpy(avg_tiv, float)
    expected_frequency = list_to_numpy(expected_frequency, float)
    swiss_re_c = list_to_numpy(swiss_re_c, float)
    avg_cedant_participation = list_to_numpy(avg_cedant_participation, float)
    avg_attachment = list_to_numpy(avg_attachment, float)

    prob_loss = np.clip(utils.ratio(expected_frequency, location_count), 0, 1)

    schedule_df = pd.DataFrame({
        "location_count": location_count,
        "avg_tiv": avg_tiv,
        "expected_frequency": expected_frequency,
        "swiss_re_c": swiss_re_c,
        "avg_cedant_participation": avg_cedant_participation,
        "avg_attachment": avg_attachment,
        "prob_loss": prob_loss,
    })

    ## NOTE DAY 2 Shared & Layered Start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    schedule_df["avg_cedant_participation"] = 1
    schedule_df["avg_attachment"] = 0
    ## NOTE DAY 2 Shared & Layered End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    schedule_df = schedule_df.loc[schedule_df["avg_tiv"] > min(limit_cnv)].copy()

    # seed and sims (round to nearest 1000 so total dataframe size later in 250,000)
    np.random.seed(10)
    no_sims = int(round(utils.ratio(250e3, len(schedule_df["prob_loss"])), -3))

    non_cat_ylt = pd.DataFrame({
        "YEAR": np.repeat(np.arange(1, no_sims + 1), len(schedule_df["prob_loss"])),
        "freq": np.random.binomial(
            n = np.tile(schedule_df["location_count"], no_sims),
            p = np.tile(schedule_df["prob_loss"], no_sims)
        ),
        "avg_tiv": np.tile(schedule_df["avg_tiv"], no_sims),
        "swiss_re_c": np.tile(schedule_df["swiss_re_c"], no_sims),
        "avg_cedant_participation": np.tile(schedule_df["avg_cedant_participation"], no_sims),
        "avg_attachment": np.tile(schedule_df["avg_attachment"], no_sims)
    })

    non_cat_ylt["b"] = np.exp(3.1 - 0.15 * (1 + non_cat_ylt["swiss_re_c"]) * non_cat_ylt["swiss_re_c"])
    non_cat_ylt["g"] = np.exp((0.78 + 0.12 * non_cat_ylt["swiss_re_c"]) * non_cat_ylt["swiss_re_c"])

    non_cat_ylt = non_cat_ylt.drop(columns = ["swiss_re_c"])

    non_cat_ylt = (
        non_cat_ylt.loc[non_cat_ylt.index.repeat(non_cat_ylt["freq"])] ###NOTE: THIS COULD CAUSE ISSUES!!!!
        .drop(columns="freq")
        .reset_index(drop=True)
    )

    non_cat_ylt["U"] = np.random.uniform(size = non_cat_ylt.shape[0])
    non_cat_ylt["loss_perc"] = mbbefd_inverse(non_cat_ylt["b"], non_cat_ylt["g"], non_cat_ylt["U"])
    non_cat_ylt["gu_loss"] = non_cat_ylt["loss_perc"] * non_cat_ylt["avg_tiv"]
    non_cat_ylt["subject_loss"] = np.maximum(non_cat_ylt["gu_loss"] - non_cat_ylt["avg_attachment"], 0)

    non_cat_ylt = non_cat_ylt.loc[:, ["YEAR", "subject_loss"]]


    # # #### debug start
    # location_count = location_count[:1]
    # avg_tiv = avg_tiv[:1]
    # expected_frequency = expected_frequency[:1]
    # swiss_re_c = swiss_re_c[:1]

    # non_cat_ylt["check"] = 1 - utils.ratio(1 - non_cat_ylt["b"], (non_cat_ylt["g"] - 1)*non_cat_ylt["b"]**(1 - non_cat_ylt["loss_perc"]) + (1 - non_cat_ylt["g"] * non_cat_ylt["b"]))
    # non_cat_ylt["diff"] = non_cat_ylt["U"] - non_cat_ylt["check"]

    # test = non_cat_ylt[non_cat_ylt["avg_tiv"] < 400e3].copy()

    # non_cat_ylt["gross_loss"] = np.minimum(25e6, np.maximum(0, non_cat_ylt["subject_loss"] - 25e6))
    # print(non_cat_ylt["subject_loss"].sum() / 10e3)
    # print(non_cat_ylt["gross_loss"].sum() / 10e3)


    # 3) Load Cat simulation infor ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cat_el = [layer.model.rms.gross_el for layer in layers]
    cat_el = list_to_numpy(cat_el, float)

    cat_lambda = utils.ratio(cat_el, limit_cnv) ## limit or occurrence limit????? NOTE NOTE NOTE

    # 4) Apply FHCF, Inuring and Beazley layers to final_ylt ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for index, layer in enumerate(layers):

        ## cat ylt
        cat_ylt = pd.DataFrame({
        "YEAR": np.arange(1, no_sims + 1),
        "freq": np.random.poisson(lam = cat_lambda[index], size = no_sims)
        })

        cat_ylt = (
            cat_ylt.loc[cat_ylt.index.repeat(cat_ylt["freq"])] ###NOTE: THIS COULD CAUSE ISSUES!!!!
            .drop(columns="freq")
            .reset_index(drop=True)
        )

        cat_ylt["subject_loss"] = excess_cnv[index] + limit_cnv[index]

        ## final ylt
        final_ylt = pd.concat([non_cat_ylt, cat_ylt])

        final_ylt = (
            final_ylt
            .sample(frac = 1, random_state = 42)
            .sort_values(by = "YEAR")
            .reset_index(drop = True)
        )

        ## layer losses
        final_ylt["gross_el"] = layer_loss(final_ylt.loc[:, ["YEAR", "subject_loss"]],
                                           limit = limit_cnv[index],
                                           excess = excess_cnv[index],
                                           no_reins = 999,
                                           aad = 0,
                                           ded_type = "Conventional")

        final_ylt["net_el_free_reins"] = layer_loss(final_ylt.loc[:, ["YEAR", "subject_loss"]],
                                                    limit = limit_cnv[index],
                                                    excess = excess_cnv[index],
                                                    no_reins = number_reins[index],
                                                    aad = aad_cnv[index],
                                                    ded_type = "Conventional")

        base_percs = [
            perc_reins_1[index],
            perc_reins_2[index],
            perc_reins_3[index]
        ]

        # Take up to the first 3
        reins_perc_list = base_percs[:number_reins[index]]

        # Fill extras with perc_reins_3
        if number_reins[index] > 3:
            reins_perc_list.extend([perc_reins_3[index]] * (number_reins[index] - 3))


        net_el = reins_calc(df = final_ylt,
                            loss_column = "net_el_free_reins",
                            limit = limit_cnv[index],
                            no_reins = number_reins[index],
                            reins_perc = reins_perc_list,
                            sims = no_sims)

        year_agg_ylt_temp = final_ylt.groupby(["YEAR"], as_index = False)[["gross_el", "net_el_free_reins"]].sum()

        year_agg_ylt = pd.DataFrame(data = {"YEAR": range(1, no_sims + 1)})
        year_agg_ylt = pd.merge(year_agg_ylt, year_agg_ylt_temp, on = "YEAR", how="left")
        year_agg_ylt["gross_el"] = year_agg_ylt["gross_el"].fillna(0)
        year_agg_ylt["net_el_free_reins"] = year_agg_ylt["net_el_free_reins"].fillna(0)

        kpi_gross = kpi_calc(year_agg_ylt, "gross_el", no_sims)
        kpi_net_free_reins = kpi_calc(year_agg_ylt, "net_el_free_reins", no_sims)

        model_limit_factor = utils.ratio(kpi_net_free_reins["el"], kpi_gross["el"])
        no_expected_reins = utils.ratio(kpi_net_free_reins["el"] - net_el, net_el)

        layer.risk_xl_exposure_rating.gross_total_el_sim = 0 if pd.isna(kpi_gross["el"]) else float(kpi_gross["el"])
        layer.risk_xl_exposure_rating.model_limit_factor = 0 if pd.isna(model_limit_factor) else float(model_limit_factor)
        layer.risk_xl_exposure_rating.no_expected_reins = 0 if pd.isna(no_expected_reins) else float(no_expected_reins)
            
        del final_ylt

 



        


        

    