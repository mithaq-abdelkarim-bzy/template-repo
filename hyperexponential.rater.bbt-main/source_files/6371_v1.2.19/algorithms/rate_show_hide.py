import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from statistics import mean

def rate_show_hide(hxd):
    cds = hxd.cds

    ########################################################
    ### 1) Show Hide Sheet Rules
    ########################################################
    cds.show_hide.page.show_rms               = False
    cds.show_hide.page.show_profit_commission = False
    cds.show_hide.page.show_triangle          = False
    cds.show_hide.page.show_actuarial         = False

    if cds.model_state.show_after_landing_page:
        
        if cds.risk_info.rms_modelling_available    == "Yes":        cds.show_hide.page.show_rms = True
        if cds.risk_info.pc_modelling_required      == "Yes":        cds.show_hide.page.show_profit_commission = True
        if cds.risk_info.tri_modelling_required     == "Yes":        cds.show_hide.page.show_triangle = True
        if ( cds.rationale.actuarial_review == "Yes") or ( cds.rationale.actuarial_view == True) :        
            cds.show_hide.page.show_actuarial = True


        ########################################################
        ### 2) Show Hide Node Rules
        ########################################################

        ## 2a) risk information - Profit Commission
        ###########################################
        cds.show_hide.node.pc_standard              = True
        cds.show_hide.node.pc_threshold             = False
        cds.show_hide.node.pc_sliding_scale         = False

        if cds.profit_commission.scenarios[0].additionalfeaturesindicator == "No":
            cds.show_hide.node.pc_standard              = True
            cds.show_hide.node.pc_threshold             = False
            cds.show_hide.node.pc_sliding_scale         = False

        if cds.profit_commission.scenarios[0].additionalfeaturesindicator == "Threshold":
            cds.show_hide.node.pc_standard              = True  # we still want to show the basic values
            cds.show_hide.node.pc_threshold             = True
            cds.show_hide.node.pc_sliding_scale         = False

        if cds.profit_commission.scenarios[0].additionalfeaturesindicator == "Sliding Scale":
            cds.show_hide.node.pc_standard              = False # we dont still want to show the basic values
            cds.show_hide.node.pc_threshold             = False
            cds.show_hide.node.pc_sliding_scale         = True



        ## 2b) rating summary - UW Rationale
        ###########################################
        cds.show_hide.node.rs_att_rationale             = False
        cds.show_hide.node.rs_lrg_rationale             = False
        cds.show_hide.node.rs_cat_rationale             = False

        if (cds.rating_summary.summary_ratios.attritional.uw_adjustment is None) == False:
            cds.show_hide.node.rs_att_rationale         = True

        if (cds.rating_summary.summary_ratios.large.uw_adjustment is None) == False:
            cds.show_hide.node.rs_lrg_rationale         = True

        if (cds.rating_summary.summary_ratios.catastrophe.uw_adjustment is None) == False:
            cds.show_hide.node.rs_cat_rationale         = True

        if (cds.rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_uw_override is None) == False:
            cds.show_hide.node.rs_att_rationale         = True

        if cds.rating_summary.summary_ratios.large.uw_override == True:
            cds.show_hide.node.rs_lrg_rationale         = True

        if cds.rating_summary.summary_ratios.catastrophe.uw_override == True:
            cds.show_hide.node.rs_cat_rationale         = True


        ## 2c) rating summary - New to Market (not)
        ###########################################
        cds.show_hide.node.not_new_to_market            = True

        if (cds.risk_info.new_to_market == "Yes"):
            cds.show_hide.node.not_new_to_market        = False


        ## 2d) rating summary - RMS or Benchmark
        ###########################################
        cds.show_hide.node.loss_ratio_rms               = False
        cds.show_hide.node.loss_ratio_benchmark         = True

        if (cds.risk_info.rms_modelling_available == "Yes"):
            cds.show_hide.node.loss_ratio_rms               = True
            cds.show_hide.node.loss_ratio_benchmark         = False

        ## 2e) risk information - proxy trifocus
        cds.show_hide.node.ri_proxy_trifocus             = (cds.risk_info.trifocus_valid == False)
