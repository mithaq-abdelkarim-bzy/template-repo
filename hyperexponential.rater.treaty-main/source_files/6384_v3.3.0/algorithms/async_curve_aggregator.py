import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, return_periods, sims
from algorithms.timer import timer
from scipy.stats import percentileofscore
from hx import params as hx_params

from algorithms.udf import generate_ymlt, generate_oep, list_to_numpy, ccy_conversion

def pull_pml_curves(hxd, progress):
    ## set dataframe variables for cleaner code
    cds = hxd.cds
    layers = cds.layers
    curve_agg_write = cds.curve_aggregator.pml_selections
    application_ccy = cds.currency

    # 1) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    weighting_rms = [layer.quote.rol_ty.weighting_rms for layer in layers]
    weighting_air = [layer.quote.rol_ty.weighting_air for layer in layers]
    weighting_rms = list_to_numpy(weighting_rms, float)
    weighting_air = list_to_numpy(weighting_air, float)

    ## set default weighting to be that of lowest layer with weighting applied
    total_weight = weighting_rms + weighting_air
    weighting_rms = utils.ratio(weighting_rms, total_weight)
    weighting_air = utils.ratio(weighting_air, total_weight)
    weight_index = np.where((weighting_air > 0) | (weighting_rms > 0))[0]
    weight_index = weight_index[0] if weight_index.size > 0 else 0

    # 2) Pull and filter PML curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    curve_segments = ["rms_curves", "air_curves", "nmp_curves", "other_curves"]
    segment_names = ["RMS", "AIR", "NMP", "Other"]

    curve_list = [None] * len(curve_segments)
    curve_name = [None] * len(curve_segments)
    include_curve = [None] * len(curve_segments)
    weight_list = [None] * len(curve_segments)

    for index, seg in enumerate(curve_segments):
        pml_curves = getattr(cds.pml_curves, seg)

        ## pull peril, description and currency
        peril_temp = [x.peril for x in pml_curves]
        description = [x.curve_description for x in pml_curves]
        curve_currency = [x.currency for x in pml_curves]
        curve_currency = list_to_numpy(curve_currency, str)
        exchange_rate_multiplicative = ccy_conversion(curve_currency, application_ccy, hx_params.table_currency)

        ## pull curves
        columns_to_read = [f"rp_loss.rp_{x}" for x in return_periods]
        curve_df = utils.pd_df_from_hx_list(pml_curves, columns_to_read)
        curve_df = curve_df.filter(regex = "rp_loss.")
        curve_df.columns = [int(col.replace("rp_loss.rp_", "")) for col in curve_df.columns]
        curve_df = (
            curve_df
            .T
            .reset_index()
            .rename(columns = {"index": "rp"})
            .sort_values("rp", ascending = False)
            .reset_index(drop = True)
            .set_index("rp")
            .fillna(0)
        )

        # filter which to include e.g [0,2,3,4]
        curve_df_0_index = curve_df.sum(axis = 0) > 0
        include_index = [x.include_in_peril_alloc for x in pml_curves]
        include_index = list_to_numpy(include_index, data_type=str)
        include_index = np.where(include_index == "Yes", 1, 0)
        final_index = curve_df_0_index * include_index
        final_index = final_index[final_index > 0].index.to_list()
        curve_df = curve_df[final_index].copy()

        ## pull in peril, description and exchange rate for each curve
        peril = [peril_temp[i] for i in final_index]
        description = [description[i] for i in final_index]
        exchange_rate_multiplicative = [exchange_rate_multiplicative[i] for i in final_index]

        peril = list_to_numpy(peril, str)
        description = list_to_numpy(description, str)
        description = np.where(description == "None", "", description)
        exchange_rate_multiplicative = list_to_numpy(exchange_rate_multiplicative, float)

        ## currency conversion of the curves
        curve_df[final_index] = curve_df[final_index].multiply(exchange_rate_multiplicative, axis=1)

        if len(peril) > 0:
            ## set weights for each curve
            default_weight = 1 if seg in ["nmp_curves", "rms_curves"] else 0
            weight_temp = np.full(len(peril), default_weight)
            if seg == "rms_curves":
                weight_temp[:] = weighting_rms[weight_index]
            elif seg == "air_curves":
                weight_temp[:] = weighting_air[weight_index]
            weight_list[index] = weight_temp

            ## set name for each curve RMS AP etc
            curve_name_temp = np.char.add(f"{segment_names[index]} ", peril)
            curve_name_temp = np.char.add(curve_name_temp, " ")
            curve_name_temp = np.char.add(curve_name_temp, description)
            curve_name[index] = curve_name_temp
            ## if AP curve exists, only include that, otherwise include individual peril curves
            include_curve_temp = list_to_numpy(peril, data_type = str)
            include_curve_temp = np.where(include_curve_temp == "AP", True, False)
            if include_curve_temp.sum() == 0:
                include_curve_temp[:] = True
            include_curve_temp = np.where(weight_temp == 0, False, include_curve_temp)
            
            include_curve[index] = include_curve_temp

        curve_list[index] = curve_df

    all_curves = pd.concat(curve_list, axis = 1)
    all_curves.columns = range(all_curves.shape[1])

    curve_name = [x for x in curve_name if x is not None]
    curve_name = np.concatenate(curve_name)

    include_curve = [x for x in include_curve if x is not None]
    include_curve = np.concatenate(include_curve)

    weight_list = [x for x in weight_list if x is not None]
    weight_list = np.concatenate(weight_list)

    # 3) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    to_write = [{
        "include_in_aggregator": include_curve[i],
        "weight": weight_list[i],
        "name": curve_name[i] ,
        "rp_loss": {
            "rp_2": all_curves.at[2, i],
            "rp_5": all_curves.at[5, i],
            "rp_10": all_curves.at[10, i],
            "rp_25": all_curves.at[25, i],
            "rp_50": all_curves.at[50, i],
            "rp_100": all_curves.at[100, i],
            "rp_200": all_curves.at[200, i],
            "rp_250": all_curves.at[250, i],
            "rp_500": all_curves.at[500, i],
            "rp_1000": all_curves.at[1000, i],
            "rp_5000": all_curves.at[5000, i],
            "rp_10000": all_curves.at[10000, i]
            }
    } for i in range(all_curves.shape[1])
    ]

    cds.curve_aggregator.pml_selections = to_write

def aggregate_curves(hxd,progress):
    ## set dataframe variables for cleaner code
    cds = hxd.cds  
    layers = cds.layers
    pml_curves = cds.curve_aggregator.pml_selections
    agg_output = cds.curve_aggregator.aggregator_output.rp_loss

    # 1) Pull and filter PML curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    curve_df = utils.pd_df_from_hx_list(pml_curves)
    curve_df = curve_df.fillna(0)
    curve_df = curve_df[(curve_df["include_in_aggregator"] & curve_df["name"] != 0)].reset_index(drop = True)

    # 2) Logic to determine weights between different curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    weight_df = curve_df[["name","weight"]].copy()
    curve_df = curve_df.drop(columns = ["include_in_aggregator","name","weight"])

    curve_df.columns = [int(col.replace("rp_loss/rp_", "")) for col in curve_df.columns]
    curve_df = (
        curve_df
        .T
        .reset_index()
        .rename(columns = {"index": "rp"})
        .sort_values("rp", ascending = False)
        .reset_index(drop = True)
        .fillna(0)
    )

    # identify which curves full weight and which to be paired
    full_weight_df = weight_df[weight_df["weight"] == 1].copy()
    partial_weight_df = weight_df[weight_df["weight"] != 1].copy()

    # match partial weight curves
    partial_weight_df["sub_name"] = partial_weight_df["name"].str.replace("RMS ","")
    partial_weight_df["sub_name"] = partial_weight_df["sub_name"].str.replace("AIR ","")

    ### create a list of pairs of duplicated curve names e.g, [[2, 3], [5, 7]]
    ### convert the naive index (from np.where) to the curve_df index
    ### converting arrays to lists
    partial_pairs_list = [
        group.index.to_list()
        for _, group in partial_weight_df.groupby("sub_name")
    ]
    full_weight_list = list(full_weight_df.index.values)

    # 3) loop through full weight and parital weight, append to list of DFs, concatenate at end ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    df_list = [None] * (len(full_weight_list) + len(partial_pairs_list))

    ## full weight
    for index, i in enumerate(full_weight_list):
        curve_temp = curve_df[["rp", i]].copy()
        curve_temp.columns = ["rp", "cedant_loss"]
        df_list[index] = generate_ymlt(curve_temp, sims)

    ## partial weight
    curve_weights = partial_weight_df["weight"]
    for index, i in enumerate(partial_pairs_list):
        curve_index_1 = i[0]
        curve_index_2 = i[1]
        
        curve_weight_1 = curve_weights.at[curve_index_1]
        curve_weight_2 = curve_weights.at[curve_index_2]

        curve_temp = curve_df[["rp", curve_index_1, curve_index_2]].copy()     
        curve_temp.columns = ["rp", "curve_1", "curve_2"]
        curve_temp["cedant_loss"] = curve_temp["curve_1"] * curve_weight_1 + curve_temp["curve_2"] * curve_weight_2
        curve_temp = curve_temp.drop(columns = ["curve_1", "curve_2"])

        df_list[len(full_weight_list) + index] = generate_ymlt(curve_temp, sims)

    # 3) Set total YMLT and calculate OEP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    total_ymlt = pd.concat(df_list)

    rp_array = np.array(hx.params.table_return_periods["return_period"])
    rp_array = np.sort(rp_array)[::-1]
    oep_curve = generate_oep(total_ymlt, "cedant_loss", sims, rp_array)

    agg_output = {
        "rp_2": oep_curve["loss"][11],
        "rp_5": oep_curve["loss"][10],
        "rp_10": oep_curve["loss"][9],
        "rp_25": oep_curve["loss"][8],
        "rp_50": oep_curve["loss"][7],
        "rp_100": oep_curve["loss"][6],
        "rp_200": oep_curve["loss"][5],
        "rp_250": oep_curve["loss"][4],
        "rp_500": oep_curve["loss"][3],
        "rp_1000": oep_curve["loss"][2],
        "rp_5000": oep_curve["loss"][1],
        "rp_10000": oep_curve["loss"][0]
    }
    
    # 4) extract entry and exit points ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit_cnv = [layer.limit_cnv for layer in layers]
    excess_cnv = [layer.excess_cnv for layer in layers]

    limit_cnv = list_to_numpy(limit_cnv, float)
    excess_cnv = list_to_numpy(excess_cnv, float)
    exit_point = limit_cnv + excess_cnv

    max_ymlt = total_ymlt.groupby("year")["cedant_loss"].agg("max")

    percentile_attach = utils.ratio(percentileofscore(max_ymlt, excess_cnv), 100)
    percentile_exit = utils.ratio(percentileofscore(max_ymlt, exit_point), 100)

    rp_attach = np.where(percentile_attach > 0, utils.ratio(1, (1 - percentile_attach)), 0)
    rp_exit = np.where(percentile_attach > 0, utils.ratio(1, (1 - percentile_exit)), 0)

    # 5) write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.curve_aggregator.aggregator_output.rp_loss = agg_output

    cds.pml_curves.curve_aggregator.rp_loss = agg_output

    for index, layer in enumerate(layers):
        layer.quote.rol_ty.curve_agg_rp_attach = rp_attach[index]
        layer.quote.rol_ty.curve_agg_rp_exit = rp_exit[index]


    
