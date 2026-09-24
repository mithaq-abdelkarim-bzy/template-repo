# v0.5.0
import hx
import pandas as pd
import numpy as np
import algorithms.rate_constants as const
from algorithms import parameter_tables_schema as lib_params
from algorithms.rate_utilities import ratio, look_up, pd_df_from_hx_list, policy_term
from algorithms.rate_constants import benchmark_lr, PLAN_GNLR
from algorithms.data_schema.sch_rater_defined import RARC_COVERAGE_USE, RARC_INSURED_ASSET_USE
if RARC_COVERAGE_USE:
    from algorithms.data_schema.sch_rater_defined import coverages_dict



def get_tp_dict(tp_params_df, yoa, bp_class, fx_rate):
    # filtering to bp_class first to avoid any rogue years on other classes
    tp_params_df         = tp_params_df[  (tp_params_df['business_plan_class'] == bp_class)   ]

    # filtering to year of account
    tp_params_df['year'] = tp_params_df['year'].astype(int)
    if yoa in list(tp_params_df['year']):
        tp_year = yoa
    else:
        tp_year_max = tp_params_df['year'].max()
        tp_year_min = tp_params_df['year'].min()
        tp_year     = np.clip(yoa, tp_year_min, tp_year_max)
    tp_params = tp_params_df[   (tp_params_df['year'].astype(int) == int(tp_year))   ]

    fx_rate = fx_rate or 1

    # Initialise and populate tp_dict
    tp_dict                 = {}
    tp_dict['che']          = tp_params['che'].iloc[0]
    tp_dict['var_exp']      = tp_params['var_exp'].iloc[0]
    tp_dict['inv_inc']      = tp_params['inv_inc'].iloc[0]
    tp_dict['cost_of_ri']   = tp_params['cost_of_ri'].iloc[0]
    tp_dict['ri_rec']       = tp_params['ri_rec'].iloc[0]
    tp_dict['roc']          = tp_params['roc'].iloc[0]
    tp_dict['capital_req']  = tp_params['capital_req'].iloc[0]
    tp_dict['nmp_load']     = tp_params['nmp_load'].iloc[0]
    tp_dict['fixed_exp_usd']= tp_params['fixed_exp'].iloc[0]
    tp_dict['fixed_exp']    = tp_dict['fixed_exp_usd'] * fx_rate

    # Calculate technical loss ratio (excl. fixed costs)
    tp_dict['technical_lr'] =(1 - tp_dict['var_exp'] 
                                + tp_dict['inv_inc'] 
                                - tp_dict['cost_of_ri'] 
                                + tp_dict['ri_rec']
                                - tp_dict['roc'] * tp_dict['capital_req'])
    return tp_dict


def calculate_premiums(hxd, cl, tp_dict, benchmark_lr, rf, exposure, limit, contribution):

    # getting the tp values from the dict
    nmp_load      = tp_dict['nmp_load'   ]
    che           = tp_dict['che'        ]
    fixed_exp     = tp_dict['fixed_exp'  ] * ratio(1, cl.written_line, 1) * contribution # grossing up fixed expenses to 100 pct level as they apply at the share level and apply contribution as we allocate down to coverage
    technical_lr  = tp_dict['technical_lr']
    var_exp       = tp_dict['var_exp'    ]
    inv_inc       = tp_dict['inv_inc'    ]
    cost_of_ri    = tp_dict['cost_of_ri' ]
    ri_rec        = tp_dict['ri_rec'     ]
    capital_req   = tp_dict['capital_req']

    # Calculate the impact of UW adjustment
    cl.uw_adj_impact = ratio(  cl.expected_loss_cost_100,   cl.expected_loss_cost_pre_uw_adj_100, 1) - 1

    # If rater priced
    if hxd.cds.standard_fields.is_rater_priced:                                         # Removed YZ request "and cl.quoted_premium_100"
        expected_loss_100                   = cl.expected_loss_cost_100                 # * (1 + nmp_load)   # REmoved nmp loading here, from typical in skeleton model as applies only to exposure
        exp_loss_pre_adj_100                = cl.expected_loss_cost_pre_uw_adj_100      # * (1 + nmp_load)   # REmoved nmp loading here, from typical in skeleton model as applies only to exposure
        quoted_premium_net_100              =(cl.quoted_premium_100 or 0)           * (1 - (cl.brokerage or 0))

        cl.technical_premium_net_100        = ratio( (expected_loss_100 * (1 + che) + fixed_exp), technical_lr)
        cl.technical_premium_100            = ratio( cl.technical_premium_net_100,                                        (1 - (cl.brokerage or 0)))
        cl.technical_premium_pre_uw_adj_100 = ratio( ratio((exp_loss_pre_adj_100 * (1 + che) + fixed_exp), technical_lr), (1 - (cl.brokerage or 0)))
        cl.benchmark_premium_100            = ratio( ratio(expected_loss_100, benchmark_lr),                              (1 - (cl.brokerage or 0)))

        cl.bpi                              = ratio(cl.quoted_premium_100, cl.benchmark_premium_100)
        cl.tpi                              = ratio(cl.quoted_premium_100, cl.technical_premium_100)
        cl.tpi_pre_uw_adj                   = ratio(cl.quoted_premium_100, cl.technical_premium_pre_uw_adj_100)
        cl.bpi_pre_uw_adj                   = cl.bpi * (cl.uw_adj_impact + 1)

        cl.pflr                             = ratio(expected_loss_100,    (quoted_premium_net_100 or 0))
        cl.pflr_pre_uw_adj                  = ratio(exp_loss_pre_adj_100, (quoted_premium_net_100 or 0))
        
        cl.roc      = ratio( 1  - cl.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec) 
                                - ratio(fixed_exp + expected_loss_100 * che, quoted_premium_net_100)
                             , capital_req)

    # For case pricing only
    if hxd.cds.standard_fields.is_case_priced and cl.bpi_case_priced:                       # Removed YZ request "and cl.quoted_premium_100"
        cl.quoted_premium_100   = cl.quoted_premium_100_case_priced
        cl.bpi                  = cl.bpi_case_priced
        cl.bpi_pre_uw_adj       = cl.bpi

        cl.benchmark_premium_100            = ratio(cl.quoted_premium_100,   cl.bpi)
        cl.expected_loss_cost_100           = cl.benchmark_premium_100 * benchmark_lr * (1 - (cl.brokerage or 0))
        cl.expected_loss_cost_pre_uw_adj_100= cl.expected_loss_cost_100
        cl.technical_premium_net_100        = ratio((cl.expected_loss_cost_100 * (1 + che) + fixed_exp), technical_lr)
        cl.technical_premium_100            = ratio(cl.technical_premium_net_100, (1 - (cl.brokerage or 0)))
        cl.technical_premium_pre_uw_adj_100 = cl.technical_premium_100
       
        quoted_premium_net_100              = (cl.quoted_premium_100 or 0)      * (1 - (cl.brokerage or 0))
        expected_loss_100                   = cl.expected_loss_cost_100

        cl.tpi              = ratio(cl.quoted_premium_100, cl.technical_premium_100)
        cl.tpi_pre_uw_adj   = cl.tpi
        cl.pflr             = ratio(benchmark_lr, cl.bpi)
        cl.pflr_pre_uw_adj  = cl.pflr

        cl.roc      = ratio( 1  - cl.pflr - var_exp + inv_inc - (cost_of_ri - ri_rec) 
                                - ratio(fixed_exp + expected_loss_100 * che, quoted_premium_net_100)
                             , capital_req)

    # NOTE - RARC requirement - Calculate annualised premium, insurer's share and net premium. These will be used for rate change and reporting
    cl.quoted_premium_annual_100        = (cl.quoted_premium_100        or 0) / (     rf.policy_term  or 1)
    cl.quoted_premium_annual            = (cl.quoted_premium_annual_100 or 0) * (     cl.written_line or 0)
    cl.quoted_premium_net_100           = (cl.quoted_premium_100        or 0) * (1 - (cl.brokerage    or 0))
    cl.quoted_premium                   = (cl.quoted_premium_100        or 0) * (     cl.written_line or 0)
    cl.quoted_premium_net               = (cl.quoted_premium            or 0) * (1 - (cl.brokerage    or 0))


    cl.benchmark_premium_annual_100     = (cl.benchmark_premium_100             or 0) / (     rf.policy_term  or 1)
    cl.benchmark_premium_annual         = (cl.benchmark_premium_annual_100      or 0) * (     cl.written_line or 0)
    cl.benchmark_premium_net_100        = (cl.benchmark_premium_100             or 0) * (1 - (cl.brokerage    or 0))
    cl.benchmark_premium                = (cl.benchmark_premium_100             or 0) * (     cl.written_line or 0)
    cl.benchmark_premium_net            = (cl.benchmark_premium                 or 0) * (1 - (cl.brokerage    or 0))
    cl.benchmark_premium_pre_uw_adj_100 = (cl.benchmark_premium_100             or 0) / (1 + (cl.uw_adj_impact or 0))  
    cl.benchmark_premium_pre_uw_adj     = (cl.benchmark_premium_pre_uw_adj_100  or 0) * (     cl.written_line or 0)


    cl.technical_premium_annual_100     = (cl.technical_premium_100        or 0) / (     rf.policy_term  or 1)
    cl.technical_premium_annual         = (cl.technical_premium_annual_100 or 0) * (     cl.written_line or 0)
    cl.technical_premium_net_100        = (cl.technical_premium_100        or 0) * (1 - (cl.brokerage    or 0))
    cl.technical_premium                = (cl.technical_premium_100        or 0) * (     cl.written_line or 0)
    cl.technical_premium_net            = (cl.technical_premium            or 0) * (1 - (cl.brokerage    or 0))
    cl.technical_premium_pre_uw_adj     = (cl.technical_premium_pre_uw_adj_100  or 0) * (cl.written_line or 0)


    # customisations
    cl.expected_loss_cost               = (cl.expected_loss_cost_100            or 0) * (cl.written_line or 0)
    cl.expected_loss_cost_pre_uw_adj    = (cl.expected_loss_cost_pre_uw_adj_100 or 0) * (cl.written_line or 0)
    cl.quoted_premium_annual            = (cl.quoted_premium_annual_100         or 0) * (cl.written_line or 0)
    cl.quoted_rol                   = ratio( cl.quoted_premium_100, limit)
    cl.quoted_roe                   = ratio( cl.quoted_premium_100, exposure)
    cl.plan_premium_100             = ratio(  ratio((cl.expected_loss_cost_100            * (1 + che)), PLAN_GNLR),    (1 - (cl.brokerage or 0)))
    cl.plan_premium_pre_uw_adj_100  = ratio(  ratio((cl.expected_loss_cost_pre_uw_adj_100 * (1 + che)), PLAN_GNLR),    (1 - (cl.brokerage or 0)))
    cl.plan_rol                     = ratio( cl.plan_premium_100,               limit)
    cl.plan_rol_pre_uw_adj          = ratio( cl.plan_premium_pre_uw_adj_100,    limit)

    cl.benchmark_rol                = ratio( cl.benchmark_premium_100,    limit)
    cl.technical_rol                = ratio( cl.technical_premium_100,    limit)

    cl.benchmark_rol_pre_uw_adj     = ratio( cl.benchmark_premium_pre_uw_adj_100,    limit)
    cl.technical_rol_pre_uw_adj     = ratio( cl.technical_premium_pre_uw_adj_100,    limit)





def rate_rating_summary(hxd, rater):
    
    # paths
    cds         = hxd.cds
    rf          = hxd.cds.rating_factors  
    sim_path    = hxd.cds.exposure.granular.event_cancel.simulation

    # Set rating methodology
    hxd.cds.standard_fields.is_case_priced  = hxd.cds.standard_fields.rating_methodology == 'Case Priced'
    hxd.cds.standard_fields.is_rater_priced = hxd.cds.standard_fields.rating_methodology == 'Rater'

    # sourcing simple scalar
    yoa     = hxd.hx_core.inception_date.year
    ccy     = hxd.cds.currencies.source_currency
    tp_dict = rater['tp_dict']
    nmp_load= tp_dict['nmp_load'   ]
 

    ### deriving event cancellation coverage always
    layer       = hxd.cds.layers[0]
    ec_exp_path = hxd.cds.exposure.granular.event_cancel.base_coverages
    ec_lay_path = hxd.cds.layers[0].coverages.ec_total        

    # getting exposure etc.
    exposure                = sum(rater['ec_events_df']['tiv'].fillna(0))
    exposure_est_overall    = ec_exp_path.ec_total.net_el_mod
    experience_est_overall  = hxd.cds.experience_rating.el_final  or 0
    experience_wgt          = hxd.cds.experience_rating.el_weight or 0
    allow_agg_factor        = sim_path.sim_agg_adj

    # getting limit/xs/deductible
    limit                = ec_lay_path.limit
    excess               = ec_lay_path.excess               if ec_lay_path.excess_use == True  else None
    deductible           = ec_lay_path.deductible           if ec_lay_path.excess_use == False else None
    aggregate_limit      = ec_lay_path.aggregate_limit
    aggregate_deductible = ec_lay_path.aggregate_deductible if ec_lay_path.excess_use == False else None
    currency             = hxd.cds.currencies.source_currency

    # assigning limit/xs/deductible
    layer.limit                = limit
    layer.excess               = excess               
    layer.deductible           = deductible           
    layer.aggregate_limit      = aggregate_limit
    layer.aggregate_deductible = aggregate_deductible
    layer.currency             = currency

    # getting frequency factor - we will use this to adjust the displayed el - default is one if missing
    freq_adj             = ratio(   sim_path.total_sim_claim_number_override
                                  , sim_path.total_sim_claim_number_calc
                                  , 1)

    # assign cvg level total premium
    for name, cvg in    ((name, cvg) for name, cvg in layer.coverages if name != "na_total" ):
        # set the path
        exp  = getattr(ec_exp_path, name)

        # get the base values
        el_pre_agg_pre_uwadj = exp.net_el           * (1 + nmp_load)  *  freq_adj   # moved nmp loading here, from typical in skeleton model as NA & EXPERIENCE BOTH HAVE IT ALREADY ADDED
        el_pre_agg_pst_uwadj = exp.net_el_mod       * (1 + nmp_load)  *  freq_adj   # moved nmp loading here, from typical in skeleton model as NA & EXPERIENCE BOTH HAVE IT ALREADY ADDED
        el_pst_agg_pre_uwadj = el_pre_agg_pre_uwadj * (1 + allow_agg_factor)
        el_pst_agg_pst_uwadj = el_pre_agg_pst_uwadj * (1 + allow_agg_factor)
        contribution         = 1 if name == "ec_total" else ratio(exp.net_el_mod, exposure_est_overall)
        experience_el        = experience_est_overall * contribution

        # assign loss cost and adjustments
        cvg.loss_cost_layer_adj         = el_pre_agg_pre_uwadj
        cvg.loss_cost_layer_agg_adj     = el_pst_agg_pre_uwadj
        cvg.loss_cost_layer_agg_uw_adj  = el_pst_agg_pst_uwadj
        cvg.experience_weight           = experience_wgt
        cvg.experience_loss_cost        = experience_el
        cvg.blended_loss_cost_no_uw_adj = (experience_el * experience_wgt) + (el_pst_agg_pre_uwadj * (1 - experience_wgt ))
        cvg.blended_loss_cost           = (experience_el * experience_wgt) + (el_pst_agg_pst_uwadj * (1 - experience_wgt ))
        cvg.agg_adjustment              = ratio(el_pst_agg_pre_uwadj, el_pre_agg_pre_uwadj, 1) - 1
        cvg.uw_adjustment               = ratio(el_pst_agg_pst_uwadj, el_pst_agg_pre_uwadj, 1) - 1

        cvg.expected_loss_cost_pre_uw_adj_100  = cvg.blended_loss_cost_no_uw_adj
        cvg.expected_loss_cost_100             = cvg.blended_loss_cost

        # assigning default values to each coverage
        fld_lst =[  "currency", "limit", "excess", "deductible", "aggregate_limit", "aggregate_excess", "aggregate_deductible"
                    ,"brokerage", "written_line", "premium", "status", "trifocus"]
        for fld in fld_lst:
            if not ( (name == "ec_total") and (fld in [ "limit", "excess", "deductible", "aggregate_limit", "aggregate_excess", "aggregate_deductible"])):
                setattr(cvg, fld, getattr(layer, fld))

        # calculated all the cds premium variations.
        calculate_premiums(hxd, cvg, tp_dict, benchmark_lr, rf, exposure, limit, contribution)                         # assume the policy term at a policy level applies to the coverage in this example

    # calculating the overall layer value
    layer.quoted_premium_100                = layer.coverages.ec_total.quoted_premium_100
    layer.expected_loss_cost_pre_uw_adj_100 = layer.coverages.ec_total.expected_loss_cost_pre_uw_adj_100
    layer.expected_loss_cost_100            = layer.coverages.ec_total.expected_loss_cost_100
    layer.rat_sum_label                     = "Combined"
    calculate_premiums(hxd, layer, tp_dict, benchmark_lr, rf, exposure, limit, 1) 

    # determine the simulation data request status
    summary_value                = ec_exp_path.ec_total.net_el
    sim_path.calc_run_value      = f"EL (orig Fx): { summary_value :,.0f}"
    check_loss_est               = sim_path.last_run_value == sim_path.calc_run_value 
    check_freq_est               = np.isclose(     sim_path.total_sim_claim_number,
                                                   sim_path.total_sim_claim_number_override
                                                or sim_path.total_sim_claim_number_calc,
                                                atol=1e-3)
    check_valid                  = check_loss_est and check_freq_est
    sim_path.check_run_consistent=("Simulation remains valid" if check_valid else "Simulation needs to be rerun - values have changed")


    # forking based on product and calculating premiums & metrics by coverage
    # arguably we are only doing 1 layer now, but leaving in the iteration as it doesnt hurt and available if needed in future
    if hxd.cds.risk_info.product_bool and hxd.cds.standard_fields.is_rater_priced:
        layers_df = rater['layers_df']
        exposure  = cds.exposure.granular.non_appearance.agg_show_value
        for layer, row in zip(hxd.cds.layers, layers_df.itertuples(index=False)):

            # assign path
            cvg   = layer.coverages.na_total

            # assigning limit/xs/deductible
            layer.limit         = limit
            layer.excess        = excess
            layer.deductible    = deductible

            # assign values to BESPOKE expected loss fields within the OVERALL layer
            layer.fgu_pct       = row.fgu_pct
            layer.description   = row.description
            layer.el_fgu_mod    = row.el_fgu_mod
            layer.el_fgu_mod_adj= row.el_fgu_mod_adj

            # assign values to BESPOKE expected loss fields within the NA COVERAGE for the layer
            cvg.fgu_pct         = row.fgu_pct
            cvg.description     = row.description
            cvg.el_fgu_mod      = row.el_fgu_mod
            cvg.el_fgu_mod_adj  = row.el_fgu_mod_adj

            # assign loss cost and adjustments to cvg
            cvg.loss_cost_layer_adj         = cvg.el_fgu_mod
            cvg.loss_cost_layer_agg_adj     = cvg.el_fgu_mod
            cvg.loss_cost_layer_agg_uw_adj  = cvg.el_fgu_mod_adj
            cvg.experience_weight           = 0
            cvg.experience_loss_cost        = 0
            cvg.blended_loss_cost_no_uw_adj = cvg.el_fgu_mod
            cvg.blended_loss_cost           = cvg.el_fgu_mod_adj
            cvg.agg_adjustment              = 0
            cvg.uw_adjustment               = ratio(cvg.el_fgu_mod_adj, cvg.el_fgu_mod, 1)  -1

            # assign loss cost and adjustments to cvg
            layer.loss_cost_layer_adj         = (layer.coverages.ec_total.loss_cost_layer_adj        or 0)  + (layer.coverages.na_total.loss_cost_layer_adj         or 0)
            layer.loss_cost_layer_agg_adj     = (layer.coverages.ec_total.loss_cost_layer_agg_adj    or 0)  + (layer.coverages.na_total.loss_cost_layer_agg_adj     or 0)
            layer.loss_cost_layer_agg_uw_adj  = (layer.coverages.ec_total.loss_cost_layer_agg_uw_adj or 0)  + (layer.coverages.na_total.loss_cost_layer_agg_uw_adj  or 0)
            # layer.experience_weight           = 
            # layer.experience_loss_cost        = 
            layer.blended_loss_cost_no_uw_adj = (layer.coverages.ec_total.blended_loss_cost_no_uw_adj or 0) + (layer.coverages.na_total.blended_loss_cost_no_uw_adj or 0)
            layer.blended_loss_cost           = (layer.coverages.ec_total.blended_loss_cost           or 0) + (layer.coverages.na_total.blended_loss_cost           or 0)
            layer.agg_adjustment              = ratio(layer.loss_cost_layer_agg_adj,    layer.loss_cost_layer_adj,     1) - 1
            layer.uw_adjustment               = ratio(layer.loss_cost_layer_agg_uw_adj, layer.loss_cost_layer_agg_adj, 1) - 1


            # assign to STANDARD expected loss fields
            cvg.expected_loss_cost_pre_uw_adj_100 = row.el_fgu_mod
            cvg.expected_loss_cost_100            = row.el_fgu_mod_adj

            # assigning default values to each coverage NOT (fld in [ "limit", "excess", "deductible", "aggregate_limit", "aggregate_excess", "aggregate_deductible"])
            fld_lst =[  "currency", "limit", "excess", "deductible", "aggregate_limit", "aggregate_excess", "aggregate_deductible"
                    ,"brokerage", "written_line", "premium", "status", "trifocus"]
            for fld in fld_lst:
                setattr(cvg, fld, getattr(layer, fld))


            # assign premium to coverage
            limit = layer.limit 
            calculate_premiums(hxd, cvg, tp_dict, benchmark_lr, rf, exposure, limit, 1)                         # assume the policy term at a policy level applies to the coverage in this example

            # calculating the overall layer value
            layer.quoted_premium_100                =(  (layer.coverages.ec_total.quoted_premium_100                or 0)  
                                                       +(layer.coverages.na_total.quoted_premium_100                or 0))
            layer.expected_loss_cost_pre_uw_adj_100 =(  (layer.coverages.ec_total.expected_loss_cost_pre_uw_adj_100 or 0)  
                                                       +(layer.coverages.na_total.expected_loss_cost_pre_uw_adj_100 or 0))
            layer.expected_loss_cost_100            =(  (layer.coverages.ec_total.expected_loss_cost_100            or 0)  
                                                       +(layer.coverages.na_total.expected_loss_cost_100            or 0))
            calculate_premiums(hxd, layer, tp_dict, benchmark_lr, rf, exposure, limit, 2)
            

