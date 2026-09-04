import hx, os, json, requests, openpyxl
import pandas as pd
from copy import deepcopy
from algorithms.rate_utilities import pd_df_from_hx_list, df_to_nested_list, transient_list_from_hx_list, ratio, weighted_average
from libraries.hx_renew_api.algorithms.init_hx_renew_api import init_hx_renew_api
from algorithms.sql_bi_fetch import bi_policy_fetch, bi_claim_fetch
from algorithms.transient_hxd import init_transient_hxd
from algorithms.rate_rate_change import expiring_policy_fetch_task
from algorithms.rating import rating_algorithm
from libraries.email_notification.algorithms.bug_report import new_bug_report, send_bug_report, cancel_bug_report, add_additional_file, generate_bug_report




@hx.task
def sql_bi_fetch_task(hxd, progress):
    if hxd.cds.standard_fields.policy_reference:
        bi_policy_fetch(hxd, progress)
        bi_claim_fetch(hxd, progress)
    else:
        hxd.messages.fetch_bi_task_status = "❗ No policy reference entered. ❗"



# 18/07/25 SB Added to help backfill exposure measure if not available on historical data, assuming current exposure and trends
@hx.task
def backfill_exposure(hxd, progress):
    ms = hxd.model_state
    er_calcs = hxd.cds.experience_rating.er_calcs
    hxd_er = hxd.cds.experience_rating

    # Determine exposure trend
    exposure_trend = hxd_er.exposure_trend or 0

    # Validate exposure trend range
    if exposure_trend < 0 or exposure_trend > 1:
        hxd.messages.fetch_bi_task_status = (
            f"❗ Exposure trend of {int(exposure_trend * 100)}% is invalid. Please enter a value between 0% and 100%. ❗"
        )
        return

    trend_msg = (
        f"✅ {int(exposure_trend * 100)}% exposure trend applied."
        if hxd_er.exposure_trend
        else "❗ 0% exposure trend assumed as none was provided."
    )

    # Get values from the current year (assumed to be index 7)
    source_non_ed = hxd_er.curr_yr.exp_non_ed
    source_ed = hxd_er.curr_yr.exp_ed

    # Check if at least one current year exposure value is populated
    if (source_non_ed in [None, "", 0]) and (source_ed in [None, "", 0]):
        hxd.messages.fetch_bi_task_status = (
            f"❗ Current exposure needs to be populated before backfilling. {trend_msg} "
        )
    else:
        # Apply compounded reduction from the current year backward
        for i in range(8):
            years_back = 8 - i
            trend_factor = (1 - exposure_trend) ** years_back
            er_calcs[i].exp_non_ed = (
                source_non_ed * trend_factor if source_non_ed not in [None, "", 0] else None
            )
            er_calcs[i].exp_ed = (
                source_ed * trend_factor if source_ed not in [None, "", 0] else None
            )

        hxd.messages.fetch_bi_task_status = (
            f"✅ Exposure backfilled successfully. {trend_msg} "
        )








@hx.task
def sync_expiring_ids(hxd, progress):
    # Note this task is to be run following each migrated policy to sync the expiring ids
    hxd.model_state.expiring_policy_option_id = hx.meta.expiring_policy_option_id
    # hxd.model_state.expiring_policy_option_id = 56654 # For debugging



@hx.task
def start_renewal_task(hxd, progress):
    # The following statement checks that the expiring information has been imported for renewals. Some teams might want to start
    # from a blank rater each time, in which case update the below
    ms = hxd.model_state
    sf = hxd.cds.standard_fields
    if not hxd.cds.standard_fields.insured_name:
        ms.landing_page_info = "❗**FAILED**: Click 'Undo' then 'Import Expiring Policy Data' in the top right corner.❗"
    else:
        ms.pressed_start_renewal_task = True
        ms.expiring_policy_option_id = hx.meta.expiring_policy_option_id
        sf.is_renewal = True

        # Add tasks which must be done before starting a policy here >>


@hx.task
def case_priced_expiry_import(hxd, progress):
    expiring_policy_snapshot = expiring_policy_fetch_task(hxd, progress)

    # Pull in expiring policy snapshot
    expiring_policy_snapshot = expiring_policy_fetch_task(hxd, progress)

    # Write expiring premiums to hxd
    pol_rc = hxd.cds.layers[0].rate_change
    pol_rc.premium_annualized_100pct.expiring = expiring_policy_snapshot["cds"]["layers"][0]["quoted_premium_annualised"]
    expiring_written_line = expiring_policy_snapshot["cds"]["layers"][0]["written_line"]
    pol_rc.premium_annualized_beazley_share.expiring = (pol_rc.premium_annualized_100pct.expiring or 0) * (expiring_written_line or 0)

    pol_rc.expiring_policy_info.expiring_bpi = expiring_policy_snapshot["cds"]["layers"][0]["bpi_case_priced"]


@hx.task
def rarc_task(hxd, progress):
    
    # ~~~~~~~~~~~~
    
    # Pull in expiring policy snapshot
    expiring_policy_snapshot = expiring_policy_fetch_task(hxd, progress)

    # Write expiring premiums to hxd
    pol_rc = hxd.cds.layers[0].rate_change
    pol_rc.premium_annualized_100pct.expiring = expiring_policy_snapshot["cds"]["layers"][0]["quoted_premium_annualised"]
    expiring_written_line = expiring_policy_snapshot["cds"]["layers"][0]["written_line"]
    pol_rc.premium_annualized_beazley_share.expiring = (pol_rc.premium_annualized_100pct.expiring or 0) * (expiring_written_line or 0)

    # Confirm task has been run
    hxd.cds.rate_change.has_fetch_run = True
    hxd.cds.rate_change.has_fetch_not_run = False

    # ~~~~~~~~~~~~~~~
    # SET UP CUMULATIVE HXD BUCKETS
    
    transient_expiring_hxd = init_transient_hxd(expiring_policy_snapshot)

    # Exposure & Risk Characteristics
    
    transient_hxd_exposure_risk = deepcopy(transient_expiring_hxd)
    transient_hxd_exposure_risk.cds.exposure.granular.education = transient_list_from_hx_list(hxd.cds.exposure.granular.education)
    transient_hxd_exposure_risk.cds.exposure.granular.non_education = transient_list_from_hx_list(hxd.cds.exposure.granular.non_education)

    transient_hxd_exposure_risk.cds.rating_factors.risk_preparedness = hxd.cds.rating_factors.risk_preparedness
    transient_hxd_exposure_risk.cds.rating_factors.security = hxd.cds.rating_factors.security
    transient_hxd_exposure_risk.cds.rating_factors.crisis_management = hxd.cds.rating_factors.crisis_management
    transient_hxd_exposure_risk.cds.rating_factors.social_media = hxd.cds.rating_factors.social_media
    transient_hxd_exposure_risk.cds.rating_factors.high_profile_event = hxd.cds.rating_factors.high_profile_event
    transient_hxd_exposure_risk.cds.modifiers.underwriter_adjustment = hxd.cds.modifiers.underwriter_adjustment

    # Deductible / excess
    transient_hxd_deductible = deepcopy(transient_hxd_exposure_risk)
    transient_hxd_deductible.cds.layers[0].type = hxd.cds.layers[0].type
    transient_hxd_deductible.cds.layers[0].excess = hxd.cds.layers[0].excess
    transient_hxd_deductible.cds.layers[0].deductible = hxd.cds.layers[0].deductible

    # Limit
    transient_hxd_limit = deepcopy(transient_hxd_deductible)
    transient_hxd_limit.cds.layers[0].limit = hxd.cds.layers[0].limit
    transient_hxd_limit.cds.layers[0].aggregate_limit = hxd.cds.layers[0].aggregate_limit

    # T&C
    transient_hxd_t_c = deepcopy(transient_hxd_limit)
    transient_hxd_t_c.cds.rating_factors.bi_and_ee_cover = hxd.cds.rating_factors.bi_and_ee_cover
    transient_hxd_t_c.cds.rating_factors.seperate_bi_ee_agg_limits = hxd.cds.rating_factors.seperate_bi_ee_agg_limits
    transient_hxd_t_c.cds.rating_factors.bi_tiv = hxd.cds.rating_factors.bi_tiv
    transient_hxd_t_c.cds.rating_factors.liability_covered = hxd.cds.rating_factors.liability_covered
    transient_hxd_t_c.cds.rating_factors.extensions_covered = hxd.cds.rating_factors.extensions_covered
       
    # Brokerage
    brokerage_expiring = transient_expiring_hxd.cds.layers[0].brokerage
    brokerage_renewal = hxd.cds.layers[0].brokerage

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # RUN RATING ALGORITHM ON EACH BUCKET
    
    rating_algorithm(transient_expiring_hxd)
    rating_algorithm(transient_hxd_exposure_risk)
    rating_algorithm(transient_hxd_deductible)
    rating_algorithm(transient_hxd_limit)
    rating_algorithm(transient_hxd_t_c)


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # CALCULATE RATE CHANGE PERCENTAGES

    rc = hxd.cds.layers[0].rate_change

    # Risk Characteristsis (must start with this one)
    ed_df = pd_df_from_hx_list(transient_expiring_hxd.cds.exposure.granular.education)
    non_ed_df = pd_df_from_hx_list(transient_expiring_hxd.cds.exposure.granular.non_education)
    expiring_rf = transient_expiring_hxd.cds.rating_factors
    expiring_modifier = (transient_expiring_hxd.cds.modifiers.underwriter_adjustment or 0) + 1

    expiring_avg_freq = (
        weighted_average(ed_df['rate_multiplier'], ed_df['num_students'], if_undefined=0) * expiring_rf.preparedness_factor_ed
        + weighted_average(non_ed_df['rate_multiplier'], non_ed_df['num_of_est'], if_undefined=0) * expiring_rf.preparedness_factor_non_ed
    ) * expiring_modifier

    ed_df = pd_df_from_hx_list(transient_hxd_exposure_risk.cds.exposure.granular.education)
    non_ed_df = pd_df_from_hx_list(transient_hxd_exposure_risk.cds.exposure.granular.non_education)
    renewal_rf = transient_hxd_exposure_risk.cds.rating_factors
    renewal_modifier = (transient_hxd_exposure_risk.cds.modifiers.underwriter_adjustment or 0) + 1

    renewal_avg_freq = (
        weighted_average(ed_df['rate_multiplier'], ed_df['num_students'], if_undefined=0) * renewal_rf.preparedness_factor_ed
        + weighted_average(non_ed_df['rate_multiplier'], non_ed_df['num_of_est'], if_undefined=0) * renewal_rf.preparedness_factor_non_ed
    ) * renewal_modifier

    rc.risk_characteristics_change.model_calculated = ratio(renewal_avg_freq, expiring_avg_freq, if_undefined=1)

    
    # Exposure
    expiring_el = transient_expiring_hxd.cds.ground_up_expected_loss
    renewal_el = transient_hxd_exposure_risk.cds.ground_up_expected_loss

    expiring_el_total = (
        (expiring_el.education_annualised or 0) * expiring_rf.preparedness_factor_ed * expiring_modifier 
        + (expiring_el.non_education_annualised or 0) * expiring_rf.preparedness_factor_non_ed * expiring_modifier
    )

    renewal_el_total = (
        (renewal_el.education_annualised or 0) * renewal_rf.preparedness_factor_ed * renewal_modifier 
        + (renewal_el.non_education_annualised or 0) * renewal_rf.preparedness_factor_non_ed * renewal_modifier
    )

    rc.exposure_change.model_calculated = ratio(
        ratio(
            renewal_el_total, 
            expiring_el_total, 
            if_undefined=1
        ),
        rc.risk_characteristics_change.model_calculated,
        if_undefined=1
    )

    
    # Deductible
    rc.deductible_change.model_calculated = ratio(
        transient_hxd_deductible.cds.layers[0].benchmark_premium_annualised, 
        transient_hxd_exposure_risk.cds.layers[0].benchmark_premium_annualised, 
        if_undefined=1
    )

    # Limit
    rc.limit_change.model_calculated = ratio(
        transient_hxd_limit.cds.layers[0].benchmark_premium_annualised, 
        transient_hxd_deductible.cds.layers[0].benchmark_premium_annualised, 
        if_undefined=1
    )

    # T&C
    rc.terms_conditions_change.model_calculated = ratio(
        transient_hxd_t_c.cds.layers[0].benchmark_premium_annualised, 
        transient_hxd_limit.cds.layers[0].benchmark_premium_annualised, 
        if_undefined=1
    )

    # deductible
    rc.brokerage_change.model_calculated = (1 - brokerage_expiring) / (1 - brokerage_renewal)

    # Other
    rc.other_change.model_calculated = 1

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # WRITE BACK TO HXD
    
    # Write benchmrk and quoted premium to flag when task needs to be re-run
    layer = hxd.cds.layers[0]
    rc.temp_storage.benchmark_premium = layer.benchmark_premium
    rc.temp_storage.quoted_premium = layer.quoted_premium

    # Confirm task has been run
    hxd.cds.rate_change.has_rarc_run = True
    hxd.cds.rate_change.has_rarc_not_run = False

    # so we can clear out the overrides on renewal we need the uw_selected values to be set within the async task - instead of row 97 of rate change algo - it could be implemented more elegantly but it works!
    for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]:
        rc_vbl = getattr(layer.rate_change, item)
        rc_vbl.uw_selected.calculated = rc_vbl.model_calculated    


# Generate policy document in Excel
@hx.task
def policy_to_excel_task(hxd, progress):    
    from openpyxl.utils.cell import coordinate_to_tuple
    
    # Load string containing data
    data = json.loads(hxd.policy_doc.data_dict)

    # Write the dictionary values to the Excel template
    template_path = f"./model/algorithms/policy_document_template.xlsx"

    # Load the workbook 
    workbook = openpyxl.load_workbook(template_path)

    # Fill the named ranges with data
    for key, value in data.items():
        if key in workbook.defined_names:
            # Get the cell corresponding to the named range
            cells = workbook.defined_names[key].destinations
            for sheet_name, coord in cells:
                # Get the relevant worksheet
                sheet = workbook[sheet_name]
                # If value is a list, write values dynamically
                if isinstance(value, list):
                    coord = coord.replace("$", "")
                    row, col = coordinate_to_tuple(coord)
                    for df_row_index, df_row in enumerate(value, start=row):
                        for df_col_index, (cell_key, cell_value) in enumerate(df_row.items(), start=col):
                            # Write each value into the corresponding cell
                            sheet.cell(row=df_row_index, column=df_col_index, value=cell_value)
                else:
                    # Assign single value to the cell
                    sheet[coord] = value


    # Protect the sheet to prevent changes
    # sheet.protection.enable()
    # sheet.protection.set_password(excel_password)

    # rationale_sheet = workbook['Rationale']
    # rationale_sheet.sheet_state = 'hidden'

    # Save the filled template to a new file
    with hxd.policy_doc.output_file.open("b") as f:
        workbook.save(f)

    # Store task data to allow comparison if anything changes in rating
    hxd.policy_doc.task_data_dict = hxd.policy_doc.data_dict

@hx.task
def new_bug_report_task(hxd, progress):
    model_name = "DWP"
    new_bug_report(hxd, progress, model_name)

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



