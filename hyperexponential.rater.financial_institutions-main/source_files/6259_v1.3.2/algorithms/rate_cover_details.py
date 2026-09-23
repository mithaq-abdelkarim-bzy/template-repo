import hx

from algorithms.rate_constants import coverages, max_towers
from algorithms.rate_risk_information import get_coverage_matrix, get_industry_matrix


def rate_cover_details(hxd):
    coverage = get_coverage_matrix(hxd)
    industry = get_industry_matrix(hxd)

    # Show/hide fields
    hxd.non_cds.cover_details.all_manager_show = not industry["is_inv"]
    hxd.non_cds.cover_details.fund_show = industry["is_inv"]
    hxd.non_cds.cover_details.do_side_a_show = coverage["is_do"] and hxd.cds.rating_factors.cover_details.primary_layer.do_type == "A"
    hxd.non_cds.cover_details.do_side_b_show = coverage["is_do"] and hxd.cds.rating_factors.cover_details.primary_layer.do_type in ("ABC", "AB")
    hxd.non_cds.cover_details.do_side_c_show = coverage["is_do"] and hxd.cds.rating_factors.cover_details.primary_layer.do_type == "ABC"
    hxd.non_cds.cover_details.rtc_limit_show = hxd.cds.rating_factors.cover_details.details_reinstatements == "Round the clock"
    hxd.non_cds.cover_details.direct_reinstatements_show = hxd.cds.rating_factors.cover_details.details_reinstatements == "Direct"
    hxd.non_cds.cover_details.premium_split_show = any((hxd.non_cds.risk_info.is_coverage_required, hxd.cds.risk_info.eea_non_eea_indicator))
    hxd.non_cds.cover_details.premium_split_coverages_show = all((hxd.non_cds.risk_info.is_coverage_required, hxd.non_cds.cover_details.is_premium_split_all_layers))

    # Validations
    if hxd.non_cds.cover_details.rtc_limit_show and not hxd.cds.rating_factors.cover_details.reinst_rtc_program_limit:
        hx.errors.validation("- Total Program Limit for RTC must be entered")

    # Rating summary towers show/hide
    selected_towers = set()
    for c, _ in coverages:
        if coverage[f"is_{c}"]:
            tower_manager = getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_all_manager, c)
            if tower_manager != "NA":
                selected_towers.add(int(tower_manager[-1]))  # only add the tower number
            tower_fund = getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_fund, c)
            if tower_fund != "NA":
                selected_towers.add(int(tower_fund[-1]))  # only add the tower number
    for tower_idx in range(1, max_towers+1):
        setattr(hxd.non_cds.cover_details, f"tower_{tower_idx}_show", tower_idx in selected_towers)

    hxd.non_cds.cover_details.show_different_towers_manager_fund_warning = False
    # Towers Manager/Fund Validation
    if hxd.non_cds.cover_details.fund_show:
        for c, _ in coverages:
            t_manager = getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_all_manager, c)
            t_fund = getattr(hxd.cds.rating_factors.cover_details.primary_layer.towers_fund, c)
            if t_manager != t_fund and t_manager != "NA" and t_fund != "NA" and coverage[f"is_{c}"]:
                hxd.non_cds.cover_details.show_different_towers_manager_fund_warning = True

    # Number of Layers
    if not 1 <= hxd.non_cds.cover_details.num_layers <= 16:
        hx.errors.validation('- Number of Layers must range from 1 to 16')

    # Calculate premium split missing amounts
    # EEA
    hxd.cds.rating_factors.cover_details.premium_split_all_layers.non_eea = 1 - (hxd.cds.rating_factors.cover_details.premium_split_all_layers.eea or 0)

    # Coverages
    hxd.non_cds.cover_details.premium_split_missing_amount = 1
    hxd.non_cds.cover_details.show_bad_premium_split_missing_amount = False
    hxd.non_cds.cover_details.show_premium_split_missing_amount = True

    premium_total = 0
    for c, _ in coverages:
        if getattr(hxd.cds.rating_factors.risk_info, f"{c}_coverage_required"):
            node = getattr(hxd.cds.rating_factors.cover_details.premium_split_all_layers, c)
            if node is not None:
                premium_total += node
    hxd.non_cds.cover_details.premium_split_missing_amount -= premium_total

    if hxd.non_cds.cover_details.premium_split_coverages_show and round(hxd.non_cds.cover_details.premium_split_missing_amount, 2) != 0.00:
        hxd.non_cds.cover_details.show_bad_premium_split_missing_amount = True
        hxd.non_cds.cover_details.show_premium_split_missing_amount = False
        hx.errors.validation(f'- "Missing amount" for Split of Premium must be equal to 0')

    hxd.non_cds.cover_details.is_brokerage_all_layers_not = not hxd.non_cds.cover_details.is_brokerage_all_layers
