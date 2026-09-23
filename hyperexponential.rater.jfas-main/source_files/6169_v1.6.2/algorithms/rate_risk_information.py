import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from operator import itemgetter
import datetime
from dateutil.relativedelta import relativedelta
import requests
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api

def rate_risk_information(hxd):
    cds = hxd.cds
    layer = cds.layers[0]  # SA: It looks like this is only intended to use one layer
    
    # SA: You can just write cds.fa_masking = cds.standard_fields.risk_class == "Fine Art" 
    # because cds.standard_fields.benchmark_class == "Fine Art" will return either True or False
    cds.fa_masking = True if cds.standard_fields.benchmark_class == "Fine Art" else False
    cds.jb_masking = True if cds.standard_fields.benchmark_class == "Jewellers Block" else False
    cds.gs_masking = True if cds.standard_fields.benchmark_class == "General Specie" else False
    cds.cit_masking = True if cds.standard_fields.benchmark_class == "Cash in Transit" else False

    # INSURED NAME
    # SA: None and "" both evaluate to False, so you can just write cds.risk_info.new_replacement if cds.risk_info.new_replacement else else cds.standard_fields.insured_name
    cds.risk_info.insured_name_final = cds.risk_info.new_replacement if cds.risk_info.new_replacement is not None and cds.risk_info.new_replacement != "" else cds.standard_fields.insured_name


    # SUBMISSION DATE
    cds.risk_info.submission_date.calculated = hxd.hx_core.inception_date  

    # POLICY DURATION
    date_diff = (hxd.hx_core.expiry_date - hxd.hx_core.inception_date).days
    leap_day = leap_day_in_duration(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    cds.risk_info.policy_duration.calculated = date_diff / (365 + leap_day)

    # SRCC
    cds.risk_info.srcc_sublimit.calculated = layer.limit


    cds.risk_info.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id or 0
    cds.risk_info.database_id = hx.meta.policy_option_id

    pass





# DATE HELPDER FUNCTIONS
# SA: This function won't count correctly if there's more than one leap day in the period
def leap_day_in_duration(start_date, end_date):
    check_date = start_date
    while check_date <= end_date:
        if last_day_of_month(check_date).day == 29:  # this is true only on leap years in february
            return 1
        
        # SA: Will this only have Feb and Aug? Other dates won't count correctly because they'll miss Feb
        check_date = check_date + relativedelta(months=+6)

    return 0



def last_day_of_month(any_day):
    # The day 28 exists in every month. 4 days later, it's always next month
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    # subtracting the number of the current day brings us back one month
    return next_month - datetime.timedelta(days=next_month.day)



# Async task (triggered by clicking a button) to import data from an expiring policy option into the current policy for rate change and analysis of movement
def expiring_policy_fetch(hxd, progress):
    cds = hxd.cds
    layer = cds.layers[0]
    cov = layer.coverages
    rc = layer.rate_change

    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password

    expiring_policy_option_id = cds.risk_info.expiring_policy_option_id.selected
    # expiring_policy_option_id = 86965  # SA: This is one way of testing, but remember you can also make use of example data! You should really
                                        # set up example data while building a project as it significantly speeds up the testing phase by alerting
                                        # you to mistakes in your logic while you're making them rather than at the end 

    # SA: I've switched this function to the v2 api as I was having problems with the v1 code for some reason
    # Call to API
    v2_api = init_hx_renew_api()
    response = v2_api.snapshots.get_snapshot(expiring_policy_option_id)

    # Error handling based on status code returned by API
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result = response.json()
        data = result["data"]
        
        schedule = pd.DataFrame(data["cds"]["schedule"])
        #setattr(hxd,"schedule",lr_temp_summaries.to_dict("schedule_prior"))
        sel_cols = [col for col in schedule.columns if col not in ["prior_country","prior_currency","prior_region","prior_risk_class","prior_tsi","prior_tsi_cnv","prior_type"]]
        schedule = schedule[sel_cols]
        setattr(cds,"schedule_prior",schedule.to_dict("records"))

        # CLASS SPECIFIC -- Premium
        cov.jb_premises.prem_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["premium"] or 0
        cov.jb_travel.prem_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["premium"] or 0
        cov.jb_additional.prem_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["premium"] or 0

        cov.fa_premises.prem_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["premium"] or 0
        cov.fa_travel.prem_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["premium"] or 0
        cov.fa_additional.prem_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["premium"] or 0

        cov.gs_metals.prem_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["premium"] or 0
        cov.gs_cash.prem_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["premium"] or 0
        cov.gs_securities.prem_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["premium"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            cov.gs_additional.prem_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["premium"]
        except:
            cov.gs_additional.prem_ly = 0

        cov.cit_premises.prem_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["premium"] or 0
        cov.cit_additional.prem_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["premium"] or 0

        # CLASS SPECIFIC -- TSI
        cov.jb_premises.tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["tsi"] or 0
        cov.jb_travel.tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["tsi"] or 0
        cov.jb_additional.tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["tsi"] or 0

        cov.fa_premises.tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["tsi"] or 0
        cov.fa_travel.tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["tsi"] or 0
        cov.fa_additional.tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["tsi"] or 0

        cov.gs_metals.tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["tsi"] or 0
        cov.gs_cash.tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["tsi"] or 0
        cov.gs_securities.tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["tsi"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            cov.gs_additional.tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["tsi"]
        except:
            cov.gs_additional.tsi_ly = 0


        cov.cit_premises.tsi_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["tsi"] or 0
        cov.cit_additional.tsi_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["tsi"] or 0

        # CLASS SPECIFIC -- Model Credit
        cov.jb_premises.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["credit"] or 0
        cov.jb_travel.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["credit"] or 0
        cov.jb_additional.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["credit"] or 0

        cov.fa_premises.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["credit"] or 0
        cov.fa_travel.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["credit"] or 0
        cov.fa_additional.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["credit"] or 0

        cov.gs_metals.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["credit"] or 0
        cov.gs_cash.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["credit"] or 0
        cov.gs_securities.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["credit"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:        
            cov.gs_additional.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["credit"]
        except:
            cov.gs_additional.ded_credit_ly = 0

        cov.cit_premises.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["credit"] or 0
        cov.cit_additional.ded_credit_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["credit"] or 0

        # CLASS SPECIFIC -- uw_adj_impact
        cov.jb_premises.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["uw_adj_impact"] or 0
        cov.jb_travel.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["uw_adj_impact"] or 0
        cov.jb_additional.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["uw_adj_impact"] or 0

        cov.fa_premises.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["uw_adj_impact"] or 0
        cov.fa_travel.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["uw_adj_impact"] or 0
        cov.fa_additional.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["uw_adj_impact"] or 0

        cov.gs_metals.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["uw_adj_impact"] or 0
        cov.gs_cash.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["uw_adj_impact"] or 0
        cov.gs_securities.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["uw_adj_impact"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:      
            cov.gs_additional.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["uw_adj_impact"]
        except:
            cov.gs_additional.uw_adj_impact_ly = 0

        cov.cit_premises.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["uw_adj_impact"] or 0
        cov.cit_additional.uw_adj_impact_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["uw_adj_impact"] or 0

        # CLASS SPECIFIC -- Premium Post Deductible
        cov.jb_premises.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["prem_post_ded"] or 0
        cov.jb_travel.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["prem_post_ded"] or 0
        cov.jb_additional.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["prem_post_ded"] or 0

        cov.fa_premises.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["prem_post_ded"] or 0
        cov.fa_travel.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["prem_post_ded"] or 0
        cov.fa_additional.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["prem_post_ded"] or 0

        cov.gs_metals.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["prem_post_ded"] or 0
        cov.gs_cash.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["prem_post_ded"] or 0
        cov.gs_securities.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["prem_post_ded"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            cov.gs_additional.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["prem_post_ded"] or 0
        except:
            cov.gs_additional.prem_post_ded_ly = 0

        cov.cit_premises.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["prem_post_ded"] or 0
        cov.cit_additional.prem_post_ded_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["prem_post_ded"] or 0


        # EXPERIENCE RATING ------------------------------------------------
        cds.risk_info.policy_reference_exp = data["cds"]["standard_fields"]["policy_reference"]
        cds.experience_rating.expiring_policy_ref = data["cds"]["standard_fields"]["policy_reference"]

        cds.experience_final_selections_model.gn_ulr_expiry = data["cds"]["experience_final_selections_model"]["gn_ulr"] or 0
        cds.experience_final_selections_uw.gn_ulr_expiry = data["cds"]["experience_final_selections_uw"]["gn_ulr"] or 0

        # EXPERIENCE RATING ------------------------------------------------

        # FINAL SELECTIONS AND SUMMARY -------------------------------------


        # FINAL SELECTIONS AND SUMMARY -------------------------------------
        cds.final_claims_summary_table.loss_cost_ly = data["cds"]["final_claims_summary_table"]["final_loss_cost"] or 0

        # FS - Allocated Loss Cost
        cov.jb_premises.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["final_summary_final_loss_cost"] or 0
        cov.jb_travel.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["final_summary_final_loss_cost"] or 0
        cov.jb_additional.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["final_summary_final_loss_cost"] or 0

        cov.fa_premises.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["final_summary_final_loss_cost"] or 0
        cov.fa_travel.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["final_summary_final_loss_cost"] or 0
        cov.fa_additional.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["final_summary_final_loss_cost"] or 0

        cov.gs_metals.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["final_summary_final_loss_cost"] or 0
        cov.gs_cash.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["final_summary_final_loss_cost"] or 0
        cov.gs_securities.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["final_summary_final_loss_cost"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            cov.gs_additional.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["final_summary_final_loss_cost"]
        except:
            cov.gs_additional.final_summary_loss_cost_ly = 0
        

        cov.cit_premises.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["final_summary_final_loss_cost"] or 0
        cov.cit_additional.final_summary_loss_cost_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["final_summary_final_loss_cost"] or 0

        # FS - KPI SUMMARY - Quote Premium Information
        try:
            cds.final_prem_prioryear_table.quoted_premium_slip_curr = data["cds"]["final_premium_summary_table"]["quoted_premium_slip_curr"]
        except:
            cds.final_prem_prioryear_table.quoted_premium_slip_curr = data["cds"]["layers"][0]["quoted_premium"] or 0

        cds.final_prem_prioryear_table.quoted_premium = data["cds"]["layers"][0]["quoted_premium"] or 0
        cds.final_prem_prioryear_table.acq_cost = data["cds"]["final_premium_summary_table"]["acq_cost"] or 0
        cds.final_prem_prioryear_table.signed_line = data["cds"]["final_premium_summary_table"]["signed_line"] or 0
        cds.final_prem_prioryear_table.gg_achieved_rate = data["cds"]["final_premium_summary_table"]["gg_achieved_rate"] or 0
        cds.final_prem_prioryear_table.gn_achieved_rate = data["cds"]["final_premium_summary_table"]["gn_achieved_rate"] or 0

        # FS - KPI SUMMARY - KPI Pre Adj
        cds.final_prem_prioryear_table.tech_prem = data["cds"]["final_premium_summary_table"]["tech_prem"] or 0
        cds.final_prem_prioryear_table.bench_prem = data["cds"]["final_premium_summary_table"]["bench_prem"] or 0
        cds.final_prem_prioryear_table.tpi_pre_uw_adj = data["cds"]["final_premium_summary_table"]["tpi_pre_uw_adj"] or 0
        cds.final_prem_prioryear_table.bpi_pre_uw_adj = data["cds"]["final_premium_summary_table"]["bpi_pre_uw_adj"] or 0
        cds.final_prem_prioryear_table.implied_roc_pre_uw_adj = data["cds"]["final_premium_summary_table"]["implied_roc_pre_uw_adj"] or 0
        cds.final_prem_prioryear_table.expected_profit_pre_uw_adj = data["cds"]["final_premium_summary_table"]["expected_profit_pre_uw_adj"] or 0

        # FS - KPI SUMMARY - Credits
        cds.final_prem_prioryear_table.uw_credit = data["cds"]["final_premium_summary_table"]["uw_credit"] or 0
        cds.final_prem_prioryear_table.client_credit = data["cds"]["final_premium_summary_table"]["client_credit"] or 0
        cds.final_prem_prioryear_table.risk_score_credit = data["cds"]["final_premium_summary_table"]["risk_score_credit"] or 0
        cds.final_prem_prioryear_table.total_credit = data["cds"]["final_premium_summary_table"]["total_credit"] or 0

        # FS - KPI SUMMARY - KPI Post Adj
        cds.final_prem_prioryear_table.tech_prem_adj = data["cds"]["final_premium_summary_table"]["tech_prem_adj"] or 0
        cds.final_prem_prioryear_table.bench_prem_adj = data["cds"]["final_premium_summary_table"]["bench_prem_adj"] or 0
        cds.final_prem_prioryear_table.tpi = data["cds"]["final_premium_summary_table"]["tpi"] or 0
        cds.final_prem_prioryear_table.bpi = data["cds"]["final_premium_summary_table"]["bpi"] or 0
        cds.final_prem_prioryear_table.implied_roc = data["cds"]["final_premium_summary_table"]["implied_roc"] or 0
        cds.final_prem_prioryear_table.expected_profit = data["cds"]["final_premium_summary_table"]["expected_profit"] or 0

        # FS - ACHIEVED RATE ALLOCATION
        cov.jb_premises.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["final_premium_summary_tsi"] or 0
        cov.jb_premises.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["final_premium_summary_tech_rate"] or 0
        cov.jb_premises.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_premises"]["final_premium_summary_ach_rate"] or 0
        cov.jb_travel.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["final_premium_summary_tsi"] or 0
        cov.jb_travel.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["final_premium_summary_tech_rate"] or 0
        cov.jb_travel.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_travel"]["final_premium_summary_ach_rate"] or 0
        cov.jb_additional.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["final_premium_summary_tsi"] or 0
        cov.jb_additional.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["final_premium_summary_tech_rate"] or 0
        cov.jb_additional.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["jb_additional"]["final_premium_summary_ach_rate"] or 0
        
        cov.fa_premises.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["final_premium_summary_tsi"] or 0
        cov.fa_premises.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["final_premium_summary_tech_rate"] or 0
        cov.fa_premises.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_premises"]["final_premium_summary_ach_rate"] or 0
        cov.fa_travel.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["final_premium_summary_tsi"] or 0
        cov.fa_travel.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["final_premium_summary_tech_rate"] or 0
        cov.fa_travel.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_travel"]["final_premium_summary_ach_rate"] or 0
        cov.fa_additional.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["final_premium_summary_tsi"] or 0
        cov.fa_additional.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["final_premium_summary_tech_rate"] or 0
        cov.fa_additional.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["fa_additional"]["final_premium_summary_ach_rate"] or 0

        cov.gs_metals.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["final_premium_summary_tsi"] or 0
        cov.gs_metals.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["final_premium_summary_tech_rate"] or 0
        cov.gs_metals.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_metals"]["final_premium_summary_ach_rate"] or 0
        cov.gs_cash.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["final_premium_summary_tsi"] or 0
        cov.gs_cash.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["final_premium_summary_tech_rate"] or 0
        cov.gs_cash.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_cash"]["final_premium_summary_ach_rate"] or 0
        cov.gs_securities.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["final_premium_summary_tsi"] or 0
        cov.gs_securities.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["final_premium_summary_tech_rate"] or 0
        cov.gs_securities.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_securities"]["final_premium_summary_ach_rate"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            cov.gs_additional.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["final_premium_summary_tsi"]
            cov.gs_additional.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["final_premium_summary_tech_rate"]
            cov.gs_additional.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["gs_additional"]["final_premium_summary_ach_rate"]
        except:
            cov.gs_additional.final_premium_summary_tsi_ly = 0
            cov.gs_additional.final_premium_summary_tech_rate_ly = 0
            cov.gs_additional.final_premium_summary_ach_rate_ly = 0

        cov.cit_premises.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["final_premium_summary_tsi"] or 0
        cov.cit_premises.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["final_premium_summary_tech_rate"] or 0
        cov.cit_premises.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["cit_premises"]["final_premium_summary_ach_rate"] or 0
        cov.cit_additional.final_premium_summary_tsi_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["final_premium_summary_tsi"] or 0
        cov.cit_additional.final_premium_summary_tech_rate_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["final_premium_summary_tech_rate"] or 0
        cov.cit_additional.final_premium_summary_ach_rate_ly = data["cds"]["layers"][0]["coverages"]["cit_additional"]["final_premium_summary_ach_rate"] or 0

        # FS - RATE CHANGE COMPONENTS
        rc.expiry_premium.model_calculated = data["cds"]["final_premium_summary_table"]["quoted_premium"]
        rc.expiry_premium.uw_selected.calculated = data["cds"]["final_premium_summary_table"]["quoted_premium"]
        rc.rate_change_calculated_pryr = data["cds"]["layers"][0]["rate_change"]["rate_change"]["model_calculated"]
        rc.rate_change_uw_selected_pryr = data["cds"]["layers"][0]["rate_change"]["rate_change"]["uw_selected"]

        # UNDERWRITER RATIONALE --------------------------------------------
        cds.rationale.insured_name_expiry = data["cds"]["rationale"]["insured_name"]
        cds.rationale.inception_date_expiry = data["cds"]["rationale"]["inception_date"]
        cds.rationale.pol_ref_expiry = data["cds"]["rationale"]["policy_ref"]
        cds.rationale.coverholder_background_expiry = data["cds"]["rationale"]["coverholder_background"]

        cds.rationale.risk_type_expiry = data["cds"]["rationale"]["risk_type"]
        cds.rationale.construction_expiry = data["cds"]["rationale"]["construction"]
        cds.rationale.signed_line_expiry = data["cds"]["rationale"]["signed_line"]
        cds.rationale.limit_expiry = data["cds"]["rationale"]["limit"]
        cds.rationale.deductions_expiry = data["cds"]["rationale"]["deductions"]
        cds.rationale.avg_limit_expiry = data["cds"]["rationale"]["avg_limit"]
        cds.rationale.top_country_expiry = data["cds"]["rationale"]["top_country"]
        
        cds.rationale.avg_model_rate_expiry = data["cds"]["rationale"]["avg_model_rate"]
        cds.rationale.avg_uw_rate_expiry = data["cds"]["rationale"]["avg_uw_rate"]
        cds.rationale.epi_expiry = data["cds"]["rationale"]["epi"]
        cds.rationale.rate_change_expiry = data["cds"]["rationale"]["rate_change"]
        cds.rationale.attr_lr_expiry = data["cds"]["rationale"]["attr_lr"]
        cds.rationale.cat_load_expiry = data["cds"]["rationale"]["cat_load"]

        cds.rationale.bpi_expiry = data["cds"]["rationale"]["bpi"]
        cds.rationale.tpi_expiry = data["cds"]["rationale"]["tpi"]
        cds.rationale.roc_expiry = data["cds"]["rationale"]["roc"]

        cds.rationale.uw_comments_expiry = data["cds"]["rationale"]["uw_comments"]
        cds.rationale.rate_change_expiry_rationale = data["cds"]["rationale"]["rate_change_rationale"]
        cds.rationale.tnc_change_expiry = data["cds"]["rationale"]["tnc_change"]
        cds.rationale.risk_profile_expiry = data["cds"]["rationale"]["risk_profile"]
        cds.rationale.territory_and_agg_dist_expiry = data["cds"]["rationale"]["territory_and_agg_dist"]
        cds.rationale.exposure_change_expiry = data["cds"]["rationale"]["exposure_change"]
        cds.rationale.large_losses_expiry = data["cds"]["rationale"]["large_losses"]

        # Assign value to written line to align with other raters
        cds.final_prem_prioryear_table.written_line = data["cds"]["final_premium_summary_table"]["signed_line"] or 0
        
        # RATE CHANGE  --------------------------------------------

        rc_temp = data["cds"]["layers"][0]["coverages"]

        # JB - TECHNICAL
        quote_prem = data["cds"]["final_premium_summary_table"]["quoted_premium"] or 0
        total_loss_cost = data["cds"]["final_claims_summary_table"]["final_loss_cost"] or 0

        jb_1_loss = rc_temp["jb_premises"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_jb_1 = quote_prem * (jb_1_loss / total_loss_cost) if total_loss_cost > 0 else 0

        jb_2_loss = rc_temp["jb_travel"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_jb_2 = quote_prem * (jb_2_loss / total_loss_cost) if total_loss_cost > 0 else 0

        jb_3_loss = rc_temp["jb_additional"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_jb_3 = quote_prem * (jb_3_loss / total_loss_cost) if total_loss_cost > 0 else 0

        layer.jb_1_rc_tech.prem_ly = data["cds"]["layers"][0]["jb_1_rc_tech"]["prem_ty"] or allocated_quote_prem_jb_1 or 0
        layer.jb_2_rc_tech.prem_ly = data["cds"]["layers"][0]["jb_2_rc_tech"]["prem_ty"] or allocated_quote_prem_jb_2 or 0
        layer.jb_3_rc_tech.prem_ly = data["cds"]["layers"][0]["jb_3_rc_tech"]["prem_ty"] or allocated_quote_prem_jb_3 or 0

        layer.jb_1_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["jb_1_rc_tech"]["prem_exp_ty"] or rc_temp["jb_premises"]["premium"] or 0
        layer.jb_2_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["jb_2_rc_tech"]["prem_exp_ty"] or rc_temp["jb_travel"]["premium"] or 0
        layer.jb_3_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["jb_3_rc_tech"]["prem_exp_ty"] or rc_temp["jb_additional"]["premium"] or 0

        jb_1_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["jb_premises"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["jb_premises"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["jb_premises"]["credit"]
        jb_2_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["jb_travel"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["jb_travel"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["jb_travel"]["credit"]
        jb_3_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["jb_additional"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["jb_additional"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["jb_additional"]["credit"]

        layer.jb_1_rc_tech.prem_ded_ly = jb_1_selected_credit_tech or 0.0
        layer.jb_2_rc_tech.prem_ded_ly = jb_2_selected_credit_tech or 0.0
        layer.jb_3_rc_tech.prem_ded_ly = jb_3_selected_credit_tech or 0.0

        layer.jb_1_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["jb_1_rc_tech"]["prem_lim_ty"] or 0
        layer.jb_2_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["jb_2_rc_tech"]["prem_lim_ty"] or 0
        layer.jb_3_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["jb_3_rc_tech"]["prem_lim_ty"] or 0

        layer.jb_1_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["jb_1_rc_tech"]["prem_tc_ty"] or 0
        layer.jb_2_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["jb_2_rc_tech"]["prem_tc_ty"] or 0
        layer.jb_3_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["jb_3_rc_tech"]["prem_tc_ty"] or 0

        # JB - UW ADJUSTED
        layer.jb_1_rc_uwadj.prem_ly = data["cds"]["layers"][0]["jb_1_rc_uwadj"]["prem_ty"] or allocated_quote_prem_jb_1 or 0
        layer.jb_2_rc_uwadj.prem_ly = data["cds"]["layers"][0]["jb_2_rc_uwadj"]["prem_ty"] or allocated_quote_prem_jb_2 or 0
        layer.jb_3_rc_uwadj.prem_ly = data["cds"]["layers"][0]["jb_3_rc_uwadj"]["prem_ty"] or allocated_quote_prem_jb_3 or 0

        layer.jb_1_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["jb_1_rc_uwadj"]["prem_exp_ty"] or rc_temp["jb_premises"]["premium"] or 0
        layer.jb_2_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["jb_2_rc_uwadj"]["prem_exp_ty"] or rc_temp["jb_travel"]["premium"] or 0
        layer.jb_3_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["jb_3_rc_uwadj"]["prem_exp_ty"] or rc_temp["jb_additional"]["premium"] or 0

        layer.jb_1_rc_uwadj.prem_ded_ly = jb_1_selected_credit_tech or 0.0
        layer.jb_2_rc_uwadj.prem_ded_ly = jb_2_selected_credit_tech or 0.0
        layer.jb_3_rc_uwadj.prem_ded_ly = jb_3_selected_credit_tech or 0.0

        layer.jb_1_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["jb_1_rc_uwadj"]["prem_lim_ty"] or 0
        layer.jb_2_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["jb_2_rc_uwadj"]["prem_lim_ty"] or 0
        layer.jb_3_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["jb_3_rc_uwadj"]["prem_lim_ty"] or 0

        layer.jb_1_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["jb_1_rc_uwadj"]["prem_tc_ty"] or 0
        layer.jb_2_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["jb_2_rc_uwadj"]["prem_tc_ty"] or 0
        layer.jb_3_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["jb_3_rc_uwadj"]["prem_tc_ty"] or 0

        # FA - TECHNICAL
        fa_1_loss = rc_temp["fa_premises"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_fa_1 = quote_prem * (fa_1_loss / total_loss_cost) if total_loss_cost > 0 else 0

        fa_2_loss = rc_temp["fa_travel"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_fa_2 = quote_prem * (fa_2_loss / total_loss_cost) if total_loss_cost > 0 else 0

        fa_3_loss = rc_temp["fa_additional"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_fa_3 = quote_prem * (fa_3_loss / total_loss_cost) if total_loss_cost > 0 else 0

        layer.fa_1_rc_tech.prem_ly = data["cds"]["layers"][0]["fa_1_rc_tech"]["prem_ty"] or allocated_quote_prem_fa_1 or 0
        layer.fa_2_rc_tech.prem_ly = data["cds"]["layers"][0]["fa_2_rc_tech"]["prem_ty"] or allocated_quote_prem_fa_2 or 0
        layer.fa_3_rc_tech.prem_ly = data["cds"]["layers"][0]["fa_3_rc_tech"]["prem_ty"] or allocated_quote_prem_fa_3 or 0

        layer.fa_1_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["fa_1_rc_tech"]["prem_exp_ty"] or rc_temp["fa_premises"]["premium"] or 0
        layer.fa_2_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["fa_2_rc_tech"]["prem_exp_ty"] or rc_temp["fa_travel"]["premium"] or 0
        layer.fa_3_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["fa_3_rc_tech"]["prem_exp_ty"] or rc_temp["fa_additional"]["premium"] or 0

        fa_1_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["fa_premises"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["fa_premises"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["fa_premises"]["credit"]
        fa_2_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["fa_travel"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["fa_travel"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["fa_travel"]["credit"]
        fa_3_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["fa_additional"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["fa_additional"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["fa_additional"]["credit"]

        layer.fa_1_rc_tech.prem_ded_ly = fa_1_selected_credit_tech or 0.0
        layer.fa_2_rc_tech.prem_ded_ly = fa_2_selected_credit_tech or 0.0
        layer.fa_3_rc_tech.prem_ded_ly = fa_3_selected_credit_tech or 0.0

        layer.fa_1_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["fa_1_rc_tech"]["prem_lim_ty"] or 0
        layer.fa_2_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["fa_2_rc_tech"]["prem_lim_ty"] or 0
        layer.fa_3_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["fa_3_rc_tech"]["prem_lim_ty"] or 0

        layer.fa_1_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["fa_1_rc_tech"]["prem_tc_ty"] or 0
        layer.fa_2_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["fa_2_rc_tech"]["prem_tc_ty"] or 0
        layer.fa_3_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["fa_3_rc_tech"]["prem_tc_ty"] or 0

        # FA - UW ADJUSTED
        layer.fa_1_rc_uwadj.prem_ly = data["cds"]["layers"][0]["fa_1_rc_uwadj"]["prem_ty"] or allocated_quote_prem_fa_1 or 0
        layer.fa_2_rc_uwadj.prem_ly = data["cds"]["layers"][0]["fa_2_rc_uwadj"]["prem_ty"] or allocated_quote_prem_fa_2 or 0
        layer.fa_3_rc_uwadj.prem_ly = data["cds"]["layers"][0]["fa_3_rc_uwadj"]["prem_ty"] or allocated_quote_prem_fa_3 or 0

        layer.fa_1_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["fa_1_rc_uwadj"]["prem_exp_ty"] or rc_temp["fa_premises"]["premium"] or 0
        layer.fa_2_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["fa_2_rc_uwadj"]["prem_exp_ty"] or rc_temp["fa_travel"]["premium"] or 0
        layer.fa_3_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["fa_3_rc_uwadj"]["prem_exp_ty"] or rc_temp["fa_additional"]["premium"] or 0

        layer.fa_1_rc_uwadj.prem_ded_ly = fa_1_selected_credit_tech or 0.0
        layer.fa_2_rc_uwadj.prem_ded_ly = fa_2_selected_credit_tech or 0.0
        layer.fa_3_rc_uwadj.prem_ded_ly = fa_3_selected_credit_tech or 0.0

        layer.fa_1_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["fa_1_rc_uwadj"]["prem_lim_ty"] or 0
        layer.fa_2_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["fa_2_rc_uwadj"]["prem_lim_ty"] or 0
        layer.fa_3_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["fa_3_rc_uwadj"]["prem_lim_ty"] or 0

        layer.fa_1_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["fa_1_rc_uwadj"]["prem_tc_ty"] or 0
        layer.fa_2_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["fa_2_rc_uwadj"]["prem_tc_ty"] or 0
        layer.fa_3_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["fa_3_rc_uwadj"]["prem_tc_ty"] or 0

        # GS - TECHNICAL
        gs_1_loss = rc_temp["gs_metals"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_gs_1 = quote_prem * (gs_1_loss / total_loss_cost) if total_loss_cost > 0 else 0

        gs_2_loss = rc_temp["gs_cash"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_gs_2 = quote_prem * (gs_2_loss / total_loss_cost) if total_loss_cost > 0 else 0

        gs_3_loss = rc_temp["gs_securities"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_gs_3 = quote_prem * (gs_3_loss / total_loss_cost) if total_loss_cost > 0 else 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch
        try:
            gs_4_loss = rc_temp["gs_additional"]["final_summary_final_loss_cost"]
            allocated_quote_prem_gs_4 = quote_prem * (gs_4_loss / total_loss_cost) if total_loss_cost > 0 else 0
        except:
            gs_4_loss = 0
            allocated_quote_prem_gs_4 = 0
        

        layer.gs_1_rc_tech.prem_ly = data["cds"]["layers"][0]["gs_1_rc_tech"]["prem_ty"] or allocated_quote_prem_gs_1 or 0
        layer.gs_2_rc_tech.prem_ly = data["cds"]["layers"][0]["gs_2_rc_tech"]["prem_ty"] or allocated_quote_prem_gs_2 or 0
        layer.gs_3_rc_tech.prem_ly = data["cds"]["layers"][0]["gs_3_rc_tech"]["prem_ty"] or allocated_quote_prem_gs_3 or 0
        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch        
        try:
            layer.gs_4_rc_tech.prem_ly = data["cds"]["layers"][0]["gs_4_rc_tech"]["prem_ty"] or allocated_quote_prem_gs_4
        except:
            layer.gs_4_rc_tech.prem_ly = allocated_quote_prem_gs_4

        layer.gs_1_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["gs_1_rc_tech"]["prem_exp_ty"] or rc_temp["gs_metals"]["premium"] or 0
        layer.gs_2_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["gs_2_rc_tech"]["prem_exp_ty"] or rc_temp["gs_cash"]["premium"] or 0
        layer.gs_3_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["gs_3_rc_tech"]["prem_exp_ty"] or rc_temp["gs_securities"]["premium"] or 0        
        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch        
        try:
            layer.gs_4_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["gs_4_rc_tech"]["prem_exp_ty"] or rc_temp["gs_additional"]["premium"] or 0
        except:
            layer.gs_4_rc_tech.prem_exp_ly = 0

        gs_1_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["gs_metals"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["gs_metals"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["gs_metals"]["credit"]
        gs_2_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["gs_cash"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["gs_cash"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["gs_cash"]["credit"]
        gs_3_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["gs_securities"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["gs_securities"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["gs_securities"]["credit"]
        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:
            gs_4_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["gs_additional"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["gs_additional"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["gs_additional"]["credit"]
        except:
            gs_4_selected_credit_tech = 0                


        layer.gs_1_rc_tech.prem_ded_ly = gs_1_selected_credit_tech or 0.0
        layer.gs_2_rc_tech.prem_ded_ly = gs_2_selected_credit_tech or 0.0
        layer.gs_3_rc_tech.prem_ded_ly = gs_3_selected_credit_tech or 0.0
        layer.gs_4_rc_tech.prem_ded_ly = gs_4_selected_credit_tech or 0.0

        layer.gs_1_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["gs_1_rc_tech"]["prem_lim_ty"] or 0
        layer.gs_2_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["gs_2_rc_tech"]["prem_lim_ty"] or 0
        layer.gs_3_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["gs_3_rc_tech"]["prem_lim_ty"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:
            layer.gs_4_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["gs_4_rc_tech"]["prem_lim_ty"]
        except:
            layer.gs_4_rc_tech.prem_lim_ly = 0

        layer.gs_1_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["gs_1_rc_tech"]["prem_tc_ty"] or 0
        layer.gs_2_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["gs_2_rc_tech"]["prem_tc_ty"] or 0
        layer.gs_3_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["gs_3_rc_tech"]["prem_tc_ty"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:
            layer.gs_4_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["gs_4_rc_tech"]["prem_tc_ty"]
        except:
            layer.gs_4_rc_tech.prem_tc_ly = 0


        # GS - UW ADJUSTED
        layer.gs_1_rc_uwadj.prem_ly = data["cds"]["layers"][0]["gs_1_rc_uwadj"]["prem_ty"] or allocated_quote_prem_gs_1 or 0
        layer.gs_2_rc_uwadj.prem_ly = data["cds"]["layers"][0]["gs_2_rc_uwadj"]["prem_ty"] or allocated_quote_prem_gs_2 or 0
        layer.gs_3_rc_uwadj.prem_ly = data["cds"]["layers"][0]["gs_3_rc_uwadj"]["prem_ty"] or allocated_quote_prem_gs_3 or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:
            layer.gs_4_rc_uwadj.prem_ly = data["cds"]["layers"][0]["gs_4_rc_uwadj"]["prem_ty"]
        except:
            layer.gs_4_rc_uwadj.prem_ly = allocated_quote_prem_gs_4 or 0


        layer.gs_1_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["gs_1_rc_uwadj"]["prem_exp_ty"] or rc_temp["gs_metals"]["premium"] or 0
        layer.gs_2_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["gs_2_rc_uwadj"]["prem_exp_ty"] or rc_temp["gs_cash"]["premium"] or 0
        layer.gs_3_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["gs_3_rc_uwadj"]["prem_exp_ty"] or rc_temp["gs_securities"]["premium"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:            
            layer.gs_4_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["gs_4_rc_uwadj"]["prem_exp_ty"] or rc_temp["gs_additional"]["premium"]
        except:
            layer.gs_4_rc_uwadj.prem_exp_ly = 0

        layer.gs_1_rc_uwadj.prem_ded_ly = gs_1_selected_credit_tech or 0.0
        layer.gs_2_rc_uwadj.prem_ded_ly = gs_2_selected_credit_tech or 0.0
        layer.gs_3_rc_uwadj.prem_ded_ly = gs_3_selected_credit_tech or 0.0
        layer.gs_4_rc_uwadj.prem_ded_ly = gs_4_selected_credit_tech or 0.0

        layer.gs_1_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["gs_1_rc_uwadj"]["prem_lim_ty"] or 0
        layer.gs_2_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["gs_2_rc_uwadj"]["prem_lim_ty"] or 0
        layer.gs_3_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["gs_3_rc_uwadj"]["prem_lim_ty"] or 0
        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:   
            layer.gs_4_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["gs_4_rc_uwadj"]["prem_lim_ty"]
        except:
            layer.gs_4_rc_uwadj.prem_lim_ly = 0

        layer.gs_1_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["gs_1_rc_uwadj"]["prem_tc_ty"] or 0
        layer.gs_2_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["gs_2_rc_uwadj"]["prem_tc_ty"] or 0
        layer.gs_3_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["gs_3_rc_uwadj"]["prem_tc_ty"] or 0

        # gs_additional added beginning of 2025, so in inputs layer model, there wouldn't have been this node. Therefore need to add a catch 
        try:   
            layer.gs_4_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["gs_4_rc_uwadj"]["prem_tc_ty"]
        except:
            layer.gs_4_rc_uwadj.prem_tc_ly = 0

        # CIT - TECHNICAL
        cit_1_loss = rc_temp["cit_premises"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_cit_1 = quote_prem * (cit_1_loss / total_loss_cost) if total_loss_cost > 0 else 0

        cit_2_loss = rc_temp["cit_additional"]["final_summary_final_loss_cost"] or 0
        allocated_quote_prem_cit_2 = quote_prem * (cit_2_loss / total_loss_cost) if total_loss_cost > 0 else 0

        layer.cit_1_rc_tech.prem_ly = data["cds"]["layers"][0]["cit_1_rc_tech"]["prem_ty"] or allocated_quote_prem_cit_1 or 0
        layer.cit_2_rc_tech.prem_ly = data["cds"]["layers"][0]["cit_2_rc_tech"]["prem_ty"] or allocated_quote_prem_cit_2 or 0
        layer.cit_3_rc_tech.prem_ly = data["cds"]["layers"][0]["cit_3_rc_tech"]["prem_ty"] or 0


        layer.cit_1_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["cit_1_rc_tech"]["prem_exp_ty"] or rc_temp["cit_premises"]["premium"] or 0
        layer.cit_2_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["cit_2_rc_tech"]["prem_exp_ty"] or rc_temp["cit_additional"]["premium"] or 0
        layer.cit_3_rc_tech.prem_exp_ly = data["cds"]["layers"][0]["cit_3_rc_tech"]["prem_exp_ty"] or 0 

        cit_1_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["cit_premises"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["cit_premises"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["cit_premises"]["credit"]
        cit_2_selected_credit_tech = data["cds"]["layers"][0]["coverages"]["cit_additional"]["uw_adj_impact"] if data["cds"]["layers"][0]["coverages"]["cit_additional"]["uw_adj_impact"] is not None else data["cds"]["layers"][0]["coverages"]["cit_additional"]["credit"]
        cit_3_selected_credit_tech = 0.0

        layer.cit_1_rc_tech.prem_ded_ly = cit_1_selected_credit_tech or 0.0
        layer.cit_2_rc_tech.prem_ded_ly = cit_2_selected_credit_tech or 0.0
        layer.cit_3_rc_tech.prem_ded_ly = cit_3_selected_credit_tech or 0.0

        layer.cit_1_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["cit_1_rc_tech"]["prem_lim_ty"] or 0
        layer.cit_2_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["cit_2_rc_tech"]["prem_lim_ty"] or 0
        layer.cit_3_rc_tech.prem_lim_ly = data["cds"]["layers"][0]["cit_3_rc_tech"]["prem_lim_ty"] or 0

        layer.cit_1_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["cit_1_rc_tech"]["prem_tc_ty"] or 0
        layer.cit_2_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["cit_2_rc_tech"]["prem_tc_ty"] or 0
        layer.cit_3_rc_tech.prem_tc_ly = data["cds"]["layers"][0]["cit_3_rc_tech"]["prem_tc_ty"] or 0

        # CIT - UW ADJUSTED
        layer.cit_1_rc_uwadj.prem_ly = data["cds"]["layers"][0]["cit_1_rc_uwadj"]["prem_ty"] or allocated_quote_prem_cit_1 or 0
        layer.cit_2_rc_uwadj.prem_ly = data["cds"]["layers"][0]["cit_2_rc_uwadj"]["prem_ty"] or allocated_quote_prem_cit_2 or 0
        layer.cit_3_rc_uwadj.prem_ly = data["cds"]["layers"][0]["cit_3_rc_uwadj"]["prem_ty"] or 0

        layer.cit_1_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["cit_1_rc_uwadj"]["prem_exp_ty"] or rc_temp["cit_premises"]["premium"] or 0
        layer.cit_2_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["cit_2_rc_uwadj"]["prem_exp_ty"] or rc_temp["cit_additional"]["premium"] or 0
        layer.cit_3_rc_uwadj.prem_exp_ly = data["cds"]["layers"][0]["cit_3_rc_uwadj"]["prem_exp_ty"] or 0

        layer.cit_1_rc_uwadj.prem_ded_ly = cit_1_selected_credit_tech or 0.0
        layer.cit_2_rc_uwadj.prem_ded_ly = cit_2_selected_credit_tech or 0.0
        layer.cit_3_rc_uwadj.prem_ded_ly = cit_3_selected_credit_tech or 0.0

        layer.cit_1_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["cit_1_rc_uwadj"]["prem_lim_ty"] or 0
        layer.cit_2_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["cit_2_rc_uwadj"]["prem_lim_ty"] or 0
        layer.cit_3_rc_uwadj.prem_lim_ly = data["cds"]["layers"][0]["cit_3_rc_uwadj"]["prem_lim_ty"] or 0

        layer.cit_1_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["cit_1_rc_uwadj"]["prem_tc_ty"] or 0
        layer.cit_2_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["cit_2_rc_uwadj"]["prem_tc_ty"] or 0
        layer.cit_3_rc_uwadj.prem_tc_ly = data["cds"]["layers"][0]["cit_3_rc_uwadj"]["prem_tc_ty"] or 0

        # SA: These assigns are all written out and you could probably save some lines using loops, however there's
        # an argument for having the explicitness of having it all written out

    # SA: When the IF part of an if statement is this long, it's unclear what if statement this 
    # else is referring to. I often like to put this short else condition at the top (i.e. make
    # the if statement if not response.ok )
    # Raises error if status code is not 200
    else:
        try:
            response_json = response.json()
            error = f"Error: {response_json.get('title')}"
            error += f"\nDetail: {response_json.get('detail')}" if response_json.get("detail") else ""
            hx.errors.fatal(error)
        except:
            hx.errors.fatal(f"Error: {response.text}")
