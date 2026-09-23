import hx

from algorithms.rate_risk_information import get_coverage_matrix, get_industry_matrix, get_sub_industry_matrix
from algorithms.rate_utilities import ratio, rgetattr, rsetattr, sum_structure_fields


def rate_exposure_details(hxd):
    # Show/hide
    show_hide_fields(hxd)

    # Regions
    for entity, coverage in zip(("employees", "revenues", "assets"), ("crime", "pi", "do")):
        # Show/hide value/percent fields
        is_percent = getattr(hxd.cds.exposure.granular.regions.splits_entered_as, entity) == "Percentage"
        setattr(hxd.non_cds.exposure_details.regions.is_value, entity, not is_percent)
        setattr(hxd.non_cds.exposure_details.regions.is_percent, entity, is_percent)
        if is_percent:            
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"percent.{entity}.show_missing", False)
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"percent.{entity}.hide_missing", True) 
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"value.{entity}.show_missing", False)
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"value.{entity}.hide_missing", False)                       
        else:
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"value.{entity}.show_missing", False)
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"value.{entity}.hide_missing", True)   
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"percent.{entity}.show_missing", False)
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"percent.{entity}.hide_missing", False)                     

        # Calculate missing amounts
        switch = "percent" if is_percent else "value"
        value_total_amount = rgetattr(hxd.cds.exposure.aggregate.total_amounts, entity)
        total_amount = 1 if is_percent else value_total_amount
        if value_total_amount < 0:
            hx.errors.validation(f'- "Total amount" for Regions ({entity}) must be a positive number')
        else:
            column_totals = sum_structure_fields(hxd.cds.exposure.granular.regions.regions_list, [f"{switch}.{entity}"])
            difference = round(total_amount - column_totals[f"{switch}.{entity}"], 2)

            # Set check on totals and missing amounts
            rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts, f"{switch}.{entity}", difference)
            if difference == 0.00:
                rsetattr(hxd.non_cds.exposure_details.regions.check_on_totals, f"{switch}.{entity}", "OK")
            else:
                rsetattr(hxd.non_cds.exposure_details.regions.check_on_totals, f"{switch}.{entity}", "")
                if getattr(hxd.cds.rating_factors.risk_info, f"{coverage}_coverage_required"):
                    rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"{switch}.{entity}.show_missing", True)
                    rsetattr(hxd.non_cds.exposure_details.regions.missing_amounts.toggles, f"{switch}.{entity}.hide_missing", False)
                    hx.errors.validation(f'- "Missing amount" for Regions ({entity}) must be equal to 0')

    # Investor profile
    # Regions & countries dropdown
    regions_table = hx.params.table_regions
    hxd.non_cds.exposure_details.investor_split.region_dropdown = sorted(set(regions_table["region"])) + ["RoW"] + sorted(regions_table["country"])
    # Totals
    hxd.non_cds.exposure_details.investor_split.type_total.percent = sum_structure_fields(hxd.cds.exposure.granular.investor_split_type, ["percent"])["percent"]
    hxd.non_cds.exposure_details.investor_split.region_total.percent = sum_structure_fields(hxd.cds.exposure.granular.investor_split_region, ["percent"])["percent"]

    # Revenue Split
    revenue_splits = ("revenue_split_banks", "revenue_split_admin", "premium_split", "revenue_split_brokers", "revenue_split_exchanges", "revenue_split_investment")
    for rs in revenue_splits:
        cds_node = getattr(hxd.cds.exposure.granular, rs)
        non_cds_node = getattr(hxd.non_cds.exposure_details, rs)

        # Total amount
        column_totals = sum_structure_fields(cds_node, ["amount"])
        rsetattr(non_cds_node, "total.amount", column_totals["amount"])

        # Calculate and set percentages
        calculate_revenue_split_ratios(cds_node, column_totals["amount"])

        # Total percent
        column_totals = sum_structure_fields(cds_node, ["percent"])
        rsetattr(non_cds_node, "total.percent", column_totals["percent"])


# Show/hide fields based on industry, coverage, ownership
def show_hide_fields(hxd):
    coverage = get_coverage_matrix(hxd)
    industry = get_industry_matrix(hxd)
    sub_industry = get_sub_industry_matrix(hxd)

    hxd.non_cds.exposure_details.no_of_locations_show = industry["has_industry"] and (coverage["is_crime"] or coverage["is_pi"])
    hxd.non_cds.exposure_details.regions.show = hxd.model_state.show_after_landing_page and industry["has_industry"] and coverage["has_coverage"]
    hxd.non_cds.exposure_details.client_info_public_show = industry["has_industry"] and coverage["is_do"] and hxd.cds.rating_factors.risk_info.ownership_type == "Public"
    hxd.non_cds.exposure_details.market_cap_us_show = hxd.non_cds.exposure_details.client_info_public_show and hxd.cds.rating_factors.exposure_details.us_listing != "NA"
    hxd.non_cds.exposure_details.client_info_show = any((hxd.non_cds.exposure_details.no_of_locations_show, (industry["has_industry"] and coverage["has_coverage"]), hxd.non_cds.exposure_details.client_info_public_show))
    hxd.non_cds.exposure_details.total_aum_show = industry["is_inv"] or (industry["is_oth"] and sub_industry["is_ta"])
    hxd.non_cds.exposure_details.capital_show = industry["is_inv"] and (sub_industry["is_pe"] or sub_industry["is_vc"]) and coverage["has_coverage"]
    hxd.non_cds.exposure_details.no_of_directorship_show = ((industry["is_inv"] and (sub_industry["is_pe"] or sub_industry["is_vc"])) or (industry["is_oth"] and sub_industry["is_ta"])) and coverage["is_do"]
    hxd.non_cds.exposure_details.transactions_av_show = industry["is_oth"] and sub_industry["is_cf"] and coverage["is_pi"]
    hxd.non_cds.exposure_details.exposure_details_show = any(((industry["has_industry"] and coverage["has_coverage"]), hxd.non_cds.exposure_details.total_aum_show, hxd.non_cds.exposure_details.capital_show, hxd.non_cds.exposure_details.no_of_directorship_show, hxd.non_cds.exposure_details.transactions_av_show))
    hxd.non_cds.exposure_details.investor_split.show = industry["is_inv"] and coverage["has_coverage"]
    hxd.non_cds.exposure_details.credit_rating_show = (industry["is_ban"] or industry["is_ins"]) and coverage["is_do"]
    #hxd.non_cds.exposure_details.revenue_split_admin.show = industry["is_oth"] and sub_industry["is_ta"] and coverage["is_pi"]
    hxd.non_cds.exposure_details.revenue_split_admin.show = False  # Disabled in Excel
    hxd.non_cds.exposure_details.revenue_split_banks.show = industry["is_ban"] and coverage["is_pi"]
    hxd.non_cds.exposure_details.premium_split.show = industry["is_ins"] and coverage["is_pi"]
    hxd.non_cds.exposure_details.revenue_split_brokers.show = industry["is_oth"] and (sub_industry["is_sb"] or sub_industry["is_cb"]) and coverage["is_pi"]
    hxd.non_cds.exposure_details.revenue_split_exchanges.show = industry["is_fin"] and coverage["has_coverage"]
    hxd.non_cds.exposure_details.revenue_split_investment.show = industry["is_inv"] and not (sub_industry["is_vc"] or sub_industry["is_pe"]) and coverage["is_pi"]


# Calculate percentages for revenue split
def calculate_revenue_split_ratios(structure_node, total_amount=None):
    if total_amount is None:
        total_amount = sum_structure_fields(structure_node, ["amount"])

    for _, activity in structure_node:
        activity.percent = ratio(activity.amount or 0, total_amount)
