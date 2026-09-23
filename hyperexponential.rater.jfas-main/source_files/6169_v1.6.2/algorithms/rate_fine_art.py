import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_utilities as utils
from operator import itemgetter

def rate_fine_art(hxd, df):
    cds = hxd.cds
    cov = cds.layers[0].coverages
    
    if cds.fa_masking == True:

        # 0. DECLARE PARAMETERS -------------------------------------------------------------------------
        df = df # data frame created from exposure input
        fa_premises_rates = hx.params.table_rating_fa_premises
        fa_travel_rates = hx.params.table_rating_fa_travel
        fa_additional_rates = hx.params.table_rating_jfas_all_additional
        fa_additional_rates = fa_additional_rates[fa_additional_rates["class"] == "Fine Art"]

        table_rating_exposure_curves = hx.params.table_rating_exposure_curves


        # 1. PREMISES RATING -------------------------------------------------------------------------
        
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
            setattr(getattr(cov, "fa_premises"), premise.lower().replace(" ", "_") + "_summary", df_summary_1.to_dict("records"))
            setattr(getattr(cov, "fa_premises"), premise.lower().replace(" ", "_") + "_summary_subtotal", df_summary_1[["tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]].sum().to_dict())

            df_summary = df[df["type"]==premise]
            df_summary_2 = df_summary[["country", "1000000", "3000000", "5000000", "10000000", "20000000", "50000000", "100000000", ">100m"]].groupby("country", as_index=False).mean()
            df_summary_2.columns.values[1:9] = ["exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "exp_band_7", "exp_band_8"]

            setattr(getattr(cov, "fa_premises"), premise.replace(" ", "_").lower() + "_summary_rates", df_summary_2.to_dict("records"))
            
            # END LOOP
        
        # Total Premises premium and TSI
        cov.fa_premises.premium = df["premium"].sum()
        cov.fa_premises.tsi = df["tsi_cnv"].sum()



        # 2. TRAVEL RATING -------------------------------------------------------------------------
        travel_summary = pd.DataFrame(fa_travel_rates)
        total_travel_tsi = 0.0
        total_travel_prem = 0.0

        for i in range(len(fa_travel_rates)):

            exec("cov.fa_travel.rating_" + str(i) + ".travel_type = travel_summary.travel_type.iloc[i]")
            exec("cov.fa_travel.rating_" + str(i) + ".prem_rate_per_100_tsi = travel_summary.rate.iloc[i]")

            travel_tsi = eval("cov.fa_travel.rating_" + str(i) + ".tsi") if eval("cov.fa_travel.rating_" + str(i) + ".tsi") is not None else 0
            travel_uw_rate = eval("cov.fa_travel.rating_" + str(i) + ".uw_rate_per_100_tsi") if eval("cov.fa_travel.rating_" + str(i) + ".uw_rate_per_100_tsi") is not None else 0

            applied_rate = travel_uw_rate if travel_uw_rate > 0 else travel_summary.rate.iloc[i]
            travel_prem = applied_rate * travel_tsi
            exec("cov.fa_travel.rating_" + str(i) + ".premium = travel_prem")

            total_travel_tsi = total_travel_tsi + travel_tsi
            total_travel_prem = total_travel_prem + travel_prem

        # Currency rate
        fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.currencies.source_currency]["fx_rate"].iloc[0]

        # Populate Travel Total, adjusted for fx_rate
        cov.fa_travel.premium = total_travel_prem / fx_rate
        cov.fa_travel.tsi = total_travel_tsi / fx_rate

        # 3. ADDITIONAL PERIL RATING -------------------------------------------------------------------------
        add_peril_summary = fa_additional_rates[fa_additional_rates["peril_type"] == "Additional Perils"][["peril_group", "rate"]]
        total_add_peril_tsi = 0.0
        total_add_peril_prem = 0.0

        # Additional Peril Premium - standard
        for i in range(len(add_peril_summary)):
            # SA: Exec is bad practice. Use getattr instead. This opens you up to errors if 
            # add_peril_summary.peril_group.iloc[i] contains special characters
            exec("cov.fa_specific.additional_" + str(i) + ".coverage = add_peril_summary.peril_group.iloc[i]")
            exec("cov.fa_specific.additional_" + str(i) + ".prem_rate_per_100_tsi = add_peril_summary.rate.iloc[i]")

            # SA: Similarly, use setattr instead of eval
            add_peril_tsi = eval("cov.fa_specific.additional_" + str(i) + ".tsi") if eval("cov.fa_specific.additional_" + str(i) + ".tsi") is not None else 0
            add_peril_uw_rate = eval("cov.fa_specific.additional_" + str(i) + ".uw_rate_per_100_tsi") if eval("cov.fa_specific.additional_" + str(i) + ".uw_rate_per_100_tsi") is not None else 0

            applied_rate = add_peril_uw_rate if add_peril_uw_rate > 0 else add_peril_summary.rate.iloc[i]
            add_peril_prem = applied_rate * add_peril_tsi
            exec("cov.fa_specific.additional_" + str(i) + ".premium = add_peril_prem")

            total_add_peril_tsi = total_add_peril_tsi + add_peril_tsi
            total_add_peril_prem = total_add_peril_prem + add_peril_prem

        # Additional Peril Premium - custom
        for row in cov.fa_specific.additional_custom:

            applied_rate = row.uw_rate_per_100_tsi if row.uw_rate_per_100_tsi is not None and row.uw_rate_per_100_tsi > 0 else row.prem_rate_per_100_tsi

            row.premium = row.tsi * applied_rate
            total_add_peril_prem = total_add_peril_prem + row.premium
            total_add_peril_tsi = total_add_peril_tsi + row.tsi



        # 4. ANCILLIARY RATING -------------------------------------------------------------------------
        ancil_summary = fa_additional_rates[fa_additional_rates["peril_type"] == "Ancillary Covers"][["peril_group", "rate"]]
        total_ancil_tsi = 0.0
        total_ancil_prem = 0.0

        # Ancilliary premium - standard
        for i in range(len(ancil_summary)):

            exec("cov.fa_specific.ancilliary_" + str(i) + ".coverage = ancil_summary.peril_group.iloc[i]")
            exec("cov.fa_specific.ancilliary_" + str(i) + ".prem_rate_per_100_tsi = ancil_summary.rate.iloc[i]")

            ancil_tsi = eval("cov.fa_specific.ancilliary_" + str(i) + ".tsi") if eval("cov.fa_specific.ancilliary_" + str(i) + ".tsi") is not None else 0
            ancil_uw_rate = eval("cov.fa_specific.ancilliary_" + str(i) + ".uw_rate_per_100_tsi") if eval("cov.fa_specific.ancilliary_" + str(i) + ".uw_rate_per_100_tsi") is not None else 0

            applied_rate = ancil_uw_rate if ancil_uw_rate > 0 else ancil_summary.rate.iloc[i]
            ancil_prem = applied_rate * ancil_tsi
            exec("cov.fa_specific.ancilliary_" + str(i) + ".premium = ancil_prem")

            total_ancil_tsi = total_ancil_tsi + ancil_tsi
            total_ancil_prem = total_ancil_prem + ancil_prem

        # Ancilliary Premium - custom
        for row in cov.fa_specific.ancilliary_custom:

            applied_rate = row.uw_rate_per_100_tsi if row.uw_rate_per_100_tsi is not None and row.uw_rate_per_100_tsi > 0 else row.prem_rate_per_100_tsi
            row.premium = row.tsi * applied_rate
            total_ancil_prem = total_ancil_prem + row.premium
            total_ancil_tsi = total_ancil_tsi + row.tsi

        
        # 5. EXHIBITIONS -------------------------------------------------------------------------
        # Exhibitions - Standard and Transit
        exh_summary = fa_additional_rates[fa_additional_rates["peril_type"] == "Exhibitions"][["peril_group", "rate"]]
        total_exh_tsi = 0.0
        total_exh_prem = 0.0

        for i in range(len(exh_summary)):

            if (i <= 2):
                # Exhibition
                exec("cov.fa_specific.exhibitions_" + str(i) + ".coverage = exh_summary.peril_group.iloc[i]")
                exec("cov.fa_specific.exhibitions_" + str(i) + ".prem_rate_per_100_tsi = exh_summary.rate.iloc[i]")

                exh_tsi = eval("cov.fa_specific.exhibitions_" + str(i) + ".tsi") if eval("cov.fa_specific.exhibitions_" + str(i) + ".tsi") is not None else 0
                exh_uw_rate = eval("cov.fa_specific.exhibitions_" + str(i) + ".uw_rate_per_100_tsi") if eval("cov.fa_specific.exhibitions_" + str(i) + ".uw_rate_per_100_tsi") is not None else 0
                exh_trips = eval("cov.fa_specific.exhibitions_" + str(i) + ".no_of_transits_per_month") if eval("cov.fa_specific.exhibitions_" + str(i) + ".no_of_transits_per_month") is not None else 0

                applied_rate = exh_uw_rate if exh_uw_rate > 0 else exh_summary.rate.iloc[i]
                exh_prem = exh_trips * applied_rate * exh_tsi

                exec("cov.fa_specific.exhibitions_" + str(i) + ".premium = exh_prem")

            else:
                # Exhibitions Transit        
                exec("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".coverage = exh_summary.peril_group.iloc[i]")
                exec("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".prem_rate_per_100_tsi = exh_summary.rate.iloc[i]")

                exh_tsi = eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".tsi") if eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".tsi") is not None else 0
                exh_uw_rate = eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".uw_rate_per_100_tsi") if eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".uw_rate_per_100_tsi") is not None else 0
                exh_trips = eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".no_of_transits_each_way") if eval("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".no_of_transits_each_way") is not None else 0

                applied_rate = exh_uw_rate if exh_uw_rate > 0 else exh_summary.rate.iloc[i]
                exh_prem = exh_trips * applied_rate * exh_tsi
                
                exec("cov.fa_specific.exhibitions_transit_" + str(i - 3) + ".premium = exh_prem")
            # end loop

            total_exh_tsi = total_exh_tsi + exh_tsi
            total_exh_prem = total_exh_prem + exh_prem

        # Exhibition Premium - custom
        for row in cov.fa_specific.exhibitions_transit_custom:

            applied_rate = row.uw_rate_per_100_tsi if row.uw_rate_per_100_tsi is not None and row.uw_rate_per_100_tsi > 0 else row.prem_rate_per_100_tsi
            row.premium = row.tsi * applied_rate
            total_exh_tsi = total_exh_tsi + row.tsi
            total_exh_prem = total_exh_prem + row.premium
        

        # 6. LIABILITY RATING -------------------------------------------------------------------------
        liab_summary = fa_additional_rates[fa_additional_rates["peril_type"] == "Liabilities"][["peril_group", "rate"]]
        liab_summary_non_pl = liab_summary[liab_summary["peril_group"] != "Public Liability"]
        liab_summary_pl = liab_summary[liab_summary["peril_group"] == "Public Liability"]
        total_liab_tsi = 0.0
        total_liab_prem = 0.0

        # Employers Liability
        for i in range(len(liab_summary_non_pl)):

            if (i <= 3):
                # Employers Liability
                exec("cov.fa_specific.liability_employers_" + str(i) + ".employers_liability = liab_summary_non_pl.peril_group.iloc[i]")
                exec("cov.fa_specific.liability_employers_" + str(i) + ".per_employee = liab_summary_non_pl.rate.iloc[i]")

                employees = eval("cov.fa_specific.liability_employers_" + str(i) + ".no_of_employees") if eval("cov.fa_specific.liability_employers_" + str(i) + ".no_of_employees") is not None else 0
                liab_prem = employees * liab_summary_non_pl.rate.iloc[i] 
                if (i == 0): liab_prem = min(liab_prem, liab_summary_non_pl.rate.iloc[i])

                exec("cov.fa_specific.liability_employers_" + str(i) + ".premium = liab_prem")
                
            else:
                # Manual Work Surcharge
                exec("cov.fa_specific.liability_manual_" + str(i - 4) + ".manual_work_surcharge = liab_summary_non_pl.peril_group.iloc[i]")
                exec("cov.fa_specific.liability_manual_" + str(i - 4) + ".prem_rate = liab_summary_non_pl.rate.iloc[i]")

                salary = eval("cov.fa_specific.liability_manual_" + str(i - 4) + ".salary") if eval("cov.fa_specific.liability_manual_" + str(i - 4) + ".salary") is not None else 0
                liab_prem = salary * liab_summary_non_pl.rate.iloc[i]

                exec("cov.fa_specific.liability_manual_" + str(i - 4) + ".premium = liab_prem")

            total_liab_prem = total_liab_prem + liab_prem


        # Public Liability
        cov.fa_specific.liability_public.public_liability = liab_summary_pl["peril_group"].iloc[0]

        if cov.fa_specific.liability_public.include_flag is True:
            pl_prem = liab_summary_pl["rate"].iloc[0]
            cov.fa_specific.liability_public.premium = pl_prem
        else:
            pl_prem = 0

        # Add to total
        total_liab_prem = total_liab_prem + pl_prem


        # Populate Additional Premium Total, adjusted for fx_rate
        cov.fa_additional.tsi = (total_add_peril_tsi + total_ancil_tsi + total_exh_tsi) / fx_rate
        cov.fa_additional.premium = (total_add_peril_prem + total_ancil_prem + total_exh_prem) / fx_rate + total_liab_prem


        # 7. SUMMARY TABLE -------------------------------------------------------------------------
        for summ_type in ["premises", "travel", "additional"]:

            ded = eval(f"cov.fa_{summ_type}.deductible") #if eval(f"cov.fa_{summ_type}.deductible") is not None else 0
            ded_perc = eval(f"cov.fa_{summ_type}.ded_perc") if eval(f"cov.fa_{summ_type}.ded_perc") is not None else 0
            tsi = eval(f"cov.fa_{summ_type}.tsi") if eval(f"cov.fa_{summ_type}.tsi") is not None else 0
            prem = eval(f"cov.fa_{summ_type}.premium") if eval(f"cov.fa_{summ_type}.premium") is not None else 0
            uw_credit = eval(f"cov.fa_{summ_type}.uw_adj_impact") if eval(f"cov.fa_{summ_type}.uw_adj_impact") is not None else 0

            # Credit
            #IR edit:
            if ded is not None:
                ded_input = ded / tsi if tsi > 0 else 0
            else:
                ded_input = ded_perc
            # ded_input = ded / tsi if ded is not None and ded > 0 else ded_perc

            exposure = table_rating_exposure_curves[["limded", f"fa{summ_type}"]]
            credit = exposure[exposure["limded"] <= ded_input][f"fa{summ_type}"].iloc[-1]
            
            exec(f"cov.fa_{summ_type}.credit = credit")

            # Premium post deductible and implied rate
            assigned_credit = uw_credit if uw_credit > 0 else credit
            prem_post_ded = prem * (1 - assigned_credit)
            implied_rate_post_ded = prem_post_ded / tsi if tsi > 0 else 0 
            exec(f"cov.fa_{summ_type}.prem_post_ded = prem_post_ded")
            exec(f"cov.fa_{summ_type}.implied_rate_post_ded = implied_rate_post_ded")



        # 8. ATTACH LAST YEAR's INFO -------------------------------------------------------------------------

    pass