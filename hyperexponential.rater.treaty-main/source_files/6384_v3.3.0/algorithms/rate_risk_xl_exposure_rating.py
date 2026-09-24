import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, max_exposure_years, max_layers
from algorithms.udf import layer_loss, mbbefd_fls, mbbefd_expected_value
from hx import params as hx_params

from algorithms.timer import timer

curve_table = hx_params.table_risk_xl_curves

def rate_risk_xl_exposure_rating(hxd, common_data_dict):
        
    # set dataframe variables for cleaner code
    cds = hxd.cds
    exp = cds.risk_xl_exposure_rating
    layers = cds.layers

    if cds.programme == "Risk XL":

        limit_cnv = common_data_dict["limit_cnv"]
        excess_cnv = common_data_dict["excess_cnv"]
        aad_cnv = common_data_dict["aad_cnv"]
        number_reins = common_data_dict["number_reins"]
        perc_reins_1 = common_data_dict["perc_reins_1"]
        perc_reins_2 = common_data_dict["perc_reins_2"]
        perc_reins_3 = common_data_dict["perc_reins_3"]

        reins_perc = [[perc_reins_1[i], perc_reins_2[i], perc_reins_3[i]] for i in range(len(layers))]

        exposure_data = utils.pd_df_from_hx_list(exp.exposure_listing)

        exposure_data = exposure_data.drop(columns = ["swiss_re_c"])

        layer_columns_to_write = [f"loss_layer_{index}" for index, value in enumerate(layers, start = 1)]

        # 1) Dynamically label segments ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        ## set segment labels
        segment_labels = [getattr(getattr(exp, f"exposure_segment_{index}"), "segment_name") for index in range(1, 21)]
        ex_cat_ulr = [getattr(getattr(exp, f"exposure_segment_{index}"), "ex_cat_ulr") for index in range(1, 21)]
        curve_selection = [getattr(getattr(exp, f"exposure_segment_{index}"), "curve_selection") for index in range(1, 21)]

        segment_selections_df = pd.DataFrame({"segment": segment_labels, "ex_cat_ulr": ex_cat_ulr, "curve_selection": curve_selection})
        segment_selections_df = segment_selections_df.drop_duplicates(subset = "segment")

        segment_selections_df = pd.merge(segment_selections_df, curve_table, how = "left", left_on = "curve_selection", right_on = "curve_name")

        segment_labels_to_write = set(segment_labels)
        segment_labels_to_write = {item for item in segment_labels_to_write if item}

        if segment_labels_to_write:
            segment_labels_to_write = list(segment_labels_to_write)
            segment_options = [
                {"option": i}
                for i in segment_labels_to_write
            ]
            exp.segment_options = segment_options

        label_map = {v: i for i, v in enumerate(segment_labels, start = 1)}


        ## NOTE DAY 2 Shared & Layered Start ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        exposure_data["net_exposed_limit"] = exposure_data["tiv"]
        exposure_data["avg_cedant_participation"] = 1
        exposure_data["avg_attachment"] = 0
        ## NOTE DAY 2 Shared & Layered End ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
        # 2) Exposed Limit Totals ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        exposure_data_grouped = exposure_data.groupby(["segment"], as_index = False)[["net_exposed_limit"]].sum()
        exposure_data_grouped["segment_index"] = exposure_data_grouped["segment"].map(label_map)

        for index, i in enumerate(exposure_data_grouped["segment_index"]):
            if pd.notna(i):
                setattr(getattr(exp, f"exposure_segment_{int(i)}"), "exposed_limit_ty", exposure_data_grouped["net_exposed_limit"][index])

        for i in range(1, 21):
            setattr(
                getattr(exp, f"exposure_segment_{i}"),
                "exposed_limit_change",
                utils.ratio((getattr(exp, f"exposure_segment_{i}").exposed_limit_ty or 0) - (getattr(exp, f"exposure_segment_{i}").exposed_limit_ly or 0), getattr(exp, f"exposure_segment_{i}").exposed_limit_ly or 0)
            )

        total_exposure = exposure_data["net_exposed_limit"].sum()
        exp.exposure_segment_total.exposed_limit_ty = total_exposure

        setattr(
            exp.exposure_segment_total,
            "exposed_limit_change",
            utils.ratio((exp.exposure_segment_total.exposed_limit_ty or 0) - (exp.exposure_segment_total.exposed_limit_ly or 0), exp.exposure_segment_total.exposed_limit_ly or 0)
        )

        gnepi_adj_factor = utils.ratio(cds.epi_yoa, exposure_data["gnepi"].sum())
        cds.risk_xl_exposure_rating.gnepi_adj_factor = gnepi_adj_factor


        # 3) Exposure Data Calcs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        exposure_data = pd.merge(exposure_data, segment_selections_df, how = "left", on = "segment")
        exposure_data = exposure_data.fillna(0)

        if cds.risk_xl_exposure_rating.gnepi_by_band == "Use Exposure":
            gnepi_exposure_fac = utils.ratio(cds.epi_yoa, total_exposure)
            exposure_data["gnepi"] = exposure_data["net_exposed_limit"] * gnepi_exposure_fac

        if not cds.risk_xl_exposure_rating.gnepi_exposure_adjustment:
            gnepi_adj_factor = 1

        exposure_data["location_count_adj"] = exposure_data["location_count"] * gnepi_adj_factor
        exposure_data["gnepi_adj"] = exposure_data["gnepi"] * gnepi_adj_factor
        exposure_data["tiv_adj"] = exposure_data["tiv"] * gnepi_adj_factor
        exposure_data["net_exposed_limit_adj"] = exposure_data["net_exposed_limit"] * gnepi_adj_factor


        exposure_data["avg_tiv"] = utils.ratio(exposure_data["tiv_adj"], exposure_data["location_count_adj"])
        exposure_data["avg_lel"] = utils.ratio(exposure_data["net_exposed_limit_adj"], exposure_data["location_count_adj"])
        exposure_data["avg_100_pol_limit"] = utils.ratio(exposure_data["avg_lel"], exposure_data["avg_cedant_participation"])

        exposure_data["swiss_re_c_override"] = exposure_data["swiss_re_c_override"].astype("string")
        exposure_data = pd.merge(exposure_data, curve_table, how = "left", left_on = "swiss_re_c_override", right_on = "curve_name", suffixes = ("", "_temp"))

        exposure_data["swiss_re_c"] = exposure_data["swiss_re_c_temp"].replace(0, np.nan).fillna(exposure_data["swiss_re_c"])

        exposure_data["b"] = np.exp(3.1 - 0.15 * (1 + exposure_data["swiss_re_c"]) * exposure_data["swiss_re_c"])
        exposure_data["g"] = np.exp((0.78 + 0.12 * exposure_data["swiss_re_c"]) * exposure_data["swiss_re_c"])

        exposure_data["entry_policy_dollar_100"] = exposure_data["avg_attachment"]
        exposure_data["exit_policy_dollar_100"] = exposure_data["avg_attachment"] + exposure_data["avg_100_pol_limit"]

        exposure_data["entry_policy_perc"] = utils.ratio(exposure_data["entry_policy_dollar_100"], exposure_data["avg_tiv"])
        exposure_data["exit_policy_perc"] = utils.ratio(exposure_data["exit_policy_dollar_100"], exposure_data["avg_tiv"])

        exposure_data["entry_policy_fls"] = mbbefd_fls(exposure_data["b"],
                                                    exposure_data["g"],
                                                    exposure_data["entry_policy_perc"])

        exposure_data["exit_policy_fls"] = mbbefd_fls(exposure_data["b"],
                                                    exposure_data["g"],
                                                    exposure_data["exit_policy_perc"])


        exposure_data["ex_cat_ulr_readonly"] = exposure_data["ex_cat_ulr"]  

        exposure_data["gross_el"] = exposure_data["gnepi_adj"] * np.where(exposure_data["ex_cat_ulr_override"] == 0, exposure_data["ex_cat_ulr_readonly"], exposure_data["ex_cat_ulr_override"])

        exposure_data["avg_policy_worth"] = exposure_data["exit_policy_fls"] - exposure_data["entry_policy_fls"]
        exposure_data["gu_el"] = utils.ratio(exposure_data["gross_el"], exposure_data["avg_policy_worth"])

        exposure_data["expected_severity_perc"] = mbbefd_expected_value(exposure_data["b"],
                                                                        exposure_data["g"])

        exposure_data["expected_severity"] = exposure_data["avg_tiv"] * exposure_data["expected_severity_perc"]
        exposure_data["expected_frequency"] = utils.ratio(exposure_data["gu_el"], exposure_data["expected_severity"])

        ## layer losses
        for index, layer in enumerate(layers):
            exposure_data["layer_entry"] = np.minimum(excess_cnv[index], exposure_data["avg_lel"])
            exposure_data["layer_exit"] = np.minimum(excess_cnv[index] + limit_cnv[index], exposure_data["avg_lel"])

            exposure_data["entry_layer_dollar_100"] = exposure_data["layer_entry"] / exposure_data["avg_cedant_participation"] + exposure_data["avg_attachment"]
            exposure_data["exit_layer_dollar_100"] = np.minimum(exposure_data["exit_policy_dollar_100"],
                                                                exposure_data["avg_attachment"] + (excess_cnv[index] + limit_cnv[index]) / exposure_data["avg_cedant_participation"]) 
        
            exposure_data["entry_layer_perc"] = exposure_data["entry_layer_dollar_100"] / exposure_data["avg_tiv"]
            exposure_data["exit_layer_perc"] = exposure_data["exit_layer_dollar_100"] / exposure_data["avg_tiv"]

            exposure_data["entry_layer_fls"] = mbbefd_fls(exposure_data["b"],
                                                        exposure_data["g"],
                                                        exposure_data["entry_layer_perc"])

            exposure_data["exit_layer_fls"] = mbbefd_fls(exposure_data["b"],
                                                        exposure_data["g"],
                                                        exposure_data["exit_layer_perc"])

            exposure_data[f"loss_layer_{index + 1}"] = exposure_data["gu_el"] * (exposure_data["exit_layer_fls"] - exposure_data["entry_layer_fls"])

            ## Exposure to layer for ROEV calc
            exposure_data["layer_exposure"] = np.minimum(np.maximum(exposure_data["avg_lel"] - excess_cnv[index], 0), limit_cnv[index]) * exposure_data["location_count_adj"]
            layer_exposure = exposure_data["layer_exposure"].sum()
            layer.quote.rol_ty.layer_exposure = layer_exposure

        exposure_data = exposure_data.fillna(0)
        utils.write_pd_to_hxd(exposure_data, exp.exposure_listing, ["location_count_adj", "gnepi_adj", "tiv_adj", "net_exposed_limit_adj", "avg_tiv", "avg_lel", "avg_100_pol_limit", "gross_el", "avg_policy_worth", "ex_cat_ulr_readonly", "gu_el", "expected_severity_perc", "expected_severity", "expected_frequency", "swiss_re_c"] + layer_columns_to_write)
        

        risk_exposure_gross_non_cat = [None] * len(layers)
        risk_exposure_gross_total = [None] * len(layers)
        risk_exposure_net_el = [None] * len(layers)

        for index, layer in enumerate(layers):

            attr_loss = exposure_data[f"loss_layer_{index + 1}"].sum()
            gross_total_el_deterministic = attr_loss + (layer.model.rms.gross_el or 0)

            layer.risk_xl_exposure_rating.gross_non_cat_el_deterministic = attr_loss
            layer.risk_xl_exposure_rating.gross_total_el_deterministic = gross_total_el_deterministic

            net_el_excl_reins_prem = gross_total_el_deterministic * (layer.risk_xl_exposure_rating.model_limit_factor or 0)

            layer.risk_xl_exposure_rating.net_el_excl_reins_prem = net_el_excl_reins_prem

            net_el = utils.ratio(net_el_excl_reins_prem, 1 + (layer.risk_xl_exposure_rating.no_expected_reins or 0))

            layer.risk_xl_exposure_rating.net_el = net_el

            setattr(exp, f"show_loss_layer_{index + 1}", True)

            risk_exposure_gross_non_cat[index] = attr_loss
            risk_exposure_gross_total[index] = gross_total_el_deterministic
            risk_exposure_net_el[index] = net_el


        common_data_dict["risk_exposure_gross_non_cat"] = risk_exposure_gross_non_cat
        common_data_dict["risk_exposure_gross_total"] = risk_exposure_gross_total

        common_data_dict["risk_exposure_net_el"] = risk_exposure_net_el