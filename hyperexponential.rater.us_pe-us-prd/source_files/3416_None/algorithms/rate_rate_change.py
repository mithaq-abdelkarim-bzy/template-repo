import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio
from operator import itemgetter
from algorithms.rate_constants import max_layers


def rate_change_buckets(hxd):

    bucket = None
    current_product_type = hxd.cds.account_details.product_type

    manutech = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": ["cds/rating_factors/revenues"],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
            "cds/layers/defence_outside_limits/limit",
        ],
        "terms_conditions": ["cds/account_details/retroactive_years/years"],
        "brokerage": ["cds/layers/brokerage"],
    }

    products = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": ["cds/rating_factors/revenues"],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
            "cds/layers/defence_outside_limits/limit",
            "cds/layers/product_liability_limits_AGG",
        ],
        "terms_conditions": ["cds/account_details/retroactive_years/years"],
        "brokerage": ["cds/layers/brokerage"],
    }

    tech = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": ["cds/rating_factors/revenues"],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
            "cds/layers/defence_outside_limits/limit",
        ],
        "terms_conditions": [
            "cds/rating_factors/tech/cont_bi_pd",
            "cds/rating_factors/tech/media_and_advertising",
            "cds/rating_factors/tech/first_party_privacy",
            "cds/rating_factors/tech/cyber_extortion_only",
            "cds/rating_factors/general_liability/value",
            "cds/account_details/retroactive_years/years",
        ],
        "brokerage": ["cds/layers/brokerage"],
    }

    staffing = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": ["cds/rating_factors/revenues"],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
        ],
        "terms_conditions": [
            "cds/account_details/retroactive_years/years"
            "cds/rating_factors/general_liability/value",
        ],
        "brokerage": ["cds/layers/brokerage"],
    }
    mpl = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": ["cds/rating_factors/revenues"],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
            "cds/rating_factors/business_with_written_contact/revenue",
            "cds/rating_factors/business_with_written_contact/percentage",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
        ],
        "terms_conditions": ["cds/account_details/retroactive_years/years"],
        "brokerage": ["cds/layers/brokerage"],
    }

    med_mal = {
        "model": [],  # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/rating_factors/med_mal/allied_medical/allied_medical_type",
            "cds/rating_factors/med_mal/allied_medical/exposure_measure",
            "cds/rating_factors/med_mal/social_services/social_services_type",
            "cds/rating_factors/med_mal/social_services/exposure_measure",
        ],
        "risk_characteristics": [
            "cds/rating_factors/loss_experience",
            "cds/rating_factors/professional_experience/years",
            "cds/rating_factors/longevity/years",
        ],
        "deductible": ["cds/layers/excess", "cds/layers/deductible"],
        "limit": [
            "cds/layers/limit",
            "cds/layers/aggregate_limit",
        ],
        "terms_conditions": ["cds/account_details/retroactive_years/years"],
        "brokerage": ["cds/layers/brokerage"],
        "other": [],
    }

    if current_product_type == "Manutech":
        bucket = manutech
    elif current_product_type == "Products":
        bucket = products
    elif current_product_type == "Tech":
        bucket = tech
    elif current_product_type == "Med Mal":
        bucket = med_mal
    elif current_product_type == "Staffing":
        bucket = staffing
    elif current_product_type == "MPL":
        bucket = mpl

    return bucket


def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    hxd.cds.rate_change.expiring_policy_option_id.calculated = 129400
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1, max_layers + 1):
        (
            setattr(hxd.cds.rate_change, f"show_layer_{index}", True)
            if index <= num_layers
            else False
        )

    for idx, layer in enumerate(layers):
        # Add renewal premium to table - NOTE: will have to be annualised if policy term is not one year
        layer_quoted_premium = layer.quoted_premium or 0
        layer.rate_change.premium_annualized_100pct.renewal = layer_quoted_premium
        layer.rate_change.premium_annualized_beazley_share.renewal = (
            layer_quoted_premium * (layer.written_line or 0)
        )

        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = (
            layer.rate_change.premium_annualized_100pct.expiring or 0
        )

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in [
            "exposure_change",
            "risk_characteristics_change",
            "deductible_change",
            "limit_change",
            "terms_conditions_change",
            "brokerage_change",
            "other_change",
        ]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)

            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(
                    f"Rate Change: {(title_rc(item))} has been overridden and no comment provided"
                )

        # Calculate final rate change with overrides
        renewal_premium = layer_quoted_premium

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = (
            layer.rate_change.rate_change.uw_selected
        ) = final_rarc

        # Valildation to ensure rate change is completed for bound layers
        if hxd.cds.standard_fields.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in [
                "Bound",
                "Post Bind Complete",
            ]:
                hx.errors.validation(
                    f"Rate change must be completed for bound layer {idx+1}"
                )
        if hxd.cds.standard_fields.is_case_priced:
            if (
                layer.rate_change.risk_adjusted_rate_change_case_priced.uw_selected.selected
                is None
                and layer.status in ["Bound", "Post Bind Complete"]
            ):
                hx.errors.validation(
                    f"Rate change must be completed for bound layer {idx+1}"
                )

    # Validate layer mapping
    current_mapping = {}
    for idx, layer in enumerate(layers):
        current_mapping[str(idx + 1)] = layer.rate_change.expiring_layer

    previous_mapping = (
        json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    )
    if current_mapping != previous_mapping:
        hx.errors.validation(
            "Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change"
        )

        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True

        return  # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        is_bm_different = (
            layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium
        )
        is_quoted_different = (
            layer_quoted_premium != layer.rate_change.temp_storage.quoted_premium
        )

        if is_bm_different and is_quoted_different:
            rc.rarc_run_again_message = "❗ Benchmark and quoted premiums have changed. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break
        elif is_bm_different:
            rc.rarc_run_again_message = f"❗ Benchmark premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break
        elif is_quoted_different:
            rc.rarc_run_again_message = f"❗ Quoted premium has changed on Layer {idx+1}. Run the rate change calculation again ❗"
            rc.rarc_message_show = True
            break

    if is_bm_different or is_quoted_different:
        hx.errors.validation(
            "'Calculate Rate Change' in the Rate Change page must be run again."
        )
