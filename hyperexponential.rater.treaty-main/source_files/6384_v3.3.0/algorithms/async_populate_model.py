import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter, attrgetter
from algorithms.rate_constants import max_curves
from algorithms.timer import timer
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.offline_hxd.offline_hxd import rgetattr, rsetattr

from algorithms.udf import generate_ymlt, generate_oep, layer_loss, kpi_calc, query_bi_database

def populate_model(hxd,progress):

    ## set dataframe variables for cleaner code
    cds = hxd.cds

    policy_option_id = cds.populate_model.policy_option_id
    # policy_option_id = 1606022

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    policy_response = hx_renew.snapshots.get_snapshot(policy_option_id = policy_option_id, stream = False)

    if policy_response.status_code != 200:
        raise Exception(policy_response.json())

    populate_data = policy_response.json()["data"]

    # 1) Non-Layer Nodes

    ## /risk_information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for child in [
        "inception_date",
        "expiry_date"
    ]:
        setattr(hxd.hx_core, child, populate_data["hx_core"][child])


    for child in [
        "rating_methodology",
        "insured_name",
        "broker",
        "is_renewal"
    ]:
        setattr(cds.standard_fields, child, populate_data["cds"]["standard_fields"][child])


    for child in [
        "case_pricing_analysis_location",
        "deadline_date",
        "short_description",
        "underwriter_location",
        "discussed_london",
        "deal_status",
        "quotation",
        "quoted",
        "declinature_reason",
        "declinature_comments",
        "programme",
        "calc_type",
        "currency",
        "multi_year",
        "ceding_commission",
        "other_acq_costs",
        "includes_us_exposure",
        "territory",
        "adj_base",
        "territorial_focus_group",
        "market_share",
        # bermuda wipe
        # "broker_contact",
        "personal_commercial",
        "core_account",
        "met_client_last_12_months",
        "carrier_type",
        "hours_clause",
        "cyber_code",
        "sanctions_clause",
        "terrorism_code",
        "named_perils",
        "non_pd_bi",
        "com_disease",
        "am_best_rating",
        "application_comments"
    ]:
        setattr(cds, child, populate_data["cds"][child])

    for child in  [
        "treaty_basis"
    ]:
        try:
            setattr(cds, child, populate_data["cds"][child]) 
        except (KeyError, AttributeError, TypeError):
            continue 


    if not hx.meta.is_renewal:
        cds.layer_totals.limit_ly = populate_data["cds"]["layer_totals"]["limit_ly"]

    ## bermuda specific fields
    cds.technical_underwriter = populate_data["cds"]["standard_fields"]["underwriter"]
    cds.risk_carrier = "Bermuda"
    cds.brokerage = 0.1
    cds.tax = 0.01

    ## /pml_curves ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.pml_curves.comments = populate_data["cds"]["pml_curves"]["comments"]

    rms_length = len(populate_data["cds"]["pml_curves"]["rms_curves"])
    air_length = len(populate_data["cds"]["pml_curves"]["air_curves"])
    other_length = len(populate_data["cds"]["pml_curves"]["other_curves"])
    nmp_length = len(populate_data["cds"]["pml_curves"]["nmp_curves"])

    cds.pml_curves.rms_curves = [{}] * rms_length
    cds.pml_curves.air_curves = [{}] * air_length
    cds.pml_curves.other_curves = [{}] * other_length
    cds.pml_curves.nmp_curves = [{}] * nmp_length

    for curve_type in ["rms_curves", "air_curves", "other_curves", "nmp_curves"]:
        for index, curve in enumerate(getattr(cds.pml_curves, curve_type)):     
            for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
                rsetattr(curve, f"rp_loss.{rp}", populate_data["cds"]["pml_curves"][curve_type][index]["rp_loss"][rp])
                rsetattr(curve, f"rp_loss_prev.{rp}", populate_data["cds"]["pml_curves"][curve_type][index]["rp_loss_prev"][rp])
            
            for child in ["include_in_peril_alloc", "peril", "curve_description", "currency"]:
                setattr(curve, child, populate_data["cds"]["pml_curves"][curve_type][index][child])

    for curve_type in ["curve_aggregator", "burn_curve"]:    
        for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
            try:
                if curve_type == "curve_aggregator":
                    rsetattr(cds.pml_curves, f"{curve_type}.rp_loss.{rp}", populate_data["cds"]["pml_curves"][f"{curve_type}"]["rp_loss"][f"{rp}"])
                rsetattr(cds.pml_curves, f"{curve_type}.rp_loss_prev.{rp}", populate_data["cds"]["pml_curves"][f"{curve_type}"]["rp_loss_prev"][f"{rp}"])
            except (KeyError, AttributeError, TypeError):
                continue 

    ## /nmp ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    nmp_curve_number = populate_data["cds"]["non_modelled_perils_visual"]["curve_number"]

    cds.non_modelled_perils_visual.curve_number = nmp_curve_number

    for index in range(nmp_curve_number):
        for child in [
            "include_in_summary",
            "broker_pml",
            "peril",
            "description",
            "curve",
            "rp",
            "loss",
            "currency"
        ]:
            setattr(cds.non_modelled_perils[index].curve_selections, child, populate_data["cds"]["non_modelled_perils"][index]["curve_selections"][child])

        for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
            setattr(cds.non_modelled_perils[index].pml_broker, rp, populate_data["cds"]["non_modelled_perils"][index]["pml_broker"][rp])

    ## /model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for child in [
        "carolinas_ws",
        "miami_dade_ws",
        "gulf_ws",
        "ne_ws",
        "fl_pinnelas_ws",
        "la_eq",
        "nm_eq",
        "nm_stress_eq",
        "sf_eq"
    ]:
        setattr(cds.modelling_account_level.rds_gross_loss.this_year, child, populate_data["cds"]["modelling_account_level"]["rds_gross_loss"]["this_year"][child]) 

    if not hx.meta.is_renewal:
        for child in [
            "carolinas_ws",
            "miami_dade_ws",
            "gulf_ws",
            "ne_ws",
            "fl_pinnelas_ws",
            "la_eq",
            "nm_eq",
            "nm_stress_eq",
            "sf_eq"
        ]:
            setattr(cds.modelling_account_level.rds_gross_loss.previous_year, child, populate_data["cds"]["modelling_account_level"]["rds_gross_loss"]["previous_year"][child]) 

    for child in [
        "rms_ws_curve_selection",
        "rms_eq_curve_selection",
        "rms_scs_curve_selection",
        "rms_eu_ws_curve_selection",
        "rms_jp_eq_curve_selection",
        "rms_jp_ws_curve_selection",
        "rms_can_eq_curve_selection",
        "rms_caribbean_ws_curve_selection"
    ]:
        setattr(cds.modelling_account_level, child, populate_data["cds"]["modelling_account_level"][child]) 

    setattr(cds.modelling_account_level, "comments", populate_data["cds"]["modelling_account_level"]["comments"]) 
    setattr(cds.modelling_account_level, "ivor_nmp_selection", populate_data["cds"]["modelling_account_level"]["ivor_nmp_selection"]) 

    ## /aggregates ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    setattr(cds.exposure.aggregate, "exposure_measure", populate_data["cds"]["exposure"]["aggregate"]["exposure_measure"])
    setattr(cds.exposure.aggregate, "exposure_comments", populate_data["cds"]["exposure"]["aggregate"]["exposure_comments"])

    setattr(cds.exposure.aggregate.ly_aggregates, "bespoke_total", populate_data["cds"]["exposure"]["aggregate"]["ly_aggregates"]["bespoke_total"])
    setattr(cds.exposure.aggregate.ty_aggregates, "bespoke_total", populate_data["cds"]["exposure"]["aggregate"]["ty_aggregates"]["bespoke_total"])

    exposure_df = pd.DataFrame(populate_data["cds"]["exposure"]["granular"]["exposures"])
    exposure_df.loc[:, ["ly_aggregate", "ty_aggregate"]] = exposure_df.loc[:, ["ly_aggregate", "ty_aggregate"]].fillna(0)

    exposure_len = exposure_df.shape[0]
    cds.exposure.granular.exposures = [{}] * exposure_len

    utils.write_pd_to_hxd(exposure_df, cds.exposure.granular.exposures, ["peril", "description", "ly_aggregate", "ty_aggregate", "key_zone_selector"])

    for index, val in enumerate(cds.exposure.granular.exposures):
        val.address_dropdown = exposure_df["address_dropdown"].to_dict()[index]

    
    ## /experience rating ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ### exposure selections
    for field in ["coverage_1", "coverage_2", "coverage_3", "coverage_4", "coverage_5", "coverage_6", "coverage_7", "coverage_8"]:
        setattr(cds.experience_rating.coverage, field, populate_data["cds"]["experience_rating"]["coverage"][field])

    cds.experience_rating.exposure.comments = populate_data["cds"]["experience_rating"]["exposure"]["comments"]
    cds.experience_rating.exposure.exposure_start_year = populate_data["cds"]["experience_rating"]["exposure"]["exposure_start_year"]
    cds.experience_rating.exposure.burn_start_year = populate_data["cds"]["experience_rating"]["exposure"]["burn_start_year"]

    for field in ["gnepi_exposure_segment", "exposure_segment_1", "exposure_segment_2", "exposure_segment_3"]:
        for index, sub_field in enumerate(["segment_type", "segment_name", "allow_for_rc", "allow_for_other_changes", "inflation_option"]):
            if not((field == "gnepi_exposure_segment") & (index < 2)):
                setattr(getattr(cds.experience_rating.exposure, field), sub_field, populate_data["cds"]["experience_rating"]["exposure"][field][sub_field])

    ### exposure
    cds.experience_rating.exposure.rate_change_gross_net.rate_change = populate_data["cds"]["experience_rating"]["exposure"]["rate_change_gross_net"]["rate_change"]

    exposure_df = pd.DataFrame(populate_data["cds"]["experience_rating"]["exposure"]["exposure_listing"])
    exposure_df = exposure_df.fillna(0)

    utils.write_pd_to_hxd(exposure_df, cds.experience_rating.exposure.exposure_listing, ["gnepi_projected", "gnepi_actual", "exposure_value_1", "exposure_value_2", "exposure_value_3", "rate_change", "inflation_option_1", "inflation_option_2", "other_changes"])


    ### claims
    cds.experience_rating.claims_other.comments = populate_data["cds"]["experience_rating"]["claims_other"]["comments"]
    cds.experience_rating.claims_other.net_or_gross_reins_calc = populate_data["cds"]["experience_rating"]["claims_other"]["net_or_gross_reins_calc"]
    cds.experience_rating.claims_other.burn_output_comments = populate_data["cds"]["experience_rating"]["claims_other"]["burn_output_comments"]

    claims_df = pd.DataFrame(populate_data["cds"]["experience_rating"]["claims"])
    claims_df.loc[:, ["gnepi_loss", "loss_segment_1", "loss_segment_2", "loss_segment_3", "previous_year_total", "as_if_loss", "return_period"]] = claims_df.loc[:, ["gnepi_loss", "loss_segment_1", "loss_segment_2", "loss_segment_3", "previous_year_total", "as_if_loss", "return_period"]].fillna(0)

    claims_df = claims_df[claims_df["year"].notna()].copy()

    claims_len = claims_df.shape[0]

    if claims_len > 0:
        cds.experience_rating.claims = [{}] * claims_len
        utils.write_pd_to_hxd(claims_df, cds.experience_rating.claims, ["year", "currency", "description", "large_loss", "coverage", "gnepi_loss", "loss_segment_1", "loss_segment_2", "loss_segment_3", "previous_year_total", "loss_type", "as_if_loss", "return_period", "comment"])


    ## /curve_aggregator ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    curve_agg_len = len(populate_data["cds"]["curve_aggregator"]["pml_selections"])
    cds.curve_aggregator.pml_selections = [{}] * curve_agg_len

    for index, curve in enumerate(cds.curve_aggregator.pml_selections):
        for child in [
            "include_in_aggregator",
            "weight",
            "name"
        ]:
            setattr(curve, child, populate_data["cds"]["curve_aggregator"]["pml_selections"][index][child])

        for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
            setattr(curve.rp_loss, rp, populate_data["cds"]["curve_aggregator"]["pml_selections"][index]["rp_loss"][rp]) 

    for rp in ["rp_2", "rp_5", "rp_10", "rp_25", "rp_50", "rp_100", "rp_200", "rp_250", "rp_500", "rp_1000", "rp_5000", "rp_10000"]:
        setattr(cds.curve_aggregator.aggregator_output.rp_loss, rp, populate_data["cds"]["curve_aggregator"]["aggregator_output"]["rp_loss"][rp])  

    ## /quote ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    setattr(cds, "tp_comments", populate_data["cds"]["tp_comments"])

    if not hx.meta.is_renewal:
        cds.quote.rol_ly.ulr = populate_data["cds"]["quote"]["rol_ly"]["ulr"]
        cds.quote.rol_ly.tpi = populate_data["cds"]["quote"]["rol_ly"]["tpi"]
        cds.quote.rol_ly.bpi = populate_data["cds"]["quote"]["rol_ly"]["bpi"]
        cds.quote.rol_ly.roc = populate_data["cds"]["quote"]["rol_ly"]["roc"]

        cds.quote.rol_ly.quote_adequacy = populate_data["cds"]["quote"]["rol_ly"]["quote_adequacy"]
        cds.quote.rol_ly.fot_adequacy = populate_data["cds"]["quote"]["rol_ly"]["fot_adequacy"]


    ## /peril_allocation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for child in [
        "allocation_methodology",
        "include_ivor"
    ]:
        setattr(cds.peril_allocation_account_level, child, populate_data["cds"]["peril_allocation_account_level"][child])


    ## /rate_change ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    setattr(cds.rate_change, "comments", populate_data["cds"]["rate_change"]["comments"])


    ## /summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cds.currency_policy_financials = populate_data["cds"]["currency_policy_financials"]

    if not hx.meta.is_renewal:
        for child in [
            "line_written_summary_fx",
            "line_estimated_summary_fx",
            "line_signed_summary_fx",

            "epi_written_summary_fx",
            "epi_estimated_summary_fx",
            "epi_signed_summary_fx",

            "mi_250",
            "mi_250_prem_ratio",
            "mi_250_estimate_prem_ratio",
        ]:
            setattr(cds.summary.multi_year_summary_ly, child, populate_data["cds"]["summary"]["multi_year_summary_ly"][child])

        for child in [
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            setattr(cds.summary.ly, child, populate_data["cds"]["summary"]["ly"][child])

        for child in [
            "rol_quote",
            "rol_fot",
            "roc",
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            setattr(cds.summary.year_before_last, child, populate_data["cds"]["summary"]["year_before_last"][child])

        for child in [
            "rol_quote",
            "rol_fot",
            "roc",
            "risk_adjusted_rate_change",
            "bpi",
            "fot_adequacy",
            "rms_adequacy",
            "ulr",
            "epi_adj_rate",
            "prem_full_line",
            "mi_250_prem_ratio",
            "mi_10_prem_ratio"            
        ]:
            setattr(cds.summary.expiring_year, child, populate_data["cds"]["summary"]["expiring_year"][child])

    ## /rationale ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for child in [
        "knowledge_comments",
        "portfolio_comments",
        "basis_comments",
        "unusual_comments",
        "facts_comments"
    ]:
        setattr(cds.rationale, child, populate_data["cds"]["rationale"][child])


    ## /pre_bind ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(1, 8):
        setattr(cds.pre_bind.answer, f"q_{i}", populate_data["cds"]["pre_bind"]["answer"][f"q_{i}"])


    ## /post_bind ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    for i in range(1, 35):
        setattr(cds.post_bind.answer, f"q_{i}", populate_data["cds"]["post_bind"]["answer"][f"q_{i}"])
        setattr(cds.post_bind.comments, f"q_{i}", populate_data["cds"]["post_bind"]["comments"][f"q_{i}"])





    # 2) Layer Nodes
    target_len = len(populate_data["cds"]["layers"])

    ## keep from renewal before wiping
    existing_layers_len = len(cds.layers)
    nodes_to_keep = list(cds.layers)


    cds.layers = [{}] * target_len

    for index, layer in enumerate(cds.layers):

        ## /risk_information ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if hx.meta.is_renewal:
            ### nodes to keep
            if (index + 1) <= existing_layers_len:
                to_write = [
                    "section_reference",
                    "loss_affected",
                    "currency",
                    "leader",
                    "layer_description",
                    "limit",
                    "excess",
                    "limit_cnv",
                    "excess_cnv",
                    "inner_type",
                    "aggregate_deductible",
                    "aggregate_deductible_cnv",
                    "number_reins",
                    "perc_reins_1",
                    "perc_reins_2",
                    "perc_reins_3",
                    "layer_structure",
                    "effective_brokerage"
                ]
                for child in to_write:
                    setattr(layer, child + "_ly", getattr(nodes_to_keep[index], f"{child}_ly"))
        else:
                to_write = [
                    "section_reference",
                    "loss_affected",
                    "currency",
                    "leader",
                    "layer_description",
                    "limit",
                    "excess",
                    "limit_cnv",
                    "excess_cnv",
                    "inner_type",
                    "aggregate_deductible",
                    "aggregate_deductible_cnv",
                    "number_reins",
                    "perc_reins_1",
                    "perc_reins_2",
                    "perc_reins_3",
                    "layer_structure",
                    "effective_brokerage"
                ]
                for child in to_write:
                    setattr(layer, child + "_ly", populate_data["cds"]["layers"][index][child + "_ly"])
        

        ### new nodes
        for child in [
            "renewal_layer",
            "is_facility",
            # bermuda wipe
            # "section_reference",
            "loss_affected",
            "currency",
            "leader",
            "layer_description",
            "limit",
            "excess",
            "inner_type",
            "aggregate_deductible",
            "number_reins",
            "perc_reins_1",
            "perc_reins_2",
            "perc_reins_3"
        ]:
            setattr(layer, child, populate_data["cds"]["layers"][index][child])

        ## /nmp ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for i in range(1, max_curves+1):
            for j in ["gross_el", "loss_on_line", "gross_sd", "include_curve"]:
                rsetattr(layer, f"nmp.non_modelled_perils_{i}.{j}", populate_data["cds"]["layers"][index]["nmp"][f"non_modelled_perils_{i}"][j])

        layer.nmp.non_modelled_perils_total.gross_el_uw = populate_data["cds"]["layers"][index]["nmp"]["non_modelled_perils_total"]["gross_el_uw"]
        layer.nmp.non_modelled_perils_total.gross_sd_uw = populate_data["cds"]["layers"][index]["nmp"]["non_modelled_perils_total"]["gross_sd_uw"]

        ## /experience rating ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for child in [
            "coverage_1",
            "coverage_2",
            "coverage_3",
            "coverage_4",
            "coverage_5",
            "coverage_6",
            "coverage_7",
            "coverage_8"
        ]:
            setattr(layer.burn.burn_coverage, child, populate_data["cds"]["layers"][index]["burn"]["burn_coverage"][child])

        setattr(layer.burn.burn_result, "selection", populate_data["cds"]["layers"][index]["burn"]["burn_result"]["selection"])
         
        ## /model ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if hx.meta.is_renewal:
            ### nodes to keep
            if (index + 1) <= existing_layers_len:
                for model_type in ["total_rms_nmp", "total_ivor_nmp", "total_air_nmp", "rms", "ivor", "air", "nmp"]:
                    for child in ["gross_el", "gross_sd"]: 
                        rsetattr(layer, f"model_prev.{model_type}.{child}", getattr(getattr(nodes_to_keep[index].model_prev, model_type), child)) 

                for child in ["ws_el", "eq_el", "scs_el", "perc_us_el", "eu_ws_el", "jp_eq_el", "jp_ws_el", "can_eq_el", "caribbean_ws_el", "perc_us_el"]:
                    rsetattr(layer, f"model_prev.rms.{child}", getattr(nodes_to_keep[index].model_prev.rms, child)) 

                for child in ["gross_el_incl_rol", "gross_sd_incl_rol", "additional_rol", "description"]:
                    rsetattr(layer, f"model_prev.nmp.{child}", getattr(nodes_to_keep[index].model_prev.nmp, child))

                for child in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
                    rsetattr(layer, f"rms_regional_prev.{child}", getattr(nodes_to_keep[index].rms_regional_prev, child))

                for child in ["treaty_us", "treaty_group", "treaty_us_quake", "treaty_intl"]:
                    for rp in ["mi_250", "mi_10"]:
                        rsetattr(layer, f"marginal_impacts_prev.{child}.{rp}", getattr(getattr(nodes_to_keep[index].marginal_impacts_prev, child), rp))
        else:
                for model_type in ["total_rms_nmp", "total_ivor_nmp", "total_air_nmp", "rms", "ivor", "air", "nmp"]:
                    for child in ["gross_el", "gross_sd"]: 
                        rsetattr(layer, f"model_prev.{model_type}.{child}", populate_data["cds"]["layers"][index]["model_prev"][f"{model_type}"][child]) 

                for child in ["ws_el", "eq_el", "scs_el", "perc_us_el", "eu_ws_el", "jp_eq_el", "jp_ws_el", "can_eq_el", "caribbean_ws_el", "perc_us_el"]:
                    rsetattr(layer, f"model_prev.rms.{child}", populate_data["cds"]["layers"][index]["model_prev"]["rms"][f"{child}"]) 

                for child in ["gross_el_incl_rol", "gross_sd_incl_rol", "additional_rol", "description"]:
                    rsetattr(layer, f"model_prev.nmp.{child}", populate_data["cds"]["layers"][index]["model_prev"]["nmp"][f"{child}"])

                for child in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
                    rsetattr(layer, f"rms_regional_prev.{child}", populate_data["cds"]["layers"][index]["rms_regional_prev"][f"{child}"])

                for child in ["treaty_us", "treaty_group", "treaty_us_quake", "treaty_intl"]:
                    for rp in ["mi_250", "mi_10"]:
                        rsetattr(layer, f"marginal_impacts_prev.{child}.{rp}", populate_data["cds"]["layers"][index]["marginal_impacts_prev"][f"{child}"][rp])

        ### new nodes
        for model_type in ["rms", "ivor", "air"]:
            for child in ["gross_el", "gross_sd"]:
                rsetattr(layer, f"model.{model_type}.{child}", populate_data["cds"]["layers"][index]["model"][f"{model_type}"][f"{child}"])

        for child in ["ws_el", "eq_el", "scs_el", "perc_us_el", "eu_ws_el", "jp_eq_el", "jp_ws_el", "can_eq_el", "caribbean_ws_el", "perc_us_el"]:
            rsetattr(layer, f"model.rms.{child}", populate_data["cds"]["layers"][index]["model"]["rms"][f"{child}"]) 

        for child in ["additional_rol", "description"]:
            rsetattr(layer, f"model.nmp.{child}", populate_data["cds"]["layers"][index]["model"]["nmp"][f"{child}"])

        for child in ["north_east", "mid_atlantic", "carolinas", "fl_se", "fl_non_se", "al_miss", "louisiana", "tx_east", "tx_west", "cal_south", "cal_north", "pnw", "new_madrid", "hawaii", "mid_west_1", "mid_west_2", "second_event", "ca_wildfire"]:
            rsetattr(layer, f"rms_regional.{child}", populate_data["cds"]["layers"][index]["rms_regional"][f"{child}"])

        for child in ["treaty_us", "treaty_group", "treaty_us_quake", "treaty_intl"]:
            for rp in ["mi_250", "mi_10"]:
                rsetattr(layer, f"marginal_impacts.{child}.{rp}", populate_data["cds"]["layers"][index]["marginal_impacts"][f"{child}"][f"{rp}"])


        ## /peril_allocation ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for child in [
            "final_proportions",
            "rms_el_approx",
            "air_el_approx",
            "rms_aal",
            "air_aal",
            "ivor_aal"
        ]:
            for i in [
                "el_eq",
                "el_ws",
                "el_scs",
                "el_wf",
                "el_winter",
                "el_fl",
                "el_other"
            ]:
                setattr(getattr(layer.peril_allocation, child), i, populate_data["cds"]["layers"][index]["peril_allocation"][child][i])


        ## /rate_change ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for child in [
            "expiring_layer_to_use",
            "exposure_selection",
            "comments"
        ]:
            setattr(layer.rate_change, child, populate_data["cds"]["layers"][index]["rate_change"][child])

        setattr(layer.rate_change.exposure_change_fixed, "model_calculated", populate_data["cds"]["layers"][index]["rate_change"]["exposure_change_fixed"]["model_calculated"])
        setattr(layer.rate_change.exposure_change_fixed, "uw_selected", populate_data["cds"]["layers"][index]["rate_change"]["exposure_change_fixed"]["uw_selected"])

        setattr(layer.rate_change.limit_change_fixed, "model_calculated", populate_data["cds"]["layers"][index]["rate_change"]["limit_change_fixed"]["model_calculated"])
        setattr(layer.rate_change.limit_change_fixed, "uw_selected", populate_data["cds"]["layers"][index]["rate_change"]["limit_change_fixed"]["uw_selected"])

        setattr(layer.rate_change.other_change_fixed, "uw_selected", populate_data["cds"]["layers"][index]["rate_change"]["other_change_fixed"]["uw_selected"])

        setattr(layer.rate_change.terms_conditions_change_fixed, "uw_selected", populate_data["cds"]["layers"][index]["rate_change"]["terms_conditions_change_fixed"]["uw_selected"])


        ## /quote ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if hx.meta.is_renewal:
            ### nodes to keep
            if (index + 1) <= existing_layers_len:
                for child in [
                    "rol_rms",
                    "rol_ivor", 
                    "rol_air", 
                    "rol_burn",
                    "rol_burn_override",
                    "weighting_rms", 
                    "weighting_ivor", 
                    "weighting_air",
                    "weighting_burn",
                    "lol_rms", 
                    "lol_ivor", 
                    "lol_air",
                    "lol_burn",
                    "lol_weighted", 
                    "gross_lol_weighted", 
                    "rol_afb_tech",
                    "tpi",
                    "roc", 
                    "ulr",
                    "bpi",
                    "rol_quote",
                    "rol_fot",
                    "quote_fot_ratio", 
                    "prem_full_line", 
                    "quote_adequacy",
                    "fot_adequacy",
                    "rms_adequacy", 
                    "written_line", 
                    "estimated_signing",
                    "signed_line",
                    "epi_written",
                    "epi_estimated", 
                    "epi_signed", 
                    "rp_quote_break_even",
                    "rp_fot_break_even",
                    "rp_attach", 
                    "rp_exit", 
                    "rp_pml_selection",
                    "rp_attach_peak",
                    "rp_exit_peak", 
                    "rp_pml_selection_peak"
                ]:
                    rsetattr(layer,f"quote.rol_ly.{child}", getattr(nodes_to_keep[index].quote.rol_ly, child))
        else:
            for child in [
                "rol_rms",
                "rol_ivor", 
                "rol_air", 
                "rol_burn",
                "rol_burn_override",
                "weighting_rms", 
                "weighting_ivor", 
                "weighting_air",
                "weighting_burn",
                "lol_rms", 
                "lol_ivor", 
                "lol_air",
                "lol_burn",
                "lol_weighted", 
                "gross_lol_weighted", 
                "rol_afb_tech",
                "tpi",
                "roc", 
                "ulr",
                "bpi",
                "rol_quote",
                "rol_fot",
                "quote_fot_ratio", 
                "prem_full_line", 
                "quote_adequacy",
                "fot_adequacy",
                "rms_adequacy", 
                "written_line", 
                "estimated_signing",
                "signed_line",
                "epi_written",
                "epi_estimated", 
                "epi_signed", 
                "rp_quote_break_even",
                "rp_fot_break_even",
                "rp_attach", 
                "rp_exit", 
                "rp_pml_selection",
                "rp_attach_peak",
                "rp_exit_peak", 
                "rp_pml_selection_peak"
            ]:
                rsetattr(layer,f"quote.rol_ly.{child}", populate_data["cds"]["layers"][index]["quote"]["rol_ly"][child])


        ### new nodes
        for child in [
            "rol_burn_override",
            "weighting_rms", 
            "weighting_ivor", 
            "weighting_air",
            "weighting_burn",
            "rol_quote",
            "rol_fot",
            # wipe lines for bermuda risk
            # "written_line", 
            # "estimated_signing",
            # "signed_line",
            "rp_pml_selection",
            "rp_pml_selection_peak",

            "curve_agg_rp_attach",
            "curve_agg_rp_exit",
            "rms_ap_attach",
            "rms_ap_exit",
            "rms_eq_attach",
            "rms_eq_exit",
            "rms_ws_attach",
            "rms_ws_exit",
            "rms_scs_attach",
            "rms_scs_exit",
            "air_ap_attach",
            "air_ap_exit",
            "air_eq_attach",
            "air_eq_exit",
            "air_ws_attach",
            "air_ws_exit",
            "air_scs_attach",
            "air_scs_exit",
            "air_winter_attach",
            "air_winter_exit",
            "air_wf_attach",
            "air_wf_exit"
        ]:
            rsetattr(layer,f"quote.rol_ty.{child}", populate_data["cds"]["layers"][index]["quote"]["rol_ty"][f"{child}"])

        rsetattr(layer,f"quote.rms_tp_calc.override_limit_factor", populate_data["cds"]["layers"][index]["quote"]["rms_tp_calc"]["override_limit_factor"])


        ## /summary ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        if hx.meta.is_renewal:
        ### nodes to keep
            if (index + 1) <= existing_layers_len:

                ### ly
                layer.summary.ly.next_year_section_reference = nodes_to_keep[index].summary.ly.next_year_section_reference
                layer.summary.ly.next_year_share = nodes_to_keep[index].summary.ly.next_year_share

                layer.summary.ly.current_year_section_reference = nodes_to_keep[index].summary.ly.current_year_section_reference
                layer.summary.ly.current_year_share = nodes_to_keep[index].summary.ly.current_year_share

                layer.summary.ly.risk_adjusted_rate_change = nodes_to_keep[index].summary.ly.risk_adjusted_rate_change

                for child in [
                    "multi_year_period",
                    "reinstatement_description",
                    "bpi",
                    "fot_adequacy",
                    "rms_adequacy",
                    "ulr", 
                    "epi_adj_rate",
                    "prem_full_line",
                    "mi_250",
                    "mi_250_prem_ratio",
                    "mi_10",
                    "mi_10_prem_ratio"
                ]:
                    setattr(layer.summary.ly, child, getattr(nodes_to_keep[index].summary.ly, child))

                ### year_before_last
                for child in [
                    "layer_structure_year_before_last",
                    "current_year_section_reference",
                    "section_reference",
                    "leader",
                    "layer_description",
                    "limit_cnv",
                    "excess_cnv",
                    "rol_quote",
                    "rol_fot",
                    "rol_afb_tech",
                    "reinstatement_description",
                    "roc",
                    "risk_adjusted_rate_change",
                    "bpi",
                    "fot_adequacy",
                    "rms_adequacy",
                    "ulr",
                    "epi_adj_rate",
                    "prem_full_line",
                    "epi_written",
                    "epi_estimated",
                    "epi_signed",
                    "written_line",
                    "estimated_signing",
                    "signed_line",
                    "mi_250",
                    "mi_250_prem_ratio",
                    "mi_10",
                    "mi_10_prem_ratio",                    
                    "current_year_share"
                ]:
                    setattr(layer.summary.year_before_last, child, getattr(nodes_to_keep[index].summary.year_before_last, child))


                ### expiring year

                for child in [
                    "layer_structure_expiring_year",
                    "epi_written",
                    "epi_estimated",
                    "epi_signed",
                    "section_reference",
                    "leader",
                    "layer_description",
                    "limit_cnv",
                    "excess_cnv",
                    "rol_quote",
                    "rol_fot",
                    "rol_afb_tech",
                    "reinstatement_description",
                    "roc",
                    "risk_adjusted_rate_change",
                    "bpi",
                    "fot_adequacy",
                    "rms_adequacy",
                    "ulr",
                    "epi_adj_rate",
                    "prem_full_line",
                    "written_line",
                    "estimated_signing",
                    "signed_line",
                    "mi_250",
                    "mi_250_prem_ratio",
                    "mi_10",
                    "mi_10_prem_ratio"
                ]:
                    setattr(layer.summary.expiring_year, child, getattr(nodes_to_keep[index].summary.expiring_year, child))
        else: 
            ### ly
            layer.summary.ly.next_year_section_reference = populate_data["cds"]["layers"][index]["summary"]["ly"]["next_year_section_reference"]
            layer.summary.ly.next_year_share = populate_data["cds"]["layers"][index]["summary"]["ly"]["next_year_share"]

            layer.summary.ly.current_year_section_reference = populate_data["cds"]["layers"][index]["summary"]["ly"]["current_year_section_reference"]
            layer.summary.ly.current_year_share = populate_data["cds"]["layers"][index]["summary"]["ly"]["current_year_share"]

            layer.summary.ly.risk_adjusted_rate_change = populate_data["cds"]["layers"][index]["summary"]["ly"]["risk_adjusted_rate_change"]

            for child in [
                "multi_year_period",
                "reinstatement_description",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr", 
                "epi_adj_rate",
                "prem_full_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio"
            ]:
                setattr(layer.summary.ly, child, populate_data["cds"]["layers"][index]["summary"]["ly"][child])

            ### year_before_last
            for child in [
                "layer_structure_year_before_last",
                "current_year_section_reference",
                "section_reference",
                "leader",
                "layer_description",
                "limit_cnv",
                "excess_cnv",
                "rol_quote",
                "rol_fot",
                "rol_afb_tech",
                "reinstatement_description",
                "roc",
                "risk_adjusted_rate_change",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr",
                "epi_adj_rate",
                "prem_full_line",
                "epi_written",
                "epi_estimated",
                "epi_signed",
                "written_line",
                "estimated_signing",
                "signed_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio",                    
                "current_year_share"
            ]:
                setattr(layer.summary.year_before_last, child, populate_data["cds"]["layers"][index]["summary"]["year_before_last"][child])

            ### expiring year

            for child in [
                "layer_structure_expiring_year",
                "epi_written",
                "epi_estimated",
                "epi_signed",
                "section_reference",
                "leader",
                "layer_description",
                "limit_cnv",
                "excess_cnv",
                "rol_quote",
                "rol_fot",
                "rol_afb_tech",
                "reinstatement_description",
                "roc",
                "risk_adjusted_rate_change",
                "bpi",
                "fot_adequacy",
                "rms_adequacy",
                "ulr",
                "epi_adj_rate",
                "prem_full_line",
                "written_line",
                "estimated_signing",
                "signed_line",
                "mi_250",
                "mi_250_prem_ratio",
                "mi_10",
                "mi_10_prem_ratio"
            ]:
                setattr(layer.summary.expiring_year, child, populate_data["cds"]["layers"][index]["summary"]["expiring_year"][child])


        ### new nodes
        setattr(layer.summary.ty, "multi_year_period", populate_data["cds"]["layers"][index]["summary"]["ty"]["multi_year_period"])
        setattr(layer.summary.ty, "share", populate_data["cds"]["layers"][index]["summary"]["ty"]["share"])
        setattr(layer.summary.next_year, "share", populate_data["cds"]["layers"][index]["summary"]["next_year"]["share"])
        setattr(layer.summary.year_after_next, "share", populate_data["cds"]["layers"][index]["summary"]["year_after_next"]["share"])



        ## /area_codes ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        northern_europe_values = ['eat', 'ebe', 'ech', 'edk', 'emz', 'efi', 'efr', 'ege', 'eic', 'eie', 'enl', 'eno', 'egf', 'ese', 'euk', 'euf']
        southern_europe_values = ['ees', 'egr', 'eit', 'ept', 'etu']
        cee_values = ['ebg', 'cef', 'ecx', 'ecz', 'ehu', 'epl', 'ero', 'eru', 'esb', 'esc', 'esr']
        us_values = ['usa01', 'usa02', 'usa03', 'usa04', 'usa05', 'usa06', 'usa07', 'usa08', 'usa09', 'usa10', 'usa11', 'usa12', 'usa13', 'usa14', 'usa15', 'usa16', 'usa20', 'usa21', 'usa22']
        lat_am_values = ['sar', 'sbz', 'sbv', 'sbr', 'scl', 'sco', 'scr', 'sec', 'sel', 'sgt', 'sgy', 'shn', 'smx', 'snq', 'spa', 'spy', 'spe', 'suy', 'sve', 'ofg']
        aus_values = ['oa1', 'oa2', 'oa3', 'oa4', 'oa5', 'oa6', 'ota', 'onz', 'ofj']
        caribbean_values = ['bag', 'bah', 'ban', 'bbb', 'bbh', 'bbm', 'bcb', 'bcm', 'bcu', 'bdo', 'bdr', 'bgn', 'bgs', 'bgu', 'bht', 'bjm', 'bkn', 'bmq', 'bms', 'bon', 'bpr', 'bsl', 'bsv', 'bv1', 'bvs', 'bx7']
        canada_values = ['cbc', 'cqu', 'con', 'cpr', 'cat', 'bpm']
        far_east_values = ['fct', 'fcq', 'fkr', 'fhk', 'fia', 'oph', 'fsp', 'fsk', 'fta', 'fjq', 'fjw', 'mbd', 'fcy', 'ogm', 'fmy', 'mma', 'fby', 'fnp', 'mpk', 'opg', 'fth', 'fvn']
        amei_values = ['mis', 'min', 'asa', 'mae', 'mba', 'aal', 'amo', 'aeg', 'ali', 'amu', 'mjo', 'mom', 'mqa', 'ayt', 'agi']

        non_us_fields = northern_europe_values + southern_europe_values + cee_values + lat_am_values + aus_values + caribbean_values + canada_values + far_east_values + amei_values

        for field in non_us_fields:
            setattr(layer.area_codes_select, field, populate_data["cds"]["layers"][index]["area_codes_select"][field])
            setattr(layer.area_codes_perc, field, populate_data["cds"]["layers"][index]["area_codes_perc"][field])

        for field in us_values:
            setattr(layer.area_codes_perc, field, populate_data["cds"]["layers"][index]["area_codes_perc"][field])

        setattr(layer, "area_code_x_eu_ws", populate_data["cds"]["layers"][index]["area_code_x_eu_ws"])






