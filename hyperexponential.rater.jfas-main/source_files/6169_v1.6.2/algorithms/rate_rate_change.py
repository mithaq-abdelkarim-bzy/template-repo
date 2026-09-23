import hx
import pandas as pd
import numpy as np
from operator import itemgetter
from statistics import mean

def rate_rate_change(hxd):
    cds = hxd.cds
    layer = cds.layers[0]
    cov = layer.coverages
    rc = layer.rate_change

    # Populate Sub-Category
    table_rating_ratechange_subcategory = hx.params.table_rating_ratechange_subcategory
    for rc_type in ["tech", "uwadj"]:
        i = 0
        for cob in ["jb", "fa", "gs", "cit"]:
            if cob == "gs": # IR: edit for GS additional
                loop = [1,2,3,4]
            else:
                loop = [1,2,3]

            for sub_group in loop:
                exec("layer." + cob + "_" + str(sub_group) + "_rc_" + rc_type + ".subcategory = table_rating_ratechange_subcategory.subcategory.iloc[" + str(i) + "]") # IR: extended table_rating_ratechange_subcategory for GS Additional, so check all still working as expected
                i = i + 1


    # Populate detailed rate change calculations - Technical
    for cob in ["jb", "fa", "gs", "cit"]:
        if cob == "gs":
            loop = [1,2,3,4]
        else:
            loop = [1,2,3]
    
        for sub_group in loop:
            
            sub_group_label = ""

            if cob == "jb" or cob == "fa":
                if sub_group == 1:
                    sub_group_label = "premises"
                elif sub_group == 2:
                    sub_group_label = "travel"
                else:
                    sub_group_label = "additional"
            elif cob == "gs":
                if sub_group == 1:
                    sub_group_label = "metals"
                elif sub_group == 2:
                    sub_group_label = "cash"
                else:
                    sub_group_label = "securities"
            else:
                if sub_group == 1:
                    sub_group_label = "premises"
                else:
                    sub_group_label = "additional"

            calc_type = "tech"

            # Allocated Quote Premium Last Year -- filled in with async task

            # Exposure Premium Change
            # Exposure Premium LY -- filled in with async task
            # Exposure Premium TY
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty = cov." + cob + "_" + sub_group_label + ".premium")

            # Change
            curr_year_exposure_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty") or 0
            last_year_exposure_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ly") or 0
            exposure_change = curr_year_exposure_prem / last_year_exposure_prem if last_year_exposure_prem > 0 else 1.0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_exp = exposure_change")
            prem_ly = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ly")
            prem_ly = prem_ly if prem_ly is not None else 0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_exp = exposure_change * prem_ly")


            # Deductibles Change
            # Deductibles LY -- filled in with async task
            # Deductibles TY
            current_year_model_credit = eval("cov." + cob + "_" + sub_group_label + ".credit")  # SA: f-strings might make these long joins easier to read! That said, I strongly advise against eval anyway
            current_year_uw_credit = eval("cov." + cob + "_" + sub_group_label + ".uw_adj_impact")
            current_year_applied_credit = (current_year_uw_credit if current_year_uw_credit is not None else current_year_model_credit) or 0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ded_ty = current_year_applied_credit")

            # Change
            # curr_year_ded_cred = eval("cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty") or 0
            last_year_applied_credit = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ded_ly") or 0
            deductible_change = (1 - current_year_applied_credit) / (1 - last_year_applied_credit) if last_year_applied_credit < 1.0 else 1.0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_ded = deductible_change")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_ded = deductible_change * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_exp")

            # Limits LY -- filled with async task
            # Limits TY -- NO IMPACT
            chg_lim = 1.0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_lim_ty = 0")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_lim = chg_lim")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_lim = layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_ded * chg_lim")

            # RISK LY -- filled with async task
            # RISK TY
            current_year_final_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_final_loss_cost")
            current_year_final_loss_cost = current_year_final_loss_cost if current_year_final_loss_cost is not None else 0
            # last_year_final_loss_cost = eval("cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ly") or 0
            last_year_final_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_loss_cost_ly") or 0
            last_year_final_loss_cost = last_year_final_loss_cost * exposure_change * deductible_change * chg_lim
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ty = current_year_final_loss_cost")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ly = last_year_final_loss_cost")

            # cov.final_jb_premises_summary.loss_cost_ly
            # eval("cov.final_" + cob + "_" + sub_group_label + "_summary.loss_cost_ly")
            # last_year_final_loss_cost

            # Change
            risk_change = current_year_final_loss_cost / last_year_final_loss_cost if last_year_final_loss_cost > 0 else 1.0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_risk = risk_change")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_risk = risk_change * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_lim")

            # T&C's LY -- filled with async task
            # T&C's TY -- NO IMPACT
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_tc_ty = 0")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_tc = 1.0")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_tc = layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_risk")

            # Allocated Quote Premium This year
            quote_prem = layer.quoted_premium if layer.quoted_premium is not None else 0

            subcategory_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_final_loss_cost")
            subcategory_loss_cost = subcategory_loss_cost if subcategory_loss_cost is not None else 0

            total_loss_cost = cds.final_claims_summary_table.final_loss_cost if cds.final_claims_summary_table.final_loss_cost is not None else 0

            allocated_quote_prem = quote_prem * (subcategory_loss_cost / total_loss_cost) if total_loss_cost > 0 else 0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ty = allocated_quote_prem")

            # RARC
            last_year_risk_adjusted_premium = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_tc") or 0
            rarc = allocated_quote_prem / last_year_risk_adjusted_premium if last_year_risk_adjusted_premium > 0 else 0.0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".rarc = rarc")

            if cob == "cit":
                # layer.cit_3_rc_tech.prem_ly = 0.0

                # layer.cit_3_rc_tech.prem_exp_ly = 0.0
                layer.cit_3_rc_tech.uwinput_exp = 0.0
                layer.cit_3_rc_tech.chg_exp = 1.0
                layer.cit_3_rc_tech.prem_adj_exp = 0.0

                # layer.cit_3_rc_tech.prem_ded_ly = 0.0
                layer.cit_3_rc_tech.uwinput_ded = 0.0
                layer.cit_3_rc_tech.prem_ded_ty = 0.0
                layer.cit_3_rc_tech.chg_ded = 1.0
                layer.cit_3_rc_tech.prem_adj_ded = 0.0

                # layer.cit_3_rc_tech.prem_lim_ly = 0.0
                layer.cit_3_rc_tech.uwinput_lim = 0.0
                layer.cit_3_rc_tech.prem_lim_ty = 0.0
                layer.cit_3_rc_tech.chg_lim = 1.0
                layer.cit_3_rc_tech.prem_adj_lim = 0.0

                # layer.cit_3_rc_tech.prem_risk_ly = 0.0
                layer.cit_3_rc_tech.uwinput_risk = 0.0
                layer.cit_3_rc_tech.prem_risk_ty = 0.0
                layer.cit_3_rc_tech.chg_risk = 1.0
                layer.cit_3_rc_tech.prem_adj_risk = 0.0

                # layer.cit_3_rc_tech.prem_tc_ly = 0.0
                layer.cit_3_rc_tech.uwinput_tc = 0.0
                layer.cit_3_rc_tech.prem_risk_ty = 0.0
                layer.cit_3_rc_tech.chg_tc = 1.0
                layer.cit_3_rc_tech.prem_adj_tc = 0.0

                layer.cit_3_rc_tech.prem_ty = 0.0
                layer.cit_3_rc_tech.rarc = 0.0


    # Populate detailed rate change calculations - UW Adjusted
    # SA: Might be easier to separate these bits into smaller functions!  
    for cob in ["jb", "fa", "gs", "cit"]: 
        if cob == "gs":
            loop = [1,2,3,4]
        else:
            loop = [1,2,3]

        for sub_group in loop:
            sub_group_label = ""

            if cob == "jb" or cob == "fa":
                if sub_group == 1:
                    sub_group_label = "premises"
                elif sub_group == 2:
                    sub_group_label = "travel"
                else:
                    sub_group_label = "additional"
            elif cob == "gs":
                if sub_group == 1:
                    sub_group_label = "metals"
                elif sub_group == 2:
                    sub_group_label = "cash"
                else:
                    sub_group_label = "securities"
            else:
                if sub_group == 1:
                    sub_group_label = "premises"
                else:
                    sub_group_label = "additional"

            calc_type = "uwadj"

            # Allocated Quote Premium Last Year -- filled in with async task

            # Exposure Premium Change
            # Exposure Premium LY -- filled in with async task
            # Exposure Premium TY
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty = cov." + cob + "_" + sub_group_label + ".premium")

            # Change
            curr_year_exposure_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty") or 0
            last_year_exposure_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ly") or 0
            exposure_change = curr_year_exposure_prem / last_year_exposure_prem if last_year_exposure_prem > 0 else 1.0

            # UW Adj Change
            exposure_change_uw = rc.exposure_change.uw_selected.selected

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".uwinput_exp = exposure_change_uw")

            exposure_change_selected = exposure_change_uw if exposure_change_uw else exposure_change
 

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_exp = exposure_change")
            prem_ly = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ly")
            prem_ly = prem_ly if prem_ly is not None else 0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_exp = exposure_change_selected * prem_ly")


            # Deductibles Change
            # Deductibles LY -- filled in with async task
            # Deductibles TY
            current_year_model_credit = eval("cov." + cob + "_" + sub_group_label + ".credit")
            current_year_uw_credit = eval("cov." + cob + "_" + sub_group_label + ".uw_adj_impact")
            current_year_applied_credit = (current_year_uw_credit if current_year_uw_credit is not None else current_year_model_credit) or 0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ded_ty = current_year_applied_credit")

            # Change
            # curr_year_ded_cred = eval("cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_exp_ty") or 0
            last_year_applied_credit = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ded_ly") or 0
            deductible_change = (1 - current_year_applied_credit) / (1 - last_year_applied_credit) if last_year_applied_credit < 1.0 else 1.0

            # UW Adj Change
            deductible_change_uw = rc.deductible_change.uw_selected.selected
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".uwinput_ded = deductible_change_uw")

            deductible_change_selected = deductible_change_uw if deductible_change_uw else deductible_change

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_ded = deductible_change")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_ded = deductible_change_selected * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_exp")

            # Limits LY -- filled with async task
            # Limits TY -- NO IMPACT
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_lim_ty = 0")

            limit_change = 1.0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_lim = limit_change")

            # UW Adj Change
            limit_change_uw = rc.limit_change.uw_selected.selected
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".uwinput_lim = limit_change_uw")

            limit_change_selected = limit_change_uw if limit_change_uw else limit_change

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_lim = limit_change_selected * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_ded")

            # RISK LY -- filled with async task
            # RISK TY
            current_year_final_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_final_loss_cost")
            current_year_final_loss_cost = current_year_final_loss_cost if current_year_final_loss_cost is not None else 0
            # last_year_final_loss_cost = eval("cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ly") or 0
            last_year_final_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_loss_cost_ly") or 0
            last_year_final_loss_cost = last_year_final_loss_cost * exposure_change * deductible_change * chg_lim
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ty = current_year_final_loss_cost")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_risk_ly = last_year_final_loss_cost")

            # Change
            risk_change = current_year_final_loss_cost / last_year_final_loss_cost if last_year_final_loss_cost > 0 else 1.0

            # UW Adj Change
            risk_change_uw = rc.risk_characteristics_change.uw_selected.selected
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".uwinput_risk = risk_change_uw")

            risk_change_selected = risk_change_uw if risk_change_uw else risk_change

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_risk = risk_change")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_risk = risk_change_selected * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_lim")

            # T&C's LY -- filled with async task
            # T&C's TY -- NO IMPACT
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_tc_ty = 0")

            tc_change = 1.0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".chg_tc = tc_change")

            # UW Adj Change
            tc_change_uw = rc.terms_conditions_change.uw_selected.selected
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".uwinput_lim = limit_change_uw")

            tc_change_selected = tc_change_uw if tc_change_uw else tc_change

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_tc = tc_change_selected * layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_risk")

            # Allocated Quote Premium This year
            quote_prem = layer.quoted_premium if layer.quoted_premium is not None else 0

            subcategory_loss_cost = eval("cov." + cob + "_" + sub_group_label + ".final_summary_final_loss_cost")
            subcategory_loss_cost = subcategory_loss_cost if subcategory_loss_cost is not None else 0

            total_loss_cost = cds.final_claims_summary_table.final_loss_cost if cds.final_claims_summary_table.final_loss_cost is not None else 0

            allocated_quote_prem = quote_prem * (subcategory_loss_cost / total_loss_cost) if total_loss_cost > 0 else 0

            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ty = allocated_quote_prem")

            # RARC
            last_year_risk_adjusted_premium = eval("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_tc") or 0
            rarc = allocated_quote_prem / last_year_risk_adjusted_premium if last_year_risk_adjusted_premium > 0 else 0.0
            exec("layer." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".rarc = rarc")

            if cob == "cit":
                # layer.cit_3_rc_uwadj.prem_ly = 0.0

                # layer.cit_3_rc_uwadj.prem_exp_ly = 0.0
                layer.cit_3_rc_uwadj.uwinput_exp = 0.0
                layer.cit_3_rc_uwadj.chg_exp = 1.0
                layer.cit_3_rc_uwadj.prem_adj_exp = 0.0

                # layer.cit_3_rc_uwadj.prem_ded_ly = 0.0
                layer.cit_3_rc_uwadj.uwinput_ded = 0.0
                layer.cit_3_rc_uwadj.prem_ded_ty = 0.0
                layer.cit_3_rc_uwadj.chg_ded = 1.0
                layer.cit_3_rc_uwadj.prem_adj_ded = 0.0

                # layer.cit_3_rc_uwadj.prem_lim_ly = 0.0
                layer.cit_3_rc_uwadj.uwinput_lim = 0.0
                layer.cit_3_rc_uwadj.prem_lim_ty = 0.0
                layer.cit_3_rc_uwadj.chg_lim = 1.0
                layer.cit_3_rc_uwadj.prem_adj_lim = 0.0

                # layer.cit_3_rc_uwadj.prem_risk_ly = 0.0
                layer.cit_3_rc_uwadj.uwinput_risk = 0.0
                layer.cit_3_rc_uwadj.prem_risk_ty = 0.0
                layer.cit_3_rc_uwadj.chg_risk = 1.0
                layer.cit_3_rc_uwadj.prem_adj_risk = 0.0

                # layer.cit_3_rc_uwadj.prem_tc_ly = 0.0
                layer.cit_3_rc_uwadj.uwinput_tc = 0.0
                layer.cit_3_rc_uwadj.prem_risk_ty = 0.0
                layer.cit_3_rc_uwadj.chg_tc = 1.0
                layer.cit_3_rc_uwadj.prem_adj_tc = 0.0

                layer.cit_3_rc_uwadj.prem_ty = 0.0
                layer.cit_3_rc_uwadj.rarc = 0.0

                
    # Populate Technical Total  ## this setup should really be improved...
    for calc_type in ["tech", "uwadj"]:

        for cob in ["jb", "fa", "cit"]:

            total_quote_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ly") or 0)
            total_prem_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ty") or 0)

            total_prem_exp_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_exp_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_exp_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_exp_ly") or 0)
            total_prem_exp_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_exp_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_exp_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_exp_ty") or 0)
            total_prem_adj_exp = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_exp") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_exp") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_exp") or 0)

            total_ded_ly = ((eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ly") or 0) + \
                           (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ly") or 0) + \
                           (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ly") or 0)) / total_quote_ly if total_quote_ly > 0 else 0.0

            total_ded_ty = ((eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ty") or 0) + \
                           (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ty") or 0) + \
                           (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ty") or 0)) / total_prem_ty if total_prem_ty > 0 else 0.0

            total_prem_adj_ded = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_ded") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_ded") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_ded") or 0)

            total_prem_lim_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_lim_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_lim_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_lim_ly") or 0)
            total_prem_lim_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_lim_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_lim_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_lim_ty") or 0)
            total_prem_adj_lim = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_lim") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_lim") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_lim") or 0)

            total_prem_risk_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_risk_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_risk_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_risk_ly") or 0)
            total_prem_risk_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_risk_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_risk_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_risk_ty") or 0)
            total_prem_adj_risk = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_risk") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_risk") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_risk") or 0)

            total_prem_tc_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_tc_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_tc_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_tc_ly") or 0)
            total_prem_tc_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_tc_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_tc_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_tc_ty") or 0)
            total_prem_adj_tc = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_tc") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_tc") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_tc") or 0)

            
            # assign to nodes
            exec("layer." + cob + "_rc_" + calc_type + ".prem_ly = total_quote_ly")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_exp_ly = total_prem_exp_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_exp_ty = total_prem_exp_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_exp = total_prem_adj_exp")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_ded_ly = total_ded_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_ded_ty = total_ded_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_ded = total_prem_adj_ded")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_lim_ly = total_prem_lim_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_lim_ty = total_prem_lim_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_lim = total_prem_adj_lim")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_risk_ly = total_prem_risk_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_risk_ty = total_prem_risk_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_risk = total_prem_adj_risk")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_tc_ly = total_prem_tc_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_tc_ty = total_prem_tc_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_tc = total_prem_adj_tc")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_ty = total_prem_ty")

            # CALCS
            exec("layer." + cob + "_rc_" + calc_type + ".chg_exp = total_prem_exp_ty / total_prem_exp_ly if total_prem_exp_ly > 0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_ded = (1 - total_ded_ty) / (1 - total_ded_ly) if total_ded_ty < 1.0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_lim = 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_risk = total_prem_risk_ty / total_prem_risk_ly if total_prem_risk_ly > 0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_tc = 1.0")

            exec("layer." + cob + "_rc_" + calc_type + ".rarc = total_prem_ty / total_prem_adj_tc if total_prem_adj_tc > 0 else 0.0")

            # UW MODIFIERS
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_exp = rc.exposure_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_ded = rc.deductible_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_lim = rc.limit_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_risk = rc.risk_characteristics_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_tc = rc.terms_conditions_change.uw_selected.selected")
        
        for cob in ["gs"]:

            total_quote_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ly") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ly") or 0)
            total_prem_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ty") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ty") or 0)

            total_prem_exp_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_exp_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_exp_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_exp_ly") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_exp_ly") or 0)
            total_prem_exp_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_exp_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_exp_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_exp_ty") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_exp_ty") or 0)
            total_prem_adj_exp = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_exp") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_exp") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_exp") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_adj_exp") or 0)

            total_ded_ly = ((eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ly") or 0) + \
                           (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ly") or 0) + \
                           (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ly") or 0) + \
                           (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ded_ly") or 0) * (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ly") or 0)) / total_quote_ly if total_quote_ly > 0 else 0.0

            total_ded_ty = ((eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_ty") or 0) + \
                           (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_ty") or 0) + \
                           (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_ty") or 0) + \
                           (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ded_ty") or 0) * (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_ty") or 0)) / total_prem_ty if total_prem_ty > 0 else 0.0

            total_prem_adj_ded = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_ded") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_ded") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_ded") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_adj_ded") or 0)

            total_prem_lim_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_lim_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_lim_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_lim_ly") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_lim_ly") or 0)
            total_prem_lim_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_lim_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_lim_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_lim_ty") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_lim_ty") or 0)
            total_prem_adj_lim = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_lim") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_lim") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_lim") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_adj_lim") or 0)

            total_prem_risk_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_risk_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_risk_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_risk_ly") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_risk_ly") or 0)
            total_prem_risk_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_risk_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_risk_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_risk_ty") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_risk_ty") or 0)
            total_prem_adj_risk = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_risk") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_risk") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_risk") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_adj_risk") or 0)

            total_prem_tc_ly = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_tc_ly") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_tc_ly") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_tc_ly") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_tc_ly") or 0)
            total_prem_tc_ty = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_tc_ty") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_tc_ty") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_tc_ty") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_tc_ty") or 0)
            total_prem_adj_tc = (eval("layer." + cob + "_1_rc_" + calc_type + ".prem_adj_tc") or 0) + (eval("layer." + cob + "_2_rc_" + calc_type + ".prem_adj_tc") or 0) + (eval("layer." + cob + "_3_rc_" + calc_type + ".prem_adj_tc") or 0) + (eval("layer." + cob + "_4_rc_" + calc_type + ".prem_adj_tc") or 0)


            # assign to nodes
            exec("layer." + cob + "_rc_" + calc_type + ".prem_ly = total_quote_ly")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_exp_ly = total_prem_exp_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_exp_ty = total_prem_exp_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_exp = total_prem_adj_exp")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_ded_ly = total_ded_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_ded_ty = total_ded_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_ded = total_prem_adj_ded")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_lim_ly = total_prem_lim_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_lim_ty = total_prem_lim_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_lim = total_prem_adj_lim")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_risk_ly = total_prem_risk_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_risk_ty = total_prem_risk_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_risk = total_prem_adj_risk")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_tc_ly = total_prem_tc_ly")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_tc_ty = total_prem_tc_ty")
            exec("layer." + cob + "_rc_" + calc_type + ".prem_adj_tc = total_prem_adj_tc")

            exec("layer." + cob + "_rc_" + calc_type + ".prem_ty = total_prem_ty")

            # CALCS
            exec("layer." + cob + "_rc_" + calc_type + ".chg_exp = total_prem_exp_ty / total_prem_exp_ly if total_prem_exp_ly > 0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_ded = (1 - total_ded_ty) / (1 - total_ded_ly) if total_ded_ty < 1.0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_lim = 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_risk = total_prem_risk_ty / total_prem_risk_ly if total_prem_risk_ly > 0 else 1.0")
            exec("layer." + cob + "_rc_" + calc_type + ".chg_tc = 1.0")

            exec("layer." + cob + "_rc_" + calc_type + ".rarc = total_prem_ty / total_prem_adj_tc if total_prem_adj_tc > 0 else 0.0")

            # UW MODIFIERS
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_exp = rc.exposure_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_ded = rc.deductible_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_lim = rc.limit_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_risk = rc.risk_characteristics_change.uw_selected.selected")
            exec("layer." + cob + "_rc_" + calc_type + ".uwinput_tc = rc.terms_conditions_change.uw_selected.selected")



   

    # # Populate summarised rate change table
    # for calc_type in ["tech", "uwadj"]:
    #     for cob in ["jb", "fa", "gs", "cit"]:
    #         # exec("cov." + cob + "_rc_" + calc_type + ".prem_ly = 0.0")
    #         exec("cov." + cob + "_rc_" + calc_type + ".prem_ty = 0.0")
    #         for sub_group in [1, 2, 3]:
    #             # exec("cov." + cob + "_rc_" + calc_type + ".prem_ly += cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ly") # Must be a better way to sum over this
    #             exec("cov." + cob + "_rc_" + calc_type + ".prem_ty += cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_ty")
    #         for step in ["exp", "ded", "lim", "risk", "tc"]:
    #             # exec("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ly = 0.0")
    #             exec("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ty = 0.0")
    #             exec("cov." + cob + "_rc_" + calc_type + ".prem_adj_" + step + " = 0.0")
    #             for sub_group in [1, 2, 3]:
    #                 # exec("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ly += cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_" + step + "_ly if rc." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_" + step + "_ly != None else 0.0")
    #                 exec("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ty += cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_" + step + "_ty if rc." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_" + step + "_ty != None else 0.0")
    #                 exec("cov." + cob + "_rc_" + calc_type + ".prem_adj_" + step + " += cov." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_" + step + " if rc." + cob + "_" + str(sub_group) + "_rc_" + calc_type + ".prem_adj_" + step + " != None else 0.0")

    #                 ty_prem = eval("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ty")
    #                 ly_prem = eval("cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ly")
    #                 ty_prem = ty_prem if ty_prem is not None else 0
    #                 ly_prem = ty_prem if ty_prem is not None else 0
    #                 # exec("cov." + cob + "_rc_" + calc_type + ".chg_" + step + " = cov." + cob + "_rc_" + calc_type + ".prem_" + step + "_ty / rc." + cob + "_rc_" + calc_type + ".prem_" + step + "_ly if rc." + cob + "_rc_" + calc_type + ".prem_" + step + "_ly > 0 else None")
    #                 exec("cov." + cob + "_rc_" + calc_type + ".chg_" + step + " =  ty_prem / ly_prem if ly_prem > 0 else None")
                
    #             prem_ty_total = eval("cov." + cob + "_rc_" + calc_type + ".prem_ty")
    #             prem_ly_risk_adjusted_total = eval("cov." + cob + "_rc_" + calc_type + ".prem_adj_tc")
    #             prem_ty_total = prem_ty_total if prem_ty_total is not None else 0
    #             prem_ly_risk_adjusted_total = prem_ly_risk_adjusted_total if prem_ly_risk_adjusted_total is not None else 0

    #             exec("cov." + cob + "_rc_" + calc_type + ".rarc = prem_ty_total / prem_ly_risk_adjusted_total if prem_ly_risk_adjusted_total > 0 else None")

    # for cob in ["jb", "fa", "gs", "cit"]:
    #     # exec("cov." + cob + "_rc_uwadj.prem_ly = 0.0")
    #     exec("cov." + cob + "_rc_uwadj.prem_ty = 0.0")
    #     for sub_group in [1, 2, 3]:
    #         # exec("cov." + cob + "_rc_uwadj.prem_ly += cov." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_ly") # Must be a better way to sum over this
    #         exec("cov." + cob + "_rc_uwadj.prem_ty += cov." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_ty")
    #     for step in ["exp", "ded", "lim", "risk", "tc"]:
    #         # exec("cov." + cob + "_rc_uwadj.prem_" + step + "_ly = 0.0")
    #         exec("cov." + cob + "_rc_uwadj.prem_" + step + "_ty = 0.0")
    #         exec("cov." + cob + "_rc_uwadj.prem_adj_" + step + " = 0.0")
    #         for sub_group in [1, 2, 3]:
    #             # exec("cov." + cob + "_rc_uwadj.prem_" + step + "_ly += cov." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_" + step + "_ly if rc." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_" + step + "_ly != None else 0.0")
    #             exec("cov." + cob + "_rc_uwadj.prem_" + step + "_ty += cov." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_" + step + "_ty if rc." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_" + step + "_ty != None else 0.0")
    #             exec("cov." + cob + "_rc_uwadj.prem_adj_" + step + " += cov." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_adj_" + step + " if rc." + cob + "_" + str(sub_group) + "_rc_uwadj.prem_adj_" + step + " != None else 0.0")
    #         #     exec("cov." + cob + "_rc_uwadj.chg_" + step + " = cov." + cob + "_rc_uwadj.prem_" + step + "_ty / rc." + cob + "_rc_uwadj.prem_" + step + "_ly if rc." + cob + "_rc_uwadj.prem_" + step + "_ly > 0 else None")
    #         # exec("cov." + cob + "_rc_uwadj.rarc = cov." + cob + "_rc_uwadj.prem_ty / rc." + cob + "_rc_uwadj.prem_adj_tc if rc." + cob + "_rc_uwadj.prem_adj_tc > 0 else None")


    # Waterfall calculations
    for cob in ["jb", "fa", "gs", "cit"]:
        if cob == "gs":
            loop = [1,2,3,4]
        else:
            loop = [1,2,3]

        for sub_group in loop:
            
            exp_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_ly")
            exposure = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_exp")
            deduct = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_ded")
            limit = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_lim") 
            risk = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_risk")
            tc = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_tc")
            risk_adj_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_adj_tc")
            quote_prem = eval("layer." + cob + "_" + str(sub_group) + "_rc_tech.prem_ty")

            exp_prem = round(exp_prem, 0) if exp_prem is not None else 0
            exposure = round(exposure, 0) if exposure is not None else 0
            deduct = round(deduct, 0) if deduct is not None else 0
            limit = round(limit, 0) if limit is not None else 0
            risk = round(risk, 0) if risk is not None else 0
            tc = round(tc, 0) if tc is not None else 0
            risk_adj_prem = round(risk_adj_prem, 0) if risk_adj_prem is not None else 0
            quote_prem = round(quote_prem, 0) if quote_prem is not None else 0
            
            exposure_delta = round(exposure - exp_prem, 0)
            deduct_delta = round(deduct - exposure, 0)
            limit_delta = round(limit - deduct, 0)
            risk_delta = round(risk - limit, 0)
            tc_delta = round(tc - risk, 0)

            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.exp_prem = exp_prem")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.exposure = exposure_delta")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.deduct = deduct_delta")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.limit = limit_delta")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.risk = risk_delta")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.t_and_cs = tc_delta")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.risk_adj_premium = risk_adj_prem")
            exec("layer." + cob + "_" + str(sub_group) + "_rc_waterfall.quoted_premium = quote_prem")

    # Assign Rate Change Metrics back TO FInal Selections and Summary
    # RATE CHANGE COMPONENTS
    if cds.standard_fields.benchmark_class == "Jewellers Block":
        # SA: another case for setattr rather than if statements

        rc.exposure_change.model_calculated = layer.jb_rc_tech.chg_exp - 1
        rc.deductible_change.model_calculated = layer.jb_rc_tech.chg_ded - 1
        rc.limit_change.model_calculated = layer.jb_rc_tech.chg_lim - 1
        rc.risk_characteristics_change.model_calculated = layer.jb_rc_tech.chg_risk - 1
        rc.terms_conditions_change.model_calculated = layer.jb_rc_tech.chg_tc - 1
        rc.risk_adj_premium.model_calculated = layer.jb_rc_tech.prem_adj_tc
        layer.rate_change.quoted_premium = layer.jb_rc_tech.prem_ty
        cds.final_rc_uwadj_summary.quoted_premium = layer.jb_rc_tech.prem_ty
        quote_prem_ty = layer.jb_rc_tech.prem_ty
        quote_prem_ly = layer.jb_rc_tech.prem_ly
        rarc = layer.jb_rc_tech.rarc

    elif cds.standard_fields.benchmark_class == "Fine Art":

        rc.exposure_change.model_calculated = layer.fa_rc_tech.chg_exp - 1
        rc.deductible_change.model_calculated = layer.fa_rc_tech.chg_ded - 1
        rc.limit_change.model_calculated = layer.fa_rc_tech.chg_lim - 1
        rc.risk_characteristics_change.model_calculated = layer.fa_rc_tech.chg_risk - 1
        rc.terms_conditions_change.model_calculated = layer.fa_rc_tech.chg_tc - 1
        rc.risk_adj_premium.model_calculated = layer.fa_rc_tech.prem_adj_tc
        layer.rate_change.quoted_premium = layer.fa_rc_tech.prem_ty
        cds.final_rc_uwadj_summary.quoted_premium = layer.fa_rc_tech.prem_ty

        quote_prem_ty = layer.fa_rc_tech.prem_ty
        quote_prem_ly = layer.fa_rc_tech.prem_ly
        rarc = layer.fa_rc_tech.rarc

    elif cds.standard_fields.benchmark_class == "General Specie":

        rc.exposure_change.model_calculated = layer.gs_rc_tech.chg_exp - 1
        rc.deductible_change.model_calculated = layer.gs_rc_tech.chg_ded - 1
        rc.limit_change.model_calculated = layer.gs_rc_tech.chg_lim - 1
        rc.risk_characteristics_change.model_calculated = layer.gs_rc_tech.chg_risk - 1
        rc.terms_conditions_change.model_calculated = layer.gs_rc_tech.chg_tc - 1
        rc.risk_adj_premium.model_calculated = layer.gs_rc_tech.prem_adj_tc
        layer.rate_change.quoted_premium = layer.gs_rc_tech.prem_ty
        cds.final_rc_uwadj_summary.quoted_premium = layer.gs_rc_tech.prem_ty
        quote_prem_ty = layer.gs_rc_tech.prem_ty
        quote_prem_ly = layer.gs_rc_tech.prem_ly
        rarc = layer.gs_rc_tech.rarc

    else:

        rc.exposure_change.model_calculated = layer.cit_rc_tech.chg_exp - 1
        rc.deductible_change.model_calculated = layer.cit_rc_tech.chg_ded - 1
        rc.limit_change.model_calculated = layer.cit_rc_tech.chg_lim - 1
        rc.risk_characteristics_change.model_calculated = layer.cit_rc_tech.chg_risk - 1
        rc.terms_conditions_change.model_calculated = layer.cit_rc_tech.chg_tc - 1
        rc.risk_adj_premium.model_calculated = layer.cit_rc_tech.prem_adj_tc
        layer.rate_change.quoted_premium = layer.cit_rc_tech.prem_ty
        cds.final_rc_uwadj_summary.quoted_premium = layer.cit_rc_tech.prem_ty
        quote_prem_ty = layer.cit_rc_tech.prem_ty
        quote_prem_ly = layer.cit_rc_tech.prem_ly
        rarc = layer.cit_rc_tech.rarc

    # Write from model_calcualted to uw_selected
    # SA: This is to accomodate the cds wanting these saved in two places
    rc.exposure_change.uw_selected.calculated = rc.exposure_change.model_calculated
    rc.deductible_change.uw_selected.calculated = rc.deductible_change.model_calculated
    rc.limit_change.uw_selected.calculated = rc.limit_change.model_calculated
    rc.risk_characteristics_change.uw_selected.calculated = rc.risk_characteristics_change.model_calculated
    rc.terms_conditions_change.uw_selected.calculated = rc.terms_conditions_change.model_calculated
    rc.risk_adj_premium.uw_selected.calculated = rc.risk_adj_premium.model_calculated
    rc.quoted_premium = cds.final_rc_uwadj_summary.quoted_premium

    # RATE CHANGE SUMMARY
    layer.rate_change.pure_rc = quote_prem_ty / quote_prem_ly if quote_prem_ly > 0 else 0.0
    rc.rate_change.model_calculated = rarc
    layer.rate_change.business = 0.0184149664520629

    cds.final_rc_uwadj_summary2.pure_rc_uw_adj = layer.rate_change.pure_rc
    cds.final_rc_uwadj_summary2.business_uw_adj = layer.rate_change.business

    # FINAL SELECTIONS WATERFALL

    if cds.standard_fields.benchmark_class == "Jewellers Block":
        cob = "jb"
    elif cds.standard_fields.benchmark_class == "Fine Art":
        cob = "fa"
    elif cds.standard_fields.benchmark_class == "General Specie":
        cob = "gs"
    else:
        cob = "cit"

    exp_prem_fs = eval("layer." + cob + "_rc_tech.prem_ly")
    exposure_fs = eval("layer." + cob + "_rc_tech.prem_adj_exp")
    deduct_fs = eval("layer." + cob + "_rc_tech.prem_adj_ded")
    limit_fs = eval("layer." + cob + "_rc_tech.prem_adj_lim") 
    risk_fs = eval("layer." + cob + "_rc_tech.prem_adj_risk")
    tc_fs = eval("layer." + cob + "_rc_tech.prem_adj_tc")
    risk_adj_prem_fs = eval("layer." + cob + "_rc_tech.prem_adj_tc")
    prem_fs = layer.quoted_premium

    exp_prem_fs = round(exp_prem_fs, 0) if exp_prem_fs is not None else 0
    exposure_fs = round(exposure_fs, 0) if exposure_fs is not None else 0
    deduct_fs = round(deduct_fs, 0) if deduct_fs is not None else 0
    limit_fs = round(limit_fs, 0) if limit_fs is not None else 0
    risk_fs = round(risk_fs, 0) if risk_fs is not None else 0
    tc_fs = round(tc_fs, 0) if tc_fs is not None else 0
    risk_adj_prem_fs = round(risk_adj_prem_fs, 0) if risk_adj_prem_fs is not None else 0
    prem_fs = round(prem_fs, 0) if prem_fs is not None else 0
    
    exposure_delta_fs = round(exposure_fs - exp_prem_fs, 0)
    deduct_delta_fs = round(deduct_fs - exposure_fs, 0)
    limit_delta_fs = round(limit_fs - deduct_fs, 0)
    risk_delta_fs = round(risk_fs - limit_fs, 0)
    tc_delta_fs = round(tc_fs - risk_fs, 0)

    # #assign to nodes
    cds.final_rc_waterfall.exp_prem = exp_prem_fs
    cds.final_rc_waterfall.exposure = exposure_delta_fs
    cds.final_rc_waterfall.deduct = deduct_delta_fs
    cds.final_rc_waterfall.limit = limit_delta_fs
    cds.final_rc_waterfall.risk = risk_delta_fs
    cds.final_rc_waterfall.t_and_cs = tc_delta_fs
    cds.final_rc_waterfall.risk_adj_premium = risk_adj_prem_fs
    cds.final_rc_waterfall.quoted_premium = prem_fs
    
    