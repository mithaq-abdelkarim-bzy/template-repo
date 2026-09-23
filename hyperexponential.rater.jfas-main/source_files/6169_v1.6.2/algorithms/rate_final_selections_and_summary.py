import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from algorithms.rate_z_utilities import ratio
from operator import itemgetter

def rate_final_selections_and_summary(hxd,df):
    cds = hxd.cds
    layer = cds.layers[0]
    cov = layer.coverages

    # Policy Information ~~~

    cds.final_selection.policy_ref = cds.standard_fields.policy_reference
    cds.final_selection.start_date = hxd.hx_core.inception_date
    cds.final_selection.end_date = hxd.hx_core.expiry_date
    cds.final_selection.policy_class = cds.standard_fields.benchmark_class
    cds.final_selection.currency = cds.currencies.source_currency

    # Rater Selected
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # Claims Summary ~~~
    if len(hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]) > 0:
        risk_class_code = hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]["tag"].iloc[0]
    else:
        risk_class_code = ""

    # Risk Quality Scoring ~~~
    if risk_class_code == "JB":
        jb_final_selection_df = utils.pd_df_from_hx_list(layer.jb_final_selection)
        jb_final_selection_df.index.names = [''] # Remove index name so that reset_index() work below

        high_level = jb_final_selection_df[[col for col in jb_final_selection_df.columns if "high_level" in col]]
        high_level = high_level.T
        high_level.columns = ["response"]
        high_level.index.name = "question"
        high_level = high_level.reset_index()
        high_level = high_level.assign(question = lambda x: x.question.str.replace("high_level_",""))

        specific = jb_final_selection_df[[col for col in jb_final_selection_df.columns if "specific" in col]]
        specific = specific.T
        specific.columns = ["response"]
        specific.index.name = "question"
        specific = specific.reset_index()
        specific = specific.assign(response2 = lambda x: np.where((x.response == "Low") | (x.response == "Medium") | (x.response == False) | (x.response == "Long Term"), 0,1 ))
        specific = specific.assign(question = lambda x: x.question.str.replace("specific_",""))


        high_level_score = hx.params.table_input_risk_quality_jb_high_level
        specific_score = hx.params.table_input_risk_quality_jb_specific

        high_level = pd.merge(high_level,high_level_score,how="left")
        specific = pd.merge(specific,specific_score,how="left")

        high_level_temp = (high_level["score"] * high_level["response"]).sum()
        specific_temp = (specific["score"] * specific["response2"]).sum()

        temp = (high_level_temp + specific_temp) * 100 / (high_level["score"].sum() + specific["score"].sum()) 

        cds.final_selection.quality_score = round(temp) if not np.isnan(temp) else 0

    if risk_class_code == "CIT":
        cit_final_selection_df = utils.pd_df_from_hx_list(layer.cit_final_selection)
        cit_final_selection_df.index.names = [''] # Remove index name so that reset_index() work below

        high_level = cit_final_selection_df[[col for col in cit_final_selection_df.columns if "high_level" in col]]
        high_level = high_level.T
        high_level.columns = ["response"]
        high_level.index.name = "question"
        high_level = high_level.reset_index()
        high_level = high_level.assign(question = lambda x: x.question.str.replace("high_level_",""))

        specific = cit_final_selection_df[[col for col in cit_final_selection_df.columns if "specific" in col]]
        specific = specific.T
        specific.columns = ["response"]
        specific.index.name = "question"
        specific = specific.reset_index()
        specific = specific.assign(response2 = lambda x: np.where((x.response == "Low") | (x.response == "Medium") | (x.response == False) | (x.response == "Long Term"), 0,1 ))
        specific = specific.assign(question = lambda x: x.question.str.replace("specific_",""))

        high_level_score = hx.params.table_input_risk_quality_cit_high_level
        specific_score = hx.params.table_input_risk_quality_cit_specific

        high_level = pd.merge(high_level,high_level_score,how="left")
        specific = pd.merge(specific,specific_score,how="left")

        high_level_temp = (high_level["score"] * high_level["response"]).sum()
        specific_temp = (specific["score"] * specific["response2"]).sum()

        temp = (high_level_temp + specific_temp) * 100 / (high_level["score"].sum() + specific["score"].sum()) 

        cds.final_selection.quality_score = round(temp) if not np.isnan(temp) else 0



    # tech params
    table_rating_tech_params = hx.params.table_rating_technical_parameters

    # currency rate
    fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.final_selection.currency]["fx_rate"].iloc[0]

    if risk_class_code != "":
        direct = table_rating_tech_params[table_rating_tech_params["Category"] == "Direct"][risk_class_code].iloc[0]
        indirect = table_rating_tech_params[table_rating_tech_params["Category"] == "Indirect"][risk_class_code].iloc[0]
        lae = table_rating_tech_params[table_rating_tech_params["Category"] == "LAE"][risk_class_code].iloc[0]
        group_cat_risk = table_rating_tech_params[table_rating_tech_params["Category"] == "Group Cat Risk"][risk_class_code].iloc[0]
        net_group_cat_risk = table_rating_tech_params[table_rating_tech_params["Category"] == "Net Group Cat Risk"][risk_class_code].iloc[0]
        held_capital = table_rating_tech_params[table_rating_tech_params["Category"] == "Held Capital"][risk_class_code].iloc[0]
        add_cat_risk = table_rating_tech_params[table_rating_tech_params["Category"] == "Add Cat Risk"][risk_class_code].iloc[0]
        cor_cap_req = table_rating_tech_params[table_rating_tech_params["Category"] == "Cor Cap Req"][risk_class_code].iloc[0]
        cap_allocation = table_rating_tech_params[table_rating_tech_params["Category"] == "Cap Allocation"][risk_class_code].iloc[0]
        reinsurance = table_rating_tech_params[table_rating_tech_params["Category"] == "Reinsurance"][risk_class_code].iloc[0]
        perc_cat = table_rating_tech_params[table_rating_tech_params["Category"] == "% Cat"][risk_class_code].iloc[0]
        acq_costs = table_rating_tech_params[table_rating_tech_params["Category"] == "AcqCosts"][risk_class_code].iloc[0]
        lr = table_rating_tech_params[table_rating_tech_params["Category"] == "LR"][risk_class_code].iloc[0]
        coc = table_rating_tech_params[table_rating_tech_params["Category"] == "CoC"][risk_class_code].iloc[0]
        investment_income = table_rating_tech_params[table_rating_tech_params["Category"] == "Investment Income"][risk_class_code].iloc[0]
        # nmp_adj = table_rating_tech_paraimage.pngms[table_rating_tech_params["Category"] == "NMP Adjustment"][risk_class_code].iloc[0]

        ## calc tsi and prem post ded for classes, assign to nodes   #surely a way shorter way to do this! :)
        cov.jb_premises.final_summary_tsi = cov.jb_premises.tsi
        cov.jb_premises.final_summary_prem_post_ded = cov.jb_premises.prem_post_ded if cov.jb_premises.prem_post_ded is not None and cov.jb_premises.prem_post_ded > 0 else 0
        cov.jb_travel.final_summary_tsi = cov.jb_travel.tsi
        cov.jb_travel.final_summary_prem_post_ded = cov.jb_travel.prem_post_ded if cov.jb_travel.prem_post_ded is not None and cov.jb_travel.prem_post_ded > 0 else 0
        cov.jb_additional.final_summary_tsi = cov.jb_additional.tsi
        cov.jb_additional.final_summary_prem_post_ded = cov.jb_additional.prem_post_ded if cov.jb_additional.prem_post_ded is not None and cov.jb_additional.prem_post_ded > 0 else 0

        cov.fa_premises.final_summary_tsi = cov.fa_premises.tsi
        cov.fa_premises.final_summary_prem_post_ded = cov.fa_premises.prem_post_ded if cov.fa_premises.prem_post_ded is not None and cov.fa_premises.prem_post_ded > 0 else 0
        cov.fa_travel.final_summary_tsi = cov.fa_travel.tsi
        cov.fa_travel.final_summary_prem_post_ded = cov.fa_travel.prem_post_ded if cov.fa_travel.prem_post_ded is not None and cov.fa_travel.prem_post_ded > 0 else 0
        cov.fa_additional.final_summary_tsi = cov.fa_additional.tsi
        cov.fa_additional.final_summary_prem_post_ded = cov.fa_additional.prem_post_ded if cov.fa_additional.prem_post_ded is not None and cov.fa_additional.prem_post_ded > 0 else 0

        cov.gs_metals.final_summary_tsi = cov.gs_metals.tsi
        cov.gs_metals.final_summary_prem_post_ded = cov.gs_metals.prem_post_ded if cov.gs_metals.prem_post_ded is not None and cov.gs_metals.prem_post_ded > 0 else 0
        cov.gs_cash.final_summary_tsi = cov.gs_cash.tsi
        cov.gs_cash.final_summary_prem_post_ded = cov.gs_cash.prem_post_ded if cov.gs_cash.prem_post_ded is not None and cov.gs_cash.prem_post_ded > 0 else 0
        cov.gs_securities.final_summary_tsi = cov.gs_securities.tsi
        cov.gs_securities.final_summary_prem_post_ded = cov.gs_securities.prem_post_ded if cov.gs_securities.prem_post_ded is not None and cov.gs_securities.prem_post_ded > 0 else 0
        cov.gs_additional.final_summary_tsi = cov.gs_additional.tsi
        cov.gs_additional.final_summary_prem_post_ded = cov.gs_additional.prem_post_ded if cov.gs_additional.prem_post_ded is not None and cov.gs_additional.prem_post_ded > 0 else 0

        cov.cit_premises.final_summary_tsi = cov.cit_premises.tsi
        cov.cit_premises.final_summary_prem_post_ded = cov.cit_premises.prem_post_ded if cov.cit_premises.prem_post_ded is not None and cov.cit_premises.prem_post_ded > 0 else 0
        cov.cit_additional.final_summary_tsi = cov.cit_additional.tsi
        cov.cit_additional.final_summary_prem_post_ded = cov.cit_additional.prem_post_ded if cov.cit_additional.prem_post_ded is not None and cov.cit_additional.prem_post_ded > 0 else 0


        ## calc bespoke total prem post ded and tsi by class, assign to nodes
        if risk_class_code == "JB":
            cds.final_claims_summary_table.exp_prem_post_ded = (cov.jb_premises.prem_post_ded or 0) + (cov.jb_travel.prem_post_ded or 0) + (cov.jb_additional.prem_post_ded or 0)
            cds.final_claims_summary_table.tsi =  (cov.jb_premises.tsi or 0) + (cov.jb_travel.tsi or 0) + (cov.jb_additional.tsi or 0)
        if risk_class_code == "FA":
            cds.final_claims_summary_table.exp_prem_post_ded = (cov.fa_premises.prem_post_ded or 0) + (cov.fa_travel.prem_post_ded or 0) + (cov.fa_additional.prem_post_ded or 0)
            cds.final_claims_summary_table.tsi = (cov.fa_premises.tsi or 0) + (cov.fa_travel.tsi or 0) + (cov.fa_additional.tsi or 0)  
        if risk_class_code == "GS":
            cds.final_claims_summary_table.exp_prem_post_ded = (cov.gs_metals.prem_post_ded or 0) + (cov.gs_cash.prem_post_ded or 0) + (cov.gs_securities.prem_post_ded or 0) + (cov.gs_additional.prem_post_ded or 0)
            cds.final_claims_summary_table.tsi = (cov.gs_metals.tsi or 0) + (cov.gs_cash.tsi or 0) + (cov.gs_securities.tsi or 0) + + (cov.gs_additional.tsi or 0)
        if risk_class_code == "CIT":
            cds.final_claims_summary_table.exp_prem_post_ded = (cov.cit_premises.prem_post_ded or 0) + (cov.cit_additional.prem_post_ded or 0)
            cds.final_claims_summary_table.tsi = (cov.cit_premises.tsi or 0) + (cov.cit_additional.tsi or 0)
        
        ## assign comms and lr to nodes
        cds.final_claims_summary_table.assumed_comms = acq_costs
        cds.final_claims_summary_table.assumed_lr_gn = lr


        # exposure_loss_cost_length_adj = cds.final_claims_summary_table.exp_prem_post_ded * (1-acq_costs) * lr * (hxd.final_end_date-hxd.final_start_date).days / 365
        exposure_loss_cost_length_adj = cds.final_claims_summary_table.exp_prem_post_ded * (1-acq_costs) * lr * cds.risk_info.policy_duration.selected # DL EDIT -- to be consistent with risk info    
        cds.final_claims_summary_table.exposure_loss_cost_length_adj = exposure_loss_cost_length_adj
        cds.final_claims_summary_table.experience_loss_cost_length_adj = cds.experience_final_selections_model.ly_prem * (cds.experience_final_selections_uw.gn_ulr if cds.experience_final_selections_uw.gn_ulr > 0 else cds.experience_final_selections_model.gn_ulr)

        cds.final_claims_summary_table.rec_exp_weight = cds.experience_final_selections_model.exp_weight

        ## calculate NMP impact
        # nmp_impact = nmp_adj / (lr - nmp_adj) # NMP impact on EL

        ## final loss cost: total and by type for each class
        # final_loss_cost = (cds.final_claims_summary_table.experience_loss_cost_length_adj * cds.final_claims_summary_table.sel_exp_weight + exposure_loss_cost_length_adj * (1-cds.final_claims_summary_table.sel_exp_weight)) * (1 + nmp_impact) # including NMP load
        final_loss_cost = (cds.final_claims_summary_table.experience_loss_cost_length_adj * cds.final_claims_summary_table.sel_exp_weight + exposure_loss_cost_length_adj * (1-cds.final_claims_summary_table.sel_exp_weight)) 
        cds.final_claims_summary_table.final_loss_cost = final_loss_cost

        if risk_class_code == "JB":
            # SA: These bits of repeated code are great candidates for helper functions! Or you could use getattr and setattr instead of the if statements as the nodes follow a logical name structure 
            cov.jb_premises.final_summary_final_loss_cost = final_loss_cost*(cov.jb_premises.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.jb_travel.final_summary_final_loss_cost = final_loss_cost*(cov.jb_travel.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.jb_additional.final_summary_final_loss_cost = final_loss_cost*(cov.jb_additional.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0

            # cov.final_jb_premises_summary.final_loss_cost = final_loss_cost * (cov.final_jb_premises_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_jb_travel_summary.final_loss_cost = final_loss_cost * (cov.final_jb_travel_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_jb_additional_summary.final_loss_cost = final_loss_cost * (cov.final_jb_additional_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0

        if risk_class_code == "FA":
            cov.fa_premises.final_summary_final_loss_cost = final_loss_cost*(cov.fa_premises.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.fa_travel.final_summary_final_loss_cost = final_loss_cost*(cov.fa_travel.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.fa_additional.final_summary_final_loss_cost = final_loss_cost*(cov.fa_additional.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0

            # cov.final_fa_premises_summary.final_loss_cost = final_loss_cost * (cov.final_fa_premises_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_fa_travel_summary.final_loss_cost = final_loss_cost * (cov.final_fa_travel_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_fa_additional_summary.final_loss_cost = final_loss_cost * (cov.final_fa_additional_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0

        if risk_class_code == "GS":
            cov.gs_metals.final_summary_final_loss_cost = final_loss_cost*(cov.gs_metals.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.gs_cash.final_summary_final_loss_cost = final_loss_cost*(cov.gs_cash.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.gs_securities.final_summary_final_loss_cost = final_loss_cost*(cov.gs_securities.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.gs_additional.final_summary_final_loss_cost = final_loss_cost*(cov.gs_additional.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0

            # cov.final_gs_metals_summary.final_loss_cost = final_loss_cost * (cov.final_gs_metals_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_gs_cash_summary.final_loss_cost = final_loss_cost * (cov.final_gs_cash_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_gs_securities_summary.final_loss_cost = final_loss_cost * (cov.final_gs_securities_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0

        if risk_class_code == "CIT": 
            cov.cit_premises.final_summary_final_loss_cost = final_loss_cost *(cov.cit_premises.final_summary_prem_post_ded *(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0
            cov.cit_additional.final_summary_final_loss_cost = final_loss_cost *(cov.cit_additional.final_summary_prem_post_ded*(1-acq_costs)*lr)/exposure_loss_cost_length_adj if exposure_loss_cost_length_adj > 0 else 0

            # cov.final_cit_premises_summary.final_loss_cost = final_loss_cost * (cov.final_cit_premises_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0
            # cov.final_cit_additional_summary.final_loss_cost = final_loss_cost * (cov.final_cit_additional_summary.tsi / cds.final_claims_summary_table.tsi) if  cds.final_claims_summary_table.tsi > 0 else 0



        ## % cat
        cds.final_claims_summary_table.perc_cat_bp = perc_cat
        cds.final_claims_summary_table.perc_cat_data = cds.experience_rms_defaults.rms_cat_lr.selected/cds.experience_lr_summary_subtotal_1.ulr_inf if cds.experience_lr_summary_subtotal_1.ulr_inf > 0 else 0




        # Premium Summary ~~~

        ## Limit authority table
        authority_table = hx.params.table_input_authority_table[hx.params.table_input_authority_table["Underwriter"] == cds.standard_fields.underwriter]
        authority_table = authority_table[authority_table["JFAS Class"] == risk_class_code]
        if len(authority_table) == 0: #if no info on UW for that JFAS class
            uw_auth_limit = 0
        else:
            if cds.standard_fields.is_renewal == True:
                uw_auth_limit = authority_table["Exposure Limit (Renewal Risks)"].max()
            else:
                uw_auth_limit = authority_table["Exposure Limit (New Business Risks)"].max() 
       
        if uw_auth_limit >= layer.limit:
            uw_auth_flag = "Limit below Underwriting Authority"
        else:
            uw_auth_flag = "Limit above Underwriting Authority - ESO required"

        uw_auth_limit = 0 if uw_auth_limit is None else uw_auth_limit

        cds.final_prem_summary_limit_table.uw_auth_limit = uw_auth_limit
        cds.final_prem_summary_limit_table.uw_auth_flag = uw_auth_flag

        ## Tech premium breakdown table
        ### Pre UW adjustment

        reins = cds.final_claims_summary_table.perc_cat_sel * final_loss_cost * reinsurance
        cap_load = cap_allocation * final_loss_cost * coc

        cds.final_prem_summary_tp_table.loss_cost = final_loss_cost
        fixed_exp = indirect  if final_loss_cost!=0 else 0
        cds.final_prem_summary_tp_table.fixed_exp = fixed_exp
        cds.final_prem_summary_tp_table.reins = cds.final_claims_summary_table.perc_cat_sel * final_loss_cost * reinsurance
        input_acq_cost = cds.final_premium_summary_table.acq_cost
        cds.final_prem_summary_tp_table.acq_cost = input_acq_cost
        cds.final_prem_summary_tp_table.cap_load = cap_allocation * final_loss_cost * coc

        tech_prem = (final_loss_cost + fixed_exp + cds.final_prem_summary_tp_table.reins + cds.final_prem_summary_tp_table.cap_load) / (1-direct+investment_income) / (1-input_acq_cost)
        cds.final_prem_summary_tp_table.tech_prem = tech_prem

        if final_loss_cost == 0 :
            var_exp = 0
            inv_income = 0
        else:
            var_exp = direct * tech_prem * (1-input_acq_cost)
            inv_income = -investment_income * tech_prem * (1-input_acq_cost) # need an iferror = 0 thing
        
        cds.final_prem_summary_tp_table.var_exp = var_exp
        cds.final_prem_summary_tp_table.inv_income = inv_income
        cds.final_prem_summary_tp_table.allocated_capital = cap_allocation * final_loss_cost

        # TECHNICAL PREMIUM WATERFALL
        cds.final_tp_waterfall.loss_cost = round(final_loss_cost, 0)
        cds.final_tp_waterfall.var_expense = round(var_exp, 0)
        cds.final_tp_waterfall.fixed_expense = round(fixed_exp, 0)
        cds.final_tp_waterfall.tot_expense = round(fixed_exp, 0) + round(var_exp, 0)
        cds.final_tp_waterfall.inv_income = round(inv_income, 0)
        cds.final_tp_waterfall.ri = round(reins, 0)
        cds.final_tp_waterfall.capital = round(cap_load, 0)
        cds.final_tp_waterfall.tech_prem = round(tech_prem, 0)
        cds.final_tp_waterfall.brokerage = round(tech_prem - final_loss_cost - var_exp - fixed_exp - inv_income - reins - cap_load, 0)
        cds.final_tp_waterfall.quoted_premium = round(layer.quoted_premium, 0)

        ## Tech prem breakdown table
        ### Post UW adjustment
        total_credit = (1+cds.final_premium_summary_table.uw_credit)*(1+cds.final_premium_summary_table.client_credit)*(1+cds.final_premium_summary_table.risk_score_credit) - 1
        uw_adj = total_credit
        adj_final_loss_cost = final_loss_cost*(1 + uw_adj)
        adj_reins = cds.final_prem_summary_tp_table.reins*(1 + uw_adj)
        adj_cap_load = cap_allocation * adj_final_loss_cost * coc
        tech_prem_adj = (adj_final_loss_cost + fixed_exp + adj_reins + adj_cap_load) / (1-direct+investment_income) / (1-input_acq_cost)
       
        if adj_final_loss_cost == 0 :
            adj_var_exp = 0
            adj_inv_income = 0
        else:
            adj_var_exp = direct * tech_prem_adj * (1-input_acq_cost) if adj_final_loss_cost!=0 else 0
            adj_inv_income = -investment_income * tech_prem_adj * (1-input_acq_cost) if adj_final_loss_cost!=0 else 0

        alloc_cap = cap_allocation * final_loss_cost
        adj_alloc_cap = cap_allocation * adj_final_loss_cost

        #assign to nodes
        cds.final_prem_summary_tp_postuwadj_table.loss_cost = adj_final_loss_cost
        cds.final_prem_summary_tp_postuwadj_table.fixed_exp = fixed_exp
        cds.final_prem_summary_tp_postuwadj_table.reins = adj_reins
        cds.final_prem_summary_tp_postuwadj_table.acq_cost = input_acq_cost
        cds.final_prem_summary_tp_postuwadj_table.cap_load = adj_cap_load
        cds.final_prem_summary_tp_postuwadj_table.tech_prem = tech_prem_adj
        cds.final_prem_summary_tp_postuwadj_table.var_exp = adj_var_exp
        cds.final_prem_summary_tp_postuwadj_table.inv_income = adj_inv_income
        cds.final_prem_summary_tp_postuwadj_table.allocated_capital = adj_alloc_cap

        # TECHNICAL PREMIUM WATERFALL
        cds.final_tp_uwadj_waterfall.loss_cost = round(adj_final_loss_cost, 0)
        cds.final_tp_uwadj_waterfall.var_expense = round(adj_var_exp, 0)
        cds.final_tp_uwadj_waterfall.fixed_expense = round(fixed_exp, 0)
        cds.final_tp_uwadj_waterfall.tot_expense = round(fixed_exp, 0) + round(adj_var_exp, 0)
        cds.final_tp_uwadj_waterfall.inv_income = round(adj_inv_income, 0)
        cds.final_tp_uwadj_waterfall.ri = round(adj_reins, 0)
        cds.final_tp_uwadj_waterfall.capital = round(adj_cap_load, 0)
        cds.final_tp_uwadj_waterfall.tech_prem = round(tech_prem_adj, 0)
        cds.final_tp_uwadj_waterfall.brokerage = round(tech_prem_adj - adj_final_loss_cost - adj_var_exp - fixed_exp - adj_inv_income - adj_reins - adj_cap_load, 0)
        cds.final_tp_uwadj_waterfall.quoted_premium = round(layer.quoted_premium, 0)


        ## Summary table
        bench_prem = final_loss_cost / 0.7 / (1-input_acq_cost)
        bench_prem_adj = final_loss_cost*(1+total_credit) / 0.7 / (1-input_acq_cost)
        quote_prem = layer.quoted_premium if layer.quoted_premium is not None else 0   
        tpi = quote_prem / tech_prem_adj if tech_prem_adj !=0 else 0
        bpi = quote_prem / bench_prem_adj if bench_prem_adj !=0 else 0
        tpi_pre_uw_adj = quote_prem / tech_prem if tech_prem !=0 else 0
        bpi_pre_uw_adj = quote_prem / bench_prem if bench_prem !=0 else 0

        expected_profit_pre_uw_adj = quote_prem - reins - fixed_exp - var_exp - final_loss_cost - (quote_prem*input_acq_cost)
        implied_roc_pre_uw_adj = expected_profit_pre_uw_adj / alloc_cap if alloc_cap != 0 else 0
        
        expected_profit = quote_prem - adj_reins - fixed_exp - adj_var_exp - adj_final_loss_cost - (quote_prem*input_acq_cost)
        implied_roc = expected_profit / adj_alloc_cap if adj_alloc_cap != 0 else 0

        #assign to nodes
        cds.final_premium_summary_table.quoted_premium = cds.final_premium_summary_table.quoted_premium_slip_curr / fx_rate
        cds.final_premium_summary_table.loss_cost = final_loss_cost
        cds.final_premium_summary_table.tech_prem = tech_prem
        layer.benchmark_premium = bench_prem
        layer.technical_premium = tech_prem_adj        
        layer.brokerage = input_acq_cost
        cds.final_premium_summary_table.total_credit = total_credit
        cds.final_premium_summary_table.tech_prem_adj = tech_prem_adj
        cds.final_premium_summary_table.bench_prem_adj = bench_prem_adj
        layer.tpi = tpi
        layer.bpi = bpi                        
        # layer.pflr = bpi * 0.7
        # layer.pflr_pre_uw_adj = bpi_pre_uw_adj * 0.7
        layer.tpi_pre_uw_adj = tpi_pre_uw_adj
        layer.bpi_pre_uw_adj = bpi_pre_uw_adj
        layer.uw_adj_impact = bpi / bpi_pre_uw_adj - 1 if bpi_pre_uw_adj != 0 else 0
        layer.roc = implied_roc
        # layer.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj
        cds.final_premium_summary_table.expected_profit = expected_profit
        # cds.final_premium_summary_table.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj
        cds.final_premium_summary_table.expected_profit_pre_uw_adj = expected_profit_pre_uw_adj
        
        cds.final_premium_summary_table.gg_achieved_rate = quote_prem / cds.final_claims_summary_table.tsi if cds.final_claims_summary_table.tsi > 0 else 0
        cds.final_premium_summary_table.gn_achieved_rate = (quote_prem * (1 - input_acq_cost)) / cds.final_claims_summary_table.tsi if cds.final_claims_summary_table.tsi > 0 else 0

        if hxd.cds.standard_fields.is_case_priced and layer.quoted_prem_kpi_summary and layer.bpi_case_priced:
            layer.bench_prem_case_priced = layer.quoted_prem_kpi_summary / layer.bpi_case_priced
            layer.technical_prem_case_priced = layer.technical_premium
            if layer.technical_prem_case_priced:
                layer.tpi_case_priced = layer.bench_prem_case_priced / layer.technical_prem_case_priced 
            else:     
                layer.tpi_case_priced = 0

            layer.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj
            cds.final_premium_summary_table.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj
            layer.pflr = bpi * 0.7
            layer.pflr_pre_uw_adj = bpi_pre_uw_adj * 0.7

        if hxd.cds.standard_fields.is_rater_priced:
            layer.pflr = bpi * 0.7
            layer.pflr_pre_uw_adj = bpi_pre_uw_adj * 0.7
            layer.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj
            cds.final_premium_summary_table.implied_roc_pre_uw_adj = implied_roc_pre_uw_adj

        ### Jewellers Block  #this is hella long and can probs be done in a wayy better way !! :)
                            # SA: Again, these could be moved to a helper function and/or use get/setattr to replace the if statements
        if risk_class_code == "JB":
            # SA: you can catch both is not None and > 0 by just checking it directly: cov.final_jb_premises_summary.tsi if cov.final_jb_premises_summary.tsi else 0
            jb_prem_tsi = cov.jb_premises.final_summary_tsi if cov.jb_premises.final_summary_tsi is not None and cov.jb_premises.final_summary_tsi > 0 else 0  
            if final_loss_cost==0 or jb_prem_tsi==0 :
                jb_prem_tech_rate = 0
                jb_prem_ach_rate = 0
            else:
                jb_prem_tech_rate = tech_prem_adj*(cov.jb_premises.final_summary_final_loss_cost/final_loss_cost)/jb_prem_tsi
                jb_prem_ach_rate = quote_prem*(cov.jb_premises.final_summary_final_loss_cost/final_loss_cost)/jb_prem_tsi

            jb_trav_tsi = cov.jb_travel.final_summary_tsi if cov.jb_travel.final_summary_tsi is not None and cov.jb_travel.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or jb_trav_tsi==0 :
                jb_trav_tech_rate = 0
                jb_trav_ach_rate = 0
            else:
                jb_trav_tech_rate = tech_prem_adj*(cov.jb_travel.final_summary_final_loss_cost/final_loss_cost)/jb_trav_tsi
                jb_trav_ach_rate = quote_prem*(cov.jb_travel.final_summary_final_loss_cost/final_loss_cost)/jb_trav_tsi

            jb_add_tsi = cov.jb_additional.final_summary_tsi if cov.jb_additional.final_summary_tsi is not None and cov.jb_additional.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or jb_add_tsi==0 :
                jb_add_tech_rate = 0
                jb_add_ach_rate = 0
            else:
                jb_add_tech_rate = tech_prem_adj*(cov.jb_additional.final_summary_final_loss_cost/final_loss_cost)/jb_add_tsi
                jb_add_ach_rate = quote_prem*(cov.jb_additional.final_summary_final_loss_cost/final_loss_cost)/jb_add_tsi
        
            #assign nodes
            cov.jb_premises.final_premium_summary_tsi = jb_prem_tsi
            cov.jb_premises.final_premium_summary_tech_rate = jb_prem_tech_rate
            cov.jb_premises.final_premium_summary_ach_rate = jb_prem_ach_rate
            
            cov.jb_travel.final_premium_summary_tsi = jb_trav_tsi
            cov.jb_travel.final_premium_summary_tech_rate = jb_trav_tech_rate
            cov.jb_travel.final_premium_summary_ach_rate = jb_trav_ach_rate

            cov.jb_additional.final_premium_summary_tsi = jb_add_tsi
            cov.jb_additional.final_premium_summary_tech_rate = jb_add_tech_rate
            cov.jb_additional.final_premium_summary_ach_rate = jb_add_ach_rate

        ## Fine Art
        if risk_class_code == "FA":
            fa_prem_tsi = cov.fa_premises.final_summary_tsi if cov.fa_premises.final_summary_tsi is not None and cov.fa_premises.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or fa_prem_tsi==0 :
                fa_prem_tech_rate = 0
                fa_prem_ach_rate = 0
            else:
                fa_prem_tech_rate = tech_prem_adj*(cov.fa_premises.final_summary_final_loss_cost/final_loss_cost)/fa_prem_tsi
                fa_prem_ach_rate = quote_prem*(cov.fa_premises.final_summary_final_loss_cost/final_loss_cost)/fa_prem_tsi

            fa_trav_tsi = cov.fa_travel.final_summary_tsi if cov.fa_travel.final_summary_tsi is not None and cov.fa_travel.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or fa_trav_tsi==0 :
                fa_trav_tech_rate = 0
                fa_trav_ach_rate = 0
            else:
                fa_trav_tech_rate = tech_prem_adj*(cov.fa_travel.final_summary_final_loss_cost/final_loss_cost)/fa_trav_tsi
                fa_trav_ach_rate = quote_prem*(cov.fa_travel.final_summary_final_loss_cost/final_loss_cost)/fa_trav_tsi

            fa_add_tsi = cov.fa_additional.final_summary_tsi if cov.fa_additional.final_summary_tsi is not None and cov.fa_additional.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or fa_add_tsi==0 :
                fa_add_tech_rate = 0
                fa_add_ach_rate = 0
            else:
                fa_add_tech_rate = tech_prem_adj*(cov.fa_additional.final_summary_final_loss_cost/final_loss_cost)/fa_add_tsi
                fa_add_ach_rate = quote_prem*(cov.fa_additional.final_summary_final_loss_cost/final_loss_cost)/fa_add_tsi
        
            #assign nodes
            cov.fa_premises.final_premium_summary_tsi = fa_prem_tsi
            cov.fa_premises.final_premium_summary_tech_rate = fa_prem_tech_rate
            cov.fa_premises.final_premium_summary_ach_rate = fa_prem_ach_rate
            
            cov.fa_travel.final_premium_summary_tsi = fa_trav_tsi
            cov.fa_travel.final_premium_summary_tech_rate = fa_trav_tech_rate
            cov.fa_travel.final_premium_summary_ach_rate = fa_trav_ach_rate

            cov.fa_additional.final_premium_summary_tsi = fa_add_tsi
            cov.fa_additional.final_premium_summary_tech_rate = fa_add_tech_rate
            cov.fa_additional.final_premium_summary_ach_rate = fa_add_ach_rate

        ## General Specie
        if risk_class_code == "GS":
            gs_met_tsi = cov.gs_metals.final_summary_tsi if cov.gs_metals.final_summary_tsi is not None and cov.gs_metals.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or gs_met_tsi==0:
                gs_met_tech_rate = 0
                gs_met_ach_rate = 0
            else:
                gs_met_tech_rate = tech_prem_adj*(cov.gs_metals.final_summary_final_loss_cost/final_loss_cost)/gs_met_tsi
                gs_met_ach_rate = quote_prem*(cov.gs_metals.final_summary_final_loss_cost/final_loss_cost)/gs_met_tsi

            gs_cash_tsi = cov.gs_cash.final_summary_tsi if cov.gs_cash.final_summary_tsi is not None and cov.gs_cash.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or gs_cash_tsi==0 :
                gs_cash_tech_rate = 0
                gs_cash_ach_rate = 0
            else:
                gs_cash_tech_rate = tech_prem_adj*(cov.gs_cash.final_summary_final_loss_cost/final_loss_cost)/gs_cash_tsi
                gs_cash_ach_rate = quote_prem*(cov.gs_cash.final_summary_final_loss_cost/final_loss_cost)/gs_cash_tsi

            gs_sec_tsi = cov.gs_securities.final_summary_tsi if cov.gs_securities.final_summary_tsi is not None and cov.gs_securities.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or gs_sec_tsi==0 :
                gs_sec_tech_rate = 0
                gs_sec_ach_rate = 0
            else:
                gs_sec_tech_rate = tech_prem_adj*(cov.gs_securities.final_summary_final_loss_cost/final_loss_cost)/gs_sec_tsi
                gs_sec_ach_rate = quote_prem*(cov.gs_securities.final_summary_final_loss_cost/final_loss_cost)/gs_sec_tsi

            gs_add_tsi = cov.gs_additional.final_summary_tsi if cov.gs_additional.final_summary_tsi is not None and cov.gs_additional.final_summary_tsi > 0 else 0
            if final_loss_cost == 0 or gs_add_tsi == 0 :
                gs_add_tech_rate = 0
                gs_add_ach_rate = 0
            else:
                gs_add_tech_rate = tech_prem_adj * (cov.gs_additional.final_summary_final_loss_cost / final_loss_cost) / gs_add_tsi
                gs_add_ach_rate = quote_prem * (cov.gs_additional.final_summary_final_loss_cost / final_loss_cost) / gs_add_tsi
        
            #assign nodes
            cov.gs_metals.final_premium_summary_tsi = gs_met_tsi
            cov.gs_metals.final_premium_summary_tech_rate = gs_met_tech_rate
            cov.gs_metals.final_premium_summary_ach_rate = gs_met_ach_rate
            
            cov.gs_cash.final_premium_summary_tsi = gs_cash_tsi
            cov.gs_cash.final_premium_summary_tech_rate = gs_cash_tech_rate
            cov.gs_cash.final_premium_summary_ach_rate = gs_cash_ach_rate

            cov.gs_securities.final_premium_summary_tsi = gs_sec_tsi
            cov.gs_securities.final_premium_summary_tech_rate = gs_sec_tech_rate
            cov.gs_securities.final_premium_summary_ach_rate = gs_sec_ach_rate

            cov.gs_additional.final_premium_summary_tsi = gs_add_tsi
            cov.gs_additional.final_premium_summary_tech_rate = gs_add_tech_rate
            cov.gs_additional.final_premium_summary_ach_rate = gs_add_ach_rate

        ## Cash in Transit 
        if risk_class_code == "CIT":
            cit_prem_tsi = cov.cit_premises.final_summary_tsi if  cov.cit_premises.final_summary_tsi is not None and  cov.cit_premises.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or cit_prem_tsi==0 :
                cit_prem_tech_rate = 0
                cit_prem_ach_rate = 0
            else:
                cit_prem_tech_rate = tech_prem_adj*(cov.cit_premises.final_summary_final_loss_cost/final_loss_cost)/cit_prem_tsi
                cit_prem_ach_rate = quote_prem*(cov.cit_premises.final_summary_final_loss_cost/final_loss_cost)/cit_prem_tsi

            cit_add_tsi = cov.cit_additional.final_summary_tsi if cov.cit_additional.final_summary_tsi is not None and cov.cit_additional.final_summary_tsi > 0 else 0
            if final_loss_cost==0 or cit_add_tsi==0 :
                cit_add_tech_rate = 0
                cit_add_ach_rate = 0
            else:
                cit_add_tech_rate = tech_prem_adj*(cov.cit_additional.final_summary_final_loss_cost/final_loss_cost)/cit_add_tsi
                cit_add_ach_rate = quote_prem*(cov.cit_additional.final_summary_final_loss_cost/final_loss_cost)/cit_add_tsi
       
            #assign nodes
            cov.cit_premises.final_premium_summary_tsi = cit_prem_tsi
            cov.cit_premises.final_premium_summary_tech_rate = cit_prem_tech_rate
            cov.cit_premises.final_premium_summary_ach_rate = cit_prem_ach_rate

            cov.cit_additional.final_premium_summary_tsi = cit_add_tsi
            cov.cit_additional.final_premium_summary_tech_rate = cit_add_tech_rate
            cov.cit_additional.final_premium_summary_ach_rate = cit_add_ach_rate

    # assign hx_core
    hxd.hx_core.charged_premium = layer.quoted_premium 
    hxd.hx_core.premium_currency = cds.currencies.source_currency
    if cds.final_premium_summary_table.tech_prem_adj is not None:
        hxd.hx_core.model_premium = cds.final_premium_summary_table.tech_prem_adj
    bpi = layer.quoted_premium if layer.quoted_premium is not None else 0
    if bpi > 0:
        hxd.hx_core.ulr = 0.7 / bpi
    
    hxd.cds.standard_fields.inception_date = hxd.hx_core.inception_date
    hxd.cds.standard_fields.expiry_date = hxd.hx_core.expiry_date

    # layer.tpi = ratio(quote_prem, tech_prem_adj)
    # # tpi = 10

    # pass