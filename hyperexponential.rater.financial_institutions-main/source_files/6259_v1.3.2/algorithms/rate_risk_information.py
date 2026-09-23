import hx

from algorithms.rate_utilities import policy_term


def rate_risk_information(hxd):
    hxd.cds.rating_factors.policy_term = policy_term(hxd.hx_core.inception_date, hxd.hx_core.expiry_date)
    hxd.non_cds.risk_info.is_coverage_required = get_coverage_matrix(hxd)["has_coverage"]

    # Validations
    if not hxd.non_cds.risk_info.is_coverage_required:
        hx.errors.validation("- At least one coverage must be selected")

    if not hxd.cds.standard_fields.insured_name:
        hx.errors.validation("- Insured Name must be selected")

    if not hxd.cds.standard_fields.underwriter:
        hx.errors.validation("- Underwriter must be selected")

    if not hxd.cds.standard_fields.broker:
        hx.errors.validation("- Broker must be selected")

    if not hxd.cds.risk_info.broker_contact:
        hx.errors.validation("- Broker Contact must be entered")

    if not hxd.cds.rating_factors.risk_info.sub_industry:
        hx.errors.validation("- Sub Industry must be selected")

    # Populate countries based on regions
    regions_table = hx.params.table_regions
    hxd.non_cds.risk_info.region_dropdown = sorted(set(regions_table["region"]))
    filtered_countries = regions_table[regions_table["region"] == hxd.cds.rating_factors.risk_info.region]
    hxd.non_cds.risk_info.country_dropdown = filtered_countries["country"]
    # Validate current selection
    selected_country = hxd.cds.standard_fields.insured_country
    if selected_country and selected_country not in filtered_countries["country"].values:
        hx.errors.validation("- Country of Domicile does not belong to the selected Region of Domicile")

    # Populate sub industries based on industries
    industries_table = hx.params.table_base_rates[["industry", "sub_industry"]].sort_values(["industry", "sub_industry"])
    hxd.non_cds.risk_info.industry_dropdown = industries_table["industry"].unique()
    filtered_subindustries = industries_table[industries_table["industry"] == hxd.cds.key_industry.code_name]
    hxd.non_cds.risk_info.sub_industry_dropdown = filtered_subindustries["sub_industry"].unique()
    # Validate current selection
    selected_subindustry = hxd.cds.rating_factors.risk_info.sub_industry
    if selected_subindustry and selected_subindustry.lower() not in filtered_subindustries["sub_industry"].str.lower().values:
        hx.errors.validation("- Sub Industry does not belong to the selected Industry")


def get_coverage_matrix(hxd):
    is_crime = hxd.cds.rating_factors.risk_info.crime_coverage_required
    is_pi = hxd.cds.rating_factors.risk_info.pi_coverage_required
    is_do = hxd.cds.rating_factors.risk_info.do_coverage_required
    has_coverage = any((is_crime, is_pi, is_do))

    return {"has_coverage": has_coverage, "is_crime": is_crime, "is_pi": is_pi, "is_do": is_do}


def get_industry_matrix(hxd):
    has_industry = hxd.cds.key_industry.code_name is not None

    code_name = str(hxd.cds.key_industry.code_name).casefold()  # Caseless comparison

    is_ban = code_name == "Banks".casefold()
    is_ins = code_name == "Insurance companies".casefold()
    is_fin = code_name == "Financial infrastructure & exchanges".casefold()
    is_inv = code_name == "Investment managers".casefold()
    is_oth = code_name == "Other".casefold()

    return {"has_industry": has_industry, "is_ban": is_ban, "is_ins": is_ins, "is_fin": is_fin, "is_inv": is_inv, "is_oth": is_oth}


def get_sub_industry_matrix(hxd):
    sub_industry = str(hxd.cds.rating_factors.risk_info.sub_industry).casefold()  # Caseless comparison

    is_pe = sub_industry == "Private Equity".casefold()
    is_vc = sub_industry == "Venture Capital".casefold()
    is_re = sub_industry == "Real Estate".casefold()
    is_mf = sub_industry == "Multi-Family Office".casefold()
    is_sf = sub_industry == "Single Family Office".casefold()
    is_ta = sub_industry == "Trust Administrator".casefold()
    is_sb = sub_industry == "Stock brokers/dealers".casefold()
    is_cb = sub_industry == "Commodities brokers/dealer".casefold()
    is_cf = sub_industry == "Corporate finance houses/boutiques".casefold()

    return {"is_pe": is_pe, "is_vc": is_vc, "is_re": is_re, "is_mf": is_mf, "is_sf": is_sf, "is_ta": is_ta, "is_sb": is_sb, "is_cb": is_cb, "is_cf": is_cf}
