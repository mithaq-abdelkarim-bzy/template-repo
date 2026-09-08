import hx
import numpy as np
import pandas as pd
from algorithms.rate_utilities import one_layer, ratio, validate_empty_fields, write_pd_to_hxd
from algorithms.data_schema.sch_rater_defined import airlines_validation_cols, ga_validation_cols

def show_and_hide_pages(hxd):
    cds = hxd.cds
    layer, cvg = one_layer(hxd)
    ms = hxd.model_state
    doc = hxd.policy_doc
    
    if not cds.rater:
        cds.is_neither = True
        hx.errors.validation("Please select 'Airlines' or 'General Aviation' in Risk Information.")

    if (cds.is_airlines and ms.pressed_ga_task) or (cds.is_ga and ms.pressed_airlines_task):
        ms.is_product_inconsistent = True
        hx.errors.validation("Inconsistent product selected and model shown. Please return to 'Risk Information' and select 'Airlines' or 'General Aviation' correctly.")
    
    # Add message as default
    doc.premium_check = "Gross Benchmark Premium must be calculated before Summary can be downloaded."
    doc.show_premium_check = True
    

def show_and_hide_fields(hxd):
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    sql = hxd.sql_db
    ms = hxd.model_state

    # Show message to prevent duplicate selection
    selected_aircrafts = [reg.registration for reg in sql.duplicate_regs if reg.is_selected]
    duplicate_aircrafts = set([ac for ac in selected_aircrafts if selected_aircrafts.count(ac) > 1])

    if duplicate_aircrafts:
        sql.are_duplicate_regs_selected = True
        sql.duplicate_regs_selected_msg = "❗❗ Can only select one aircraft per registration. Duplicate selections: " + str(duplicate_aircrafts)
    
    # Show button to keep selected regs when duplicates are present
    sql.is_at_least_one_reg_selected = True if any(reg.is_selected for reg in sql.duplicate_regs) else False
    sql.is_at_least_one_reg_selected *= sql.has_duplicate_regs or False
    sql.is_at_least_one_reg_selected *= not (sql.are_duplicate_regs_selected or False)

    # Check status split
    ss = expo.status_split
    status_split_sum = sum([ss.in_service or 0, ss.storage or 0, ss.other or 0])
    is_status_split_used = (ss.in_service is not None) or (ss.storage is not None) or (ss.other is not None)
    
    if is_status_split_used and (status_split_sum != 1):
        expo.show_status_split_msg = True
        expo.status_split_msg = f"Status split must add up to 100% when used. Current sum is {status_split_sum:.0%}."
        hx.errors.validation("Status split in Airlines/Aircraft Details must add up to 100%.")

    # Show full Details table vs. validation
    expo.show_full_table = sql.are_regs_selected and (not expo.show_check_cols)
    expo.show_validation_table = sql.are_regs_selected and expo.show_check_cols


def allow_policy_doc_download(hxd):
    layer, cvg = one_layer(hxd)
    doc = hxd.policy_doc

    # Allow quote summary download
    if (layer.benchmark_premium or 0) <= 0:
        doc.premium_check = "Gross Benchmark Premium must be calculated before Summary can be downloaded."
        doc.show_premium_check = True
    elif (layer.quoted_premium or 0) <= 0:
        doc.premium_check = "Gross Quoted Premium must be greater than 0 before Summary can be downloaded."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True
        doc.show_premium_check = False


def validate_custom_fields(hxd):
    layer, cvg = one_layer(hxd)
    expo = hxd.cds.exposure.granular
    ms = hxd.model_state

    # YZ: change this to allow 0
    # Check fleet size
    if ms.pressed_airlines_task or ms.pressed_ga_task:
        if (expo.fleet_size.selected or 0) < 0:
            hx.errors.validation("Fleet Size cannot be less than 0.")


def validate_status(hxd):
    layer, cvg = one_layer(hxd)

    finalizable_status = ["Bound", "Post Bind Complete"] 

    if layer.status not in finalizable_status:
        hx.errors.validation("If you wish to set the policy to Final, the Status in Risk Information should be either 'Bound' or 'Post Bind Complete'.")


def fill_check_columns(hxd, rating_df):
    # inception_date = hxd.hx_core.inception_date
    # expiry_date = hxd.hx_core.expiry_date

    inception_date = pd.Timestamp(hxd.hx_core.inception_date)
    expiry_date = pd.Timestamp(hxd.hx_core.expiry_date)

    # Define conditions and corresponding failure messages based on model
    common_conditions = {
        "no_of_aircraft": (rating_df["no_of_aircraft"] > 0),
        "value": (rating_df["value"] >= 0) | (rating_df["value"].isna()),
        "attachment_date": (rating_df["attachment_date"] >= inception_date) & (rating_df["attachment_date"] <= expiry_date),
        "time_in_service": ((rating_df["time_in_service"] >= 0) & (rating_df["time_in_service"] <= 1)) | (rating_df["time_in_service"].isna()),
        "total_seats": (rating_df["total_seats"] >= 0) | (rating_df["total_seats"].isna()),
    }
    common_fail_messages = {
        "no_of_aircraft": "🔴 Must be > 0",
        "value": "🔴 Must be ≥ 0",
        "attachment_date": "🔴 Must be between policy's inception and expiry",
        "time_in_service": "🔴 Must be between 0% and 100%",
        "total_seats": "🔴 Must be ≥ 0",
    }

    if hxd.cds.is_ga:
        conditions = {
            **common_conditions,
            "per_occ_deductible_pct": ((rating_df["per_occ_deductible_pct"] >= 0) & (rating_df["per_occ_deductible_pct"] <= 1))| (rating_df["per_occ_deductible_pct"].isna()), 
            "per_occ_deductible": (rating_df["per_occ_deductible"] >= 0) | (rating_df["per_occ_deductible"].isna()), 
            #YZ change crew seats allow 0
            "crew_seats": (rating_df["crew_seats"] >= 0) | (rating_df["crew_seats"].isna()), 
            "per_pax_liab_limit": (rating_df["per_pax_liab_limit"] >= 0) | (rating_df["per_pax_liab_limit"].isna()), 
            "combined_single_limit": (rating_df["combined_single_limit"] >= 0) | (rating_df["combined_single_limit"].isna()), 
            #YZ change tpl_limit_exposed to allow 0
            "tpl_limit_exposed": ((rating_df["tpl_limit_exposed"] >= 0) & (rating_df["tpl_limit_exposed"] <= 1)) | (rating_df["tpl_limit_exposed"].isna()), 
            # FS 27/08/2025: Build year validation added to ensure it is greater than 1900
            "build_year": (rating_df["build_year"] > 1900), # Removed na allowance
            "use": (rating_df["use"].notna()),
            #"registration": (rating_df["registration"].notna()),
            "operator_country" : (rating_df["operator_country"].notna()),
            "aircraft_class" : (rating_df["aircraft_class"].notna()),
        }
        fail_messages = {
            **common_fail_messages,
            "per_occ_deductible_pct": "🔴 Must be between 0% and 100%",
            "per_occ_deductible": "🔴 Must be ≥ 0",
            "crew_seats": "🔴 Must be ≥ 0",
            "per_pax_liab_limit": "🔴 Must be ≥ 0",
            "combined_single_limit": "🔴 Must be ≥ 0",
            "tpl_limit_exposed": "🔴 Must be between 0% and 100%",
            # FS 27/08/2025: Build year validation added to ensure it is greater than 1900
            "build_year": "🔴 Must be > 1900",
            "use": "🔴 Must not be blank",
            #"registration": "🔴 Must not be blank",
            "operator_country": "🔴 Must not be blank",
            "aircraft_class": "🔴 Must not be blank",
        }
    else:
        conditions = {
            **common_conditions,
            # YZ 08/06/2026: Build year validation added to ensure it is greater than 1900
            # "build_year": (rating_df["build_year"] > 1900) | (rating_df["build_year"].isna()),
            "build_year": (rating_df["build_year"] > 1900),
            "previous12_months_hours": (rating_df["previous12_months_hours"] >= 0) | (rating_df["previous12_months_hours"].isna()),
            "operating_mtow_lb": (rating_df["operating_mtow_lb"] > 0) | (rating_df["operating_mtow_lb"].isna()),
            "hull_limit": (rating_df["hull_limit"] >= 0) | (rating_df["hull_limit"].isna()),
            "hull_excess": (rating_df["hull_excess"] >= 0) | (rating_df["hull_excess"].isna()),
            "liability_limit": (rating_df["liability_limit"] >= 0) | (rating_df["liability_limit"].isna()),
            "liability_excess": (rating_df["liability_excess"] >= 0) | (rating_df["liability_excess"].isna()),
            "pll_award": (rating_df["pll_award"] >= 0) | (rating_df["pll_award"].isna()),
            "time_in_service": ((rating_df["time_in_service"] == 0) & (rating_df["aircraft_status"] == "Storage")) | (rating_df["aircraft_status"] != "Storage"), # FS 20/09/2025: Additional condition added for time_in_service
        }

        fail_messages = {
            **common_fail_messages,
            "build_year": "🔴 Must be > 1900",
            "previous12_months_hours": "🔴 Must be ≥ 0",
            "operating_mtow_lb": "🔴 Must be > 0",
            "hull_limit": "🔴 Must be ≥ 0",
            "hull_excess": "🔴 Must be ≥ 0",
            "liability_limit": "🔴 Must be ≥ 0",
            "liability_excess": "🔴 Must be ≥ 0",
            "pll_award": "🔴 Must be ≥ 0",
            "time_in_service": "🔴 Must be 0% if in status is storage" # FS 20/09/2025: Additional condition added for time_in_service
        }

    # Apply standard conditions with specific failure messages
    for col, condition in conditions.items():
        check_col = col + "_check"
        rating_df[check_col] = np.where(condition, "", fail_messages[col])

    # Handle expiry_date separately with multiple potential failure messages
    expiry_cond = (rating_df["expiry_date"] > inception_date) & \
                  (rating_df["expiry_date"] > rating_df["attachment_date"]) & \
                  (rating_df["expiry_date"] <= expiry_date)
    expiry_conditions = [
        rating_df["expiry_date"] <= rating_df["attachment_date"],
        rating_df["expiry_date"] <= inception_date,
        rating_df["expiry_date"] > expiry_date
    ]
    expiry_fail_msgs = [
        "🔴 Must be after attachment date",
        "🔴 Must be after policy's inception",
        "🔴 Must be on or before policy's expiry"
    ]

    # Use np.select to assign messages based on which sub-condition fails first; if all pass, assign no message
    rating_df["expiry_date_check"] = np.select(expiry_conditions, expiry_fail_msgs, default="")

    # List all check columns including expiry_date_check
    check_cols = [col + "_check" for col in conditions] + ["expiry_date_check"]

    # Determine if all fields are valid. This is used in show and hide Rating Summary and Rate Change page too.
    rating_df["has_error"] = rating_df[check_cols].apply(lambda row: any(val != "" for val in row), axis=1)
    all_fields_valid = rating_df[[col + "_check" for col in conditions]].apply(lambda x: x.eq("")).all().all()

    #Validation added that for airlines cannot have empty coverages for both Hull and Liab
    cds = hxd.cds
    coverage = cds.layers[0].coverages
    no_coverages_bool = True
    if cds.is_airlines:
        if (coverage.hull.coverage is None) and (coverage.liability.coverage is None):
            no_coverages_bool = False
        
    all_fields_valid = all_fields_valid and no_coverages_bool

    # Generate a summary label for each condition across the dataframe
    check_labels = {
        col + "_check_label": "✅ Okay" if conditions[col].all() else "🔴 Error"
        for col in conditions
    }

    # Add summary for expiry_date separately
    check_labels["expiry_date_check_label"] = "✅ Okay" if expiry_cond.all() else "🔴 Error"

    # Prepare filtered dataframe with check columns replaced for readability
    filtered_rating_df = rating_df[check_cols + ["has_error"]]

    return filtered_rating_df, all_fields_valid, check_labels

def validate_table(hxd, rating_df):
    expo = hxd.cds.exposure.granular

    # Define variable based on model
    if hxd.cds.is_ga:
        table_name = "Aircraft"
        air_list = expo.aircrafts
        validation_cols = ga_validation_cols
        hxd_check_col_labels = "ga_check_col_labels"
    else:
        table_name = "Airlines"
        air_list = expo.airlines
        validation_cols = airlines_validation_cols
        hxd_check_col_labels = "airlines_check_col_labels"

    # Validate entries in the table
    filtered_rating_df, all_fields_valid, check_labels = fill_check_columns(hxd, rating_df)

    okay_msg = "✅ All entries are valid."
    error_msg = "⚠️ Click on 'Validate data'. All details must be valid to proceed to the rating summary."
    expo.data_check = okay_msg if all_fields_valid else error_msg

    expo.all_fields_valid = all_fields_valid
    expo.show_rc_page = (all_fields_valid & hxd.cds.standard_fields.is_renewal) 
     
    if expo.show_check_cols:
        expo.data_check = "🔴 Fix the invalid entries." if not all_fields_valid else okay_msg
        check_cols = [(col + "_check") for col in validation_cols]
        
        # Push validation to hxd
        write_pd_to_hxd(filtered_rating_df, air_list, check_cols + ["has_error"])
        setattr(expo, hxd_check_col_labels, check_labels)
    
    #Validation added that for airlines cannot have empty coverages for both Hull and Liab
    cds = hxd.cds
    coverage = cds.layers[0].coverages
    no_coverages_bool = True
    if cds.is_airlines:
        if (coverage.hull.coverage is None) and (coverage.liability.coverage is None):
            no_coverages_bool = False
        
    all_fields_valid = all_fields_valid and no_coverages_bool

    # Check entries are valid
    if (not all_fields_valid) :
        hx.errors.validation(f"Some entries in the {table_name} Details table are invalid and must be fixed.")