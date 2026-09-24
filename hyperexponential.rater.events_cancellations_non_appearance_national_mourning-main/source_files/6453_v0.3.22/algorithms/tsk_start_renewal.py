# v0.5.0
import hx
import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api

def tsk_start_renewal(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    ms      = hxd.model_state
    sf      = hxd.cds.standard_fields
    layer   = hxd.cds.layers[0]
    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
        return

    ms.pressed_start_renewal_task = True
    ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id
    sf.is_renewal = True

    # Add tasks which must be done before starting a policy here >>
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id # Assigning this node in this tasks allows to clear the override at the creation of a renewal

    # Call to API (do not update)
    v2_api                    = init_hx_renew_api()
    response                  = v2_api.snapshots.get_snapshot(hx.meta.expiring_policy_option_id)

    # Error handling based on status code returned by API (do not update)
    if response.ok:
        # results stored in dict : {data:{variable_name: value}}
        result  = response.json()

        # experience rating
        er_path     = hxd.cds.experience_rating.analysis_table
        er_data     = result["data"]["cds"]["experience_rating"]
        er_df       = pd.DataFrame.from_dict(er_data["analysis_table"])
        er_df       = er_df.iloc[1:, :].reset_index(drop=True)
        max_rows    = min(len(er_df), len(er_path) - 1)
        input_cols  =  [ 'include',               'tiv_ovd',        
                         'gnwp_nominal_ovd',      'rate_inc_ovd',            'inf_inc_ovd',    
                         'attr_incurred_ovd',     'large_incurred_ovd',      'cat_incurred_ovd',
                         'attr_pct_ultimate_ovd', 'large_pct_ultimate_ovd',  'cat_pct_ultimate_ovd',
                         'attr_ielr_ovd',         'large_ielr_ovd',          'cat_ielr_ovd'              ]
 
        for index, i in enumerate(er_path):
            if index >= max_rows:  
                break
            for col in input_cols:
                val = er_df[col].iat[index]
                if not pd.isnull(val):
                    setattr(i, col, val)
        
        # dates 
        inception_date = datetime.strptime(    result["data"]["hx_core"]["inception_date"],    "%Y-%m-%d")
        expiry_date    = datetime.strptime(    result["data"]["hx_core"]["expiry_date"],       "%Y-%m-%d")
        hxd.hx_core.inception_date = inception_date + relativedelta(years=1)
        hxd.hx_core.expiry_date    = expiry_date    + relativedelta(years=1)
        
        # layer
        layer.status               = "Rating"
        ms.use_nm_app_old_model    = False
        ms.use_determ_agg_calc     = False

        # section reference
        for cvg in ["ec_total"]: # , "na_total"]: # requested by YZ/AC 19 Aug convert to override
            ref  = result["data"]["cds"]["layers"][0]["coverages"][cvg]['section_reference']
            path = getattr(layer.coverages, cvg)
            if ref is not None:
                try:
                    ref_yr                  = f"{int(ref[6:8]) + 1:02d}"   # preserves 2 digits
                    path.section_reference = ref[:6] + ref_yr + ref[8:14]
                except:
                    path.section_reference = ref