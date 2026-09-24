import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves, max_exposure_years, max_layers
from algorithms.udf import create_index, layer_loss, ccy_conversion, list_to_numpy, reins_calc, generate_oep, reins_calc_burn
from hx import params as hx_params

from algorithms.timer import timer


def rate_burn(hxd, common_data_dict):
        
    # set dataframe variables for cleaner code
    cds = hxd.cds
    coverage = cds.experience_rating.coverage
    exp = cds.experience_rating.exposure
    claims = cds.experience_rating.claims
    clm_other = cds.experience_rating.claims_other
    layers = cds.layers

    rms_gross_el = [layer.model.rms.gross_el for layer in layers]
    rms_gross_sd = [layer.model.rms.gross_sd for layer in layers]

    rms_gross_el = list_to_numpy(rms_gross_el, float)
    rms_gross_sd = list_to_numpy(rms_gross_sd, float)

    is_risk_xl = cds.programme == "Risk XL"

    # 1) Dynamically label segments ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.burn_ol_ccy_label = f"On-Levelled Loss {cds.currency}"

    for i in range(1, 4):
        exp_seg = getattr(exp, f"exposure_segment_{i}")
        if exp_seg.segment_name in ["", None]:

            ## exposure segments
            setattr(exp_seg, "exposure_label", f"Exposure {i}")
            setattr(exp_seg, "exposure_change_label", f"Exposure Change {i}")
            setattr(exp_seg, "exposure_index_label", f"Exposure Index {i}")
            setattr(exp_seg, "total_index_label", f"Total Index {i}")

            ## claim segments
            setattr(clm_other, f"loss_segment_label_{i}", f"Loss Segment {i}")

        else:
            ## exposure segments
            setattr(exp_seg, "exposure_label", exp_seg.segment_name + " Exposure")
            setattr(exp_seg, "exposure_change_label", exp_seg.segment_name + " Exposure Change")
            setattr(exp_seg, "exposure_index_label", exp_seg.segment_name + " Exposure Index")
            setattr(exp_seg, "total_index_label", exp_seg.segment_name + " Total Index")

            ## claim segments
            setattr(clm_other, f"loss_segment_label_{i}", exp_seg.segment_name + " Loss")
    
    ## set coverage labels
    coverage_labels = [getattr(coverage,f"coverage_{i}") for i in range(1,9)]
    coverage_labels_to_write = set(coverage_labels)
    coverage_labels_to_write = {item for item in coverage_labels_to_write if item}

    # 2) Load input values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #timer.start("load")

    application_ccy = common_data_dict["application_ccy"]
    burn_start_year = exp.burn_start_year
    exposure_start_year = exp.exposure_start_year
    yoa = hxd.hx_core.inception_date.year

    rc_allowance = [exp.gnepi_exposure_segment.allow_for_rc, 
                    exp.exposure_segment_1.allow_for_rc, 
                    exp.exposure_segment_2.allow_for_rc, 
                    exp.exposure_segment_3.allow_for_rc]
    
    other_allowance = [exp.gnepi_exposure_segment.allow_for_other_changes,
                        exp.exposure_segment_1.allow_for_other_changes,
                       exp.exposure_segment_2.allow_for_other_changes,
                       exp.exposure_segment_3.allow_for_other_changes]

    inflation_option = [exp.gnepi_exposure_segment.inflation_option,
                        exp.exposure_segment_1.inflation_option,
                        exp.exposure_segment_2.inflation_option,
                        exp.exposure_segment_3.inflation_option]

    exposure_columns_to_read = [
        "pif",
        "gnepi_actual",
        "gnepi_projected",
        "exposure_value_1",
        "exposure_value_2",
        "exposure_value_3",
        "rate_change",
        "inflation_option_1",
        "inflation_option_2",
        "other_changes"
    ]
    exposure_data = utils.pd_df_from_hx_list(exp.exposure_listing, exposure_columns_to_read)

    loss_layer_columns_to_read = [f"loss_layer_{i}" for i in range(1, max_layers) if i <= len(layers)]
    claims_columns_to_read = [
        "year",
        "currency",
        "description",
        "cat_non_cat",
        "cat_name",
        "coverage",
        "gnepi_loss",
        "loss_segment_1",
        "loss_segment_2",
        "loss_segment_3",
        "previous_year_total",
        "loss_type",
        "as_if_loss",
        "return_period",
        "comment"
    ]
    claims_data = utils.pd_df_from_hx_list(claims, claims_columns_to_read + loss_layer_columns_to_read)

    ## supercat validation
    if claims_data.loc[claims_data["loss_type"].isin(["SuperCat", "SuperCat As-If"]) & (claims_data["comment"] == "")].shape[0] > 0:
        hx.errors.validation("All SuperCat and SuperCat As-If claims must have a comment entered.")

    ##
    inner_type = [layer.inner_type for layer in layers]
    inner_type = ["Conventional" if item is None else item for item in inner_type]

    selection = [layer.burn.burn_result.selection for layer in layers]

    limit_cnv = common_data_dict["limit_cnv"]
    excess_cnv = common_data_dict["excess_cnv"]
    aad_cnv = common_data_dict["aad_cnv"]
    number_reins = common_data_dict["number_reins"]
    perc_reins_1 = common_data_dict["perc_reins_1"]
    perc_reins_2 = common_data_dict["perc_reins_2"]
    perc_reins_3 = common_data_dict["perc_reins_3"]

    risk_xl_occurrence_limit_cnv = common_data_dict["risk_xl_occurrence_limit_cnv"]

    reins_perc = [[perc_reins_1[i], perc_reins_2[i], perc_reins_3[i]] for i in range(len(layers))]

    layer_columns_to_write = [f"loss_layer_{index}" for index, value in enumerate(layers, start = 1)]
    risk_gross_layer_columns_to_write = [f"gross_loss_layer_{index}" for index, value in enumerate(layers, start = 1)]

    selection = list_to_numpy(selection, str)

    #timer.end("load")

    # 3) Set show/hides and years ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    year_list = pd.Series(range(yoa - max_exposure_years + 1, yoa + 1))
    show_row = np.where(year_list < burn_start_year, False, True)
    show_row_exposure = np.where(year_list < exposure_start_year, False, True)

    exposure_data["year"] = year_list
    exposure_data["show_row_exposure"] = show_row_exposure

    # 4) Exposure indexation calcs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    exposure_data["gnepi_to_use"] = np.where((exposure_data["year"] < yoa) & (exposure_data["gnepi_actual"] > 0),
                                             exposure_data["gnepi_actual"],
                                             
                                             np.where(exposure_data["gnepi_projected"] > 0,
                                                exposure_data["gnepi_projected"],
                                                exposure_data["gnepi_actual"]))

    #timer.start("exposure_indexation")
    exposure_data["inflation_option_1"] = exposure_data["inflation_option_1"].fillna(0)
    exposure_data["inflation_option_2"] = exposure_data["inflation_option_2"].fillna(0)
    exposure_data["other_changes"] = exposure_data["other_changes"].fillna(0)
    exposure_data["rate_change"] = exposure_data["rate_change"].fillna(0)

    exposure_data["inflation_index_1"] = create_index(exposure_data["inflation_option_1"])
    exposure_data["inflation_index_2"] = create_index(exposure_data["inflation_option_2"])
    exposure_data["other_index"] = create_index(exposure_data["other_changes"])

    rc_definition = exp.rate_change_gross_net.rate_change
    exposure_data["rc_base_index"] = create_index(exposure_data["rate_change"])

    if rc_definition == "Inclusive of Inflation":
        exposure_data["rc_index_gnepi"] = exposure_data["rc_base_index"]
        exposure_data["rc_index_1"] = exposure_data["rc_base_index"]
        exposure_data["rc_index_2"] = exposure_data["rc_base_index"]
        exposure_data["rc_index_3"] = exposure_data["rc_base_index"]
    else:
        exposure_data["rc_index_gnepi"] = exposure_data["rc_base_index"] * (exposure_data["inflation_index_1"] if inflation_option[0] == 1 else exposure_data["inflation_index_2"])
        exposure_data["rc_index_1"] = exposure_data["rc_base_index"] * (exposure_data["inflation_index_1"] if inflation_option[1] == 1 else exposure_data["inflation_index_2"])
        exposure_data["rc_index_2"] = exposure_data["rc_base_index"] * (exposure_data["inflation_index_1"] if inflation_option[2] == 1 else exposure_data["inflation_index_2"])
        exposure_data["rc_index_3"] = exposure_data["rc_base_index"] * (exposure_data["inflation_index_1"] if inflation_option[3] == 1 else exposure_data["inflation_index_2"])

    exposure_data["gnepi_to_use"] = exposure_data["gnepi_to_use"] * exposure_data["rc_index_gnepi"] if rc_allowance[0] else exposure_data["gnepi_to_use"]
    exposure_data["exposure_value_1"] = exposure_data["exposure_value_1"] * exposure_data["rc_index_1"] if rc_allowance[1] else exposure_data["exposure_value_1"]
    exposure_data["exposure_value_2"] = exposure_data["exposure_value_2"] * exposure_data["rc_index_2"] if rc_allowance[2] else exposure_data["exposure_value_2"]
    exposure_data["exposure_value_3"] = exposure_data["exposure_value_3"] * exposure_data["rc_index_3"] if rc_allowance[3] else exposure_data["exposure_value_3"]

    exposure_data["gnepi_exposure_change"] = utils.ratio(exposure_data["gnepi_to_use"] - exposure_data["gnepi_to_use"].shift(1), exposure_data["gnepi_to_use"].shift(1), 0)
    exposure_data["exposure_change_1"] = utils.ratio(exposure_data["exposure_value_1"] - exposure_data["exposure_value_1"].shift(1), exposure_data["exposure_value_1"].shift(1), 0)
    exposure_data["exposure_change_2"] = utils.ratio(exposure_data["exposure_value_2"] - exposure_data["exposure_value_2"].shift(1), exposure_data["exposure_value_2"].shift(1), 0)
    exposure_data["exposure_change_3"] = utils.ratio(exposure_data["exposure_value_3"] - exposure_data["exposure_value_3"].shift(1), exposure_data["exposure_value_3"].shift(1), 0)

    exposure_data = exposure_data.fillna(0)

    exposure_data["gnepi_exposure_index"] = create_index(exposure_data["gnepi_exposure_change"])
    exposure_data["exposure_index_1"] = create_index(exposure_data["exposure_change_1"])
    exposure_data["exposure_index_2"] = create_index(exposure_data["exposure_change_2"])
    exposure_data["exposure_index_3"] = create_index(exposure_data["exposure_change_3"])

    exposure_data["gnepi_total_index"] = (exposure_data["gnepi_exposure_index"] * 
                                         (exposure_data["inflation_index_1"] if inflation_option[0] == 1 else exposure_data["inflation_index_2"]) * 
                                         (exposure_data["other_index"] if other_allowance[0] else 1) 
                                         )

    exposure_data["total_index_1"] = (exposure_data["exposure_index_1"] * 
                                     (exposure_data["inflation_index_1"] if inflation_option[1] == 1 else exposure_data["inflation_index_2"]) * 
                                     (exposure_data["other_index"] if other_allowance[1] else 1) 
                                     )

    exposure_data["total_index_2"] = (exposure_data["exposure_index_2"] * 
                                     (exposure_data["inflation_index_1"] if inflation_option[2] == 1 else exposure_data["inflation_index_2"]) * 
                                     (exposure_data["other_index"] if other_allowance[2] else 1) 
                                     )

    exposure_data["total_index_3"] = (exposure_data["exposure_index_3"] * 
                                     (exposure_data["inflation_index_1"] if inflation_option[3] == 1 else exposure_data["inflation_index_2"]) * 
                                     (exposure_data["other_index"] if other_allowance[3] else 1) 
                                     )

    if is_risk_xl:
        exposure_data["risk_frequency_index"] = np.where(exposure_data["pif"].sum() > 0, create_index(exposure_data["pif"]), exposure_data["gnepi_exposure_index"])
        exposure_data["risk_avg_exposure_index"] = utils.ratio(exposure_data["gnepi_exposure_index"], exposure_data["risk_frequency_index"])
        exposure_data["risk_inflation_index"] = exposure_data["inflation_index_1"]
        exposure_data["risk_severity_index"] = exposure_data["risk_avg_exposure_index"] * exposure_data["risk_inflation_index"]
    else:
        exposure_data["risk_frequency_index"] = 0
        exposure_data["risk_avg_exposure_index"] = 0
        exposure_data["risk_inflation_index"] = 0
        exposure_data["risk_severity_index"] = 0



    exposure_columns_to_write = [
        "year",
        "show_row_exposure",

        "gnepi_exposure_change",
        "exposure_change_1",
        "exposure_change_2",
        "exposure_change_3",

        "gnepi_exposure_index",
        "exposure_index_1",
        "exposure_index_2",
        "exposure_index_3",

        "gnepi_total_index",
        "total_index_1",
        "total_index_2",
        "total_index_3",

        "risk_frequency_index",
        "risk_avg_exposure_index", 
        "risk_inflation_index", 
        "risk_severity_index"   
    ]    

    ## get epi for yoa to use in summary
    cds.epi_yoa = exposure_data.loc[exposure_data["year"] == yoa, "gnepi_to_use"].iloc[0]
    cds.exposure.aggregate.perc_change.prem_change = exposure_data.loc[exposure_data["year"] == yoa - 1, "gnepi_exposure_index"].iloc[0]

    #timer.end("exposure_indexation")

    # 5) Claim indexation calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #timer.start("claim_indexation")

    index_df = exposure_data.copy()
    index_df = index_df.loc[:, ["year", "gnepi_total_index", "total_index_1", "total_index_2", "total_index_3", "risk_frequency_index", "risk_severity_index"]]
    ## year NAs get defaulted to 0, therefore filter out to ensure not merging on index year 0 to claims data year 0
    index_df = index_df[index_df["year"] > 0]

    claims_data = claims_data.fillna(0)
    claims_data["year"] = claims_data["year"].astype(int)
    claims_data = pd.merge(claims_data, index_df, how = "left", on = "year")
    claims_data = claims_data.fillna(0)
    
    claims_data["this_year_total"] = claims_data["gnepi_loss"] + claims_data["loss_segment_1"] + claims_data["loss_segment_2"] + claims_data["loss_segment_3"]
    claims_data["exchange_rate_multiplicative"] = ccy_conversion(claims_data["currency"].astype(str), application_ccy, hx_params.table_currency)
    claims_data["this_year_total"] = claims_data["this_year_total"] * claims_data["exchange_rate_multiplicative"]
    claims_data["movement"] = claims_data["this_year_total"] - claims_data["previous_year_total"]

    if is_risk_xl:
        claims_data["on_levelled_loss"] = np.where( (claims_data["loss_type"] == "Nominal") | (claims_data["loss_type"] == "SuperCat"),
                                                    claims_data["gnepi_loss"] * claims_data["risk_severity_index"],
                                                    claims_data["as_if_loss"])
    else:
        claims_data["on_levelled_loss"] = np.where( (claims_data["loss_type"] == "Nominal") | (claims_data["loss_type"] == "SuperCat"),
                                                    (np.array(claims_data[["gnepi_loss", "loss_segment_1", "loss_segment_2", "loss_segment_3"]])
                                                    * np.array(claims_data[["gnepi_total_index", "total_index_1", "total_index_2", "total_index_3"]])).sum(axis = 1),
                                                    (claims_data["as_if_loss"]))

    claims_data["on_levelled_loss"] *= claims_data["exchange_rate_multiplicative"]

    #timer.end("claim_indexation")
                                                            
    # 6) Layer loss calculations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #timer.start("layer_loss")
    calc_type = cds.experience_rating.claims_other.net_or_gross_reins_calc

    if calc_type == "Gross":
        cds.experience_rating.claims_other.show_gross_fields = True
        cds.experience_rating.claims_other.show_net_fields = False
    else:
        cds.experience_rating.claims_other.show_gross_fields = False
        cds.experience_rating.claims_other.show_net_fields = True

    if is_risk_xl:
        cds.experience_rating.claims_other.show_gross_fields = False
        cds.experience_rating.claims_other.show_net_fields = True

    el = [None] * len(layers)

    if is_risk_xl:
        for index, layer in enumerate(layers):
            coverage = [getattr(layer.burn.burn_coverage,f"coverage_{i}") for i in range(1,9)]
            coverage = np.where(coverage, coverage_labels, None)
            coverage = np.append(coverage, 0) # this ensures that if no coverage coding for loss it is included in layer calc

            claims_data["covered"] = np.where(np.isin(claims_data["coverage"], coverage), 1, 0)
            claims_data["loss_for_layer_calc"] = claims_data["on_levelled_loss"] * claims_data["covered"]

            # here we calculate subject losses to layer, i.e no allowance for AAD or reinstatements
            claims_data[f"gross_loss_layer_{index + 1}"] = layer_loss(claims_data.loc[:, ["year", "loss_for_layer_calc"]],
                                                                limit_cnv[index],
                                                                excess_cnv[index],
                                                                99,
                                                                ded_type = inner_type[index])

            # here we calculate subject losses to layer allowing for AAD and reinstatements
            claims_data[f"loss_layer_{index + 1}"] = layer_loss(claims_data.loc[:, ["year", "loss_for_layer_calc"]],
                                                                limit_cnv[index],
                                                                excess_cnv[index],
                                                                number_reins[index],
                                                                aad_cnv[index],
                                                                ded_type = inner_type[index])

    else:
        ## Gross
        if cds.experience_rating.claims_other.show_gross_fields:
            for index, layer in enumerate(layers):
                coverage = [getattr(layer.burn.burn_coverage,f"coverage_{i}") for i in range(1,9)]
                coverage = np.where(coverage, coverage_labels, None)
                coverage = np.append(coverage, 0) # this ensures that if no coverage coding for loss it is included in layer calc

                claims_data["covered"] = np.where(np.isin(claims_data["coverage"], coverage), 1, 0)
                claims_data["loss_for_layer_calc"] = claims_data["on_levelled_loss"] * claims_data["covered"]

                # here we calculate subject losses to layer, i.e no allowance for AAD or reinstatements
                claims_data[f"loss_layer_{index + 1}"] = layer_loss(claims_data.loc[:, ["year", "loss_for_layer_calc"]],
                                                                    limit_cnv[index],
                                                                    excess_cnv[index],
                                                                    99,
                                                                    ded_type = inner_type[index])
        ## Net
        else:
            for index, layer in enumerate(layers):
                coverage = [getattr(layer.burn.burn_coverage,f"coverage_{i}") for i in range(1,9)]
                coverage = np.where(coverage, coverage_labels, None)
                coverage = np.append(coverage, 0) # this ensures that if no coverage coding for loss it is included in layer calc

                claims_data["covered"] = np.where(np.isin(claims_data["coverage"], coverage), 1, 0)
                claims_data["loss_for_layer_calc"] = claims_data["on_levelled_loss"] * claims_data["covered"]

                # here we calculate subject losses to layer allowing for AAD and reinstatements
                claims_data[f"loss_layer_{index + 1}"] = layer_loss(claims_data.loc[:, ["year", "loss_for_layer_calc"]],
                                                                    limit_cnv[index],
                                                                    excess_cnv[index],
                                                                    number_reins[index],
                                                                    aad_cnv[index],
                                                                    ded_type = inner_type[index])



    claims_columns_to_write = ["this_year_total", "movement", "on_levelled_loss"]  
    all_columns_to_write = claims_columns_to_write + layer_columns_to_write

    #timer.end("layer_loss")

    # 7) Layer Loss Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #timer.start("layer_loss_summ")

    table_for_chart = claims_data[["year", "loss_type", "this_year_total"]].copy()
    table_for_chart = table_for_chart[table_for_chart['this_year_total'] > 0].groupby('year', as_index = False)['this_year_total'].agg({"non_zero_claim_count": "count", "nominal_loss": "sum"})

    latest_year = exposure_data["year"].max()

    if not is_risk_xl:
        burn_year_table_temp = claims_data[["year", "loss_type", "return_period", "on_levelled_loss"] + layer_columns_to_write].copy()
    else:
        burn_year_table_temp = claims_data[["year", "loss_type", "return_period", "on_levelled_loss", "cat_non_cat", "cat_name"] + risk_gross_layer_columns_to_write].copy()

        ## Group cat claims and apply occurrence limit start
        loss_cols = ["on_levelled_loss"] + risk_gross_layer_columns_to_write

        df_no = burn_year_table_temp[burn_year_table_temp["cat_non_cat"] == "Non-Cat"]

        df_yes_grouped = (
            burn_year_table_temp.loc[
                (burn_year_table_temp["cat_non_cat"] == "Cat") & (burn_year_table_temp["cat_name"] != 0)
            ]
            .groupby(["year", "cat_name"], as_index=False)
            .agg({col: "sum" for col in loss_cols})
        )

        df_yes_grouped[risk_gross_layer_columns_to_write] = np.minimum(df_yes_grouped[risk_gross_layer_columns_to_write], risk_xl_occurrence_limit_cnv)
        df_yes_grouped["cat_non_cat"] = "Cat"

        df_yes_unnamed = burn_year_table_temp.loc[
            (burn_year_table_temp["cat_non_cat"] == "Cat") & (burn_year_table_temp["cat_name"] == 0)
        ]

        burn_year_table_temp = pd.concat(
            [df_no, df_yes_grouped, df_yes_unnamed],
            ignore_index=True
        )
        # Group cat claims and apply occurrence limit end

        #### NOTE
        # apply freq adjustment to gross_layer unlimited free
        # net off AAD
        # cap at limited number of reinstatements
        # apply paid reinstatement factor

        ## apply aad and reinstatements
        burn_year_table_temp = burn_year_table_temp.sort_values("year")

        risk_burn_table = burn_year_table_temp[["year", "cat_non_cat"] + risk_gross_layer_columns_to_write].copy()

        burn_year_table_temp = burn_year_table_temp.groupby(["year"], as_index = False).sum()

        burn_year_table_temp = pd.merge(burn_year_table_temp, index_df[["year", "risk_frequency_index"]], how = "left", on = "year")

        for col in risk_gross_layer_columns_to_write:
            burn_year_table_temp[col] *= burn_year_table_temp["risk_frequency_index"]

        for index, _ in enumerate(layers):
            burn_year_table_temp[f"loss_layer_{index + 1}"] = np.minimum(limit_cnv[index] * (1 + number_reins[index]), np.maximum(0, burn_year_table_temp[f"gross_loss_layer_{index + 1}"] - aad_cnv[index]))

        burn_year_table_temp["loss_type"] = "temp"
        burn_year_table_temp["return_period"] = 0


        # need extra table for cat / non-cat split
        risk_burn_table = pd.merge(risk_burn_table, index_df[["year", "risk_frequency_index"]], how = "left", on = "year")

        for col in risk_gross_layer_columns_to_write:
            risk_burn_table[col] *= risk_burn_table["risk_frequency_index"]

        risk_burn_table = risk_burn_table.groupby(["year", "cat_non_cat"], as_index = False).sum()

        risk_non_cat_table = risk_burn_table.loc[(risk_burn_table["cat_non_cat"] == "Non-Cat")].reset_index()
        risk_cat_table = risk_burn_table.loc[(risk_burn_table["cat_non_cat"] != "Non-Cat")].reset_index()

        risk_non_cat_table = risk_non_cat_table[["year"] + risk_gross_layer_columns_to_write].copy()
        risk_non_cat_table = pd.merge(exposure_data[["year"]].copy(), risk_non_cat_table, on = "year", how = "left")
        risk_non_cat_table = risk_non_cat_table.fillna(0)

        risk_cat_table = risk_cat_table[["year"] + risk_gross_layer_columns_to_write].copy()
        risk_cat_table = pd.merge(exposure_data[["year"]].copy(), risk_cat_table, on = "year", how = "left")
        risk_cat_table = risk_cat_table.fillna(0)

        ## Non-Cat
        all_avg_risk_non_cat = risk_non_cat_table.loc[(risk_non_cat_table["year"] >= burn_start_year) &  (risk_non_cat_table["year"] <= latest_year - 1)]
        trailing_3_avg_risk_non_cat = all_avg_risk_non_cat.loc[(all_avg_risk_non_cat["year"] >= latest_year - 3)]
        trailing_5_avg_risk_non_cat = all_avg_risk_non_cat.loc[(all_avg_risk_non_cat["year"] >= latest_year - 5)]
        trailing_7_avg_risk_non_cat = all_avg_risk_non_cat.loc[(all_avg_risk_non_cat["year"] >= latest_year - 7)]

        ## Cat
        all_avg_risk_cat = risk_cat_table.loc[(risk_cat_table["year"] >= burn_start_year) &  (risk_cat_table["year"] <= latest_year - 1)]
        trailing_3_avg_risk_cat = all_avg_risk_cat.loc[(all_avg_risk_cat["year"] >= latest_year - 3)]
        trailing_5_avg_risk_cat = all_avg_risk_cat.loc[(all_avg_risk_cat["year"] >= latest_year - 5)]
        trailing_7_avg_risk_cat = all_avg_risk_cat.loc[(all_avg_risk_cat["year"] >= latest_year - 7)]



    super_cat_claims = burn_year_table_temp[burn_year_table_temp["loss_type"].isin(["SuperCat", "SuperCat As-If"])].copy()

    burn_year_table_temp = burn_year_table_temp[~burn_year_table_temp["loss_type"].isin(["SuperCat", "SuperCat As-If"])]

    burn_year_table_temp = burn_year_table_temp.groupby("year", as_index = False).agg("sum")
    
    burn_year_table = exposure_data[["year", "gnepi_to_use"]].copy()    
    burn_year_table = pd.merge(burn_year_table, burn_year_table_temp, on = "year", how = "left")
    burn_year_table = pd.merge(burn_year_table, table_for_chart, on = "year", how = "left")
    burn_year_table = burn_year_table.fillna(0)
    burn_year_table["freq_per_m_prem"] = utils.ratio(burn_year_table["non_zero_claim_count"], burn_year_table["gnepi_to_use"] / 1e6)
    burn_year_table["show_row"] = show_row

    burn_year_table["severity"] = utils.ratio(burn_year_table["on_levelled_loss"], burn_year_table["non_zero_claim_count"])

    # 8) Selection Summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if not super_cat_claims.empty:
        super_cat_claims["return_period"] = np.maximum(super_cat_claims["return_period"], 1)
        super_cat_claims = super_cat_claims[["return_period"] + layer_columns_to_write]
        super_cat_claims = super_cat_claims.reset_index()

        super_cat_claims = pd.melt(
            super_cat_claims,
            id_vars = ["index", "return_period"],
            value_vars=layer_columns_to_write,
            var_name="layer",
            value_name="loss"
        )
        
        super_cat_claims["prob"] = utils.ratio(1, super_cat_claims["return_period"])
        super_cat_claims["el"] = super_cat_claims["loss"] * super_cat_claims["prob"]
        super_cat_claims["el_2"] = (super_cat_claims["loss"]**2) * super_cat_claims["prob"]
        super_cat_claims["var"] = super_cat_claims["el_2"] - super_cat_claims["el"]**2

        super_cat_claims = super_cat_claims.groupby("layer").agg({"el": sum, "var": sum})

        super_cat_el = np.array(super_cat_claims["el"])
        super_cat_sd = np.array(np.sqrt(super_cat_claims["var"]))
    else:
        super_cat_el = np.zeros(len(layers))
        super_cat_sd = np.zeros(len(layers))


    avg_3_year_gross = [None] * len(layers)
    avg_5_year_gross = [None] * len(layers)
    avg_7_year_gross = [None] * len(layers)
    avg_all_year_gross = [None] * len(layers)

    sd_3_year_gross = [None] * len(layers)
    sd_5_year_gross = [None] * len(layers)
    sd_7_year_gross = [None] * len(layers)
    sd_all_year_gross = [None] * len(layers)

    avg_3_year_net = [None] * len(layers)
    avg_5_year_net = [None] * len(layers)
    avg_7_year_net = [None] * len(layers)
    avg_all_year_net = [None] * len(layers)

    sd_3_year_net = [None] * len(layers)
    sd_5_year_net = [None] * len(layers)
    sd_7_year_net = [None] * len(layers)
    sd_all_year_net = [None] * len(layers)

    avg_3_year_gross_risk_non_cat = [None] * len(layers)
    avg_5_year_gross_risk_non_cat = [None] * len(layers)
    avg_7_year_gross_risk_non_cat = [None] * len(layers)
    avg_all_year_gross_risk_non_cat = [None] * len(layers)

    sd_3_year_gross_risk_non_cat = [None] * len(layers)
    sd_5_year_gross_risk_non_cat = [None] * len(layers)
    sd_7_year_gross_risk_non_cat = [None] * len(layers)
    sd_all_year_gross_risk_non_cat = [None] * len(layers)

    avg_3_year_gross_risk_cat = [None] * len(layers)
    avg_5_year_gross_risk_cat = [None] * len(layers)
    avg_7_year_gross_risk_cat = [None] * len(layers)
    avg_all_year_gross_risk_cat = [None] * len(layers)

    sd_3_year_gross_risk_cat = [None] * len(layers)
    sd_5_year_gross_risk_cat = [None] * len(layers)
    sd_7_year_gross_risk_cat = [None] * len(layers)
    sd_all_year_gross_risk_cat = [None] * len(layers)


    if not is_risk_xl:
        burn_year_table_for_calcs = burn_year_table[["year"] + layer_columns_to_write].copy()
    else:
        burn_year_table_for_calcs = burn_year_table[["year"] + layer_columns_to_write + risk_gross_layer_columns_to_write].copy()

    all_avg = burn_year_table_for_calcs.loc[(burn_year_table_for_calcs["year"] >= burn_start_year) &  (burn_year_table_for_calcs["year"] <= latest_year - 1)]
    trailing_3_avg = all_avg.loc[(all_avg["year"] >= latest_year - 3)]
    trailing_5_avg = all_avg.loc[(all_avg["year"] >= latest_year - 5)]
    trailing_7_avg = all_avg.loc[(all_avg["year"] >= latest_year - 7)]

    ## Gross    
    for index, layer in enumerate(layers):
        if not is_risk_xl:
            avg_3_year_gross[index] = trailing_3_avg.iloc[:, (index + 1)].mean()
            avg_5_year_gross[index] = trailing_5_avg.iloc[:, (index + 1)].mean()
            avg_7_year_gross[index] = trailing_7_avg.iloc[:, (index + 1)].mean()
            avg_all_year_gross[index] = all_avg.iloc[:, (index + 1)].mean()

            sd_3_year_gross[index] = trailing_3_avg.iloc[:, (index + 1)].std()
            sd_5_year_gross[index] = trailing_5_avg.iloc[:, (index + 1)].std()
            sd_7_year_gross[index] = trailing_7_avg.iloc[:, (index + 1)].std()
            sd_all_year_gross[index] = all_avg.iloc[:, (index + 1)].std()
        else:
            avg_3_year_gross[index] = trailing_3_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_5_year_gross[index] = trailing_5_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_7_year_gross[index] = trailing_7_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_all_year_gross[index] = all_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()

            sd_3_year_gross[index] = trailing_3_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_5_year_gross[index] = trailing_5_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_7_year_gross[index] = trailing_7_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_all_year_gross[index] = all_avg[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()


            ## Non-Cat
            avg_3_year_gross_risk_non_cat[index] = trailing_3_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_5_year_gross_risk_non_cat[index] = trailing_5_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_7_year_gross_risk_non_cat[index] = trailing_7_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_all_year_gross_risk_non_cat[index] = all_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()

            sd_3_year_gross_risk_non_cat[index] = trailing_3_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_5_year_gross_risk_non_cat[index] = trailing_5_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_7_year_gross_risk_non_cat[index] = trailing_7_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_all_year_gross_risk_non_cat[index] = all_avg_risk_non_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()

            avg_3_year_gross_risk_non_cat = list_to_numpy(avg_3_year_gross_risk_non_cat, float)
            avg_5_year_gross_risk_non_cat = list_to_numpy(avg_5_year_gross_risk_non_cat, float)
            avg_7_year_gross_risk_non_cat = list_to_numpy(avg_7_year_gross_risk_non_cat, float)
            avg_all_year_gross_risk_non_cat = list_to_numpy(avg_all_year_gross_risk_non_cat, float)

            sd_3_year_gross_risk_non_cat = list_to_numpy(sd_7_year_gross_risk_non_cat, float)
            sd_5_year_gross_risk_non_cat = list_to_numpy(sd_5_year_gross_risk_non_cat, float)
            sd_7_year_gross_risk_non_cat = list_to_numpy(sd_7_year_gross_risk_non_cat, float)
            sd_all_year_gross_risk_non_cat = list_to_numpy(sd_all_year_gross_risk_non_cat, float)

            risk_gross_non_cat_el = np.where(selection == "All Years", avg_all_year_gross_risk_non_cat,
                                        np.where(selection == "3 Year", avg_3_year_gross_risk_non_cat,
                                            np.where(selection == "5 Year", avg_5_year_gross_risk_non_cat,
                                                avg_7_year_gross)))

            risk_gross_non_cat_sd = np.where(selection == "All Years", sd_all_year_gross_risk_non_cat,
                                        np.where(selection == "3 Year", sd_3_year_gross_risk_non_cat,
                                            np.where(selection == "5 Year", sd_5_year_gross_risk_non_cat,
                                                sd_7_year_gross_risk_non_cat)))

            ## Cat
            avg_3_year_gross_risk_cat[index] = trailing_3_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_5_year_gross_risk_cat[index] = trailing_5_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_7_year_gross_risk_cat[index] = trailing_7_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()
            avg_all_year_gross_risk_cat[index] = all_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].mean()

            sd_3_year_gross_risk_cat[index] = trailing_3_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_5_year_gross_risk_cat[index] = trailing_5_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_7_year_gross_risk_cat[index] = trailing_7_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()
            sd_all_year_gross_risk_cat[index] = all_avg_risk_cat[["year"] + risk_gross_layer_columns_to_write].iloc[:, (index + 1)].std()

            avg_3_year_gross_risk_cat = list_to_numpy(avg_3_year_gross_risk_cat, float)
            avg_5_year_gross_risk_cat = list_to_numpy(avg_5_year_gross_risk_cat, float)
            avg_7_year_gross_risk_cat = list_to_numpy(avg_7_year_gross_risk_cat, float)
            avg_all_year_gross_risk_cat = list_to_numpy(avg_all_year_gross_risk_cat, float)

            sd_3_year_gross_risk_cat = list_to_numpy(sd_3_year_gross_risk_cat, float)
            sd_5_year_gross_risk_cat = list_to_numpy(sd_5_year_gross_risk_cat, float)
            sd_7_year_gross_risk_cat = list_to_numpy(sd_7_year_gross_risk_cat, float)
            sd_all_year_gross_risk_cat = list_to_numpy(sd_all_year_gross_risk_cat, float)

            risk_gross_cat_el = np.where(selection == "All Years", avg_all_year_gross_risk_cat,
                                    np.where(selection == "3 Year", avg_3_year_gross_risk_cat,
                                        np.where(selection == "5 Year", avg_5_year_gross_risk_cat,
                                            avg_7_year_gross_risk_cat)))

            risk_gross_cat_sd = np.where(selection == "All Years", sd_all_year_gross_risk_cat,
                                    np.where(selection == "3 Year", sd_3_year_gross_risk_cat,
                                        np.where(selection == "5 Year", sd_5_year_gross_risk_cat,
                                            sd_7_year_gross_risk_cat)))




    avg_3_year_gross = list_to_numpy(avg_3_year_gross, float)
    avg_5_year_gross = list_to_numpy(avg_5_year_gross, float)
    avg_7_year_gross = list_to_numpy(avg_7_year_gross, float)
    avg_all_year_gross = list_to_numpy(avg_all_year_gross, float)

    sd_3_year_gross = list_to_numpy(sd_3_year_gross, float)
    sd_5_year_gross = list_to_numpy(sd_5_year_gross, float)
    sd_7_year_gross = list_to_numpy(sd_7_year_gross, float)
    sd_all_year_gross = list_to_numpy(sd_all_year_gross, float)

    avg_3_year_gross += super_cat_el
    avg_5_year_gross += super_cat_el
    avg_7_year_gross += super_cat_el
    avg_all_year_gross += super_cat_el

    sd_3_year_gross = np.sqrt(sd_3_year_gross**2 + super_cat_sd**2)
    sd_5_year_gross = np.sqrt(sd_5_year_gross**2 + super_cat_sd**2)
    sd_7_year_gross = np.sqrt(sd_7_year_gross**2 + super_cat_sd**2)
    sd_all_year_gross = np.sqrt(sd_all_year_gross**2 + super_cat_sd**2)

    gross_burn_el = np.where(selection == "All Years", avg_all_year_gross,
                        np.where(selection == "3 Year", avg_3_year_gross,
                            np.where(selection == "5 Year", avg_5_year_gross,
                                avg_7_year_gross)))

    gross_burn_sd = np.where(selection == "All Years", sd_all_year_gross,
                        np.where(selection == "3 Year", sd_3_year_gross,
                            np.where(selection == "5 Year", sd_5_year_gross,
                                sd_7_year_gross)))

    gross_burn_lol = utils.ratio(gross_burn_el, limit_cnv)
    gross_burn_sd_rol = utils.ratio(gross_burn_sd, limit_cnv)

    common_data_dict["burn_gross_el"] = gross_burn_el
    common_data_dict["burn_gross_sd"] = gross_burn_sd
    ## Net
    if cds.experience_rating.claims_other.show_net_fields or is_risk_xl:
        for index, layer in enumerate(layers):
            temp = reins_calc_burn(trailing_3_avg,
                                    f"loss_layer_{index + 1}",
                                    limit_cnv[index],
                                    number_reins[index],
                                    reins_perc[index],
                                    super_cat_el[index],
                                    super_cat_sd[index])

            avg_3_year_net[index] = temp[0]
            sd_3_year_net[index] = temp[1]

            temp = reins_calc_burn(trailing_5_avg,
                                    f"loss_layer_{index + 1}",
                                    limit_cnv[index],
                                    number_reins[index],
                                    reins_perc[index],
                                    super_cat_el[index],
                                    super_cat_sd[index])

            avg_5_year_net[index] = temp[0]
            sd_5_year_net[index] = temp[1]

            temp = reins_calc_burn(trailing_7_avg,
                                    f"loss_layer_{index + 1}",
                                    limit_cnv[index],
                                    number_reins[index],
                                    reins_perc[index],
                                    super_cat_el[index],
                                    super_cat_sd[index])

            avg_7_year_net[index] = temp[0]
            sd_7_year_net[index] = temp[1]

            temp = reins_calc_burn(all_avg,
                                    f"loss_layer_{index + 1}",
                                    limit_cnv[index],
                                    number_reins[index],
                                    reins_perc[index],
                                    super_cat_el[index],
                                    super_cat_sd[index])

            avg_all_year_net[index] = temp[0]
            sd_all_year_net[index] = temp[1]

        avg_3_year_net = list_to_numpy(avg_3_year_net, float)
        avg_5_year_net = list_to_numpy(avg_5_year_net, float)
        avg_7_year_net = list_to_numpy(avg_7_year_net, float)
        avg_all_year_net = list_to_numpy(avg_all_year_net, float)

        sd_3_year_net = list_to_numpy(sd_3_year_net, float)
        sd_5_year_net = list_to_numpy(sd_5_year_net, float)
        sd_7_year_net = list_to_numpy(sd_7_year_net, float)
        sd_all_year_net = list_to_numpy(sd_all_year_net, float)

        net_burn_el = np.where(selection == "All Years", avg_all_year_net,
                            np.where(selection == "3 Year", avg_3_year_net,
                                np.where(selection == "5 Year", avg_5_year_net,
                                    avg_7_year_net)))

        net_burn_sd = np.where(selection == "All Years", sd_all_year_net,
                            np.where(selection == "3 Year", sd_3_year_net,
                                np.where(selection == "5 Year", sd_5_year_net,
                                    sd_7_year_net)))

        net_burn_lol = utils.ratio(net_burn_el, limit_cnv)
        net_burn_sd_rol = utils.ratio(net_burn_sd, limit_cnv)

        common_data_dict["burn_net_el"] = net_burn_el
        common_data_dict["burn_net_sd"] = net_burn_sd

    #timer.end("layer_loss_summ")

    # 9) 10 largest claims, last 8 premium years, burn curve ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    ten_largest = claims_data.loc[:, ["year", "description", "previous_year_total", "this_year_total", "on_levelled_loss"]]
    ten_largest = ten_largest.sort_values(by = "on_levelled_loss", ascending = False).head(10)

    last_eight_premium = exposure_data.loc[:, ["year", "gnepi_actual", "gnepi_projected"]]
    last_eight_premium = last_eight_premium.sort_values(by = "year", ascending = False).head(8).reset_index(drop = True)

    ## curve
    rp_array = np.array(hx.params.table_return_periods["return_period"])
    rp_array = np.sort(rp_array)[::-1]

    year_table = pd.DataFrame(data = {"year": range(burn_start_year, latest_year + 1)})

    burn_curve = claims_data.loc[:, ["year", "on_levelled_loss"]]
    burn_curve = burn_curve.loc[(burn_curve["year"] >= burn_start_year)]

    burn_curve = (burn_curve
        .groupby("year")
        .agg(loss = pd.NamedAgg("on_levelled_loss", "max"))
    )
    year_table = pd.merge(year_table, burn_curve, on = "year", how = "left").fillna(0)

    oep_curve = pd.DataFrame(data = {"rp": rp_array, "loss": np.quantile(year_table["loss"], 1 - 1 / rp_array)})

    curve_output = {
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

    # 10) Write back to hxd ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #timer.start("write_back")

    ## NOTE if risk XL then rename risk_gross columns
    if is_risk_xl:
        claims_data = claims_data.drop(columns = layer_columns_to_write)
        claims_data = claims_data.rename(columns = dict(zip(risk_gross_layer_columns_to_write, layer_columns_to_write)))

    cds.pml_curves.burn_curve.rp_loss = curve_output
    
    clm_other.ten_largest = ten_largest.to_dict(orient = "records")
    utils.write_pd_to_hxd(last_eight_premium, exp.last_eight, ["year", "gnepi_actual", "gnepi_projected"])

    utils.write_pd_to_hxd(exposure_data, exp.exposure_listing, exposure_columns_to_write)
    utils.write_pd_to_hxd(claims_data, claims, all_columns_to_write)
    utils.write_pd_to_hxd(burn_year_table, clm_other.burn_year_result, ["year", "show_row", "non_zero_claim_count", "severity", "freq_per_m_prem", "nominal_loss", "on_levelled_loss"] + layer_columns_to_write)

    if is_risk_xl:

        risk_xl_total_aad_reins_factor = utils.ratio(net_burn_el, gross_burn_el) 

        ## Gross
        if cds.experience_rating.claims_other.risk_xl_use_rms_cat:
            gross_burn_el = risk_gross_non_cat_el + rms_gross_el
            gross_burn_sd = np.sqrt(risk_gross_non_cat_sd**2 + rms_gross_sd**2)
    
        gross_burn_lol = utils.ratio(gross_burn_el, limit_cnv)
        gross_burn_sd_rol = utils.ratio(gross_burn_sd, limit_cnv)

        ## Net
        if cds.experience_rating.claims_other.risk_xl_use_rms_cat:
            net_burn_el = gross_burn_el * risk_xl_total_aad_reins_factor
            net_burn_sd = gross_burn_sd * risk_xl_total_aad_reins_factor

        net_burn_lol = utils.ratio(gross_burn_el, limit_cnv)
        net_burn_sd_rol = utils.ratio(gross_burn_sd, limit_cnv)

        common_data_dict["burn_net_el"] = net_burn_el
        common_data_dict["burn_net_sd"] = net_burn_sd

        common_data_dict["risk_burn_gross_non_cat"] = risk_gross_non_cat_el
        common_data_dict["risk_burn_gross_total"] = gross_burn_el

        for index, layer in enumerate(layers):
            layer.burn.burn_result.avg_3_year = avg_3_year_gross[index]
            layer.burn.burn_result.avg_5_year = avg_5_year_gross[index]
            layer.burn.burn_result.avg_7_year = avg_7_year_gross[index]
            layer.burn.burn_result.avg_all_year = avg_all_year_gross[index]

            layer.burn.burn_result.gross_burn_el = gross_burn_el[index]
            layer.burn.burn_result.gross_burn_sd = gross_burn_sd[index]
        
            layer.burn.burn_result.risk_xl_non_cat_burn_gross_el = risk_gross_non_cat_el[index]
            layer.burn.burn_result.risk_xl_cat_burn_gross_el = risk_gross_cat_el[index]

            layer.burn.burn_result.gross_burn_lol = gross_burn_lol[index]
            layer.burn.burn_result.gross_burn_sd_rol = gross_burn_sd_rol[index]


            layer.burn.burn_result.net_burn_el = net_burn_el[index]
            layer.burn.burn_result.net_burn_sd = net_burn_sd[index]

            layer.burn.burn_result.net_burn_lol = net_burn_lol[index]
            layer.burn.burn_result.net_burn_sd_rol = net_burn_sd_rol[index]


            setattr(clm_other, f"show_loss_layer_{index + 1}", True)

            layer.burn.burn_result.risk_xl_rms_gross_el = rms_gross_el[index]

    else:
        if cds.experience_rating.claims_other.show_gross_fields:
            for index, layer in enumerate(layers):
                layer.burn.burn_result.avg_3_year = avg_3_year_gross[index]
                layer.burn.burn_result.avg_5_year = avg_5_year_gross[index]
                layer.burn.burn_result.avg_7_year = avg_7_year_gross[index]
                layer.burn.burn_result.avg_all_year = avg_all_year_gross[index]

                layer.burn.burn_result.gross_burn_el = gross_burn_el[index]
                layer.burn.burn_result.gross_burn_sd = gross_burn_sd[index]

                layer.burn.burn_result.gross_burn_lol = gross_burn_lol[index]
                layer.burn.burn_result.gross_burn_sd_rol = gross_burn_sd_rol[index]

                setattr(clm_other, f"show_loss_layer_{index + 1}", True)
        else:
            for index, layer in enumerate(layers):
                layer.burn.burn_result.avg_3_year = avg_3_year_net[index]
                layer.burn.burn_result.avg_5_year = avg_5_year_net[index]
                layer.burn.burn_result.avg_7_year = avg_7_year_net[index]
                layer.burn.burn_result.avg_all_year = avg_all_year_net[index]

                layer.burn.burn_result.net_burn_el = net_burn_el[index]
                layer.burn.burn_result.net_burn_sd = net_burn_sd[index]

                layer.burn.burn_result.net_burn_lol = net_burn_lol[index]
                layer.burn.burn_result.net_burn_sd_rol = net_burn_sd_rol[index]

                setattr(clm_other, f"show_loss_layer_{index + 1}", True)


    if coverage_labels_to_write:
        coverage_labels_to_write = list(coverage_labels_to_write)
        coverage_options = [
            {"option": i}
            for i in coverage_labels_to_write
        ]
        clm_other.coverage_options = coverage_options
    
    #timer.end("write_back")

    #timer.print_all()
    #timer.reset()