import hx
import pandas as pd
import numpy as np
import algorithms.utils_global_lists as lst


def calc_totals(hxd):
    layer = hxd.cds.layers[0]
    exp_agg = hxd.cds.exposure.aggregate
    cov = layer.coverages
        
    # This calculates the sub totals for each coverage, under the condition that it is both available
    # and selected to be included by the UW 

    lst_cover_vbl = lst.cover_hxd_vbl(hxd)

    # First table 'Form' in exposure sheet
    # Set requirements to only sum coverages that are available (given the form) and 
    # included (selected by UW)
    layer.subtotal_forms.coverage_premium_post_a_rating = sum([
      loop_cover.coverage_premium_post_a_rating for loop_cover in lst_cover_vbl[:23] if loop_cover.available and loop_cover.include
    ])
    layer.subtotal_forms.coverage_premium_post_a_rating_annual = layer.subtotal_forms.coverage_premium_post_a_rating / layer.term_adjustment

    # Safe deposit policy table 
    layer.subtotal_safe_deposit_policy.coverage_premium_post_a_rating = 0
    for loop_cover in lst_cover_vbl[23:25]:
        if loop_cover.available is True and loop_cover.include is True:
            layer.subtotal_safe_deposit_policy.coverage_premium_post_a_rating += loop_cover.coverage_premium_post_a_rating
    layer.subtotal_safe_deposit_policy.coverage_premium_post_a_rating_annual = layer.subtotal_safe_deposit_policy.coverage_premium_post_a_rating / layer.term_adjustment

    # Computer crime policy table
    layer.subtotal_computer_crime_policy.coverage_premium_post_a_rating = 0
    for loop_cover in lst_cover_vbl[25:]:
        if loop_cover.available is True and loop_cover.include is True:
            layer.subtotal_computer_crime_policy.coverage_premium_post_a_rating += loop_cover.coverage_premium_post_a_rating
    layer.subtotal_computer_crime_policy.coverage_premium_post_a_rating_annual = layer.subtotal_computer_crime_policy.coverage_premium_post_a_rating / layer.term_adjustment

    # Round premium to the nearest integer    
    # Summing to get total unity premium
    layer.unity_premium = 0
    for cover in lst.cover_hxd_vbl(hxd):
        if cover.final_include:
            cover.coverage_premium_post_experience = round(cover.coverage_premium_post_experience)
            layer.unity_premium += cover.coverage_premium_post_experience

    # Summing to get total final premium
    layer.final_premium = 0
    for cover in lst.cover_hxd_vbl(hxd):
        if cover.final_include:
            cover.coverage_premium_post_a_rating = round(cover.coverage_premium_post_a_rating)
            layer.final_premium += cover.coverage_premium_post_a_rating


    # Sum any premium bearing endorsements to total

    # Calculate annualised endorsement premiums
    for endt in layer.premium_bearing_endorsements:
        endt.premium = endt.premium_annual * layer.term_adjustment

    # Assume the unity premium for endorsements is equal to the charged premium (UW doesn't have benchmark estimates for endt)
    layer.premium_bearing_endorsements_total.premium = sum(endt.premium for endt in layer.premium_bearing_endorsements)
    layer.premium_bearing_endorsements_total.premium_annual = layer.premium_bearing_endorsements_total.premium / layer.term_adjustment
    layer.premium_bearing_endorsements_total.benchmark_premium = layer.premium_bearing_endorsements_total.premium