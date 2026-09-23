import hx
import pandas as pd
import numpy as np
import math
from operator import itemgetter
import algorithms.rate_z_global_parameters as global_params
#import pyodbc
import algorithms.rate_z_utilities as util


def fetch_bi_data(hxd, df):
    cds = hxd.cds
    cov = cds.layers[0].coverages

    # claims_data = {}
    # policy_data = {}

    policy_ref = cds.standard_fields.policy_reference
    # "JCT61L23ANYJ"  # hxd.hx_core.policy_reference L0262V16ANFJ
    index_ref = policy_ref[:6] + policy_ref[8:]

    policy_data = pd.DataFrame(hx.params.table_input_experience_policy_data)
    claims_data = pd.DataFrame(hx.params.table_input_experience_claim_data)

    policy_data = policy_data[policy_data["Index"] == index_ref]
    claims_data = claims_data[claims_data["Index"] == index_ref]

    claims_data = claims_data.sort_values(by = ["BeazleyShareTotalIncurredInUSD"], ascending = False).iloc[0:10]

    if policy_data.empty:
        # do nothing
        cds.fetch_bi_task_status_policy = "Policy Information not found for selected Reference"
    else:
        setattr(hxd,"bi_policy_data",policy_data.to_dict("records"))
        cds.fetch_bi_task_status_policy = "Policy Data successfully retrieved"

    if policy_data.empty:
        # do nothing
        cds.fetch_bi_task_status_claims = "Claims Information not found for selected Reference"
    else:
        setattr(hxd,"bi_claims_data",claims_data.to_dict("records"))

        cds.fetch_bi_task_status_claims = "Claims Data successfully retrieved"

    return



def rate_experience_rating_bi(hxd, df):
    cds = hxd.cds
    cov = cds.layers[0].coverages

    # 0. DECLARE GLOBAL PARAMETERS --------------------
    cds.experience_rms_defaults.rms_cat_lr.calculated = global_params.experience_rms_cat_lr
    cds.bi_masking = True if cds.experience_rating.data_source == "BI" else False  # SA: can just do cds.bi_masking = cds.experience_rating.data_source == "BI"
    cds.manual_masking = True if cds.experience_rating.data_source == "Manual" else False
    cds.experience_rating.policy_ref = cds.standard_fields.policy_reference

    # SA: as you're doing the same filter twice, it's better to save the result to a variable first, otherwise you're performing that computation twice. 
    # Won't matter much though as it's only one line rather than an item in a loop
    if len(hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]) > 0:  
        risk_class_code = hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]["tag"].iloc[0]
    else:
        risk_class_code = ""

    if risk_class_code != "":

        # A) set parameters 

        policy_year = hxd.hx_core.inception_date.year or 2023
        policy_month = hxd.hx_core.inception_date.month or 1
        policy_ref  = cds.standard_fields.policy_reference # "JCT61L23ANYJ" 
        index_ref = policy_ref[:6] + policy_ref[8:] # "JCT61LANYJ" 
        curr = cds.currencies.source_currency
        curr_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == curr]["fx_rate"].iloc[0]

        # B) class specific data
        if risk_class_code == "JB":
            ielr_table = hx.params.table_input_experience_ielr[["YOA", "Jewellers"]]
            dfm_pattern = hx.params.table_input_experience_dfm[["Development Month", "Jewellers"]]
        else:
            ielr_table = hx.params.table_input_experience_ielr[["YOA", "Fine Art and Specie"]]
            dfm_pattern = hx.params.table_input_experience_dfm[["Development Month", "Fine Art and Specie"]]


        bp_infl = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Inflation"][risk_class_code].iloc[0]
        bp_rc = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "RC"][risk_class_code].iloc[0]
        bp_ll_lr = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] =="LcLoad"][risk_class_code].iloc[0]
        bp_cat_lr = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Cat"][risk_class_code].iloc[0]
        bp_ll_threshold = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "LargeLoss"][risk_class_code].iloc[0]

        cds.experience_rms_defaults.rms_cat_lr.calculated = bp_cat_lr

        policy_data = pd.DataFrame(cds.bi_policy_data)
        claims_data = pd.DataFrame(cds.bi_claims_data)

        # policy_ref = cds.standard_fields.policy_reference 
        # # "JCT61L23ANYJ"  # hxd.hx_core.policy_reference L0262V16ANFJ
        # index_ref = policy_ref[:6] + policy_ref[8:]

        # policy_data = pd.DataFrame(hx.params.table_input_experience_policy_data)
        # claims_data = pd.DataFrame(hx.params.table_input_experience_claim_data)

        # policy_data = policy_data[policy_data["Index"] == index_ref]
        # claims_data = claims_data[claims_data["Index"] == index_ref]

        if policy_data.shape[0]==0:
            policy_data = pd.DataFrame({
                "PolicyReference" : "",
                "SectionReference" : "",
                "YOA" : 2024,
                "CoverageName" : "",
                "TriFocusName" : "",
                "Division" : "",
                "RateChangeDivisor" : 0.0,
                "SettlementCurrency" : "",
                "WrittenOrEstimatPrem" : 0.0,
                "TotalIncurred" : 0.0,
                "RateChangeReformat" : 0.0,
                "WEPOnLevel" : 0.0,
                "Index" : "",
                "TotalWrittenIfNotSignedMultiplier" : 0.0,
                "TotalWEP" : 0.0
                }, index = [0])
        elif policy_data.shape[0] > 0:
            policy_data = util.pd_df_from_hx_list(cds.bi_policy_data)

        if claims_data.shape[0]==0:
            claims_data = pd.DataFrame({
                "SectionReference" : "",
                "ClaimReference" : "",
                "TriFocusName" : "",
                "Division" : "",
                "PolicyYOA" : 2024,
                "PolicyReference" : "",
                "TriFocusName" : "",
                "BeazleyCatCode" : "",
                "BeazleyCat" : "",
                "MarketCatCode" : "",
                "MarketCat" : "",
                "MarketCatCode" : "",
                "HasBeazleyCatCode" : "",
                "BeazleyShareTotalIncurredInUSD" : 0.0,
                "BeazleyShareTotalOutstandingInUSD" : 0.0,
                "CauseOfLoss" : "",
                "LargeLossIndicator" : 0.0,
                "Index" : "",
                "SignedLineMultiplier":1.0,
                "TotalIncurredInUSD" : 0.0,
                }, index = [0])
        elif claims_data.shape[0] > 0:
            claims_data = util.pd_df_from_hx_list(cds.bi_claims_data)

        # C) Premium Data

        if cds.bi_masking:

            policy_data_agg = policy_data.groupby("YOA",as_index=False)[["TotalWEP","RateChangeReformat"]].agg({"TotalWEP" : "sum", "RateChangeReformat" : "first"})

            ## converting premium to slip currency !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            min_year = min(policy_data_agg["YOA"].min(), policy_year - 10)

            if math.isnan(min_year):
                min_year = policy_year - 10

            policy_data_agg.loc[:,"TotalWEP"] = policy_data_agg.loc[:,"TotalWEP"] * curr_rate   
            summary_table = pd.DataFrame( {"YOA" : list(range(int(min_year), int(policy_year)))})
            summary_table = pd.merge(summary_table, policy_data_agg, how = "left", on = "YOA")

            ## calc on level premium
            summary_table.loc[:,"RateChangeReformat"] = summary_table.loc[:,"RateChangeReformat"].fillna(1+bp_rc)
            summary_table.loc[:,"rc_index"] = summary_table.loc[:,"RateChangeReformat"][::-1].cumprod()[::-1]
            summary_table = summary_table.assign(ol_prem = lambda x: x.TotalWEP * x.rc_index)

            ## extract dev% and ielr
            summary_table.loc[:,"Development Month"] = np.minimum((policy_year - summary_table["YOA"])*12 + policy_month,50)
            summary_table = pd.merge(summary_table,dfm_pattern,how="left", on = "Development Month")
            summary_table = pd.merge(summary_table,ielr_table,how="left", on = "YOA")
            summary_table.columns.values[6] = "dev"
            summary_table.columns.values[7] = "ielr"


            # D) Claims Data
            # claims_data = claims_data[claims_data["Index"] == index_ref]
            # claims_data = util.pd_df_from_hx_list(cds.bi_claims_data)
            claims_data.loc[:,"MarketCat"] = claims_data.loc[:,"MarketCat"].astype("string")

            ## coverting to slip currency!!!!!!
            claims_data.loc[:,"TotalIncurredSlipCurr"] = claims_data["BeazleyShareTotalIncurredInUSD"] * curr_rate

            att_claims_data_agg = claims_data[(claims_data["LargeLossIndicator"] == 0) & (claims_data["MarketCat"]  == "")]
            att_claims_data_agg = att_claims_data_agg.assign(TotalIncurred = lambda x: np.where(x.SignedLineMultiplier > 0,
                                                                                                x.BeazleyShareTotalIncurredInUSD / x.SignedLineMultiplier,
                                                                                                x.BeazleyShareTotalIncurredInUSD))
            att_claims_data_agg = att_claims_data_agg.groupby("PolicyYOA",as_index=False)["TotalIncurred"].agg({"TotalIncurred":"sum"})
            att_claims_data_agg.columns.values[1] = "att_incurred"

            large_claims_data_agg = claims_data[(claims_data["LargeLossIndicator"] == 1) & (claims_data["MarketCat"]  == "")]
            large_claims_data_agg = large_claims_data_agg.assign(TotalIncurred = lambda x: np.where(x.SignedLineMultiplier > 0,
                                                                                                x.BeazleyShareTotalIncurredInUSD / x.SignedLineMultiplier,
                                                                                                x.BeazleyShareTotalIncurredInUSD))
            large_claims_data_agg = large_claims_data_agg.groupby("PolicyYOA",as_index=False)["TotalIncurred"].agg({"TotalIncurred":"sum"})
            large_claims_data_agg.columns.values[1] = "large_incurred"

            cat_claims_data_agg = claims_data[(claims_data["MarketCat"]  != "")]
            cat_claims_data_agg = cat_claims_data_agg.assign(TotalIncurred = lambda x: np.where(x.SignedLineMultiplier > 0,
                                                                                                x.BeazleyShareTotalIncurredInUSD / x.SignedLineMultiplier,
                                                                                                x.BeazleyShareTotalIncurredInUSD))
            # SA: I think calling assign is overkill. You should be able to just use:
            # cat_claims_data_agg['TotalIncurred'] = np.where(x.SignedLineMultiplier > 0,
            #                                                 x.BeazleyShareTotalIncurredInUSD / x.SignedLineMultiplier,
            #                                                 x.BeazleyShareTotalIncurredInUSD)
            cat_claims_data_agg = cat_claims_data_agg.groupby("PolicyYOA",as_index=False)["TotalIncurred"].agg({"TotalIncurred":"sum"})
            cat_claims_data_agg.columns.values[1] = "cat_incurred"

            # E) BI calculations and assign to nodes

            ## claims
            claims_data = claims_data.loc[:,["PolicyYOA","ClaimReference","BeazleyShareTotalOutstandingInUSD","BeazleyShareTotalIncurredInUSD","CauseOfLoss"]]
            claims_data.columns.values[0:6] = ["yoa","claim_ref","outstanding","incurred","description"]
            claims_data = claims_data.sort_values(by = ["incurred"], ascending = False).iloc[0:10]
            setattr(cds,"experience_top_10_claims_bi",claims_data.to_dict("records"))


            ## premium ~~~~
            prem_temp = summary_table.loc[:,["YOA","TotalWEP","RateChangeReformat","rc_index","ol_prem"]]
            prem_temp.columns.values[0:5] = ["yoa","gnwp","rate_change","rate_change_index","gnwp_onlvl"]
            prem_temp = prem_temp.fillna(0)
            setattr(cds,"experience_gnwp_summary",prem_temp.to_dict("records"))

            ## attritional ultimate ~~~~
            summary_table = pd.merge(summary_table,att_claims_data_agg.rename(columns={"PolicyYOA":"YOA"}) ,how="left",on="YOA")
            summary_table = summary_table.fillna(0)
            summary_table = summary_table.assign(att_ult = lambda x: np.where(x.dev > 0.7, x.att_incurred/x.dev, x.att_incurred + (1-x.dev) * x.ol_prem * x.ielr))

            att_temp = summary_table.loc[:,["YOA","att_incurred","dev","ielr","att_ult"]]
            att_temp.columns.values[0:5] = ["yoa","incurred","dev_factor","ielr","ultimate"]
            att_temp = att_temp.fillna(0)
            setattr(cds,"experience_attr_projection",att_temp.to_dict("records"))

            ## large ultimate ~~~~
            summary_table = pd.merge(summary_table,large_claims_data_agg.rename(columns={"PolicyYOA":"YOA"}) ,how="left",on="YOA")
            summary_table = summary_table.fillna(0)
            average_ll_lr = summary_table[summary_table["dev"]> 0.75]["large_incurred"].sum() / summary_table[summary_table["dev"]> 0.75]["TotalWEP"].sum()
            if average_ll_lr != average_ll_lr:
                average_ll_lr = 0
            credible_years = summary_table.loc[(summary_table["YOA"] < (policy_year-1)) & (summary_table["TotalWEP"]>0)].agg({"TotalWEP":"count"}).iloc[0] or 1
            credibility_table = hx.params.table_input_experience_credibility
            weight = credibility_table.loc[credibility_table["Years"]<=credible_years]["Weight"].iloc[-1]
            weighted_lr = bp_ll_lr * weight + average_ll_lr * (1-weight)
            summary_table = summary_table.assign(large_ult = lambda x: weighted_lr* x.ol_prem )

            large_temp = summary_table.loc[:,["YOA","large_ult" ]]
            large_temp.columns.values[0:2] = ["yoa","ultimate"]
            large_temp.loc[:,["ll_avg_lr","ll_assumption","ll_weighted"]] = [average_ll_lr,bp_ll_lr,weighted_lr]
            large_temp = large_temp.fillna(0)
            setattr(cds,"experience_large_projection",large_temp.to_dict("records"))

            ## cat ultimate ~~~~
            summary_table = pd.merge(summary_table,cat_claims_data_agg.rename(columns={"PolicyYOA":"YOA"}) ,how="left",on="YOA")
            summary_table = summary_table.fillna(0)
            prem_inc_for_weight = summary_table.loc[(summary_table["YOA"] < (policy_year-1)) & (summary_table["TotalWEP"]>0)].agg({"ol_prem":"sum","cat_incurred":"sum"})
            summary_table = summary_table.assign(average_cat = lambda x: (prem_inc_for_weight.iloc[1]/prem_inc_for_weight.iloc[0]) * x.ol_prem,
                                                rms_implied = lambda x: x.ol_prem * cds.experience_rms_defaults.rms_cat_lr.selected)
            summary_table = summary_table.replace(np.nan,0)
            summary_table = summary_table.assign(cat_ult = lambda x: np.maximum(x.average_cat,x.rms_implied))

            cat_temp = summary_table.loc[:,["YOA","cat_incurred","average_cat","rms_implied","cat_ult"]]
            cat_temp.columns.values[0:5] = ["yoa","cat_incurred","cat_average","cat_rms","ultimate"]
            cat_temp = cat_temp.fillna(0)
            setattr(cds,"experience_cat_projection",cat_temp.to_dict("records"))

            ## total ultimate ~~~~
            summary_table = summary_table.assign(total_ult = lambda x: x.att_ult + x.large_ult + x.cat_ult,
                                                 infl_index = lambda x: (1+bp_infl)**(policy_year - x.YOA) )
            summary_table = summary_table.assign(total_infl_ult = lambda x: (x.att_ult + x.large_ult) * x.infl_index + np.where(x.cat_ult == x.average_cat,x.cat_ult * x.infl_index,x.cat_ult) )
            summary_table = summary_table.assign(att_infl_ult = lambda x: x.att_ult * x.infl_index,
                                                 large_infl_ult = lambda x: x.large_ult * x.infl_index,
                                                 cat_infl_ult = lambda x: np.where(x.cat_ult == x.average_cat,x.cat_ult * x.infl_index,x.cat_ult))

            summary_table = summary_table.assign(ulr_total = lambda x: np.where(x.ol_prem > 0, x.total_infl_ult/x.ol_prem,0))
            

            ####### this needs to be changed!!!!!!! at the moment its just fixed at 5 rows!!!!!!!!!!!!!!!!!!!!!!!!!! #TODO
            total_temp = summary_table.loc[:,["YOA","total_ult","infl_index","total_infl_ult","ulr_total"]]
            total_temp.columns.values[0:5] = ["yoa","ult_incurred","inf_index","ult_incurred_inf","ulr"]
            total_temp = total_temp.fillna(0)
            # total_temp["include"] = True
            # util.write_pd_to_hxd(total_temp,cds.experience_ult_claims,["yoa","ult_incurred","inf_index","ult_incurred_inf"])
            # setattr(hxd,"experience_ult_claims",total_temp.to_dict("records"))

            for schedule_row, df_row in zip(cds.experience_ult_claims, total_temp.iloc):
                schedule_row.yoa = df_row["yoa"]
                schedule_row.ult_incurred = df_row["ult_incurred"]
                schedule_row.inf_index = df_row["inf_index"]
                schedule_row.ult_incurred_inf = df_row["ult_incurred_inf"]
                schedule_row.ulr = df_row["ulr"]

            ## final calcs ~~~~
            #summary_table = summary_table.loc[summary_table["ol_prem"] > 0 ]
            previous_ol_prem = summary_table.loc[summary_table["YOA"] == policy_year-1]["ol_prem"].iloc[0]
            summary_table = summary_table.assign(exposure_factor = lambda x: x.ol_prem / previous_ol_prem if previous_ol_prem > 0 else 1.0)
            summary_table = summary_table.assign(decay_factor = lambda x: 0.9**(policy_year - x.YOA) )

            final_temp = util.pd_df_from_hx_list(cds.experience_ult_claims)
            final_temp = final_temp.loc[final_temp["yoa"] == final_temp["yoa"]]
            summary_table = pd.merge(summary_table,final_temp.rename(columns={"yoa":"YOA"}), how = "left",on = "YOA")
            summary_table = summary_table.assign(weight = lambda x: x.dev * x.exposure_factor * x.decay_factor * x.include )
            total_weight = summary_table["weight"].sum()
            # summary_table = summary_table.assign(ulr = lambda x: x.total_infl_ult/x.ol_prem)
            summary_table.loc[:,"weight"] = summary_table.loc[:,"weight"] / total_weight if total_weight > 0 else 0.0
            ulr_final = (summary_table["weight"] * summary_table["ulr_total"]).sum()
            
            lr_temp = summary_table.loc[:,["YOA","TotalWEP","ol_prem","att_incurred","large_incurred","cat_incurred","total_ult","total_infl_ult","att_infl_ult","large_infl_ult","cat_infl_ult"]]
            lr_temp.columns.values[0:2] = ["yoa","gnwp"]
            lr_temp = lr_temp.assign(incurred = lambda x: (x.att_incurred + x.large_incurred + x.cat_incurred),
                                    ilr = lambda x: np.where(x.gnwp > 0, (x.att_incurred + x.large_incurred + x.cat_incurred) / x.gnwp,0),
                                    ulr_inf = lambda x: np.where(x.ol_prem > 0, x.total_infl_ult / x.ol_prem, 0),
                                    ulr = lambda x: np.where(x.gnwp, x.total_ult / x.gnwp,0))
            
            lr_temp = lr_temp.assign(attr_ulr = lambda x: np.where(x.ol_prem > 0, x.att_infl_ult / x.ol_prem,0),
                                     large_ulr = lambda x: np.where(x.ol_prem > 0,x.large_infl_ult / x.ol_prem,0),
                                     cat_ulr = lambda x: np.where(x.ol_prem > 0, x.cat_infl_ult / x.ol_prem,0)
                                    )
            
            lr_temp = lr_temp.fillna(0)

            lr_temp_summaries = lr_temp.loc[:,["yoa","gnwp", "ilr","ulr","ulr_inf"]]
            lr_temp_summaries = lr_temp_summaries.tail(7) # force just last 5 years in summary table
            setattr(cds,"experience_lr_summary_list",lr_temp_summaries.to_dict("records"))

            lr_temp_summaries = lr_temp_summaries.loc[:, ["yoa","ilr","ulr_inf"]]
            lr_temp_summaries.columns.values[2] = "ulr"
            setattr(cds,"experience_lr_summaries",lr_temp_summaries.to_dict("records"))

            # G) Final Selections
            cds.experience_final_selections_model.gn_ulr = ulr_final

            max_cred = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Max_Cred"][risk_class_code].iloc[0]
            ly_prem = lr_temp.loc[lr_temp["yoa"] == policy_year - 1, "gnwp"].iloc[0]
            cds.experience_final_selections_model.ly_prem = ly_prem
            cds.experience_final_selections_model.exp_weight = min(1, math.sqrt(ly_prem * curr_rate / max_cred))
            cds.experience_final_selections_uw.exp_weight = cds.final_claims_summary_table.sel_exp_weight


            for i in [1,2]:
                path = f'experience_lr_summary_subtotal_{i}'

                if i == 1:
                    subtotal = lr_temp.agg({"gnwp":"sum","ol_prem":"sum","incurred":"sum","total_ult":"sum","total_infl_ult":"sum"})
                elif i == 2:
                    subtotal = lr_temp.loc[lr_temp["yoa"] < policy_year - 1 ].agg({"gnwp":"sum","ol_prem":"sum","incurred":"sum","total_ult":"sum","total_infl_ult":"sum"})

                if subtotal["gnwp"] > 0:
                    subtotal["ilr"] = subtotal["incurred"] / subtotal["gnwp"]
                    subtotal["ulr"] = subtotal["total_ult"] / subtotal["gnwp"]
                    subtotal["ulr_inf"] = subtotal["total_infl_ult"] / subtotal["ol_prem"] if subtotal["ol_prem"] > 0 else 0
                    subtotal = subtotal.loc[["gnwp","ilr","ulr","ulr_inf"]]
                    subtotal = subtotal.fillna(0)
                else:
                    subtotal["gnwp"] = 0
                    subtotal["ilr"] = 0
                    subtotal["ulr"] = 0
                    subtotal["ulr_inf"] = 0
                    subtotal = subtotal.loc[["gnwp","ilr","ulr","ulr_inf"]]
                    
                setattr(cds,path,subtotal.to_dict())

            # H) Detailed
            cds.experience_detailed.trifocus = "Jewellers" if risk_class_code == "JB" else "Fine Art and Specie"
            cds.experience_detailed.bp_rc = bp_rc
            cds.experience_detailed.infl = bp_infl
            cds.experience_detailed.ll_threshold = bp_ll_threshold
            cds.experience_detailed.ll_load = bp_ll_lr
            cds.experience_detailed.cat_load = bp_cat_lr

            # I) POPULATE CHARTS
            lr_chart_summary = lr_temp.loc[:,["yoa","gnwp", "ilr","ulr"]]
            lr_chart_summary["sel_ulr"] = cds.experience_final_selections_model.gn_ulr
            lr_chart_summary["uw_ulr"] = cds.experience_final_selections_uw.gn_ulr

            setattr(cds,"experience_loss_ratio_summary_chart",lr_chart_summary.to_dict("records"))

            lr_chart_type = lr_temp.loc[:,["yoa","attr_ulr", "large_ulr","cat_ulr"]]

            setattr(cds,"experience_loss_ratio_type_chart",lr_chart_type.to_dict("records"))

            # SA: this is a very long function - it'd be more understandable broken out into separate functions that are sequentially ran,
            # like you've done for rating

            # SA: Also, nice efficient pandas code in this section! 
    return 


def rate_experience_rating_manual(hxd, df):
    cds = hxd.cds
    cov = cds.layers[0].coverages

    # 0. DECLARE GLOBAL PARAMETERS --------------------
    cds.experience_rms_defaults.rms_cat_lr.calculated = global_params.experience_rms_cat_lr
    cds.bi_masking = True if cds.experience_rating.data_source == "BI" else False
    cds.manual_masking = True if cds.experience_rating.data_source == "Manual" else False
    cds.experience_rating.policy_ref = cds.standard_fields.policy_reference

    if len(hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]) > 0:
        risk_class_code = hx.params.table_input_classes_tag[hx.params.table_input_classes_tag["classes"] == cds.standard_fields.benchmark_class]["tag"].iloc[0]
    else:
        risk_class_code = ""

    if risk_class_code != "":

        # A) set parameters 
        policy_data = hx.params.table_input_experience_policy_data
        claims_data = hx.params.table_input_experience_claim_data

        policy_year = hxd.hx_core.inception_date.year or 2023
        policy_month = hxd.hx_core.inception_date.month or 1
        policy_ref  = cds.standard_fields.policy_reference # "JCT61L23ANYJ" 
        index_ref = policy_ref[:6] + policy_ref[8:]
        curr =  cds.currencies.source_currency
        curr_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == curr]["fx_rate"].iloc[0]

        # B) class specific data
        if risk_class_code == "JB":
            ielr_table = hx.params.table_input_experience_ielr[["YOA", "Jewellers"]]
            dfm_pattern = hx.params.table_input_experience_dfm[["Development Month", "Jewellers"]]
        else:
            ielr_table = hx.params.table_input_experience_ielr[["YOA", "Fine Art and Specie"]]
            dfm_pattern = hx.params.table_input_experience_dfm[["Development Month", "Fine Art and Specie"]]

        # SA: Should save hx.params.table_input_experience_class_params to a variable to avoid loading from hx.params each time 
        bp_infl = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Inflation"][risk_class_code].iloc[0]
        bp_rc = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "RC"][risk_class_code].iloc[0]
        bp_ll_lr = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"]=="LcLoad"][risk_class_code].iloc[0]
        bp_cat_lr = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Cat"][risk_class_code].iloc[0]
        bp_ll_threshold = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "LargeLoss"][risk_class_code].iloc[0]

        cds.experience_rms_defaults.rms_cat_lr.calculated = bp_cat_lr
        
        if cds.manual_masking:


            # F) manual calculations and assign to nodes
            manual_summary_table = pd.DataFrame( {"yoa" : list(range(policy_year - 10,policy_year))})
            util.write_pd_to_hxd(manual_summary_table,cds.experience_gnwp_summary_manual,["yoa"])
            util.write_pd_to_hxd(manual_summary_table,cds.experience_attr_projection_manual,["yoa"])
            util.write_pd_to_hxd(manual_summary_table,cds.experience_large_projection_manual,["yoa"])
            util.write_pd_to_hxd(manual_summary_table,cds.experience_cat_projection_manual,["yoa"])
            util.write_pd_to_hxd(manual_summary_table,cds.experience_ult_claims_manual,["yoa"])

            # for schedule_row, df_row in zip(cds.experience_gnwp_summary_manual, manual_summary_table.iloc):
            #     schedule_row.yoa = df_row["yoa"]

            # for schedule_row, df_row in zip(cds.experience_attr_projection_manual, manual_summary_table.iloc):
            #     schedule_row.yoa = df_row["yoa"]

            # for schedule_row, df_row in zip(cds.experience_large_projection_manual, manual_summary_table.iloc):
            #     schedule_row.yoa = df_row["yoa"]

            # for schedule_row, df_row in zip(cds.experience_cat_projection_manual, manual_summary_table.iloc):
            #     schedule_row.yoa = df_row["yoa"]

            # for schedule_row, df_row in zip(cds.experience_ult_claims_manual, manual_summary_table.iloc):
            #     schedule_row.yoa = df_row["yoa"]
            

            ## premium
            manual_summary_table = util.pd_df_from_hx_list(cds.experience_gnwp_summary_manual)
            manual_summary_table["rate_change_index"] = manual_summary_table["rate_change"][::-1].cumprod()[::-1]
            manual_summary_table = manual_summary_table.assign(ol_prem = lambda x: x.gnwp * x.rate_change_index)

            manual_prem_temp = manual_summary_table.loc[:,["rate_change_index","ol_prem"]]
            manual_prem_temp.columns.values[1] = "gnwp_onlvl"
            # util.write_pd_to_hxd(manual_prem_temp,cds.experience_gnwp_summary_manual,["rate_change_index","gnwp_onlvl"])

            manual_prem_temp = manual_prem_temp.fillna(0)

            for schedule_row, df_row in zip(cds.experience_gnwp_summary_manual, manual_prem_temp.iloc):
                schedule_row.rate_change_index = df_row["rate_change_index"]
                schedule_row.gnwp_onlvl = df_row["gnwp_onlvl"]

            ## attritional claims
            manual_att = util.pd_df_from_hx_list(cds.experience_attr_projection_manual)
            manual_att = manual_att.loc[:,["yoa","total_incurred","large_cat"]]
            manual_att["Development Month"] = np.minimum((policy_year - manual_att["yoa"])*12 + policy_month,50)
            manual_att = pd.merge(manual_att,dfm_pattern,how="left", on = "Development Month")
            manual_att = pd.merge(manual_att,ielr_table,how="left", left_on = "yoa", right_on = "YOA")
            manual_att.columns.values[4:7] = ["dev","YOA","ielr"]
            manual_att = manual_att.assign(att_incurred = lambda x: x.total_incurred - x.large_cat)
            manual_summary_table = pd.merge(manual_summary_table,manual_att, how = "left", on = "yoa")
            manual_summary_table = manual_summary_table.assign(att_ult = lambda x: np.where(x.dev > 0.7, x.att_incurred/x.dev, x.att_incurred + (1-x.dev) * x.ol_prem * x.ielr))

            manual_att_temp = manual_summary_table.loc[:,["yoa","att_incurred","dev","ielr","att_ult"]]
            manual_att_temp.columns.values[1:5] = ["incurred","dev_factor","ielr","ultimate"]
            # util.write_pd_to_hxd(manual_att_temp,cds.experience_attr_projection_manual,["yoa","incurred","dev_factor","ielr","ultimate"])

            manual_att_temp = manual_att_temp.fillna(0)

            for schedule_row, df_row in zip(cds.experience_attr_projection_manual, manual_att_temp.iloc):
                schedule_row.yoa = df_row["yoa"]
                schedule_row.incurred = df_row["incurred"]
                schedule_row.dev_factor = df_row["dev_factor"]
                schedule_row.ielr = df_row["ielr"]
                schedule_row.ultimate = df_row["ultimate"]

            ## large claims
            manual_large = util.pd_df_from_hx_list(cds.experience_large_projection_manual)
            manual_large = manual_large.loc[:,["yoa","ll_assumption","ll_selected","ll_uw_view"]]
            bp_ll_lr = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"]=="LcLoad"][risk_class_code].iloc[0]
            manual_large = manual_large.assign(ll_selected = lambda x: np.maximum(x.ll_uw_view,bp_ll_lr),
                                            ll_assumption = bp_ll_lr)
            manual_summary_table = pd.merge(manual_summary_table, manual_large, how = "left", on = "yoa")
            manual_summary_table = manual_summary_table.assign(ll_ultimate = lambda x: x.ol_prem * x.ll_selected)

            manual_large_temp = manual_summary_table.loc[:,["yoa","ll_assumption","ll_selected","ll_ultimate"]]
            manual_large_temp.columns.values[3] = "ultimate"
            # util.write_pd_to_hxd(manual_large_temp,cds.experience_large_projection_manual,["yoa","ll_assumption","ll_selected","ultimate"])

            manual_large_temp = manual_large_temp.fillna(0)

            for schedule_row, df_row in zip(cds.experience_large_projection_manual, manual_large_temp.iloc):
                schedule_row.yoa = df_row["yoa"]
                schedule_row.ll_assumption = df_row["ll_assumption"]
                schedule_row.ll_selected = df_row["ll_selected"]
                schedule_row.ultimate = df_row["ultimate"]

            ## cat claims
            manual_cat = util.pd_df_from_hx_list(cds.experience_cat_projection_manual)
            manual_cat = manual_cat.loc[:,["yoa","cat_uw_view"]]
            manual_cat = manual_cat.assign(cat_bp = bp_cat_lr,cat_rms = cds.experience_rms_defaults.rms_cat_lr.selected)
            manual_summary_table = pd.merge(manual_summary_table,manual_cat, how = "left", on = "yoa")
            manual_summary_table = manual_summary_table.assign(cat_ult = lambda x: np.where(x.cat_uw_view > 0, x.cat_uw_view * x.ol_prem, x.cat_rms * x.ol_prem) )
            
            manual_cat_temp = manual_summary_table.loc[:,["yoa","cat_bp","cat_rms","cat_ult"]]
            manual_cat_temp.columns.values[3] = "ultimate"
            # util.write_pd_to_hxd(manual_cat_temp,cds.experience_cat_projection_manual,["yoa","cat_bp","cat_rms","ultimate"])

            manual_cat_temp = manual_cat_temp.fillna(0)

            for schedule_row, df_row in zip(cds.experience_cat_projection_manual, manual_cat_temp.iloc):
                schedule_row.yoa = df_row["yoa"]
                schedule_row.cat_bp = df_row["cat_bp"]
                schedule_row.cat_rms = df_row["cat_rms"]
                schedule_row.ultimate = df_row["ultimate"]

            ## final calcs ~~~~
            bp_infl = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Inflation"][risk_class_code].iloc[0]
            manual_summary_table = manual_summary_table.assign(total_ult = lambda x: x.att_ult + x.ll_ultimate + x.cat_ult,
                                                               infl_index = lambda x: (1+bp_infl)**(policy_year - x.YOA) )
            manual_summary_table = manual_summary_table.assign(total_infl_ult = lambda x: (x.att_ult + x.ll_ultimate) * x.infl_index + np.where(x.cat_ult == x.cat_rms,x.cat_ult,x.cat_ult * x.infl_index) )
            manual_summary_table = manual_summary_table.assign(att_infl_ult = lambda x: x.att_ult * x.infl_index,
                                                               large_infl_ult = lambda x: x.ll_ultimate * x.infl_index,
                                                               cat_infl_ult = lambda x: np.where(x.cat_ult == x.cat_rms,x.cat_ult,x.cat_ult * x.infl_index))

            manual_summary_table = manual_summary_table.assign(ulr_total = lambda x: np.where(x.ol_prem > 0, x.total_infl_ult/x.ol_prem,0))

            manual_total_temp = manual_summary_table.loc[:,["YOA","total_ult","infl_index","total_infl_ult","ulr_total"]]
            manual_total_temp.columns.values[0:5] = ["yoa","ult_incurred","inf_index","ult_incurred_inf","ulr"]
            # util.write_pd_to_hxd(manual_total_temp,cds.experience_ult_claims_manual,["yoa","ult_incurred","inf_index","ult_incurred_inf"])

            manual_total_temp = manual_total_temp.fillna(0)

            for schedule_row, df_row in zip(cds.experience_ult_claims_manual, manual_total_temp.iloc):
                schedule_row.yoa = df_row["yoa"]
                schedule_row.ult_incurred = df_row["ult_incurred"]
                schedule_row.inf_index = df_row["inf_index"]
                schedule_row.ult_incurred_inf = df_row["ult_incurred_inf"]
                schedule_row.ulr = df_row["ulr"]

            if manual_summary_table.loc[manual_summary_table["YOA"] == policy_year-1].shape[0] > 0:
                previous_ol_prem = manual_summary_table.loc[manual_summary_table["YOA"] == policy_year-1]["ol_prem"].iloc[0]
            else:
                previous_ol_prem = 0
            manual_summary_table = manual_summary_table.assign(exposure_factor = lambda x: x.ol_prem / previous_ol_prem if previous_ol_prem > 0 else 1.0)
            manual_summary_table = manual_summary_table.assign(decay_factor = lambda x: 0.9**(policy_year - x.YOA) )

            final_temp = util.pd_df_from_hx_list(cds.experience_ult_claims_manual)
            final_temp = final_temp.loc[final_temp["yoa"] == final_temp["yoa"]]
            final_temp = final_temp.loc[:,["yoa","include"]]
            manual_summary_table = pd.merge(manual_summary_table,final_temp.rename(columns={"yoa":"YOA"}), how = "left",on = "YOA")
            manual_summary_table = manual_summary_table.assign(weight = lambda x: x.dev * x.exposure_factor * x.decay_factor * x.include )
            total_weight_manual = manual_summary_table["weight"].sum()
            #manual_summary_table = manual_summary_table.assign(ulr = lambda x: x.total_infl_ult/x.ol_prem)
            manual_summary_table.loc[:,"weight"] = manual_summary_table.loc[:,"weight"] / total_weight_manual if total_weight_manual > 0 else 0.0
            ulr_final = (manual_summary_table["weight"] * manual_summary_table["ulr_total"]).sum()

            lr_temp = manual_summary_table.loc[:,["yoa","total_incurred","gnwp","ol_prem","total_ult","total_infl_ult","att_infl_ult","large_infl_ult","cat_infl_ult"]]
            lr_temp.columns.values[1] = "incurred"
            lr_temp = lr_temp.assign(ilr = lambda x: np.where(x.gnwp > 0, (x.incurred) / x.gnwp,0),
                                    ulr_inf = lambda x: np.where(x.ol_prem > 0, x.total_infl_ult / x.ol_prem,0),
                                    ulr = lambda x: np.where(x.gnwp > 0, x.total_ult / x.gnwp,0) )

            lr_temp = lr_temp.assign(attr_ulr = lambda x: np.where(x.ol_prem > 0, x.att_infl_ult / x.ol_prem,0),
                                     large_ulr = lambda x: np.where(x.ol_prem > 0,x.large_infl_ult / x.ol_prem,0),
                                     cat_ulr = lambda x: np.where(x.ol_prem > 0, x.cat_infl_ult / x.ol_prem,0)
                                    )

            lr_temp = lr_temp.fillna(0)

            lr_temp_summaries = lr_temp.loc[:,["yoa","gnwp", "ilr","ulr","ulr_inf"]]
            lr_temp_summaries = lr_temp_summaries.tail(7) # force just last 5 years in summary table
            setattr(cds,"experience_lr_summary_list",lr_temp_summaries.to_dict("records"))
            
            lr_temp_summaries = lr_temp_summaries.loc[:,["yoa","ilr","ulr"]]
            setattr(cds,"experience_lr_summaries_manual",lr_temp_summaries.to_dict("records"))

            # for schedule_row, df_row in zip(cds.experience_ult_claims_manual, final_temp.iloc):
            #     # schedule_row.yoa = df_row["yoa"]
            #     schedule_row.ult_incurred = df_row["ult_incurred"]
            #     schedule_row.inf_index = df_row["inf_index"]
            #     schedule_row.ult_incurred_inf = df_row["ult_incurred_inf"]

            # G) Final Selections
            # SA: Again these sections may be good candidates for smaller functions!
            
            cds.experience_final_selections_model.gn_ulr = ulr_final

            max_cred = hx.params.table_input_experience_class_params[hx.params.table_input_experience_class_params["Category"] == "Max_Cred"][risk_class_code].iloc[0]
            if lr_temp[lr_temp["yoa"] == policy_year - 1].shape[0] > 0:
                ly_prem = lr_temp.loc[lr_temp["yoa"] == policy_year - 1, "gnwp"].iloc[0]
            else:
                ly_prem = 0
            cds.experience_final_selections_model.ly_prem = ly_prem
            cds.experience_final_selections_model.exp_weight = min(1, math.sqrt(ly_prem * curr_rate / max_cred))
            cds.experience_final_selections_uw.exp_weight = cds.final_claims_summary_table.sel_exp_weight

            for i in [1,2]:
                path = f'experience_lr_summary_subtotal_{i}'

                if i == 1:
                    subtotal = lr_temp.agg({"gnwp":"sum","ol_prem":"sum","incurred":"sum","total_ult":"sum","total_infl_ult":"sum"})
                elif i == 2:
                    subtotal = lr_temp.loc[lr_temp["yoa"] < policy_year - 1 ].agg({"gnwp":"sum","ol_prem":"sum","incurred":"sum","total_ult":"sum","total_infl_ult":"sum"})

                if subtotal["gnwp"] > 0:
                    subtotal["ilr"] = subtotal["incurred"] / subtotal["gnwp"]
                    subtotal["ulr"] = subtotal["total_ult"] / subtotal["gnwp"]
                    subtotal["ulr_inf"] = subtotal["total_infl_ult"] / subtotal["ol_prem"] if subtotal["ol_prem"] > 0 else 0
                    subtotal = subtotal.loc[["gnwp","ilr","ulr","ulr_inf"]]
                    subtotal = subtotal.fillna(0)
                else:
                    subtotal["gnwp"] = 0
                    subtotal["ilr"] = 0
                    subtotal["ulr"] = 0
                    subtotal["ulr_inf"] = 0
                    subtotal = subtotal.loc[["gnwp","ilr","ulr","ulr_inf"]]
                    
                setattr(cds,path,subtotal.to_dict())

            # H) Detailed
            cds.experience_detailed.trifocus = "Jewellers" if risk_class_code == "JB" else "Fine Art and Specie"
            cds.experience_detailed.bp_rc = bp_rc
            cds.experience_detailed.infl = bp_infl
            cds.experience_detailed.ll_threshold = bp_ll_threshold
            cds.experience_detailed.ll_load = bp_ll_lr
            cds.experience_detailed.cat_load = bp_cat_lr

            # I) POPULATE CHARTS
            lr_chart_summary = lr_temp.loc[:,["yoa","gnwp", "ilr","ulr"]]
            lr_chart_summary["sel_ulr"] = cds.experience_final_selections_model.gn_ulr
            lr_chart_summary["uw_ulr"] = cds.experience_final_selections_uw.gn_ulr

            setattr(cds,"experience_loss_ratio_summary_chart",lr_chart_summary.to_dict("records"))

            lr_chart_type = lr_temp.loc[:,["yoa","attr_ulr", "large_ulr","cat_ulr"]]

            setattr(cds,"experience_loss_ratio_type_chart",lr_chart_type.to_dict("records"))



    return 


