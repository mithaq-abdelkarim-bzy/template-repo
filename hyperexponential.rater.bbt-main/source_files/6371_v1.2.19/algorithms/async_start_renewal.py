import hx
import requests
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_utilities as utils
from operator import itemgetter
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api


### requested by Mark Fleet - only used in initial migration - triggered by migration task
def set_migration_flag(hxd,progress):
    cds = hxd.cds
    cds.model_state.migrated_record = True


def start_renewal(hxd,df):
    cds = hxd.cds
    rating_summary = cds.rating_summary
        
    if not cds.standard_fields.underwriter:
        hx.errors.fatal("Please press 'Undo' and 'Import Expiring Policy Data' at the top right corner")
        
    cds.model_state.pressed_start_renewal_task = True

    user = hx.secrets.rest_api_user
    password = hx.secrets.rest_api_password
    expiring_policy_option_id = hx.meta.expiring_policy_option_id
    #expiring_policy_option_id = 154108


    # Call to API (do not update)  
    v2_api = init_hx_renew_api()
    response = v2_api.snapshots.get_snapshot(expiring_policy_option_id)

    # Error handling based on status code returned by API (do not update)
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result  = response.json()
        data    = result["data"]["cds"]["rating_summary"]

    
        
        # UPDATE FROM HERE >>

        # load detail by year df
        detail_by_year_df = pd.DataFrame.from_dict(data["detail_by_year"])

        # shifting things back one year. i.e. drop first row, add new row, then reindex
        detail_by_year_df = detail_by_year_df.iloc[1:, :]
        detail_by_year_df = detail_by_year_df.append(pd.Series(), ignore_index=True)
        detail_by_year_df = detail_by_year_df.reset_index(drop=True)

        # writing list back to hxd, cant use write_pd_to_hxd due to Nulls
        for index, i in enumerate(cds.rating_summary.detail_by_year):
            #loading "priors"
            if pd.isnull(detail_by_year_df['port_chg_selected'].iat[index]) == False:                    i.port_chg_prior            = detail_by_year_df['port_chg_selected'].iat[index]
            if pd.isnull(detail_by_year_df['rate_chg_selected'].iat[index]) == False:                    i.rate_chg_prior            = detail_by_year_df['rate_chg_selected'].iat[index]
            if pd.isnull(detail_by_year_df['infl_chg_selected'].iat[index]) == False:                    i.infl_chg_prior            = detail_by_year_df['infl_chg_selected'].iat[index]
            if pd.isnull(detail_by_year_df['incurred_att_selected'].iat[index]) == False:                i.incurred_att_prior        = detail_by_year_df['incurred_att_selected'].iat[index]
            if pd.isnull(detail_by_year_df['interp_blended_selected_perc_ult'].iat[index]) == False:     i.prior_selected_perc_ult   = detail_by_year_df['interp_blended_selected_perc_ult'].iat[index]

            # 16 elements in list, starting at 0, we dont want the last 1 override (15) loaded
            if index < 15:  
                if pd.isnull(detail_by_year_df['port_chg_override'].iat[index]) == False:                    i.port_chg_override         = detail_by_year_df['port_chg_override'].iat[index]
                if pd.isnull(detail_by_year_df['rate_chg_override'].iat[index]) == False:                    i.rate_chg_override         = detail_by_year_df['rate_chg_override'].iat[index]
                if pd.isnull(detail_by_year_df['infl_chg_override'].iat[index]) == False:                    i.infl_chg_override         = detail_by_year_df['infl_chg_override'].iat[index]

            # 16 elements in list, starting at 0, we dont want the last 2 overrides (14 & 15) loaded - issue with migrated data going into 14th place
            if index < 14:  
                if pd.isnull(detail_by_year_df['include_override'].iat[index]) == False:                     i.include_override          = detail_by_year_df['include_override'].iat[index]
                if pd.isnull(detail_by_year_df['policy_length_override'].iat[index]) == False:               i.policy_length_override    = detail_by_year_df['policy_length_override'].iat[index]
                if pd.isnull(detail_by_year_df['premium_override'].iat[index]) == False:                     i.premium_override          = detail_by_year_df['premium_override'].iat[index]
                if pd.isnull(detail_by_year_df['incurred_override'].iat[index]) == False:                    i.incurred_override         = detail_by_year_df['incurred_override'].iat[index]
                if pd.isnull(detail_by_year_df['incurred_cat_override'].iat[index]) == False:                i.incurred_cat_override     = detail_by_year_df['incurred_cat_override'].iat[index]
                if pd.isnull(detail_by_year_df['incurred_large_override'].iat[index]) == False:              i.incurred_large_override   = detail_by_year_df['incurred_large_override'].iat[index]


        # writing individual values back to hxd
        rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_previous_override   = data["summary_ratios"]["attritional"]["gg_pre_uw_adj"]["ulr_uw_override"]
        rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_previous            = data["summary_ratios"]["attritional"]["gg_pre_uw_adj"]["ulr_final"]
        rating_summary.summary_ratios.attritional.gg_pre_uw_adj.ulr_previous_suggested  = data["summary_ratios"]["attritional"]["gg_pre_uw_adj"]["ulr_selected_ol_exc_scalant"]

        rating_summary.summary_ratios.large.gg_pre_uw_adj.ulr_previous                  = data["summary_ratios"]["large"]["gg_pre_uw_adj"]["ulr_final"]

        rating_summary.summary_ratios.catastrophe.gg_pre_uw_adj.ulr_previous_exc_nml    = data["summary_ratios"]["catastrophe"]["gg_pre_uw_adj"]["ulr_selected_ol_exc_nml"]
        rating_summary.summary_ratios.catastrophe.gg_pre_uw_adj.ulr_previous            = data["summary_ratios"]["catastrophe"]["gg_pre_uw_adj"]["ulr_final"]

        rating_summary.summary_ratios.total.gn_pre_uw_adj.ulr_prior                     = data["summary_ratios"]["total"]["gn_pre_uw_adj"]["ulr_priced_final_inc_pc"]
        rating_summary.summary_ratios.total.gn_pst_uw_adj.ulr_prior                     = data["summary_ratios"]["total"]["gn_pst_uw_adj"]["ulr_priced_final_inc_pc"]

        rating_summary.kpi.pre_uw_adj.bpi_prior                                         = data["kpi"]["pre_uw_adj"]["bpi"]
        rating_summary.kpi.pst_uw_adj.bpi_prior                                         = data["kpi"]["pst_uw_adj"]["bpi"]
        rating_summary.kpi.pre_uw_adj.tpi_prior                                         = data["kpi"]["pre_uw_adj"]["tpi"]
        rating_summary.kpi.pst_uw_adj.tpi_prior                                         = data["kpi"]["pst_uw_adj"]["tpi"]

        cds.standard_fields.is_renewal                                                  = True
        cds.layers[0].status                                                            = "Rating"

        cds.model_state.expiring_policy                                                 = hx.meta.expiring_policy_option_id

        # ~~~~~~~~~~~~~~

        
    # Raises error if status code is not 200 (do not update)
    else:
        try:
            response_json = response.json()
            error = f"Error: {response_json.get('title')}"
            error += f"\nDetail: {response_json.get('detail')}" if response_json.get("detail") else ""
            hx.errors.fatal(error)
        except:
            hx.errors.fatal(f"Error: {response.text}")



