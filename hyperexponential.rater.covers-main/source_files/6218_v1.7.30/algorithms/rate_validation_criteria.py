##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### validation on lists i have used a for loop without an obvious vectorised method without the overhead of loading a dataframe.
### i considered a while loop as below but seemed overly complex for the rare time it can exit the function early.
    # if cds.rms.use_override:
    #     index = 0
    #     test = False        
    #     while (index < len(cds.rms.edm_epcurve)) and (test == False):
    #         if cds.rms.edm_epcurve[index].all_peril_override_at_acc_fx <0:
    #             hx.errors.validation(f"b RMS Override Exceedance Probability Curve (RMS Tab) has 1 or more negative values")
    #             test = True
    #         index +=1


import hx
import re


def rate_validation_criteria(hxd):
    
    cds     = hxd.cds

    ###########################################
    ### 1) Risk Information   
    ###########################################

    layer   = cds.layers[0]
    pc      = cds.profit_commission.scenarios[0]

    ## 1a) Risk Information - Account Details
    ###########################################
    if not cds.standard_fields.insured_name:
        hx.errors.validation(f"A Binder Name (Risk Information Tab) must be entered.")
    
    if not cds.standard_fields.underwriter:
        hx.errors.validation(f"An Underwriter (Risk Information Tab) must be entered.")

    # Matches reference
    reference_format = "......\d\d...."
    format_description = "6 char of any type, 2 digits and 4 chars of any type"

    if (cds.standard_fields.facility_reference is None)  or  (not re.fullmatch(reference_format, cds.standard_fields.facility_reference)):
        hx.errors.validation(f"The facility reference (Risk Information Tab) must be in the format of {format_description}")


    ## 1b) Risk Information - Business Line
    ###########################################
    if not cds.standard_fields.trifocus:
        hx.errors.validation(f"A Tri-Focus (Risk Information Tab) must be entered.")

    if (not cds.risk_info.proxy_trifocus) and (cds.risk_info.trifocus_valid == False):
        hx.errors.validation(f"A Proxy Tri-Focus (Risk Information Tab) must be entered.")

    ## 1c) Risk Information - Premium and Status
    ###########################################
    if (layer.quoted_premium_100pct is None) or  (layer.quoted_premium_100pct < 0):
        hx.errors.validation(f"EPI 100% (Risk Information Tab) greater than or equal to 0 must be entered")

    ## 1d) Check Renewal
    ###########################################
    if (cds.standard_fields.is_renewal is True) and (cds.bi_data.fetch_facility_detail_task_status == ""):
        hx.errors.validation(f"Load premium and claims history task needs rerunning")

    if (layer.signed_line is None)  or  (layer.signed_line < 0.000001) or (layer.signed_line > 1):
        hx.errors.validation(f"Signed Line (Risk Information Tab) between 0 and 1 must be entered")  

    if (layer.written_line is None)  or  (layer.written_line < 0) or (layer.written_line > 1):
        hx.errors.validation(f"Written Line (Risk Information Tab) between 0 and 1 must be entered")

    if (layer.expiry_signed_line is None)  or  (layer.expiry_signed_line < 0) or (layer.expiry_signed_line > 1):
         hx.errors.validation(f"Expiry Signed Line (Risk Information Tab) between 0 and 1 must be entered")

    if (layer.status != "Bound"):
        hx.errors.validation(f"Deal Status (Risk Information Tab) must be set to Bound prior to Finalising.")


    ## 1d) Risk Information - Fixed Deductions
    ###########################################
    if ((layer.commission is None)==False)          and   ((layer.commission < 0) or (layer.commission > 1)):
        hx.errors.validation(f"Commission (Risk Information Tab) between 0 and 1 must be entered")

    if ((layer.brokerage is None)==False)           and   ((layer.brokerage < 0) or (layer.brokerage > 1)):
        hx.errors.validation(f"Brokerage (Risk Information Tab) between 0 and 1 must be entered")

    if ((layer.ipt is None)==False)                 and   ((layer.ipt < 0) or (layer.ipt > 1)):
        hx.errors.validation(f"IPT (Risk Information Tab) between 0 and 1 must be entered")

    if ((layer.total_deductions is None)==False)    and   ((layer.total_deductions < 0) or (layer.total_deductions > 1)):
        hx.errors.validation(f"Total Deductions (Risk Information Tab) between 0 and 1 must be entered")


    ## 1e) Risk Information - Profit Commission
    ###########################################
    # threshold or standard
    if ((pc.additionalfeaturesindicator == "Threshold") or (pc.additionalfeaturesindicator == "No")): 
        if ((pc.share is None)==False)                              and   (pc.share < 0 or pc.share > 1):
            hx.errors.validation(f"Profit Commission Share (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.expenses is None)==False)                           and   (pc.expenses < 0 or pc.expenses > 1):
            hx.errors.validation(f"Profit Commission Expenses (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.deficit is None)==False)                            and   (pc.deficit < 0):
            hx.errors.validation(f"Profit Commission Deficit (Risk Information Tab) greater than or equal to 0 must be entered")

    # threshold or standard
    if (pc.additionalfeaturesindicator == "Threshold"):
        if ((pc.threshold_bonus_share1 is None)==False)              and   (pc.threshold_bonus_share1 < 0 or pc.threshold_bonus_share1 > 1):
            hx.errors.validation(f"Profit Commission Threshold Share (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.threshold_lr_cutoff1 is None)==False)                and   (pc.threshold_lr_cutoff1 < 0 or pc.threshold_lr_cutoff1 > 1):
            hx.errors.validation(f"Profit Commission Threshold LR (Risk Information Tab) between 0 and 1 must be entered")


    # sliding scale
    if (pc.additionalfeaturesindicator == "Sliding Scale"):
        if ((pc.slidingscale_bonus_lr is None)==False)              and   (pc.slidingscale_bonus_lr < 0   or   pc.slidingscale_bonus_lr > 1):
            hx.errors.validation(f"Profit Commission sliding scale -below- Net LR (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.slidingscale_bonus_scale is None)==False)           and   (pc.slidingscale_bonus_scale < 0   or   pc.slidingscale_bonus_scale > 1):
            hx.errors.validation(f"Profit Commission sliding scale -below- increase % (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.slidingscale_bonus_maxtotalpc is None)==False)      and   (pc.slidingscale_bonus_maxtotalpc < 0   or   pc.slidingscale_bonus_maxtotalpc > 1):
            hx.errors.validation(f"Profit Commission sliding scale -below- max profit commission (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.slidingscale_clawback_lr is None)==False)           and   (pc.slidingscale_clawback_lr < 0   or   pc.slidingscale_clawback_lr > 1):
            hx.errors.validation(f"Profit Commission sliding scale -above- Net LR (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.slidingscale_clawback_scale is None)==False)        and   (pc.slidingscale_clawback_scale < 0   or   pc.slidingscale_clawback_scale > 1):
            hx.errors.validation(f"Profit Commission sliding scale -above- decrease % (Risk Information Tab) between 0 and 1 must be entered")

        if ((pc.slidingscale_clawback_mintotalpc is None)==False)   and   (pc.slidingscale_clawback_mintotalpc < 0   or   pc.slidingscale_clawback_mintotalpc > 1):
            hx.errors.validation(f"Profit Commission sliding scale -above- min profit commission (Risk Information Tab) between 0 and 1 must be entered")


    if ((pc.result_exp_pc_payable_override is None)==False)     and   (pc.result_exp_pc_payable_override < 0):
        hx.errors.validation(f"Profit Commission Result Override (Profit Commission Tab) greater than or equal to 0 must be entered") ### adding here as more logical for base case

    if ((cds.profit_commission.consistent_pc_latest_param is None)==True)     or   (cds.profit_commission.consistent_pc_latest_param != "PC Parameters up to date"):
         hx.errors.validation(f"Profit Commission Calculation is not up to date, please run the calculation")



    ## 1f) Risk Information - Civil Unrest
    ###########################################

    if ((cds.risk_info.srcc_sublimit is None)==False)                              and   (cds.risk_info.srcc_sublimit < 0):
        hx.errors.validation(f"SRCC sub-limit (Risk Information Tab) greater than or equal to 0 must be entered")



    ###########################################
    ### 2) RMS
    ###########################################

    ## 2a) RMS - Summary Information
    ###########################################
    
    if cds.rms.use_override:
        if ((cds.rms.edm_summary.all_peril_override_at_acc_fx.aal is None))      or   (cds.rms.edm_summary.all_peril_override_at_acc_fx.aal < 0):
            hx.errors.validation(f"RMS Override AAL (RMS Tab) greater than or equal to 0 must be entered")

        if ((cds.rms.edm_summary.all_peril_override_at_acc_fx.std_dev is None))      or   (cds.rms.edm_summary.all_peril_override_at_acc_fx.std_dev < 0):
            hx.errors.validation(f"RMS Override Standard Deviation (RMS Tab) greater than or equal to 0 must be entered")

        if ((cds.rms.edm_summary.all_peril_override_at_acc_fx.prem is None))      or   (cds.rms.edm_summary.all_peril_override_at_acc_fx.prem < 0):
            hx.errors.validation(f"RMS Override Premium (RMS Tab) greater than or equal to 0 must be entered")


    ## 2b) RMS - EP Curve
    ###########################################
    if cds.rms.use_override:
        test = False
        for i in cds.rms.edm_epcurve:
            if (i.all_peril_override_at_acc_fx is None) == False:
                if i.all_peril_override_at_acc_fx <0:
                    test = True
        if test == True: hx.errors.validation(f"RMS Override Exceedance Probability Curve (RMS Tab) has 1 or more negative values")



    ###########################################
    ### 3) Triangle Projection
    ###########################################

    ## 3a) Triangle Projection - Experience Override list
    ###########################################
    test = False
    for i in cds.triangle_projection.incremental_dev_factor:
        if (i.experience_override is None) == False:
            if i.experience_override <= 0:
                test = True
    if test == True: hx.errors.validation(f"Experience Override - Development Factors (Triangle Projection Tab) has 1 or more negative/nil values")


    ## 3b) Triangle Projection - Experience Override Tail Factor
    ###########################################
    if (cds.triangle_projection.tail_factor.experience_override is None) == False:
        if (cds.triangle_projection.tail_factor.experience_override <= 0):
            hx.errors.validation(f"Experience Override - Tail Factor (Triangle Projection Tab) is negative/nil")


    ## 3c) Triangle Projection - Experience Weight
    ###########################################
    if (cds.triangle_projection.experience_weight.override is None) == False:
        if  (cds.triangle_projection.experience_weight.override < 0   or   cds.triangle_projection.experience_weight.override > 1):
            hx.errors.validation(f"Experience Override - Weight (Triangle Projection Tab) between 0 and 1 must be entered")



    ###########################################
    ### 4) Rating Summary
    ###########################################

    ## 4a) Rating Summary - policy_length_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.policy_length_override is None) == False:
            if i.policy_length_override <= 0:
                test = True
    if test == True: hx.errors.validation(f"Policy Length Override (Rating Summary Tab) has 1 or more values <=0")

    ## 4b) Rating Summary - port_chg_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.port_chg_override is None) == False:
            if i.port_chg_override <= 0:
                test = True
    if test == True: hx.errors.validation(f"Portfolio Change Override (Rating Summary Tab) has 1 or more values <=0")

    ## 4c) Rating Summary - rate_chg_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.rate_chg_override is None) == False:
            if i.rate_chg_override <= 0:
                test = True
    if test == True: hx.errors.validation(f"Rate Change Override (Rating Summary Tab) has 1 or more values <=0")

    ## 4d) Rating Summary - infl_chg_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.infl_chg_override is None) == False:
            if i.infl_chg_override < 0:
                test = True
    if test == True: hx.errors.validation(f"Inflation Change Override (Rating Summary Tab) has 1 or more values <0")

    ## 4e) Rating Summary - premium_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.premium_override is None) == False:
            if i.premium_override < 0:
                test = True
    if test == True: hx.errors.validation(f"Premium Override (Rating Summary Tab) has 1 or more negative values")

    ## 4f) Rating Summary - incurred_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.incurred_override is None) == False:
            if i.incurred_override < 0:
                test = True
    if test == True: hx.errors.validation(f"Incurred Total Override (Rating Summary Tab) has 1 or more negative values")

    ## 4g) Rating Summary - incurred_large_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.incurred_large_override is None) == False:
            if i.incurred_large_override < 0:
                test = True
    if test == True: hx.errors.validation(f"Incurred Large Override (Rating Summary Tab) has 1 or more negative values")

    ## 4h) Rating Summary - incurred_cat_override
    ###########################################
    test = False
    for i in cds.rating_summary.detail_by_year:
        if (i.incurred_cat_override is None) == False:
            if i.incurred_cat_override < 0:
                test = True
    if test == True: hx.errors.validation(f"Incurred Cat Override (Rating Summary Tab) has 1 or more negative values")

    ## 4i) Rating Summary - individual nodes
    ###########################################
    # attritional loss ratio override
    if (cds.rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_uw_override is None) == False:
        if  (cds.rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_uw_override < 0):
            hx.errors.validation(f"UW Loss Ratio Override - Attritional (Rating Summary Tab) has a negative number entered")

    # uw adjustment boundaries
    if (cds.rating_summary.summary_ratios.attritional.uw_adjustment is None) == False:
        if (   (cds.rating_summary.summary_ratios.attritional.uw_adjustment < -0.5)
            or (cds.rating_summary.summary_ratios.attritional.uw_adjustment > 2)):
            hx.errors.validation(f"UW Loss Ratio Adjustment - Attritional (Rating Summary Tab) needs to be between -50% and +200%")

    if (cds.rating_summary.summary_ratios.large.uw_adjustment is None) == False:
        if (   (cds.rating_summary.summary_ratios.large.uw_adjustment < -0.5)
            or (cds.rating_summary.summary_ratios.large.uw_adjustment > 2)):
            hx.errors.validation(f"UW Loss Ratio Adjustment - Large (Rating Summary Tab) needs to be between -50% and +200%")

    if (cds.rating_summary.summary_ratios.catastrophe.uw_adjustment is None) == False:
        if (   (cds.rating_summary.summary_ratios.catastrophe.uw_adjustment < -0.5)
            or (cds.rating_summary.summary_ratios.catastrophe.uw_adjustment > 2)):
            hx.errors.validation(f"UW Loss Ratio Adjustment - Catastrophe (Rating Summary Tab) needs to be between -50% and +200%")

    # uw commentary requirement
    if ((cds.rating_summary.summary_ratios.attritional.uw_adjustment                 is None) == False or
        (cds.rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_uw_override is None) == False     ):
        if (cds.rating_summary.summary_ratios.attritional.uw_rationale is None):
            hx.errors.validation(f"Loss Ratio Adjusted/Overriden - Attritional (Rating Summary Tab) needs rationale")

    if ((cds.rating_summary.summary_ratios.large.uw_adjustment                 is None) == False or
        (cds.rating_summary.summary_ratios.large.uw_override)):
        if (cds.rating_summary.summary_ratios.large.uw_rationale is None):        
            hx.errors.validation(f"Loss Ratio Adjusted/Overriden - Large (Rating Summary Tab) needs rationale")

    if ((cds.rating_summary.summary_ratios.catastrophe.uw_adjustment                 is None) == False or
        (cds.rating_summary.summary_ratios.catastrophe.uw_override)):
        if (cds.rating_summary.summary_ratios.catastrophe.uw_rationale is None):
            hx.errors.validation(f"Loss Ratio Adjusted/Overriden - Catastrophe (Rating Summary Tab) needs rationale")


    ###########################################
    ### 5) Profit Commission
    ###########################################

    pc_list = cds.profit_commission.scenarios

    ## 5a) Profit Commission - policy_length_override
    ###########################################
    
    test_share = False
    test_expenses = False
    test_deficit = False
    test_threshold_bonus_share = False
    test_threshold_lr_cutoff = False
    test_slidingscale_bonus_lr = False
    test_slidingscale_bonus_scale = False
    test_slidingscale_bonus_maxtotalpc = False
    test_slidingscale_clawback_lr = False
    test_slidingscale_clawback_scale = False
    test_slidingscale_clawback_mintotalpc = False
    test_result_exp_pc_payable_override = False

    for index, i in enumerate(cds.profit_commission.scenarios):
        if index > 0:   # we already handle the base case (0) under the risk information tab
            if ( (i.share                            is None) == False)  and  (i.share < 0                              or i.share > 1):                            test_share = True
            if ( (i.expenses                         is None) == False)  and  (i.expenses < 0                           or i.expenses > 1):                         test_expenses = True
            if ( (i.deficit                          is None) == False)  and  (i.deficit < 0):                                                                      test_deficit = True
            if ( (i.threshold_bonus_share1            is None) == False)  and  (i.threshold_bonus_share1 < 0              or i.threshold_bonus_share1 > 1):            test_threshold_bonus_share = True
            if ( (i.threshold_lr_cutoff1              is None) == False)  and  (i.threshold_lr_cutoff1 < 0                or i.threshold_lr_cutoff1 > 1):              test_threshold_lr_cutoff = True
            if ( (i.slidingscale_bonus_lr            is None) == False)  and  (i.slidingscale_bonus_lr < 0              or i.slidingscale_bonus_lr > 1):            test_slidingscale_bonus_lr = True
            if ( (i.slidingscale_bonus_scale         is None) == False)  and  (i.slidingscale_bonus_scale < 0           or i.slidingscale_bonus_scale > 1):         test_slidingscale_bonus_scale = True
            if ( (i.slidingscale_bonus_maxtotalpc    is None) == False)  and  (i.slidingscale_bonus_maxtotalpc < 0      or i.slidingscale_bonus_maxtotalpc > 1):    test_slidingscale_bonus_maxtotalpc = True
            if ( (i.slidingscale_clawback_lr         is None) == False)  and  (i.slidingscale_clawback_lr < 0           or i.slidingscale_clawback_lr > 1):         test_slidingscale_clawback_lr = True
            if ( (i.slidingscale_clawback_scale      is None) == False)  and  (i.slidingscale_clawback_scale < 0        or i.slidingscale_clawback_scale > 1):      test_slidingscale_clawback_scale = True
            if ( (i.slidingscale_clawback_mintotalpc is None) == False)  and  (i.slidingscale_clawback_mintotalpc < 0   or i.slidingscale_clawback_mintotalpc > 1): test_slidingscale_clawback_mintotalpc = True
            if ( (i.result_exp_pc_payable_override   is None) == False)  and  (i.result_exp_pc_payable_override < 0):                                               test_result_exp_pc_payable_override = True

    if test_share == True                            : hx.errors.validation(f"Profit Commission Scenarios - Share - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_expenses == True                         : hx.errors.validation(f"Profit Commission Scenarios - Expenses - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_deficit == True                          : hx.errors.validation(f"Profit Commission Scenarios - Deficit - (Profit Commission Tab) greater than or equal to 0 must be entered")
    if test_threshold_bonus_share == True            : hx.errors.validation(f"Profit Commission Scenarios - Threshold Share - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_threshold_lr_cutoff == True              : hx.errors.validation(f"Profit Commission Scenarios - Threshold LR - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_bonus_lr == True            : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- Net LR - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_bonus_scale == True         : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- increase % - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_bonus_maxtotalpc == True    : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- max profit commission - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_clawback_lr == True         : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- Net LR - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_clawback_scale == True      : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- increase % - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_slidingscale_clawback_mintotalpc == True : hx.errors.validation(f"Profit Commission Scenarios - sliding scale -below- max profit commission - (Profit Commission Tab) between 0 and 1 must be entered")
    if test_result_exp_pc_payable_override == True   : hx.errors.validation(f"Profit Commission Scenarios - Result Override - (Profit Commission Tab) greater than or equal to 0 must be entered")

    ############### Exposure Validation #################

 
