import hx
# import pandas as pd
# import numpy as np

# SA: This page is to deal with the structures that couldn't be adjusted to fit the cds and the view. I've tried 
# to match the cds data as closely to the mapping sheet as possible for reporting purposes, and duplicated information
# here when that meant it couldn't be put into the correct structures for the view. Restructuring of the data schema
# to better fit with the view may reduce the need for this section. 

def rate_view_data_mapping_inputs(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    rc = layer.rate_change

    layer.excess = cds.final_prem_summary_limit_table.excess
    layer.limit = cds.final_prem_summary_limit_table.limit

    fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.currencies.source_currency]["fx_rate"].iloc[0]
    quoted_premium = cds.final_premium_summary_table.quoted_premium if cds.final_premium_summary_table.quoted_premium is not None else 0
    layer.quoted_premium = cds.final_premium_summary_table.quoted_premium_slip_curr / fx_rate
    print("sag")

def rate_view_data_mapping_outputs(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    rc = layer.rate_change

    cds.final_premium_summary_table.bench_prem = layer.benchmark_premium

    cds.final_premium_summary_table.tpi_pre_uw_adj = layer.tpi_pre_uw_adj
    cds.final_premium_summary_table.bpi_pre_uw_adj = layer.bpi_pre_uw_adj
    
    cds.final_premium_summary_table.tpi = layer.tpi
    cds.final_premium_summary_table.bpi = layer.bpi
    
    cds.final_premium_summary_table.implied_roc = layer.roc

    # Total column in view
    hxd.final_rc_total_summary_view_only.expiry_premium.uw_selected.calculated = rc.expiry_premium.model_calculated 
    hxd.final_rc_total_summary_view_only.exposure_change.uw_selected = rc.exposure_change.model_calculated
    hxd.final_rc_total_summary_view_only.deductible_change.uw_selected = rc.deductible_change.model_calculated
    hxd.final_rc_total_summary_view_only.limit_change.uw_selected = rc.limit_change.model_calculated
    hxd.final_rc_total_summary_view_only.risk_characteristics_change.uw_selected = rc.risk_characteristics_change.model_calculated
    hxd.final_rc_total_summary_view_only.terms_conditions_change.uw_selected = rc.terms_conditions_change.model_calculated
    hxd.final_rc_total_summary_view_only.risk_adj_premium.uw_selected = rc.risk_adj_premium.model_calculated
    hxd.final_rc_total_summary_view_only.quoted_premium = layer.rate_change.quoted_premium

    hxd.final_rc_total_summary_view_only.pure_rc = cds.final_rc_uwadj_summary2.pure_rc_uw_adj
    hxd.final_rc_total_summary_view_only.rate_change.uw_selected = rc.rate_change.model_calculated
    hxd.final_rc_total_summary_view_only.business = layer.rate_change.business
    hxd.final_rc_total_summary_view_only.rate_change_calculated_pryr = rc.rate_change_calculated_pryr
    
    # UW Adj column for rate change
    rc.pure_rc = cds.final_rc_uwadj_summary2.pure_rc_uw_adj
    rc.business = layer.rate_change.business



