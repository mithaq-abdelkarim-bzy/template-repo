import hx
from algorithms.rate_utilities import one_layer, ratio

def show_and_hide_pages(hxd):
    sel = hxd.cds.cover_selection
    sel.show_cargo_cyber = False
    if sel.cover:
        sel.is_selected = True
        if sel.cover == "Cargo":
            sel.is_cargo = True
            sel.show_cargo_cyber = True
        elif sel.cover == "Specie":
            sel.is_specie = True
        elif sel.cover == "Con Loss":
            sel.is_conloss = True
        elif sel.cover =="Cargo Cyber":
            sel.is_cargo_cyber_dropdown = True
    #sel.is_cargo_cyber_combined = sel.is_cargo_cyber or sel.is_cargo_cyber_dropdown
    sel.is_cargo_cyber_combined = False
    if sel.is_cargo_cyber and sel.is_cargo:
        sel.is_cargo_cyber_combined = True
    if sel.is_cargo_cyber_dropdown:
        sel.is_cargo_cyber_combined = True
    # sel.is_selected = sel.is_cargo = sel.is_specie = sel.is_conloss = True # NOTE: uncomment for development

def show_and_hide_fields(hxd):
    sel = hxd.cds.cover_selection
    layer, cvg = one_layer(hxd)
    ct = cvg.cargo_transit
    cs = cvg.cargo_storage
    ss = cvg.specie_storage
    clt = cvg.conloss_transit
    clc = cvg.conloss

    # Double section reference
    layer.has_single_section_ref = not layer.has_double_section_ref
    
    if hxd.cds.standard_fields.rating_methodology == "Rater":
        # Sum checks
        ct_conv_condition = sum([ct.conv_air_factor, ct.conv_land_factor, ct.conv_sea_factor]) != 1
        clt_conv_condition = sum([clt.conv_air_factor, clt.conv_land_factor, clt.conv_sea_factor]) != 1
        clt_pack_condition = sum([clt.packaging_1_factor, clt.packaging_2_factor]) != 1

        # Cargo conveyance validation
        if sel.cover == "Cargo" and ct.transit_flag and ct_conv_condition:
            ct.conv_check_show = True
            ct.conv_check = "Conveyance splits must add up to 100%."
            hx.errors.validation("Conveyance splits in Cargo must add up to 100%.")

        # Cargo CAT exposure check
        ca_country_total_expo = sum([country.cat_expo for country in cs.countries])
        ca_cat_expo_ratio = ratio(ca_country_total_expo, cs.cat_expo)
        ca_cat_condition = cs.cat_expo > 0 and ca_cat_expo_ratio != 1

        if sel.cover == "Cargo" and cs.storage_flag and ca_cat_condition:
            cs.cat_expo_check_show = True
            cs.cat_expo_check = f"Total CAT exposure so far is {round(ca_cat_expo_ratio * 100, 2)}%"
            hx.errors.validation("Total CAT exposure in Cargo must add up to 100%.")

        # Specie CAT exposure check
        sp_country_total_expo = sum([country.cat_expo for country in ss.countries])
        sp_cat_expo_ratio = ratio(sp_country_total_expo, ss.cat_expo)
        sp_cat_condition = ss.cat_expo > 0 and sp_cat_expo_ratio != 1

        if sel.cover == "Specie" and ss.storage_flag and sp_cat_condition:
            ss.cat_expo_check_show = True
            ss.cat_expo_check = f"Total CAT exposure so far is {round(sp_cat_expo_ratio * 100, 2)}%"
            hx.errors.validation("Total CAT exposure in Specie must add up to 100%.")

        # Con Loss conveyance validation
        if sel.cover == "Con Loss" and clt.transit_flag and clt_conv_condition:
            clt.conv_check_show = True
            clt.conv_check = "Conveyance splits must add up to 100%."
            hx.errors.validation("Conveyance splits in Transit must add up to 100%.")
        
        # Con Loss packaging validation
        if sel.cover == "Con Loss" and clt.transit_flag and clt_pack_condition:
            clt.packaging_check_show = True
            clt.packaging_check = "Packaging splits must add up to 100%."
            hx.errors.validation("Packaging splits in Transit must add up to 100%.")

        # Con Loss indemnity and deductible validation
        if sel.cover == "Con Loss" and clc.conloss_flag:
            if not clc.deductible_level or not clc.indemnity_period:
                clc.indemnity_message_show = True
                hx.errors.validation("Please enter both the indemnity period and deductible in the Con Loss section.")

def allow_policy_doc_download(hxd):
    layer, cvg = one_layer(hxd)
    ct = cvg.cargo_transit
    cs = cvg.cargo_storage
    st = cvg.specie_transit
    ss = cvg.specie_storage
    clt = cvg.conloss_transit
    clc = cvg.conloss
    doc = hxd.policy_doc

    # Set up the premium condition
    coverages = {
        "Cargo": [ct, cs],
        "Specie": [st, ss],
        "Con Loss": [clt, clc]
    }
    cover = hxd.cds.cover_selection.cover
    hxd_cvg_list = coverages.get(cover, [])
    premium_condition = True

    # Get the selected subcoverages
    sub_cvg_selection = []
    if cover == "Cargo":
        sub_cvg_selection = [ct.transit_flag, cs.storage_flag]
    elif cover == "Specie":
        sub_cvg_selection = [st.transit_flag, ss.storage_flag]
    elif cover == "Con Loss":
        sub_cvg_selection = [clt.transit_flag, clc.conloss_flag]

    # Make premium_condition false if one the technical premiums in the sub-coverages has not been calculated
    for cvg, flag in zip(hxd_cvg_list, sub_cvg_selection):
        technical_premium = getattr(cvg, "technical_premium")
        condition = (technical_premium or 0) > 0 if flag else True # Don't invalidate if sub-coverage has not been selected
        premium_condition *= condition

    if layer.benchmark_premium <= 0:
        doc.premium_check = f"Gross Benchmark Premium has not been calculated. Please fill in the relevant fields in {cover}."
        doc.show_premium_check = True
    elif not premium_condition:
        doc.premium_check = "Gross Benchmark Premium has not been fully calculated. Please check the validation errors at the bottom right corner."
        doc.show_premium_check = True
    elif layer.quoted_premium <= 0:
        doc.premium_check = "Gross Quoted Premium should be greater than 0. Please input a valid number in Rating Summary."
        doc.show_premium_check = True
    else:
        doc.show_generate_button = True
            

def validate_status(hxd):
    layer, cvg = one_layer(hxd)

    finalizable_status = ["Bound", "Post Bind Complete"] 

    if layer.status not in finalizable_status:
        hx.errors.validation("If you wish to set the policy to Final, the Status in Rating Summary should be either 'Bound' or 'Post Bind Complete'.")

def validate_written_line(hxd):
    layer, cvg = one_layer(hxd)

    if layer.written_line is None:
        hx.errors.validation("Written Line cannot be blank.")

    if layer.written_line == 0:
        hx.errors.validation("Written Line cannot be 0.")     

def validate_currency(hxd):
    if hxd.cds.currencies.source_currency is None:
        hx.errors.validation("Currency cannot be blank.")