import json
import os
import pandas as pd
import polars as pl

import hx

from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from libraries.rate_change.algorithms.rate_change import RateChange as RateChangeLib
from mailmerge import MailMerge
from libraries.rate_change.algorithms.transient_hxd.transient_hxd import rgetattr, rsetattr
# from algorithms.rate_change_execuguard import RateChangeExecuguard
from algorithms.rate_utilities import calc_pro_rata, look_up, look_up_with_bounds
from datetime import datetime
from algorithms.rate_rate_change import rate_change_exposure, rate_change_deductible, rate_change_limit, weighted_sum_with_none_handling
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report
from algorithms.utilities import html_to_text

# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''

@hx.task
def num_layers_task(hxd, progress):
    current_num_layers = len(hxd.cds.layers)
    new_num_layers = hxd.non_cds.cover_details.num_layers

    if current_num_layers < new_num_layers:
        # Add new rows
        hxd.cds.layers.extend([{} for _ in range(current_num_layers, new_num_layers)])
    elif current_num_layers > new_num_layers:
        # Delete rows
        for i in range(current_num_layers - 1, new_num_layers - 1, -1):
            del hxd.cds.layers[i]


@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id

@hx.task
def start_renewal_task(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below    
    ms = hxd.model_state
    sf = hxd.cds.standard_fields
    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
        
    else:
        sf.is_renewal = True
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id        
        # Add tasks which must be done before starting a policy here >>    

@hx.task
def expiring_policy_fetch_task(hxd, progress):
    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected
    # expiring_policy_option_id = "1215558"
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]
    return expiring_data


@hx.task
def rarc_task(hxd, progress):
    '''HX task to calculate and populate rate change tables'''
    # if not hxd.cds.rate_change.expiring_policy_option_id.selected:
    #     hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Make sure expiring data is up to date
    expiring_data = expiring_policy_fetch_task(hxd, progress)

        #determine which coverages to include
    rc = hxd.cds.rate_change
    qg_summary = hxd.cds.quote_grid_summary
    coverages = []
    for coverage in ["epl", "fid", "pcl"]:
        if getattr(hxd.cds.coverage_elections, coverage) and expiring_data["cds"]["coverage_elections"][coverage]:
            coverages.append(coverage)
            setattr(rc.coverage_indicator, coverage, True)
    
    if len(coverages) > 1:
        execuguard_package = True
    else: 
        execuguard_package = False

    if execuguard_package and "pcl" in coverages:
        rc.execugard_package = True
    elif not execuguard_package and "pcl" in coverages: 
        rc.not_execugard_package = True
    else:
        rc.execugard_package = False
        rc.not_execugard_package = False


    # pull prem data for selected covereages
    #rc.premium_annualized_beazley_share.execuguard.renewal = hxd.cds.final_premium_summary.post_rounding_admitted_premium
    #rc.premium_annualized_beazley_share.execuguard.expiring = expiring_data["cds"]["final_premium_summary"]["post_rounding_admitted_premium"]

    for coverage in coverages:
        getattr(rc.premium_annualized_beazley_share, coverage).renewal = getattr(qg_summary,coverage).post_rounding_admitted_premium
        #getattr(rc.premium_annualized_beazley_share, coverage).expiring = expiring_data["cds"]["quote_grid_summary"][coverage]["post_rounding_admitted_premium"]

        vals_cov =[expiring_data["cds"]["quote_grid_summary"][coverage]["post_rounding_admitted_premium"],expiring_data["cds"]["quote_grid_summary"][coverage]["selected_premium"],expiring_data["cds"]["quote_grid_summary"][coverage]["pre_rounding_admitted_premium"]]
        expiring_prem_cov= [x for x in vals_cov if x is not None and x!=0]
        getattr(rc.premium_annualized_beazley_share, coverage).expiring = expiring_prem_cov[0] if expiring_prem_cov else 1.0

    # pull data for execuguard package
    rc.premium_annualized_beazley_share.execuguard.renewal = hxd.cds.final_premium_summary.post_rounding_admitted_premium
    
    expiring_execuguard_cov_sum = sum(getattr(rc.premium_annualized_beazley_share, coverage).expiring for coverage in coverages)
    rc.premium_annualized_beazley_share.execuguard.expiring = expiring_execuguard_cov_sum if expiring_execuguard_cov_sum else 1.0
      
    

    # Brokerage 
    exp_brokerage = expiring_data["cds"]["layers"][0]["brokerage"] if expiring_data["cds"]["layers"][0]["brokerage"] else 0
    ren_brokerage = hxd.cds.layers[0].brokerage if hxd.cds.layers[0].brokerage else 0 
    brokerage_factor = (1 - exp_brokerage) / (1 - ren_brokerage) if (1 - ren_brokerage) != 0 else 1
     
    # Set RC factors that are user input 
    for factor in ["risk_characteristics_change", "terms_conditions_change", "brokerage_change"]:
        value = brokerage_factor if factor == "brokerage_change" else 1
        for coverage in coverages + ["execuguard"]:
            getattr(getattr(rc, factor), coverage).model = value
            getattr(getattr(rc, factor),coverage).selected.calculated = value


    #calcualte RC 
    # # expsoure RC calcs 
    rate_change_exposure(hxd, execuguard_package, coverages, expiring_data)

    # Ded rate change calcs
    rate_change_deductible(hxd, execuguard_package, coverages, expiring_data)

    rate_change_limit(hxd, execuguard_package, coverages, expiring_data)

    ### Execugard package risk characteristics change
    # write execuguard package data 
    weights = {
        'epl': 0.55,
        'fid': 0.1,
        'pcl': 0.35
    }

    # Model values
    variables_model = {
        'epl': rc.risk_characteristics_change.epl.model,
        'fid': rc.risk_characteristics_change.fid.model,
        'pcl': rc.risk_characteristics_change.pcl.model
    }
    variables_selected = {
        'epl': rc.risk_characteristics_change.epl.selected.selected,
        'fid': rc.risk_characteristics_change.fid.selected.selected,
        'pcl': rc.risk_characteristics_change.pcl.selected.selected
    }

    # Assign results
    rc.risk_characteristics_change.execuguard.model = weighted_sum_with_none_handling(variables_model, weights)
    rc.risk_characteristics_change.execuguard.selected.calculated = weighted_sum_with_none_handling(variables_selected, weights)
    
    ### Execugard package terms conditions change
    # Model values
    variables_model = {
        'epl': rc.terms_conditions_change.epl.model,
        'fid': rc.terms_conditions_change.fid.model,
        'pcl': rc.terms_conditions_change.pcl.model
    }
    variables_selected = {
        'epl': rc.terms_conditions_change.epl.selected.selected,
        'fid': rc.terms_conditions_change.fid.selected.selected,
        'pcl': rc.terms_conditions_change.pcl.selected.selected
    }

    # Assign results
    rc.terms_conditions_change.execuguard.model = weighted_sum_with_none_handling(variables_model, weights)
    rc.terms_conditions_change.execuguard.selected.calculated = weighted_sum_with_none_handling(variables_selected, weights)
   
   

    for coverage in coverages + ["execuguard"]:
        if coverage == "execuguard":
            #set premiums
            #rc.premium_annualized_beazley_share.execuguard.renewal = sum(getattr(qg_summary, cov).post_rounding_admitted_premium for cov in coverages)
            #rc.premium_annualized_beazley_share.execuguard.expiring = sum(expiring_data["cds"]["quote_grid_summary"][cov]["post_rounding_admitted_premium"] for cov in coverages)
            #rc.premium_annualized_beazley_share.execuguard.expiring = sum((expiring_data["cds"]["quote_grid_summary"][cov]["post_rounding_admitted_premium"]
             #   if expiring_data["cds"]["quote_grid_summary"][cov]["post_rounding_admitted_premium"] is not None
              #  else expiring_data["cds"]["quote_grid_summary"][cov]["pre_rounding_admitted_premium"]) for cov in coverages)

            running_prem_model_expected = sum(getattr(rc.premium_annualized_beazley_share, cov).expiring for cov in coverages)
            running_prem_selected_expected = running_prem_model_expected
        else:
           # getattr(rc.premium_annualized_beazley_share, coverage).renewal = getattr(qg_summary,coverage).post_rounding_admitted_premium
            #getattr(rc.premium_annualized_beazley_share, coverage).expiring = expiring_data["cds"]["quote_grid_summary"][coverage]["post_rounding_admitted_premium"]
           # getattr(rc.premium_annualized_beazley_share, coverage).expiring = (expiring_data["cds"]["quote_grid_summary"][coverage]["post_rounding_admitted_premium"]
            #    if expiring_data["cds"]["quote_grid_summary"][coverage]["post_rounding_admitted_premium"] is not None
             #   else expiring_data["cds"]["quote_grid_summary"][coverage]["pre_rounding_admitted_premium"])

            running_prem_model_expected = getattr(rc.premium_annualized_beazley_share, coverage).expiring
            running_prem_selected_expected = getattr(rc.premium_annualized_beazley_share, coverage).expiring


        for factor in ["exposure_change", "risk_characteristics_change", "limit_change", "deductible_change", "terms_conditions_change", "brokerage_change"]:
            
            running_prem_model_expected *= getattr(getattr(rc,factor),coverage).model if getattr(getattr(rc,factor),coverage).model else 1
            running_prem_selected_expected *= getattr(getattr(rc,factor),coverage).selected.selected if getattr(getattr(rc,factor),coverage).selected.selected else 1
        
        getattr(rc.rate_change, coverage).model = getattr(rc.premium_annualized_beazley_share,coverage).renewal / running_prem_model_expected if running_prem_model_expected != 0 else 0 
        getattr(rc.rate_change, coverage).selected.calculated = getattr(rc.premium_annualized_beazley_share,coverage).renewal / running_prem_selected_expected  if running_prem_selected_expected != 0 else 0 

    # using this to check if prem changed and task needs to be ran again
    rc.check_if_prem_changed = hxd.cds.final_premium_summary.pre_rounding_admitted_premium + hxd.cds.final_premium_summary.post_rounding_admitted_premium

    # set overall UW selected RC 
    rc.uw_selected_rarc = rc.rate_change.execuguard.selected.selected

# def rate_change_warning_message(bool_r: bool, bool_e: bool, coverage: str, existing_message: str) -> str:
#     '''Construct rate change warning message.  Each new message is placed on a new line'''
#     message = ""
#     new_line = "\n" if existing_message != "" else ""

#     if bool_r and not bool_e:
#         message += f"{new_line}⚠️ Warning! {coverage} rate change has not been calculated:      {coverage} coverage is selected but is not selected in the expiring data"
#     elif not bool_r and bool_e:
#         message += f"{new_line}⚠️ Warning! {coverage} rate change has not been calculated:      {coverage} coverage is not selected but is selected in the expiring data"

#     return existing_message + message



@hx.task
def word_documents_task(hxd, progress):
    #define the path of the document
    template = os.path.join(os.path.dirname(__file__), "documents/coverage_options.docx")
    #create the document
    document = MailMerge(template)

    rc = hxd.cds.rate_change.rate_change

    #merging in the items to match the merge fields in template
    document.merge(
    underwriter_name=f"{hxd.cds.standard_fields.underwriter}",
    insured_name=f"{hxd.cds.standard_fields.insured_name}",
    inception_date=f"{hxd.hx_core.inception_date}",
    expiry_date=f"{hxd.hx_core.expiry_date}",
    status_input = f"{hxd.cds.layers[0].status}",
    section_reference = f"{hxd.cds.layers[0].section_reference}",
    brokerage = f"{hxd.cds.layers[0].brokerage*100:.1f}%",
    written_line = f"{hxd.cds.layers[0].written_line*100:.1f}%",
    quoted_premium = f"{hxd.cds.layers[0].quoted_premium:,.0f}", # Format with comma and no decimals
    technical_premium = f"{hxd.cds.layers[0].technical_premium:,.0f}", # Format with comma and no decimals
    technical_premium_pre_uw_adj = f"{hxd.cds.layers[0].technical_premium_pre_uw_adj:,.0f}" if hxd.cds.standard_fields.is_rater_priced else "N/A", # Format with comma and no decimals
    benchmark_premium = f"{hxd.cds.layers[0].benchmark_premium:,.0f}", # Format with comma and no decimals
    tpi = f"{hxd.cds.layers[0].tpi*100:.1f}%", # Format with comma and no decimals
    tpi_pre_uw_adj = f"{hxd.cds.layers[0].tpi_pre_uw_adj*100:.1f}%" if hxd.cds.standard_fields.is_rater_priced else "N/A", # Format with comma and no decimals
    bpi = f"{hxd.cds.layers[0].bpi*100:,.1f}%", # Format with comma and no decimals
    pflr = f"{hxd.cds.layers[0].pflr*100:,.1f}%", # Format with comma and two decimals
    roc = f"{hxd.cds.layers[0].roc*100:,.1f}%", # Format with comma and two decimals
    uw_adj_impact = f"{hxd.cds.layers[0].uw_adj_impact*100:,.1f}%", # Format with comma and no decimals

    # Industry information
    naics_code = f"{hxd.cds.industry.naics_code}",
    mapped_sic_code = f"{hxd.cds.industry.mapped_sic_code}",
    class_of_business = f"{hxd.cds.industry.class_of_business}",

    # coverage details 
    epl_limit                   = f"{hxd.cds.quote_grid_summary.epl.limit:,.0f}"         if hxd.cds.quote_grid_summary.epl.limit else "N/A",
    epl_retention               = f"{hxd.cds.quote_grid_summary.epl.retention:,.0f}"     if  hxd.cds.quote_grid_summary.epl.retention else "N/A",
    fid_limit                   = f"{hxd.cds.quote_grid_summary.fid.limit:,.0f}"         if hxd.cds.quote_grid_summary.fid.limit else "N/A",
    fid_retention               = f"{hxd.cds.quote_grid_summary.fid.retention:,.0f}"     if hxd.cds.quote_grid_summary.fid.retention else "N/A",
    pcl_limit                   = f"{hxd.cds.quote_grid_summary.pcl.limit:,.0f}"         if hxd.cds.quote_grid_summary.pcl.limit else "N/A",
    pcl_retention               = f"{hxd.cds.quote_grid_summary.pcl.retention:,.0f}"     if hxd.cds.quote_grid_summary.pcl.retention else "N/A",
    
    # rate change
    epl_rc_calculated           = f"{rc.epl.model*100:,.1f}%"          if rc.epl.model not in [None, 0] else "N/A",
    fid_rc_calculated           = f"{rc.fid.model*100:,.1f}%"          if rc.fid.model not in [None, 0] else "N/A" ,
    pcl_rc_calculated           = f"{rc.pcl.model*100:,.1f}%"          if rc.pcl.model not in [None, 0] else "N/A",
    execuguard_rc_calculated    = f"{rc.execuguard.model*100:,.1f}%"   if rc.execuguard.model not in [None, 0] else "N/A",
    epl_rc_uw                   = f"{rc.epl.selected.selected*100:,.1f}%"         if rc.epl.selected.selected not in [None, 0] else "N/A",
    fid_rc_uw                   = f"{rc.fid.selected.selected*100:,.1f}%"         if rc.fid.selected.selected not in [None, 0] else "N/A" ,
    pcl_rc_uw                   = f"{rc.pcl.selected.selected*100:,.1f}%"         if rc.pcl.selected.selected not in [None, 0] else "N/A",
    execuguard_rc_uw            = f"{rc.execuguard.selected.selected*100:,.1f}%"  if rc.execuguard.selected.selected not in [None, 0]  else "N/A",



    rationale_input = html_to_text(hxd.cds.standard_fields.uw_rationale)

    )
    
    #create the document
    with hxd.cds.coverage_options.open("b") as f:
        document.write(f)

@hx.task
def rationale_word_documents_task(hxd, progress):
    #define the path of the document
    template = os.path.join(os.path.dirname(__file__), "documents/rationale_document.docx")
    #create the document
    document = MailMerge(template)

    #merging in the items to match the merge fields in template
    document.merge(
    underwriter_name=f"{hxd.cds.standard_fields.underwriter}",
    insured_name=f"{hxd.cds.standard_fields.insured_name}",
    inception_date=f"{hxd.hx_core.inception_date}",
    expiry_date=f"{hxd.hx_core.expiry_date}",
    rationale_input = f"{hxd.cds.standard_fields.uw_rationale}",   
    
    )
    
    #create the document
    with hxd.cds.rationale_document.open("b") as f:
        document.write(f)        

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "Specialty Risks - US ML Execuguard"
    new_bug_report(hxd, progress, model_name)

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)


@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)


@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)           