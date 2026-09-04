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

def rate_rms(hxd):
    cds = hxd.cds

    cds.rms.edm_reference_requested = cds.standard_fields.facility_reference
    
    #######################################
    ### START cds.rms.ep_curve          ###
    #######################################

    #converting i) edm = raw data extracted from exposure mgmt; ii) ep_curve = what we want to visualise;   to dataframes
    ep_curve_df = pd_df_from_hx_list(cds.rms.edm_epcurve)
    edm_df = pd_df_from_hx_list(cds.rms.edm)


    #converting to numeric columns
    edm_df.rename(columns={'return_period':'return_period_text' ,'probability':'probability_text'} , inplace = True)
    edm_df['return_period'] = pd.to_numeric(edm_df.return_period_text, errors='coerce').fillna(0)
    edm_df['probability'] = pd.to_numeric(edm_df.probability_text, errors='coerce').fillna(0)
 

    #rms uplift
    uplift_df               = hx.params.tb_rms_uplift
    uplift_row_df           = uplift_df[ (uplift_df['Benchmark Class'] == cds.standard_fields.benchmark_class) ] 
    uplift_row_empty        = uplift_row_df.empty
    uplift_ws               = 1 if uplift_row_empty else uplift_row_df['RMS Uplift Hurricane'].iat[0]
    uplift_eq               = 1 if uplift_row_empty else uplift_row_df['RMS Uplift Earthquake'].iat[0]
    cds.rms.rms_uplift_ws   = uplift_ws
    cds.rms.rms_uplift_eq   = uplift_eq



    #aggregating wind and quake as sqrt(sumsq())
    edm_df.loc[:,'ws_loss_amount']          = edm_df['ws_loss_amount'].fillna(0) * uplift_ws
    edm_df.loc[:,'eq_loss_amount']          = edm_df['eq_loss_amount'].fillna(0) * uplift_eq
    edm_df['all_peril_calc_at_edm_fx']      = ( (edm_df.ws_loss_amount **2) + (edm_df.eq_loss_amount **2) ) **0.5  
    edm_df['all_peril_calc_at_acc_fx']      = (    ((edm_df.ws_loss_amount * edm_df.ws_fxrate) **2) 
                                                 + ((edm_df.eq_loss_amount * edm_df.eq_fxrate) **2) ) **0.5   
    
       
    #new dataframe for just the ep_curve information - notice name change: edm_to_ep_curve_df and reset index due to appending info latterly
    edm_to_ep_curve_df = edm_df[  (edm_df.return_period !=0)   &   (edm_df.portnum == cds.rms.edm_reference_selected)]
    edm_to_ep_curve_df.reset_index(drop=True, inplace=True)
    

    #want to still show return periods and probability incase no EDM data is loaded/selected and underwriter wants to enter manually
    if edm_to_ep_curve_df.empty:
        edm_to_ep_curve_df['return_period'] = [10000,5000,1000,500,250,200,150,100,50,30,10,2]
        edm_to_ep_curve_df['probability']   = 1 / edm_to_ep_curve_df['return_period']

    edm_to_ep_curve_df['return_period_label'] = (f"1 in " + edm_to_ep_curve_df['return_period'].astype(int).astype(str) +" Yr")


    #incorporating overrides
    edm_to_ep_curve_df['all_peril_override_at_acc_fx'] = ep_curve_df['all_peril_override_at_acc_fx']
    edm_to_ep_curve_df['all_peril_selected_at_acc_fx'] = (edm_to_ep_curve_df['all_peril_override_at_acc_fx']  if cds.rms.use_override else edm_to_ep_curve_df['all_peril_calc_at_acc_fx'])
    
    # error trap nils
    edm_to_ep_curve_df['all_peril_selected_at_acc_fx'] = np.where(edm_to_ep_curve_df['all_peril_selected_at_acc_fx']<0,0,edm_to_ep_curve_df['all_peril_selected_at_acc_fx'])
       
    #writing edm_to_ep_curve_df to cds.rms.edm_epcurve
    output_columns= ['probability','return_period','return_period_label','ws_loss_amount','eq_loss_amount','all_peril_calc_at_edm_fx','all_peril_calc_at_acc_fx','all_peril_selected_at_acc_fx']
    write_pd_to_hxd(edm_to_ep_curve_df.fillna(0), cds.rms.edm_epcurve, output_columns)

    #######################################
    ### END cds.rms.ep_curve            ###
    #######################################
    
    #######################################
    ### START cds.rms.ep_summary        ###
    #######################################

    edm_sum = hxd.cds.rms.edm_summary
 
    edm_summary_df = edm_df[  (edm_df.return_period_text.isin(['AAL','StdDev']))   &   (edm_df.portnum == cds.rms.edm_reference_selected)]
    empty_aal = edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL"].empty
    empty_sd  = edm_summary_df.loc[edm_summary_df['return_period_text'] == "StdDev"].empty



    ### windstorm derivation
    edm_sum.ws_loss_amount.fx           =  '' if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'ws_currency'].iat[0]
    edm_sum.ws_loss_amount.fxrate       =  0  if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'ws_fxrate'].iat[0]
    edm_sum.ws_loss_amount.aal          =  0  if empty_aal else edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'ws_loss_amount'].iat[0]
    edm_sum.ws_loss_amount.std_dev      =  0  if empty_sd  else edm_summary_df.loc[edm_summary_df['return_period_text'] == "StdDev", 'ws_loss_amount'].iat[0]
    edm_sum.ws_loss_amount.prem         =  0  if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'ws_premium'].iat[0]
    edm_sum.ws_loss_amount.coeff_var    =  0  if (empty_aal or (edm_sum.ws_loss_amount.aal ==0)) else edm_sum.ws_loss_amount.std_dev / edm_sum.ws_loss_amount.aal 
    edm_sum.ws_loss_amount.gross_lr     =  0  if (empty_aal or (edm_sum.ws_loss_amount.prem==0)) else edm_sum.ws_loss_amount.aal     / edm_sum.ws_loss_amount.prem


    ### earthquake derivation
    edm_sum.eq_loss_amount.fx           =  '' if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'eq_currency'].iat[0]
    edm_sum.eq_loss_amount.fxrate       =  0  if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'eq_fxrate'].iat[0]
    edm_sum.eq_loss_amount.aal          =  0  if empty_aal else edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'eq_loss_amount'].iat[0]
    edm_sum.eq_loss_amount.std_dev      =  0  if empty_sd  else edm_summary_df.loc[edm_summary_df['return_period_text'] == "StdDev", 'eq_loss_amount'].iat[0]
    edm_sum.eq_loss_amount.prem         =  0  if empty_aal else  edm_summary_df.loc[edm_summary_df['return_period_text'] == "AAL",    'eq_premium'].iat[0]
    edm_sum.eq_loss_amount.coeff_var    =  0  if (empty_aal or (edm_sum.eq_loss_amount.aal==0)) else edm_sum.eq_loss_amount.std_dev / edm_sum.eq_loss_amount.aal 
    edm_sum.eq_loss_amount.gross_lr     =  0  if (empty_aal or (edm_sum.eq_loss_amount.prem==0)) else edm_sum.eq_loss_amount.aal     / edm_sum.eq_loss_amount.prem


    ### all peril calc edm fx derivation
    edm_sum.all_peril_calc_at_edm_fx.fx           =  '' 
    edm_sum.all_peril_calc_at_edm_fx.fxrate       =  0  
    edm_sum.all_peril_calc_at_edm_fx.aal          =  0  if empty_aal else edm_sum.ws_loss_amount.aal   +   edm_sum.eq_loss_amount.aal  
    edm_sum.all_peril_calc_at_edm_fx.std_dev      =  0  if empty_sd  else ( (edm_sum.ws_loss_amount.std_dev **2) + (edm_sum.eq_loss_amount.std_dev **2) ) **0.5
    edm_sum.all_peril_calc_at_edm_fx.prem         =  0  if empty_aal else edm_sum.ws_loss_amount.prem + edm_sum.eq_loss_amount.prem
    edm_sum.all_peril_calc_at_edm_fx.coeff_var    =  0  if (empty_aal or (edm_sum.all_peril_calc_at_edm_fx.aal ==0)) else edm_sum.all_peril_calc_at_edm_fx.std_dev / edm_sum.all_peril_calc_at_edm_fx.aal
    edm_sum.all_peril_calc_at_edm_fx.gross_lr     =  0  if (empty_aal or (edm_sum.all_peril_calc_at_edm_fx.prem==0)) else edm_sum.all_peril_calc_at_edm_fx.aal     / edm_sum.all_peril_calc_at_edm_fx.prem


    ### all peril calc acc fx derivation
    edm_sum.all_peril_calc_at_acc_fx.fx           =  cds.currencies.source_currency 
    edm_sum.all_peril_calc_at_acc_fx.fxrate       =  1  
    edm_sum.all_peril_calc_at_acc_fx.aal          =  0  if empty_aal else (   edm_sum.ws_loss_amount.aal * edm_sum.ws_loss_amount.fxrate
                                                                            + edm_sum.eq_loss_amount.aal * edm_sum.eq_loss_amount.fxrate)
    edm_sum.all_peril_calc_at_acc_fx.std_dev      =  0  if empty_sd  else (  (edm_sum.ws_loss_amount.std_dev * edm_sum.ws_loss_amount.fxrate) **2
                                                                            +(edm_sum.eq_loss_amount.std_dev * edm_sum.eq_loss_amount.fxrate) **2) **0.5
    edm_sum.all_peril_calc_at_acc_fx.prem         =  0  if empty_aal else (   edm_sum.ws_loss_amount.prem * edm_sum.ws_loss_amount.fxrate
                                                                            + edm_sum.eq_loss_amount.prem * edm_sum.eq_loss_amount.fxrate)
    edm_sum.all_peril_calc_at_acc_fx.coeff_var    =  0  if (empty_aal or (edm_sum.all_peril_calc_at_acc_fx.aal ==0)) else edm_sum.all_peril_calc_at_acc_fx.std_dev / edm_sum.all_peril_calc_at_acc_fx.aal 
    edm_sum.all_peril_calc_at_acc_fx.gross_lr     =  0  if (empty_aal or (edm_sum.all_peril_calc_at_acc_fx.prem==0)) else edm_sum.all_peril_calc_at_acc_fx.aal     / edm_sum.all_peril_calc_at_acc_fx.prem

  
    ### all peril override
    empty_override_coeff_var    = (edm_sum.all_peril_override_at_acc_fx.aal is None) or (edm_sum.all_peril_override_at_acc_fx.std_dev is None)  or (edm_sum.all_peril_override_at_acc_fx.aal ==0)
    empty_override_gross_lr     = (edm_sum.all_peril_override_at_acc_fx.aal is None) or (edm_sum.all_peril_override_at_acc_fx.prem is None)     or (edm_sum.all_peril_override_at_acc_fx.prem==0)
    edm_sum.all_peril_override_at_acc_fx.fx           =  cds.currencies.source_currency 
    edm_sum.all_peril_override_at_acc_fx.fxrate       =  1  
    edm_sum.all_peril_override_at_acc_fx.coeff_var    =  0  if empty_override_coeff_var else edm_sum.all_peril_override_at_acc_fx.std_dev / edm_sum.all_peril_override_at_acc_fx.aal
    edm_sum.all_peril_override_at_acc_fx.gross_lr     =  0  if empty_override_gross_lr  else edm_sum.all_peril_override_at_acc_fx.aal     / edm_sum.all_peril_override_at_acc_fx.prem


    ### all peril selected including error trap nils
    edm_sum.all_peril_selected_at_acc_fx.fx           =  cds.currencies.source_currency 
    edm_sum.all_peril_selected_at_acc_fx.fxrate       =  1  
    edm_sum.all_peril_selected_at_acc_fx.aal          =  max(0,edm_sum.all_peril_override_at_acc_fx.aal or 0)       if cds.rms.use_override else edm_sum.all_peril_calc_at_acc_fx.aal 
    edm_sum.all_peril_selected_at_acc_fx.std_dev      =  max(0,edm_sum.all_peril_override_at_acc_fx.std_dev or 0)   if cds.rms.use_override else edm_sum.all_peril_calc_at_acc_fx.std_dev
    edm_sum.all_peril_selected_at_acc_fx.prem         =  max(0,edm_sum.all_peril_override_at_acc_fx.prem or 0)      if cds.rms.use_override else edm_sum.all_peril_calc_at_acc_fx.prem
    edm_sum.all_peril_selected_at_acc_fx.coeff_var    =  max(0,edm_sum.all_peril_override_at_acc_fx.coeff_var or 0) if cds.rms.use_override else edm_sum.all_peril_calc_at_acc_fx.coeff_var 
    edm_sum.all_peril_selected_at_acc_fx.gross_lr     =  max(0,edm_sum.all_peril_override_at_acc_fx.gross_lr or 0)  if cds.rms.use_override else edm_sum.all_peril_calc_at_acc_fx.gross_lr
 
 
    #######################################
    ### END cds.rms.ep_summary          ###
    #######################################




    pass