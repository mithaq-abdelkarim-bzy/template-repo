import hx
from datetime import datetime
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api


def fetch_bbt(hxd):
    follow_main_syndicate_bool = hxd.cds.risk_information.follow_main_syndicate
    bbt_option_id = hxd.cds.risk_information.bbt_option_id
    # bbt_option_id = 790955

    if not follow_main_syndicate_bool:
        return

    if not bbt_option_id:
        hx.errors.fatal("BBt option ID cannot be empty.")
    else:
        # Initialise the hx_renew_api library
        hx_renew = init_hx_renew_api()

        # Get expiring policy data
        bbt_response = hx_renew.snapshots.get_snapshot(
            policy_option_id=bbt_option_id, stream=False)

        if bbt_response.status_code != 200:
            raise Exception(bbt_response.json())

        bbt_data = bbt_response.json()["data"]["cds"]

        # extract values from json
        incept                          = bbt_data['standard_fields']['inception_date']
        expiry                          = bbt_data['standard_fields']['expiry_date']
        insured_name                    = bbt_data['standard_fields']['insured_name']
        broker_contact                  = bbt_data['broker_contact']
        is_renewal                      = bbt_data['standard_fields']['is_renewal']
        currency                        = bbt_data['currencies']['source_currency']

        total_deductions                = bbt_data['layers'][0]['total_deductions']
        benchmark_class                 = bbt_data['standard_fields']['benchmark_class']
        gnulr_no_pc_no_uwadj            = bbt_data['rating_summary']['summary_ratios']['total']['gn_pre_uw_adj']['ulr_priced_final_exc_pc']
        gnulr_with_pc_no_uwadj          = bbt_data['rating_summary']['summary_ratios']['total']['gn_pre_uw_adj']['ulr_priced_final_inc_pc']
        gnulr_with_pc_with_uwadj        = bbt_data['rating_summary']['summary_ratios']['total']['gn_pst_uw_adj']['ulr_priced_final_inc_pc']
        cat_gn_ulr_final_no_uwadj       = bbt_data['rating_summary']['summary_ratios']['catastrophe']['gn_pre_uw_adj']['ulr_final']


        # set model state
        hxd.cds.risk_information.is_profit_comission        = True
        hxd.cds.uncertainty.charge_required                 = False             # req PB 5-Feb
        hxd.cds.anti_selection.charge_required              = False             # req PB 5-Feb
       
        # write standard fields to hxd
        hxd.hx_core.inception_date                          = incept
        hxd.hx_core.expiry_date                             = expiry
        hxd.cds.standard_fields.insured_name                = insured_name
        hxd.cds.standard_fields.is_renewal                  = is_renewal
        hxd.cds.currencies.source_currency                  = currency
        hxd.cds.risk_information.broker_contact             = broker_contact
        hxd.cds.risk_information.facility_type              = "Single product facility " # notice input table has some trailing spaces on some of these descriptions

        # write pricing outputs to hxd
        pricing_outputs_path                                = hxd.cds.rating_summary.pricing_outputs
        pricing_outputs_path.bbt_gn_ulr.calculated          = gnulr_no_pc_no_uwadj
        pricing_outputs_path.bbt_gn_cat_ulr.calculated      = cat_gn_ulr_final_no_uwadj
        pricing_outputs_path.deductions_623_2623.calculated = total_deductions
        pricing_outputs_path.deductions_5623                = total_deductions  # req PB 5-Feb
        pricing_outputs_path.bbt_class.calculated           = benchmark_class

        # write uw adjustment to hxd
        paf_path            = hxd.cds.rating_summary.pricing_adequacy_metrics.pricing_adequacy_final_pricing.summary
        paf_path.uw_adj_bbt = gnulr_with_pc_with_uwadj - gnulr_with_pc_no_uwadj

        # write pc to hxd
        # FYI for bbt the algo accesses these in rating summary function get_pc_impact when it looks at rater['pc_details']   
        hxd.cds.pc.profit_commission.details                        = [{}] # need to setup the list first
        hxd.cds.pc.profit_commission.details[0].selected_lob        = 'lob'
        hxd.cds.pc.profit_commission.details[0].total_gn_ulr_pre    = gnulr_no_pc_no_uwadj
        hxd.cds.pc.profit_commission.details[0].total_gn_ulr_post   = gnulr_with_pc_no_uwadj
        hxd.cds.pc.profit_commission.details[0].pc_impact           = gnulr_with_pc_no_uwadj - gnulr_no_pc_no_uwadj

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        hxd.cds.risk_information.bbt_last_fetch_time = f"BBT data last fetched at: {current_time}"
        return