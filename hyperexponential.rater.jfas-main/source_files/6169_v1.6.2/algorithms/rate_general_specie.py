import hx
import pandas as pd
import numpy as np
import math as math
import algorithms.rate_z_global_parameters as z_global_parameters
import algorithms.rate_z_utilities as utils
from operator import itemgetter

def rate_general_specie(hxd, df):
    cds = hxd.cds
    layer = cds.layers[0]
    cov = layer.coverages

    if cds.gs_masking == True:
    
        # 0. DECLARE PARAMETERS -------------------------------------------------------------------------
        df = pd.DataFrame(df) # data frame created from exposure input
        cds.gs_transit_relativity = z_global_parameters.gs_transit_relativity
        table_rating_gs = pd.DataFrame(hx.params.table_rating_gs)
        table_rating_gs = table_rating_gs[["type","region","relativity","param_a","param_b"]].drop_duplicates()
        table_region = pd.DataFrame(hx.params.table_lookup_region)
        table_rating_exp = hx.params.table_rating_exposure_curves


        # 1. RATING ------------------------------------------------------------------------- 

        # Declare totals 
        total_tsi = 0
        total_premium = 0

        # Loop through General Specie Types
        for gs_type in ["Metals", "Cash", "Securities"]:

            gs_type_lower = gs_type.lower()

            # Exposure input summary
            df_summary = df[df["type"] == gs_type][["region", "tsi_cnv"]].groupby("region", as_index=False).sum()

            # get rate parameters
            table_specific = table_rating_gs[table_rating_gs.type == gs_type]

            # attach to general region table
            region_summary = table_region
            region_summary = region_summary.rename(columns={"regions": "region"})
            region_summary = region_summary.merge(df_summary, how = "left", left_on = "region", right_on = "region")
            region_summary = region_summary.merge(table_specific[["region", "relativity", "param_a", "param_b"]], how = "left", left_on = "region", right_on = "region")
            region_summary = region_summary.fillna(0)

            # calculate static rate and premium
            region_summary["rate"] = region_summary.apply(lambda x : utils.gs_calculate_rate(tsi = x["tsi_cnv"], relativity = x["relativity"], param_a = x["param_a"], param_b = x["param_b"]), axis = 1)
            region_summary["premium"] = region_summary["tsi_cnv"] * region_summary["rate"]

            subtotal_tsi_t = 0
            subtotal_premium_t = 0

            # Loop Through each region within each General Specie Type
            for i in range(len(region_summary)):

                # STATICS
                exec("cov.gs_" + gs_type_lower + ".static_" + str(i) + ".region = region_summary.region.iloc[" + str(i) + "]")
                exec("cov.gs_" + gs_type_lower + ".static_" + str(i) + ".tsi = region_summary.tsi_cnv.iloc[" + str(i) + "]")
                exec("cov.gs_" + gs_type_lower + ".static_" + str(i) + ".rate = region_summary.rate.iloc[" + str(i) + "]")
                exec("cov.gs_" + gs_type_lower + ".static_" + str(i) + ".premium = region_summary.premium.iloc[" + str(i) + "]")

                # TRANSIT
                exec("cov.gs_" + gs_type_lower + ".transit_" + str(i) + ".region = region_summary.region.iloc[" + str(i) + "]")

                # Calculate transit rate and premium -- based on user input
                tsi = eval("cov.gs_" + gs_type_lower + ".transit_" + str(i) + ".tsi") if eval("cov.gs_" + gs_type_lower + ".transit_" + str(i) + ".tsi") != None else 0.0
                relativity = eval("region_summary.relativity.iloc[" + str(i) + "]")
                param_a = eval("region_summary.param_a.iloc[" + str(i) + "]")
                param_b = eval("region_summary.param_b.iloc[" + str(i) + "]")
                
                rate_t = utils.gs_calculate_rate(relativity, param_a, param_b, tsi) * cds.gs_transit_relativity
                premium_t = rate_t * tsi

                # Assign to tables
                exec("cov.gs_" + gs_type_lower + ".transit_" + str(i) + ".rate = rate_t")
                exec("cov.gs_" + gs_type_lower + ".transit_" + str(i) + ".premium = premium_t")

                # Add to subtotal
                subtotal_tsi_t = subtotal_tsi_t + tsi
                subtotal_premium_t = subtotal_premium_t + premium_t

                # End loop - region table

            # Generate sub-totals - Static
            subtotal_tsi_s = region_summary["tsi_cnv"].sum()
            subtotal_premium_s = region_summary["premium"].sum()
            
            exec("cov.gs_" + gs_type_lower + ".static_subtotal.tsi = subtotal_tsi_s")
            exec("cov.gs_" + gs_type_lower + ".static_subtotal.premium = subtotal_premium_s")
            exec("cov.gs_" + gs_type_lower + ".static_subtotal.rate = subtotal_premium_s / subtotal_tsi_s if subtotal_tsi_s > 0 else 0")

            # Generate sub-totals - Transit
            exec("cov.gs_" + gs_type_lower + ".transit_subtotal.tsi = subtotal_tsi_t")
            exec("cov.gs_" + gs_type_lower + ".transit_subtotal.premium = subtotal_premium_t")
            exec("cov.gs_" + gs_type_lower + ".transit_subtotal.rate = subtotal_premium_t / subtotal_tsi_t if subtotal_tsi_t > 0 else 0")

            # Assign total TSI and Premium
            exec("cov.gs_" + gs_type_lower + ".tsi = subtotal_tsi_s + subtotal_tsi_t")
            exec("cov.gs_" + gs_type_lower + ".premium = subtotal_premium_s + subtotal_premium_t")


            # SUMMARY TABLE
            # Credit
            ded = eval("cov.gs_" + gs_type_lower + ".deductible")
            ded_perc = eval("cov.gs_" + gs_type_lower + ".ded_perc")
            tsi = eval("cov.gs_" + gs_type_lower + ".tsi")
            
            #IR edit:
            if ded is not None:
                ded_lookup = ded / tsi if tsi > 0 else 0
            else:
                ded_lookup = ded_perc
            # ded_lookup = ded / tsi if ded is not None and ded > 0 and tsi > 0 else ded_perc

            # look up credit from exposure table
            credit = table_rating_exp[table_rating_exp["limded"] <= ded_lookup]["gs" + gs_type_lower].iloc[-1]
            exec("cov.gs_" + gs_type_lower + ".credit = credit")

            # Premium post deductible credit
            uw_credit = eval("cov.gs_" + gs_type_lower + ".uw_adj_impact")

            credit_select = uw_credit if uw_credit is not None and uw_credit > 0 else credit

            prem_post_ded = (subtotal_premium_s + subtotal_premium_t) * (1 - credit_select)
            implied_rate_post_ded = prem_post_ded / (subtotal_tsi_s + subtotal_tsi_t) if (subtotal_tsi_s + subtotal_tsi_t) > 0 else 0
            
            exec("cov.gs_" + gs_type_lower + ".prem_post_ded = prem_post_ded")
            exec("cov.gs_" + gs_type_lower + ".implied_rate_post_ded = implied_rate_post_ded")

            
        # Additional ---
        additional_df = pd.DataFrame(cov.gs_additional.custom)
        desired_columns = additional_df.iloc[0].str[0]
        additional_df.columns = desired_columns
        for col in additional_df.columns:
            additional_df[col] = additional_df[col].apply(itemgetter(1))

        additional_df["premium"] = (additional_df["prem_rate_per_100_tsi"] * additional_df["tsi"])

        # assign back to hxd object
        for custom_row, df_row in zip(cov.gs_additional.custom, additional_df.iloc):
            custom_row.premium = df_row["premium"]

        # summary table
        subtotal_prem_a = additional_df["premium"].sum()
        subtotal_tsi_a = additional_df["tsi"].sum()

        # Currency rate
        fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.currencies.source_currency]["fx_rate"].iloc[0]

        # final premium and tsi converted to USD
        cov.gs_additional.premium = subtotal_prem_a / fx_rate
        cov.gs_additional.tsi = subtotal_tsi_a / fx_rate

        ded = cov.gs_additional.deductible
        ded_perc = cov.gs_additional.ded_perc        

        if ded is not None:
            ded_lookup = ded / subtotal_tsi_a if subtotal_tsi_a > 0 else 0
        else:
            ded_lookup = ded_perc

        # look up credit from exposure table
        credit = table_rating_exp[table_rating_exp["limded"] <= ded_lookup]["gsadditional"].iloc[-1]
        cov.gs_additional.credit = credit

        # Premium post deductible credit
        uw_credit = cov.gs_additional.uw_adj_impact
        credit_select = uw_credit if uw_credit is not None and uw_credit > 0 else credit

        prem_post_ded = cov.gs_additional.premium * (1 - credit_select)
        implied_rate_post_ded = prem_post_ded / cov.gs_additional.premium if cov.gs_additional.premium > 0 else 0

        cov.gs_additional.prem_post_ded = prem_post_ded
        cov.gs_additional.implied_rate_post_ded = implied_rate_post_ded





        # TODO: Populate expiring information ----------------------------------

        # TODO: Populate expiring information ----------------------------------

    pass