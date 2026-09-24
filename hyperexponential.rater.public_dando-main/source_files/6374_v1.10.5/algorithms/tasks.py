import hx
import os
import pandas as pd
import requests
import json
from algorithms.rate_rate_change import rate_change_buckets
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.rate_change import RateChange as RateChangeLib
from algorithms.async_capiq import capiq_fetch, populate_capiq_data, populate_capiq_data_from_wb, skip_capiq
from algorithms.async_admitted import set_admitted, reset_admitted_reasons
from algorithms.rate_pricing import calc_pro_rata, calc_ipo_rarc
from algorithms.async_rationale import process_comment
from algorithms.rate_rate_change import compute_private_rate_change
from datetime import datetime, date
import random
from libraries.email_notification.algorithms.bug_report import new_bug_report,send_bug_report, cancel_bug_report, generate_bug_report, add_additional_file

# Update example task below
@hx.task
def example_empty_task(hxd, progress):
    pass


# Importing expiring policy for rate change
'''
Async task to import data from an expiring policy option for rate change calculation and analysis of movement.
Developers will need to update the task in two places, first for which variables from the expiring policy to import,
second to assign these to the current model variables.
'''

@hx.task
def expiring_policy_fetch_task(hxd, progress):

    expiring_policy_option_id = (
        hxd.cds.rate_change.expiring_policy_option_id.selected
        or hx.meta.expiring_policy_option_id
    )

    if not expiring_policy_option_id:
        hx.errors.fatal("Expiring policy option ID cannot be empty.")

    # Initialise the hx_renew_api library
    hx_renew = init_hx_renew_api()

    # Get expiring policy data
    expiring_policy_option_id = hxd.cds.rate_change.expiring_policy_option_id.selected #or 85244 # NOTE: use hardcoded ID for debugging if needed
    expiring_response = hx_renew.snapshots.get_snapshot(policy_option_id=expiring_policy_option_id, stream=False)

    if expiring_response.status_code != 200:
        raise Exception(expiring_response.json())

    expiring_data = expiring_response.json()["data"]

    # Get fields from json response and push to hxd
    expiring_layers_len = len(expiring_data["cds"]["layers"])
    layer_mapping = {}

    for idx, layer in enumerate(hxd.cds.layers):
        # Throw error if expiring layer doesn't exist
        if layer.rate_change.expiring_layer > expiring_layers_len:
            hx.errors.fatal(f"Expiring Layer {layer.rate_change.expiring_layer}, mapped to Renewal Layer {idx+1}, does not exist. Number of expiring layers is {expiring_layers_len}.")

        mapped_expiring_layer_idx = layer.rate_change.expiring_layer - 1
        
        expiring_layer = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]

        gross_premium = expiring_layer.get("quoted_premium")

        # Backward compatibility for older expiring snapshots.
        # In the current model, layer.quoted_premium is derived from the active coverage premium.
        # Older snapshots may have the value on the coverage, but not on layer.quoted_premium.
        if gross_premium is None:
            if expiring_data["cds"].get("is_side_a"):
                gross_premium = expiring_layer.get("coverages", {}).get("side_a", {}).get("premium")
            elif expiring_data["cds"].get("is_abc"):
                gross_premium = expiring_layer.get("coverages", {}).get("abc", {}).get("premium")

        if gross_premium is None:
            hx.errors.fatal(
                f"Gross premium is missing for Expiring Layer {layer.rate_change.expiring_layer}. "
                f"Checked layer.quoted_premium and the active coverage premium."
            )

        layer.rate_change.premium_policy_term_100pct.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium"]
        incept = datetime.strptime(expiring_data["hx_core"]["inception_date"], '%Y-%m-%d')
        expiry = datetime.strptime(expiring_data["hx_core"]["expiry_date"], '%Y-%m-%d')
        pro_rata = 1 if (incept is None) or (expiry is None) else calc_pro_rata(incept, expiry, 2)
        pro_rata = pro_rata or 1
        layer.rate_change.premium_annualized_100pct.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["quoted_premium"] / pro_rata

        expiring_written_line = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["written_line"]
        layer.rate_change.premium_annualized_beazley_share.expiring.calculated = layer.rate_change.premium_annualized_100pct.expiring.calculated * (expiring_written_line or 0)
        # NOTE: ... Add expiring fields as required here
        layer.rate_change.limit.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["limit"]
        layer.rate_change.deductible.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["deductible"]
        layer.rate_change.excess.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["excess"]

        layer.rate_change.side_a_excess.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["excess"]
        layer.rate_change.abc_tower.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["coverages"]["side_a"]["tower"]
        layer.rate_change.total_excess.expiring.calculated = (layer.rate_change.side_a_excess.expiring.calculated or 0) + (layer.rate_change.abc_tower.expiring.calculated or 0)

        layer.rate_change.market_cap.expiring.calculated = expiring_data["cds"]["exposure"]["aggregate"]["market_cap"]
        layer.rate_change.insider_share.expiring.calculated = expiring_data["cds"]["exposure"]["aggregate"]["insider_share"]
        layer.rate_change.revised_market_cap.expiring.calculated = expiring_data["cds"]["exposure"]["aggregate"]["revised_market_cap"]

        layer.rate_change.brokerage.expiring.calculated = expiring_data["cds"]["layers"][mapped_expiring_layer_idx]["brokerage"]

        # Save layer mapping
        layer_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    hxd.cds.rate_change.layer_mapping = json.dumps(layer_mapping)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False


@hx.task
def rarc_task(hxd, progress):
    if hxd.cds.review_type.rater_priced == True:

    #if not hxd.cds.rate_change.expiring_policy_option_id.selected:
    #    hx.errors.fatal("Expiring policy option ID cannot be empty.") Uncomment when not testing

       # Make sure expiring data is up to date
        expiring_policy_fetch_task(hxd, progress)

        # Get correct buckets based on coverage
        buckets = rate_change_buckets(hxd)

        data_schema_static_filename = "data_schema/data_schema_static_copy.py"
        data_schema_static_path = os.path.join(os.path.dirname(__file__), data_schema_static_filename)

        # Rate Change with transient_hxd
        rc = RateChangeLib(
            hxd=hxd,
            progress=progress,
            buckets=buckets,
            layers_path="cds/layers",
            expiring_actual_prem="quoted_premium",
            expiring_technical_prem="benchmark_premium",
            async_tasks=[],  # Pass the actual tasks, not strings
            data_schema_static_path=data_schema_static_path
        )

        rc.calculate_repriced_values(
            #expiring_policy_option_id=679560 #718387 # NOTE: for debugging if needed
        )

        # Use the repriced values to calculate the changes for each bucket
        rarc_df, rarc_list = rc.calculate_rarc_by_layer()
        
        # NOTE: for debugging if needed
        # pd.set_option('display.max_columns', None)
        # print(rarc_df)
        # print(rarc_list)

        # Push to hxd
        for rarc_layer, hxd_layer in zip(rarc_list, hxd.cds.layers):
            hxd_layer.rate_change.temp_storage = rarc_layer["temp_storage"]
            rarc_layer.pop("temp_storage")

            for key, value in rarc_layer.items():
                setattr(hxd_layer.rate_change, key, value)

        # Change in IPO is handelled separately by looking up the ipo lag in a table
        # These values are different than just recalculating tech premium with additional year out from the IPO
        risk_char_rarc = calc_ipo_rarc(hxd) 
        
        for layer in hxd.cds.layers:
            layer.rate_change.risk_characteristics_change.model_calculated = risk_char_rarc

        # Confirm task has been run
        hxd.cds.rate_change.has_rarc_run = True
        hxd.cds.rate_change.has_rarc_not_run = False
    
    else:  # private-priced

        # Set task flags so the UI knows the task completed
        hxd.cds.rate_change.has_rarc_run = True
        hxd.cds.rate_change.has_rarc_not_run = False


@hx.task
def rc_private_task(hxd, progress):
    compute_private_rate_change(hxd)

@hx.task
def start_renewal_task(hxd, progress):
   
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    if not hxd.cds.standard_fields.insured_name:
        hxd.model_state.landing_page_info = "❗❗ FAILED: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner ❗❗"
    else:
        hxd.model_state.pressed_start_renewal_task = True

        # Add tasks which must be done before starting a policy here >>

        # expiring_policy_fetch_task(hxd, progress)

@hx.task
def capiq_fetch_task(hxd, progress):
    capiq_fetch(hxd, progress)
    pass

@hx.task
def populate_capiq_data_task(hxd, progress):
    populate_capiq_data(hxd, progress)
    pass

@hx.task
def populate_capiq_data_from_wb_task(hxd, progress):
    populate_capiq_data_from_wb(hxd, progress)
    pass

@hx.task
def skip_capiq_task(hxd, progress):
    skip_capiq(hxd, progress)
    pass

@hx.task
def set_admitted_to_min_task(hxd, progress):
    adm = hxd.cds.admitted 
    nyftz = True if hxd.cds.company_state == 'New York (FTZ)' else False 
    set_admitted(hxd, "min", adm, nyftz, progress)
    pass

@hx.task
def set_admitted_to_max_task(hxd, progress):
    adm = hxd.cds.admitted
    nyftz = True if hxd.cds.company_state == 'New York (FTZ)' else False 
    set_admitted(hxd, "max", adm, nyftz, progress)
    pass

@hx.task
def set_admitted_to_midpoint_task(hxd, progress):
    adm = hxd.cds.admitted 
    nyftz = True if hxd.cds.company_state == 'New York (FTZ)' else False 
    set_admitted(hxd, "midpoint", adm, nyftz, progress)
    pass

@hx.task
def reset_admitted_reasons_task(hxd, progress):
    reset_admitted_reasons(hxd, progress)
    pass

@hx.task
def process_comment_task(hxd, progress):
    process_comment(hxd, progress)
    pass

@hx.task
def generate_tags_quickquote_add(hxd, progress):
    current_tags = hx.meta.policy_tags
    if "Quick_Quote" not in current_tags:
        new_tags = ["Quick_Quote"]
        hx.meta.policy_tags = current_tags + new_tags       
    else:   # remove "Quick_Quote" ?
        hx.meta.policy_tags = current_tags

@hx.task
def generate_tags_cuap(hxd,progress):
    selected_option = 0
    layer_count_selected = 0
    layers = hxd.cds.layers
    for idx, layer in enumerate(layers):
        if hxd.cds.is_side_a:
            if layer.coverages.side_a.selected == True:
                layer_count_selected += 1
                selected_option = idx + 1
        else:
            if layer.coverages.abc.selected == True:
                layer_count_selected += 1
                selected_option = idx + 1

    current_tags = hx.meta.policy_tags
    #overwrite selected option so only keep quick quote if there.
    if "Quick_Quote" in current_tags:
        current_tags = ["Quick_Quote"]
    else:
        current_tags = []

    p_coverage = hxd.cds.coverage
    p_uw = hxd.cds.standard_fields.underwriter

    p_attach = (hxd.cds.layers[selected_option - 1].excess or 0)
    p_attach = f"{p_attach / 1_000_000:.0f}M"
    if hxd.cds.is_side_a:
        p_tower = (hxd.cds.layers[selected_option - 1].coverages.side_a.tower or 0)
        p_attach = "xs_" + str(p_attach) + "_abc_" + f"{p_tower / 1_000_000:.0f}M" if p_tower > 0 else "xs_" + str(p_attach)
    else:
        p_attach = "xs_" + str(p_attach)

    p_sic = hxd.cds.key_industry.code

    if not p_coverage or not p_uw or (p_attach is None or p_attach == "") or layer_count_selected != 1.0: 
        msg_string = 'Error saving policy tags - Please select: '
        if layer_count_selected != 1:
            msg_string += "One layer only, "
        if not p_coverage:
            msg_string += 'Coverage, '
        if not p_uw:
            msg_string += 'Underwriter, '
        if not p_attach:
            msg_string += 'Layer Attachment'
        if not p_sic:
            msg_string += 'SIC Code'
        hx.errors.validation(msg_string)
        hxd.cds.is_policy_tag_error = True
        hxd.cds.policy_tag_error = msg_string
    else:
        new_tags = ["cov_" + p_coverage.replace(" ",""), 
                    "uw_" + p_uw.replace(" ",""), 
                    p_attach,
                    "sic_" + str(p_sic)]
        hx.meta.policy_tags = current_tags + new_tags
        hxd.cds.is_policy_tag_error = False
        hxd.cds.policy_tag_error = ""
        print(hx.meta.policy_tags)

@hx.task
def generate_tags_twice(hxd, progress):
    generate_tags_cuap(hxd, progress)
    generate_tags_cuap(hxd, progress)

@hx.task
def new_bug_report_task(hxd, progress):
    new_bug_report(hxd, progress, "Rater")

@hx.task
def send_bug_report_task(hxd, progress):
    send_bug_report(hxd, progress)

@hx.task
def cancel_bug_report_task(hxd, progress):
    cancel_bug_report(hxd, progress)

@hx.task
def generate_bug_report_task(hxd, progress):
    generate_bug_report(hxd, progress)

@hx.task
def add_additional_file_task(hxd, progress):
    add_additional_file(hxd, progress)
