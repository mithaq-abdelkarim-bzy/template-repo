import hx
import pandas as pd
import numpy as np
import math as math


def product_types_with_revenue_tier_types():
    # Returns a list of product types with revenue tier types
    return ["Manutech", "Products"]


def product_types_with_longevity():
    # Returns a list of product types with longevity
    return ["MPL", "Tech", "Med Mal"]


def product_types_with_professional_experience():
    # Returns a list of product types with professional experience
    return ["MPL", "Med Mal"]


def product_types_with_business_with_written_contract():
    return ["MPL"]


def set_loss_factor_empty_pane(hxd):
    if (
        not hxd.cds.rating_factors.longevity.show
        and not hxd.cds.rating_factors.professional_experience.show
    ):
        hxd.cds.rating_factors.show_loss_experience_empty_panel = True
    else:
        hxd.cds.rating_factors.show_loss_experience_empty_panel = False


def init_professional_experience(hxd):
    # Function to set professional experience based on given parameters

    if (
        hxd.cds.rating_factors.product_type
        in product_types_with_professional_experience()
    ):
        hxd.cds.rating_factors.professional_experience.show = True
        professional_experience_table = hx.params.table_input_professional_experience

        # Get the current professional experience row based on professional experience name
        filtered_years = professional_experience_table[
            professional_experience_table["product_type"]
            == hxd.cds.rating_factors.product_type
        ]["years_of_experience"].values

        hxd.cds.rating_factors.professional_experience.years_list = [
            {"years": item} for item in filtered_years
        ]

        factor_rows = professional_experience_table[
            (
                professional_experience_table["years_of_experience"]
                == hxd.cds.rating_factors.professional_experience.years
            )
            & (
                professional_experience_table["product_type"]
                == hxd.cds.rating_factors.product_type
            )
        ]["factor"].values

        if len(factor_rows) == 1:
            hxd.cds.rating_factors.professional_experience.factor = factor_rows[0]
        elif len(factor_rows) > 0:
            raise ValueError(
                "Non unique key found in professional experience table",
                hxd.cds.rating_factors.professional_experience.years,
            )
    else:
        hxd.cds.rating_factors.professional_experience.show = False
    set_loss_factor_empty_pane(hxd)


def init_longevity(hxd):
    # Function to set longevity based on given parameters

    if hxd.cds.rating_factors.product_type in product_types_with_longevity():
        hxd.cds.rating_factors.longevity.show = True
        longevity_table = hx.params.table_input_longevity

        # Get the current longevity row based on name
        filtered_years = longevity_table[
            longevity_table["product_type"] == hxd.cds.rating_factors.product_type
        ]["years"].values

        hxd.cds.rating_factors.longevity.years_list = [
            {"years": item} for item in filtered_years
        ]

        factor_rows = longevity_table[
            (longevity_table["years"] == hxd.cds.rating_factors.longevity.years)
            & (longevity_table["product_type"] == hxd.cds.rating_factors.product_type)
        ]["factor"].values

        if len(factor_rows) == 1:
            hxd.cds.rating_factors.longevity.factor = factor_rows[0]
        elif len(factor_rows) > 0:
            raise ValueError(
                "Non unique key found in longevity table",
                hxd.cds.rating_factors.longevity.years,
            )
    else:
        hxd.cds.rating_factors.longevity.show = False
    set_loss_factor_empty_pane(hxd)


def init_endorsements(hxd):

    if hxd.cds.rating_factors.product_type == "Med Mal":
        endorsements_table = hx.params.table_input_endorsements
        endorsements = getattr(hxd.cds.rating_factors.med_mal, "endorsements")
        total_endorsement = 0

        for endorsement in endorsements:
            factor_rows = endorsements_table[
                endorsements_table["endorsement"].values == endorsement.endorsement
            ]["factor"].values

            if len(factor_rows) == 1:
                endorsement.factor = factor_rows[0]
                total_endorsement += factor_rows[0]
            elif len(factor_rows) > 0:
                raise ValueError(
                    "Non unique key found in endorsements table",
                    endorsement.endorsement,
                )

        hxd.cds.rating_factors.med_mal.total_endorsement = total_endorsement


def init_allied_medical(hxd):
    if hxd.cds.rating_factors.product_type == "Med Mal":
        allied_medical_table = hx.params.table_allied_medical
        allied_medical_type = (
            hxd.cds.rating_factors.med_mal.allied_medical.allied_medical_type
        )

        hxd.cds.rating_factors.med_mal.allied_medical.exposure_type = (
            allied_medical_table[
                allied_medical_table["allied_medical"].values == allied_medical_type
            ]["exposure_type"].values
        )

        factor_rows = allied_medical_table[
            allied_medical_table["allied_medical"].values == allied_medical_type
        ]["exposure_factor"].values

        type_rows = allied_medical_table[
            allied_medical_table["allied_medical"].values == allied_medical_type
        ]["exposure_type"].values

        if len(type_rows) == 1:
            hxd.cds.rating_factors.med_mal.allied_medical.exposure_type = type_rows[0]
        elif len(type_rows) > 0:
            raise ValueError(
                "Non unique key found in allied medical table",
                allied_medical_type,
            )

        if len(factor_rows) == 1:
            hxd.cds.rating_factors.med_mal.allied_medical.exposure_factor = factor_rows[
                0
            ]
        elif len(factor_rows) > 0:
            raise ValueError(
                "Non unique key found in allied medical table",
                allied_medical_type,
            )


def init_social_services(hxd):
    if hxd.cds.rating_factors.product_type == "Med Mal":
        social_services_table = hx.params.table_input_social_services
        social_services_type = (
            hxd.cds.rating_factors.med_mal.social_services.social_services_type
        )

        hxd.cds.rating_factors.med_mal.social_services.exposure_type = (
            social_services_table[
                social_services_table["social_services"].values == social_services_type
            ]["exposure_type"].values
        )

        factor_rows = social_services_table[
            social_services_table["social_services"].values == social_services_type
        ]["exposure_factor"].values

        type_rows = social_services_table[
            social_services_table["social_services"].values == social_services_type
        ]["exposure_type"].values

        if len(factor_rows) == 1:
            hxd.cds.rating_factors.med_mal.social_services.exposure_factor = (
                factor_rows[0]
            )
        elif len(factor_rows) > 0:
            raise ValueError(
                "Non unique key found in social services table",
                social_services_type,
            )

        if len(type_rows) == 1:
            hxd.cds.rating_factors.med_mal.social_services.exposure_type = type_rows[0]
        elif len(type_rows) > 0:
            raise ValueError(
                "Non unique key found in social services table",
                social_services_type,
            )


def init_product_selection(hxd):
    if hxd.cds.rating_factors.product_type == "Med Mal":
        hxd.cds.rating_factors.med_mal.show = True
        hxd.cds.rating_factors.med_mal.hide = False
    else:
        hxd.cds.rating_factors.med_mal.show = False
        hxd.cds.rating_factors.med_mal.hide = True
        if hxd.cds.rating_factors.product_type == "Staffing":
            hxd.cds.rating_factors.staffing.show = True
        else:
            hxd.cds.rating_factors.staffing.show = False


def add_credit_or_debit(hxd):
    # Function to add credit or debit based on given parameters

    if hxd.cds.rating_factors.product_type == "Med Mal":
        professional_experience_value = (
            hxd.cds.rating_factors.professional_experience.factor or 0
        )

        longevity_value = hxd.cds.rating_factors.longevity.factor or 0

        underwriter_judgement_value = hxd.cds.modifiers.underwriter_judgement or 0

        hxd.cds.rating_factors.med_mal.total_credit_or_debit = (
            underwriter_judgement_value
            + professional_experience_value
            + longevity_value
        )


def init_staffing(hxd):
    if hxd.cds.rating_factors.product_type == "Staffing":
        permanent_staffing_value = hxd.cds.rating_factors.staffing.permanent or 0

        PEO_value = hxd.cds.rating_factors.staffing.peo or 0

        temporary_staffing_value = hxd.cds.rating_factors.staffing.temporary or 0

        hxd.cds.rating_factors.staffing.total = (
            permanent_staffing_value + PEO_value + temporary_staffing_value
        )


def init_revenue_types(hxd):
    product_type = hxd.cds.rating_factors.product_type
    # Determine whether to show revenue type or not based on product type
    if product_type in product_types_with_revenue_tier_types():
        hxd.cds.rating_factors.show_revenue_type = True
        revenue_types_table = hx.params.table_revenue_types_factors
        hxd.cds.rating_factors.types_list = revenue_types_table[
            revenue_types_table["product_type"] == product_type
        ]["revenue_type"].values
        return list(set(revenue_types_table["revenue_type"]))
    else:
        hxd.cds.rating_factors.show_revenue_type = False


def rate_exposure(hxd):
    # Function to rate exposure based on given parameters

    init_product_selection(hxd)
    init_longevity(hxd)
    init_professional_experience(hxd)
    init_revenue_types(hxd)
    init_allied_medical(hxd)
    init_endorsements(hxd)
    init_social_services(hxd)
    init_staffing(hxd)
    add_credit_or_debit(hxd)

    # Get the retroactive years table from parameters
    retroactive_years_table = hx.params.table_input_retroactive_years

    # Filter the retroactive years table to match the selected product type
    filtered_retroactive_years = retroactive_years_table[
        retroactive_years_table["product"].values == hxd.cds.rating_factors.product_type
    ]["years"].values

    # Populate the retroactive years list with the filtered values
    hxd.non_cds.rating_factors.retroactive_years_list = [
        {"years": item} for item in filtered_retroactive_years
    ]

    sub_occupations_table = hx.params.table_input_sub_occupations
    occupations_table = hx.params.table_input_occupations
    hazard_tiers_table = hx.params.table_hazard_tiers

    # Get the current occupation row based on occupation name
    current_occupation_row = occupations_table[
        occupations_table["occupation_name"] == hxd.cds.key_industry.code_name
    ]

    # Get the current occupation code
    current_occupation_code = current_occupation_row["occupation_group"].values

    # Filter sub occupations based on current occupation code
    filtered_sub_occupations = sub_occupations_table[
        sub_occupations_table["sub_occupation_group"].values == current_occupation_code
    ]["sub_occupation_name"].values

    # Update the sub occupations list in hxd object
    hxd.cds.key_industry.sub_occupation.list = [
        {"name": item} for item in filtered_sub_occupations
    ]

    hxd.cds.rating_factors.business_with_written_contract.show = (
        True
        if hxd.cds.rating_factors.product_type
        in product_types_with_business_with_written_contract()
        else False
    )

    # Get hazard tiers based on product type
    hazard_tiers = hazard_tiers_table[
        hazard_tiers_table["product_type"] == hxd.cds.rating_factors.product_type
    ].values

    # Update the tiers list in hxd object
    hxd.cds.rating_factors.tiers_list = [
        {
            "tier": row[1],
            "business_description": row[2],
        }
        for row in hazard_tiers
    ]

    revenues = hxd.cds.rating_factors.revenues
    total_revenue = 0

    # Calculate total revenue
    for revenue in revenues:
        if revenue.value is None:
            continue
        total_revenue += revenue.value

    # Update the total revenue in hxd object
    hxd.cds.exposure.aggregate.total_revenue = total_revenue
