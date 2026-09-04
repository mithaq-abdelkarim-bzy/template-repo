##############################################################################################################################
################                             NOTES                                                            ################ 
##############################################################################################################################

### 

##############################################################################################################################
################                             OUTSTANDING ITEMS                                                ################ 
##############################################################################################################################

### 1) Comment out policy # on row 44
### 2) 
### 3) 
### 4) 
### 5) 

##############################################################################################################################

# import hx, os, openpyxl, json, requests
import hx, os, json
import pandas as pd
pd.set_option('display.max_rows', None)

# from algorithms.rate_utilities                           import look_up, rgetattr, pd_df_from_hx_list, write_pd_to_hxd, date_to_string
from algorithms.rate_utilities                           import sanitize_and_sort_expiring_list_by_renewal, split_renewal_list_by_expiring
# from algorithms.rate_utilities                           import get_countries_retrieved, one_layer, rgetkey, rsetattr, rgetattr

# from datetime                                            import datetime, date
from copy                                                import deepcopy
# from algorithms.data_schema.sch_rater_defined            import perils, ihs_risk_names

from libraries.rate_change.algorithms.rate_change        import RateChange as RateChangeLib
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_rate_change                         import rate_change_buckets



### --- RATE CHANGE --- ###
def get_expiring_data(hxd):
    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected or 980960 # NOTE: id used for testing
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False).json()
    expiring_data = expiring_response["data"]

    return expiring_data


def clean_expiring_data(hxd, split=False, remove_duplicates=False):
    """
    Sorts the expiring countries in the same order as the renewing countries.
    Renewal may have additional countries which are not present in expiring; they will be added at the end of the list.
    If 'split' is set to True, returns two expiring_data dictionaries:
        - expiring_data_common: contains the sorted list of countries that are common between expiring and renewal;
        - expiring_data_others: contains the list of additional countries that are present in renewal but not in expiring.
    """

    expo = hxd.cds.exposure.granular

    # Get expiring data and remove bloating from IHS data
    expiring_data = get_expiring_data(hxd)
    expiring_data.pop("ihs", None)
    expiring_list = expiring_data["cds"]["exposure"]["granular"]["countries"]

    # patch added to force the expiring lookup to always be present which it wasnt on the inputs only rater 30-apr-2026
    for row in expiring_list:
        row["country_cvg_subcvg"] = (
            str(row.get("rated_country"))
            + "&" + str(row.get("coverage"))
            + "&" + str(row.get("subcoverage"))
        )
    
    # Get renewal list
    renewal_list = json.loads(hxd.rate_change.countries)

    # Sort expiring list to follow renewal order
    sorting_key = "country_cvg_subcvg"
    sorted_expiring_list, warnings = sanitize_and_sort_expiring_list_by_renewal(
        expiring_list,
        renewal_list, 
        sorting_key=sorting_key,
        remove_duplicates=remove_duplicates
    )

    expiring_data_sorted = deepcopy(expiring_data)
    expiring_data_sorted["cds"]["exposure"]["granular"]["countries"] = sorted_expiring_list

    if split:
        expiring_list_common, renewal_list_others, expiring_list_dropped = split_renewal_list_by_expiring(sorted_expiring_list, renewal_list, sorting_key=sorting_key)
        expiring_data_common = deepcopy(expiring_data)
        expiring_data_others = deepcopy(expiring_data) # Calling this expiring_data even though the specified list will contain renewal elements
        expiring_data_dropped = deepcopy(expiring_data)

        expiring_data_common["cds"]["exposure"]["granular"]["countries"] = expiring_list_common
        expiring_data_others["cds"]["exposure"]["granular"]["countries"] = renewal_list_others
        expiring_data_dropped["cds"]["exposure"]["granular"]["countries"] = expiring_list_dropped

        return expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped, warnings

    return expiring_data_sorted, warnings





# Import expiring policy for rate change
def tsk_expiring_policy_fetch(hxd, progress):

    if not hxd.cds.rate_change.expiring_policy_option_id.selected:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    expiring_data = get_expiring_data(hxd)


### JB CHECK ENRICO CODE
    # Get fields from json response and push to hxd
    # for idx, layer in enumerate(hxd.cds.layers):

    #     # Overall
    #     layer.rate_change.expiring_policy_info.expiring_premium             = expiring_data["cds"]["layers"][idx]["quoted_premium"]
    #     layer.rate_change.expiring_policy_info.expiring_premium_annualised  = expiring_data["cds"]["layers"][idx]["quoted_premium_annualised"]
    #     layer.rate_change.expiring_policy_info.expiring_written_line        = expiring_data["cds"]["layers"][idx]["written_line"]




### JB CHECK STANDARD CODE ############################
    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        mapped_expiring_layer_idx   = layer.rate_change.expiring_layer - 1
        expiring_written_line       = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"] or 1
        expiring_brokerage          = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["brokerage"] or 0
        expiring_premium_annual_bzly= expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium_annualised"] or 0
        expiring_premium_term_bzly  = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium"] or 0

        layer.rate_change.expiring_policy_info.expiring_written_line    = expiring_written_line
        layer.rate_change.expiring_policy_info.expiring_brokerage       = expiring_brokerage
        layer.rate_change.premium.line_100pct.annualised.expiring       = expiring_premium_annual_bzly / expiring_written_line
        layer.rate_change.premium.beazley_line.annualised.expiring      = expiring_premium_annual_bzly
        layer.rate_change.premium.line_100pct.policy_term.expiring      = expiring_premium_term_bzly   / expiring_written_line
        layer.rate_change.premium.beazley_line.policy_term.expiring     = expiring_premium_term_bzly

        # NOTE add other expiring fields as required here

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False
####################################################



def tsk_rarc(hxd, progress):
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected

    if not expiring_policy_option_id:
       hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Get correct buckets based on coverage
    buckets = rate_change_buckets()

    data_schema_static_filename = "data_schema/data_schema_static_copy.py"
    data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

    # Get expiring data split between common and other aircrafts
    expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped, warnings = clean_expiring_data(
        hxd, split=True, remove_duplicates=True
    )

    # Prepare arguments for calculate_repriced_values() function
    kw_args = {
        "custom_expiring_data": [expiring_data_sorted, expiring_data_common, expiring_data_others, expiring_data_dropped],
        "split_list_path": "cds/exposure/granular/countries",
        "matching_key": "country_cvg_subcvg",
        "additional_items_bucket": "exposure"
    }
    
    # Rate Change with offline_hxd
    rc = RateChangeLib(
        hxd=hxd,
        progress=progress,
        buckets=buckets,
        layers_path="cds/layers",
        expiring_actual_prem="quoted_premium_annualised",
        expiring_technical_prem="benchmark_premium_annualised",
        async_tasks=[],
        data_schema_static_path=data_schema_static_path
    )

    rc_hxds = rc.calculate_repriced_values(**kw_args)

    # Use the repriced values to calculate the changes for each bucket
    rarc_df, rarc_list = rc.calculate_rarc_by_layer()
    
    # Calculate brokerage change for storage but not display
    for layer in hxd.cds.layers:
        expiring_brokerage = layer.rate_change.expiring_policy_info.expiring_brokerage or 0
        renewal_brokerage = layer.brokerage or 0
        layer.rate_change.brokerage_change.model_calculated         = (1 - expiring_brokerage) / (1 - renewal_brokerage)
        layer.rate_change.brokerage_change.uw_selected.calculated   = (1 - expiring_brokerage) / (1 - renewal_brokerage) # CUSTOM

    # Push to hxd
    for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
        hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
        rarc_layer.pop("temp_storage")

        if hxd_layer.rate_change.expiring_layer:
            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

    # so we can clear out the overrides on renewal we need the uw_selected values to be set within the async task - instead of row 97 of rate change algo - it could be implemented more elegantly but it works!
    for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
        rc_vbl                          = getattr(hxd_layer.rate_change, item)
        rc_vbl.uw_selected.calculated   = rc_vbl.model_calculated

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False