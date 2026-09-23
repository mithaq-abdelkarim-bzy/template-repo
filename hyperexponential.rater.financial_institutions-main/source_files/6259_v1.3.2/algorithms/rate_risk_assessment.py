import hx

from algorithms.rate_constants import min_uw_adj
from algorithms.rate_risk_information import get_coverage_matrix, get_industry_matrix, get_sub_industry_matrix
from algorithms.rate_utilities import str_isblank


def rate_risk_assessment(hxd):
    # Show/Hide fields based on industry and converage
    coverage = get_coverage_matrix(hxd)
    industry = get_industry_matrix(hxd)
    sub_industry = get_sub_industry_matrix(hxd)

    hxd.non_cds.risk_assesment.any_any = industry["has_industry"] and coverage["has_coverage"]
    hxd.non_cds.risk_assesment.any_crime = industry["has_industry"] and coverage["is_crime"]
    hxd.non_cds.risk_assesment.any_pi = industry["has_industry"] and coverage["is_pi"]
    hxd.non_cds.risk_assesment.any_do = industry["has_industry"] and coverage["is_do"]
    hxd.non_cds.risk_assesment.any_crime_pi = industry["has_industry"] and (coverage["is_crime"] or coverage["is_pi"])
    hxd.non_cds.risk_assesment.any_pi_do = industry["has_industry"] and (coverage["is_pi"] or coverage["is_do"])
    hxd.non_cds.risk_assesment.fin_any = industry["is_fin"] and coverage["has_coverage"]
    hxd.non_cds.risk_assesment.notins_crime_pi = industry["has_industry"] and not industry["is_ins"] and (coverage["is_crime"] or coverage["is_pi"])
    hxd.non_cds.risk_assesment.ins_pi = industry["is_ins"] and coverage["is_pi"]
    hxd.non_cds.risk_assesment.fin_pi = industry["is_fin"] and coverage["is_pi"]
    hxd.non_cds.risk_assesment.ban_fin_pi = (industry["is_ban"] or industry["is_fin"]) and coverage["is_pi"]
    hxd.non_cds.risk_assesment.inv_pi = industry["is_inv"] and coverage["is_pi"]
    hxd.non_cds.risk_assesment.inv_PE_VC_RE_pi = industry["is_inv"] and (sub_industry["is_pe"] or sub_industry["is_vc"] or sub_industry["is_re"]) and coverage["is_pi"]
    hxd.non_cds.risk_assesment.inv_PE_VC_do = industry["is_inv"] and (sub_industry["is_pe"] or sub_industry["is_vc"]) and coverage["is_do"]

    # Validation
    uw_adj_value = hxd.cds.modifiers.risk_category.uw_adj
    uw_adj_comment = hxd.cds.modifiers.comment.uw_adj

    if uw_adj_value:
        if uw_adj_value < min_uw_adj:
            hx.errors.validation(f"- Underwriting adjustment: Maximum credit is {min_uw_adj*100}%")
        elif uw_adj_value < 0 and str_isblank(uw_adj_comment):
            hx.errors.validation("- Underwriting adjustment: Please provide a comment for the negative value")
