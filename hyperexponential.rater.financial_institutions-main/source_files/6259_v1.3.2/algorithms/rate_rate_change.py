import json

import hx

from algorithms.rate_constants import max_layers
from algorithms.rate_utilities import get_layer_idx_from_label, ratio, title_rc


def rate_change_buckets():
    buckets = {
        "model": [
            {"node": "cds/layers/tower_1/excess", "override": True, "source_from_expiring": True},
            {"node": "cds/layers/tower_2/excess", "override": True, "source_from_expiring": True},
            {"node": "cds/layers/tower_3/excess", "override": True, "source_from_expiring": True},
            {"node": "cds/layers/tower_4/excess", "override": True, "source_from_expiring": True},
            {"node": "cds/layers/tower_5/excess", "override": True, "source_from_expiring": True},
            {"node": "cds/layers/tower_6/excess", "override": True, "source_from_expiring": True},
        ], # Excess is calculated in rating and dependant on layer order, but want them to be independant for rate change, so move these to the override fields
        "exposure": [
            "cds/key_industry/code_name",
            "cds/rating_factors/risk_info/sub_industry",

            "cds/standard_fields/insured_country",
            "cds/rating_factors/risk_info/region",

            "cds/rating_factors/exposure_details/currency",
            "cds/rating_factors/exposure_details/us_listing",

            "cds/exposure/aggregate/market_cap",
            "cds/exposure/aggregate/market_cap_us",

            "cds/exposure/aggregate/total_amounts/employees",
            "cds/exposure/aggregate/total_amounts/revenues",
            "cds/exposure/aggregate/total_amounts/assets",
            "cds/exposure/aggregate/total_amounts/aum",

            "cds/exposure/granular/regions/splits_entered_as/employees",
            "cds/exposure/granular/regions/splits_entered_as/revenues",
            "cds/exposure/granular/regions/splits_entered_as/assets",

            "cds/exposure/granular/regions/regions_list/africa/value/employees",
            "cds/exposure/granular/regions/regions_list/africa/value/revenues",
            "cds/exposure/granular/regions/regions_list/africa/value/assets",
            "cds/exposure/granular/regions/regions_list/arab_states/value/employees",
            "cds/exposure/granular/regions/regions_list/arab_states/value/revenues",
            "cds/exposure/granular/regions/regions_list/arab_states/value/assets",
            "cds/exposure/granular/regions/regions_list/asia/value/employees",
            "cds/exposure/granular/regions/regions_list/asia/value/revenues",
            "cds/exposure/granular/regions/regions_list/asia/value/assets",
            "cds/exposure/granular/regions/regions_list/oceania/value/employees",
            "cds/exposure/granular/regions/regions_list/oceania/value/revenues",
            "cds/exposure/granular/regions/regions_list/oceania/value/assets",
            "cds/exposure/granular/regions/regions_list/europe/value/employees",
            "cds/exposure/granular/regions/regions_list/europe/value/revenues",
            "cds/exposure/granular/regions/regions_list/europe/value/assets",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/value/employees",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/value/revenues",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/value/assets",
            "cds/exposure/granular/regions/regions_list/usa/value/employees",
            "cds/exposure/granular/regions/regions_list/usa/value/revenues",
            "cds/exposure/granular/regions/regions_list/usa/value/assets",
            "cds/exposure/granular/regions/regions_list/canada/value/employees",
            "cds/exposure/granular/regions/regions_list/canada/value/revenues",
            "cds/exposure/granular/regions/regions_list/canada/value/assets",
            "cds/exposure/granular/regions/regions_list/south_latin_america/value/employees",
            "cds/exposure/granular/regions/regions_list/south_latin_america/value/revenues",
            "cds/exposure/granular/regions/regions_list/south_latin_america/value/assets",
            "cds/exposure/granular/regions/regions_list/caribbean/value/employees",
            "cds/exposure/granular/regions/regions_list/caribbean/value/revenues",
            "cds/exposure/granular/regions/regions_list/caribbean/value/assets",
            "cds/exposure/granular/regions/regions_list/row/value/employees",
            "cds/exposure/granular/regions/regions_list/row/value/revenues",
            "cds/exposure/granular/regions/regions_list/row/value/assets",

            "cds/exposure/granular/regions/regions_list/africa/percent/employees",
            "cds/exposure/granular/regions/regions_list/africa/percent/revenues",
            "cds/exposure/granular/regions/regions_list/africa/percent/assets",
            "cds/exposure/granular/regions/regions_list/arab_states/percent/employees",
            "cds/exposure/granular/regions/regions_list/arab_states/percent/revenues",
            "cds/exposure/granular/regions/regions_list/arab_states/percent/assets",
            "cds/exposure/granular/regions/regions_list/asia/percent/employees",
            "cds/exposure/granular/regions/regions_list/asia/percent/revenues",
            "cds/exposure/granular/regions/regions_list/asia/percent/assets",
            "cds/exposure/granular/regions/regions_list/oceania/percent/employees",
            "cds/exposure/granular/regions/regions_list/oceania/percent/revenues",
            "cds/exposure/granular/regions/regions_list/oceania/percent/assets",
            "cds/exposure/granular/regions/regions_list/europe/percent/employees",
            "cds/exposure/granular/regions/regions_list/europe/percent/revenues",
            "cds/exposure/granular/regions/regions_list/europe/percent/assets",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/percent/employees",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/percent/revenues",
            "cds/exposure/granular/regions/regions_list/former_soviet_republics/percent/assets",
            "cds/exposure/granular/regions/regions_list/usa/percent/employees",
            "cds/exposure/granular/regions/regions_list/usa/percent/revenues",
            "cds/exposure/granular/regions/regions_list/usa/percent/assets",
            "cds/exposure/granular/regions/regions_list/canada/percent/employees",
            "cds/exposure/granular/regions/regions_list/canada/percent/revenues",
            "cds/exposure/granular/regions/regions_list/canada/percent/assets",
            "cds/exposure/granular/regions/regions_list/south_latin_america/percent/employees",
            "cds/exposure/granular/regions/regions_list/south_latin_america/percent/revenues",
            "cds/exposure/granular/regions/regions_list/south_latin_america/percent/assets",
            "cds/exposure/granular/regions/regions_list/caribbean/percent/employees",
            "cds/exposure/granular/regions/regions_list/caribbean/percent/revenues",
            "cds/exposure/granular/regions/regions_list/caribbean/percent/assets",
            "cds/exposure/granular/regions/regions_list/row/percent/employees",
            "cds/exposure/granular/regions/regions_list/row/percent/revenues",
            "cds/exposure/granular/regions/regions_list/row/percent/assets",

            "cds/exposure/granular/investor_split_type/institutional/percent",
            "cds/exposure/granular/investor_split_type/retail/percent",
            "cds/exposure/granular/investor_split_type/other/percent",

            "cds/exposure/granular/investor_split_region/region_1/region",
            "cds/exposure/granular/investor_split_region/region_1/percent",
            "cds/exposure/granular/investor_split_region/region_2/region",
            "cds/exposure/granular/investor_split_region/region_2/percent",
            "cds/exposure/granular/investor_split_region/region_3/region",
            "cds/exposure/granular/investor_split_region/region_3/percent",

            "cds/exposure/granular/revenue_split_banks/interest/amount",
            "cds/exposure/granular/revenue_split_banks/fee/amount",
            "cds/exposure/granular/revenue_split_banks/trading/amount",
            "cds/exposure/granular/revenue_split_banks/other/amount",

            "cds/exposure/granular/premium_split/life/amount",
            "cds/exposure/granular/premium_split/pc/amount",
            "cds/exposure/granular/premium_split/personal/amount",
            "cds/exposure/granular/premium_split/commercial/amount",
            "cds/exposure/granular/premium_split/healthcare/amount",
            "cds/exposure/granular/premium_split/ripc/amount",
            "cds/exposure/granular/premium_split/other/amount",

            "cds/exposure/granular/revenue_split_brokers/institutional_advisory/amount",
            "cds/exposure/granular/revenue_split_brokers/institutional_execution/amount",
            "cds/exposure/granular/revenue_split_brokers/retail_advisory/amount",
            "cds/exposure/granular/revenue_split_brokers/retail_execution/amount",
            "cds/exposure/granular/revenue_split_brokers/retail_discretionary/amount",
            "cds/exposure/granular/revenue_split_brokers/other/amount",

            "cds/exposure/granular/revenue_split_exchanges/exchange/amount",
            "cds/exposure/granular/revenue_split_exchanges/listing/amount",
            "cds/exposure/granular/revenue_split_exchanges/clear_settlement/amount",
            "cds/exposure/granular/revenue_split_exchanges/depositary/amount",
            "cds/exposure/granular/revenue_split_exchanges/other/amount",

            "cds/exposure/granular/revenue_split_admin/est_companies/amount",
            "cds/exposure/granular/revenue_split_admin/est_trusts/amount",
            "cds/exposure/granular/revenue_split_admin/outside_board/amount",
            "cds/exposure/granular/revenue_split_admin/legal_advice/amount",
            "cds/exposure/granular/revenue_split_admin/accountancy/amount",
            "cds/exposure/granular/revenue_split_admin/tax/amount",
            "cds/exposure/granular/revenue_split_admin/other/amount",
        ],
        "risk_characteristics": [
            "cds/rating_factors/risk_info/ownership_type",
            "cds/modifiers/risk_category/policy_wording",
            "cds/modifiers/risk_category/claims_history_cpi",
            "cds/modifiers/risk_category/claims_history_do",
            "cds/modifiers/risk_category/risk_management",
            "cds/modifiers/risk_category/strength_of_financial",
            "cds/modifiers/risk_category/technological_infrastructure",
            "cds/modifiers/risk_category/quality_of_control",
            "cds/modifiers/risk_category/agents_as_employees",
            "cds/modifiers/risk_category/regulatory_risk",
            "cds/modifiers/risk_category/quality_of_claims_handling",
            "cds/modifiers/risk_category/product_complexity",
            "cds/modifiers/risk_category/quality_of_bcp",
            "cds/modifiers/risk_category/market_regulator",
            "cds/modifiers/risk_category/extent_of_leveraged_gearing",
            "cds/modifiers/risk_category/quality_of_performance_non_pevc",
            "cds/modifiers/risk_category/redemption_gates",
            "cds/modifiers/risk_category/valuation_for_pevc",
            "cds/modifiers/risk_category/loan_covenant",
            "cds/modifiers/risk_category/dando_portfolio_companies",
            "cds/modifiers/risk_category/data_centre",
            "cds/modifiers/risk_category/tech_outsourcing",
            "cds/modifiers/risk_category/difference_in_conditions",
            "cds/modifiers/risk_category/uw_adj",
        ],
        "deductible": [
            "cds/rating_factors/cover_details/primary_layer/sir_all_manager/crime",
            "cds/rating_factors/cover_details/primary_layer/sir_all_manager/pi",
            "cds/rating_factors/cover_details/primary_layer/sir_all_manager/do",
            "cds/rating_factors/cover_details/primary_layer/sir_all_manager/do_side_c",
            "cds/rating_factors/cover_details/primary_layer/sir_fund/crime",
            "cds/rating_factors/cover_details/primary_layer/sir_fund/pi",
            "cds/rating_factors/cover_details/primary_layer/sir_fund/do",
            "cds/rating_factors/cover_details/primary_layer/sir_fund/do_side_c",
            {"node": "cds/layers/tower_1/excess", "override": True},
            {"node": "cds/layers/tower_2/excess", "override": True},
            {"node": "cds/layers/tower_3/excess", "override": True},
            {"node": "cds/layers/tower_4/excess", "override": True},
            {"node": "cds/layers/tower_5/excess", "override": True},
            {"node": "cds/layers/tower_6/excess", "override": True},
        ],
        "limit": [
            "cds/rating_factors/cover_details/sublimits_req",
            "cds/rating_factors/cover_details/details_reinstatements",
            "cds/rating_factors/cover_details/reinst_rtc_program_limit",
            "cds/rating_factors/cover_details/no_direct_reinstatements",

            "cds/layers/tower_1/limit",
            "cds/layers/tower_2/limit",
            "cds/layers/tower_3/limit",
            "cds/layers/tower_4/limit",
            "cds/layers/tower_5/limit",
            "cds/layers/tower_6/limit",

            "cds/layers/tower_1/direct_reinstatements",
            "cds/layers/tower_2/direct_reinstatements",
            "cds/layers/tower_3/direct_reinstatements",
            "cds/layers/tower_4/direct_reinstatements",
            "cds/layers/tower_5/direct_reinstatements",
            "cds/layers/tower_6/direct_reinstatements",

            "cds/layers/tower_1/rtc_reinstatements",
            "cds/layers/tower_2/rtc_reinstatements",
            "cds/layers/tower_3/rtc_reinstatements",
            "cds/layers/tower_4/rtc_reinstatements",
            "cds/layers/tower_5/rtc_reinstatements",
            "cds/layers/tower_6/rtc_reinstatements",

            "cds/layers/coverages/crime/all_manager/sublimit",
            "cds/layers/coverages/pi/all_manager/sublimit",
            "cds/layers/coverages/do/all_manager/sublimit",
            "cds/layers/coverages/crime/fund/sublimit",
            "cds/layers/coverages/pi/fund/sublimit",
            "cds/layers/coverages/do/fund/sublimit",
        ],
        "terms_conditions": [
            "hx_core/inception_date",
            "hx_core/expiry_date",

            "cds/rating_factors/risk_info/crime_coverage_required",
            "cds/rating_factors/risk_info/pi_coverage_required",
            "cds/rating_factors/risk_info/do_coverage_required",

            "cds/rating_factors/cover_details/crime_retroactive_date",
            "cds/rating_factors/cover_details/pi_retroactive_date",
            "cds/rating_factors/cover_details/do_retroactive_date",

            "cds/rating_factors/cover_details/primary_layer/do_type",
            "cds/rating_factors/cover_details/primary_layer/towers_all_manager/crime",
            "cds/rating_factors/cover_details/primary_layer/towers_all_manager/pi",
            "cds/rating_factors/cover_details/primary_layer/towers_all_manager/do",
            "cds/rating_factors/cover_details/primary_layer/towers_fund/crime",
            "cds/rating_factors/cover_details/primary_layer/towers_fund/pi",
            "cds/rating_factors/cover_details/primary_layer/towers_fund/do",

            "cds/rating_factors/cover_details/premium_split_all_layers/crime",
            "cds/rating_factors/cover_details/premium_split_all_layers/pi",
            "cds/rating_factors/cover_details/premium_split_all_layers/do",

            "cds/layers/coverages/crime/premium_split",
            "cds/layers/coverages/pi/premium_split",
            "cds/layers/coverages/do/premium_split",
        ],
        "other": [
            'cds/rating_factors/cover_details/brokerage_all_layers/brk',
            'cds/layers/brokerage',
            'cds/risk_info/currency',
            'cds/rating_factors/cover_details/brokerage_all_layers/ncb',
            'cds/rating_factors/cover_details/brokerage_all_layers/lta',
            'cds/layers/ncb',
            'cds/layers/lta',
        ]
    }

    return buckets


def rate_rate_change(hxd):
    layers = hxd.cds.layers
    rc = hxd.cds.rate_change
    rc.expiring_policy_option_id.calculated = hx.meta.expiring_policy_option_id
    sf = hxd.cds.standard_fields

    # For layers not used in the pricing summary, the rate change is hidden
    num_layers = len(layers)
    for index in range(1, max_layers + 1):
        setattr(hxd.cds.rate_change, f"show_layer_{index}", index <= num_layers)

    for idx, layer in enumerate(layers):
        rc_prem = layer.rate_change.premium
        # Add renewal premium to table - NOTE: this assumes 'quoted_premium' is annualised
        rc_prem.line_100pct.annualised.renewal = layer.quoted_premium_annualised or 0
        rc_prem.beazley_line.annualised.renewal = (layer.quoted_premium_annualised or 0) * (layer.written_line or 0)
        
        # Calculate change for each bucket
        rebased_premium_model = rebased_premium_uw = rc_prem.line_100pct.annualised.expiring or 0

        # Initialise list to check all changes are filled in
        rate_changes = []

        for item in ["exposure_change", "risk_characteristics_change", "deductible_change", "limit_change", "terms_conditions_change", "other_change"]:
            # Calculate rebased premium based on % changes
            rc_vbl = getattr(layer.rate_change, item)
            rc_vbl.uw_selected.calculated = rc_vbl.model_calculated
            rebased_premium_model *= rc_vbl.model_calculated or 0
            rebased_premium_uw *= rc_vbl.uw_selected.selected or 0

            # Add selected change to list
            rate_changes.append(rc_vbl.uw_selected.selected)
            
            # Validate overrides if unexplained
            if rc_vbl.uw_selected.is_overridden is True and rc_vbl.comments is None:
                hx.errors.validation(f"Rate Change: {(title_rc(item))} has been overridden and no comment provided")

        # Calculate final rate change with overrides
        renewal_premium = layer.quoted_premium_annualised or 0

        model_rarc = ratio(renewal_premium, rebased_premium_model, 1)
        final_rarc = ratio(renewal_premium, rebased_premium_uw, 1)

        layer.rate_change.rate_change.model_calculated = model_rarc
        layer.rate_change.risk_adjusted_rate_change = layer.rate_change.rate_change.uw_selected = final_rarc

        # For PMD reporting
        brokerage_change = layer.rate_change.brokerage_change.model_calculated or 1
        layer.rate_change.risk_adjusted_rate_change_gross_for_reporting = final_rarc * brokerage_change

        # Valildation to ensure rate change is completed for bound layers
        if sf.is_rater_priced:
            if any(change is None for change in rate_changes) and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")
        if sf.is_case_priced:
            if layer.rate_change.risk_adjusted_rate_change_case_priced is None and layer.status in ["Bound", "Post Bind Complete"]:
                hx.errors.validation(f"Rate change must be completed for bound layer {idx+1}")

    # # Validate layer mapping
    # current_mapping = {}
    # for idx, layer in enumerate(layers):
    #     current_mapping[str(idx+1)] = get_layer_idx_from_label(layer.rate_change.expiring_layer_label) + 1

    # previous_mapping = json.loads(rc.layer_mapping) if rc.layer_mapping else current_mapping
    # if current_mapping != previous_mapping:
    #     hx.errors.validation("Mapping of Expiring Layers to Renewal Layers is inconsistent with numbers shown in Rate Change")

    #     task = "'Calculate Rate Change'" if rc.has_rarc_run else "'Fetch Expiring Data'"
    #     rc.rarc_run_again_message = f"❗ Mapping of Expiring Layers to Renewal Layers has changed. Run {task} again ❗"
    #     rc.rarc_message_show = True
        
    #     return  # Do not validate any further until the task is run again

    # Validate premiums
    if not rc.has_rarc_run:
        return

    for idx, layer in enumerate(layers):
        # Here we compare the annualised benchmark and quoted premiums, the temp storage premiums are already annualised
        is_bm_different = (layer.benchmark_premium_annualised_100 != layer.rate_change.temp_storage.benchmark_premium)
        is_quoted_different = (layer.quoted_premium_annualised != layer.rate_change.temp_storage.quoted_premium)

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
