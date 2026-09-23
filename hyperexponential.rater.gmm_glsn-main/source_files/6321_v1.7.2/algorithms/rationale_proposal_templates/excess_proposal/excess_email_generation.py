from email import policy
from email.generator import BytesGenerator
from algorithms.rate_constants import max_layers

from algorithms.rationale_proposal_templates.utils import generate_email, EmailType
from algorithms.rationale_proposal_templates.excess_proposal.string_templates import (
    SUBJECTIVITIES_SECTION,
    ERP_SECTION,
    ENDORSEMENTS_SECTION,
    RETROACTIVE_DATES_SECTION,
    COMMENTS_SECTION,
    MINIMUM_EARNED_SECTION,
    SCHEDULED_HPL_KEY_SECTION
)
from algorithms.rationale_proposal_templates.utils import (
    GMM_COVERAGES,
    GLS_COVERAGES,
    LABELS_MAPPING
)


def build_excess_rows(hxd, selected_option):
    labels = [
        "First", "Second", "Third", "Fourth", "Fifth",
        "Sixth", "Seventh", "Eighth", "Ninth", "Tenth"
    ]

    excess_mapper = {}
    for i in range(1, max_layers + 1):
        # Dynamically populate the value based on 'add excess' flag
        if getattr(hxd.cds, f"add_excess_{i}", False):
            loss_limit_value = getattr(selected_option, f"per_claim_limit_{i}_excess", "")
            aggr_limit_value = getattr(selected_option, f"aggregate_limit_{i}_excess", "")
            loss_limit_value_formatted = f"${loss_limit_value:,.0f}" if loss_limit_value else " — "
            aggr_limit_value_formatted = f"${aggr_limit_value:,.0f}" if aggr_limit_value else " — "
            value = f"{loss_limit_value_formatted}/{aggr_limit_value_formatted}"
              
            excess_mapper[i] = value
        else:
            break

    rows = []
    for idx, (i, value) in enumerate(excess_mapper.items(), start=1):
        if idx == 1:
            rows.append(f"""
                <tr>
                  <td rowspan={len(excess_mapper)} style="padding:0; margin:0; line-height:0; border-left:1px solid #000;">
                    <div style="display:block; line-height:1; padding:8px 0;">
                        Excess
                    </div>
                  </td>
                  <td>{labels[i-1]} Excess</td>
                  <td>{value}</td>
                  <td></td>
                </tr>
            """)
        else:
            # Other rows skip that first cell
            rows.append(f"""
                <tr>
                  <td>{labels[i-1]} Excess</td>
                  <td>{value}</td>
                  <td></td>
                </tr>
            """)

    return "\n".join(rows)

def build_primary_rows(hxd, coverages, selected_option, primary_auto, primary_el):
    included_in_primary = list()
    for coverage in coverages:
        try:
            if getattr(getattr(hxd.cds.rating_factors.pricing, coverage), 'include_primary'):
                included_in_primary.append(coverage)
        except AttributeError:
            # Field missing or not structured as expected; skip it
            continue

    num_rows = len(included_in_primary)
    
    # Check if we need to increase the rowspan
    if primary_auto:
        num_rows += 1
    if primary_el:
        num_rows += 1

    result_html = ""
    for i, coverage in enumerate(included_in_primary):
        result_html += "<tr>"

        if i == 0:
            result_html += f"""<td rowspan={num_rows} style="padding:0; margin:0; line-height:0; border-left:1px solid #000;">
                <div style="display:block; line-height:1; padding:8px 0;">
                    Primary
                </div>
            </td>"""


        layer = getattr(selected_option.coverages, coverage)
        per_claim = f"${layer.per_claim_limit:,.0f}" if layer.per_claim_limit else " — "
        aggregate = f"${layer.aggregate_limit:,.0f}" if layer.aggregate_limit else " — "
        deductible = f"${layer.retention:,.0f}" if layer.retention else ""
        limits = f"{per_claim}/{aggregate}"
        label = LABELS_MAPPING.get(coverage, coverage.upper())

        result_html += f"<td>{label}</td>"
        result_html += f"<td>{limits}</td>"
        result_html += f"<td>{deductible}</td>"
        result_html += "</tr>"
    
    # add the rows for primary auto/el
    if primary_auto:
        result_html += f"""<tr>
            <td>Auto</td>
            <td>{primary_auto}</td>
            <td></td>
        </tr>"""
    if primary_el:
        result_html += f"""<tr>
          <td>EL</td>
          <td>{primary_el}</td>
          <td></td>
        </tr>"""

    return result_html.strip()

def build_commission_and_premium_rows(layers, selected_option):
    commission_rows = list()
    premium_rows = list()
    for layer in layers:
        # We're only looking at Excess layers
        if layer.layer_label in ["Retention", "Primary Layer"]:
            continue

        if layer.status in ["Bound", "Quoted"]:
            # layer labels are like 'Excess 1', 'Excess 2', we parse it so we know which layer's selected option to take
            label_split = layer.layer_label.split(" ")
            label_id = int(label_split[-1])

            # create the commission section
            excess_brokerage = getattr(selected_option, f"brokerage_{label_id}_excess", "")
            commission_value = f"Excess {label_id}: {excess_brokerage * 100:.1f}%\n" if excess_brokerage else f"Excess {label_id}: —\n"
            commission_rows.append(commission_value)

            # create the premium section
            excess_premium = layer.bound_premium if layer.bound_premium else layer.quoted_premium
            premium_value = f"Excess {label_id}: ${excess_premium:,.0f}\n" if excess_premium else f"Excess {label_id}: —\n"
            premium_rows.append(premium_value)

    commission = "\n".join(commission_rows) if commission_rows else "No Bound or Quoted layers found"
    premium = "\n".join(premium_rows) if premium_rows else "No Bound or Quoted layers found"
    return commission, premium

def generate_email_proposal(hxd):
    insured_name = hxd.cds.standard_fields.insured_name if hxd.cds.standard_fields.insured_name else " "
    broker = hxd.cds.standard_fields.broker if hxd.cds.standard_fields.broker else " "
    inception_date = hxd.hx_core.inception_date
    expiry_date = hxd.hx_core.expiry_date
    policy_period = f"{inception_date} - {expiry_date}"
    exposure = f"${hxd.cds.exposure.aggregate.revenue:,.2f}" if hxd.cds.exposure.aggregate.revenue else " "
    governing_law = hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law \
        if hxd.cds.rating_factors.us_international_choice_of_law.choice_of_law else " "

    # Map the fields from coverages
    selected_option_id = int(hxd.cds.option_selected[-1]) - 1  # We get the index
    selected_option =  hxd.cds.options[selected_option_id]

    if hxd.cds.gmm_masking:
        coverages = GMM_COVERAGES
        cob_code = hxd.cds.exposure.granular.gmm_product.cob_code_description
        primary_auto = f"${hxd.cds.rating_factors.gmm.umbrella.auto_liability.underlying_ee:,.0f}" if hxd.cds.rating_factors.gmm.umbrella.auto_liability.underlying_ee else ""
        primary_el = f"${hxd.cds.rating_factors.gmm.umbrella.employers_liability.underlying_ee:,.0f}" if hxd.cds.rating_factors.gmm.umbrella.employers_liability.underlying_ee else ""
    else:
        coverages = GLS_COVERAGES
        cob_code = hxd.cds.exposure.granular.glsn_product.cob_code_description
        primary_auto = f"${hxd.cds.rating_factors.glsn.umbrella.auto_liability.underlying_ee:,.0f}" if hxd.cds.rating_factors.glsn.umbrella.auto_liability.underlying_ee else ""
        primary_el = f"${hxd.cds.rating_factors.glsn.umbrella.employers_liability.underlying_ee:,.0f}" if hxd.cds.rating_factors.glsn.umbrella.employers_liability.underlying_ee else ""
    
    commission, premium = build_commission_and_premium_rows(hxd.cds.layers, selected_option)
    primary_rows = build_primary_rows(hxd, coverages, selected_option, primary_auto, primary_el)
    excess_rows = build_excess_rows(hxd, selected_option)

    quote_options_section = f"""<table border="0" style="border-collapse:collapse; width:100%; margin:0; padding:0;">
        <tr>
          <th style="padding: 0;">Carrier</th>
          <th style="padding: 0;">Coverage</th>
          <th style="padding: 0;">Limits</th>
          <th style="padding: 0;">Deductible</th>
        </tr>
        {primary_rows}
        {excess_rows}
    </table>"""

    # Creating a dict that will be used to create the email table structure
    table_fields = {
        "Named Insured": insured_name,
        "Broker": broker,
        "Policy Period": policy_period,
        "COB Code": cob_code,
        "Commission": commission,
        "Premium": premium,
        "Quote Options:": quote_options_section,
        "Subjectivities": SUBJECTIVITIES_SECTION,
        "Minimum Earned Premium": MINIMUM_EARNED_SECTION,
        "Retroactive dates": RETROACTIVE_DATES_SECTION,
        "ERP": ERP_SECTION,
        SCHEDULED_HPL_KEY_SECTION: " ",
        "Governing Law": governing_law,
        "Exposure (internal use only - revenues)": exposure,
        "Comments": COMMENTS_SECTION,
        "TRIA": "2% AP ($500 minimum)",
        "Endorsements": ENDORSEMENTS_SECTION,
    }

    underwriter = hxd.cds.standard_fields.underwriter
    formatted_underwriter = underwriter.replace(" ", ".").lower()
    underwriter_email = formatted_underwriter + "@beazley.com"
    hxd.cds.email.sender = underwriter_email
    hxd.cds.email.recipient = underwriter_email

    email_msg = generate_email(table_fields=table_fields, insured_name=insured_name, sender=underwriter_email, recipient=underwriter_email, email_type=EmailType.EXCESS)

    # Save the email as an .eml file
    with hxd.cds.excess_proposal_template_file.open("b") as file:
        gen = BytesGenerator(file, policy=policy.default)
        gen.flatten(email_msg)