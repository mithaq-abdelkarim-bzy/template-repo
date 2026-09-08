##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

##############################################################################################################################


import hx
import pandas as pd
import numpy as np
import math as math
from algorithms.rate_utilities import pd_df_from_hx_list, write_pd_to_hxd, write_pd_to_hxd_no_overrides
from operator import itemgetter

def rate_profit_commission(hxd):

    
    
    cds = hxd.cds
    pc  = hxd.cds.profit_commission
    rs  = hxd.cds.rating_summary
    rms = cds.rms

    #prem = cds.layers[0].quoted_premium_100pct 


    if (cds.layers[0].quoted_premium_100pct  is None) == False    and    cds.layers[0].quoted_premium_100pct < 0:
        pc.consistent_pc_latest_param =  "Please resolve negative premium to proceed"
        return

    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        line_use = hxd.cds.layers[0].signed_line
    else:
        line_use = hxd.cds.layers[0].written_line
    
    # defaulting to 1 here unlike elsewhere in model so formulas dont give Div0  when divide gross to 100pct equivalent 

    signed_line = (line_use or 1)
    
    for i in range(10):    
        pc_i = pc.scenarios[i]
        pc_i.label    =      ("Base" if i==0 else f"Scenario {i}")
        
        pc_i.result_exp_pc_payable_selected = pc_i.result_exp_pc_payable        if pd.isnull(pc_i.result_exp_pc_payable_override)       else pc_i.result_exp_pc_payable_override

        if pc_i.additionalfeaturesindicator == "Sliding Scale":
            pc_i.complete = ((  (pc_i.slidingscale_bonus_lr                is None)
                                | (pc_i.slidingscale_bonus_scale             is None)
                                | (pc_i.slidingscale_bonus_maxtotalpc        is None)
                                | (pc_i.slidingscale_clawback_lr             is None)
                                | (pc_i.slidingscale_clawback_scale          is None)
                                | (pc_i.slidingscale_clawback_mintotalpc     is None)) == False
                              and (pc_i.slidingscale_bonus_lr           >=0 and pc_i.slidingscale_bonus_lr           <= 1)
                              and (pc_i.slidingscale_bonus_scale        >=0 and pc_i.slidingscale_bonus_scale        <= 1)
                              and (pc_i.slidingscale_bonus_maxtotalpc   >=0 and pc_i.slidingscale_bonus_maxtotalpc   <= 1)
                              and (pc_i.slidingscale_clawback_lr        >=0 and pc_i.slidingscale_clawback_lr        <= 1)
                              and (pc_i.slidingscale_clawback_scale     >=0 and pc_i.slidingscale_clawback_scale     <= 1)
                              and (pc_i.slidingscale_clawback_mintotalpc>=0 and pc_i.slidingscale_clawback_mintotalpc<= 1))

        elif pc_i.additionalfeaturesindicator == "Threshold":
            pc_i.complete = (( 
                                (pc_i.expenses                             is None)
                                | (pc_i.threshold_bonus_share1                is None)
                                | (pc_i.threshold_lr_cutoff1                  is None)) == False
                           
                              and (pc_i.expenses              >=0 and pc_i.expenses              <= 1)
                              and (pc_i.threshold_bonus_share1 >=0 and pc_i.threshold_bonus_share1 <= 1)
                              and (pc_i.threshold_lr_cutoff1   >=0 and pc_i.threshold_lr_cutoff1   <= 1)
                              and (pc_i.deficit or 0        ) >=0) 

        else:
            pc_i.complete = ((  (pc_i.share                                is None)
                                | (pc_i.expenses                             is None)) == False
                              and (pc_i.share                 >=0 and pc_i.share                 <= 1)
                              and (pc_i.expenses              >=0 and pc_i.expenses              <= 1)
                              and (pc_i.deficit or 0        ) >=0) 



    rms_available = (   (rms.edm_summary.all_peril_selected_at_acc_fx.aal         or 0) == 0
                        or (rms.edm_summary.all_peril_selected_at_acc_fx.std_dev  or 0) == 0
                        or (rms.edm_summary.all_peril_selected_at_acc_fx.gross_lr or 0) == 0
                        or (rms.edm_epcurve[11].all_peril_selected_at_acc_fx      or 0) == 0 # last value in list is 1 in 10000 testing if it is populated
                        or (rs.technical.amts_pst_uw_adj.losses_cat_afb           or 0) == 0
                    ) == False


    # calculate expected losses
    pc.param_attritional.expected_loss  = (rs.technical.amts_pst_uw_adj.losses_att_afb or 0) / signed_line
    pc.param_large.expected_loss        = (rs.technical.amts_pst_uw_adj.losses_lrg_afb or 0) / signed_line
    pc.param_cat_natural.expected_loss  = (rs.technical.amts_pst_uw_adj.losses_cat_afb or 0) / signed_line if rms_available else 0
    pc.param_cat_other.expected_loss    = (rs.technical.amts_pst_uw_adj.losses_cat_afb or 0) / signed_line if (rms_available == False) else 0



    # calculate benchmark cov's
    benchmark_parameters_df  = hx.params.table_benchmarkclassparameters 
    bench_df                 = benchmark_parameters_df[(benchmark_parameters_df['Benchmark Class'] == cds.standard_fields.benchmark_class)]

    att_cov                             = bench_df[(bench_df['Item'] == "Att COV") ]['Value']
    pc.param_attritional.cov_benchmark  = 0 if att_cov.empty else att_cov.iat[0]
 
    lrg_cov                             = bench_df[(bench_df['Item'] == "Large COV") ]['Value']
    pc.param_large.cov_benchmark        = 0 if att_cov.empty else lrg_cov.iat[0]

    cat_cov                             = bench_df[(bench_df['Item'] == "Cat COV") ]['Value']
    cat_cov                             = 0 if att_cov.empty else cat_cov.iat[0]
    pc.param_cat_natural.cov_benchmark  = cat_cov if rms_available else 0
    pc.param_cat_other.cov_benchmark    = cat_cov if (rms_available == False) else 0


    # calculate benchmark standard deviations
    pc.param_attritional.stdev_benchmark= pc.param_attritional.expected_loss  *  pc.param_attritional.cov_benchmark
    pc.param_large.stdev_benchmark      = pc.param_large.expected_loss        *  pc.param_large.cov_benchmark
    pc.param_cat_natural.stdev_benchmark= pc.param_cat_natural.expected_loss  *  pc.param_cat_natural.cov_benchmark
    pc.param_cat_other.stdev_benchmark  = pc.param_cat_other.expected_loss    *  pc.param_cat_other.cov_benchmark


    # calculate actual standard deviations - THESE NEED TO BE CODED BUT AS NOT ACTUALLY USED CURRENTLY SET TO ZERO - IT WOULD MAKE SENSE TO CALCULATE AND STORE IN a NODE AS PART OF RATIGN SUMMARY RATHER THAN IMPORT THEDF HERE AGAIN.
    pc.param_attritional.stdev_actual   = 0 if (pc.param_attritional.expected_loss==0)  else cds.rating_summary.standard_deviation.attritional 
    pc.param_large.stdev_actual         = 0 if (pc.param_large.expected_loss==0)        else cds.rating_summary.standard_deviation.large
    pc.param_cat_natural.stdev_actual   = 0 if (pc.param_cat_natural.expected_loss==0)  else cds.rating_summary.standard_deviation.catastrophe      #expected_loss==0 is used to infer which node catastrophe goes to
    pc.param_cat_other.stdev_actual     = 0 if (pc.param_cat_other.expected_loss==0)    else cds.rating_summary.standard_deviation.catastrophe      #expected_loss==0 is used to infer which node catastrophe goes to

    # calculate actual COVs
    pc.param_attritional.cov_actual     = 0 if (pc.param_attritional.expected_loss==0)  else (pc.param_attritional.stdev_actual / pc.param_attritional.expected_loss)
    pc.param_large.cov_actual           = 0 if (pc.param_large.expected_loss==0)        else (pc.param_large.stdev_actual       / pc.param_large.expected_loss)
    pc.param_cat_natural.cov_actual     = 0 if (pc.param_cat_natural.expected_loss==0)  else (pc.param_cat_natural.stdev_actual / pc.param_cat_natural.expected_loss)
    pc.param_cat_other.cov_actual       = 0 if (pc.param_cat_other.expected_loss==0)    else (pc.param_cat_other.stdev_actual   / pc.param_cat_other.expected_loss)

    # assign Client Weights - current assumption is Nil always
    pc.param_attritional.client_weight  = 0
    pc.param_large.client_weight        = 0
    pc.param_cat_natural.client_weight  = 0
    pc.param_cat_other.client_weight    = 0

    # calculate selected COVs
    pc.param_attritional.cov_selected   = (pc.param_attritional.cov_actual  *  pc.param_attritional.client_weight)  +  (pc.param_attritional.cov_benchmark  *  (1 - pc.param_attritional.client_weight))
    pc.param_large.cov_selected         = (pc.param_large.cov_actual        *  pc.param_large.client_weight)        +  (pc.param_large.cov_benchmark        *  (1 - pc.param_large.client_weight))    
    pc.param_cat_natural.cov_selected   = (pc.param_cat_natural.cov_actual  *  pc.param_cat_natural.client_weight)  +  (pc.param_cat_natural.cov_benchmark  *  (1 - pc.param_cat_natural.client_weight))
    pc.param_cat_other.cov_selected     = (pc.param_cat_other.cov_actual    *  pc.param_cat_other.client_weight)    +  (pc.param_cat_other.cov_benchmark    *  (1 - pc.param_cat_other.client_weight))

    # calculate selected standard deviations
    pc.param_attritional.stdev_selected = pc.param_attritional.expected_loss  *  pc.param_attritional.cov_selected
    pc.param_large.stdev_selected       = pc.param_large.expected_loss        *  pc.param_large.cov_selected
    pc.param_cat_natural.stdev_selected = pc.param_cat_natural.expected_loss  *  pc.param_cat_natural.cov_selected
    pc.param_cat_other.stdev_selected   = pc.param_cat_other.expected_loss    *  pc.param_cat_other.cov_selected

    # assign distribution
    pc.param_attritional.distribution   = "Log Normal(mu, sigma"
    pc.param_large.distribution         = "Pareto(shape, scale)"
    pc.param_cat_natural.distribution   = "Bespoke Exponential (alpha, beta)" # F(x) = 1 - alpha  *  exp{  beta * (x ^ 0.5) }
    pc.param_cat_other.distribution     = "Pareto(shape, scale)"

    # test whether sufficient data is available for fitting - THINK IF MORE CLEVER WAY TO CHECK IF ALL POINTS ON EP CURVE ARE AVAILABLE
    unavail_att                         = (pc.param_attritional.expected_loss<=0) | (pc.param_attritional.stdev_selected<=0)
    unavail_lrg                         = (pc.param_large.expected_loss<=0)       | (pc.param_large.stdev_selected<=0)
    unavail_cat_natural                 = (pc.param_cat_natural.expected_loss<=0) | (pc.param_cat_natural.stdev_selected<=0)   |  (rms_available==False)
    unavail_cat_other                   = (pc.param_cat_other.expected_loss<=0)   | (pc.param_cat_other.stdev_selected<=0)


    # helper calculation for natcat - load rms into df and fit a polynomial of order 1... a straight line
    # it maybe cleaner to calculate this directlty on rms sheet so we dont need to reload the dataframe here
    # notice it is calibrated off the afb loss amounts hence there is a large scalant applied in the simulation to bring it to 100% - ideally this would happen at outset
    
    ##################################################### equation explanation #####################################################
    ### for critical (survival) probability: y;   and loss amount x
    ### its is assumed that a linear curve can be fit once y and x are transformed appropriately
    ###       ln(y) = m   *  sqrt(x)   +  b;      
    ###           y = exp(b)       *   exp( m  *           sqrt(x) )              
    ###             = cat_nat_p1   *   exp( cat_nat_p2  *  (x ** 0.5) )                                                noting the b parameter gets exponentiated immediately below to give cat_nat_p1
    ###           x = [                1 / m         *    ln (  y                        / c)           ]  **2        re-expressing, where c = exp(b) 
    ###             =  np.maximum(0,  (1/cat_nat_p2) * np.log( {RANDOM UNIFORM (0,1)}    / cat_nat_p1 ) )  **2        which is the formula we simulate in the async task
    ##################################################### equation explanation #####################################################
    
    if rms_available:
        epcurve_df = pd_df_from_hx_list(cds.rms.edm_epcurve)
        m,b = np.polyfit(   (epcurve_df['all_peril_selected_at_acc_fx'] **0.5) ,   np.log(  epcurve_df['probability'] ),    1)


    # assign Parameter 1
    pc.param_attritional.param_1        = 0 if unavail_att else np.log(  pc.param_attritional.expected_loss  /(( ((pc.param_attritional.stdev_selected / pc.param_attritional.expected_loss) **2)   +1)  **0.5))
    pc.param_large.param_1              = 0 if unavail_lrg else        1 + ((1+  (pc.param_large.expected_loss     / pc.param_large.stdev_selected    ) **2)     **0.5)
    pc.param_cat_natural.param_1        = 0 if unavail_cat_natural else np.exp(b)
    pc.param_cat_other.param_1          = 0 if unavail_cat_other else  1 + ((1+  (pc.param_cat_other.expected_loss / pc.param_cat_other.stdev_selected) **2)     **0.5)


    # assign Parameter 2
    pc.param_attritional.param_2        = 0 if unavail_att else ( np.log( ( (pc.param_attritional.stdev_selected / pc.param_attritional.expected_loss) **2)   +1)    **0.5)
    pc.param_large.param_2              = 0 if unavail_lrg else       ((pc.param_large.param_1      -1)  * pc.param_large.expected_loss     ) / pc.param_large.param_1 
    pc.param_cat_natural.param_2        = 0 if unavail_cat_natural else  m
    pc.param_cat_other.param_2          = 0 if unavail_cat_other else ((pc.param_cat_other.param_1  -1)  * pc.param_cat_other.expected_loss ) / pc.param_cat_other.param_1 

    # test if pc parameters are consistent - this could be enhanced to allow for other influences e.g. premium, deductions, expected loss, scenario settings
    pc_consistent_test  = (   (round(pc.param_attritional.param_1 or 0, 4)  ==  round(pc.scenarios[0].result_param_1_att         or 0, 4))
                            & (round(pc.param_large.param_1       or 0, 4)  ==  round(pc.scenarios[0].result_param_1_large       or 0, 4))
                            & (round(pc.param_cat_other.param_1   or 0, 4)  ==  round(pc.scenarios[0].result_param_1_cat_other   or 0, 4))
                            & (round(pc.param_cat_natural.param_1 or 0, 4)  ==  round(pc.scenarios[0].result_param_1_cat_natural or 0, 4))
                            & (round(pc.param_attritional.param_2 or 0, 4)  ==  round(pc.scenarios[0].result_param_2_att         or 0, 4))
                            & (round(pc.param_large.param_2       or 0, 4)  ==  round(pc.scenarios[0].result_param_2_large       or 0, 4))
                            & (round(pc.param_cat_other.param_2   or 0, 4)  ==  round(pc.scenarios[0].result_param_2_cat_other   or 0, 4))
                            & (round(pc.param_cat_natural.param_2 or 0 ,4)  ==  round(pc.scenarios[0].result_param_2_cat_natural or 0, 4))    )


    # test if pc parameters are missing
    pc_missing_test     =  False

    # standard
    if (pc.scenarios[0].additionalfeaturesindicator == "No"): 
        if ((pc.scenarios[0].share is None)      or      (pc.scenarios[0].expenses is None)      or   (pc.scenarios[0].deficit is None)):
            pc_missing_test     =  True

    # threshold
    if (pc.scenarios[0].additionalfeaturesindicator == "Threshold"):
        if (    (pc.scenarios[0].share is None)      or      (pc.scenarios[0].expenses is None)      
            or  (pc.scenarios[0].deficit is None)    or      (pc.scenarios[0].threshold_bonus_share1 is None)
            or  (pc.scenarios[0].threshold_lr_cutoff1 is None)):
            pc_missing_test     =  True

    # sliding scale
    if (pc.scenarios[0].additionalfeaturesindicator == "Sliding Scale"):
        if (   (pc.scenarios[0].slidingscale_bonus_lr            is None) or (pc.scenarios[0].slidingscale_bonus_scale         is None)
            or (pc.scenarios[0].slidingscale_bonus_maxtotalpc    is None) or (pc.scenarios[0].slidingscale_clawback_lr         is None)
            or (pc.scenarios[0].slidingscale_clawback_scale      is None) or (pc.scenarios[0].slidingscale_clawback_mintotalpc is None)):
            pc_missing_test     =  True


    pc.consistent_pc_latest_param = "PC Parameters up to date"
    if pc_consistent_test ==False : pc.consistent_pc_latest_param = "Inputs have changed please re-run PC Calculator"  
    if pc_missing_test            : pc.consistent_pc_latest_param = "Inputs not complete - please resolve first"  



    pass