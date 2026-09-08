import hx_data_schema as hx
import data_schema.sch_utilities as utils
import data_schema.sch_tooltips as tips
from algorithms.rate_constants import max_layers

'''
NOTE: The 'override_node_properties' method is not cumulative. If two overrides are added in seperate places 
to the same node in the script, the one added last will override all the others. 
'''

def sch_overrides(cds):

    ######################################################################################################
    ### Override on hx core fields                                                                     ###
    ######################################################################################################
    cds.override_node_properties('hx_core/expiry_date'               , {  'async_input'     : ['rarc_task']
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})
    cds.override_node_properties('hx_core/inception_date'            , {  'async_input'     : ['rarc_task']
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})


    ######################################################################################################
    ### Override on standard fields                                                                    ###
    ######################################################################################################
    cds.override_node_properties('cds/standard_fields/underwriter'   , {  'options_table'   : 'table_input_underwriters'
                                                                        , 'options_column'  : 'underwriter'
                                                                        , 'allow_custom_value': True
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})

    cds.override_node_properties('cds/standard_fields/insured_name'  , {  'options_table'   : 'lst_insured_names'
                                                                        , 'options_column'  : 'insured_name'
                                                                        , 'allow_custom_value': True
                                                                        , 'async_input'     : ['start_renewal_task']
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})

    cds.override_node_properties('cds/currencies/source_currency'    , {  'default'         : 'USD'
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})

    cds.override_node_properties('cds/standard_fields/broker'        , {  'allow_custom_value': True
                                                                        , 'options_table'   : 'lst_brokers'
                                                                        , 'options_column'  : 'Broker Name'
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})


    cds.override_node_properties('cds/standard_fields/is_renewal'    , {  'async_output'    : [ {'task': 'task_sql_bi_data',  'reset': False}
                                                                                               ,{'task': 'start_renewal_task','reset':False}]})
    
    cds.override_node_properties('cds/standard_fields/insured_country',{  'mode'            : 'output'
                                                                        , 'allow_custom_value': True,})

    cds.override_node_properties('cds/standard_fields/policy_reference',{ 'mode'            : 'output'})
    cds.override_node_properties('cds/standard_fields/benchmark_class',{  'mode'            : 'output'})
    cds.override_node_properties('cds/standard_fields/trifocus'      , {  'mode'            : 'output'})



    ######################################################################################################
    ### Override on standard layers fields                                                             ###
    ######################################################################################################
    cds.override_node_properties('cds/layers/quoted_premium'         , {  'mode'            : 'output'
                                                                        , 'async_input'     : ['rarc_task']})

    cds.override_node_properties('cds/layers/section_reference'      , {  'view'            : { 'label': 'Policy Section Reference'
                                                                                               ,'options': {'read_only': {'read_only': True}}}
                                                                        , 'async_input'     : ['task_sql_bi_data']})

    cds.override_node_properties('cds/layers/brokerage'              , {  'default'         : 0
                                                                        , 'optionality'     : 'required'
                                                                        , 'view'            : {"options": {   "read_only"   : {   "read_only"   : True
                                                                                                                                , "label"       : "Brokerage (excl. PC's)"}}}
                                                                        , 'async_input'     : ['rarc_task']
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})

    cds.override_node_properties('cds/layers/written_line'           , {  'view'            : {'options' : {'read_only': {'read_only': True}}
                                                                                                , "info" : tips.tip_ri03}
                                                                        , 'async_output'    : [{'task': 'task_sql_bi_data', 'reset': False}]})


    cds.override_node_properties('cds/layers'                        , {'max_element_count' : max_layers})
    cds.override_node_properties('cds/layers/status'                 , {'view'              : {'options'  : {'read_only': {'read_only': True}}}
                                                                        , 'async_output'    : ['start_renewal_task']})

    cds.override_node_properties('cds/layers/bpi_case_priced'        , {'default'           : 0
                                                                        , 'optionality'     : 'required'})
    cds.override_node_properties('cds/layers/limit'                  , {'view'              : {'label'   : 'Policy Limit'
                                                                                                , "info" : tips.tip_ri02}
                                                                        , 'async_input'     : [ 'rarc_task'
                                                                                                ,'task_sim_political']})
    cds.override_node_properties('cds/layers/excess'                 , {'view'              : {'label'   : 'Policy Excess'
                                                                                                , "info" : tips.tip_ri01}
                                                                        , 'async_input'     : [ 'rarc_task'
                                                                                                ,'task_sim_political']})
    cds.override_node_properties('cds/layers/deductible'             , {'async_input'       : ['rarc_task']})    
    cds.override_node_properties('cds/layers/benchmark_premium'      , {'async_input'       : ['rarc_task']})

    cds.override_node_properties('cds/layers/rate_change/other_change',{'view'              : {'label'   : "Other Change (incl. Brokerage)"}})

    cds.override_node_properties('cds/layers/currency'               , {'mode'              : 'output'})
    cds.override_node_properties('cds/layers/trifocus'               , {'mode'              : 'output'})
    cds.override_node_properties('cds/layers/aggregate_limit'        , {'mode'              : 'output'})
    cds.override_node_properties('cds/layers/aggregate_excess'       , {'mode'              : 'output'})


    ######################################################################################################
    ### Override on bespoke fields                                                                     ###
    ######################################################################################################

    cds.override_node_properties('cds/product',                                     {'async_input'    : ['rarc_task'],})

    cds.override_node_properties('cds/ihs/calc_run_value',                          {'async_input'    : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/last_run_status',                         {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/last_run_date',                           {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/last_run_value',                          {'async_output'   : ['task_api_ihs_data'],})

    cds.override_node_properties('cds/ihs/ihs_detail',                              {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_detail/country',                      {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_detail/risk_name',                    {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_detail/historic_updated_date',        {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_detail/historic_updated_value',       {'async_output'   : ['task_api_ihs_data'],})

    cds.override_node_properties('cds/ihs/ihs_outlook',                             {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/country',                     {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/risk_name',                   {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/outlook',                     {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/outlook_description',         {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/last_updated_date',           {'async_output'   : ['task_api_ihs_data'],})
    cds.override_node_properties('cds/ihs/ihs_outlook/last_updated_value',          {'async_output'   : ['task_api_ihs_data'],})

    cds.override_node_properties('cds/bi/last_run_status',                          {'async_output'   : ['task_sql_bi_data'],})
    cds.override_node_properties('cds/bi/last_run_date',                            {'async_output'   : ['task_sql_bi_data'],})
    cds.override_node_properties('cds/bi/last_run_value',                           {'async_output'   : ['task_sql_bi_data'],})
    cds.override_node_properties('cds/risk_info/crcf_industry',                     {'async_output'   : [{'task': 'task_sql_bi_data', 'reset': False}],})
    cds.override_node_properties('cds/risk_info/crcf_country',                      {'async_output'   : [{'task': 'task_sql_bi_data', 'reset': False}]
                                                                                    ,'async_input'    : ['rarc_task']})

    cds.override_node_properties('cds/exposure/granular/political/country_exposure',                    {'async_input'   : [ 'task_sim_political'
                                                                                                                            ,'rarc_task']})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/sum_insured',        {'async_input'   : ['task_sim_political'
                                                                                                                            ,'rarc_task']})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/excess',             {'async_input'   : ['task_sim_political'
                                                                                                                            ,'rarc_task']})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/limit',              {'async_input'   : ['task_sim_political'
                                                                                                                            ,'rarc_task']})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/country',            {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/check',              {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/loss_roe_gai',       {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/loss_roe_crg',       {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/loss_roe_pv',        {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/deductible_pv',      {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/sublimit_pv',        {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/loss_roe_ci',        {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/country_exposure/sublimit_ci',        {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/ec_param_b',                          {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/ec_param_g',                          {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/num_sims',                 {'async_input'   : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/total_sim_loss_capped',    {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/total_sim_loss_uncapped',  {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_status',          {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_date',            {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_value',           {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/calc_run_value',           {'async_output'  : ['task_sim_political'],})

    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_status',          {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_date',            {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/last_run_value',           {'async_output'  : ['task_sim_political'],})
    cds.override_node_properties('cds/exposure/granular/political/simulation/calc_run_value',           {'async_input'   : ['task_sim_political'],})


    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/mobile_assets/gov_action',            {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/mobile_assets/pol_violence',          {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/mobile_assets/cur_inconvertibility',  {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/mobile_assets/cont_relation_govt',    {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/fixed_assets/gov_action',             {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/fixed_assets/pol_violence',           {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/fixed_assets/cur_inconvertibility',   {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/fixed_assets/cont_relation_govt',     {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/lenders_interest/gov_action',         {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/lenders_interest/pol_violence',       {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/lenders_interest/cur_inconvertibility',{'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/lenders_interest/cont_relation_govt', {'async_input'  : ['rarc_task'],})           
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/sublimit/pol_violence',               {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/sublimit/cur_inconvertibility',       {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/exposure/granular/political/coverage_matrix/deductible/pol_violence',             {'async_input'  : ['rarc_task'],})

    cds.override_node_properties('cds/modifiers/political/override/industry',                                           {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/modifiers/political/override/insured_quality',                                    {'async_input'  : ['rarc_task'],})
    cds.override_node_properties('cds/modifiers/political/override/asset_composition',                                  {'async_input'  : ['rarc_task'],})

    cds.override_node_properties('cds/exposure/granular/political/exposure_curve',                                      {'async_input'  : ['rarc_task'],})

    cds.override_node_properties('cds/rating_factors/policy_term',                                                      {'async_input'  : ['rarc_task'],})



    cds.override_node_properties('cds/risk_info/crcf_term',                                             {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_basis',                           {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_step_opening_si',                 {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_step_instal_amt',                 {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_step_instal_freq',                {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_step_grace_period',               {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_step_term',                       {'async_input'   : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/load_amt_flat',                            {'async_input'   : ['task_fill_exposure_profile'],})

    cds.override_node_properties('cds/exposure/granular/crcf/last_run_date',                            {'async_output'  : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/last_run_status',                          {'async_output'  : ['task_fill_exposure_profile'],})
    cds.override_node_properties('cds/exposure/granular/crcf/last_run_value',                           {'async_output'  : ['task_fill_exposure_profile'],})

    cds.override_node_properties('cds/exposure/granular/crcf/pre_shipment_risk',                        {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/pre_shipment_amt',                         {'async_input'   : ['rarc_task']})

    cds.override_node_properties('cds/modifiers/crcf/rating_source',                                    {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/modifiers/crcf/rating_corporate',                                 {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/modifiers/crcf/override/grade',                                   {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/modifiers/crcf/override/lgd',                                     {'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/modifiers/crcf/override/uw_adj',                                  {'async_input'   : ['rarc_task']})



    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_1',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_2',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_3',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_4',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_5',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_6',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_7',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_8',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_9',                 {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_10',                {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_11',                {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})
    cds.override_node_properties('cds/exposure/granular/crcf/exposure_profile/month_12',                {'async_output'  : ['task_fill_exposure_profile']
                                                                                                        ,'async_input'   : ['rarc_task']})



    



    