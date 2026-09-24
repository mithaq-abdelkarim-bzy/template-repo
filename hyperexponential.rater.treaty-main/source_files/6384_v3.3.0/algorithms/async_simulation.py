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

from algorithms.udf import list_to_numpy, sim_elt_calc, sim_elt_all, fhcf_recoveries, layer_loss, kpi_calc, reins_calc, generate_oep, duplicate_ylt

def file_processing(hxd, progress):

    # set dataframe variables for cleaner code
    cds = hxd.cds  
    sim = cds.simulation

    max_files = 8

    elt_col_names_expected = ["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "TABLE_INDEX"]
    ylt_col_names_expected = ["YEAR", "EVENTID", "LOSS", "TABLE_INDEX"]

    elt_col_set = set(elt_col_names_expected)
    ylt_col_set = set(ylt_col_names_expected)

    file_name = [None] * max_files
    table_type = [None] * max_files
    max_sims = [None] * max_files
    table_el = [None] * max_files

    elt_count = 0
    ylt_count = 0

    # Load tables
    for i in range(max_files):
        file_node = getattr(sim.files, f"input_file_{i + 1}")
        if file_node.exists:
            with file_node.open(mode="b") as f:
                temp = pd.read_csv(f)

            temp = temp.rename(columns=str.upper) 
            temp["TABLE_INDEX"] = i
            temp_col_set = set(temp.columns.values)

            # store file name
            file_name[i] = file_node.file_name
            
            # store table type and max sims
            if elt_col_set.issubset(temp_col_set):
                table_type[i] = "ELT"
                table_el[i] = (temp["RATE"] * temp["PERSPVALUE"]).sum()
                elt_count += 1
            elif ylt_col_set.issubset(temp_col_set):
                table_type[i] = "YLT"
                max_sims[i] = temp["YEAR"].max()
                table_el[i] = utils.ratio((temp["LOSS"]).sum(), temp["YEAR"].max())
                ylt_count += 1
            else:
                table_type[i] = "Check Columns"

    # write back to hxd
    for index, file in enumerate(sim.file_list):
        file.file_name = file_name[index]
        file.table_type = table_type[index]
        file.max_sims = max_sims[index]
        file.table_el = table_el[index]

    if ylt_count > 0:
        max_sims = list_to_numpy(max_sims, int)
        max_sims = max_sims[max_sims > 0]
        max_sims = (np.ceil(max_sims / 1e3) * 1e3).astype(np.int64)
        lcm = np.lcm.reduce(max_sims)
        cds.simulation.sims_lcm = lcm

    # sims commentary
    if (elt_count > 0) & (ylt_count == 0):
        cds.simulation.sims_commentary = "ELTs only, no restrictions on No. Sims."
    elif (ylt_count > 0) & (elt_count == 0):
        cds.simulation.sims_commentary = f"YLTs only, No. Sims must be a multiple of {lcm:,}."
    elif (ylt_count > 0) & (elt_count > 0):
        cds.simulation.sims_commentary = f"ELTs and YLTs, No. Sims must be a multiple of {lcm:,}."


def run_simulation(hxd, progress):

    # load parameter tables
    other_event_state_map = hx_params.table_event_state_map
    ws_event_state_map = hx_params.table_ws_event_state_map

    # set dataframe variables for cleaner code
    cds = hxd.cds  
    sim = cds.simulation
    file_list = sim.file_list
    layers = cds.layers

    # seed and sims
    np.random.seed(10)
    no_sims = sim.max_sims

    # YLT sims error handling
    lcm = cds.simulation.sims_lcm or 0

    if lcm > 0:
        if no_sims % lcm != 0:
            hx.errors.fatal(f"YLT tables included, sims must be a multiple of {lcm:,}")

    # table info
    max_files = 8

    elt_col_names_expected = ["EVENTID", "RATE", "PERSPVALUE", "STDDEVC", "STDDEVI", "EXPVALUE", "TABLE_INDEX"]
    ylt_col_names_expected = ["YEAR", "EVENTID", "LOSS", "TABLE_INDEX"]

    # 1) Load layer info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    limit = [layer.limit for layer in layers]
    excess = [layer.excess for layer in layers]
    inner_type = [layer.inner_type for layer in layers]
    inner_type = [x if x is not None else "Conventional" for x in inner_type]
    aad = [layer.aggregate_deductible for layer in layers]
    number_reins = [layer.number_reins for layer in layers]
    perc_reins_1 = [layer.perc_reins_1 for layer in layers]
    perc_reins_2 = [layer.perc_reins_2 for layer in layers]
    perc_reins_3 = [layer.perc_reins_3 for layer in layers]

    run_layer = [sim_layer.simulation.run_layer for sim_layer in layers]
    include_combined_layer_1 = [sim_layer.simulation.include_combined_layer_1 for sim_layer in layers]
    include_combined_layer_2 = [sim_layer.simulation.include_combined_layer_2 for sim_layer in layers]

    include_table_1 = [sim_layer.simulation.sim_coverage.coverage_1 for sim_layer in layers]
    include_table_2 = [sim_layer.simulation.sim_coverage.coverage_2 for sim_layer in layers]
    include_table_3 = [sim_layer.simulation.sim_coverage.coverage_3 for sim_layer in layers]
    include_table_4 = [sim_layer.simulation.sim_coverage.coverage_4 for sim_layer in layers]
    include_table_5 = [sim_layer.simulation.sim_coverage.coverage_5 for sim_layer in layers]
    include_table_6 = [sim_layer.simulation.sim_coverage.coverage_6 for sim_layer in layers]
    include_table_7 = [sim_layer.simulation.sim_coverage.coverage_7 for sim_layer in layers]
    include_table_8 = [sim_layer.simulation.sim_coverage.coverage_8 for sim_layer in layers]

    limit = list_to_numpy(limit, float)
    excess = list_to_numpy(excess, float)
    aad = list_to_numpy(aad, float)
    number_reins = list_to_numpy(number_reins, int)
    perc_reins_1 = list_to_numpy(perc_reins_1, float)
    perc_reins_2 = list_to_numpy(perc_reins_2, float)
    perc_reins_3 = list_to_numpy(perc_reins_3, float)

    use_agg_qs_method = cds.show_agg_qs_input

    # 2) Load simulation info ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    exposure_increase = sim.exposure_increase if sim.exposure_increase else 0
    subject_lae = sim.subject_lae if sim.subject_lae else 0
    cut_off = sim.cut_off if sim.cut_off else 0

    attr_mean = sim.attritional_sim.mean or 0
    attr_sd = sim.attritional_sim.sd or 0

    qualifying_excess = [file.qualifying_excess for file in file_list]
    qualifying_limit = [file.qualifying_limit for file in file_list]

    fhcf_1_include = [file.fhcf_1 for file in file_list]
    fhcf_2_include = [file.fhcf_2 for file in file_list]

    inur_1_include = [file.inur_1 for file in file_list]
    inur_2_include = [file.inur_2 for file in file_list]
    inur_3_include = [file.inur_3 for file in file_list]
    inur_4_include = [file.inur_4 for file in file_list]

    qualifying_excess = list_to_numpy(qualifying_excess, float)
    qualifying_limit = list_to_numpy(qualifying_limit, float)

    fhcf_1_include = list_to_numpy(fhcf_1_include, float)
    fhcf_2_include = list_to_numpy(fhcf_2_include, float)

    inur_1_include = list_to_numpy(inur_1_include, float)
    inur_2_include = list_to_numpy(inur_2_include, float)
    inur_3_include = list_to_numpy(inur_3_include, float)
    inur_4_include = list_to_numpy(inur_4_include, float)

    combined_1 = {child_name: child_node for child_name, child_node in sim.combined_1}
    combined_2 = {child_name: child_node for child_name, child_node in sim.combined_2}

    fhcf_1 = {child_name: child_node for child_name, child_node in sim.fhcf_1}
    fhcf_2 = {child_name: child_node for child_name, child_node in sim.fhcf_2}
    inur_1 = {child_name: child_node for child_name, child_node in sim.inuring_ri.inur_1}
    inur_2 = {child_name: child_node for child_name, child_node in sim.inuring_ri.inur_2}
    inur_3 = {child_name: child_node for child_name, child_node in sim.inuring_ri.inur_3}
    inur_4 = {child_name: child_node for child_name, child_node in sim.inuring_ri.inur_4}

    # 3) Load ELTs and YLTs, + sim ELTs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    elt_col_set = set(elt_col_names_expected)
    ylt_col_set = set(ylt_col_names_expected)

    elt_list = [None] * max_files
    ylt_list = [None] * max_files

    ## Load tables
    for i in range(max_files):
        file_node = getattr(sim.files, f"input_file_{i + 1}")
        if file_node.exists:
            with file_node.open(mode="b") as f:
                temp = pd.read_csv(f)

            temp = temp.rename(columns=str.upper) 
            temp["TABLE_INDEX"] = i
            temp_col_set = set(temp.columns.values)
            
            # store table
            if elt_col_set.issubset(temp_col_set):
                temp = temp[elt_col_names_expected]
                elt_list[i] = temp
            elif ylt_col_set.issubset(temp_col_set):
                temp = temp[ylt_col_names_expected]
                temp = duplicate_ylt(temp, no_sims)
                ylt_list[i] = temp

    
    ###### Easy Debugging Start TODO
    # temp = pd.read_csv("/workspace/editing/test_cases/input_file_1.csv")
    # temp["TABLE_INDEX"] = 0
    # elt_list[0] = temp
    # temp = pd.read_csv("/workspace/editing/test_cases/input_file_2.csv")
    # temp["TABLE_INDEX"] = 1
    # elt_list[1] = temp

    # temp = pd.read_csv("/workspace/editing/test_cases/AP ELT.csv")
    # temp["TABLE_INDEX"] = 0
    # temp = temp[elt_col_names_expected]
    # elt_list[0] = temp

    # no_sims = 100000
    # use_agg_qs_method = True
    # limit[0] = 100e6
    # excess[0] = 50e6
    # temp = pd.read_csv("/workspace/editing/test_cases/ws_ylt.csv")
    # temp = temp.rename(columns=str.upper) 
    # temp["TABLE_INDEX"] = 0
    # temp_col_set = set(temp.columns.values)
    # temp = temp[ylt_col_names_expected]
    # temp = duplicate_ylt(temp, no_sims)
    # duplicate_ylt(temp, no_sims)["LOSS"].sum() / no_sims
    # ylt_list[0] = temp

    # final_ylt.to_csv("/workspace/editing/test_cases/final_ylt.csv")
    #np.random.seed(10)
    ###### Easy Debugging End

    no_elts = sum(1 for x in elt_list if x is not None)
    no_ylts = sum(1 for x in ylt_list if x is not None)

    if (no_elts > 0) & (no_ylts > 0):
        ## stack elts
        stacked_elt = pd.concat(elt_list, ignore_index = True)
        ## generate ylt from elt
        ylt_from_elt = sim_elt_all(stacked_elt, no_sims)
        ## stack ylts
        stacked_ylt = pd.concat(ylt_list, ignore_index = True)
        final_ylt = pd.concat([ylt_from_elt, stacked_ylt], ignore_index = True)
    elif no_elts > 0:
        ## stack elts
        stacked_elt = pd.concat(elt_list, ignore_index = True)
        ## generate ylt from elt
        ylt_from_elt = sim_elt_all(stacked_elt, no_sims)
        final_ylt = ylt_from_elt.copy()
    elif no_ylts > 0:
        ## stack ylts
        stacked_ylt = pd.concat(ylt_list, ignore_index = True)
        final_ylt = stacked_ylt.copy()
    else:
        final_ylt = pd.DataFrame(columns = ylt_col_names_expected)
        final_ylt["YEAR"] = range(1, no_sims + 1)
        final_ylt = final_ylt.fillna(0)

    # 4) Apply FHCF, Inuring and Beazley layers to final_ylt ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if final_ylt.shape[0] > 0:
        ## scale for exposure increase
        final_ylt["LOSS"] = final_ylt["LOSS"] * (1 + exposure_increase)
        final_ylt = final_ylt[final_ylt["LOSS"] >= cut_off]
        ## turn table losses into columns: needed for differing inuring / fhcf application between tables
        ## unstack applies to right most index, ie here applies to table_index
        final_ylt = final_ylt.groupby(['YEAR', 'EVENTID', 'TABLE_INDEX'])['LOSS'].sum().unstack(fill_value = 0)
        final_ylt = final_ylt.reset_index()
        final_ylt.columns = final_ylt.columns.map(str)
        ## get loss columns in scope to avoid errors later
        columns_in_scope = final_ylt.columns
        columns_in_scope = [x for x in columns_in_scope if x not in ["YEAR", "EVENTID"]]

        ## 4.1) FHCF Inuring ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        fhcf_table = pd.DataFrame([fhcf_1, fhcf_2])
        fhcf_table = fhcf_table.fillna(0)

        fhcf_1_include = np.where(fhcf_1_include)[0].astype(str)
        fhcf_2_include = np.where(fhcf_2_include)[0].astype(str)

        fhcf_1_include = [x for x in fhcf_1_include if x in columns_in_scope]
        fhcf_2_include = [x for x in fhcf_2_include if x in columns_in_scope]     

        if fhcf_1_include:
            final_ylt["fhcf_1_recovery"] = fhcf_recoveries(year = final_ylt["YEAR"],
                                                           indemnity_loss = final_ylt[fhcf_1_include].sum(axis = 1),
                                                           fhcf_limit = fhcf_table["limit"].iloc[0],
                                                           fhcf_excess = fhcf_table["excess"].iloc[0],
                                                           fhcf_participation = fhcf_table["participation"].iloc[0],  
                                                           lae_actual = subject_lae,
                                                           lae_cap = fhcf_table["lae_cap"].iloc[0])
        else:
            final_ylt["fhcf_1_recovery"] = 0

        if fhcf_2_include:
            final_ylt["fhcf_2_recovery"] = fhcf_recoveries(year = final_ylt["YEAR"],
                                                           indemnity_loss = final_ylt[fhcf_2_include].sum(axis = 1),
                                                           fhcf_limit = fhcf_table["limit"].iloc[0],
                                                           fhcf_excess = fhcf_table["excess"].iloc[0],
                                                           fhcf_participation = fhcf_table["participation"].iloc[0], 
                                                           lae_actual = subject_lae,
                                                           lae_cap = fhcf_table["lae_cap"].iloc[0])
        else:
            final_ylt["fhcf_2_recovery"] = 0

        ## write back to hxd
        kpi_fhcf_1 = kpi_calc(final_ylt, "fhcf_1_recovery", no_sims)
        kpi_fhcf_2 = kpi_calc(final_ylt, "fhcf_2_recovery", no_sims)
        
        sim.fhcf_1.el = kpi_fhcf_1["el"]
        sim.fhcf_1.sd = kpi_fhcf_1["sd"]
        sim.fhcf_2.el = kpi_fhcf_2["el"]
        sim.fhcf_2.sd = kpi_fhcf_2["sd"]

        ## 4.2) Other Inuring ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        inur_table = pd.DataFrame([inur_1, inur_2, inur_3, inur_4])
        inur_table = inur_table.fillna(0)
        inur_table["deductible_type"] = np.where(inur_table["deductible_type"] == 0, "Conventional", inur_table["deductible_type"])

        inur_1_include = np.where(inur_1_include)[0].astype(str)
        inur_2_include = np.where(inur_2_include)[0].astype(str)
        inur_3_include = np.where(inur_3_include)[0].astype(str)
        inur_4_include = np.where(inur_4_include)[0].astype(str)

        inur_1_include = [x for x in inur_1_include if x in columns_in_scope]
        inur_2_include = [x for x in inur_2_include if x in columns_in_scope]
        inur_3_include = [x for x in inur_3_include if x in columns_in_scope] 
        inur_4_include = [x for x in inur_4_include if x in columns_in_scope] 

        inur_include = {
                        "inur_1_include": inur_1_include,
                        "inur_2_include": inur_2_include,
                        "inur_3_include": inur_3_include,
                        "inur_4_include": inur_4_include
                        }

        for i in range(4):
            if inur_include[f"inur_{i + 1}_include"]:
                lae_final = inur_table["inur_lae"].iloc[i]
                lae_factor = 1 + lae_final
                final_ylt["net_fhcf_subject_inur"] = (
                                                      (final_ylt[inur_include[f"inur_{i + 1}_include"]].sum(axis = 1) * lae_factor) 
                                                      - final_ylt["fhcf_1_recovery"] 
                                                      - final_ylt["fhcf_2_recovery"]
                                                     )
                
                final_ylt["temp_inur_recovery"] = layer_loss(final_ylt.loc[:, ["YEAR", "net_fhcf_subject_inur"]],
                                                             limit = inur_table["limit"].iloc[i],
                                                             excess = inur_table["excess"].iloc[i],
                                                             no_reins = inur_table["reinstatements"].iloc[i],
                                                             aad = 0,
                                                             ded_type = inur_table["deductible_type"].iloc[i])

                final_ylt["temp_inur_recovery"] = final_ylt["temp_inur_recovery"] * inur_table["placed"].iloc[i]
                final_ylt = final_ylt.drop(columns = "net_fhcf_subject_inur")
                del lae_factor
            else:
                final_ylt["temp_inur_recovery"] = 0

            final_ylt = final_ylt.rename(columns = {"temp_inur_recovery": f"inur_{i + 1}_recovery"})

        ## 4.3) Subject Layers ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Store attritional losses for later use
        if (attr_mean > 0) and (attr_sd > 0) and use_agg_qs_method:
            ## method of moments
            mu = np.log(attr_mean**2) - np.log(np.sqrt(attr_mean**2 + attr_sd**2))
            sigma2 = np.log(1 + attr_sd**2 / attr_mean**2)

            attr_losses = np.random.lognormal(mean = mu, sigma = np.sqrt(sigma2), size = no_sims)
        else:
            attr_losses = 0

        subject_include_table = pd.DataFrame([include_table_1,
                                              include_table_2,
                                              include_table_3,
                                              include_table_4,
                                              include_table_5,
                                              include_table_6,
                                              include_table_7, 
                                              include_table_8])

        ### A) scale table losses for subject LAE
        subject_lae_factor = 1 + subject_lae
        for col in columns_in_scope:
            final_ylt[col] *= subject_lae_factor

        for index, layer in enumerate(layers):
            if run_layer[index]:
                ## which tables included in layer
                layer_include = subject_include_table[index]
                layer_include = np.array(layer_include)
                layer_include = np.where(layer_include)[0].astype(str)
                layer_include = [x for x in layer_include if x in columns_in_scope]

                table_include = [int(x) for x in layer_include]

                layer_ylt = final_ylt.copy()

                ### B) Calculte AAL applicable to layer
                layer_ylt["temp_aal"] = layer_ylt[layer_include].sum(axis = 1)
                
                kpi_aal = kpi_calc(layer_ylt, "temp_aal", no_sims, attr_losses)
                layer.simulation.sim_result.aal = kpi_aal["el"]

                ### C) Allocate fhcf and inuring recovery based on table loss

                ##~~ add pre inuring losses
                layer_ylt["pre_inur_beazley_layers"] = 0

                for col in layer_include:                    
                    layer_ylt["pre_inur_temp"] = layer_ylt[col]
                    layer_ylt["pre_inur_beazley_layers"] += layer_ylt["pre_inur_temp"]
                    ##~~

                for col in layer_include:
                    layer_ylt[col] = (
                        layer_ylt[col]
                        - (utils.ratio(layer_ylt[col], layer_ylt[fhcf_1_include].sum(axis = 1)) * layer_ylt["fhcf_1_recovery"] if col in fhcf_1_include else 0)
                        - (utils.ratio(layer_ylt[col], layer_ylt[fhcf_2_include].sum(axis = 1)) * layer_ylt["fhcf_2_recovery"] if col in fhcf_2_include else 0)
                        - (utils.ratio(layer_ylt[col], layer_ylt[inur_1_include].sum(axis = 1)) * layer_ylt["inur_1_recovery"] if col in inur_1_include else 0)
                        - (utils.ratio(layer_ylt[col], layer_ylt[inur_2_include].sum(axis = 1)) * layer_ylt["inur_2_recovery"] if col in inur_2_include else 0)
                        - (utils.ratio(layer_ylt[col], layer_ylt[inur_3_include].sum(axis = 1)) * layer_ylt["inur_3_recovery"] if col in inur_3_include else 0)
                        - (utils.ratio(layer_ylt[col], layer_ylt[inur_4_include].sum(axis = 1)) * layer_ylt["inur_4_recovery"] if col in inur_4_include else 0)
                    )

                ### D) Calculte net of qualifying (subject loss)
                layer_ylt["subject_beazley_layers"] = 0
                qualifying_limit_table = qualifying_limit[table_include]
                qualifying_excess_table = qualifying_excess[table_include]

                for qual_lim, qual_ex, col in zip(qualifying_limit_table, qualifying_excess_table, layer_include):

                    if qual_lim == 0 and qual_ex == 0:
                        layer_ylt["subject_temp"] = layer_ylt[col]
                    else: 
                        layer_ylt["subject_temp"] = layer_loss(layer_ylt.loc[:, ["YEAR", col]],
                                                               limit = qual_lim,
                                                               excess = qual_ex,
                                                               no_reins = 999,
                                                               aad = 0,
                                                               ded_type = "Conventional")

                    layer_ylt["subject_beazley_layers"] += layer_ylt["subject_temp"]

                kpi_subject = kpi_calc(layer_ylt, "subject_beazley_layers", no_sims, attr_losses)
                layer.simulation.sim_result.subject_loss = kpi_subject["el"]


                ## 5) Calc Gross (of RI / RI Prem) losses ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                if use_agg_qs_method:
                    
                    year_agg_ylt_temp = layer_ylt.groupby(["YEAR"], as_index = False)["subject_beazley_layers"].sum()

                    year_agg_ylt = pd.DataFrame(data = {"YEAR": range(1, no_sims + 1)})
                    year_agg_ylt = pd.merge(year_agg_ylt, year_agg_ylt_temp, on="YEAR", how="left")
                    year_agg_ylt["subject_beazley_layers"] = year_agg_ylt["subject_beazley_layers"].fillna(0)

                    year_agg_ylt["subject_beazley_layers"] += attr_losses

                    # calculate losses to agg. aggs don't reinstate
                    year_agg_ylt["temp_gross_layer"] = layer_loss(year_agg_ylt.loc[:, ["YEAR", "subject_beazley_layers"]],
                                                                  limit = limit[index],
                                                                  excess = excess[index],
                                                                  no_reins = 0,
                                                                  aad = 0,
                                                                  ded_type = inner_type[index])

                    kpi = kpi_calc(year_agg_ylt, "temp_gross_layer", no_sims)

                    ## write back to hxd
                    layer.simulation.sim_result.gross_el = kpi["el"]
                    layer.simulation.sim_result.gross_sd = kpi["sd"]
                else:
                    layer_ylt["temp_gross_layer"] = layer_loss(layer_ylt.loc[:, ["YEAR", "subject_beazley_layers"]],
                                                               limit = limit[index],
                                                               excess = excess[index],
                                                               no_reins = 999,
                                                               aad = 0,
                                                               ded_type = inner_type[index])

                    kpi = kpi_calc(layer_ylt, "temp_gross_layer", no_sims)

                    ## write back to hxd
                    layer.simulation.sim_result.gross_el = kpi["el"]
                    layer.simulation.sim_result.gross_sd = kpi["sd"]

                    ##~~ add pre inuring losses
                    layer_ylt["temp_pre_inur_layer"] = layer_loss(layer_ylt.loc[:, ["YEAR", "pre_inur_beazley_layers"]],
                                                                  limit = limit[index],
                                                                  excess = excess[index],
                                                                  no_reins = 999,
                                                                  aad = 0,
                                                                  ded_type = inner_type[index])

                    kpi_pre_inur = kpi_calc(layer_ylt, "temp_pre_inur_layer", no_sims)

                    ## write back to hxd
                    layer.simulation.sim_result.gross_el_pre_inur = kpi_pre_inur["el"]
                    layer.simulation.sim_result.gross_sd_pre_inur = kpi_pre_inur["sd"]
                    ##~~


                    ## table-layer losses
                    peril_layer_df = layer_ylt.loc[:, ["YEAR", "temp_gross_layer", "subject_beazley_layers"] + layer_include]

                    for table in layer_include:
                        peril_layer_df[f"gross_table_{table}"] = peril_layer_df["temp_gross_layer"] * utils.ratio(peril_layer_df[table], peril_layer_df["subject_beazley_layers"])

                    to_write_perc = {
                        f"gross_table_{i}": utils.ratio(kpi_calc(peril_layer_df, f"gross_table_{i}", no_sims)["el"], kpi["el"])
                        if f"gross_table_{i}" in peril_layer_df.columns 
                        else 0
                        for i in range(8)
                    }

                    to_write_dollar_el = {
                        f"gross_table_{i}": kpi_calc(peril_layer_df, f"gross_table_{i}", no_sims)["el"]
                        if f"gross_table_{i}" in peril_layer_df.columns 
                        else 0
                        for i in range(8)
                    }

                    to_write_dollar_std = {
                        f"gross_table_{i}": kpi_calc(peril_layer_df, f"gross_table_{i}", no_sims)["sd"]
                        if f"gross_table_{i}" in peril_layer_df.columns 
                        else 0
                        for i in range(8)
                    }

                    layer.peril_allocation.simulation_perc = to_write_perc
                    layer.peril_allocation.simulation_dollar = to_write_dollar_el
                    layer.peril_allocation.simulation_std_dollar = to_write_dollar_std

                    layer_ylt = layer_ylt.rename(columns = {"temp_gross_layer": f"beazley_loss_layer_{index + 1}"})

                    ## 6) Calc Net (of RI / RI Prem) losses ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    layer_ylt["temp_net_layer_excl_reins_prem"] = layer_loss(layer_ylt.loc[:, ["YEAR", "subject_beazley_layers"]],
                                                                             limit = limit[index],
                                                                             excess = excess[index],
                                                                             no_reins = number_reins[index],
                                                                             aad = aad[index],
                                                                             ded_type = inner_type[index])

                    reins_perc_list = [perc_reins_1[index], perc_reins_2[index], perc_reins_3[index]]
                    reins_perc_list = reins_perc_list[:number_reins[index]]

                    net_el = reins_calc(df = layer_ylt,
                                        loss_column = "temp_net_layer_excl_reins_prem",
                                        limit = limit[index],
                                        no_reins = number_reins[index],
                                        reins_perc = reins_perc_list,
                                        sims = no_sims)

                    net_sd = utils.ratio(kpi["sd"] * net_el, kpi["el"])
                    layer.simulation.sim_result.net_el = net_el
                    layer.simulation.sim_result.net_sd = net_sd
                    
                del layer_include

        ## 7) Calculate PML for simulation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        rp_array = np.array(hx.params.table_return_periods["return_period"])
        rp_array = np.sort(rp_array)[::-1]

        ## 7.1) Individual Curves
        for table, col in enumerate(columns_in_scope):
            table_kpi = kpi_calc(final_ylt, col, no_sims)
            cds.simulation.file_list[table].aal = table_kpi["el"]

            # aep
            aep_gross = generate_oep(final_ylt, col, no_sims, rp_array, "AEP", attr_losses)
            aep_gross_output = {
                "rp_2": aep_gross["loss"][11],
                "rp_5": aep_gross["loss"][10],
                "rp_10": aep_gross["loss"][9],
                "rp_25": aep_gross["loss"][8],
                "rp_50": aep_gross["loss"][7],
                "rp_100": aep_gross["loss"][6],
                "rp_200": aep_gross["loss"][5],
                "rp_250": aep_gross["loss"][4],
                "rp_500": aep_gross["loss"][3],
                "rp_1000": aep_gross["loss"][2],
                "rp_5000": aep_gross["loss"][1],
                "rp_10000": aep_gross["loss"][0]
            }
            cds.simulation.file_list[table].curve_aep = aep_gross_output

            # oep
            oep_gross = generate_oep(final_ylt, col, no_sims, rp_array)
            oep_gross_output = {
                "rp_2": oep_gross["loss"][11],
                "rp_5": oep_gross["loss"][10],
                "rp_10": oep_gross["loss"][9],
                "rp_25": oep_gross["loss"][8],
                "rp_50": oep_gross["loss"][7],
                "rp_100": oep_gross["loss"][6],
                "rp_200": oep_gross["loss"][5],
                "rp_250": oep_gross["loss"][4],
                "rp_500": oep_gross["loss"][3],
                "rp_1000": oep_gross["loss"][2],
                "rp_5000": oep_gross["loss"][1],
                "rp_10000": oep_gross["loss"][0]
            }
            cds.simulation.file_list[table].curve = oep_gross_output

        ## 7.2) Total Curve
        final_ylt["gross_loss"] = final_ylt[columns_in_scope].sum(axis = 1)

        final_ylt["subject_beazley_layers"] = ( 
                                        final_ylt["gross_loss"]
                                        - final_ylt["fhcf_1_recovery"] 
                                        - final_ylt["fhcf_2_recovery"]
                                        - final_ylt["inur_1_recovery"]
                                        - final_ylt["inur_2_recovery"]
                                        - final_ylt["inur_3_recovery"]
                                        - final_ylt["inur_4_recovery"]
                                        )

        gross_kpi = kpi_calc(final_ylt, "gross_loss", no_sims, attr_losses)
        net_inur_kpi = kpi_calc(final_ylt, "subject_beazley_layers", no_sims, attr_losses)        

        # aep
        total_curve_gross_aep = generate_oep(final_ylt, "gross_loss", no_sims, rp_array, "AEP", attr_losses)
        total_curve_net_inur_aep = generate_oep(final_ylt, "subject_beazley_layers", no_sims, rp_array, "AEP", attr_losses)

        total_curve_gross_output_aep = {
            "rp_2": total_curve_gross_aep["loss"][11],
            "rp_5": total_curve_gross_aep["loss"][10],
            "rp_10": total_curve_gross_aep["loss"][9],
            "rp_25": total_curve_gross_aep["loss"][8],
            "rp_50": total_curve_gross_aep["loss"][7],
            "rp_100": total_curve_gross_aep["loss"][6],
            "rp_200": total_curve_gross_aep["loss"][5],
            "rp_250": total_curve_gross_aep["loss"][4],
            "rp_500": total_curve_gross_aep["loss"][3],
            "rp_1000": total_curve_gross_aep["loss"][2],
            "rp_5000": total_curve_gross_aep["loss"][1],
            "rp_10000": total_curve_gross_aep["loss"][0],
            "aal": gross_kpi["el"]
        }

        total_curve_net_inur_output_aep = {
            "rp_2": total_curve_net_inur_aep["loss"][11],
            "rp_5": total_curve_net_inur_aep["loss"][10],
            "rp_10": total_curve_net_inur_aep["loss"][9],
            "rp_25": total_curve_net_inur_aep["loss"][8],
            "rp_50": total_curve_net_inur_aep["loss"][7],
            "rp_100": total_curve_net_inur_aep["loss"][6],
            "rp_200": total_curve_net_inur_aep["loss"][5],
            "rp_250": total_curve_net_inur_aep["loss"][4],
            "rp_500": total_curve_net_inur_aep["loss"][3],
            "rp_1000": total_curve_net_inur_aep["loss"][2],
            "rp_5000": total_curve_net_inur_aep["loss"][1],
            "rp_10000": total_curve_net_inur_aep["loss"][0],
            "aal": net_inur_kpi["el"]
        }

        cds.simulation.pml_comparison.simulation_gross_aep = total_curve_gross_output_aep
        cds.simulation.pml_comparison.simulation_net_inur_aep = total_curve_net_inur_output_aep

        # oep
        total_curve_gross = generate_oep(final_ylt, "gross_loss", no_sims, rp_array, "OEP")
        total_curve_net_inur = generate_oep(final_ylt, "subject_beazley_layers", no_sims, rp_array, "OEP")

        total_curve_gross_output = {
            "rp_2": total_curve_gross["loss"][11],
            "rp_5": total_curve_gross["loss"][10],
            "rp_10": total_curve_gross["loss"][9],
            "rp_25": total_curve_gross["loss"][8],
            "rp_50": total_curve_gross["loss"][7],
            "rp_100": total_curve_gross["loss"][6],
            "rp_200": total_curve_gross["loss"][5],
            "rp_250": total_curve_gross["loss"][4],
            "rp_500": total_curve_gross["loss"][3],
            "rp_1000": total_curve_gross["loss"][2],
            "rp_5000": total_curve_gross["loss"][1],
            "rp_10000": total_curve_gross["loss"][0],
            "aal": gross_kpi["el"]
        }

        total_curve_net_inur_output = {
            "rp_2": total_curve_net_inur["loss"][11],
            "rp_5": total_curve_net_inur["loss"][10],
            "rp_10": total_curve_net_inur["loss"][9],
            "rp_25": total_curve_net_inur["loss"][8],
            "rp_50": total_curve_net_inur["loss"][7],
            "rp_100": total_curve_net_inur["loss"][6],
            "rp_200": total_curve_net_inur["loss"][5],
            "rp_250": total_curve_net_inur["loss"][4],
            "rp_500": total_curve_net_inur["loss"][3],
            "rp_1000": total_curve_net_inur["loss"][2],
            "rp_5000": total_curve_net_inur["loss"][1],
            "rp_10000": total_curve_net_inur["loss"][0],
            "aal": net_inur_kpi["el"]
        }

        cds.simulation.pml_comparison.simulation_gross = total_curve_gross_output
        cds.simulation.pml_comparison.simulation_net_inur = total_curve_net_inur_output

        ## Map ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        other_event_state_map = other_event_state_map[["eventid", "state"]]
        other_event_state_map = other_event_state_map[~other_event_state_map["eventid"].isin(ws_event_state_map["eventid"])]

        final_ylt = final_ylt[["eventid","gross_loss"]]

        # split into ws_ylt and other_ylt (ws_ylt maps event -> state 1 to many; other_ylt only maps event -> state 1 to 1)
        ws_ylt = final_ylt[final_ylt["eventid"].isin(ws_event_state_map["eventid"])].copy()
        other_ylt = final_ylt[~final_ylt["eventid"].isin(ws_event_state_map["eventid"])].copy()

        # ws_ylt
        ws_ylt = pd.merge(ws_ylt, ws_event_state_map, how = "left")
        ws_ylt = pd.melt(ws_ylt, id_vars = ["eventid", "gross_loss"], var_name = "state", value_name = "perc")
        ws_ylt["aal"] = ws_ylt["gross_loss"] * ws_ylt["perc"]
        ws_ylt = ws_ylt[ws_ylt["aal"] > 0]
        ws_ylt = ws_ylt.groupby("state", as_index=False)["aal"].agg("sum")

        # other_ylt
        other_ylt = pd.merge(other_ylt, other_event_state_map, how = "left")
        other_ylt["state"] = other_ylt["state"].fillna("Other")
        other_ylt = other_ylt.groupby("state", as_index=False)["gross_loss"].sum()
        other_ylt = other_ylt.rename(columns = {"gross_loss": "aal"})

        # combine
        choropleth_data = pd.concat([ws_ylt, other_ylt], ignore_index=True)
        choropleth_data = choropleth_data.groupby("state", as_index=False)["aal"].agg("sum")

        # write total value
        cds.simulation.total.value = utils.ratio(choropleth_data["aal"].sum(), no_sims)

        choropleth_data["aal"] = utils.ratio(choropleth_data["aal"], no_sims)
        other_loss = choropleth_data[choropleth_data["state"] == "Other"]
        caribbean_loss = choropleth_data[choropleth_data["state"] == "Caribbean"]

        choropleth_data = choropleth_data[~choropleth_data["state"].isin(["Other", "Caribbean"])]
        choropleth_data = choropleth_data.sort_values(by = "aal", ascending=False)
        choropleth_data = choropleth_data.rename(columns = {"aal": "value"})

        # write mapped us states
        to_write = choropleth_data.to_dict(orient="records")       
        cds.simulation.choropleth_map = to_write

        # write caribbean
        cds.simulation.choropleth_caribbean.state = "Caribbean"
        if caribbean_loss["aal"].shape[0] > 0:
            cds.simulation.choropleth_caribbean.value = caribbean_loss["aal"].iloc[0]
        else:
            cds.simulation.choropleth_caribbean.value = 0

        # write all other
        cds.simulation.choropleth_other.state = "Other"
        if other_loss["aal"].shape[0] > 0:
            cds.simulation.choropleth_other.value = other_loss["aal"].iloc[0]
        else:
            cds.simulation.choropleth_other.value = 0
       
            
def file_formatter_read(hxd, progress):
    # set dataframe variables for cleaner code
    cds = hxd.cds  
    sim = cds.simulation

    # Load table
    file_node = sim.file_formatter.input_file

    if file_node.exists:
        with file_node.open(mode="b") as f:
            temp = pd.read_csv(f)

        col_names = temp.columns.to_list()

        for index, name in enumerate(col_names, start = 1):
            setattr(sim.file_formatter.file_column_names, f"column_{index}", name)


def file_formatter_write(hxd, progress):
    # set dataframe variables for cleaner code
    cds = hxd.cds  
    sim = cds.simulation

    # Load override column names
    override_cols = [None] * 9

    for index, _ in enumerate(override_cols):
        override_cols[index] = getattr(sim.file_formatter.override_column_names, f"column_{index + 1}")

    # Load table
    file_node = sim.file_formatter.input_file

    if file_node.exists:
        with file_node.open(mode="b") as f:
            temp = pd.read_csv(f)

        for index, override_name in enumerate(override_cols):
            if override_name is not None:
                temp.columns.values[index] = override_name

        with sim.file_formatter.output_file.open(mode="b") as f:
            temp.to_csv(f, index = False)


        


        

    