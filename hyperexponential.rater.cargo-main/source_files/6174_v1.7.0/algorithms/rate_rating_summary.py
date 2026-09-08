import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import one_layer, ratio, tp_lookup
from algorithms.rate_constants import benchmark_lr
from algorithms import parameter_tables_schema as params

def rate_rating_summary(hxd):
        
    layer, cvg = one_layer(hxd)
    layer.deal_status_record = layer.status

    # Get YOA and NMP load
    yoa = hxd.hx_core.inception_date.year
    tp_params_df = params.tp_parameters.df()
    tp_year = yoa if yoa in list(tp_params_df["year"]) else tp_params_df["year"].max()
    bp_class = hxd.cds.standard_fields.benchmark_class
    nmp_load = tp_lookup("nmp_load", bp_class, tp_year)

    ### Calculate pricing metrics for main coverages from DROPDOWN in the Risk Information.
    # Calculate benchmark premium
    coverages = {
        "Cargo": ["cargo_transit", "cargo_storage"],
        "Cargo Cyber": ["cargo_cyber_transit", "cargo_cyber_storage"],
        "Specie": ["specie_transit", "specie_storage"],
        "Con Loss": ["conloss_transit", "conloss"]
    }
    cover = hxd.cds.cover_selection.cover
    sel_coverages = coverages[cover] if cover else []

    layer.benchmark_premium = 0
    layer.benchmark_premium_pre_uw_adj = 0
    layer.benchmark_premium_att = 0
    layer.benchmark_premium_cat = 0
    
    for cvg_hxd in sel_coverages:
        # Get the BP for each coverage and sum to layer BP
        hxd_cvg_structure = getattr(layer.coverages, cvg_hxd)

        # Value is retrieved from technical premium to match naming of original rater, even though it's a benchmark premium
        bp = getattr(hxd_cvg_structure, "technical_premium") or 0
        bp_pre_uw_adj = getattr(hxd_cvg_structure, "technical_premium_pre_uw_adj") or 0
        bp_att = getattr(hxd_cvg_structure, "technical_premium_att") or 0
        bp_cat = getattr(hxd_cvg_structure, "technical_premium_cat") or 0

        layer.benchmark_premium += bp
        layer.benchmark_premium_pre_uw_adj += bp_pre_uw_adj
        layer.benchmark_premium_att += bp_att
        layer.benchmark_premium_cat += bp_cat

    # Add NMP load
    layer.benchmark_premium *= 1 + nmp_load
    layer.benchmark_premium_pre_uw_adj *= 1 + nmp_load
    layer.benchmark_premium_att *= 1 + nmp_load
    layer.benchmark_premium_cat *= 1 + nmp_load

    # Reverse engineer the expected loss
    layer.expected_loss_cost = layer.benchmark_premium * benchmark_lr * (1-layer.brokerage)
    layer.expected_loss_cost_pre_uw_adj = layer.benchmark_premium_pre_uw_adj * benchmark_lr * (1-layer.brokerage)
    layer.expected_loss_cost_att = layer.benchmark_premium_att * benchmark_lr * (1-layer.brokerage)
    layer.expected_loss_cost_cat = layer.benchmark_premium_cat * benchmark_lr * (1-layer.brokerage)

    # Gross Premium Label
    if layer.status in ["Bound", "Post Bind Complete"]:
        layer.gross_premium_label = "Gross Bound Premium"
    else:
        layer.gross_premium_label = "Gross Quoted Premium"

    layers = hxd.cds.layers
    for index, layer in enumerate(layers):
        layer.quoted_premium_view = layer.quoted_premium  
        layer.written_line_view = layer.written_line
        layer.brokerage_view = layer.brokerage     
        layer.status_view = layer.status
        layer.section_reference_view = hxd.cds.standard_fields.policy_reference
    
    ### Calculate pricing metrics for the add on coverage - Cargo Cyber. when them main coverage from dropdown selection is Cargo.
    # Calculate benchmark premium

    cover_selection = hxd.cds.cover_selection
    layer, cvg = one_layer(hxd)

    if cover_selection.is_cargo_cyber:
        sel_coverages = ["cargo_cyber_transit", "cargo_cyber_storage"]
        layer_cyber = layer.coverages.cargo_cyber_addon
        layer_cyber.benchmark_premium = 0
        layer_cyber.benchmark_premium_pre_uw_adj = 0
        layer_cyber.benchmark_premium_att = 0
        layer_cyber.benchmark_premium_cat = 0
        
        for cvg_hxd in sel_coverages:
            # Get the BP for each coverage and sum to layer BP
            hxd_cvg_structure = getattr(layer.coverages, cvg_hxd)

            # Value is retrieved from technical premium to match naming of original rater, even though it's a benchmark premium
            bp = getattr(hxd_cvg_structure, "technical_premium") or 0
            bp_pre_uw_adj = getattr(hxd_cvg_structure, "technical_premium_pre_uw_adj") or 0
            bp_att = getattr(hxd_cvg_structure, "technical_premium_att") or 0
            bp_cat = getattr(hxd_cvg_structure, "technical_premium_cat") or 0

            layer_cyber.benchmark_premium += bp
            layer_cyber.benchmark_premium_pre_uw_adj += bp_pre_uw_adj
            layer_cyber.benchmark_premium_att += bp_att
            layer_cyber.benchmark_premium_cat += bp_cat

        # Add NMP load
        layer_cyber.benchmark_premium *= 1 + nmp_load
        layer_cyber.benchmark_premium_pre_uw_adj *= 1 + nmp_load
        layer_cyber.benchmark_premium_att *= 1 + nmp_load
        layer_cyber.benchmark_premium_cat *= 1 + nmp_load

        # Reverse engineer the expected loss
        cargo_cyber_brokerage = layer_cyber.brokerage if layer_cyber.brokerage else 0
        layer_cyber.expected_loss_cost = layer_cyber.benchmark_premium * benchmark_lr * (1-cargo_cyber_brokerage)
        layer_cyber.expected_loss_cost_pre_uw_adj = layer_cyber.benchmark_premium_pre_uw_adj * benchmark_lr * (1-cargo_cyber_brokerage)
        layer_cyber.expected_loss_cost_att = layer_cyber.benchmark_premium_att * benchmark_lr * (1-cargo_cyber_brokerage)
        layer_cyber.expected_loss_cost_cat = layer_cyber.benchmark_premium_cat * benchmark_lr * (1-cargo_cyber_brokerage)


        layers = hxd.cds.layers
        for index, layer in enumerate(layers):
            layer_01 = layer.coverages.cargo_cyber_addon
            layer_01.quoted_premium_view = layer_01.quoted_premium  
            layer_01.written_line_view = layer_01.written_line
            layer_01.brokerage_view = layer_01.brokerage     
            layer_01.status_view = layer.status
    else:
        pass


    


    
