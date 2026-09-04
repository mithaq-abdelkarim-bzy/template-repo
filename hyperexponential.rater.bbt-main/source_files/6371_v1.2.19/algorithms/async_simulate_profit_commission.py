################################## TO DO ##############################################################

#######################################################################################################

import pandas as pd
import numpy as np
import scipy
# from algorithms.timer import timer



def simulate_pc(hxd,progress):

    # timer.start("async_pc")
    


    ########################################################
    ### 1 Loading in scenario independent values  
    #######################################################
    cds                 = hxd.cds
    pc                  = hxd.cds.profit_commission
    
    scen_col            = ['scenario','bucket','uw_profit','pc_payable','ulr_att_net_bucket',  'ulr_lrg_net_bucket',  'ulr_cat_oth_net_bucket',  'ulr_cat_nat_net_bucket',  'ulr_total_net_bucket' ]
    pc_all_dist_df      = pd.DataFrame(columns = scen_col)

    number_simulations  = 20000
    np.random.seed(123)


    # assigning scenario independent values from hxd
    prem        = cds.layers[0].quoted_premium_100pct
    brok_rate   = cds.layers[0].total_deductions
    
    att_dist    = pc.param_attritional.distribution
    att_p1      = pc.param_attritional.param_1
    att_p2      = pc.param_attritional.param_2
    attrition_el= pc.param_attritional.expected_loss 

    lrg_dist    = pc.param_large.distribution
    lrg_p1      = pc.param_large.param_1
    lrg_p2      = pc.param_large.param_2
    lrg_el      = pc.param_large.expected_loss  

    cat_nat_dist= pc.param_cat_natural.distribution
    cat_nat_p1  = pc.param_cat_natural.param_1
    cat_nat_p2  = pc.param_cat_natural.param_2
    cat_nat_el  = pc.param_cat_natural.expected_loss 

    cat_oth_dist= pc.param_cat_other.distribution
    cat_oth_p1  = pc.param_cat_other.param_1
    cat_oth_p2  = pc.param_cat_other.param_2
    cat_oth_el  = pc.param_cat_other.expected_loss 

    # testing values from W:\Finance\Actuarial\Pricing\01 - Property\JB\hx_BBT\Visuals\capecod- BBT Rater - uat 20240627_TestModel_locked - 7970c.xlsm
    # prem        = 11500000
    # brok_rate   = 0.25

    # att_dist    = "Log Normal"
    # att_p1      = 14.6825460218269
    # att_p2      = 0.207705023323819
    # attrition_el= 2431738 

    # lrg_dist    = "Pareto"
    # lrg_p1      = 3.62606566161923
    # lrg_p2      = 315867.367324753
    # lrg_el      = 436149 

    # cat_nat_dist= "Exponential"
    # cat_nat_p1  = 0.193286643474359
    # cat_nat_p2  = -0.0009531069513975
    # cat_nat_el  = 1546381

    # cat_oth_dist= ""
    # cat_oth_p1  = 0
    # cat_oth_p2  = 0
    # cat_oth_el  = 0



    ########################################################
    ### 2 SCENARIO
    #######################################################
    for i in range(10):



        ########################################################
        ### 3 LOADING IN SCENARIO DEPENDENT VALUES
        #######################################################
        # assigning scenario independent values from hxd
        profit_comm = pc.scenarios[i].share or 0
        expen_rate  = pc.scenarios[i].expenses or 0
        basis       = pc.scenarios[i].basis
        deficit     = pc.scenarios[i].deficit or 0
        ind_bonus   = pc.scenarios[i].additionalfeaturesindicator or 0
        cutoff      = pc.scenarios[i].threshold_lr_cutoff or 0
        bonus_pc    = pc.scenarios[i].threshold_bonus_share or 0

        minLRth     = pc.scenarios[i].slidingscale_bonus_lr or 0
        minLRth_mov = pc.scenarios[i].slidingscale_bonus_scale or 0
        mincomm     = pc.scenarios[i].slidingscale_bonus_maxtotalpc or 0
        maxLRth     = pc.scenarios[i].slidingscale_clawback_lr or 0
        maxLRth_mov = pc.scenarios[i].slidingscale_clawback_scale or 0
        maxcomm     = pc.scenarios[i].slidingscale_clawback_mintotalpc or 0

        include     = pc.scenarios[i].include
        complete    = pc.scenarios[i].complete


        # profit_comm = 0.275
        # expen_rate  = 0.275
        # basis       = "Gross"
        # deficit     = 0
        # ind_bonus   = "No"
        # cutoff      = 0
        # bonus_pc    = 0

        # maxLRth     = 0
        # maxLRth_mov = 0
        # maxcomm     = 0
        # minLRth     = 0
        # minLRth_mov = 0
        # mincomm     = 0

        # include        = True
        # complete    = True



        if ((complete == True) & (include == True)):



            #####################################################################
            ### 4 WHERE COMPLETE SIMULATE LOSSES AND FORCE RECONCILE
            #####################################################################

            # reset output values
            mean_loss_att_pst_mean_recon        = 0
            mean_loss_lrg_pst_mean_recon        = 0
            mean_loss_cat_oth_pst_mean_recon    = 0
            mean_loss_cat_nat_pst_mean_recon    = 0
            mean_loss_total_pst_mean_recon      = 0
            mean_pc_payable                     = 0
            return_period_losses                = 0

           
            # setting up dataframe
            col = ['loss_att_random',  'loss_lrg_random',  'loss_cat_oth_random',  'loss_cat_nat_random',  'loss_cat_nat_helper_random' ]
            pc_df = pd.DataFrame(0, index = range(1, number_simulations+1), columns = col)


            # checking if available
            att_unavl     = ( (att_p1==0) or (att_p2==0) or (attrition_el==0))
            lrg_unavl     = ( (lrg_p1==0) or (lrg_p2==0) or (lrg_el==0))
            cat_oth_unavl = ( (cat_oth_p1==0) or (cat_oth_p2==0) or (cat_oth_el==0))
            cat_nat_unavl = ( (cat_nat_p1==0) or (cat_nat_p2==0) or(cat_nat_el==0))


            # simulate losses
            pc_df['loss_att_random']           = 0 if att_unavl else        np.random.lognormal(mean=att_p1,  sigma=att_p2,  size = number_simulations)
            pc_df['loss_lrg_random']           = 0 if lrg_unavl else     (  np.random.pareto(a=lrg_p1,     size = number_simulations)    + 1) * lrg_p2          #CHECK - described here: https://numpy.org/doc/stable/reference/random/generated/numpy.random.pareto.html
            pc_df['loss_cat_oth_random']       = 0 if cat_oth_unavl else (  np.random.pareto(a=cat_oth_p1, size = number_simulations)    + 1) * cat_oth_p2      #CHECK - described here: https://numpy.org/doc/stable/reference/random/generated/numpy.random.pareto.html
            pc_df['loss_cat_nat_helper_random']= 0 if cat_nat_unavl else    np.random.uniform(low = 0, high = 1, size = number_simulations)
            pc_df['loss_cat_nat_random']       = 0 if cat_nat_unavl else    np.maximum(0,  (1/cat_nat_p2) * np.log( pc_df['loss_cat_nat_helper_random'] / cat_nat_p1 ) )  **2    


            # calculate loss distribution means
            mean_loss_att       = pc_df['loss_att_random'].mean()
            mean_loss_lrg       = pc_df['loss_lrg_random'].mean()
            mean_loss_cat_oth   = pc_df['loss_cat_oth_random'].mean() 
            mean_loss_cat_nat   = pc_df['loss_cat_nat_random'].mean()


            # calculate reconciling factor for mean losses
            factor_att      = 0 if att_unavl     else  attrition_el / mean_loss_att
            factor_lrg      = 0 if lrg_unavl     else  lrg_el       / mean_loss_lrg
            factor_cat_oth  = 0 if cat_oth_unavl else  cat_oth_el   / mean_loss_cat_oth
            factor_cat_nat  = 0 if cat_nat_unavl else  cat_nat_el   / mean_loss_cat_nat


            # calculate reconciled loss distributions
            pc_df['loss_att_pst_mean_recon']      = 0 if att_unavl else        pc_df['loss_att_random']     * factor_att
            pc_df['loss_lrg_pst_mean_recon']      = 0 if lrg_unavl else        pc_df['loss_lrg_random']     * factor_lrg
            pc_df['loss_cat_oth_pst_mean_recon']  = 0 if cat_oth_unavl else    pc_df['loss_cat_oth_random'] * factor_cat_oth
            pc_df['loss_cat_nat_pst_mean_recon']  = 0 if cat_nat_unavl else    pc_df['loss_cat_nat_random'] * factor_cat_nat
            pc_df['loss_total_pst_mean_recon']    = (  pc_df['loss_att_pst_mean_recon'] 
                                                        + pc_df['loss_lrg_pst_mean_recon']
                                                        + pc_df['loss_cat_oth_pst_mean_recon'] 
                                                        + pc_df['loss_cat_nat_pst_mean_recon'] )

            # calculate reconciled mean losses
            mean_loss_att_pst_mean_recon       = pc_df['loss_att_pst_mean_recon'].mean()
            mean_loss_lrg_pst_mean_recon       = pc_df['loss_lrg_pst_mean_recon'].mean()
            mean_loss_cat_oth_pst_mean_recon   = pc_df['loss_cat_oth_pst_mean_recon'].mean() 
            mean_loss_cat_nat_pst_mean_recon   = pc_df['loss_cat_nat_pst_mean_recon'].mean()
            mean_loss_total_pst_mean_recon     = pc_df['loss_total_pst_mean_recon'].mean()



            #####################################################################
            ### 5 WHERE COMPLETE CALCULATE ULRs
            #####################################################################

            # calculate brokerage and expense $
            brok    = prem * brok_rate
            expen   = prem * expen_rate * ( (1)     if basis=="Gross"      else    (1-brok_rate) )

            
            # calculate gross and net of deductions loss ratios by loss type
            pc_df['ulr_att_gross']      =  ( pc_df['loss_att_pst_mean_recon']     /  prem )
            pc_df['ulr_att_net']        =  ( pc_df['loss_att_pst_mean_recon']     /  prem )   /   ( 1 - brok_rate )

            pc_df['ulr_lrg_gross']      =  ( pc_df['loss_lrg_pst_mean_recon']     /  prem )
            pc_df['ulr_lrg_net']        =  ( pc_df['loss_lrg_pst_mean_recon']     /  prem )   /   ( 1 - brok_rate )

            pc_df['ulr_cat_oth_gross']  =  ( pc_df['loss_cat_oth_pst_mean_recon']  /  prem )
            pc_df['ulr_cat_oth_net']    =  ( pc_df['loss_cat_oth_pst_mean_recon']  /  prem )   /   ( 1 - brok_rate )

            pc_df['ulr_cat_nat_gross']  =  ( pc_df['loss_cat_nat_pst_mean_recon']  /  prem )
            pc_df['ulr_cat_nat_net']    =  ( pc_df['loss_cat_nat_pst_mean_recon']  /  prem )   /   ( 1 - brok_rate )

            pc_df['ulr_total_gross']    =  ( pc_df['loss_total_pst_mean_recon']   /  prem )
            pc_df['ulr_total_net']      =  ( pc_df['loss_total_pst_mean_recon']   /  prem )   /   ( 1 - brok_rate )



            #####################################################################
            ### 6 APPLY PROFIT COMMISSION STRUCTURES
            #####################################################################

            # calculate profit befor allowing for PC, after allowing any deficit
            pc_df['profit_temp']     =  prem -  brok - expen - deficit - pc_df['loss_total_pst_mean_recon']
            

            # THRESHOLD: For threshold commission a higher "bonus" profit commission is paid if the loss ratio drops below a certain level
            if (ind_bonus == "Threshold"):
                pc_df['pc_payable']      = (  np.maximum(0,    pc_df['profit_temp'] ) 
                                             * np.where( (pc_df['ulr_total_net']  <  cutoff)   , bonus_pc    , profit_comm ) )
                # calculating profit as above but now excluding deficit and allowing for the derived pc_payable
                pc_df['uw_profit']          =  prem -  brok - expen  - pc_df['loss_total_pst_mean_recon']  - pc_df['pc_payable']


            # SLIDING SCALE: For sliding scale profit commissions the commission payable is adjusted on a scale as the loss ratio increases or decreases above minimum or maximum defined thresholds
            elif (ind_bonus == "Sliding Scale") :
            
                # Create bands that apply to the slide scale PC bands
                hgr                         = (pc_df['ulr_total_gross']   >   maxLRth)
                lwr                         = (pc_df['ulr_total_gross']   <   minLRth)
                mid                         = (hgr == False)   &   (lwr == False)

                # apply commission bands according to whether hgr, lwr, mid
                pc_df.loc[hgr, 'pc_perc']   = np.maximum( maxcomm - brok_rate,   (maxLRth  - pc_df.loc[hgr, 'ulr_total_gross'] )  *100  *(maxLRth_mov))
                pc_df.loc[lwr, 'pc_perc']   = np.minimum( mincomm - brok_rate,   (minLRth  - pc_df.loc[lwr, 'ulr_total_gross'] )  *100  *(minLRth_mov))
                pc_df.loc[mid, 'pc_perc']   = 0

                # assigning profit
                pc_df['pc_payable']         = pc_df['pc_perc']  *  prem
                pc_df['uw_profit']          = pc_df['pc_perc']  *  prem


            # DEFAULT: If no additional features simply use the standard profit commissions calculation
            else:
                pc_df['pc_payable']        = np.maximum( 0,     pc_df['profit_temp']  * profit_comm)
                pc_df['uw_profit']         = prem -  brok - expen  - pc_df['loss_total_pst_mean_recon']  - pc_df['pc_payable']       
                

            # calculate average (mean) profit commission payable
            mean_pc_payable                = pc_df['pc_payable'].mean()
            number_yrs_uw_loss             = pc_df[pc_df['uw_profit']<=0]['uw_profit'].count() 
            return_period_losses           = 0      if (number_yrs_uw_loss == 0)         else (number_simulations / number_yrs_uw_loss)



            #####################################################################
            ### 7 WRITING AMOUNTS to HXD for scenario
            #####################################################################
            pc.scenarios[i].result_exp_loss_att         = mean_loss_att_pst_mean_recon
            pc.scenarios[i].result_exp_loss_large       = mean_loss_lrg_pst_mean_recon
            pc.scenarios[i].result_exp_loss_cat_other   = mean_loss_cat_oth_pst_mean_recon
            pc.scenarios[i].result_exp_loss_cat_natural = mean_loss_cat_nat_pst_mean_recon
            pc.scenarios[i].result_exp_loss_total       = mean_loss_total_pst_mean_recon
            pc.scenarios[i].result_exp_pc_payable       = mean_pc_payable
            pc.scenarios[i].result_exp_frequency_loss   = return_period_losses

            pc.scenarios[i].result_param_1_att          = att_p1
            pc.scenarios[i].result_param_1_large        = lrg_p1
            pc.scenarios[i].result_param_1_cat_other    = cat_oth_p1
            pc.scenarios[i].result_param_1_cat_natural  = cat_nat_p1

            pc.scenarios[i].result_param_2_att          = att_p2
            pc.scenarios[i].result_param_2_large        = lrg_p2
            pc.scenarios[i].result_param_2_cat_other    = cat_oth_p2
            pc.scenarios[i].result_param_2_cat_natural  = cat_nat_p2


            #####################################################################
            ### 8 GET ULR DISTRIBUTIONS for scenario
            #####################################################################

            # calculate ulr distributions
            buckets = [   0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105
                        ,110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200, 999999999]
            bucket_percs = [ x/100   for x in buckets]
            
            pc_df['ulr_att_net_bucket']     = pd.cut(x=pc_df['ulr_att_net'],     bins=bucket_percs, right=False)
            pc_df['ulr_lrg_net_bucket']     = pd.cut(x=pc_df['ulr_lrg_net'],     bins=bucket_percs, right=False)
            pc_df['ulr_cat_oth_net_bucket'] = pd.cut(x=pc_df['ulr_cat_oth_net'], bins=bucket_percs, right=False)
            pc_df['ulr_cat_nat_net_bucket'] = pd.cut(x=pc_df['ulr_cat_nat_net'], bins=bucket_percs, right=False)
            pc_df['ulr_total_net_bucket']   = pd.cut(x=pc_df['ulr_total_net'],   bins=bucket_percs, right=False)

            bucket_cols = [   'ulr_att_net_bucket'
                            , 'ulr_lrg_net_bucket'
                            , 'ulr_cat_oth_net_bucket'
                            , 'ulr_cat_nat_net_bucket'
                            , 'ulr_total_net_bucket' ]

            # counting the numnber of entries by bin - note they are counts not percentages
            # logic described here: https://stackoverflow.com/questions/32589829/how-to-get-value-counts-for-multiple-columns-at-once-in-pandas-dataframe
            melted_df           = pc_df.loc[:, bucket_cols].melt(var_name='column_names', value_name='index')
            pc_cnt_df           = pd.crosstab(index=melted_df['index'], columns=melted_df['column_names'])
            pc_cnt_df           = pc_cnt_df.reset_index(drop=False).rename(columns={'index': 'bucket'})

            # calculate amounts df, notice they are sums not averages at this time
            pc_amt_df           = pc_df.groupby(['ulr_total_net_bucket'])[['pc_payable','uw_profit']].sum()
            pc_amt_df           = pc_amt_df.reset_index(drop=False).rename(columns={'ulr_total_net_bucket': 'bucket'})

            # merging together amounts and counts
            pc_one_dist_df              = pc_amt_df.merge(pc_cnt_df, on='bucket', how='left')
            pc_one_dist_df['scenario']  = 'Base' if i == 0 else f"Scenario {i}"

            # scen_col            = ['scenario','bucket','uw_profit','pc_payable','ulr_att_net_bucket',  'ulr_lrg_net_bucket',  'ulr_cat_oth_net_bucket',  'ulr_cat_nat_net_bucket',  'ulr_total_net_bucket' ]

            pc_all_dist_df              = pc_all_dist_df.append(pc_one_dist_df, ignore_index=True)



    #####################################################################
    ### 9 GET overall distribution
    #####################################################################

    pc_all_dist_df['bucket']        = pc_all_dist_df['bucket'].astype(str)
    pc_all_dist_df                  = pc_all_dist_df.fillna(0)
    pc_all_dist_df['ulr']           = pc_all_dist_df['bucket'].str[1:].str.split(",").str[0].astype(float)                                                            # gives the lower bin edge
    pc_all_dist_df['uw_profit']     = np.where(pc_all_dist_df['ulr_total_net_bucket'] ==0, 0, pc_all_dist_df['uw_profit']  / pc_all_dist_df['ulr_total_net_bucket'])  # gives the average in the group
    pc_all_dist_df['pc_payable']    = np.where(pc_all_dist_df['ulr_total_net_bucket'] ==0, 0, pc_all_dist_df['pc_payable'] / pc_all_dist_df['ulr_total_net_bucket'])  # gives the average in the group 
    
    pc_all_dist_df['pdf_att']       = pc_all_dist_df['ulr_att_net_bucket']         / number_simulations                                                    # gives the percentage in the group 
    pc_all_dist_df['pdf_large']     = pc_all_dist_df['ulr_lrg_net_bucket']         / number_simulations                                                    # gives the percentage in the group
    pc_all_dist_df['pdf_cat_other'] = pc_all_dist_df['ulr_cat_oth_net_bucket']     / number_simulations                                                    # gives the percentage in the group
    pc_all_dist_df['pdf_cat_natural']=pc_all_dist_df['ulr_cat_nat_net_bucket']     / number_simulations                                                    # gives the percentage in the group
    pc_all_dist_df['pdf_total']     = pc_all_dist_df['ulr_total_net_bucket']       / number_simulations                                                    # gives the percentage in the group



    #####################################################################
    ### 10 WRITNG overall distribution to HXD
    #####################################################################


    output_cols = ['scenario'              
                    , 'bucket'               
                    , 'ulr'                 
                    , 'uw_profit'         
                    , 'pc_payable'        
#                    , 'cdf_att'           
                    , 'pdf_att'           
#                    , 'cdf_large'         
                    , 'pdf_large'         
#                    , 'cdf_cat_other'     
                    , 'pdf_cat_other'     
#                    , 'cdf_cat_natural'   
                    , 'pdf_cat_natural'   
#                    , 'cdf_total'         
                    , 'pdf_total']


    if pc_all_dist_df.shape[0] < 1:
        # do nothing
        cds.profit_commission.simulate_pc_task_status = "PC Simulation unsuccesful - contact actuarial pricing"
    else:
        setattr(cds.profit_commission,"distributions", pc_all_dist_df[output_cols].to_dict("records"))
        cds.profit_commission.simulate_pc_task_status = "PC Simulation Succesful"

    
    # timer.end("async_pc")

    pass

            




