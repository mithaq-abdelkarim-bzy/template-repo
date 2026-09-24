import hx
import pandas as pd
from datetime import datetime
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
import algorithms.rate_utilities as utils
import algorithms.rate_constants as constants
from algorithms.risk_information.risk_information_helpers import import_inception_date
from dateutil.relativedelta import relativedelta

###########################################################################################
### Helper Functions
###########################################################################################

# helper function to source expiring policy data from hx api (v2)
def get_expiring_policy_data(expiring_option_id):
    # Initialize renewal API client
    hx_renew = init_hx_renew_api()
    # Fetch snapshot of expiring policy data
    response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_option_id, stream=False)
    if response.status_code != 200:
        raise Exception(response.json())  # Raise error if API call fails
    return response.json()["data"]

def dict_get_path(d, keys):
    """Get nested value from dict using / separated path."""
    for k in keys:
        d = d[k]
    return d

def obj_get_path(o, keys):
    """Get nested value from object using / separated attribute path."""
    for k in keys:
        o = getattr(o, k)
    return o

# helper function so only have to enter path once and assigns to hxd testing if value in accepted range
def walk_path_and_assign(hxd, expiring_dict, str_path, allowed_values=None):
    # walk the dictionary and hxd
    keys = str_path.split('/')
    val  = dict_get_path(expiring_dict, keys     )
    obj  = obj_get_path( hxd,           keys[:-1])
    # gate: only assign if val is allowed (when provided)
    if allowed_values is not None and val not in allowed_values:
        return False  # not written
    # set the value
    setattr(obj, keys[-1], val)
    return True

# custom function to walk the dictionary and assign all nested value to the object where they exist therein
def assign_dict_to_obj(obj, data_dict):
    """Recursively assign keys in a dict onto matching attributes in obj."""
    for k, v in data_dict.items():
        # check if in dictionary and if not skip to next
        if not hasattr(obj, k):
            continue
        # check if is dictionary, and if so call recursively
        if isinstance(v, dict):
            assign_dict_to_obj(getattr(obj, k), v)
        # if not dictionary then set value
        else: 
            setattr(obj, k, v)
    return 

# syncs an hx list to be a given length
def sync_list(node, lob_list_length):
    current_length = len(node)
    if current_length > lob_list_length:
        target_length = max(lob_list_length, 1)
        while len(node) > target_length:
            del node[len(node) - 1]
    elif current_length < lob_list_length:
        for _ in range(lob_list_length - current_length):
            node.append({})     


###########################################################################################
### Main Code
###########################################################################################

# main function to control flow
def task_renewal_start(hxd):
    # Get the expiring option ID from the CDS risk information
    expiring_option_id  = ( hxd.cds.risk_information.expiring_option_id 
                            or hx.meta.expiring_policy_option_id
                            or 1510357
                            )

    # Pull expiring policy data via API
    expiring_data       = get_expiring_policy_data(expiring_option_id)

    # Update various parts of the HXD with expiring data
    renewal_update_risk_info(   expiring_data, hxd)
    renewal_update_anti_sel(    expiring_data, hxd)
    renewal_update_uncertainty( expiring_data, hxd)
    renewal_update_rate_change( expiring_data, hxd)
    return


# function to update risk info values
def renewal_update_risk_info(rater_data, hxd):
    
    # set lists to check values are within
    facility_lst    = hx.params.table_input_facility_type['facility_type'].values
    underwriter_lst = hx.params.table_input_underwriters['underwriter'].values
    yoa_basis_lst   = ["Calendar Year","Policy Year"]

    # cds risk information - transformations
    hxd.cds.risk_information.deal_status    = "Submission"
    hxd.cds.standard_fields.is_renewal      = True
    hxd.hx_core.inception_date              = pd.to_datetime( rater_data['hx_core']['inception_date']) + relativedelta(years=1)
    hxd.hx_core.expiry_date                 = pd.to_datetime( rater_data['hx_core']['expiry_date']   ) + relativedelta(years=1)
    hxd.cds.standard_fields.policy_reference= (rater_data['cds']['standard_fields']['policy_reference'] or "x")[:6] + str(hxd.hx_core.inception_date.year)[-2:]

    # cds standard field assignments
    walk_path_and_assign(hxd, rater_data, 'cds/standard_fields/underwriter',            underwriter_lst )
    walk_path_and_assign(hxd, rater_data, 'cds/standard_fields/insured_name'                            )
    walk_path_and_assign(hxd, rater_data, 'cds/currencies/source_currency'                              )

    # cds custom field assignment - risk information
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/facility_type',         facility_lst)
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/is_large_model_mode'                )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/follow_main_syndicate'              )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/prem_data_available'                )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/is_profit_comission'                )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/data_yoa_basis',        yoa_basis_lst)
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/det_claims_data_available'          )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/cat_modelling_available'            )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/broker_contact'                     )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/show_refs'                          )
    walk_path_and_assign(hxd, rater_data, 'cds/risk_information/priced_by'                          )

    return


# function to update anti selection values
def renewal_update_anti_sel(rater_data, hxd):
    # set lists to check values are within
    baseline_lst                = hx.params.table_antiselection_1['Grade'].values
    competing_portfolio_lst     = hx.params.table_antiselection_2['Grade'].values
    delegation_scope_lst        = hx.params.table_antiselection_3['Grade'].values
    quantity_quality_lst        = hx.params.table_antiselection_4['Grade'].values
    cover_holder_alignment_lst  = hx.params.table_antiselection_5['Grade'].values
    participation_lst           = hx.params.table_antiselection_6['Grade'].values

    # cds custom field assignment - anti-selection
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/charge_required'                                                  )   
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/baseline/selection',               baseline_lst            )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/baseline/comments'                                         )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/competing_portfolio/selection',    competing_portfolio_lst )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/competing_portfolio/comments'                              )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/delegation_scope/selection',       delegation_scope_lst    )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/delegation_scope/comments'                                 )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/quantity_quality/selection',       quantity_quality_lst    )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/quantity_quality/comments'                                 )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/cover_holder_alignment/selection', cover_holder_alignment_lst)
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/cover_holder_alignment/comments'                           )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/participation/selection',          participation_lst       )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/participation/comments'                                    )
    walk_path_and_assign(hxd, rater_data, 'cds/anti_selection/matrix/overall_selected/comments'                                 )

    return


# function to update uncertainty values
def renewal_update_uncertainty(rater_data, hxd):
    # set lists to check values are within
    quantity_lst                    = hx.params.table_uncertainty_1['Grade'].values
    quality_lst                     = hx.params.table_uncertainty_2['Grade'].values
    new_or_existing_facility_lst    = hx.params.table_uncertainty_3['Grade'].values
    perf_volatility_lst             = hx.params.table_uncertainty_4['Grade'].values
    reliance_on_ext_modelling_lst   = hx.params.table_uncertainty_5['Grade'].values

    # cds custom field assignment - uncertainty
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/charge_required'                                                             )   
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/quantity/selection',                  quantity_lst                    )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/quantity/comments'                                                    )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/quality/selection',                   quality_lst                     )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/quality/comments'                                                     )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/new_or_existing_facility/selection',  new_or_existing_facility_lst    )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/new_or_existing_facility/comments'                                    )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/perf_volatility/selection',           perf_volatility_lst             )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/perf_volatility/comments'                                             )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/reliance_on_ext_modelling/selection', reliance_on_ext_modelling_lst   )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/reliance_on_ext_modelling/comments'                                   )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/perf_discount/comments'                                               )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/add_subjectivity/comments'                                            )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/perf_discount/comments'                                               )
    walk_path_and_assign(hxd, rater_data, 'cds/uncertainty/matrix/overall_selected/comments'                                            )

    return


# function to update rate change values
def renewal_update_rate_change(rater_data, hxd):
    src_path = 'cds/rate_change'                        # assign paths
    dst_path = 'cds/expiring/rate_change'
    src_keys = src_path.split('/')                      # split path into keys
    dst_keys = dst_path.split('/')
    src_list = dict_get_path(rater_data, src_keys)      # navigate through the dictionary to right point
    dst_list = obj_get_path( hxd,        dst_keys)      # navigate through the hxd to right point
    sync_list(dst_list, len(src_list))                  # make hxd list match size of expiring list
    for i in range(len(src_list)):                      # write values to hxd
        assign_dict_to_obj(dst_list[i], src_list[i])    
    return






