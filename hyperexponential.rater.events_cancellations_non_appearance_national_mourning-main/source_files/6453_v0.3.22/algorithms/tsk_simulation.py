import hx
import numpy as np
import pandas as pd
from algorithms.rate_constants import NUMBER_OF_SIMS_T_HXD, RNG_SEED
from algorithms.rate_utilities import ratio, stratified_uniform
from datetime import datetime


###############################################################################################################
### function to generate a vector of impacts for a specific cover within a event                            ###
###############################################################################################################
def sim_event_cover(rate: float, xs: float, lim: float, ded: float, si: float, b: float, g: float, mean_b_g: float, no_sim: int, freq_override: float):
    # Two independent RNG streams (freq vs sev) for cleanliness
    r_int               = np.random.randint(0,1000)
    seed_seq            = np.random.SeedSequence(123+r_int)
    rng_freq, rng_sev   =[np.random.default_rng(s) for s in seed_seq.spawn(2)]

    # Frequency (Bernoulli thinning) using stratified uniform
    freq_unif_ss        = stratified_uniform(no_sim, rng=rng_freq, shuffle=True)
    prob                = min(1.0,  max(0.0,   ratio(rate, mean_b_g)*freq_override))                                  # clamp to [0,1] for safety
    freq_ss             = (freq_unif_ss < prob)                                                         # bool: TRUE for Loss
    no_simulated_claims = int(freq_ss.sum())

    # building output array                                                                             # FYI array (ss) of length = no_sim
    fgu_to_lim_all_ss, ded_occur_all_ss, xs_occur_all_ss, net_occur_all_ss = [ np.zeros(no_sim, dtype=np.float64) for _ in range(4) ]

    # Severity
    if no_simulated_claims > 0:
        # generate stratified random uniform & flick to points on exposure curve:                       # FYI array (ss) of length = no_simulated_claims 
        u_sev_ss        = stratified_uniform(no_simulated_claims, rng=rng_sev, shuffle=True)          
        sev_help1_ss    = ((1 - b) / (1 - u_sev_ss) - (1 - b * g)) / (g - 1)                                         
        sev_help2_ss    = (1 - (1 / np.log(b)) * np.log(sev_help1_ss))                                
        sev_fgu_ss      = np.where( sev_help1_ss <=0, 1,   np.minimum(1, sev_help2_ss) ) * si         

        # generate vector for all clm, applying occurrence terms at claim level                         # FYI array (ss) of length = no_simulated_claims
        fgu_to_lim_clm_ss = np.minimum(xs + lim, sev_fgu_ss)
        ded_occur_clm_ss  = np.minimum(ded,      sev_fgu_ss)
        xs_occur_clm_ss   = np.minimum(xs,       sev_fgu_ss) - (ded_occur_clm_ss if xs != 0 else 0)
        net_occur_clm_ss  = fgu_to_lim_clm_ss - ded_occur_clm_ss - xs_occur_clm_ss

        # generate vectors of all sim ... the combined frequency/severity impact                        # FYI array (ss) of length = no_sim
        idx                     = np.flatnonzero(freq_ss)
        fgu_to_lim_all_ss[idx]  = fgu_to_lim_clm_ss
        ded_occur_all_ss[idx]   = ded_occur_clm_ss
        xs_occur_all_ss[idx]    = xs_occur_clm_ss
        net_occur_all_ss[idx]   = net_occur_clm_ss

    return fgu_to_lim_all_ss, ded_occur_all_ss, xs_occur_all_ss, net_occur_all_ss, no_simulated_claims


###############################################################################################################
### function to generate a vector of impacts for all events and covers                                      ###
###############################################################################################################
def sim_all_event(cvg_path: object,  p_dict: dict,  seed:int,  no_sim: int, freq_override: float):

    # fix seed for reproducability and number of sims
    np.random.seed(seed)

    # build an output dataframe for the specified number of sim (no_sim) and the total impact
    output_df           = pd.DataFrame(0.0, index = range(1,no_sim+1), columns = ['fgu_to_lim', 'ded_occur', 'xs_occur', 'net_occur', 'claims_number'])
    
    for index, row in enumerate(cvg_path.events):

        # checking if a simulation is needed - only run on rows marked ok    
        # if str(row.check).strip().lower() != "ok":                     # REMOVED - VALIDATION ON THIS IS SOFT to mirror deterministic calc
        #     continue
        si              = row.tiv   or 0
        
        # iterating over events within a specific cover
        for c_dict in p_dict.values():
            # loading rate and covered and checking simulation is needed
            rate    = getattr(row, c_dict['rate_name'], 0) or 0
            covered = c_dict['covered'] or False
            if (rate == 0)  or  (covered == False):             # arguably rate=0 when covered=False, so belt and braces
                continue
            
            # loading remaining parameters
            lim     = c_dict['limit']      or 0
            ded     = c_dict['deductible'] or 0
            xs      = c_dict['excess']     or 0
            xs      = xs if xs>ded else 0                       # errortrapping xs<ded and setting to nil which then gets ignored later
            b       = c_dict['b']  
            g       = c_dict['g']  
            mean_b_g= c_dict['mean_b_g']

            # running simulation and appending 
            fgu_to_lim, ded_occur, xs_occur, net_occur, no_simulated_claims = sim_event_cover(   rate, xs, lim, ded, si, b, g, mean_b_g, no_sim, freq_override)
            output_df['fgu_to_lim'] += fgu_to_lim
            output_df['ded_occur']  += ded_occur
            output_df['xs_occur']   += xs_occur
            output_df['net_occur']  += net_occur
            output_df['claims_number']  += no_simulated_claims
    
    return output_df


###############################################################################################################
### build parameter dictionary for all covers                                                               ###
###############################################################################################################
def build_paramater_dictionary(cvg_path, layer_path):
    
    p_dict              = {}
    ec_coverages_lst    = [  "all_risks",     "adverse_weather",   "earthquake",  "windstorm",  "wildfire",  "terrorism",  "cyber"
                           , "national_mourning",  "riots_and_civil_commotion",   "strike",     "war",       "catastrophic_non_app"]
    weather_lst         = [  "adverse_weather",   "windstorm",  "wildfire"]
    eq_lst              = [  "earthquake"]

    for i, c in enumerate(ec_coverages_lst):
        # coverages settings
        c_path  = getattr(cvg_path.base_coverages, c)        
        f_path  = cvg_path.factors
        c_dict  = {}
        sublimit= c_path.sublimit   if c != "all_risks" else None 
        limit   = layer_path.limit

        # get exposure curve factors for coverage
        b      = f_path.exp_cve_ws_b if c in weather_lst else (f_path.exp_cve_eq_b if c in eq_lst else f_path.exp_cve_attr_b)
        g      = f_path.exp_cve_ws_g if c in weather_lst else (f_path.exp_cve_eq_g if c in eq_lst else f_path.exp_cve_attr_g)

        # load names and exposure curves
        c_dict['index']     = i
        c_dict['cvg_name']  = c
        c_dict['rate_name'] = f'rate_{c}'
        c_dict['b']         = b 
        c_dict['g']         = g    
        c_dict['mean_b_g']  = ratio(( np.log(b*g) * (1-b) ),    ( np.log(b) * (1-b*g) ))

        # load financials for coverage
        c_dict['covered']   = c_path.covered    if c != "all_risks" else True
        c_dict['uw_adj']    = c_path.uw_adj_fin                                 # Not used if we did want to simulate before and after uw adj need to consider the special mods on national mourning
        c_dict['limit']     = limit  if sublimit is None else np.minimum(sublimit, limit)
        c_dict['excess']    = layer_path.excess                                 
        c_dict['deductible']= layer_path.deductible

        # assign to dictionary as a dictionary of dictionaries
        p_dict[c]               = c_dict
    
    return p_dict 


###############################################################################################################
### function to simulate the impact of aggs and decutibles on event cancellation policies                   ###
###############################################################################################################
def tsk_simulation(hxd,progress):

    # paths  
    cvg_path   = hxd.cds.exposure.granular.event_cancel
    layer_path = hxd.cds.layers[0]
    sim_path   = hxd.cds.exposure.granular.event_cancel.simulation

    # checking if no data is entered 
    if sim_path.calc_run_value is None or sim_path.calc_run_value==0:
        # do nothing
        sim_path.last_run_status = "No Simulation Run - no data entered"
        return

    # settings
    no_sim    = int(sim_path.num_sims if hxd.model_state.live_hxd else NUMBER_OF_SIMS_T_HXD) ### using a smaller number of sims if using transient hxd => rarc task
    p_dict    = build_paramater_dictionary(cvg_path, layer_path)
    freq_ovd  = sim_path.total_sim_claim_number_override
    freq_calc = sim_path.total_sim_claim_number_calc
    freq_check= (freq_ovd is not None) and (freq_ovd > 0)
    freq_adj  = ratio(freq_ovd, freq_calc) if freq_check else 1
    output_df = sim_all_event(cvg_path,  p_dict,  RNG_SEED,  no_sim, freq_adj)

    # get agg_ded, agg_lim and determine if limit is primary and hence eroded by deductible
    agg_ded = layer_path.aggregate_deductible   or 9e9 # using an arbitrariliy large number for unlimitted
    agg_lim = layer_path.aggregate_limit        or 9e9 # using an arbitrariliy large number for unlimitted
    xs_used = (hxd.cds.layers[0].excess or 0) != 0

    # apply agg xs & lim to the  vector of total impact from above
    output_df['ded_agg']   = np.minimum(agg_ded, output_df['ded_occur'])
    output_df['xs_agg']    = (output_df['xs_occur'] + output_df['ded_occur'] - output_df['ded_agg']) if xs_used else 0 # no xs means deductible erodes primary
    output_df['net_agg']   = np.minimum(agg_lim, output_df['fgu_to_lim']  - output_df['ded_agg'] - output_df['xs_agg']) 

    # output the result
    summary_value                       = cvg_path.base_coverages.ec_total.net_el
    sim_path.last_run_value             = f"EL (orig Fx): { summary_value :,.0f}"
    sim_path.total_sim_claim_number     = ratio(output_df["claims_number"].iloc[0], no_sim)
    sim_path.total_sim_loss_before_agg  = np.mean(output_df['net_occur'])
    sim_path.total_sim_loss_after_agg   = np.mean(output_df['net_agg'])
    sim_path.last_run_date              = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sim_path.last_run_status            = f"Event Cancellation Simulation run successfully at {sim_path.last_run_date}"

    return
