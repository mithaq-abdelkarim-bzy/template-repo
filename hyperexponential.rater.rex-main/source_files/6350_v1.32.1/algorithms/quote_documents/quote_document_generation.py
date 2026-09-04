import hx
import pandas as pd
import polars as pl
import os
from mailmerge import MailMerge
from datetime import datetime


def quote_doc_rater_calc(hxd, df):
    # Quote Doc async task rater calculation
    george_df = df[["tiv_total_usd", "industry", "occupancy"]].groupby(["industry", "occupancy"], maintain_order=True).agg(pl.col("tiv_total_usd").sum()).sort("tiv_total_usd", descending=True)
    hxd.quote_documents.bpro_outputs.george_occupancy = george_df.row(0, named=True)['occupancy']


def quote_doc_rating_actions(hxd):    
    ex_rate = hxd.policy_information.exchange_rate or 1 

    hxd.quote_documents.bpro_outputs.insured_name = hxd.policy_information.insured
    hxd.quote_documents.bpro_outputs.underwriter = hxd.policy_information.underwriter
    hxd.quote_documents.bpro_outputs.global_rater_id = hx.meta.policy_option_id
    
    hxd.quote_documents.bpro_outputs.insured_from = hxd.hx_core.inception_date
    hxd.quote_documents.bpro_outputs.insured_until = hxd.hx_core.expiry_date
    hxd.quote_documents.bpro_outputs.office = hxd.policy_information.uw_office

    hxd.quote_documents.bpro_outputs.num_locs = hxd.schedule.schedule_total.num_locs
    hxd.quote_documents.bpro_outputs.tiv = hxd.schedule.schedule_total.tiv_total
    hxd.quote_documents.bpro_outputs.itv_per_sqft = (hxd.schedule.schedule_total.tiv_buildings / hxd.schedule.schedule_total.floor_area) / ex_rate if hxd.schedule.schedule_total.floor_area and ex_rate else 0

    hxd.quote_documents.bpro_outputs.bpro_occupancy = hxd.non_layer_perils.equipment_breakdown.occupancy.selected


    quote_doc_types = hx.params.quote_doc_types
    peril_type = hxd.quote_documents.bpro_outputs.peril
    filtered_quote_doc_types = quote_doc_types[quote_doc_types['peril'] == peril_type]
    if filtered_quote_doc_types.shape[0] > 0:
        manuscript = filtered_quote_doc_types['quote_type'].iloc[0] == "Manuscript"
        hxd.quote_documents.manuscript_flag = manuscript
        hxd.quote_documents.special_form_flag = not manuscript
    

    selected_layer = hxd.quote_documents.layer
    for index, layer in enumerate(hxd.layers):
        if index + 1 == selected_layer:
            writ_line = (layer.written_line_perc if layer.status in {'Bound', 'MTA', 'Cancellation'} else layer.quoted_line_perc) or 0

            hxd.quote_documents.bpro_outputs.tria = "Y" if layer.perils.tria.include else "N"
            hxd.quote_documents.bpro_outputs.equipment_breakdown = "Y" if layer.perils.equipment_breakdown.include else "N"

            hxd.quote_documents.bpro_outputs.commission = layer.brokerage
            hxd.quote_documents.bpro_outputs.limit = layer.limit * writ_line / ex_rate if layer.limit and writ_line and ex_rate else 0
            hxd.quote_documents.bpro_outputs.bpro_ref = layer.reference  
            hxd.quote_documents.bpro_outputs.prem_rates = layer.pre_uw_adjustment.achieved_rate

            # hxd.quote_documents.fixed_sublimits.ordinance_and_law = layer.perils.
            hxd.quote_documents.fixed_sublimits.wind.val = hxd.sublimit.scs_sublimit / ex_rate if hxd.sublimit.scs_sublimit and ex_rate else 0
            hxd.quote_documents.fixed_sublimits.wind_2.val = layer.perils.named_windstorm.location_ded.option_1.sublimit / ex_rate if layer.perils.named_windstorm.location_ded.option_1.sublimit and ex_rate else 0
            hxd.quote_documents.fixed_sublimits.quake.val = hxd.sublimit.eq_sublimit / ex_rate if hxd.sublimit.eq_sublimit and ex_rate else 0
            hxd.quote_documents.fixed_sublimits.quake_2.val = layer.perils.quake.location_ded.option_1.sublimit / ex_rate if layer.perils.quake.location_ded.option_1.sublimit and ex_rate else 0
            hxd.quote_documents.fixed_sublimits.flood.val = hxd.sublimit.fl_sublimit / ex_rate if hxd.sublimit.fl_sublimit and ex_rate else 0

            hxd.quote_documents.premium.property_only = layer.achieved_premium_100_gg * writ_line / ex_rate if layer.achieved_premium_100_gg else 0
            hxd.quote_documents.premium.tria = (layer.perils.tria.actual_tria_premium * writ_line / ex_rate if layer.perils.tria.actual_tria_premium else layer.perils.tria.tria_premium * writ_line / ex_rate if layer.perils.tria.tria_premium else 0) or 0
            hxd.quote_documents.premium.equipment_breakdown = (layer.perils.equipment_breakdown.actual_eb_premium * writ_line / ex_rate if layer.perils.equipment_breakdown.actual_eb_premium else layer.perils.equipment_breakdown.eb_premium * writ_line / ex_rate if layer.perils.equipment_breakdown.eb_premium else 0) or 0 if hxd.non_layer_perils.equipment_breakdown.travelers else 0
            hxd.quote_documents.premium.total_exc_fees = hxd.quote_documents.premium.property_only + hxd.quote_documents.premium.tria + hxd.quote_documents.premium.equipment_breakdown

            hxd.quote_documents.excess = layer.excess
            hxd.quote_documents.written_line = writ_line

            hxd.quote_documents.including_flood = "including" if layer.perils.flood.include else "excluding"
            hxd.quote_documents.including_quake = "including" if layer.perils.quake.include else "excluding"
            hxd.quote_documents.including_eb = "including" if layer.perils.equipment_breakdown.include else "excluding"

            for ded_index, ded_layer in enumerate(hxd.quote_documents.deductibles):
                if ded_layer.peril is not None and ded_layer.peril != "Other":
                    deductible_fetches = {
                        "Fire/AOP": ["fire", "deductible"],
                        "Named Storm": ["named_windstorm", "per_occurrence_ded"],
                        "All Other Wind": ["scs", "per_occurrence_ded"],
                        "Wind/Hail": ["scs", "per_occurrence_ded"],
                        "Earthquake": ["quake", "per_occurrence_ded"],
                        "Flood": ["flood", "per_occurrence_ded"],
                        "Wildfire": ["wildfire", "deductible"],
                        }
                    ded_attr = getattr(layer.perils, deductible_fetches[ded_layer.peril][0])
                    ded = getattr(ded_attr, deductible_fetches[ded_layer.peril][1])

                    ded_layer.ded_min.calculated = ded / ex_rate if ded and ex_rate else 0



# Async task (triggered by clicking a button) to import data from an expiring policy option into the current policy for rate change and analysis of movement
def generate_quote_doc(hxd, progress):
    manuscript = hxd.quote_documents.manuscript_flag

    inception_date = hxd.quote_documents.bpro_outputs.insured_from
    expiry_date = hxd.quote_documents.bpro_outputs.insured_until
    issue_date = hxd.quote_documents.issue_date
    broker_name = hxd.quote_documents.broker_name
    broker_address = hxd.quote_documents.broker_address
    insured_name = hxd.quote_documents.bpro_outputs.insured_name
    largest_tiv_address = hxd.quote_documents.key_location
    total_insurable_value = hxd.quote_documents.bpro_outputs.tiv
    premium = hxd.quote_documents.premium.property_only
    min_earned_percent = hxd.quote_documents.bpro_outputs.min_earned_pct
    actual_tria_premium = hxd.quote_documents.premium.tria
    actual_eb_premium = hxd.quote_documents.premium.equipment_breakdown
    inspection_fees = hxd.quote_documents.inspection_fees

    selected_layer = hxd.quote_documents.layer
    excess = hxd.quote_documents.excess
    written_line = hxd.quote_documents.written_line
    limit = hxd.quote_documents.bpro_outputs.limit
    brokerage = hxd.quote_documents.bpro_outputs.commission
    including_flood = hxd.quote_documents.including_flood
    including_quake = hxd.quote_documents.including_quake
    including_eb = hxd.quote_documents.including_eb

    issue_date_str = issue_date.strftime("%d-%b-%Y") if issue_date else "None"
    inception_date_str = inception_date.strftime("%d-%b-%Y")
    expiry_date_str = expiry_date.strftime("%d-%b-%Y")


    mailing_address = hxd.quote_documents.mailing_address
    red_date = f"({hxd.quote_documents.schedule_received_date})" if manuscript else ""
    standard_time = "Local Standard Time at the Location of the Property involved" if manuscript else "Standard Time at the Insured's Address"
    territory = "\n\tTerritory:\tU.S.A\n" if manuscript else ""

    

    # Format strings
    total_insurable_value_str=f"${total_insurable_value:,.2f}" if total_insurable_value else "$0"
    premium_str=f"${premium:,.2f}" if premium else "$0"
    min_earned_percent_str=f"{min_earned_percent*100:,.2f}%" if min_earned_percent else "0%"
    tria_str=f"${actual_tria_premium:,.2f}" if actual_tria_premium else "$0"
    equipment_breakdown_str = f"${actual_eb_premium:,.2f}" if actual_eb_premium else ("" if manuscript else "Not Applicable")
    inspection_fees_str = f"${inspection_fees}" if inspection_fees else ("$0" if manuscript else "*INSERT*")
    brokers_commission = f"{brokerage*100:,.2f}%" if brokerage else "$0"


    
    
    
    earthquake_name = "Earth Movement (Earthquake)" if manuscript else "Earthquake"
    eb_name = "Boiler & Machinery (Equipment Breakdown)" if manuscript else "Equipment Breakdown"
    perils_included_text = f"All Risks {including_flood} Flood, {including_quake} {earthquake_name} and {including_eb} {eb_name}."

    flood_text = "\n\n\tExcluding Flood at all properties located wholly or partially in a 100-year flood area, Special Flood Hazard Areas, or zones with an “A” and “V” prefix or X-shaded (as defined by FEMA)" if manuscript and including_flood else ""

    coverages = "Real Property, Personal Property, Business Interruption and Extra Expense" if manuscript else "" ## TODO: add special coverage

    
    excess_text = f"excess of ${excess}" if excess else "*INSERT*"
    # limit_text = f"{l imit:,.2f}" if limit else "*INSERT*" # TODO: check this is limit of liability

    liability_perc = f"${limit:,.2f} ({written_line*100:.2f}%) part of ${limit/written_line:,.2f} each occurence" if (written_line < 1) or (written_line is None) else f"{excess_text} Per Occurence"

    if including_flood and including_quake:
        liability_peril_text = f" in respect of Flood and {earthquake_name}"
    elif including_flood:
        liability_peril_text = f" in respect of Flood"
    elif including_quake:
        liability_peril_text = f" in respect of {earthquake_name}"
    else:
        liability_peril_text = ""

    
    conditions = ""
    if not manuscript:
        for e in endorsements():
            endorsement = getattr(hxd.quote_documents.endorsements, e)
            if endorsement.yesno:
                if endorsement.comments:
                    conditions += f"""{e}: {endorsement.comments}
                    """
                else:
                    conditions += f"""{e}
                    """

    form = "" if manuscript else special_form_subjectives(hxd)


    path = "manuscript.docx" if manuscript else "special_form.docx"
    template = os.path.join(os.path.dirname(__file__), path)
    document = MailMerge(template)

    document.merge(
        issue_date=issue_date_str,
        expiry_date=inception_date_str,
        recipient_name=broker_name,
        recipient_address=broker_address,
        insured_name=insured_name,
        key_location=largest_tiv_address,
        red_date=red_date,
        standard_time=standard_time,
        territory=territory,
        policy_start_date=inception_date_str,
        policy_end_date=expiry_date_str,
        perils_included=perils_included_text,
        flood_text=flood_text,
        coverages=coverages,
        liability_share=liability_perc,
        liability_perils=liability_peril_text,
        total_insurable_value=total_insurable_value_str,
        premium=premium_str,
        tria=tria_str,
        equipment_breakdown=equipment_breakdown_str,
        inspection_fees=inspection_fees_str,
        brokers_commission=brokers_commission,
        min_earned_percent=min_earned_percent_str,
        conditions=conditions,
        quote_comments=hxd.quote_documents.quote_comments,
        form=form,
        mailing_address=mailing_address,
    )

    
    deductible_perils = []
    for i in hxd.quote_documents.deductibles:
        if i.peril:
            if i.ded_pct:
                ded_str = f"{i.ded_pct:,.2f} Of Values Per Building, Per Occurrence ${i.ded_min.selected:,.0f} Minimum Per Occurrence"
            else:
                ded_str = f"${(i.ded_min.selected or 0):,.0f} Per Occurrence"
            
            deductible_perils.append({
                "peril_1_ded": f"{i.peril}",
                "peril_deductible_1": ded_str,
                "peril_deductible_comment_1": i.comments,
            })
    document.merge_rows("peril_1_ded", deductible_perils)

    sublimit_peril_list = [
        "ordinance_and_law",
        "wind",
        "wind_2",
        "quake",
        "quake_2",
        "flood"   
        ]

    sublimit_perils = []
    for peril in sublimit_peril_list:
        peril_sublimit = getattr(getattr(hxd.quote_documents.fixed_sublimits, peril), "val")

        if peril_sublimit:
            sublimit_perils.append({
                "peril_1_sublim": f"{peril}",
                "peril_sublimit_1": f"${peril_sublimit:,.2f} Per Occurrence",
                "peril_sublimit_comment_1": getattr(getattr(hxd.quote_documents.fixed_sublimits, peril), "comments"),
            })
    for i, s in enumerate(hxd.quote_documents.other_sublimits):
        if s.val or s.comments:
            sublimit_perils.append({
                "peril_1_sublim": f"Other{i}",
                "peril_sublimit_1": f"${s.val:,.2f} Per Occurrence",
                "peril_sublimit_comment_1": s.comments,
            })

    document.merge_rows("peril_1_sublim", sublimit_perils)

    if manuscript:
        coinsurance_coverage_list = {
            "Real Property, Personal Property": "pd", 
            "Business Interruption & Extra Expenses": "bi"
        }
    else:
        coinsurance_coverage_list = {
            "Buildings, Personal Property": "pd", 
            "Business Income": "bi"
        }

    coinsurance_coverages = []
    for coverage in coinsurance_coverage_list:
        coinsurance = getattr(getattr(hxd.quote_documents.coinsurance, coinsurance_coverage_list[coverage]), "pct")
        coinsurance_valuation = getattr(getattr(hxd.quote_documents.coinsurance, coinsurance_coverage_list[coverage]), "settlement")
        coinsurance_str = f"${coinsurance:,.2f}" if coinsurance else "Nil"
        coinsurance_coverages.append({
            "coinsurance_1": coinsurance_str,
            "coinsurance_valuation_1": coinsurance_valuation,
            "coinsurance_coverage_1": coverage,
        })
    document.merge_rows("coinsurance_1", coinsurance_coverages)

    with hxd.quote_documents.document.open("b") as f:
        document.write(f)
    






def special_form_subjectives(hxd):
    text = """
    Subjectivities:

    """

    subjectivities_counter = 1
    
    if hxd.quote_documents.subjectivities.loss_run:
        text += f"{subjectivities_counter}. Satisfactory 3-year Loss Runs or No Loss Letter received prior to binding.\n"
        subjectivities_counter += 1

    if hxd.quote_documents.subjectivities.favourable_inspection:
        text += f"{subjectivities_counter}. Favorable Inspection by Beazley E&S within 45 days of inception and Compliance to Recommendations as Applicable.\n"
        subjectivities_counter += 1

    if hxd.quote_documents.subjectivities.favourable_inspection:
        text += f"{subjectivities_counter}. Inspection contact name and phone number due within 14 days of binding\n"
        subjectivities_counter += 1

    return text




def endorsements():
    return [
        "additional_covered_property",
        "additional_property_not_covered",
        "burglary_or_robbery_safeguards",
        "civil_or_military_authority_ext",
        "condition_of_coverage",
        "condo_maintenance_fees",
        "condo_association_coverage",
        "endorcements_condo_maintenance_fees",
        "damage_to_roof_structure_limitation",
        "fire_and_explosion",
        "first_tier_wind_counties_and_parishes",
        "hurricane_minimum_earned_premium",
        "ingress_egress_extension",
        "limitations_on_coverage_for_roof_surfacing",
        "ordinance_or_law_increased_period_of_restoration",
        "outdoor_property_extension",
        "prior_loss_clause",
        "property_enhancement",
        "protective_safeguards",
        "second_tier_wind_counties_and_parishes",
        "theft_and_resulting_damage_limitation",
        "vacancy_permit",
        "vacant_or_unoccupied_limitatin",
        "values_limitation_clause",
        "wind_limitation",
        "windstorm_or_hail_exclusion",
    ]
