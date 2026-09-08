import hx
import algorithms.rate_utilities as utils
from libraries.common_data_schema.algorithms.sync_hx_core              import sync_hx_core

# These are for both BBT and Exposure rating
from algorithms.rate_risk_information                                  import rate_risk_information
from algorithms.rate_exp_det                                           import rate_exp_det
from algorithms.rate_rating_summary                                    import rate_rating_summary
from algorithms.model_state                                            import model_state


# These are from the BBT
from algorithms.aysnc_tasks.triangles.rate_triangle_projection         import rate_triangle_projection
from algorithms.rate_show_hide                                         import rate_show_hide  # added parts of Exposure rating here
from algorithms.aysnc_tasks.profit_commission.rate_profit_commission   import rate_profit_commission
from algorithms.aysnc_tasks.em_bi_sql.rate_rms                         import rate_rms
from algorithms.rate_graph_string_creation                             import adjust_graph_strings
   
# These are from the Exposure rating section
from algorithms.rate_bordereau                                         import read_bordereau_table
from algorithms.perils.rate_wildfire                                   import wf_rating_calcs
from algorithms.perils.fire.rate_fire                                  import fire_rating_calcs
from algorithms.perils.rate_flood                                      import fl_rating_calcs
from algorithms.perils.scs.rate_scs                                    import scs_rating_calcs
from algorithms.rate_expected_loss                                     import el_calcs
from algorithms.rate_premium                                           import premium_calcs
from algorithms.rate_data_assignment                                   import data_assignment
from algorithms.rate_claim_summary                                     import rate_claim_summary
from algorithms.rate_summary_exhibits                                  import report_summary, region_summary
from algorithms.rate_validation_criteria                               import rate_validation_criteria

from algorithms.rate_rationale                                         import rate_rationale







@hx.rating
def rating_algorithm(hxd):
    rate_risk_information(hxd)
    rate_exp_det(hxd)
    rate_rms(hxd)
    rate_triangle_projection(hxd)
    rate_rating_summary(hxd)
    rate_claim_summary(hxd)     #after rating summary - uses some of its values
    rate_profit_commission(hxd)     #after rating summary - uses some of its values
    
    model_state(hxd)
    rate_show_hide(hxd)
    rate_validation_criteria(hxd)
    sync_hx_core(hxd)
    adjust_graph_strings(hxd)
 
    rate_rationale(hxd)
    pass


def run_bordereau_rater(hxd, progress):
    '''
    Function that runs most of the rater function (apart from frontend mapping and text populate)
    '''
    # # other_data is a dict that carries the information that are not stored in dataframe format in variable df
    # other_data = {}


    #these are used for the async task check

    hxd.cds.sch_check_async.exposure_premium = hxd.cds.layers[0].quoted_premium_100pct
    hxd.cds.sch_check_async.exposure_deductions = hxd.cds.layers[0].total_deductions
    
    if hxd.cds.layers[0].status == "Bound" and hxd.cds.layers[0].signed_line != 0:
        hxd.cds.sch_check_async.exposure_signed_line = hxd.cds.layers[0].signed_line
    else:
        hxd.cds.sch_check_async.exposure_signed_line = hxd.cds.layers[0].written_line
    
    # all these are part of the run bordereau_rater_task
    df = read_bordereau_table(hxd)
    df = fire_rating_calcs(hxd, df)
    df = fl_rating_calcs(hxd, df)
    df = scs_rating_calcs(hxd, df)
    df = wf_rating_calcs(hxd, df)
    df = el_calcs(hxd, df)
    df = premium_calcs(hxd, df)

    report_summary(hxd, df)    
    region_summary(hxd, df)
    data_assignment(hxd, df)



    return df




#########################
# import pandas
# df_pd = df.to_pandas()
# with pandas.ExcelWriter(hxd.cds.output_file.open("b"), engine='xlsxwriter') as f:
#     df_pd.to_excel(f, sheet_name="Power of Renew")

####################

   
