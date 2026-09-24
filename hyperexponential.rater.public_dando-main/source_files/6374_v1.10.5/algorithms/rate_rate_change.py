from __future__ import annotations
import hx
import pandas as pd
import numpy as np
import math as math
import json
from algorithms.rate_utilities import title_rc, ratio, look_up_condition
from operator import itemgetter
from algorithms.rate_constants import max_layers
from algorithms.rate_pricing import calc_pro_rata
from dataclasses import dataclass
from pathlib import Path

def rate_change_buckets(hxd):

    buckets = {
        "model": [], # NOTE: leave this empty - starts from expiry data priced with current model
        "exposure": [
            "cds/exposure/aggregate/market_cap"
        ],
        "risk_characteristics": [
            "hx_core/inception_date",
            "hx_core/expiry_date",
            "cds/exposure/aggregate/ignore_ipo",
            "cds/exposure/aggregate/ipo_date",
        ],
        "deductible": [
            "cds/layers/coverages/abc/excess",
            "cds/layers/coverages/abc/deductible",
            "cds/layers/coverages/side_a/excess",
            "cds/layers/coverages/side_a/deductible",
            "cds/layers/coverages/side_a/tower"
        ],
        "limit": [
            "cds/layers/coverages/abc/limit",
            "cds/layers/coverages/side_a/limit"
        ],
        "terms_conditions": [],
        "brokerage": [],
        "other": [
            "cds/layers/coverages/abc/brokerage",
            "cds/layers/coverages/side_a/brokerage"
        ]
    }

    return buckets

def rate_rate_change(hxd):
    layers = hxd.cds.layers
    agg = hxd.cds.exposure.aggregate
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id

    # Show hide table when policy is rater or private priced 
    is_private = hxd.cds.review_type.private_priced
    is_rater = hxd.cds.review_type.rater_priced
    rc.show_rarc_table = is_private or is_rater

    if is_private or is_rater:
        for idx, layer in enumerate(layers):
            missing_fields = []
 
            if layer.quoted_premium is None:
                missing_fields.append("Gross Quoted Premium")
 
            if is_private:
                if layer.benchmark_premium is None:
                    missing_fields.append("Benchmark Premium")
 
                if layer.technical_premium is None:
                    missing_fields.append("Technical Premium")
 
            if is_rater:
                if layer.benchmark_premium is None:
                    missing_fields.append("Benchmark Premium")
 
            if missing_fields:
                hx.errors.validation(
                    f"Layer {idx + 1}: RC missing "
                    + ", ".join(missing_fields)
                )
    
    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1,max_layers+1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", True) if index <= num_layers else False
    
    for idx, layer in enumerate(layers):  
        # Adding for validation
        if layer.benchmark_premium is not None:
            # Add renewal premium to table - NOTE: annualised when policy term is not one year
            layer.rate_change.premium_policy_term_100pct.renewal = layer.quoted_premium 
            pro_rata = 1 if (hxd.hx_core.inception_date is None) or (hxd.hx_core.expiry_date is None) else calc_pro_rata(hxd.hx_core.inception_date, hxd.hx_core.expiry_date, 2)

            premium_annualized_100pct = (layer.quoted_premium / pro_rata if layer.quoted_premium is not None else 0)
            layer.rate_change.new_premium.gross = premium_annualized_100pct
            layer.rate_change.premium_annualized_100pct.renewal = premium_annualized_100pct
            layer.rate_change.premium_annualized_beazley_share.renewal = (premium_annualized_100pct * (layer.written_line or 0))

            # Add other fields to table
            layer.rate_change.limit.renewal = layer.limit
            layer.rate_change.deductible.renewal = layer.deductible
            layer.rate_change.excess.renewal = layer.excess
            layer.rate_change.side_a_excess.renewal = layer.excess
            layer.rate_change.abc_tower.renewal = layer.coverages.side_a.tower
            layer.rate_change.total_excess.renewal = (layer.excess or 0) + (layer.coverages.side_a.tower or 0)
            layer.rate_change.market_cap.renewal = agg.market_cap
            layer.rate_change.insider_share.renewal = agg.insider_share
            layer.rate_change.revised_market_cap.renewal = agg.revised_market_cap
            layer.rate_change.brokerage.renewal = layer.brokerage

            # if hxd.cds.review_type.rater_priced:
            #     populate_rater_rate_change(hxd, layer, agg, idx)
            # elif hxd.cds.review_type.private_priced:
            #     populate_private_rate_change(hxd, layer, agg, idx)
    
    # ---- RUN CALCULATIONS AFTER ALL DATA IS SET ----
    for idx, layer in enumerate(layers):
        if layer.benchmark_premium is not None:
            if hxd.cds.review_type.rater_priced:
                populate_rater_rate_change(hxd)
            # elif hxd.cds.review_type.private_priced:
            #     populate_private_rate_change(hxd, layer, agg, idx)



    # Validate aggregate expiring exposure fields are consistent across layers
    if len(layers) > 1:
        aggregate_rc_attrs = ["market_cap", "insider_share", "revised_market_cap"]

        inconsistent_attrs = []

        for rc_attr in aggregate_rc_attrs:
            per_layer_values = [getattr(layer.rate_change, rc_attr).expiring.selected for layer in layers]

            if len(set(per_layer_values)) > 1:
                inconsistent_attrs.append(rc_attr.replace("_", " "))

        if inconsistent_attrs:
            pretty_names = ", ".join(inconsistent_attrs)
            hx.errors.validation(f"Rate Change: expiring {pretty_names} must match across all layers before repricing.")

    # Validate layer mapping
    current_mapping = {}
    for idx, layer in enumerate(layers):
        current_mapping[str(idx+1)] = layer.rate_change.expiring_layer

    previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    if current_mapping != previous_mapping:
        hx.errors.validation("Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")

        task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
        rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
        rc.rarc_message_show = True
        
        return # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        is_bm_different = (layer.benchmark_premium != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different = (layer.quoted_premium != layer.rate_change.temp_storage.quoted_premium)

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
        hx.errors.validation("'Calculate Rate Change' in the Rate Change page must be run again.")

# Calculates risk characteristics rate change looking up the ipo lag in a param table
# Done for each sector and then weighted
def calc_ipo_rarc(hxd):
    ind = hxd.cds.key_industry
    agg = hxd.cds.exposure.aggregate
    
    rarc = 1
    if (not agg.ignore_ipo):
        rarc = 0

        sector_ids = [ind.sector_id, ind.sector_id_2, ind.sector_id_3]
        sector_wghts = [
            ind.sic_percentage if ind.sic_percentage else 0, 
            ind.sic_percentage_2 if ind.sic_percentage_2 else 0, 
            ind.sic_percentage_3 if ind.sic_percentage_3 else 0
            ]

        df_ipo_rarc = hx.params.ref_ipo_lag

        ipo_max = max(df_ipo_rarc["Lag"])  
        ipo_lag = calc_pro_rata(agg.ipo_date, hxd.hx_core.inception_date, 2) * 360
        ipo_lag = min(math.floor(ipo_lag / 360), ipo_max) 

        for i, sector in enumerate(sector_ids):
            if (not ind.blended_sic) and (i > 0):
                break
            
            if sector_wghts[i] > 0 and sector is not None:
                ipo_sector = 1 if sector == 1 else 0
                change = look_up_condition((df_ipo_rarc["Lag"] == ipo_lag) & (df_ipo_rarc["Sector"] == ipo_sector),
                    "Reduction to apply in RC",
                    df_ipo_rarc,
                    0
                )
                rarc += change * sector_wghts[i]

        rarc = 1 if rarc == 0 else rarc

    return rarc   


def populate_rater_rate_change(hxd):
    agg = hxd.cds.exposure.aggregate
    layers = hxd.cds.layers
    for idx, layer in enumerate(layers):
        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = layer.rate_change.premium_annualized_100pct.expiring.selected or 0

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "brokerage_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)

            # # Change in IPO is handelled separately by looking up the ipo lag in a table
            # # These values are different than just recalculating tech premium with additional year out from the IPO
            # if item == "risk_characteristics_change":
            #     rc_vbl.model_calculated = calc_ipo_rarc(hxd)

            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            # if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
            #     hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        #renewal_premium = layer.quoted_premium
        # TODO: review if this change is correct
        renewal_premium = layer.rate_change.premium_annualized_100pct.renewal

        if renewal_premium is None or rebased_premium_model is None:
            layer.rate_change.rate_change.model_calculated = None
            layer.rate_change.risk_adjusted_rate_change.uw_selected = None
            layer.rate_change.rate_change.uw_selected = None
            layer.rate_change.new_calculated_premium.uw_selected = None
            continue
        

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = layer.rate_change.rate_change.uw_selected = final_rarc
        layer.rate_change.new_calculated_premium.uw_selected = rebased_premium_uw

        # Valildation to ensure rate change is completed for bound layers
        if hxd.cds.standard_fields.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
        if hxd.cds.standard_fields.is_case_priced:
            if layer.rate_change.risk_adjusted_rate_change_case_priced.uw_selected.selected is None and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

        # Making some fields uneditable
        layer.rate_change.exposure_change_fixed.model_calculated = layer.rate_change.exposure_change_fixed.uw_selected = layer.rate_change.exposure_change.model_calculated
        layer.rate_change.deductible_change_fixed.model_calculated = layer.rate_change.deductible_change_fixed.uw_selected = layer.rate_change.deductible_change.model_calculated
        layer.rate_change.limit_change_fixed.model_calculated = layer.rate_change.limit_change_fixed.uw_selected = layer.rate_change.limit_change.model_calculated
        layer.rate_change.excess_change_fixed.model_calculated = layer.rate_change.excess_change_fixed.uw_selected = layer.rate_change.excess_change.model_calculated
        layer.rate_change.brokerage_change_fixed.model_calculated = layer.rate_change.brokerage_change_fixed.uw_selected = layer.rate_change.brokerage_change.model_calculated
        layer.rate_change.other_change_fixed.model_calculated = layer.rate_change.other_change_fixed.uw_selected = layer.rate_change.other_change.model_calculated

def compute_private_rate_change(hxd):
    """
    Async task:
    - calculates all private D&O RC factors
    - stores them in layer.rate_change.private_rc_result
    - writes only task-enabled model_calculated fields
    - treats Other Change as brokerage RC
    """

    agg = hxd.cds.exposure.aggregate

    table_base_rate = hx.params.table_pcl_base_rate_ranges_cw
    table_ret_factors = hx.params.table_pcl_retention_factors_cw
    table_clrf = hx.params.table_pcl_combined_limit_retention_factor

    def lookup_factor(min_col, max_col, x, table, value_col):
        t = table.sort_values(min_col).reset_index(drop=True)
        idxs = t.index[(t[min_col] <= x) & (x <= t[max_col])]
        if len(idxs) == 0:
            return None

        i = idxs[0]
        value = t.loc[i, value_col]

        if not isinstance(value, (int, float, np.number)):
            return value

        if i == len(t) - 1:
            return value

        next_value = t.loc[i + 1, value_col]
        if not isinstance(next_value, (int, float, np.number)):
            return value

        x1 = (t.loc[i, min_col] + t.loc[i, max_col]) / 2
        x2 = (t.loc[i + 1, min_col] + t.loc[i + 1, max_col]) / 2

        if x2 == x1:
            return value

        weight = (x - x1) / (x2 - x1)
        return value + weight * (next_value - value)

    def lookup_ilf(limit_value, table):
        exact = table.loc[table["Limit"] == limit_value, "Factor"]
        if not exact.empty:
            return exact.iloc[0]

        below = table[table["Limit"] < limit_value].tail(1)
        above = table[table["Limit"] > limit_value].head(1)

        if below.empty and above.empty:
            return None
        if below.empty:
            return above["Factor"].iloc[0]
        if above.empty:
            return below["Factor"].iloc[0]

        lo_limit, lo_factor = below.iloc[0][["Limit", "Factor"]]
        hi_limit, hi_factor = above.iloc[0][["Limit", "Factor"]]
        weight = (limit_value - lo_limit) / (hi_limit - lo_limit)

        return lo_factor + weight * (hi_factor - lo_factor)

    for idx, layer in enumerate(hxd.cds.layers):

        # -----------------------------
        # Exposure / Asset RC
        # -----------------------------
        exp_assets = layer.rate_change.asset_size.private_priced
        ren_assets = agg.total_assets

        if exp_assets is None or ren_assets is None:
            asset_rc = None
        elif exp_assets == ren_assets:
            asset_rc = 1
        else:
            exp_asset_factor = lookup_factor("Min", "Max", exp_assets, table_base_rate, "Base Premium")
            ren_asset_factor = lookup_factor("Min", "Max", ren_assets, table_base_rate, "Base Premium")
            asset_rc = ren_asset_factor / exp_asset_factor if exp_asset_factor not in (None, 0) else None

        # -----------------------------
        # Limit RC
        # -----------------------------
        exp_limit = layer.rate_change.limit.private_priced
        ren_limit = layer.rate_change.limit.renewal
        retention_for_limit = layer.rate_change.deductible.private_priced or 0

        if exp_limit is None or ren_limit is None:
            limit_rc = None
        elif exp_limit == ren_limit:
            limit_rc = 1
        else:
            exp_lim_retention = exp_limit + retention_for_limit
            ren_lim_retention = ren_limit + retention_for_limit

            exp_limit_factor = lookup_ilf(exp_lim_retention, table_clrf)
            ren_limit_factor = lookup_ilf(ren_lim_retention, table_clrf)

            limit_rc = (
                ren_limit_factor / exp_limit_factor
                if exp_limit_factor not in (None, 0) and ren_limit_factor not in (None, 0)
                else None
            )

        # -----------------------------
        # Excess RC
        # -----------------------------
        if hxd.cds.coverage == "Side A":
            exp_excess = layer.rate_change.total_excess.private_priced or 0
            ren_excess = layer.rate_change.total_excess.renewal or 0
        else:
            exp_excess = layer.rate_change.excess.private_priced
            ren_excess = layer.rate_change.excess.renewal

        exp_retention = layer.rate_change.deductible.private_priced or 0
        exp_limit_for_excess = layer.rate_change.limit.private_priced or 0

        if exp_excess is None or ren_excess is None:
            excess_rc = None
        elif exp_excess == ren_excess:
            excess_rc = 1
        else:
            base_attachment = exp_retention + exp_limit_for_excess
            exp_top = base_attachment + exp_excess
            ren_top = base_attachment + ren_excess

            exp_base_factor = lookup_ilf(base_attachment, table_clrf)
            exp_top_factor = lookup_ilf(exp_top, table_clrf)
            ren_top_factor = lookup_ilf(ren_top, table_clrf)

            if None in (exp_base_factor, exp_top_factor, ren_top_factor):
                excess_rc = None
            else:
                exp_excess_factor = exp_top_factor - exp_base_factor
                ren_excess_factor = ren_top_factor - exp_base_factor

                excess_rc = (
                    ren_excess_factor / exp_excess_factor
                    if exp_excess_factor not in (None, 0) and ren_excess_factor not in (None, 0)
                    else None
                )

        # -----------------------------
        # Deductible / Retention RC
        # -----------------------------
        asset_class = lookup_factor(
            "Min",
            "Max",
            agg.total_assets,
            table_base_rate,
            "Asset Size Category Description"
        )

        exp_retention = layer.rate_change.deductible.private_priced
        ren_retention = layer.rate_change.deductible.renewal

        def normalize_retention_factor(raw_factor, retention):
            """
            Treat 0 retention as no deductible credit, i.e. factor = 1.0.
            This avoids a 0 table value driving the rate change to 0%.
            """
            if retention is None:
                return None

            if retention == 0:
                return 1.0

            if raw_factor in (None, 0):
                return None

            return raw_factor

        if exp_retention is None or ren_retention is None:
            deductible_rc = None
        elif exp_retention == ren_retention:
            deductible_rc = 1
        else:
            exp_retention_factor_raw = lookup_factor(
                "Retention - Low",
                "Retention - High",
                exp_retention,
                table_ret_factors,
                asset_class
            )

            ren_retention_factor_raw = lookup_factor(
                "Retention - Low",
                "Retention - High",
                ren_retention,
                table_ret_factors,
                asset_class
            )

            exp_retention_factor = normalize_retention_factor(
                exp_retention_factor_raw,
                exp_retention
            )

            ren_retention_factor = normalize_retention_factor(
                ren_retention_factor_raw,
                ren_retention
            )

            deductible_rc = (
                ren_retention_factor / exp_retention_factor
                if exp_retention_factor not in (None, 0)
                and ren_retention_factor is not None
                else None
            )


        # -----------------------------
        # Brokerage RC -> Other RC
        # -----------------------------
        exp_brokerage = (
            layer.rate_change.brokerage.private_priced
            if layer.rate_change.brokerage.private_priced is not None
            else 0
        )

        # Read renewal brokerage directly from pricing coverage, not rate_change/brokerage/renewal
        if hxd.cds.coverage == "Side A":
            ren_brokerage = layer.coverages.side_a.brokerage if layer.coverages.side_a.brokerage is not None else 0
        else:
            ren_brokerage = layer.coverages.abc.brokerage if layer.coverages.abc.brokerage is not None else 0

        if exp_brokerage == ren_brokerage:
            brokerage_rc = 1
        else:
            denom = 1 - exp_brokerage
            brokerage_rc = ((1 - ren_brokerage) / denom) if denom not in (None, 0) else None

        # For this rater, Other Change is brokerage change
        other_rc = brokerage_rc

        # -----------------------------
        # Defaults
        # -----------------------------
        risk_characteristics_rc = 1
        terms_conditions_rc = 1

        # -----------------------------
        # Total RC
        # Do NOT include brokerage_rc separately since other_rc already equals brokerage_rc
        # -----------------------------
        factors = [
            asset_rc,
            risk_characteristics_rc,
            deductible_rc,
            limit_rc,
            excess_rc,
            terms_conditions_rc,
            other_rc,
        ]

        total_rc = None if any(f is None for f in factors) else float(np.prod(factors))

        # -----------------------------
        # Store in private_rc_result
        # -----------------------------
        slot = layer.rate_change.private_rc_result
        slot.layer_index = idx
        slot.asset_rc = asset_rc
        slot.limit_rc = limit_rc
        slot.excess_rc = excess_rc
        slot.deductible_rc = deductible_rc
        slot.risk_characteristics_rc = risk_characteristics_rc
        slot.terms_conditions_rc = terms_conditions_rc
        slot.brokerage_rc = brokerage_rc
        slot.other_rc = other_rc
        slot.total_rc = total_rc

        # -----------------------------
        # Write only task-enabled model_calculated fields
        # Do NOT write excess_change.model_calculated here
        # Do NOT write brokerage_change here because brokerage is included in other
        # -----------------------------
        layer.rate_change.exposure_change.model_calculated = asset_rc
        layer.rate_change.risk_characteristics_change.model_calculated = risk_characteristics_rc
        layer.rate_change.deductible_change.model_calculated = deductible_rc
        layer.rate_change.limit_change.model_calculated = limit_rc
        layer.rate_change.terms_conditions_change.model_calculated = terms_conditions_rc
        layer.rate_change.other_change.model_calculated = other_rc

def constant_private_rate_change(hxd):
    """
    Normal rating-path publisher for private D&O RC.

    Reads layer.rate_change.private_rc_result and:
      1) sets uw_selected.calculated on RC nodes
      2) populates _fixed nodes
      3) calculates final rebased premium + total RARC outputs

    Other Change includes brokerage for this rater.
    """

    rc_map_keys = {
        "exposure_change": "asset_rc",
        "risk_characteristics_change": "risk_characteristics_rc",
        "deductible_change": "deductible_rc",
        "limit_change": "limit_rc",
        "excess_change": "excess_rc",
        "terms_conditions_change": "terms_conditions_rc",
        "other_change": "other_rc",
    }

    for idx, layer in enumerate(hxd.cds.layers):
        results = layer.rate_change.private_rc_result

        # -----------------------------
        # Push staged values into visible/private RC structures
        # -----------------------------
        for rc_key, result_attr in rc_map_keys.items():
            rc_value = getattr(results, result_attr)
            rc_obj = getattr(layer.rate_change, rc_key)

            # Set calculated value on override node
            rc_obj.uw_selected.calculated = rc_value

            # Populate _fixed display node if it exists
            fixed_name = f"{rc_key}_fixed"
            if hasattr(layer.rate_change, fixed_name):
                fixed_obj = getattr(layer.rate_change, fixed_name)
                fixed_obj.model_calculated = rc_value

                if hasattr(fixed_obj, "uw_selected"):
                    fixed_obj.uw_selected = rc_value

        # -----------------------------
        # Final private rate change outputs
        # -----------------------------
        base_premium = layer.rate_change.premium_annualized_100pct.private_priced
        renewal_premium = layer.rate_change.premium_annualized_100pct.renewal

        if base_premium is None or renewal_premium is None:
            layer.rate_change.rate_change.model_calculated = None
            layer.rate_change.rate_change.uw_selected = None
            layer.rate_change.risk_adjusted_rate_change.technical = None
            layer.rate_change.risk_adjusted_rate_change.uw_selected = None
            layer.rate_change.new_calculated_premium.technical = None
            layer.rate_change.new_calculated_premium.uw_selected = None
            continue

        rebased_model = base_premium
        rebased_uw = base_premium
        factors_complete = True

        for rc_key, result_attr in rc_map_keys.items():
            rc_value = getattr(results, result_attr)
            rc_obj = getattr(layer.rate_change, rc_key)

            model_factor = rc_value

            uw_factor = (
                rc_obj.uw_selected.selected
                if rc_obj.uw_selected.selected is not None
                else rc_obj.uw_selected.calculated
            )

            if model_factor is None or uw_factor is None:
                factors_complete = False
                break

            rebased_model *= model_factor
            rebased_uw *= uw_factor

        if not factors_complete:
            layer.rate_change.rate_change.model_calculated = None
            layer.rate_change.rate_change.uw_selected = None
            layer.rate_change.risk_adjusted_rate_change.technical = None
            layer.rate_change.risk_adjusted_rate_change.uw_selected = None
            layer.rate_change.new_calculated_premium.technical = None
            layer.rate_change.new_calculated_premium.uw_selected = None
            continue

        model_rarc = ratio(renewal_premium, rebased_model, 1)
        uw_rarc = ratio(renewal_premium, rebased_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.rate_change.uw_selected = uw_rarc
        layer.rate_change.risk_adjusted_rate_change.technical = model_rarc
        layer.rate_change.risk_adjusted_rate_change.uw_selected = uw_rarc
        layer.rate_change.new_calculated_premium.technical = rebased_model
        layer.rate_change.new_calculated_premium.uw_selected = rebased_uw
