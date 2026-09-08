##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################
### 

##############################################################################################################################
##############################################################################################################################
import hx
import numpy as np
import pandas as pd
from algorithms.rate_constants import number_of_sims_t_hxd 
from algorithms.rate_utilities import pd_df_from_hx_list
from datetime import datetime

###############################################################################################################
### function to generate a vector of impacts for a specific cover within a country                          ###
###############################################################################################################
def sim_country_cover(rate: float, xs: float, lim: float, ded: float, si: float, b: float, g: float, mean_b_g: float, no_sim: int):
    # build a temporary dataframe for the specified number of sim (no_sim) and columns (cover_country_col)
    cover_country_col       = ['f_runif',  'freq',  's_runif',  's_help1',  's_help2',  'sev',  'f_x_s' ]
    df                      = pd.DataFrame(0, index = range(1, no_sim+1), columns = cover_country_col)

    # generate a vector of frequencies (either 0 or 1) by generating random uniform on (0,1) and comparing to the rate after removing the impact of severity (mean_b_g)
    df['f_runif']           = np.random.uniform(low = 0, high = 1, size = no_sim)
    df['freq']              = np.where(df['f_runif'] < rate / mean_b_g,  1,  0)

    # generate a vector of severities and restrict them to be >0 and <lim and <si at various points
    sev_lt_0                = min(lim,  max(0,  si - xs  -  ded ))
    df['s_runif']           = np.random.uniform(low = 0, high = 1, size = no_sim)
    df['s_help1']           = ((1 - b) / (1 - df['s_runif'])   -   (1 - b*g))  / (g - 1)
    df['s_help2']           = (1-  (1 / np.log(b)) * np.log( df['s_help1'] )) * si
    df['sev']               = np.where( df['s_help1']<=0,    sev_lt_0,    np.minimum(lim,  np.maximum(0,  np.minimum(si,  df['s_help2'])  -xs  -ded)))

    # return a vector of the combined frequency/severity impact for a given country/cover combination
    return df['sev'] * df['freq']



###############################################################################################################
### function to generate a vector of impacts for a specific country across all covers                       ###
###############################################################################################################
def sim_country( rate_pv: float, xs_pv: float, lim_pv: float,   ded_pv: float
                ,rate_ci: float, xs_ci: float, lim_ci: float,   ded_ci: float
                ,rate_ot: float, xs_ot: float, lim_ot: float,   ded_ot: float
                ,     si: float,     b: float,      g: float, mean_b_g: float, no_sim: int):

    # build a temporary dataframe for the specified number of sim (no_sim) and columns (cover_country_col)
    df = pd.DataFrame(0, index = range(1, no_sim+1), columns = ['impact'])

    # assess the impact vector for each of the 3 modelled coverages: pv (political violence); ci (currency incovertibilty); ot (other = gov action + contract rel gov)
    if rate_pv>0 and lim_pv>0:      df['impact']    += sim_country_cover(rate_pv, xs_pv, lim_pv, ded_pv, si, b, g, mean_b_g, no_sim)
    if rate_ci>0 and lim_ci>0:      df['impact']    += sim_country_cover(rate_ci, xs_ci, lim_ci, ded_ci, si, b, g, mean_b_g, no_sim)
    if rate_ot>0 and lim_ot>0:      df['impact']    += sim_country_cover(rate_ot, xs_ot, lim_ot, ded_ot, si, b, g, mean_b_g, no_sim)
    
    # return a vector of the combined frequency/severity impact for a given country
    return df['impact']



###############################################################################################################
### function to generate a vector of impacts for all countries and covers                                   ###
###############################################################################################################
def sim_political(hxd,progress):

    
    pol                 = hxd.cds.exposure.granular.political

    # checking if no data is entered 
    if pol.simulation.calc_run_value is None or pol.simulation.calc_run_value==0:
        # do nothing
        pol.simulation.last_run_status = "No Simulation Run - no data entered"
        return

    # load exposure curve factors
    b                   = pol.ec_param_b                    
    g                   = pol.ec_param_g                  
    mean_b_g            = ( np.log(b*g) * (1-b) )    /    ( np.log(b) * (1-b*g) )


    # fix seed for reproducability and number of sims
    np.random.seed(42)
    no_sim              = int(pol.simulation.num_sims if hxd.live_hxd else number_of_sims_t_hxd) ### using a smaller number of sims if using transient hxd => rarc task

    # build an output dataframe for the specified number of sim (no_sim) and the total impact
    output_df           = pd.DataFrame(0, index = range(1,no_sim+1), columns = ['impact'])
    cumul_rate          = 0

    for index, row in enumerate(pol.country_exposure):
        if row.check == "ok":
            si              = row.sum_insured   or 0

            rate_ot         = row.loss_roe_gai + row.loss_roe_crg
            ded_ot          = 0                     
            xs_ot           = row.excess        or 0
            lim_ot          = row.limit         or 0

            rate_pv         = row.loss_roe_pv   or 0
            ded_pv          = row.deductible_pv or 0
            xs_pv           = xs_ot                 
            lim_pv          = row.sublimit_pv   or 0

            rate_ci         = row.loss_roe_ci   or 0
            ded_ci          = ded_ot                
            xs_ci           = xs_ot                 
            lim_ci          = row.sublimit_ci   or 0

            cumul_rate     += rate_ot + rate_pv + rate_ci
            output_df['impact'] += sim_country(   rate_pv, xs_pv, lim_pv, ded_pv, rate_ci, xs_ci, lim_ci, ded_ci
                                                , rate_ot, xs_ot, lim_ot, ded_ot, si, b, g, mean_b_g, no_sim)

    # apply agg xs & lim to the  vector of total impact from above
    agg_xs  = hxd.cds.layers[0].excess                
    agg_lim = hxd.cds.layers[0].limit                
    output_df['impact_capped'] = np.minimum( agg_lim, np.maximum(0, output_df['impact'] - agg_xs))

    # output the result
    pol.simulation.total_sim_loss_uncapped  = np.mean(output_df['impact'])
    pol.simulation.total_sim_loss_capped    = np.mean(output_df['impact_capped'])
    pol.simulation.last_run_date            = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pol.simulation.last_run_status          = f"Political Risk Simulation run successfully at {pol.simulation.last_run_date}"
    pol.simulation.last_run_value           = f"{ cumul_rate :.5f}"

