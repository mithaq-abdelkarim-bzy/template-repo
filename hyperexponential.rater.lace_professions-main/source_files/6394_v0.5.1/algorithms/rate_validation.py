# v0.5.0
import hx
import pandas as pd
import numpy as np
import re


def _has_text(value):
    if not value:
        return False

    text = re.sub(r"<[^>]*>", "", str(value))
    text = text.replace("&nbsp;", " ").strip()
    return bool(text)


def _is_populated(value):
    if value is None:
        return False
    if isinstance(value, str):
        return _has_text(value)
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float, np.number)):
        return value != 0
    return True


def _validate_claims_mandatory_fields(hxd):
    mandatory_fields = ["claim_name", "claim_made_date", "currency"]
    fields_to_check = [
        "claim_id",
        "claim_name",
        "loss_date",
        "claim_made_date",
        "claim_status",
        "claim_close_date",
        "deductible",
        "paid_claims",
        "incurred_claims",
        "transaction_date",
        "defense_fgu_paid",
        "defense_fgu_os",
        "indemnity_fgu_paid",
        "indemnity_fgu_os",
    ]

    for index, claim in enumerate(hxd.cds.experience_rating.claims, start=1):
        row_has_data = any(_is_populated(getattr(claim, field)) for field in fields_to_check)
        missing_mandatory_field = any(not _is_populated(getattr(claim, field)) for field in mandatory_fields)

        if row_has_data and missing_mandatory_field:
            hx.errors.validation(
                "Claims row {index}: Claim Made, Claim Made Date and Currency must be populated.".format(index=index)
            )


def rate_validations(hxd):

    # Pricing Page
    # Retention Table
    rs_neg_check = False
    for item in hxd.cds.retention_split:
        if (item.eec or 0) < 0: rs_neg_check = True
        if (item.aggregate or 0) < 0: rs_neg_check = True
        if (item.retention_underlying or 0) < 0: rs_neg_check = True
        if (item.retention_residual or 0) < 0: rs_neg_check = True

    if rs_neg_check:
        hx.errors.validation("There are negative values in the Retention table")

    # Policy Structures
    ps_neg_check = False
    node_list = ""
    for item in hxd.cds.layers:
        for node in ["limit_eec", "limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg", "brokerage" ]:
            if (getattr(item, node) or 0) < 0: 
                ps_neg_check = True
                node_list += f"{node}, "

    if ps_neg_check:
        hx.errors.validation(f"There are negative values in columns in the Policy Structures Table that are not allowed negative values: {node_list}")

    # Policy Structures
    ps_neg_check = False
    node_list = ""
    for item in hxd.cds.layers_addl:
        for node in ["limit_eec", "limit_agg", "excess_eec", "excess_agg", "rtc", "rtc_agg", "brokerage"]:
            if (getattr(item, node) or 0) < 0: 
                ps_neg_check = True
                node_list += f"{node}, "

    if ps_neg_check:
        hx.errors.validation(f"There are negative values in columns in the Additinoal Policy Structures Table that are not allowed negative values: {node_list}")

    # RISK INFORMATION
    # Insured name must be completed, this is needed to ensure landing page works correctly
    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("Insured name field must be completed.")
    
    if not hxd.cds.standard_fields.underwriter:
        hx.errors.validation("Underwriter field must be completed")
    
    # if not hxd.cds.profession:
    #     hx.errors.validation("Profession field must be completed")

    if not hxd.cds.currencies.source_currency:
        hx.errors.validation("Source Currency field must be completed")       


    # Claims
    _validate_claims_mandatory_fields(hxd)

    if not hxd.cds.experience_rating.claims_asatdate:
        bool_claims_populated = False
        for item in hxd.cds.experience_rating.claims:
            if item.claim_name:
                bool_claims_populated = True

        if bool_claims_populated:
            hx.errors.validation("Claims As At Date must be completed")
    # TERRITORY

    # Validation to check how many layers are set as bound, also updates premium label for bound policies
    bound_count = 0
    include_count = 0
    layers_all = [hxd.cds.layers, hxd.cds.layers_addl]

    for layer_set in layers_all:
        for layer in layer_set:
            if layer.status in ["Bound", "Post Bind Complete"]:
                bound_count += 1
                layer.premium_label = "Gross Bound Premium"
            else:
                layer.premium_label = "Gross Quoted Premium"

            if layer.include:
                include_count +=1

    if include_count == 0:
        hx.errors.validation("At least one layer must be included")
    
    # bound_count = 0
    # for layer_set in layers_all:
    #     for layer in layer_set:
    #         if layer.status in ["Bound", "Not Taken Up"]:
    #             bound_count += 1

    if bound_count == 0:
        hx.errors.validation("Status must be set as 'Bound' or 'Post Bind Complete' to mark a policy as final")


    # agg_ret is unique
    regions = [item.region for item in hxd.cds.retention_split if item.region is not None]
    if len(regions) != len(set(regions)):
        hx.errors.validation("There are duplicate regions in the Retention table")

    # UW Comments in Structure & Pricing Page
    comments_bool = False
    for layer_set in layers_all:
        for layer in layer_set:
            if layer.include:
                if (
                    (layer.wordings_adj or 0) != 0
                    or (layer.uw_adj or 0) != 0
                    or layer.experience_weighting_2.is_overridden
                ):
                    comments_bool = True

    uw_comments = hxd.cds.standard_fields.uw_rationale
    if comments_bool:
        if not _has_text(uw_comments):
            hx.errors.validation("UW comments in the Structure & Pricing page need to be populated with rationale around non-zero UW adjustments (wordings or UW) or overridden experience weighting")


    