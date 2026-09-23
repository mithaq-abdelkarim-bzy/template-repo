from email import policy
from email.generator import BytesGenerator

from algorithms.rationale_proposal_templates.utils import generate_email, EmailType
from algorithms.rationale_proposal_templates.primary_proposal.string_templates import (
    QUOTE_OPTIONS_TEMPLATE_GMM,
    QUOTE_OPTIONS_TEMPLATE_GLS,
    RETROACTIVE_DATES_TEMPLATE_GMM,
    RETROACTIVE_DATES_TEMPLATE_GLS,
    MINIMUM_EARNED_SECTION,
    ERP_SECTION,
    COMMENTS_SECTION,
    ENDORSEMENTS_KEY_SECTION,
    ENDORSEMENTS_VALUE_SECTION,
    SUBJECTIVITIES_SECTION
) 

from algorithms.rationale_proposal_templates.utils import (
    GMM_COVERAGES,
    GMM_FIELDS,
    GMM_RETRO_PRICINGS,
    GMM_RETRO_FIELDS,
    GLS_COVERAGES,
    GLS_FIELDS,
    GLS_RETRO_PRICINGS,
    GLS_RETRO_FIELDS
)


def generate_email_proposal(hxd):
    insured_name = hxd.cds.standard_fields.insured_name if hxd.cds.standard_fields.insured_name else " "
    broker = hxd.cds.standard_fields.broker if hxd.cds.standard_fields.broker else " "
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    policy_period = f"{inception_date} - {expiry_date}"
    governing_law = hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law \
        if hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law else " "
    exposure = f"${hxd.cds.exposure.aggregate.revenue:,.0f}" if hxd.cds.exposure.aggregate.revenue else " "

    if hxd.cds.gmm_masking:
        cob_code = hxd.cds.exposure.granular.gmm_product.cob_code_description
        coverages = GMM_COVERAGES
        fields = GMM_FIELDS
        retro_pricings = GMM_RETRO_PRICINGS
        retro_fields = GMM_RETRO_FIELDS
        options_template = QUOTE_OPTIONS_TEMPLATE_GMM
        retroactive_dates_template = RETROACTIVE_DATES_TEMPLATE_GMM
    else:
        cob_code = hxd.cds.exposure.granular.glsn_product.cob_code_description
        coverages = GLS_COVERAGES
        fields = GLS_FIELDS
        retro_pricings = GLS_RETRO_PRICINGS
        retro_fields = GLS_RETRO_FIELDS
        options_template = QUOTE_OPTIONS_TEMPLATE_GLS
        retroactive_dates_template = RETROACTIVE_DATES_TEMPLATE_GLS

    # Map the fields from coverages
    selected_option_id = int(hxd.cds.option_selected[-1]) - 1  # We get the index
    selected_option =  hxd.cds.options[selected_option_id]
    commission = f"{selected_option.brokerage_primary * 100:.1f}%" if selected_option.brokerage_primary is not None else ""

    fields_mapping = dict()
    fields_mapping['option_number'] = selected_option_id + 1 # We add 1 to get the actual option number instead of the index

    for key, name in zip(fields, coverages):
        layer = getattr(selected_option.coverages, name)
        
        value = ""
        if getattr(getattr(hxd.cds.rating_factors.pricing, name), 'include_primary'):
            per_claim = f"${layer.per_claim_limit:,.0f}" if layer.per_claim_limit else "None"
            aggregate = f"${layer.aggregate_limit:,.0f}" if layer.aggregate_limit else "None"
            retention = f"${layer.retention:,.0f}" if layer.retention else "None"
            value = f"{per_claim}/{aggregate} xs {retention}"

        fields_mapping[key] = value

    # Map the fields from pricing to get the retroactive dates
    for key, name in zip(retro_fields, retro_pricings):
        value = ""
        if getattr(getattr(hxd.cds.rating_factors.pricing, name), 'retroactive_date'):
            value = f"{getattr(getattr(hxd.cds.rating_factors.pricing, name), 'retroactive_date')}"
        fields_mapping[key] = value

    fields_mapping["quote_premium"] = f"${selected_option.quoted_premium_primary:,.0f}" if selected_option.quoted_premium_primary is not None else None
    fields_mapping["policy_aggregate"] = f"${selected_option.agg_limit:,.0f}"
    
    # Replace the mapped fields in the string templates
    quote_options_section = options_template.substitute(**fields_mapping)
    retroactive_dates_section = retroactive_dates_template.substitute(**fields_mapping)

    # Creating a dict that will be used to create the email table structure
    table_fields = {
        "Named Insured": insured_name,
        "Broker": broker,
        "Policy Period": policy_period,
        "COB Code": cob_code,
        "Commission": commission,
        "Quote Options:": quote_options_section,
        "Minimum Earned Premium": MINIMUM_EARNED_SECTION,
        "Retroactive dates": retroactive_dates_section,
        "ERP": ERP_SECTION,
        "Governing Law": governing_law,
        "Exposure (internal use only - revenues)": exposure,
        "Comments": COMMENTS_SECTION,
        "TRIA": "2% AP ($500 minimum)",
        ENDORSEMENTS_KEY_SECTION: ENDORSEMENTS_VALUE_SECTION,
        "Subjectivities": SUBJECTIVITIES_SECTION
    }

    underwriter = hxd.cds.standard_fields.underwriter
    formatted_underwriter = underwriter.replace(" ", ".").lower()
    underwriter_email = formatted_underwriter + "@beazley.com"
    hxd.cds.email.sender = underwriter_email
    hxd.cds.email.recipient = underwriter_email

    email_msg = generate_email(table_fields=table_fields, insured_name=insured_name, sender=underwriter_email, recipient=underwriter_email, email_type=EmailType.PRIMARY)

    # Save the email as an .eml file
    with hxd.cds.primary_proposal_template_file.open("b") as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(email_msg)