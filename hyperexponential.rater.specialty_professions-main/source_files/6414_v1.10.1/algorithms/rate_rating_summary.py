import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from algorithms.rate_utilities import ratio, look_up, _perform_lookup, calc_tp_year
from algorithms import parameter_tables_schema as params
from algorithms.rate_constants import benchmark_lr_const, assumed_lr_const, bp_class, busa_commission_rebase
from operator import itemgetter
from datetime import date, timedelta
import calendar

def rate_rating_summary(hxd):
    
    # INITIALISATION ########################################

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced = hxd.cds.standard_fields.rating_methodology == "Case Priced"
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == "Rater"

    # CASE PRICING #########################################
    # Define options location -
    options = hxd.cds.options
    layers = hxd.cds.layers

    # Dynamic dropdown based on number of options selected
    option_label = []  

    # get item from list
    for item in options:
        # define items in options list structure        
        option_label.append(getattr(item, "option_label"))  

    # Add option label
    for i in range(0, len(options)):
        option_label[i] = i+1

    # Save down outputs
    for i, item in zip(range(0, len(options)), options):
        setattr(item,"option_label",option_label[i])
    
    # RATER PRICING #########################################

    # Define cds locations
    engi_disc = hxd.cds.exposure.granular.engineering
    con_disc = hxd.cds.exposure.granular.contractor

    # define maximum number of excess layers in the rater 
    max_excess_layers = 5

    # Brokerage
    brokerage = hxd.cds.brokerage

    # Written line 
    written_line = 1

    # Engineering and contractor base premiums
    engi_tot_base_prem = hxd.cds.exposure.granular.engineering.total.base_premium_size_discount
    con_tot_base_prem = hxd.cds.exposure.granular.contractor.total.base_premium_size_discount
    total_prop_factor = hxd.cds.exposure.aggregate.project_type_category.cat_type_total.proportional_loading

    tot_base_prem = (engi_tot_base_prem + con_tot_base_prem) * (1-busa_commission_rebase) * (1 + total_prop_factor)
    
    # rateable exposure
    engi_rateable_exp = engi_disc.total.rateable_exposure
    con_rateable_exp = con_disc.total.rateable_exposure
    total_rateable_exp = engi_rateable_exp + con_rateable_exp

    if (total_rateable_exp != 0):
        engi_rateable_exp_perc = engi_rateable_exp / total_rateable_exp
        con_rateable_exp_perc = con_rateable_exp / total_rateable_exp
    else:
        engi_rateable_exp_perc = 0
        con_rateable_exp_perc = 0

    # SET UP MINIMUMS ########################################

    # Minimum_premiums - assuming $1m ILF
    # Engineering and contractor gross minimums
    engi_minprem_gross = engi_disc.total.min_premium
    con_minprem_gross = con_disc.total.min_premium   

    # Total gross minimum
    minprem_gross = engi_disc.total.min_premium * engi_rateable_exp_perc + con_disc.total.min_premium * con_rateable_exp_perc
    # Total net minimum
    minprem_net = (engi_disc.total.min_premium * engi_rateable_exp_perc + con_disc.total.min_premium * con_rateable_exp_perc)* (1 - brokerage)

    # Minimum Deductible
    # Engineering and contractor minimum deductible   
    # engi_min_deductible = engi_disc.total.min_deductible
    # con_min_deductible = con_disc.total.min_deductible

    # Total minimum deductible
    min_deductible = engi_disc.total.min_deductible * engi_rateable_exp_perc + con_disc.total.min_deductible * con_rateable_exp_perc
  
    #### RISK MODIFICATION FACTORS ########################################

    # Base model premium (subject to minimum premium) #####################        
    model_prem = max(tot_base_prem, minprem_net)
    model_prem_non_min = tot_base_prem

    # Base model premium (not subject to minimum premium) #####################        

    # Paths
    location = hxd.cds.rating_factors.location
    rating_factors = hxd.cds.rating_factors     
    modifiers = hxd.cds.modifiers
                            
    #### State modification factor #####################
    # Apply state adjustment factors
    model_prem_non_min = model_prem_non_min * location.state_factor_selected
    model_prem_non_min_pre_uw_adj = model_prem_non_min * location.state_factor_selected
    # Apply state adjustment factors, subjected to minimum premium
    model_prem = max(model_prem * location.state_factor_selected ,minprem_net)
    model_prem_pre_uw_adj = max(model_prem * location.state_factor_selected ,minprem_net)
        
    #### Experience modification #####################

    if (modifiers.exp_mod.written_premium is not None):
        if (modifiers.exp_mod.incurred_loss is not None):
            modifiers.exp_mod.incurred_lr.calculated = modifiers.exp_mod.incurred_loss / modifiers.exp_mod.written_premium
        elif (modifiers.exp_mod.incurred_loss is None):
            modifiers.exp_mod.incurred_lr.calculated = 0

    # Exp mod factor
    if (modifiers.exp_mod.incurred_lr.selected is None):
        modifiers.exp_mod.exp_mod_factor.calculated = 1
    else:
        if modifiers.exp_mod.incurred_lr.selected < -0.6:
            modifiers.exp_mod.exp_mod_factor.calculated = 1
        else:
            modifiers.exp_mod.exp_mod_factor.calculated = max(0.8,min(2,math.sqrt(1-(0.4-modifiers.exp_mod.incurred_lr.selected))))
    
    # Apply exp mod factor
    model_prem_non_min = model_prem_non_min * modifiers.exp_mod.exp_mod_factor.selected
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * modifiers.exp_mod.exp_mod_factor.calculated
    
    # Apply exp mod factor, subjected to minimum prem
    model_prem = max(model_prem * modifiers.exp_mod.exp_mod_factor.selected,minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * modifiers.exp_mod.exp_mod_factor.calculated,minprem_net)

    # incurred lr label
    modifiers.exp_mod.incurred_lr_info_label = "Calculated as total incurred loss divided by total written premium, or can be overwritten"
    # exp mod factor label
    modifiers.exp_mod.exp_mod_factor_info_label = "Sliding scale factor based on incurred loss ratio, or can be overwritten"

    #### Use of Written Contract #####################
    # Apply written contracts factor
    model_prem_non_min = model_prem_non_min * rating_factors.written_contracts.written_contracts_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.written_contracts.written_contracts_factor

    # Apply written contracts factor, subjected to minimum prem
    model_prem = max(model_prem * rating_factors.written_contracts.written_contracts_factor,minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.written_contracts.written_contracts_factor,minprem_net)

    #### Longevity_With_Carrier #####################

    # Longevity with Carrier factor
    if (hxd.cds.standard_fields.is_renewal == True and rating_factors.longevity_with_carrier.lr == True and rating_factors.longevity_with_carrier.yrs_insured > 3):        
        rating_factors.longevity_with_carrier.longevity_with_carrier_factor = 0.95
    else:
        rating_factors.longevity_with_carrier.longevity_with_carrier_factor = 1
    
    # Apply longevity with carrier factor
    model_prem_non_min = model_prem_non_min * rating_factors.longevity_with_carrier.longevity_with_carrier_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.longevity_with_carrier.longevity_with_carrier_factor

    # Apply longevity with carrier factor, subjected to minimum
    model_prem = max(model_prem * rating_factors.longevity_with_carrier.longevity_with_carrier_factor, minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.longevity_with_carrier.longevity_with_carrier_factor, minprem_net)    

    #### Longevity  #################################
    # Longevity parameter table
    param_mod_yrsinbusiness = hx.params.tbl_yrsinbusiness        

    # Calculate longevity yrs in business
    if (rating_factors.longevity.yr_start is None):
        rating_factors.longevity.yrs_in_business = 0
    elif (rating_factors.longevity.yr_start > hxd.hx_core.inception_date.year):
        rating_factors.longevity.yrs_in_business = 0
    else:
        rating_factors.longevity.yrs_in_business = hxd.hx_core.inception_date.year - rating_factors.longevity.yr_start

    # Longevity Factor
    rating_factors.longevity.longevity_factor = param_mod_yrsinbusiness[param_mod_yrsinbusiness['Years in Business'] <= rating_factors.longevity.yrs_in_business]['Factor'].iloc[-1]    

    # Apply longevity factor
    model_prem_non_min = model_prem_non_min * rating_factors.longevity.longevity_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.longevity.longevity_factor

    # Apply longevity factor, subjected to minimum premiums
    model_prem = max(model_prem * rating_factors.longevity.longevity_factor,minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.longevity.longevity_factor,minprem_net)
    
    #### ERP #####################################

    # ERP parameter table
    param_mod_erp = hx.params.tbl_erp

    # ERP Factor
    rating_factors.erp.erp_factor = param_mod_erp[param_mod_erp['Extended Reporting Period'] == rating_factors.erp.erp]['Factor'].iloc[0]

    # Apply ERP Factor
    model_prem_non_min = model_prem_non_min * rating_factors.erp.erp_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.erp.erp_factor

    # Apply ERP Factor, subjected to minimum premiums
    model_prem = max(model_prem * rating_factors.erp.erp_factor,minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.erp.erp_factor,minprem_net)

    #### RESIDENTIAL FACTORS ########################################

    # Components of residential factors
    # Multiple units
    if (rating_factors.resi.multiple_units == True):
        # 1.25 loading
        rating_factors.resi.multiple_units_factor = 1.25
    else:
        rating_factors.resi.multiple_units_factor = 1
    
    # High value
    if (rating_factors.resi.high_value == True):
        # 1.25 loading
        rating_factors.resi.high_value_factor = 1.25
    else:
        rating_factors.resi.high_value_factor = 1

    # Condos
    if (rating_factors.resi.condos == True):
        # placeholder for now
        rating_factors.resi.condos_factor = 1
    else:
        rating_factors.resi.condos_factor = 1
    
    # Residential factor
    if (rating_factors.resi.resi_proj == False):
        rating_factors.resi.resi_proj_factor = 1
    else:
        rating_factors.resi.resi_proj_factor = rating_factors.resi.multiple_units_factor * rating_factors.resi.high_value_factor * rating_factors.resi.condos_factor

    # Apply residential factor
    model_prem_non_min = model_prem_non_min * rating_factors.resi.resi_proj_factor    
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.resi.resi_proj_factor    
    model_prem = model_prem * rating_factors.resi.resi_proj_factor
    model_prem_pre_uw_adj = model_prem_pre_uw_adj * rating_factors.resi.resi_proj_factor

    #### OPTIONAL COVERAGES ########################################

    # Full Prior Acts Coverage        

    # Number of years retro based on entered retro date
    if (rating_factors.opt_coverages.full_prior_act_date is None):
        num_retro_yr = 0
    else:
        num_retro_yr = max(round((hxd.hx_core.inception_date - rating_factors.opt_coverages.full_prior_act_date).days/365.25,0),0)
    
    # Selected retro year
    selected_retro_yr = 0

    if (rating_factors.opt_coverages.full_prior_act == False):
        selected_retro_yr = num_retro_yr
    else:
        selected_retro_yr = max(num_retro_yr, rating_factors.longevity_with_carrier.yrs_insured)    

    # FPA parameter table
    param_mod_fpa = hx.params.tbl_retro
    
    # Retro factor
    if (rating_factors.opt_coverages.full_prior_act == True):
        rating_factors.opt_coverages.retro_factor = 1
    else:
        rating_factors.opt_coverages.retro_factor = param_mod_fpa[param_mod_fpa['Retro'] <= selected_retro_yr]['Factor'].iloc[-1]           
    
    # Apply retro factor
    model_prem_non_min = model_prem_non_min * rating_factors.opt_coverages.retro_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.opt_coverages.retro_factor

    # Apply retro factor, subject to  minimum premiums                   
    model_prem = max(model_prem * rating_factors.opt_coverages.retro_factor, minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.opt_coverages.retro_factor, minprem_net)

    # CPL Coverage     
    if (rating_factors.opt_coverages.cpl == True):
        rating_factors.opt_coverages.cpl_factor = 1            
    else:
        # 5% discount if opt out
        rating_factors.opt_coverages.cpl_factor = 0.95
        model_prem_non_min = model_prem_non_min * rating_factors.opt_coverages.cpl_factor
        model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.opt_coverages.cpl_factor
        model_prem = max(model_prem * rating_factors.opt_coverages.cpl_factor,minprem_net)
        model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.opt_coverages.cpl_factor,minprem_net)

    # Tech Coverage
    # tech coverage factor depends on wherther cpl coverage is taken        

    if (rating_factors.opt_coverages.tech == True):
        rating_factors.opt_coverages.tech_cpl_factor = 1            
    elif (rating_factors.opt_coverages.cpl == False):
        rating_factors.opt_coverages.tech_cpl_factor = 0.925 / rating_factors.opt_coverages.cpl_factor
        # capped at 7.5% discount if they don't take CPL and Tech coverages
        model_prem_non_min = model_prem_non_min * rating_factors.opt_coverages.tech_cpl_factor
        model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.opt_coverages.tech_cpl_factor
        model_prem = max(model_prem * rating_factors.opt_coverages.tech_cpl_factor,minprem_net)
        model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.opt_coverages.tech_cpl_factor,minprem_net)
    else:
        rating_factors.opt_coverages.tech_cpl_factor = 0.95
        model_prem_non_min = model_prem_non_min * rating_factors.opt_coverages.tech_cpl_factor
        model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.opt_coverages.tech_cpl_factor
        model_prem = max(model_prem * rating_factors.opt_coverages.tech_cpl_factor,minprem_net)
        model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.opt_coverages.tech_cpl_factor,minprem_net)

    # Primary NoN Contributary
    # Primary NoN Contributary Factor      
    if (rating_factors.opt_coverages.non_contributary == True):
        # 5% AP if opt to select PNC
        rating_factors.opt_coverages.non_contributary_factor = 1.05            
        model_prem_non_min = model_prem_non_min * rating_factors.opt_coverages.non_contributary_factor
        model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * rating_factors.opt_coverages.non_contributary_factor
        model_prem = max(model_prem * rating_factors.opt_coverages.non_contributary_factor,minprem_net)
        model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * rating_factors.opt_coverages.non_contributary_factor,minprem_net)    
    else:
        rating_factors.opt_coverages.non_contributary_factor = 1
   
    #### SCHEDULE RATING FACTORS ########################################

    # define schedule rating factor location
    mods_srf = hxd.cds.modifiers.schedule_rating_factor

    # create list to loop through all the schedule rating items
    lst_srf_vbl = [mods_srf.qual_of_staff,
                    mods_srf.rm_attendance,
                    mods_srf.foreign_work,
                    mods_srf.loss_prev,
                    mods_srf.client_type,
                    mods_srf.contractual_practices,
                    mods_srf.engi_procure_construct,
                    mods_srf.peer_review]

    mods_srf.total.factor = 1

    # set min and max for each schedule rating
    for loop_vbl in lst_srf_vbl:
        loop_vbl.min = -0.25
        loop_vbl.max = 0.5

        # set total min, max and factor
        mods_srf.total.min = -0.25
        mods_srf.total.max = 0.5
        mods_srf.total.factor *= (1 + loop_vbl.factor)
    
    # cap total factor at between -0.25 and 0.25
    mods_srf.total.factor = min(max(mods_srf.total.factor - 1, -0.25),0.5)
    
    # Apply total schedule rating factor
    model_prem_non_min = model_prem_non_min * (1+mods_srf.total.factor)
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * 1
    model_prem = max(model_prem * (1+mods_srf.total.factor),minprem_net)
    model_prem_pre_uw_adj = max(model_prem_pre_uw_adj * 1,minprem_net)

    # RATING SUMMARY ########################################       

    # PRIMARY OPTIONS CALCULATIONS ########################################       

    ## Populate Override fields in the options table:
    
    # Primary brokerage and aggregate limit
    for i, option in enumerate(options):
        setattr(option.brokerage_primary, "calculated", brokerage)
        setattr(option.aggregate_limit, "calculated", getattr(option, "limit"))

    # Excess brokerage
    for i, option in enumerate(options):
        for j in range (1, max_excess_layers+1):
            setattr(getattr(option, f"excess_{j}_brokerage"), "calculated", getattr(option.brokerage_primary, "selected"))

    
    # Options location
    # Note that overrides in a list don't get called in properly in the RARC calcs, therefore need to call override nodes in separately and merge onto dataframe
    options = utils.pd_df_from_hx_list(hxd.cds.options)
    
    # Call override node
    guideline_deductible = []    
    for i in range(options.shape[0]):
        guideline_deductible.append(getattr(getattr(hxd.cds.options[i], "guideline_deductible"),"selected"))

    # Convert to dataframe
    guideline_deductible_df = pd.DataFrame({'guideline_deductible':guideline_deductible})

    # Replace override node in options with guideline deductible
    options["guideline_deductible"] = guideline_deductible_df["guideline_deductible"]    

    # Beazley or carrier primary
    hxd.cds.carrier_primary = not all(options["beazley_primary"])

    # Define output variables    
    options.quoted_premium_view = options.quoted_premium

    # ILF
    # ILF params table, levels, and columns
    param_ilf = hx.params.tbl_ilfs
    param_ilf_lev = param_ilf["Limit"].to_numpy()
    param_ilf_light_factor = param_ilf["Light"].to_numpy()
    param_ilf_heavy_factor = param_ilf["Heavy"].to_numpy()
    param_ilf_BUSA_factor = param_ilf["BUSA A&E"].to_numpy()

    # Lookup parameter value
    options["ilf_factor"] = np.where(
        options["ilf_type"] == "Light",
        np.interp(options["limit"],param_ilf_lev, param_ilf_light_factor),
        np.where(options["ilf_type"] == "Heavy",
            np.interp(options["limit"],param_ilf_lev, param_ilf_heavy_factor),
            np.interp(options["limit"],param_ilf_lev, param_ilf_BUSA_factor)
        ))


    # NUMBER OF REINSTATEMENTS
    # Number of reinstatements params table
    param_reinstatements = hx.params.tbl_reinstatements
    param_reinstatements_no = param_reinstatements["Number of Reinstatement"].to_numpy()
    param_reinstatements_factor = param_reinstatements["Factor"].to_numpy()

    # Calculate number of reinstatements (can be any number)
    number_of_reinstatements = np.where(options.aggregate_limit <= options.limit, 1, ratio(options.aggregate_limit, options.limit)) - 1
    # updated to take the value of the ratio between the aggregate limit and individual limit
    options.number_of_reinstatements = number_of_reinstatements + 1
    # Look up reinstatement factor value from parameters table    
    options["reinstatements_factor"] = np.interp(number_of_reinstatements, param_reinstatements_no, param_reinstatements_factor)

    # DEDUCTIBLE
    # Deductible param table, levels and factors
    param_deductible = hx.params.tbl_quotedguidelineded
    param_deductible_upper_lev = param_deductible["Upper Ratio"].to_numpy()
    param_deductible_upper_factor = param_deductible["Upper Ratio Factor"].to_numpy()

    # Guideline Deductible
    # Look up guideline deductible from parameters table
    exposure =  hxd.cds.exposure.granular 
    options.minimum_deductible = min_deductible

    rateable_exposure = exposure.total.override_avg_rateable_exposure.selected
    if rateable_exposure <= 1_000_000:
        guideline_deductible = rateable_exposure * 0.0075
    elif rateable_exposure >= 5_000_000:
        guideline_deductible = np.minimum(rateable_exposure, 300_000_000) * 0.005
    else:
        # interpolate guideline deductible rate between 1m and 5m
        guideline_deductible = (1_000_000 * 0.0075) + (rateable_exposure - 1_000_000) / (5_000_000 - 1_000_000) * ((5_000_000 * 0.005) - (1_000_000 * 0.0075))

    # Calculated
    options["guideline_deductible_calculated"] = np.maximum(guideline_deductible, options.minimum_deductible)
    options["guideline_deductible_calculated"] = np.maximum(2000, options["guideline_deductible_calculated"])

    # If UW selected exist, take UW selected, else pick calculated
    options["guideline_deductible_selected"] = np.where(options["guideline_deductible"].isna() , options["guideline_deductible_calculated"], options["guideline_deductible"])

    # Is minimum deductible being used in guideline deductible?
    options["minimum_deductible_flag"] = np.where(options["guideline_deductible_selected"] == options["minimum_deductible"], "Yes","No")  

    # Look up factor value from parameters table        
    # calculate qg_deductible factor
    qg_deductible = options.deductible / options.guideline_deductible_selected        
    # Model calculated number required to work out UW adjustment
    qg_deductible_calculated = options.deductible / options.guideline_deductible_calculated    
    # qg_deductible = options.deductible / options.guideline_deductible
      
    # deductible factor (interpolate between levels)
    options.deductible_factor = np.interp(qg_deductible, param_deductible_upper_lev, param_deductible_upper_factor)
    options.deductible_factor_calculated = np.interp(qg_deductible_calculated, param_deductible_upper_lev, param_deductible_upper_factor)
    
    # Apply ILF, deductible and reinstatement factors
    # minimum premiums are $1M ILF and 0 deductible
    model_prem_non_min = model_prem_non_min * options.ilf_factor * options.reinstatements_factor * options.deductible_factor
    model_prem_non_min_pre_uw_adj = model_prem_non_min_pre_uw_adj * options.ilf_factor * options.reinstatements_factor * options.deductible_factor_calculated

    # Apply ILF, deductible and reinstatement factors, subjected to minimum
    minprem_after_ilf_ded = minprem_net * options.ilf_factor * options.reinstatements_factor * options.deductible_factor
    model_prem = np.maximum(model_prem * options.ilf_factor * options.reinstatements_factor * options.deductible_factor,minprem_after_ilf_ded)
    model_prem_pre_uw_adj = np.maximum(model_prem_pre_uw_adj * options.ilf_factor * options.deductible_factor,minprem_after_ilf_ded)   
       
    # Model premium
    model_premium_non_min_pre_term = model_prem_non_min
    model_premium_non_min_pre_term_pre_uw_adj = model_prem_non_min_pre_uw_adj
    model_premium_net_pre_term = model_prem
    model_premium_net_pre_term_pre_uw_adj = model_prem_pre_uw_adj

    # FX rate and term adjustment
    # FX rate parameter table
    param_ccy = hx.params.tbl_ccy

    # Currency
    # Save in cds
    hxd.cds.currencies.source_currency = hxd.cds.ccy

    # Use in calc
    ccy = hxd.cds.ccy    

    # Currency factor
    hxd.cds.ccy_factor = look_up(ccy, 'Currency code', 'Units Per USD', param_ccy, if_not_found=1)    

    # Term adjustment factor
    hxd.cds.standard_fields.inception_date = hxd.hx_core.inception_date
    hxd.cds.standard_fields.expiry_date = hxd.hx_core.expiry_date
    hxd.cds.term_adj_factor = round((hxd.cds.standard_fields.expiry_date - hxd.cds.standard_fields.inception_date).days / 365.25,2)

    # Apply term adjustment factor    
    minprem_net = minprem_net * hxd.cds.term_adj_factor
    model_premium_non_min = model_premium_non_min_pre_term * hxd.cds.term_adj_factor
    model_premium_non_min_pre_uw_adj = model_premium_non_min_pre_term_pre_uw_adj * hxd.cds.term_adj_factor
    model_premium_net = model_premium_net_pre_term * hxd.cds.term_adj_factor
    model_premium_net_pre_uw_adj = model_premium_net_pre_term_pre_uw_adj * hxd.cds.term_adj_factor

    # Gross model premium under policy brokerage
    options.minimum_premium = minprem_after_ilf_ded / (1 - brokerage)
    options.model_premium = model_premium_net / (1 - brokerage)
    options.model_premium_pre_uw_adj = model_premium_net_pre_uw_adj / (1 - brokerage)

    # Rebase gross model premium to option brokerage 
    options.minimum_premium = options.minimum_premium * (1 - options.brokerage_primary) / (1 - brokerage)
    options.model_premium = options.model_premium * (1 - options.brokerage_primary) / (1 - brokerage)
    options.model_premium_pre_uw_adj = options.model_premium_pre_uw_adj * (1 - options.brokerage_primary) / (1 - brokerage)
         
    # TPI SUMMARY CALCS #############################################################################################

    # Pull in technical premium parameters and fx rates from user library
    tp_params_df = params.tp_parameters.df()

    year = calc_tp_year(hxd)
    tp_params_df = tp_params_df[(tp_params_df['business_plan_class'] == bp_class) & (tp_params_df['year'] == year)]

    # Look up tp params
    che = tp_params_df['che'].iloc[0]
    var_exp = tp_params_df['var_exp'].iloc[0]
    inv_inc = tp_params_df['inv_inc'].iloc[0]
    cost_of_ri = tp_params_df['cost_of_ri'].iloc[0]
    ri_rec = tp_params_df['ri_rec'].iloc[0]
    roc = tp_params_df['roc'].iloc[0]
    fixed_exp_usd = tp_params_df['fixed_exp'].iloc[0]
    capital_req = tp_params_df['capital_req'].iloc[0]
    nmp_load = tp_params_df['nmp_load'].iloc[0]    

    # Convert fixed expenses to model currency (default to USD if error)             
    # Fixed expenses treated as local currency
    fixed_exp = fixed_exp_usd

    # assumed lr
    assumed_lr = assumed_lr_const    

    # expected loss cost
    expected_loss_non_min = assumed_lr * model_premium_non_min * (1 + nmp_load)
    expected_loss_non_min_pre_uw_adj = assumed_lr * model_premium_non_min_pre_uw_adj * (1 + nmp_load)

    # Gross benchmark premium    
    options.benchmark_premium = np.maximum(ratio(ratio(expected_loss_non_min, benchmark_lr_const),(1 - options.brokerage_primary)), options.model_premium)
    options.benchmark_premium_pre_uw_adj = np.maximum(ratio(ratio(expected_loss_non_min_pre_uw_adj, benchmark_lr_const),(1 - options.brokerage_primary)),options.model_premium_pre_uw_adj)

    # expected loss cost (subject to minimums)    
    options.expected_loss_cost = options.benchmark_premium * benchmark_lr_const * (1 - options.brokerage_primary)
    options.expected_loss_cost_pre_uw_adj = options.benchmark_premium_pre_uw_adj * benchmark_lr_const * (1 - options.brokerage_primary)
    
    # Primary 1m expected loss cost - back out the ILF and reinstatement factor from the primary expected loss cost to use it as a base loss cost for excess layer pricing
    options.expected_loss_cost_primary_1m = options.expected_loss_cost / (options.ilf_factor * options.reinstatements_factor)
    options.expected_loss_cost_pre_uw_adj_primary_1m = options.expected_loss_cost_pre_uw_adj / (options.ilf_factor * options.reinstatements_factor)
    # Primary 1m net model premium - back out the ILF from the primary net model prem to use as a base premium for excess layer model premium calculation 
    options.model_premium_net_primary_1m = options.model_premium * (1 - options.brokerage_primary) / (options.ilf_factor * options.reinstatements_factor)
    options.model_premium_net_pre_uw_adj_primary_1m = options.model_premium_pre_uw_adj * (1 - options.brokerage_primary) / (options.ilf_factor * options.reinstatements_factor)

    # technical loss ratio (excl. fixed costs)
    technical_lr = 1 - var_exp + inv_inc - (cost_of_ri - ri_rec) - roc*capital_req

    # Net technical premium
    technical_premium_net = ratio((options.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
    technical_premium_net_pre_uw_adj = ratio((options.expected_loss_cost_pre_uw_adj*(1+che) + fixed_exp), technical_lr)
    options.technical_premium_net = technical_premium_net
    options["technical_premium_net_pre_uw_adj"] = technical_premium_net_pre_uw_adj

    # Gross technical premium
    options.technical_premium = options.technical_premium_net / (1-options.brokerage_primary)
    options.technical_premium_pre_uw_adj = technical_premium_net_pre_uw_adj / (1-options.brokerage_primary)    

    # BPI and TPI
    options.bpi = ratio(options.quoted_premium, options.benchmark_premium)    

    options.tpi = ratio(options.quoted_premium, options.technical_premium)
    if hxd.cds.standard_fields.is_rater_priced:
        options.tpi_pre_uw_adj = ratio(options.quoted_premium, options.technical_premium_pre_uw_adj)
        options.bpi_pre_uw_adj = ratio(options.quoted_premium, options.benchmark_premium_pre_uw_adj)
    else:
        options.tpi_pre_uw_adj = 0
        options.bpi_pre_uw_adj = 0
        
    options.quoted_premium_net = options.quoted_premium * (1 - options.brokerage_primary)  

    expected_loss_val = options.expected_loss_cost * (1 + nmp_load)
    expected_loss_pre_adj = options.expected_loss_cost_pre_uw_adj * (1 + nmp_load)
    options.pflr = np.where(options.quoted_premium_net == 0, 0, ratio(expected_loss_val, options.quoted_premium_net))
    options.pflr_pre_uw_adj = np.where(options.quoted_premium_net == 0, 0, ratio(expected_loss_pre_adj, options.quoted_premium_net))
    options.uw_adj_impact =  (options.expected_loss_cost_pre_uw_adj / options.expected_loss_cost) - 1

    # roc
    options.roc = np.where(options.quoted_premium_net == 0,
    0,
    ratio(1 - options.pflr - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + options.expected_loss_cost*che, options.quoted_premium_net), capital_req))   
    
    # Minimum premium flag #################################################################    

    # Set up minimum premium flags to flag if whether minimum premiums are being used
    options["minimum_premium_flag"] = np.where(options["benchmark_premium"] == options["minimum_premium"], "Yes",
        np.where(options["technical_premium"] == options["minimum_premium"], "Yes", "No"))

    # Excess calculations - all options #################################################################

    # ILF params table, levels, and columns
    param_ilf = hx.params.tbl_ilfs
    param_ilf_lev = param_ilf["Limit"].to_numpy()
    param_ilf_light_factor = param_ilf["Light"].to_numpy()
    param_ilf_heavy_factor = param_ilf["Heavy"].to_numpy()
    param_ilf_BUSA_factor = param_ilf["BUSA A&E"].to_numpy()
   
    for layer in range(1, max_excess_layers+1):
        # Show / hide additional rows in excess layer tables
        setattr(hxd.cds, f"excess_{layer}_beazley_participation", any(options[f"excess_{layer}_beazley_participation"]))

        #### Set excess / cumulative attachment - this is the sum of the excess and limit from the previous layer 
        # _excess is used for RARC calc 
        # _cum_attachment is displayed in the Rating Summary page
        if layer == 1:
            options[f"excess_{layer}_excess"] = options.limit
        else:
            options[f"excess_{layer}_excess"] = options[f"excess_{layer-1}_cum_attachment"] + options[f"excess_{layer-1}_limit"]

        # For RARC calc 
        # - write the excess_{layer}_excess values to the calculated value of the override node 
        # - and then re-import the selected value of the node back into the options table to be used in the rest of the calculation 
        utils.write_pd_to_hxd(options, hxd.cds.options, [], [f"excess_{layer}_excess"])
        options[f"excess_{layer}_excess"] = utils.pd_df_from_hx_list(hxd.cds.options)[f"excess_{layer}_excess"]

        options[f"excess_{layer}_cum_attachment"] = options[f"excess_{layer}_excess"]
       
        #### Get ILF for the layer 
        # ILF for attachment
        options[f"excess_{layer}_ilf_attach"] = np.where(
            options["ilf_type"] == "Light",
            np.interp(options[f"excess_{layer}_cum_attachment"], param_ilf_lev, param_ilf_light_factor),
            np.where(
                options["ilf_type"] == "Heavy",
                np.interp(options[f"excess_{layer}_cum_attachment"], param_ilf_lev, param_ilf_heavy_factor),
                np.interp(options[f"excess_{layer}_cum_attachment"], param_ilf_lev, param_ilf_BUSA_factor),
            )
        )
        # ILF for attachment + limit
        options[f"excess_{layer}_ilf_limit_attach"] = np.where(
            options["ilf_type"] == "Light",
            np.interp(options[f"excess_{layer}_cum_attachment"] + options[f"excess_{layer}_limit"], param_ilf_lev, param_ilf_light_factor),
            np.where(
                options["ilf_type"] == "Heavy",
                np.interp(options[f"excess_{layer}_cum_attachment"] + options[f"excess_{layer}_limit"], param_ilf_lev, param_ilf_heavy_factor),
                np.interp(options[f"excess_{layer}_cum_attachment"] + options[f"excess_{layer}_limit"], param_ilf_lev, param_ilf_BUSA_factor),
            )
        )
        # ILF for layer 
        options[f"excess_{layer}_ilf_curve"] = options[f"excess_{layer}_ilf_limit_attach"] - options[f"excess_{layer}_ilf_attach"]

        #### Technical Premium               
        # calculate technical premiums for current layer using ILF curve on the primary 1m expected loss
        options[f"excess_{layer}_expected_loss_cost"] = options.expected_loss_cost_primary_1m * options[f"excess_{layer}_ilf_curve"]
        options[f"excess_{layer}_expected_loss_cost_pre_uw_adj"] = options.expected_loss_cost_pre_uw_adj_primary_1m * options[f"excess_{layer}_ilf_curve"]

        options[f"excess_{layer}_technical_premium_net"] = ratio((options[f"excess_{layer}_expected_loss_cost"]*(1+che) + fixed_exp), technical_lr)
        options[f"excess_{layer}_technical_premium_net_pre_uw_adj"] = ratio((options[f"excess_{layer}_expected_loss_cost_pre_uw_adj"]*(1+che) + fixed_exp), technical_lr)

        options[f"excess_{layer}_model_premium_net"] = options.model_premium_net_primary_1m * options[f"excess_{layer}_ilf_curve"]
        options[f"excess_{layer}_model_premium_net_pre_uw_adj"] = options.model_premium_net_pre_uw_adj_primary_1m * options[f"excess_{layer}_ilf_curve"]

        options[f"excess_{layer}_technical_premium"] = options[f"excess_{layer}_technical_premium_net"] / (1 - options[f"excess_{layer}_brokerage"])
        options[f"excess_{layer}_technical_premium_pre_uw_adj"] = options[f"excess_{layer}_technical_premium_net_pre_uw_adj"] / (1 - options[f"excess_{layer}_brokerage"])
        options[f"excess_{layer}_model_premium"] = options[f"excess_{layer}_model_premium_net"] / (1 - options[f"excess_{layer}_brokerage"])
        options[f"excess_{layer}_model_premium_pre_uw_adj"] = options[f"excess_{layer}_model_premium_net_pre_uw_adj"] / (1 - options[f"excess_{layer}_brokerage"])
        
        # Benchmark Premium 
        # Reverse out expected loss for roc calculations (as excess technical/benchmark premiums are based on ILF curves on the primary technical/benchmark premiums)
        # benchmark premium calculated based on technical premium. Adding a max here as if there's no technical premium entered, expected loss would be negative due to fixed expenses
        options[f"excess_{layer}_expected_loss_cost_inc_nmp"] = options[f"excess_{layer}_expected_loss_cost"] * (1 + nmp_load)
        options[f"excess_{layer}_expected_loss_cost_inc_nmp_pre_uw_adj"] = options[f"excess_{layer}_expected_loss_cost_pre_uw_adj"] * (1 + nmp_load)

        options[f"excess_{layer}_benchmark_premium"] = ratio(ratio(options[f"excess_{layer}_expected_loss_cost"], benchmark_lr_const), (1 - options[f"excess_{layer}_brokerage"]))
        options[f"excess_{layer}_benchmark_premium_pre_uw_adj"] = ratio(ratio(options[f"excess_{layer}_expected_loss_cost_pre_uw_adj"], benchmark_lr_const), (1 - options[f"excess_{layer}_brokerage"]))

        # TPI and BPI
        options[f"excess_{layer}_quoted_premium"] = options[f"excess_{layer}_quoted_premium"].fillna(0).astype(float)
        options[f"excess_{layer}_quoted_premium_net"] = options[f"excess_{layer}_quoted_premium"] * (1 - options[f"excess_{layer}_brokerage"])

        options[f"excess_{layer}_carrier_premium"] = options[f"excess_{layer}_carrier_premium"].fillna(0).astype(float)
        options[f"excess_{layer}_carrier_premium_net"] = options[f"excess_{layer}_carrier_premium"] * (1 - options[f"excess_{layer}_brokerage"])

        options[f"excess_{layer}_tpi"] = np.where(options[f"excess_{layer}_technical_premium"] == 0, 0, options[f"excess_{layer}_quoted_premium"] / options[f"excess_{layer}_technical_premium"])
        options[f"excess_{layer}_tpi_pre_uw_adj"] = np.where(options[f"excess_{layer}_technical_premium_pre_uw_adj"] == 0, 0, options[f"excess_{layer}_quoted_premium"] / options[f"excess_{layer}_technical_premium_pre_uw_adj"])
        options[f"excess_{layer}_bpi"] = np.where(options[f"excess_{layer}_benchmark_premium"] == 0, 0, options[f"excess_{layer}_quoted_premium"] / options[f"excess_{layer}_benchmark_premium"])
        options[f"excess_{layer}_bpi_pre_uw_adj"] = np.where(options[f"excess_{layer}_benchmark_premium_pre_uw_adj"] == 0, 0, options[f"excess_{layer}_quoted_premium"] / options[f"excess_{layer}_benchmark_premium_pre_uw_adj"])

        options[f"excess_{layer}_carrier_tpi"] = np.where(options[f"excess_{layer}_technical_premium"] == 0, 0, options[f"excess_{layer}_carrier_premium"] / options[f"excess_{layer}_technical_premium"])
        options[f"excess_{layer}_carrier_bpi"] = np.where(options[f"excess_{layer}_benchmark_premium"] == 0, 0, options[f"excess_{layer}_carrier_premium"] / options[f"excess_{layer}_benchmark_premium"])

        # PFLR
        options[f"excess_{layer}_pflr"] = np.where(options[f"excess_{layer}_quoted_premium_net"] == 0, 0, options[f"excess_{layer}_expected_loss_cost_inc_nmp"] / options[f"excess_{layer}_quoted_premium_net"])
        options[f"excess_{layer}_pflr_pre_uw_adj"] = np.where(options[f"excess_{layer}_quoted_premium_net"] == 0, 0, options[f"excess_{layer}_expected_loss_cost_inc_nmp_pre_uw_adj"] / options[f"excess_{layer}_quoted_premium_net"])

        # ROC 
        options[f"excess_{layer}_roc"] = np.where((options[f"excess_{layer}_quoted_premium_net"] == 0) | (options[f"excess_{layer}_technical_premium"] == 0), 0, \
            (1 - options[f"excess_{layer}_pflr"] - var_exp + inv_inc - (cost_of_ri-ri_rec) - \
                ((fixed_exp + options[f"excess_{layer}_expected_loss_cost"]*che) / options[f"excess_{layer}_quoted_premium_net"])) / capital_req)

    # save down to data schema #################################################################
    # options table has values at 100%, not AFB    

    # rename 
    # options.rename(columns={'guideline_deductible': 'guideline_deductible_calculated'}, inplace=True)

    lst_vbls = [
    "number_of_reinstatements",   
    "benchmark_premium",
    "benchmark_premium_pre_uw_adj",    
    "technical_premium",
    "technical_premium_pre_uw_adj",
    "technical_premium_net",
    "quoted_ilf_curve",
    "quoted_premium_view",
    "bpi",
    "bpi_pre_uw_adj",
    "tpi",
    "tpi_pre_uw_adj",
    "pflr",
    "pflr_pre_uw_adj",
    "pflr_att",
    "roc",
    "ilf_factor",
    "reinstatements_factor",
    "deductible_factor",
    "expected_loss_cost",
    "expected_loss_cost_pre_uw_adj",
    "quoted_premium_net",
    "model_premium",
    "model_premium_pre_uw_adj",
    "quoted_premium_view",
    "minimum_premium",
    "minimum_premium_flag",
    "minimum_deductible_flag",
    ]

    excess_vbls = [
        *[f"excess_{layer}_cum_attachment" for layer in range(1,max_excess_layers+1)],
        *[f"excess_{layer}_ilf_curve" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_technical_premium" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_benchmark_premium" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_tpi" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_bpi" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_pflr" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_roc" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_carrier_tpi" for layer in range(1, max_excess_layers+1)],
        *[f"excess_{layer}_carrier_bpi" for layer in range(1, max_excess_layers+1)],
        ]
    
    lst_vbls.extend(excess_vbls)
    
    lst_vbls_override = [
        *[f"excess_{layer}_excess" for layer in range(1, max_excess_layers+1)],
    ]

    utils.write_pd_to_hxd(options, hxd.cds.options, lst_vbls, lst_vbls_override)

    # Save down overrideable variable
    for i in range(options.shape[0]):
        setattr(getattr(hxd.cds.options[i], "guideline_deductible"),"calculated",options["guideline_deductible_calculated"][i])

    # Primary option selected #################################################################    

    # Selected option

    selected_option = int(hxd.cds.option_selected - 1)

    # For view page because cannot show two lists (e.g. options list and excess list) in one, so set up primary structure to capture selected primary option
    # primary data schema
    primary = hxd.cds.primary

    # Set primary attributs to selected option    
    primary.limit = options.limit[selected_option]
    primary.model_premium = options.model_premium[selected_option]
    primary.benchmark_premium_100 = options.benchmark_premium[selected_option]
    primary.technical_premium_100 = options.technical_premium[selected_option]
    primary.quoted_premium_100 = options.quoted_premium_view[selected_option]
    primary.benchmark_premium = primary.benchmark_premium_100 * written_line
    primary.technical_premium = primary.technical_premium_100 * written_line
    primary.quoted_premium = primary.quoted_premium_100 * written_line
    primary.brokerage = options.brokerage_primary[selected_option]
    primary.carrier = options.carrier[selected_option]
    primary.carrier_premium = options.carrier_premium[selected_option]
    primary.bpi = options.bpi[selected_option]
    primary.tpi = options.tpi[selected_option]
    primary.pflr = options.pflr[selected_option]
    primary.pflr_att = options.pflr_att[selected_option]
    primary.roc = options.roc[selected_option]    

    # EXCESS OPTION SELECTED #############################################

    # cds
    layers = hxd.cds.layers

    # Loop through excess layers and assign layer nodes from options dataframe based on the selected option 
    for index, layer in enumerate(layers):
        if index == 0:
            layer.layer_label = "Primary"                                           # Set the label for each layer
            layer.excess_flag = False                                               # Set up for view page
            layer.is_primary_excess = "Primary"
            layer.written_line = written_line
            layer.brokerage = options.brokerage_primary[selected_option]
            layer.status = primary.status_view
            layer.section_reference = primary.section_reference_view
            layer.limit = options.limit[selected_option]
            layer.deductible = options.deductible[selected_option]
            layer.aggregate_limit = options.aggregate_limit[selected_option]
            layer.cum_attachment = 0
            layer.excess = 0
            layer.ilf_curve = options.ilf_factor[selected_option]
            layer.technical_premium_100 = options.technical_premium[selected_option]
            layer.technical_premium = layer.technical_premium_100 * written_line
            layer.technical_premium_pre_uw_adj = options.technical_premium_pre_uw_adj[selected_option] * written_line
            layer.technical_premium_net = options.technical_premium_net[selected_option] * written_line
            layer.model_premium = options.model_premium[selected_option] * written_line
            layer.model_premium_pre_uw_adj = options.model_premium_pre_uw_adj[selected_option] * written_line
            layer.quoted_premium_100 = options.quoted_premium[selected_option]
            layer.quoted_premium_annual_100 = layer.quoted_premium_100 / hxd.cds.term_adj_factor
            layer.quoted_premium = layer.quoted_premium_100 * written_line
            layer.quoted_premium_annual = layer.quoted_premium / hxd.cds.term_adj_factor
            layer.quoted_premium_net = options.quoted_premium_net[selected_option] * written_line
            layer.expected_loss_cost_100 = options.expected_loss_cost[selected_option]
            layer.expected_loss_cost = layer.expected_loss_cost_100 * written_line
            layer.expected_loss_cost_pre_uw_adj = options.expected_loss_cost_pre_uw_adj[selected_option] * written_line
            layer.benchmark_premium_100 = options.benchmark_premium[selected_option]
            layer.benchmark_premium_annual_100 = layer.benchmark_premium_100 / hxd.cds.term_adj_factor
            layer.benchmark_premium = layer.benchmark_premium_100 * written_line
            layer.benchmark_premium_annual = layer.benchmark_premium / hxd.cds.term_adj_factor
            layer.benchmark_premium_pre_uw_adj = options.benchmark_premium_pre_uw_adj[selected_option] * written_line
            layer.tpi = options.tpi[selected_option]
            layer.tpi_pre_uw_adj = options.tpi_pre_uw_adj[selected_option]
            layer.bpi = options.bpi[selected_option]
            layer.bpi_pre_uw_adj = options.bpi_pre_uw_adj[selected_option]
            layer.pflr = options.pflr[selected_option]
            layer.pflr_pre_uw_adj = options.pflr_pre_uw_adj[selected_option]
            layer.pflr_att = options.pflr_att[selected_option]
            layer.roc = options.roc[selected_option]
        else:
            layer.layer_label = f"Excess {index}"                                   # Set the label for each layer
            layer.excess_flag = getattr(hxd.cds, f"add_excess_{index}")             # Set up for view page
            layer.is_primary_excess = "Excess"
            layer.written_line = layer.written_line_view
            layer.brokerage = options[f"excess_{index}_brokerage"][selected_option]
            layer.status = layer.status_view
            layer.section_reference = layer.section_reference_view
            layer.limit = options[f"excess_{index}_limit"][selected_option]
            layer.deductible = 0
            layer.cum_attachment = options[f"excess_{index}_cum_attachment"][selected_option]
            layer.excess = layer.cum_attachment
            layer.ilf_curve = options[f"excess_{index}_ilf_curve"][selected_option]
            layer.technical_premium_100 = options[f"excess_{index}_technical_premium"][selected_option]
            layer.technical_premium = layer.technical_premium_100 * written_line
            layer.technical_premium_pre_uw_adj = options[f"excess_{index}_technical_premium_pre_uw_adj"][selected_option] * written_line
            layer.technical_premium_net = options[f"excess_{index}_technical_premium_net"][selected_option] * written_line
            layer.model_premium = options[f"excess_{index}_model_premium"][selected_option] * written_line
            layer.model_premium_pre_uw_adj = options[f"excess_{index}_model_premium_pre_uw_adj"][selected_option] * written_line
            layer.quoted_premium_100 = options[f"excess_{index}_quoted_premium"][selected_option]
            layer.quoted_premium_annual_100 = layer.quoted_premium_100 / hxd.cds.term_adj_factor
            layer.quoted_premium = layer.quoted_premium_100 * written_line
            layer.quoted_premium_annual = layer.quoted_premium / hxd.cds.term_adj_factor
            layer.quoted_premium_net = options[f"excess_{index}_quoted_premium_net"][selected_option] * written_line
            layer.expected_loss_cost_100 = options[f"excess_{index}_expected_loss_cost"][selected_option]
            layer.expected_loss_cost = layer.expected_loss_cost_100 * written_line
            layer.expected_loss_cost_pre_uw_adj = options[f"excess_{index}_expected_loss_cost_pre_uw_adj"][selected_option] * written_line
            layer.benchmark_premium_100 = options[f"excess_{index}_benchmark_premium"][selected_option]
            layer.benchmark_premium_annual_100 = layer.benchmark_premium_100 / hxd.cds.term_adj_factor
            layer.benchmark_premium = layer.benchmark_premium_100 * written_line
            layer.benchmark_premium_annual = layer.benchmark_premium / hxd.cds.term_adj_factor
            layer.benchmark_premium_pre_uw_adj = options[f"excess_{index}_benchmark_premium_pre_uw_adj"][selected_option] * written_line
            layer.tpi = options[f"excess_{index}_tpi"][selected_option]
            layer.tpi_pre_uw_adj = options[f"excess_{index}_tpi_pre_uw_adj"][selected_option]
            layer.bpi = options[f"excess_{index}_bpi"][selected_option]
            layer.bpi_pre_uw_adj = options[f"excess_{index}_bpi_pre_uw_adj"][selected_option]
            layer.pflr = options[f"excess_{index}_pflr"][selected_option]
            layer.pflr_pre_uw_adj = options[f"excess_{index}_pflr_pre_uw_adj"][selected_option]
            layer.pflr_att = ratio(benchmark_lr_const, layer.bpi)
            layer.roc = options[f"excess_{index}_roc"][selected_option]

        # for all layers 
        layer.currency = hxd.cds.ccy
        # UW Impact 
        if (layer.expected_loss_cost_pre_uw_adj == 0 or layer.expected_loss_cost_pre_uw_adj == None or layer.expected_loss_cost == 0 or layer.expected_loss_cost == None):
            layer.uw_adj_impact = None
        else:    
            layer.uw_adj_impact = (layer.expected_loss_cost_pre_uw_adj / layer.expected_loss_cost) -1          
        # Convert to USD 
        layer.model_premium_usd = layer.model_premium / hxd.cds.ccy_factor
        layer.benchmark_premium_usd = layer.benchmark_premium / hxd.cds.ccy_factor
        layer.technical_premium_usd = layer.technical_premium / hxd.cds.ccy_factor
        layer.expected_loss_cost_usd = layer.expected_loss_cost / hxd.cds.ccy_factor
        
            
    #### For case pricing only ############################################################################################
    for option in hxd.cds.options:
        if hxd.cds.standard_fields.is_case_priced:
            if option.quoted_premium and option.bpi_case_priced:
                option.benchmark_premium_case_priced = ratio(option.quoted_premium, option.bpi_case_priced)
                option.expected_loss_cost = option.benchmark_premium_case_priced * benchmark_lr_const * (1-option.brokerage)
            
                option.technical_premium_net = ratio((option.expected_loss_cost*(1+che) + fixed_exp), technical_lr)
                option.technical_premium_case_priced = ratio(option.technical_premium_net, (1-option.brokerage))
                        
                option.tpi_case_priced = ratio(option.quoted_premium, option.technical_premium_case_priced)

                option.pflr_case_priced = ratio(benchmark_lr_const, option.bpi_case_priced)
            
                quoted_premium_net = option.quoted_premium * (1-option.brokerage)

                option.roc_case_priced = ratio(
                1 - option.pflr_case_priced - var_exp + inv_inc - (cost_of_ri-ri_rec) - ratio(fixed_exp + option.expected_loss_cost*che, quoted_premium_net),
                capital_req
                )
                option.bpi_case_priced_view = option.bpi_case_priced
            option.brokerage_view = option.brokerage
            option.written_line_case_priced = option.written_line_view

    