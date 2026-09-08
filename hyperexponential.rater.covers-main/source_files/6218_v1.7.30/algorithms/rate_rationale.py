import hx
import polars as pl
import pandas as pd
import os
from datetime import datetime
from mailmerge import MailMerge
from algorithms.rate_common_rating_functions import join_param_table
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd


def rate_rationale(hxd):
    
    cds = hxd.cds

    # Load in premiums/incurred historical information
    df = pd_df_from_hx_list(cds.rating_summary.detail_by_year)

    total_deductions = cds.layers[0].total_deductions

    # initialise to 0, then do calc where it will not cause an error
    df["premium_selected_gn"] = None
    df.loc[df['premium_selected'].notnull(), 'premium_selected_gn'] = df["premium_selected"] * (1 - total_deductions)

    # initialise to 0, then do calc where it will not cause an error
    df["incurred_selected_lr"] = 0
    df["incurred_selected_lr_gn"] = 0
    
    df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'incurred_selected_lr'] = df["incurred_selected"] / df["premium_selected"]
    df.loc[df['premium_selected_gn'].notnull() & df['premium_selected_gn'] != 0, 'incurred_selected_lr_gn'] = df["incurred_selected"] / df["premium_selected_gn"]

    # initialise to 0, then do calc where it will not cause an error
    df["incurred_non_cat_selected_lr"] = 0
    df["incurred_non_cat_selected_lr_gn"] = 0
    
    df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'incurred_non_cat_selected_lr'] = (df["incurred_att_selected"] + df["incurred_large_selected"]) / df["premium_selected"]
    df.loc[df['premium_selected_gn'].notnull() & df['premium_selected_gn'] != 0, 'incurred_non_cat_selected_lr_gn'] = (df["incurred_att_selected"] + df["incurred_large_selected"]) / df["premium_selected_gn"]

    # set any GN blank premiums to 0 (need to only set this to 0 at the end owing to a division by 0 error on the previous line if set to 0 earlier.)
    df.loc[df['premium_selected_gn'].isnull(), "premium_selected_gn"] = 0

    # write value to incurred LR column
    write_pd_to_hxd(df, cds.rating_summary.detail_by_year, [
        "premium_selected_gn", "incurred_selected_lr", "incurred_selected_lr_gn",
        "incurred_non_cat_selected_lr", "incurred_non_cat_selected_lr_gn"
        ])

    # calculate overall incurred LR
    tot_incurred = df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'incurred_selected'].sum()
    tot_premium = df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'premium_selected'].sum()
    tot_premium_gn = df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'premium_selected_gn'].sum()

    tot_att_incurred = df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'incurred_att_selected'].sum()
    tot_large_incurred = df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'incurred_large_selected'].sum()

    tot_non_cat_incurred = tot_att_incurred + tot_large_incurred

    tot_ilr = tot_incurred / tot_premium if tot_premium > 0 else 0
    tot_ilr_gn = tot_incurred / tot_premium_gn if tot_premium_gn > 0 else 0

    tot_non_cat_ilr = tot_non_cat_incurred / tot_premium if tot_premium > 0 else 0
    tot_non_cat_ilr_gn = tot_non_cat_incurred / tot_premium_gn if tot_premium_gn > 0 else 0

    cds.rating_summary.detail_by_year_total.premium_selected = tot_premium
    cds.rating_summary.detail_by_year_total.premium_selected_gn = tot_premium_gn

    cds.rating_summary.detail_by_year_total.incurred_selected = tot_incurred

    cds.rating_summary.detail_by_year_total.incurred_selected_lr = tot_ilr
    cds.rating_summary.detail_by_year_total.incurred_selected_lr_gn = tot_ilr_gn

    cds.rating_summary.detail_by_year_total.incurred_non_cat_selected_lr = tot_non_cat_ilr
    cds.rating_summary.detail_by_year_total.incurred_non_cat_selected_lr_gn = tot_non_cat_ilr_gn



    # calculate earliest year of data
    if (df.shape[0] > 0) & (df['premium_selected'].sum() > 0):
        first_year = int(df.loc[df['premium_selected'].notnull() & df['premium_selected'] != 0, 'yoa'].iloc[0])
    else:
        first_year = ''

    # select type of Coverage
    if cds.layers[0].HO6_coverage == "Yes":
        coverage_name = "HO6"
    else:
        coverage_name = cds.risk_info.coverage

    # set contract summary string
    if coverage_name == "Special":
        cds.rationale.contract_summary.calculated = f"This contract has an incurred ratio of {str(round(tot_ilr * 100, 0))}% since {first_year}"
    else:
        cds.rationale.contract_summary.calculated = f"This is a {coverage_name} contract and since {first_year} has an incurred ratio of {str(round(tot_ilr * 100, 0))}%."

    # set risk type string
    if coverage_name == "Special":
        cds.rationale.risk_type.calculated = ""
    else:
        cds.rationale.risk_type.calculated = coverage_name

    # set previous rate change
    prev_yr = hxd.cds.standard_fields.inception_date.year - 1
    if (df.shape[0] > 0) & (prev_yr in df["yoa"].unique()):
        prev_rc = df.loc[df["yoa"] == prev_yr, "rate_chg_selected"].iloc[0]
    else:
        prev_rc = None

    cds.rationale.prev_rc = prev_rc

    # # set attrititonal + large loss ratio
    # if (cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.ulr_selected_ol is not None) & (cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.ulr_selected_ol is not None):
    #     att_lr_ol = cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.ulr_selected_ol + cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.ulr_selected_ol
    # else:
    #     att_lr_ol = None
    # cds.rationale.att_lr_ol = att_lr_ol

    # # set attrititonal + large loss picks
    # if (cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.ulr_final is not None) & (cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.ulr_final is not None):
    #     att_lr = cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.ulr_final + cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.ulr_final
    # else:
    #     att_lr = None
    # cds.rationale.att_lr = att_lr

    # set combined ratio (fixed method of adding 20% to sum of other LRs)
    # comb_ratio = cds.exposure_experience_weights.experience_rating.post_uw_adj_gn_ulr + 0.2 if cds.exposure_experience_weights.experience_rating.post_uw_adj_gn_ulr else None
    # comb_ratio = cds.rating_summary.gn_comb_ratio_inc_pc
    # cds.rationale.comb_ratio = comb_ratio

    # set premium to AAL ratio
    prem = cds.layers[0].quoted_premium_100pct
    aal = cds.rms.edm_summary.all_peril_selected_at_acc_fx.aal
    prm_aal_ratio = prem / aal if prem and aal and aal != 0 else 0
    cds.rationale.prm_aal_ratio = prm_aal_ratio

     #need to define rationale variables so the label names are correct
    
    cds.rationale.gg_att_lr_pre = cds.rating_summary.summary_ratios.attritional.gg_pst_uw_adj.blended_LR
    cds.rationale.att_uw_adj = cds.rating_summary.summary_ratios.attritional.uw_adjustment
    cds.rationale.gg_att_lr_pst = cds.rating_summary.summary_ratios.attritional.gg_pst_uw_adj.ulr_final

    cds.rationale.gg_large_lr_pre = cds.rating_summary.summary_ratios.large.gg_pst_uw_adj.blended_LR
    cds.rationale.large_uw_adj = cds.rating_summary.summary_ratios.large.uw_adjustment
    cds.rationale.gg_large_lr_pst = cds.rating_summary.summary_ratios.large.gg_pst_uw_adj.ulr_final

    cds.rationale.gg_cat_lr_pre = cds.rating_summary.summary_ratios.catastrophe.gg_pst_uw_adj.blended_LR
    cds.rationale.cat_uw_adj = cds.rating_summary.summary_ratios.catastrophe.uw_adjustment
    cds.rationale.gg_cat_lr_pst = cds.rating_summary.summary_ratios.catastrophe.gg_pst_uw_adj.ulr_final

    cds.rationale.gg_total_lr_pre = cds.rating_summary.summary_ratios.total.gg_pre_uw_adj.ulr_priced_final
    cds.rationale.gg_total_lr_pst = cds.rating_summary.summary_ratios.total.gg_pst_uw_adj.ulr_priced_final

    cds.rationale.gn_att_lr_pre = cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.blended_LR
    cds.rationale.gn_att_lr_pst = cds.rating_summary.summary_ratios.attritional.gn_pst_uw_adj.ulr_final

    cds.rationale.gn_large_lr_pre = cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.blended_LR
    cds.rationale.gn_large_lr_pst = cds.rating_summary.summary_ratios.large.gn_pst_uw_adj.ulr_final

    cds.rationale.gn_cat_lr_pre = cds.rating_summary.summary_ratios.catastrophe.gn_pst_uw_adj.blended_LR
    cds.rationale.gn_cat_lr_pst = cds.rating_summary.summary_ratios.catastrophe.gn_pst_uw_adj.ulr_final

    cds.rationale.gn_total_lr_pre = cds.rating_summary.summary_ratios.total.gn_pre_uw_adj.ulr_priced_final_exc_pc
    cds.rationale.gn_total_lr_pst = cds.rating_summary.summary_ratios.total.gn_pst_uw_adj.ulr_priced_final_exc_pc
    
    cds.rationale.comb_ratio_pre_adj_exc_pc   =   hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_exc_pc 
    cds.rationale.comb_ratio_pre_adj_inc_pc   =   hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_inc_pc 
    cds.rationale.comb_ratio_pst_adj_exc_pc   =   hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_exc_pc 
    cds.rationale.comb_ratio_pst_adj_inc_pc   =   hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_inc_pc 

def generate_uw_rationale_doc(hxd, progress):
    
    cds = hxd.cds
      


    coverholder_str = cds.standard_fields.insured_name if cds.standard_fields.insured_name else ""
    inception_date_str = cds.standard_fields.inception_date.strftime("%d-%b-%Y")
    binder_ref_str = cds.standard_fields.facility_reference if cds.standard_fields.facility_reference else ""
    coverholder_background = cds.rationale.coverholder_background
    contract_summary_str = cds.rationale.contract_summary.selected
    broker_str = cds.standard_fields.broker if cds.standard_fields.broker else ""
    risk_type_str = cds.rationale.risk_type.selected if cds.rationale.risk_type.selected else ""
    construction_str = cds.rationale.construction.selected if cds.rationale.construction.selected else ""
    written_line_str = f"{cds.layers[0].written_line*100:,.2f}%" if cds.layers[0].written_line else "0%"
    signed_line_str = f"{cds.layers[0].signed_line*100:,.2f}%" if cds.layers[0].signed_line else "0%"
    total_deductions_str = f"{cds.layers[0].total_deductions*100:,.2f}%" if cds.layers[0].total_deductions else "0%"
    risk_currency_str = cds.currencies.source_currency if cds.currencies.source_currency else ""
    risk_limit_str = f"{cds.rationale.risk_limit:,.0f}" if cds.rationale.risk_limit else ""
    avg_limit_str = f"{cds.rationale.avg_limit:,.0f}" if cds.rationale.avg_limit else ""
    top_counties_str = cds.rationale.top_counties.selected if cds.rationale.top_counties.selected else ""
    avg_rate_str = f"{cds.rationale.avg_rate.selected:,.2f}" if cds.rationale.avg_rate.selected else "0.00"
    curr_epi_str = f"{cds.rationale.curr_epi:,.0f}" if cds.rationale.curr_epi else "0"
    prev_epi_str = f"{cds.rationale.prev_epi:,.0f}" if cds.rationale.prev_epi else "0"
    curr_rc_str = f"{cds.rationale.curr_rc*100:,.2f}%" if cds.rationale.curr_rc else "0%"
    prev_rc_str = f"{cds.rationale.prev_rc*100:,.2f}%" if cds.rationale.prev_rc else "0%"
    # att_lr_str = f"{cds.rationale.att_lr_ol*100:,.1f}%" if cds.rationale.att_lr_ol else "0%"
    # att_lr_sel_str = f"{cds.rationale.att_lr*100:,.1f}%" if cds.rationale.att_lr else "0%"
    # cat_lr_sel_str = f"{cds.rating_summary.summary_ratios.catastrophe.gn_pst_uw_adj.ulr_final*100:,.1f}%" if cds.rating_summary.summary_ratios.catastrophe.gn_pst_uw_adj.ulr_final else "0%"
    
    comb_ratio_pre_inc_pc_str = f"{hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_inc_pc*100:,.1f}%" if hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_inc_pc else "0%"
    comb_ratio_inc_pc_str = f"{hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_inc_pc*100:,.1f}%" if hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_inc_pc else "0%"
    
    comb_ratio_pre_exc_pc_str = f"{hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_exc_pc*100:,.1f}%" if hxd.cds.rating_summary.summary_ratios.total.pre_uw_adj.comb_ratio_exc_pc else "0%"
    comb_ratio_exc_pc_str = f"{hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_exc_pc*100:,.1f}%" if hxd.cds.rating_summary.summary_ratios.total.pst_uw_adj.comb_ratio_exc_pc else "0%"


    bpi_str = f"{cds.rating_summary.kpi.pst_uw_adj.bpi*100:,.1f}%" if cds.rating_summary.kpi.pst_uw_adj.bpi else "0%"
    tpi_str = f"{cds.rating_summary.kpi.pst_uw_adj.tpi*100:,.1f}%" if cds.rating_summary.kpi.pst_uw_adj.tpi else "0%"
    roc_str = f"{cds.rating_summary.kpi.pst_uw_adj.roc*100:,.1f}%" if cds.rating_summary.kpi.pst_uw_adj.roc else "0%"
    aal_str = f"{cds.rms.edm_summary.all_peril_selected_at_acc_fx.aal:,.0f}" if cds.rms.edm_summary.all_peril_selected_at_acc_fx.aal else "0"
    prm_aal_ratio_str = f"{cds.rationale.prm_aal_ratio:,.2f}x" if cds.rationale.prm_aal_ratio else "0x"
    amount_pc_100_str = f"{cds.rating_summary.technical.amount_pc_100:,.0f}" if cds.rating_summary.technical.amount_pc_100 else "0"
    percent_pc_str = f"{cds.rating_summary.technical.percent_pc*100:,.2f}%" if cds.rating_summary.technical.percent_pc else "0%"
    uw_commentary = cds.rationale.uw_commentary
    actuarial_notes = cds.rationale.actuarial_notes
    rc_commentary = cds.rationale.rc_commentary
    tc_commentary = cds.rationale.tc_commentary
    agglim_util_commentary = cds.rationale.agglim_util_commentary
    risk_profile_commentary = cds.rationale.risk_profile_commentary
    territory_profile_commentary = cds.rationale.territory_profile_commentary
    exposure_change_commentary = cds.rationale.exposure_change_commentary
    large_losses_commentary = cds.rationale.large_losses_commentary


    gg_att_lr_pre_str = f"{cds.rationale.gg_att_lr_pre*100:,.1f}%" if cds.rationale.gg_att_lr_pre else "0%"
    att_uw_adj_str = f"{cds.rationale.att_uw_adj*100:,.1f}%" if cds.rationale.att_uw_adj else "0%"
    gg_att_lr_pst_str = f"{cds.rationale.gg_att_lr_pst*100:,.1f}%" if cds.rationale.gg_att_lr_pst else "0%"

    gg_large_lr_pre_str = f"{cds.rationale.gg_large_lr_pre*100:,.1f}%" if cds.rationale.gg_large_lr_pre else "0%"
    large_uw_adj_str = f"{cds.rationale.large_uw_adj*100:,.1f}%" if cds.rationale.large_uw_adj else "0%"
    gg_large_lr_pst_str = f"{cds.rationale.gg_large_lr_pst*100:,.1f}%" if cds.rationale.gg_large_lr_pst else "0%"

    gg_cat_lr_pre_str = f"{cds.rationale.gg_cat_lr_pre*100:,.1f}%" if cds.rationale.gg_cat_lr_pre else "0%"
    cat_uw_adj_str = f"{cds.rationale.cat_uw_adj*100:,.1f}%" if cds.rationale.cat_uw_adj else "0%"
    gg_cat_lr_pst_str = f"{cds.rationale.gg_cat_lr_pst*100:,.1f}%" if cds.rationale.gg_cat_lr_pst else "0%"

    gg_total_lr_pre_str = f"{cds.rationale.gg_total_lr_pre*100:,.1f}%" if cds.rationale.gg_total_lr_pre else "0%"
    gg_total_lr_pst_str = f"{cds.rationale.gg_total_lr_pst*100:,.1f}%" if cds.rationale.gg_total_lr_pst else "0%"

    gn_att_lr_pre_str = f"{cds.rationale.gn_att_lr_pre*100:,.1f}%" if cds.rationale.gn_att_lr_pre else "0%"
    gn_att_lr_pst_str = f"{cds.rationale.gn_att_lr_pst*100:,.1f}%" if cds.rationale.gn_att_lr_pst else "0%"

    gn_large_lr_pre_str = f"{cds.rationale.gn_large_lr_pre*100:,.1f}%" if cds.rationale.gn_large_lr_pre else "0%"
    gn_large_lr_pst_str = f"{cds.rationale.gn_large_lr_pst*100:,.1f}%" if cds.rationale.gn_large_lr_pst else "0%"

    gn_cat_lr_pre_str = f"{cds.rationale.gn_cat_lr_pre*100:,.1f}%" if cds.rationale.gn_cat_lr_pre else "0%"
    gn_cat_lr_pst_str = f"{cds.rationale.gn_cat_lr_pst*100:,.1f}%" if cds.rationale.gn_cat_lr_pst else "0%"

    gn_total_lr_pre_str = f"{cds.rationale.gn_total_lr_pre*100:,.1f}%" if cds.rationale.gn_total_lr_pre else "0%"
    gn_total_lr_pst_str = f"{cds.rationale.gn_total_lr_pst*100:,.1f}%" if cds.rationale.gn_total_lr_pst else "0%"

    att_uw_adj_rationale_str = hxd.cds.rating_summary.summary_ratios.attritional.uw_rationale
    lrg_uw_adj_rationale_str = hxd.cds.rating_summary.summary_ratios.large.uw_rationale
    cat_uw_adj_rationale_str = hxd.cds.rating_summary.summary_ratios.catastrophe.uw_rationale

    # total_uw_adj_str = f"{total_uw_pre*100:,.1f}%" if cds.rationale.total_lr_pre else "0%"
    # total_lr_pst_str = f"{total_lr_pst*100:,.1f}%" if cds.rationale.total_lr_pst else "0%"


    template = os.path.join(os.path.dirname(__file__), "rationale_documents/uw_rationale_doc.docx")
    document = MailMerge(template)

    document.merge(
        coverholder = coverholder_str,
        inception_date = inception_date_str,
        binder_ref = binder_ref_str,
        coverholder_background = coverholder_background,
        contract_summary = contract_summary_str,
        broker = broker_str,
        risk_type = risk_type_str,
        construction = construction_str,
        written_line = written_line_str,
        signed_line = signed_line_str,
        total_deductions = total_deductions_str,
        risk_currency = risk_currency_str,
        risk_limit = risk_limit_str,
        avg_limit = avg_limit_str,
        top_counties = top_counties_str,
        avg_rate = avg_rate_str,
        curr_epi = curr_epi_str,
        prev_epi = prev_epi_str,
        curr_rc = curr_rc_str,
        prev_rc = prev_rc_str,
        
        gg_att_lr_pre = gg_att_lr_pre_str,
        att_uw_adj = att_uw_adj_str,
        gg_att_lr_pst = gg_att_lr_pst_str,

        gg_large_lr_pre = gg_large_lr_pre_str,
        large_uw_adj = large_uw_adj_str,
        gg_large_lr_pst = gg_large_lr_pst_str,

        gg_cat_lr_pre = gg_cat_lr_pre_str,
        cat_uw_adj = cat_uw_adj_str,
        gg_cat_lr_pst = gg_cat_lr_pst_str,


        gg_total_lr_pre = gg_total_lr_pre_str, 
        gg_total_lr_pst = gg_total_lr_pst_str, 

        gn_att_lr_pre = gn_att_lr_pre_str,
        gn_att_lr_pst = gn_att_lr_pst_str,

        gn_large_lr_pre = gn_large_lr_pre_str,
        gn_large_lr_pst = gn_large_lr_pst_str,

        gn_cat_lr_pre = gn_cat_lr_pre_str,
        gn_cat_lr_pst = gn_cat_lr_pst_str,

        gn_total_lr_pre = gn_total_lr_pre_str, 
        gn_total_lr_pst = gn_total_lr_pst_str, 

        att_uw_adj_rationale = att_uw_adj_rationale_str,
        lrg_uw_adj_rationale = lrg_uw_adj_rationale_str,
        cat_uw_adj_rationale = cat_uw_adj_rationale_str,

        comb_ratio_exc_pc = comb_ratio_exc_pc_str,
        comb_ratio_inc_pc = comb_ratio_inc_pc_str,

        bpi = bpi_str,
        tpi = tpi_str,
        roc = roc_str,
        aal = aal_str, 
        prm_aal_ratio = prm_aal_ratio_str,
        amount_pc_100 = amount_pc_100_str,
        percent_pc = percent_pc_str,
        uw_commentary = uw_commentary,
       # uw_commentary_file1 = hxd.cds.rationale.uw_commentary_file1,                      # files dont seem to work currnetly
        actuarial_notes = hxd.cds.rationale.actuarial_notes,
       # actuarial_commentary_file1 = hxd.cds.rationale.actuarial_commentary_file1,           # not sure why white doesnt work
        rc_commentary = rc_commentary,
        tc_commentary = tc_commentary,
        agglim_util_commentary = agglim_util_commentary,
        risk_profile_commentary = risk_profile_commentary,
        territory_profile_commentary = territory_profile_commentary,
        exposure_change_commentary = exposure_change_commentary,
        large_losses_commentary = large_losses_commentary
        )

    binder_history = []
    for i in hxd.cds.rating_summary.detail_by_year:
        if i.yoa:
            binder_history.append({
                "yoa": f"{int(i.yoa)}",
                "gg_written_prem": f"{i.premium_selected:,.0f}",
                "gn_written_prem": f"{i.premium_selected_gn:,.0f}",
                "incurred": f"{i.incurred_selected:,.0f}",
                "gg_incurred_lr": f"{i.incurred_selected_lr*100:,.2f}%",
                "gn_incurred_lr": f"{i.incurred_selected_lr_gn*100:,.2f}%",
                "gg_non_cat_incurred_lr": f"{i.incurred_non_cat_selected_lr*100:,.2f}%",
                "gn_non_cat_incurred_lr": f"{i.incurred_non_cat_selected_lr_gn*100:,.2f}%",
            })
    document.merge_rows("yoa", binder_history)
    
    # total row
    i = hxd.cds.rating_summary.detail_by_year_total
    document.merge(
        gg_written_prem_tot = f"{i.premium_selected:,.0f}",
        gn_written_prem_tot = f"{i.premium_selected_gn:,.0f}",
        incurred_tot = f"{i.incurred_selected:,.0f}",
        gg_incurred_lr_tot = f"{i.incurred_selected_lr*100:,.2f}%",
        gn_incurred_lr_tot = f"{i.incurred_selected_lr_gn*100:,.2f}%",
        gg_non_cat_incurred_lr_tot = f"{i.incurred_non_cat_selected_lr*100:,.2f}%",
        gn_non_cat_incurred_lr_tot = f"{i.incurred_non_cat_selected_lr_gn*100:,.2f}%",
    )

    with hxd.cds.rationale.document.open("b") as f:
        document.write(f)



