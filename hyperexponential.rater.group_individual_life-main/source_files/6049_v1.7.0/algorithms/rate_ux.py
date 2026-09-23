import hx
from algorithms.rate_utilities import one_layer, ratio, validate_empty_fields, pd_df_from_hx_list, write_pd_to_hxd
import numpy as np
import pandas as pd

def show_and_hide_pages(hxd):
    cds = hxd.cds
    ms = hxd.model_state
    layer, cvg = one_layer(hxd)
    db = cvg.death
    ci = cvg.critical_illness
    cover = hxd.cds.cover_selection
    pi = hxd.cds.policy_info
    has_pc = pi.has_profit_commission
    has_ncb = pi.has_no_claims_bonus

    if not cds.is_group:
        return

    # Check DB mandatory fields have been filled in to unhide Premium Calcs
    cover.are_db_fields_full = False
    db_mandatory_fields = ["cover_type", "accidental_death_adj", "sick_weight_to_nationality", "accidental_death_rate"]   
    cover.are_db_fields_full = validate_empty_fields(
        validation_nodes=db_mandatory_fields,
        structure_path="death",
        hxd_structure=db,
        cover_name="Death Benefits",
        include_zero_fields=False
    )
    ms.show_premium_group = cover.are_db_fields_full and ms.show_after_landing_page

    # Check CI mandatory fields
    if ci.is_covered:
        ci_mandatory_fields = ["benefit"]

        if ci.benefit == "Fixed":
            ci_mandatory_fields.append("benefit_amount_fixed")
        elif ci.benefit == "Perc_salary":
            ci_mandatory_fields.append("benefit_amount_pct")

        cover.are_ci_fields_full = validate_empty_fields(
            validation_nodes=ci_mandatory_fields,
            structure_path="critical_illness",
            hxd_structure=ci,
            cover_name="Critical Illness"
        )

    # Check aggs
    cover.are_agg_limits_full = (layer.aggregate_deductible is not None) or (layer.aggregate_limit is not None) or (has_pc) or (has_ncb)

def show_and_hide_fields(hxd):
    layer, cvg = one_layer(hxd)
    tot_ex = layer.totals.total_ex_pc_ncb
    temp = layer.temp
    cover = hxd.cds.cover_selection
    doc = hxd.policy_doc
    pi = hxd.cds.policy_info
    has_pc = pi.has_profit_commission
    has_ncb = pi.has_no_claims_bonus

    #Region (Group Life)
    expo = hxd.cds.exposure.granular

    lives_for_location = expo.lives
    lives_for_location_df = pd_df_from_hx_list(lives_for_location)

    input_cols = [
        "no_lives", 
        "sex", 
        "age_attained", 
        "salary", 
        "salary_multiple",
        "sum_insured",
        "nationality", 
        "location", 
        "region",
        "occupation_code"
        ]

    lives_for_location_df = lives_for_location_df[input_cols]

    # Regions drop down menu for the UK
    region_list = [
        "SOUTH EAST",
        "LONDON",
        "SOUTH WEST",
        "EAST",
        "EAST MIDLANDS",
        "WEST MIDLANDS",
        "NORTHERN IRELAND",
        "YORKSHIRE AND THE HUMBER",
        "WALES",
        "NORTH WEST",
        "NORTH EAST",
        "SCOTLAND"
    ]

    # Assigning UK regions drop down menu
    lives_for_location_df["RegionOptionsList"] = [[] for _ in range(len(lives_for_location_df))]
    lives_for_location_df["RegionOptionsList"] = lives_for_location_df["location"].apply(
        lambda loc: region_list if loc == "United Kingdom" else []
    )

    # Providing the regions options to the data schema
    for i in range(lives_for_location_df.shape[0]):
        listdict = [{"region_options":i} for i in lives_for_location_df["RegionOptionsList"][i]]
        setattr(expo.lives[i],"region_options_list",listdict)
   
    # Critical illness
    ci = cvg.critical_illness

    if ci.benefit == "Fixed":
        ci.show_benefit_amount = True
    elif ci.benefit == "Perc_salary":
        ci.show_benefit_pct = True

    # Agg limits
    are_agg_limits_full = cover.are_agg_limits_full
    are_temp_limits_full = (temp.aggregate_deductible is not None) and (temp.aggregate_limit is not None)  
    are_limits_full = are_agg_limits_full and are_temp_limits_full

    # Total Quoted rates excluding pc and ncb
    total_quoted_rate_excl_pc_ncb_sum = float(
        layer.coverages.death.quoted_rate 
        + layer.coverages.additional_death.quoted_rate 
        + layer.coverages.terminal_illness.quoted_rate 
        + layer.coverages.critical_illness.quoted_rate 
        + layer.coverages.repat_exp.quoted_rate)

    if (are_agg_limits_full or (has_pc) or (has_ncb)) and not temp.is_agg_priced :
        cover.agg_limits_check_show = True
        validation_message = "Inconsistent aggregate limit/deductible and expected loss. Run 'Price for PC/NCB and/or Agg'."
        check_message = "⚠️ PC/NCB and/or Aggregate limit and/or Deductible have been input but expected loss has not been adjusted. Click on 'Price for PC/NCB and/or Agg'."
        hx.errors.validation(validation_message)
        cover.agg_limits_check_message = check_message
        
    elif are_agg_limits_full and temp.is_agg_priced:
        condition = (
            (layer.aggregate_deductible == temp.aggregate_deductible) 
            and (layer.aggregate_limit == temp.aggregate_limit)
            and (pi.profit_commission == temp.profit_commission)
            and (pi.pc_expenses == temp.pc_expenses)
            and (pi.pc_deficit == temp.pc_deficit)
            and (pi.ncb_pct == temp.ncb_pct)
            and (abs(total_quoted_rate_excl_pc_ncb_sum -temp.total_quoted_rate_excl_pc_ncb) < 0.005) )
        if not condition:
            cover.agg_limits_check_show = True
            validation_message = "Inconsistent aggregate limit/deductible and expected loss. Run 'Price for PC/NCB and/or Agg' again."
            check_message = "⚠️ PC/NCB and/or Aggregate limit and/or Deductible have changed. Recalculate the expected loss cost by clicking on 'Price for PC/NCB and/or Agg'."
            hx.errors.validation(validation_message)
            cover.agg_limits_check_message = check_message
    

def allow_policy_doc_download(hxd):
    layer, cvg = one_layer(hxd)
    tot_ex = layer.totals.total_ex_pc_ncb
    cover = hxd.cds.cover_selection
    doc = hxd.policy_doc

    # Allow quote summary download
    if (tot_ex.benchmark_premium or 0) <= 0:
        doc.premium_check = "Gross Benchmark Premium must be calculated before Quote Summary can be downloaded."
        doc.show_premium_check = True
    elif (tot_ex.quoted_premium or 0) <= 0:
        doc.premium_check = "Commercially Achieved Premium must be greater than 0 before Quote Summary can be downloaded."
        doc.show_premium_check = True
    elif cover.agg_limits_check_show:
        doc.premium_check = "Aggregate limit and/or deductible must be priced for before Quote Summary can be downloaded."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True


def validate_status(hxd):
    layer, cvg = one_layer(hxd)

    finalizable_status = ["Bound", "Post Bind Complete"] 

    if layer.status not in finalizable_status:
        hx.errors.validation("If you wish to set the policy to Final, the Status in Risk Information should be either 'Bound' or 'Post Bind Complete'.")


def fill_check_columns(lives_df):
    lstCountry = hx.params.lstCountry
    lstRegion = hx.params.lstRegion
    tblOccupation = hx.params.tblOccupation

    valid_countries = lstCountry["lstCountry"].tolist()
    valid_regions = lstRegion["lstRegion"].tolist()
    valid_codes = tblOccupation["Occupation code"].tolist()

    # Define vectorized conditions directly on the dataframe
    conditions = {
        "no_lives": (lives_df["no_lives"] > 0),
        "sex": (lives_df["sex"].isin(["M", "F"])),
        "age_attained": (lives_df["age_attained"] > 16) & (lives_df["age_attained"] < 85),
        "salary": (lives_df["salary"] > 0),
        "salary_multiple": (lives_df["salary_multiple"] > 0),
        "sum_insured": (lives_df["sum_insured"] > 0),
        "nationality": (lives_df["nationality"].isin(valid_countries)),
        "location": (lives_df["location"].isin(valid_countries)),
        "region": (True),
        "occupation_code": (lives_df["occupation_code"].isin(valid_codes)),
    }

    # Generate the check columns based on vectorized conditions
    for col, condition in conditions.items():
        check_col = col + "_check"
        lives_df[check_col] = condition

    # Determine if all fields are valid
    all_fields_valid = lives_df[[col + "_check" for col in conditions]].all().all()

    # Generate a dictionary indicating if each condition has been met for each column
    check_labels = {
        col + "_check_label": "✅ Okay" if lives_df[col + "_check"].all() else "🔴 Error"
        for col in conditions
    }

    # Replace boolean values with emojis for better readability
    lives_df = lives_df.replace({True: "", False: "🔴 Check"})

    # Validate regions entered for UK are from the drop down menu
    valid_regions.append(None)
    lives_df["region_check"] = lives_df.apply(
        lambda row: row["region"] in valid_regions if row["location"] == "United Kingdom" else True , axis = 1
    )

    # Apply Regions warning to column header
    check_labels["region_check_label"] = "✅ Okay" if lives_df["region_check"].all().all() else "⚠️ Warning"
    lives_df = lives_df.replace({True: "", False: "⚠️ Warning"})

    return lives_df, all_fields_valid, check_labels
