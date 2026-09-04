import hx
import datetime
from algorithms.rate_change import rate_change_rater
from algorithms.constant import MAX_OPTIONS
import os
from mailmerge import MailMerge
import pandas as pd



def update_first_saved(hxd, progress):
    hxd.rationale.first_saved = datetime.date.today()
    # hxd.rationale.button_text = "Saved"


def rationale_rater(hxd):
    if hxd.rationale.first_saved:
        hxd.rationale.show_save_button = False
        hxd.rationale.show_button_text = True
    else:
        hxd.rationale.show_save_button = True
        hxd.rationale.show_button_text = False


    hxd.rationale.show_dropdown = True
    hxd.rationale.show_bound = False
    lookup_layer = hxd.rationale.layers - 1 
    max_layer = 0
    for index, layer in enumerate(hxd.layers, start=1):
        max_layer += 1 
        if layer.status == "Bound":
            lookup_layer = index - 1
            hxd.rationale.bound_layer = f"Displaying data for Layer {index} - Bound Layer"
            hxd.rationale.show_dropdown = False
            hxd.rationale.show_bound = True

    uw_list_df = pd.DataFrame(hx.params.team)
    
    hxd.rationale.layer_label = hxd.layers[lookup_layer].layer_label if lookup_layer < max_layer else ""
 
    hxd.rationale.risk_information.risk_name = hxd.policy_information.insured
    hxd.rationale.risk_information.policy_ref = hxd.layers[lookup_layer].reference if lookup_layer < max_layer else ""
    hxd.rationale.risk_information.policy_period_start = hxd.hx_core.inception_date
    hxd.rationale.risk_information.policy_period_end = hxd.hx_core.expiry_date
    hxd.rationale.risk_information.underwriter = uw_list_df[uw_list_df["Initials"] == hxd.policy_information.underwriter]["Full Name"].iloc[0] if hxd.policy_information.underwriter != None else ""
    hxd.rationale.risk_information.broker = hxd.policy_information.broker_contact
    hxd.rationale.risk_information.tiv = hxd.schedule.schedule_total.tiv_total
    hxd.rationale.risk_information.occupancy = hxd.non_layer_perils.equipment_breakdown.occupancy.selected
    hxd.rationale.risk_information.new_renewal = hxd.layers[lookup_layer].new_renewal if lookup_layer < max_layer else ""

    hxd.rationale.rating_terms.limit = hxd.layers[lookup_layer].limit if lookup_layer < max_layer else None
    hxd.rationale.rating_terms.excess = hxd.layers[lookup_layer].excess if lookup_layer < max_layer else None

    if lookup_layer < max_layer and hxd.layers[lookup_layer].status in {'Bound', 'MTA', 'Cancellation'} :
        hxd.rationale.rating_terms.written_line = hxd.layers[lookup_layer].written_line_perc 
    elif lookup_layer < max_layer and hxd.layers[lookup_layer].quoted_line_perc:
        hxd.rationale.rating_terms.written_line = hxd.layers[lookup_layer].quoted_line_perc
    else :
        hxd.rationale.rating_terms.written_line = None 


    if lookup_layer < max_layer:
        if hxd.rationale.rating_terms.written_line == None or hxd.schedule.schedule_total.tiv_total == None:
            hxd.rationale.rating_terms.afb_exposure = None
        else: hxd.rationale.rating_terms.afb_exposure = (hxd.rationale.rating_terms.written_line) * min(hxd.layers[lookup_layer].limit, hxd.schedule.schedule_total.tiv_total)
    else: hxd.rationale.rating_terms.afb_exposure = None

    hxd.rationale.rating_terms_2.achieved_premium_100_gg = hxd.layers[lookup_layer].achieved_premium_100_gg if lookup_layer < max_layer else None
    hxd.rationale.rating_terms_2.commission = hxd.layers[lookup_layer].brokerage if lookup_layer < max_layer else None
    hxd.rationale.rating_terms_2.rate_change = hxd.rate_change.risk_adjusted_rate_change.underwriter

    hxd.rationale.natural_perils.tpi_post_uw_adj = hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.tpi if lookup_layer < max_layer else None

    exchange_rate = hxd.policy_information.exchange_rate or 1
    excess = hxd.layers[lookup_layer].excess if lookup_layer < max_layer else 0
    limit = hxd.layers[lookup_layer].limit if lookup_layer < max_layer else 0
    
    # gets peril sublimits
    hxd.rationale.natural_perils.fire.limit = (hxd.layers[lookup_layer].limit if not hxd.layers[lookup_layer].limit is None else 0 ) if lookup_layer < max_layer else None
    hxd.rationale.natural_perils.wildfire.limit = (hxd.layers[lookup_layer].limit if not hxd.layers[lookup_layer].limit is None else 0 ) if lookup_layer < max_layer else None
    
    for peril, peril_name in zip(("ws", "eq", "scs", "fl"), ("windstorm", "eq", "scs", "flood")):
        if  lookup_layer < max_layer:
            if not getattr(hxd.sublimit, f"{peril}_sublimit") is None and getattr(hxd.sublimit, f"{peril}_sublimit") > excess:
                setattr(getattr(hxd.rationale.natural_perils, f"{peril_name}"), "limit", min(int(getattr(hxd.sublimit, f"{peril}_sublimit")) - excess, limit))
            elif getattr(hxd.sublimit, f"{peril}_sublimit") is None:
                 setattr(getattr(hxd.rationale.natural_perils, f"{peril_name}"), "limit", limit)
            else:
                setattr(getattr(hxd.rationale.natural_perils,f"{peril_name}"), "limit", 0)
        else:
            setattr(getattr(hxd.rationale.natural_perils,f"{peril_name}"), "limit", None)

    # gets peril deductibles
    hxd.rationale.natural_perils.wildfire.deductible = (hxd.layers[lookup_layer].perils.wildfire.deductible if not hxd.layers[lookup_layer].perils.wildfire.deductible is None else 0) if lookup_layer < max_layer else None
    hxd.rationale.natural_perils.fire.deductible = (hxd.layers[lookup_layer].perils.fire.deductible if not hxd.layers[lookup_layer].perils.fire.deductible is None else 0) if lookup_layer < max_layer else None

    for peril, peril_name in zip(("windstorm", "eq", "scs", "flood"), ("named_windstorm", "quake", "scs", "flood")):
        if lookup_layer < max_layer:
            if not getattr(hxd.layers[lookup_layer].perils, f"{peril_name}").per_occurrence_ded is None:
                setattr(getattr(hxd.rationale.natural_perils, f"{peril}"), "deductible", getattr(hxd.layers[lookup_layer].perils, f"{peril_name}").per_occurrence_ded)
            else:
                setattr(getattr(hxd.rationale.natural_perils, f"{peril}"), "deductible", 0) 
        else:
            setattr(getattr(hxd.rationale.natural_perils, f"{peril}"), "deductible", None)
    
    # is ded structre complex? 
    hxd.rationale.natural_perils.fire.complex_ded_structure = "No" if lookup_layer < max_layer else None
    hxd.rationale.natural_perils.wildfire.complex_ded_structure = "No" if lookup_layer < max_layer else None
    
    for peril, peril_name in zip(("windstorm", "eq", "scs", "flood"), ("named_windstorm", "quake", "scs", "flood")):
        complex_ded = False
        if (lookup_layer < max_layer):
            for index in range(1, MAX_OPTIONS + 1):
                if(getattr(getattr(hxd.layers[lookup_layer].perils, f"{peril_name}").location_ded, f"option_{index}").type != None):
                    complex_ded = True
            if (complex_ded == True):
                getattr(hxd.rationale.natural_perils,f"{peril}").complex_ded_structure = "Yes"
            else: 
                getattr(hxd.rationale.natural_perils,f"{peril}").complex_ded_structure = "No"
        else: 
            getattr(hxd.rationale.natural_perils,f"{peril}").complex_ded_structure = None

    # gets peril prem data
    if lookup_layer < max_layer and hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat.tornado_us != None and  hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat.hail_us != None and hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat.tornado_intl != None and hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat.hail_intl != None:
        hxd.rationale.natural_perils.scs.premium = (hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat.tornado_us + hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat.hail_us + hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat.tornado_intl + hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat.hail_intl) * exchange_rate
    else: 
        hxd.rationale.natural_perils.scs.premium = None

    if lookup_layer < max_layer and hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.fire!= None:
        hxd.rationale.natural_perils.fire.premium = hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.fire
    else:
        hxd.rationale.natural_perils.fire.premium = None
    
       
    for peril, peril_name in zip(( "windstorm", "eq", "flood", "wildfire"), ("windstorm", "earthquake", "flood", "wildfire")):
        if lookup_layer < max_layer and getattr(hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat, f"{peril_name}_us") != None and  getattr(hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat, f"{peril_name}_intl") != None:
            peril_gross_tech_prem = (getattr(hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.us_cat, f"{peril_name}_us") + getattr(hxd.layers[lookup_layer].post_uw_adjustment.gross_tech_prem.intl_cat, f"{peril_name}_intl")) * exchange_rate
            setattr(getattr(hxd.rationale.natural_perils, f"{peril}"), "premium", peril_gross_tech_prem) 
        else:
            setattr(getattr(hxd.rationale.natural_perils, f"{peril}"), "premium", None)


def generate_uw_rationale_doc(hxd, progress):
    layer_str = f"{hxd.rationale.layers}" if hxd.rationale.layers else ""
    layer_label = hxd.rationale.layer_label
    date_saved = hxd.rationale.first_saved.strftime("%d-%b-%Y") if hxd.rationale.first_saved else ""
    risk_name = hxd.rationale.risk_information.risk_name
    policy_ref = hxd.rationale.risk_information.policy_ref
    policy_period_start_str = hxd.rationale.risk_information.policy_period_start.strftime("%d-%b-%Y")
    policy_period_end_str = hxd.rationale.risk_information.policy_period_end.strftime("%d-%b-%Y")
    underwriter =  hxd.rationale.risk_information.underwriter
    broker = hxd.rationale.risk_information.broker
    occupancy = hxd.rationale.risk_information.occupancy
    tiv_str = f"${hxd.rationale.risk_information.tiv:,.2f}" if hxd.rationale.risk_information.tiv else "$0"
    new_renewal = hxd.rationale.risk_information.new_renewal
    insurance_type = hxd.rationale.rating_terms.insurance_type
    limit_str =  f"${hxd.rationale.rating_terms.limit:,.2f}" if hxd.rationale.rating_terms.limit else "$0"
    excess_str = f"${hxd.rationale.rating_terms.excess:,.2f}" if hxd.rationale.rating_terms.excess else "$0"
    written_line_str = f"{hxd.rationale.rating_terms.written_line*100:,.2f}%" if hxd.rationale.rating_terms.written_line else "0%"
    afb_exposure_str = f"${hxd.rationale.rating_terms.afb_exposure:,.2f}" if hxd.rationale.rating_terms.afb_exposure else "$0"
    achieved_premium_100_gg_str = f"${hxd.rationale.rating_terms_2.achieved_premium_100_gg:,.2f}" if hxd.rationale.rating_terms_2.achieved_premium_100_gg else "$0"
    commission_str = f"{hxd.rationale.rating_terms_2.commission*100:,.2f}%" if hxd.rationale.rating_terms_2.commission else "0%"
    rate_change_str = f"{hxd.rationale.rating_terms_2.rate_change*100:,.2f}%" if hxd.rationale.rating_terms_2.rate_change else "0%"
    fire_limit_str = f"${hxd.rationale.natural_perils.fire.limit:,.2f}" if hxd.rationale.natural_perils.fire.limit else "$0"
    ws_limit_str = f"${hxd.rationale.natural_perils.windstorm.limit:,.2f}" if hxd.rationale.natural_perils.windstorm.limit else "$0"
    eq_limit_str = f"${hxd.rationale.natural_perils.eq.limit:,.2f}" if hxd.rationale.natural_perils.eq.limit else "$0"
    wf_limit_str = f"${hxd.rationale.natural_perils.wildfire.limit:,.2f}" if hxd.rationale.natural_perils.wildfire.limit else "$0"
    scs_limit_str = f"${hxd.rationale.natural_perils.scs.limit:,.2f}" if hxd.rationale.natural_perils.scs.limit else "$0"
    fl_limit_str = f"${hxd.rationale.natural_perils.flood.limit:,.2f}" if hxd.rationale.natural_perils.flood.limit else "$0"
    fire_ded_str = f"${hxd.rationale.natural_perils.fire.deductible:,.2f}" if hxd.rationale.natural_perils.fire.deductible else "$0"
    ws_ded_str = f"${hxd.rationale.natural_perils.windstorm.deductible:,.2f}" if hxd.rationale.natural_perils.windstorm.deductible else "$0"
    eq_ded_str = f"${hxd.rationale.natural_perils.eq.deductible:,.2f}" if hxd.rationale.natural_perils.eq.deductible else "$0"
    wf_ded_str = f"${hxd.rationale.natural_perils.wildfire.deductible:,.2f}" if hxd.rationale.natural_perils.wildfire.deductible else "$0"
    scs_ded_str = f"${hxd.rationale.natural_perils.scs.deductible:,.2f}" if hxd.rationale.natural_perils.scs.deductible else "$0"
    fl_ded_str = f"${hxd.rationale.natural_perils.flood.deductible:,.2f}" if hxd.rationale.natural_perils.flood.deductible else "$0"
    fire_complex_ded_str = hxd.rationale.natural_perils.fire.complex_ded_structure
    ws_complex_ded_str = hxd.rationale.natural_perils.windstorm.complex_ded_structure
    eq_complex_ded_str = hxd.rationale.natural_perils.eq.complex_ded_structure
    wf_complex_ded_str = hxd.rationale.natural_perils.wildfire.complex_ded_structure
    scs_complex_ded_str = hxd.rationale.natural_perils.scs.complex_ded_structure
    fl_complex_ded_str = hxd.rationale.natural_perils.flood.complex_ded_structure
    fire_prem_str = f"${hxd.rationale.natural_perils.fire.premium:,.2f}" if hxd.rationale.natural_perils.fire.premium else "$0"
    ws_prem_str = f"${hxd.rationale.natural_perils.windstorm.premium:,.2f}" if hxd.rationale.natural_perils.windstorm.premium else "$0"
    eq_prem_str = f"${hxd.rationale.natural_perils.eq.premium:,.2f}" if hxd.rationale.natural_perils.eq.premium else "$0"
    wf_prem_str = f"${hxd.rationale.natural_perils.wildfire.premium:,.2f}" if hxd.rationale.natural_perils.wildfire.premium else "$0"
    scs_prem_str = f"${hxd.rationale.natural_perils.scs.premium:,.2f}" if hxd.rationale.natural_perils.scs.premium else "$0"
    fl_prem_str = f"${hxd.rationale.natural_perils.flood.premium:,.2f}" if hxd.rationale.natural_perils.flood.premium else "$0"
    tpi_post_uw_adj_str = f"{ hxd.rationale.natural_perils.tpi_post_uw_adj*100:,.2f}%" if  hxd.rationale.natural_perils.tpi_post_uw_adj else "0%"
    adj_factor_reason = hxd.rationale.natural_perils.adj_factor_reason
    consortium = "Yes" if hxd.rationale.reinsurance.consortium is True else "No"
    fac_purchased = "Yes" if hxd.rationale.reinsurance.fac_purchased is True else "No"
    fac_structure = hxd.rationale.reinsurance.fac_structure
    description = hxd.rationale.note_section.description
    special_processing = hxd.rationale.note_section.special_processing
    underwriter_thoughts = hxd.rationale.note_section.underwriter_thoughts


   
    template = os.path.join(os.path.dirname(__file__), "rationale_documents/uw_rationale_doc.docx")
    document = MailMerge(template)

    document.merge(
        layer = layer_str,
        layer_label = layer_label,
        date_saved = date_saved,
        risk_name = risk_name,
        policy_ref = policy_ref,
        policy_start = policy_period_start_str,
        policy_end = policy_period_end_str,
        underwriter = underwriter,
        broker = broker,
        occupancy = occupancy,
        tiv = tiv_str,
        new_renewal = new_renewal,
        insurance_type = insurance_type,
        limit = limit_str,
        excess = excess_str,
        written_line = written_line_str,
        afb_exposure = afb_exposure_str,
        achieved_premium_100_gg = achieved_premium_100_gg_str,
        commission = commission_str,
        rate_change = rate_change_str,
        fire_limit = fire_limit_str,
        ws_limit = ws_limit_str,
        eq_limit = eq_limit_str,
        wf_limit = wf_limit_str,
        scs_limit = scs_limit_str,
        fl_limit = fl_limit_str, 
        fire_ded = fire_ded_str,
        ws_ded = ws_ded_str,
        eq_ded = eq_ded_str,
        wf_ded = wf_ded_str,
        scs_ded = scs_ded_str,
        fl_ded = fl_ded_str,
        fire_complex_ded = fire_complex_ded_str,
        ws_complex_ded = ws_complex_ded_str,
        eq_complex_ded = eq_complex_ded_str,
        wf_complex_ded = wf_complex_ded_str,
        scs_complex_ded = scs_complex_ded_str,
        fl_complex_ded = fl_complex_ded_str,
        fire_prem = fire_prem_str,
        ws_prem = ws_prem_str,
        eq_prem = eq_prem_str,
        wf_prem = wf_prem_str,
        scs_prem = scs_prem_str,
        fl_prem = fl_prem_str,
        tpi_post_uw_adj = tpi_post_uw_adj_str,
        adj_factor_reason = adj_factor_reason,
        consortium = consortium,
        fac_purchased = fac_purchased,
        fac_structure = fac_structure,
        description = description,
        special_processing = special_processing,
        underwriter_thoughts = underwriter_thoughts
        )

    with hxd.rationale.document.open("b") as f:
        document.write(f)
