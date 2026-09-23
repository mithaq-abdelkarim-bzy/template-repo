import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from operator import itemgetter

# SA: If these are depreciated, they should be removed! You have version history natively in the branch
# menu so you can always go back to a previous version if needed!

def rate_fine_art(hxd, df):
    
    # 0. DECLARE PARAMETERS -------------------------------------------------------------------------
    df = df # data frame created from exposure input
    fa_premises_rates = hx.params.table_rating_fa_premises
    fa_travel_rates = hx.params.table_rating_fa_travel
    fa_additional_rates = hx.params.table_rating_jfas_all_additional
    fa_additional_rates = fa_additional_rates[fa_additional_rates["class"] == "Fine Art"]

    table_rating_exposure_curves = hx.params.table_rating_exposure_curves

    # Generate summaries by premise
    df["exp_band_1"] = df["tsi_band_1"] + df["tsi_band_2"]
    df["exp_band_2"] = df["tsi_band_3"] + df["tsi_band_4"]
    df["exp_band_3"] = df["tsi_band_5"]
    df["exp_band_4"] = df["tsi_band_6"]
    df["exp_band_5"] = df["tsi_band_7"]
    df["exp_band_6"] = df["tsi_band_8"]
    df["exp_band_7"] = df["tsi_band_9"]
    df["exp_band_8"] = df["tsi_band_10"]

    # Attach rates
    df = df.merge(fa_premises_rates, how="left", left_on=["type", "country"], right_on=["type", "country"])

    df["premium"] = (df["exp_band_1"] * df["1000000"] + 
                    df["exp_band_2"] * df["3000000"] + 
                    df["exp_band_3"] * df["5000000"] + 
                    df["exp_band_4"] * df["10000000"] + 
                    df["exp_band_5"] * df["20000000"] + 
                    df["exp_band_6"] * df["50000000"] + 
                    df["exp_band_7"] * df["100000000"] + 
                    df["exp_band_8"] * df[">100m"])

    for premise in ("Static Art", "Exhibitions", "FA Misc"):
        df_summary = df[df["type"]==premise]
        df_summary_1 = df_summary[["country", "tsi_cnv", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]].groupby("country", as_index=False).sum()
        df_summary_1 = df_summary_1.rename(columns={"tsi_cnv": "tsi"})
        setattr(hxd, "fa_" + premise.replace(" ", "_").lower() + "_summary", df_summary_1.to_dict("records"))
        setattr(hxd, "fa_" + premise.replace(" ", "_").lower() + "_summary_subtotal", df_summary_1[["tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]].sum().to_dict())

        df_summary = df[df["type"]==premise]
        df_summary_2 = df_summary[["country", "1000000", "3000000", "5000000", "10000000", "20000000", "50000000", "100000000", ">100m"]].groupby("country", as_index=False).mean()
        df_summary_2 = df_summary_2.rename(columns={"1000000": "exp_band_1"})
        df_summary_2 = df_summary_2.rename(columns={"3000000": "exp_band_2"})
        df_summary_2 = df_summary_2.rename(columns={"5000000": "exp_band_3"})
        df_summary_2 = df_summary_2.rename(columns={"10000000": "exp_band_4"})
        df_summary_2 = df_summary_2.rename(columns={"20000000": "exp_band_5"})
        df_summary_2 = df_summary_2.rename(columns={"50000000": "exp_band_6"})
        df_summary_2 = df_summary_2.rename(columns={"100000000": "exp_band_7"})
        df_summary_2 = df_summary_2.rename(columns={">100m": "exp_band_8"})
        setattr(hxd, "fa_" + premise.replace(" ", "_").lower() + "_summary_rates", df_summary_2.to_dict("records"))
        # END LOOP
    
    premises_static_art_premium = df[df["type"] == "Static Art"]["premium"].sum()
    premises_exhibitions_premium = df[df["type"] == "Exhibitions"]["premium"].sum()
    premises_fa_misc_premium = df[df["type"] == "FA Misc"]["premium"].sum()

    cov.fa_premises_summary.premium = premises_static_art_premium + premises_exhibitions_premium + premises_fa_misc_premium
    cov.fa_premises_summary.tsi = df["tsi_cnv"].sum()



    # TRACVEL RATING ----------------------------------------------
    # DECLARE RATES

    rate_travel_within_city = fa_travel_rates[fa_travel_rates["travel_type"] == "Transits within city"]["rate"].iloc[0]
    rate_travel_within_country = fa_travel_rates[fa_travel_rates["travel_type"] == "Transits within country"]["rate"].iloc[0]
    rate_travel_within_eu = fa_travel_rates[fa_travel_rates["travel_type"] == "Transits within EU"]["rate"].iloc[0]
    rate_travel_eu_us = fa_travel_rates[fa_travel_rates["travel_type"] == "Transits EU - USA"]["rate"].iloc[0]
    rate_travel_row = fa_travel_rates[fa_travel_rates["travel_type"] == "Transits ROW"]["rate"].iloc[0]


    hxd.fa_travel_rating_transitswithincity.prem_rate_per_100_tsi = rate_travel_within_city
    hxd.fa_travel_rating_transitswithincountry.prem_rate_per_100_tsi = rate_travel_within_country
    hxd.fa_travel_rating_transitswithineu.prem_rate_per_100_tsi = rate_travel_within_eu
    hxd.fa_travel_rating_transitseuusa.prem_rate_per_100_tsi = rate_travel_eu_us
    hxd.fa_travel_rating_transitsrow.prem_rate_per_100_tsi = rate_travel_row

    # TRAVEL PREMIUM

    if hxd.fa_travel_rating_transitswithincity.uw_rate_per_100_tsi is not None and hxd.fa_travel_rating_transitswithincity.uw_rate_per_100_tsi > 0:
        hxd.fa_travel_rating_transitswithincity.premium = hxd.fa_travel_rating_transitswithincity.tsi * hxd.fa_travel_rating_transitswithincity.uw_rate_per_100_tsi
    else:
        hxd.fa_travel_rating_transitswithincity.premium = hxd.fa_travel_rating_transitswithincity.tsi * rate_travel_within_city

    if hxd.fa_travel_rating_transitswithincountry.uw_rate_per_100_tsi is not None and hxd.fa_travel_rating_transitswithincountry.uw_rate_per_100_tsi > 0:
        hxd.fa_travel_rating_transitswithincountry.premium = hxd.fa_travel_rating_transitswithincountry.tsi * hxd.fa_travel_rating_transitswithincountry.uw_rate_per_100_tsi
    else:
        hxd.fa_travel_rating_transitswithincountry.premium = hxd.fa_travel_rating_transitswithincountry.tsi * rate_travel_within_country

    if hxd.fa_travel_rating_transitswithineu.uw_rate_per_100_tsi is not None and hxd.fa_travel_rating_transitswithineu.uw_rate_per_100_tsi > 0:
        hxd.fa_travel_rating_transitswithineu.premium = hxd.fa_travel_rating_transitswithineu.tsi * hxd.fa_travel_rating_transitswithineu.uw_rate_per_100_tsi
    else:
        hxd.fa_travel_rating_transitswithineu.premium = hxd.fa_travel_rating_transitswithineu.tsi * rate_travel_within_eu

    if hxd.fa_travel_rating_transitseuusa.uw_rate_per_100_tsi is not None and hxd.fa_travel_rating_transitseuusa.uw_rate_per_100_tsi > 0:
        hxd.fa_travel_rating_transitseuusa.premium = hxd.fa_travel_rating_transitseuusa.tsi * hxd.fa_travel_rating_transitseuusa.uw_rate_per_100_tsi
    else:
        hxd.fa_travel_rating_transitseuusa.premium = hxd.fa_travel_rating_transitseuusa.tsi * rate_travel_eu_us

    if hxd.fa_travel_rating_transitsrow.uw_rate_per_100_tsi is not None and hxd.fa_travel_rating_transitsrow.uw_rate_per_100_tsi > 0:
        hxd.fa_travel_rating_transitsrow.premium = hxd.fa_travel_rating_transitsrow.tsi * hxd.fa_travel_rating_transitsrow.uw_rate_per_100_tsi
    else:
        hxd.fa_travel_rating_transitsrow.premium = hxd.fa_travel_rating_transitsrow.tsi * rate_travel_row

    # TRAVEL SUMMARY

    cov.fa_travel_summary.premium = (
        hxd.fa_travel_rating_transitswithincity.premium + 
        hxd.fa_travel_rating_transitswithincountry.premium + 
        hxd.fa_travel_rating_transitswithineu.premium + 
        hxd.fa_travel_rating_transitseuusa.premium + 
        hxd.fa_travel_rating_transitsrow.premium
    )

    cov.fa_travel_summary.tsi = (
        hxd.fa_travel_rating_transitswithincity.tsi + 
        hxd.fa_travel_rating_transitswithincountry.tsi + 
        hxd.fa_travel_rating_transitswithineu.tsi + 
        hxd.fa_travel_rating_transitseuusa.tsi + 
        hxd.fa_travel_rating_transitsrow.tsi
    )


    # ADDITIONAL RATING ----------------------------------------------
    # DECLARE RATES

    rate_additional_dt = fa_additional_rates[fa_additional_rates["peril_group"] == "Defective Title"]["rate"].iloc[0]
    rate_additional_cl = fa_additional_rates[fa_additional_rates["peril_group"] == "Computers/Laptops"]["rate"].iloc[0]
    rate_additional_g = fa_additional_rates[fa_additional_rates["peril_group"] == "Glass"]["rate"].iloc[0]
    rate_additional_jis = fa_additional_rates[fa_additional_rates["peril_group"] == "Jewellery in safe"]["rate"].iloc[0]
    rate_additional_jw = fa_additional_rates[fa_additional_rates["peril_group"] == "Jewellery worn"]["rate"].iloc[0]
    rate_additional_lr = fa_additional_rates[fa_additional_rates["peril_group"] == "Library/Reference"]["rate"].iloc[0]
    rate_additional_m = fa_additional_rates[fa_additional_rates["peril_group"] == "Money"]["rate"].iloc[0]
    rate_additional_oc = fa_additional_rates[fa_additional_rates["peril_group"] == "Office Contents"]["rate"].iloc[0]

    hxd.fa_specific_additional_defectivetitle.prem_rate_per_100_tsi = rate_additional_dt
    hxd.fa_specific_additional_computerslaptops.prem_rate_per_100_tsi = rate_additional_cl
    hxd.fa_specific_additional_glass.prem_rate_per_100_tsi = rate_additional_g
    hxd.fa_specific_additional_jewelleryinsafe.prem_rate_per_100_tsi = rate_additional_jis
    hxd.fa_specific_additional_jewelleryworn.prem_rate_per_100_tsi = rate_additional_jw
    hxd.fa_specific_additional_libraryreference.prem_rate_per_100_tsi = rate_additional_lr
    hxd.fa_specific_additional_money.prem_rate_per_100_tsi = rate_additional_m
    hxd.fa_specific_additional_officecontents.prem_rate_per_100_tsi = rate_additional_oc
    # hxd.fa_specific_additional_custom.prem_rate_per_100_tsi = 0.0025

    # PREMIUM
    if hxd.fa_specific_additional_defectivetitle.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_defectivetitle.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_defectivetitle.premium = hxd.fa_specific_additional_defectivetitle.tsi * hxd.fa_specific_additional_defectivetitle.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_defectivetitle.premium = hxd.fa_specific_additional_defectivetitle.tsi * rate_additional_dt

    if hxd.fa_specific_additional_computerslaptops.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_computerslaptops.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_computerslaptops.premium = hxd.fa_specific_additional_computerslaptops.tsi * hxd.fa_specific_additional_computerslaptops.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_computerslaptops.premium = hxd.fa_specific_additional_computerslaptops.tsi * rate_additional_cl
    
    if hxd.fa_specific_additional_glass.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_glass.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_glass.premium = hxd.fa_specific_additional_glass.tsi * hxd.fa_specific_additional_glass.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_glass.premium = hxd.fa_specific_additional_glass.tsi * rate_additional_g
    
    if hxd.fa_specific_additional_jewelleryinsafe.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_jewelleryinsafe.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_jewelleryinsafe.premium = hxd.fa_specific_additional_jewelleryinsafe.tsi * hxd.fa_specific_additional_jewelleryinsafe.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_jewelleryinsafe.premium = hxd.fa_specific_additional_jewelleryinsafe.tsi * rate_additional_jis
    
    if hxd.fa_specific_additional_jewelleryworn.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_jewelleryworn.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_jewelleryworn.premium = hxd.fa_specific_additional_jewelleryworn.tsi * hxd.fa_specific_additional_jewelleryworn.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_jewelleryworn.premium = hxd.fa_specific_additional_jewelleryworn.tsi * rate_additional_jw
    
    if hxd.fa_specific_additional_libraryreference.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_libraryreference.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_libraryreference.premium = hxd.fa_specific_additional_libraryreference.tsi * hxd.fa_specific_additional_libraryreference.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_libraryreference.premium = hxd.fa_specific_additional_libraryreference.tsi * rate_additional_lr
    
    if hxd.fa_specific_additional_money.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_money.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_money.premium = hxd.fa_specific_additional_money.tsi * hxd.fa_specific_additional_money.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_money.premium = hxd.fa_specific_additional_money.tsi * rate_additional_m
    
    if hxd.fa_specific_additional_officecontents.uw_rate_per_100_tsi is not None and hxd.fa_specific_additional_officecontents.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_additional_officecontents.premium = hxd.fa_specific_additional_officecontents.tsi * hxd.fa_specific_additional_officecontents.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_additional_officecontents.premium = hxd.fa_specific_additional_officecontents.tsi * rate_additional_oc
    
    # TOTAL PREMIUM AND TOTAL SI
    total_additional_premium = (
        hxd.fa_specific_additional_defectivetitle.premium +
        hxd.fa_specific_additional_computerslaptops.premium +
        hxd.fa_specific_additional_glass.premium +
        hxd.fa_specific_additional_jewelleryinsafe.premium +
        hxd.fa_specific_additional_jewelleryworn.premium +
        hxd.fa_specific_additional_libraryreference.premium +
        hxd.fa_specific_additional_money.premium +
        hxd.fa_specific_additional_officecontents.premium
    )

    total_additional_tsi = (
        hxd.fa_specific_additional_defectivetitle.tsi +
        hxd.fa_specific_additional_computerslaptops.tsi +
        hxd.fa_specific_additional_glass.tsi +
        hxd.fa_specific_additional_jewelleryinsafe.tsi +
        hxd.fa_specific_additional_jewelleryworn.tsi +
        hxd.fa_specific_additional_libraryreference.tsi +
        hxd.fa_specific_additional_money.tsi +
        hxd.fa_specific_additional_officecontents.tsi
    )

    # ANCILLIARY RATING ----------------------------------------------
    rate_ancilliary_bi = fa_additional_rates[fa_additional_rates["peril_group"] == "BI"]["rate"].iloc[0]
    rate_ancilliary_bl = fa_additional_rates[fa_additional_rates["peril_group"] == "Buildings"]["rate"].iloc[0]
    rate_ancilliary_t = fa_additional_rates[fa_additional_rates["peril_group"] == "Terrorism"]["rate"].iloc[0]

    hxd.fa_specific_ancilliary_bi.prem_rate_per_100_tsi = rate_ancilliary_bi
    hxd.fa_specific_ancilliary_buildings.prem_rate_per_100_tsi = rate_ancilliary_bl
    hxd.fa_specific_ancilliary_terrorism.prem_rate_per_100_tsi = rate_ancilliary_t

    if hxd.fa_specific_ancilliary_bi.uw_rate_per_100_tsi is not None and hxd.fa_specific_ancilliary_bi.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_ancilliary_bi.premium = hxd.fa_specific_ancilliary_bi.tsi * hxd.fa_specific_ancilliary_bi.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_ancilliary_bi.premium = hxd.fa_specific_ancilliary_bi.tsi * rate_ancilliary_bi

    if hxd.fa_specific_ancilliary_buildings.uw_rate_per_100_tsi is not None and hxd.fa_specific_ancilliary_buildings.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_ancilliary_buildings.premium = hxd.fa_specific_ancilliary_buildings.tsi * hxd.fa_specific_ancilliary_buildings.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_ancilliary_buildings.premium = hxd.fa_specific_ancilliary_buildings.tsi * rate_ancilliary_bl

    if hxd.fa_specific_ancilliary_terrorism.uw_rate_per_100_tsi is not None and hxd.fa_specific_ancilliary_terrorism.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_ancilliary_terrorism.premium = hxd.fa_specific_ancilliary_terrorism.tsi * hxd.fa_specific_ancilliary_terrorism.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_ancilliary_terrorism.premium = hxd.fa_specific_ancilliary_terrorism.tsi * rate_ancilliary_t

    # TOTAL PREMIUM AND TOTAL SI
    total_ancilliary_premium = (
        hxd.fa_specific_ancilliary_bi.premium +
        hxd.fa_specific_ancilliary_buildings.premium +
        hxd.fa_specific_ancilliary_terrorism.premium
    )

    total_ancilliary_tsi = (
        hxd.fa_specific_ancilliary_bi.tsi +
        hxd.fa_specific_ancilliary_buildings.tsi +
        hxd.fa_specific_ancilliary_terrorism.tsi 
    )

    # EXHIBITIONS RATING ----------------------------------------------
    rate_exhibitions_natcat = fa_additional_rates[(fa_additional_rates["peril_group"] == "Nat cat") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_stay = fa_additional_rates[(fa_additional_rates["peril_group"] == "Stay") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_ter = fa_additional_rates[(fa_additional_rates["peril_group"] == "Terrorism") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]

    rate_exhibitions_transit_within_city = fa_additional_rates[(fa_additional_rates["peril_group"] == "Transits within city") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_transit_within_country = fa_additional_rates[(fa_additional_rates["peril_group"] == "Transits within country") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_transit_within_eu = fa_additional_rates[(fa_additional_rates["peril_group"] == "Transits within EU") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_transit_eu_usa = fa_additional_rates[(fa_additional_rates["peril_group"] == "Transits EU - USA") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]
    rate_exhibitions_transit_row = fa_additional_rates[(fa_additional_rates["peril_group"] == "Transits ROW") & (fa_additional_rates["peril_type"] == "Exhibitions")]["rate"].iloc[0]

    hxd.fa_specific_exhibitions_natcat.prem_rate_per_100_tsi = rate_exhibitions_natcat
    hxd.fa_specific_exhibitions_stay.prem_rate_per_100_tsi = rate_exhibitions_stay
    hxd.fa_specific_exhibitions_terrorism.prem_rate_per_100_tsi = rate_exhibitions_ter

    hxd.fa_specific_exhibitions_transit_transitswithincity.prem_rate_per_100_tsi = rate_exhibitions_transit_within_city
    hxd.fa_specific_exhibitions_transit_transitswithincountry.prem_rate_per_100_tsi = rate_exhibitions_transit_within_country
    hxd.fa_specific_exhibitions_transit_transitswithineu.prem_rate_per_100_tsi = rate_exhibitions_transit_within_eu
    hxd.fa_specific_exhibitions_transit_transitseuusa.prem_rate_per_100_tsi = rate_exhibitions_transit_eu_usa
    hxd.fa_specific_exhibitions_transit_transitsrow.prem_rate_per_100_tsi = rate_exhibitions_transit_row

    # PREMIUM _ EXHIBITIONS
    if hxd.fa_specific_exhibitions_natcat.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_natcat.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_natcat.premium = hxd.fa_specific_exhibitions_natcat.tsi * hxd.fa_specific_exhibitions_natcat.no_of_transits_per_month * hxd.fa_specific_exhibitions_natcat.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_natcat.premium = hxd.fa_specific_exhibitions_natcat.tsi * hxd.fa_specific_exhibitions_natcat.no_of_transits_per_month * rate_exhibitions_natcat

    if hxd.fa_specific_exhibitions_stay.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_stay.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_stay.premium = hxd.fa_specific_exhibitions_stay.tsi * hxd.fa_specific_exhibitions_stay.no_of_transits_per_month * hxd.fa_specific_exhibitions_stay.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_stay.premium = hxd.fa_specific_exhibitions_stay.tsi * hxd.fa_specific_exhibitions_stay.no_of_transits_per_month * rate_exhibitions_stay

        
    if hxd.fa_specific_exhibitions_terrorism.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_terrorism.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_terrorism.premium = hxd.fa_specific_exhibitions_terrorism.tsi * hxd.fa_specific_exhibitions_terrorism.no_of_transits_per_month * hxd.fa_specific_exhibitions_terrorism.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_terrorism.premium = hxd.fa_specific_exhibitions_terrorism.tsi * hxd.fa_specific_exhibitions_terrorism.no_of_transits_per_month * rate_exhibitions_ter

    # PREMIUM _ EXHIBITIONS TRANSIT
    if hxd.fa_specific_exhibitions_transit_transitswithincity.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_transit_transitswithincity.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_transit_transitswithincity.premium = hxd.fa_specific_exhibitions_transit_transitswithincity.tsi * hxd.fa_specific_exhibitions_transit_transitswithincity.no_of_transits_each_way * hxd.fa_specific_exhibitions_transit_transitswithincity.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_transit_transitswithincity.premium = hxd.fa_specific_exhibitions_transit_transitswithincity.tsi * hxd.fa_specific_exhibitions_transit_transitswithincity.no_of_transits_each_way * rate_exhibitions_transit_within_city

    if hxd.fa_specific_exhibitions_transit_transitswithincountry.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_transit_transitswithincountry.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_transit_transitswithincountry.premium = hxd.fa_specific_exhibitions_transit_transitswithincountry.tsi * hxd.fa_specific_exhibitions_transit_transitswithincountry.no_of_transits_each_way * hxd.fa_specific_exhibitions_transit_transitswithincountry.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_transit_transitswithincountry.premium = hxd.fa_specific_exhibitions_transit_transitswithincountry.tsi * hxd.fa_specific_exhibitions_transit_transitswithincountry.no_of_transits_each_way * rate_exhibitions_transit_within_country

    if hxd.fa_specific_exhibitions_transit_transitswithineu.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_transit_transitswithineu.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_transit_transitswithineu.premium = hxd.fa_specific_exhibitions_transit_transitswithineu.tsi * hxd.fa_specific_exhibitions_transit_transitswithincountry.no_of_transits_each_way * hxd.fa_specific_exhibitions_transit_transitswithineu.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_transit_transitswithineu.premium = hxd.fa_specific_exhibitions_transit_transitswithineu.tsi * hxd.fa_specific_exhibitions_transit_transitswithineu.no_of_transits_each_way * rate_exhibitions_transit_within_eu

    if hxd.fa_specific_exhibitions_transit_transitseuusa.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_transit_transitseuusa.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_transit_transitseuusa.premium = hxd.fa_specific_exhibitions_transit_transitseuusa.tsi * hxd.fa_specific_exhibitions_transit_transitseuusa.no_of_transits_each_way * hxd.fa_specific_exhibitions_transit_transitseuusa.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_transit_transitseuusa.premium = hxd.fa_specific_exhibitions_transit_transitseuusa.tsi * hxd.fa_specific_exhibitions_transit_transitseuusa.no_of_transits_each_way * rate_exhibitions_transit_eu_usa

    if hxd.fa_specific_exhibitions_transit_transitsrow.uw_rate_per_100_tsi is not None and hxd.fa_specific_exhibitions_transit_transitsrow.uw_rate_per_100_tsi > 0:
        hxd.fa_specific_exhibitions_transit_transitsrow.premium = hxd.fa_specific_exhibitions_transit_transitsrow.tsi * hxd.fa_specific_exhibitions_transit_transitsrow.no_of_transits_each_way * hxd.fa_specific_exhibitions_transit_transitsrow.uw_rate_per_100_tsi
    else:
        hxd.fa_specific_exhibitions_transit_transitsrow.premium = hxd.fa_specific_exhibitions_transit_transitsrow.tsi * hxd.fa_specific_exhibitions_transit_transitsrow.no_of_transits_each_way * rate_exhibitions_transit_row


    # TOTAL PREMIUM AND TOTAL SI
    total_exhibitions_premium = (
        hxd.fa_specific_exhibitions_natcat.premium +
        hxd.fa_specific_exhibitions_stay.premium +
        hxd.fa_specific_exhibitions_terrorism.premium + 

        hxd.fa_specific_exhibitions_transit_transitswithincity.premium + 
        hxd.fa_specific_exhibitions_transit_transitswithincountry.premium + 
        hxd.fa_specific_exhibitions_transit_transitswithineu.premium + 
        hxd.fa_specific_exhibitions_transit_transitseuusa.premium + 
        hxd.fa_specific_exhibitions_transit_transitsrow.premium
    )

    total_exhibitions_tsi = (
        hxd.fa_specific_exhibitions_natcat.tsi +
        hxd.fa_specific_exhibitions_stay.tsi +
        hxd.fa_specific_exhibitions_terrorism.tsi + 

        hxd.fa_specific_exhibitions_transit_transitswithincity.tsi + 
        hxd.fa_specific_exhibitions_transit_transitswithincountry.tsi + 
        hxd.fa_specific_exhibitions_transit_transitswithineu.tsi + 
        hxd.fa_specific_exhibitions_transit_transitseuusa.tsi + 
        hxd.fa_specific_exhibitions_transit_transitsrow.tsi
    )

    # LIABILITY -------------------------------------

    rate_liabilities_base = fa_additional_rates[(fa_additional_rates["peril_group"] == "Base Premium") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_5_10 = fa_additional_rates[(fa_additional_rates["peril_group"] == "5-10 employees") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_10_20 = fa_additional_rates[(fa_additional_rates["peril_group"] == "10-20 employees") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_20plus = fa_additional_rates[(fa_additional_rates["peril_group"] == "20+ employees") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    
    rate_liabilities_wood = fa_additional_rates[(fa_additional_rates["peril_group"] == "Woodworkers") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_ware = fa_additional_rates[(fa_additional_rates["peril_group"] == "Warehouseman") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_driv = fa_additional_rates[(fa_additional_rates["peril_group"] == "Drivers") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    rate_liabilities_metpol = fa_additional_rates[(fa_additional_rates["peril_group"] == "Metalworkers & Polishers") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]
    
    rate_liabilities_publiab = fa_additional_rates[(fa_additional_rates["peril_group"] == "Public Liability") & (fa_additional_rates["peril_type"] == "Liabilities")]["rate"].iloc[0]


    hxd.fa_specific_liability_employers_base_premium.per_employee = rate_liabilities_base
    hxd.fa_specific_liability_employers_5_10_employees.per_employee = rate_liabilities_5_10
    hxd.fa_specific_liability_employers_10_20_employees.per_employee = rate_liabilities_10_20
    hxd.fa_specific_liability_employers_20_or_more_employees.per_employee = rate_liabilities_20plus
    
    hxd.fa_specific_liability_manual_woodworkers.prem_rate = rate_liabilities_wood
    hxd.fa_specific_liability_manual_warehouseman.prem_rate = rate_liabilities_ware
    hxd.fa_specific_liability_manual_drivers.prem_rate = rate_liabilities_driv
    hxd.fa_specific_liability_manual_metalworkerspolishers.prem_rate = rate_liabilities_metpol

    # Employers Liability Premium
    if hxd.fa_specific_liability_employers_base_premium.no_of_employees is not None and hxd.fa_specific_liability_employers_base_premium.no_of_employees > 0:
        hxd.fa_specific_liability_employers_base_premium.premium = rate_liabilities_base
    else:
        hxd.fa_specific_liability_employers_base_premium.premium = 0

    if hxd.fa_specific_liability_employers_5_10_employees.no_of_employees is not None and hxd.fa_specific_liability_employers_5_10_employees.no_of_employees > 0 and hxd.fa_specific_liability_employers_base_premium.no_of_employees is not None and hxd.fa_specific_liability_employers_base_premium.no_of_employees:
        hxd.fa_specific_liability_employers_5_10_employees.premium = max(0, min(10, hxd.fa_specific_liability_employers_5_10_employees.no_of_employees)) * rate_liabilities_5_10
    else:
        hxd.fa_specific_liability_employers_5_10_employees.premium = 0

    if hxd.fa_specific_liability_employers_10_20_employees.no_of_employees is not None and hxd.fa_specific_liability_employers_10_20_employees.no_of_employees > 0 and hxd.fa_specific_liability_employers_base_premium.no_of_employees is not None and hxd.fa_specific_liability_employers_base_premium.no_of_employees:
        hxd.fa_specific_liability_employers_10_20_employees.premium = max(0, min(10, hxd.fa_specific_liability_employers_10_20_employees.no_of_employees)) * rate_liabilities_10_20
    else:
        hxd.fa_specific_liability_employers_10_20_employees.premium = 0

    if hxd.fa_specific_liability_employers_20_or_more_employees.no_of_employees is not None and hxd.fa_specific_liability_employers_20_or_more_employees.no_of_employees > 0 and hxd.fa_specific_liability_employers_base_premium.no_of_employees is not None and hxd.fa_specific_liability_employers_base_premium.no_of_employees:
        hxd.fa_specific_liability_employers_20_or_more_employees.premium = hxd.fa_specific_liability_employers_20_or_more_employees.no_of_employees * rate_liabilities_20plus
    else:
        hxd.fa_specific_liability_employers_20_or_more_employees.premium = 0

    # Manual Work Surcharge Premium
    if hxd.fa_specific_liability_manual_woodworkers.salary is not None and hxd.fa_specific_liability_manual_woodworkers.salary > 0:
        hxd.fa_specific_liability_manual_woodworkers.premium = hxd.fa_specific_liability_manual_woodworkers.salary * rate_liabilities_wood
    else:
        hxd.fa_specific_liability_manual_woodworkers.premium = 0  

    if hxd.fa_specific_liability_manual_warehouseman.salary is not None and hxd.fa_specific_liability_manual_warehouseman.salary > 0:
        hxd.fa_specific_liability_manual_warehouseman.premium = hxd.fa_specific_liability_manual_warehouseman.salary * rate_liabilities_ware
    else:
        hxd.fa_specific_liability_manual_warehouseman.premium = 0  

    if hxd.fa_specific_liability_manual_drivers.salary is not None and hxd.fa_specific_liability_manual_drivers.salary > 0:
        hxd.fa_specific_liability_manual_drivers.premium = hxd.fa_specific_liability_manual_drivers.salary * rate_liabilities_driv
    else:
        hxd.fa_specific_liability_manual_drivers.premium = 0  

    if hxd.fa_specific_liability_manual_metalworkerspolishers.salary is not None and hxd.fa_specific_liability_manual_metalworkerspolishers.salary > 0:
        hxd.fa_specific_liability_manual_metalworkerspolishers.premium = hxd.fa_specific_liability_manual_metalworkerspolishers.salary * rate_liabilities_metpol
    else:
        hxd.fa_specific_liability_manual_metalworkerspolishers.premium = 0  

    # Public Liability
    if hxd.fa_specific_liability_public.include_flag is True:
        hxd.fa_specific_liability_public.premium = rate_liabilities_publiab
    else:
        hxd.fa_specific_liability_public.premium = 0


    total_liabilities_premium = (
        hxd.fa_specific_liability_employers_base_premium.premium +
        hxd.fa_specific_liability_employers_5_10_employees.premium +
        hxd.fa_specific_liability_employers_10_20_employees.premium + 
        hxd.fa_specific_liability_employers_20_or_more_employees.premium + 

        hxd.fa_specific_liability_manual_woodworkers.premium + 
        hxd.fa_specific_liability_manual_warehouseman.premium + 
        hxd.fa_specific_liability_manual_drivers.premium + 
        hxd.fa_specific_liability_manual_metalworkerspolishers.premium + 

        hxd.fa_specific_liability_public.premium
    )



    # ADDITIONAL PREMIUM SUMMARY

    cov.fa_additional_summary.premium = (
        total_additional_premium +
        total_ancilliary_premium +
        total_exhibitions_premium +
        total_liabilities_premium 
    )
    cov.fa_additional_summary.tsi = (
        total_additional_tsi +
        total_ancilliary_tsi +
        total_exhibitions_tsi
    )

    

    # FA EXPOSURE RATE SUMMARY -----------------------------

    # CREDIT - PREMISES
    if cov.fa_premises_summary.tsi > 0:
        if cov.fa_premises_summary.ded is None or cov.fa_premises_summary.ded is 0:
            ded_input_premises = cov.fa_premises_summary.ded_perc
        else:
            ded_input_premises = cov.fa_premises_summary.ded / cov.fa_premises_summary.tsi
    else:
        ded_input_premises = 0
    
    fa_premises_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_premises]["fapremises"].iloc[-1]
    cov.fa_premises_summary.credit = fa_premises_exposure_curve

    # CREDIT - TRAVEL
    if cov.fa_travel_summary.tsi > 0:
        if cov.fa_travel_summary.ded is None or cov.fa_travel_summary.ded is 0:
            ded_input_travel = cov.fa_travel_summary.ded_perc
        else:
            ded_input_travel = cov.fa_travel_summary.ded / cov.fa_travel_summary.tsi
    else:
        ded_input_travel = 0
    
    fa_travel_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_travel]["fatravel"].iloc[-1]
    cov.fa_travel_summary.credit = fa_travel_exposure_curve

    # CREDIT - ADDITIONAL
    if cov.fa_additional_summary.tsi > 0:
        if cov.fa_additional_summary.ded is None or cov.fa_additional_summary.ded is 0:
            ded_input_additional = cov.fa_additional_summary.ded_perc
        else:
            ded_input_additional = cov.fa_additional_summary.ded / cov.fa_additional_summary.tsi
    else:
        ded_input_additional = 0
    
    fa_additional_exposure_curve = table_rating_exposure_curves[table_rating_exposure_curves["limded"] <= ded_input_additional]["faadditional"].iloc[-1]
    cov.fa_additional_summary.credit = fa_additional_exposure_curve


    # PREMIUM POST DEDUCTIBLE CREDIT
    if cov.fa_premises_summary.uw_adj_impact is not None and cov.fa_premises_summary.uw_adj_impact > 0: 
        cov.fa_premises_summary.prem_post_ded = cov.fa_premises_summary.premium * (1 - cov.fa_premises_summary.uw_adj_impact)
    else:
        cov.fa_premises_summary.prem_post_ded = cov.fa_premises_summary.premium * (1 - cov.fa_premises_summary.credit)

    if cov.fa_travel_summary.uw_adj_impact is not None and cov.fa_travel_summary.uw_adj_impact > 0: 
        cov.fa_travel_summary.prem_post_ded = cov.fa_travel_summary.premium * (1 - cov.fa_travel_summary.uw_adj_impact)
    else:
        cov.fa_travel_summary.prem_post_ded = cov.fa_travel_summary.premium * (1 - cov.fa_travel_summary.credit)
    
    if cov.fa_additional_summary.uw_adj_impact is not None and cov.fa_additional_summary.uw_adj_impact > 0: 
        cov.fa_additional_summary.prem_post_ded = cov.fa_additional_summary.premium * (1 - cov.fa_additional_summary.uw_adj_impact)
    else:
        cov.fa_additional_summary.prem_post_ded = cov.fa_additional_summary.premium * (1 - cov.fa_additional_summary.credit)
    
    # BRING IN LAST YEAR'S INFO


    pass