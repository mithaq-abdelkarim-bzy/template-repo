import hx
import pandas as pd
import numpy as np
from operator import itemgetter

def rate_jewellers_block(hxd, df):
    cds = hxd.cds
    cov = cds.layers[0].coverages

    # Generate summaries by premise
    df["exp_band_1"] = df["tsi_band_1"]
    df["exp_band_2"] = df["tsi_band_2"]
    df["exp_band_3"] = df["tsi_band_3"]
    df["exp_band_4"] = df["tsi_band_4"] + df["tsi_band_5"]
    df["exp_band_5"] = df["tsi_band_6"] + df["tsi_band_7"] + df["tsi_band_8"] + df["tsi_band_9"] + df["tsi_band_10"]

    # Read in rating tables
    table_rating_jb_premises = hx.params.table_rating_jb_premises

    prem_premises = 0.0

    for premise in ("Retail", "Wholesale", "Manufacturing"):
        df_summary = df[df["type"]==premise]
        df_summary = df_summary[["country", "tsi_cnv", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5"]].groupby("country", as_index=False).sum()
        df_summary = df_summary.rename(columns={"tsi_cnv": "tsi"})
        table_rates = table_rating_jb_premises[table_rating_jb_premises.type==premise][["country", "500000", "1000000", "2000000", "5000000", "10000000"]]
        table_rates = table_rates.rename(columns={"500000": "rate_band_1", "1000000": "rate_band_2", "2000000": "rate_band_3", "5000000": "rate_band_4", "10000000": "rate_band_5"})
        df_summary = df_summary.merge(table_rates, how="left", on="country")
        setattr(getattr(cov, "jb_premises"), premise.lower() + "_summary", df_summary.to_dict("records"))
        # Surely there is a better way of doing this weighted average summary
        df_summary.rate_band_1 = (df_summary.rate_band_1 * df_summary.exp_band_1) / df_summary.exp_band_1.sum() if df_summary.exp_band_1.sum() > 0 else 0
        df_summary.rate_band_2 = (df_summary.rate_band_2 * df_summary.exp_band_2) / df_summary.exp_band_2.sum() if df_summary.exp_band_2.sum() > 0 else 0
        df_summary.rate_band_3 = (df_summary.rate_band_3 * df_summary.exp_band_3) / df_summary.exp_band_3.sum() if df_summary.exp_band_3.sum() > 0 else 0
        df_summary.rate_band_4 = (df_summary.rate_band_4 * df_summary.exp_band_4) / df_summary.exp_band_4.sum() if df_summary.exp_band_4.sum() > 0 else 0
        df_summary.rate_band_5 = (df_summary.rate_band_5 * df_summary.exp_band_5) / df_summary.exp_band_5.sum() if df_summary.exp_band_5.sum() > 0 else 0
        df_summary_subtotal = df_summary[["tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "rate_band_1", "rate_band_2", "rate_band_3", "rate_band_4", "rate_band_5"]].sum()
        setattr(getattr(cov, "jb_premises"), premise.lower() + "_summary_subtotal", df_summary_subtotal.to_dict())
        prem_premises = prem_premises + df_summary_subtotal.exp_band_1 * df_summary_subtotal.rate_band_1 + df_summary_subtotal.exp_band_2 * df_summary_subtotal.rate_band_2 + df_summary_subtotal.exp_band_3 * df_summary_subtotal.rate_band_3 + df_summary_subtotal.exp_band_4 * df_summary_subtotal.rate_band_4 + df_summary_subtotal.exp_band_5 * df_summary_subtotal.rate_band_5
        
    cov.jb_premises.premium = prem_premises
    cov.jb_premises.tsi = df.tsi_cnv.sum()

    # Travel rating
    # # Convert cov.jb_travel_rating to DataFrame - is there a way to make this method work?
    lst = []
    for row in cov.jb_travel.rating:
        lst.append({
            "region": row.type_elsewhere_region.type,
            "elsewhere_region": row.type_elsewhere_region.elsewhere_region
        })
    df_jb_travel = pd.DataFrame(cov.jb_travel.rating)
    # desired_columns = df_jb_travel.iloc[0].str[0]
    # df_jb_travel.columns = desired_columns
    # for col in df_jb_travel.columns:
    #     df_jb_travel[col] = df_jb_travel[col].apply(itemgetter(1)) # Need a special unpack for the linked dropdown

    # df_jb_travel["key"] = df_jb_travel["origin_region"] + df_jb_travel["type"]
    # df_jb_travel.merge(hx.params.table_input_rates_jb_travel, how="left", left_on="key", right_on="index")
    # df_jb_travel.merge(hx.params.table_input_rates_jb_travel_elsewhere, how="left", left_on=["key", "elsewhere_region"], right_on=["index", "elsewhere_region"])
    # df_jb_travel["prem_rate_per_100_tsi"] = df_jb_travel["rate"]

    # # Put results back into cov.jb_travel_rating
    # for jb_travel_row, df_jb_travel_row in zip(cov.jb_travel_rating, df_jb_travel.iloc):
    #     jb_travel_row.prem_rate_per_100_tsi = df_jb_travel_row["prem_rate_per_100_tsi"]
    #     jb_travel_row.premium = df_jb_travel_row["premium"]

    # [{"key": "...", "type_elsewhere_region": {"type": "...", }}]

    table_jb = hx.params.table_rating_jb_travel
    table_jb_elsewhere = hx.params.table_rating_jb_travel_elsewhere

    prem_travel = 0.0
    tsi_travel = 0.0 # Better way than to loop through every row?

    for jb_travel in cov.jb_travel.rating:
        base_rate = table_jb[table_jb.key == jb_travel.origin_region + jb_travel.type_elsewhere_region.type]["rate"] # Using "rate" vs .rate? pros vs cons?
        if len(base_rate)>0: # Is this the right way to check emptiness of list?
            jb_travel_base_rate = base_rate.iloc[0]
        else:
            jb_travel_base_rate = 0.0
        if jb_travel.type_elsewhere_region.type == "Elsewhere": # Is there a more efficient way to write this block?
            if jb_travel.type_elsewhere_region.elsewhere_region == '':
                jb_travel_relativity = 1                
            else:
                jb_travel_relativity = table_jb_elsewhere[(table_jb_elsewhere.key == jb_travel.origin_region + jb_travel.type_elsewhere_region.type) & (table_jb_elsewhere.elsewhere_region == jb_travel.type_elsewhere_region.elsewhere_region)]["relativity"].iloc[0]
        else:
            jb_travel_relativity = 1

        jb_travel.prem_rate_per_100_tsi = jb_travel_base_rate * jb_travel_relativity

        if jb_travel.average_carryings > 0 and jb_travel.max_carryings > 0:
            jb_travel.premium = (jb_travel.average_carryings + jb_travel.max_carryings) / 2 * jb_travel.no_of_days / 250 * jb_travel.prem_rate_per_100_tsi
        else:
            jb_travel.premium = (jb_travel.average_carryings + jb_travel.max_carryings) * jb_travel.no_of_days / 250 * jb_travel.prem_rate_per_100_tsi

        prem_travel = prem_travel + jb_travel.premium
        tsi_travel = tsi_travel + jb_travel.max_carryings

    cov.jb_travel.premium = sum([row.premium for row in cov.jb_travel.rating])
    cov.jb_travel.tsi = sum([row.max_carryings for row in cov.jb_travel.rating])

    # JB Specific Rating
    ## Populate defaults   
    table_rating_jb_additional = hx.params.table_rating_jb_additional    

    prem_additional = 0.0
    tsi_additional = 0.0
    
    for specific in ["additional", "ancillary", "shipping"]:
        table_specific = table_rating_jb_additional[table_rating_jb_additional.specific == specific]
        for i in range(len(table_specific)):
            exec("cov.jb_specific." + specific + "_" + str(i) + ".coverage = table_specific.coverage.iloc[" + str(i) + "]") # Seems messy, there must be a better way
            exec("cov.jb_specific." + specific + "_" + str(i) + ".prem_rate_per_100_tsi = table_specific.rate.iloc[" + str(i) + "]")
            exec("cov.jb_specific." + specific + "_" + str(i) + ".premium = cov.jb_specific." + specific + "_" + str(i) + ".tsi * cov.jb_specific." + specific + "_" + str(i) + ".prem_rate_per_100_tsi")
            prem_additional = prem_additional + eval("cov.jb_specific." + specific + "_" + str(i) + ".premium") # Is this the best way to dynamically reference variables?
            tsi_additional = tsi_additional + eval("cov.jb_specific." + specific + "_" + str(i) + ".tsi")

    ## Additional Peril Premiums
    for jb_additional in cov.jb_specific.additional_custom: # looping through additional_custom, or just additional_x (x from 0 to n?)
        jb_additional.premium = jb_additional.prem_rate_per_100_tsi * jb_additional.tsi
        prem_additional = prem_additional + jb_additional.premium
        tsi_additional = tsi_additional + jb_additional.tsi

    ## Ancillary Premium
    for jb_additional in cov.jb_specific.ancillary_custom:
        jb_additional.premium = jb_additional.prem_rate_per_100_tsi * jb_additional.tsi
        prem_additional = prem_additional + jb_additional.premium
        tsi_additional = tsi_additional + jb_additional.tsi

    ## Shipping Premium
    for jb_additional in cov.jb_specific.shipping_custom:
        jb_additional.premium = jb_additional.prem_rate_per_100_tsi * jb_additional.tsi
        prem_additional = prem_additional + jb_additional.premium
        tsi_additional = tsi_additional + jb_additional.tsi

    # Currency rate
    fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.currencies.source_currency]["fx_rate"].iloc[0]

    # final premium and tsi converted to USD
    cov.jb_additional.premium = prem_additional / fx_rate
    cov.jb_additional.tsi = tsi_additional / fx_rate

    # Populate exposure rate summary table
    table_exp_curves = hx.params.table_rating_exposure_curves
    for sub_group in ["premises", "travel", "additional"]:
        # if eval("cov.jb_" + sub_group + ".ded_perc") != None:
        #     ded_perc = eval("cov.jb_" + sub_group + ".ded_perc")
        # else:
        #     ded_perc = eval("cov.jb_" + sub_group + ".deductible") / eval("cov.jb_" + sub_group + ".tsi") if eval("cov.jb_" + sub_group + ".tsi") > 0 and eval("cov.jb_" + sub_group + ".deductible") != None else 0
        #IR edit:
        if eval("cov.jb_" + sub_group + ".deductible") != None:
            ded_perc = eval("cov.jb_" + sub_group + ".deductible") / eval("cov.jb_" + sub_group + ".tsi") if eval("cov.jb_" + sub_group + ".tsi") > 0 else 0
        else:
            ded_perc = eval("cov.jb_" + sub_group + ".ded_perc") if eval("cov.jb_" + sub_group + ".ded_perc") != None else 0
        
        credit = table_exp_curves[table_exp_curves.limded <= ded_perc]["jb" + sub_group].iloc[-1]
        exec("cov.jb_" + sub_group + ".credit = credit") # How do assign to a dynamic variable name with local scope?
        credit_applied = eval("cov.jb_" + sub_group + ".uw_adj_impact") if eval("cov.jb_" + sub_group + ".uw_adj_impact") != None else credit
        prem_post_ded = eval("cov.jb_" + sub_group + ".premium") * (1 - credit_applied)
        exec("cov.jb_" + sub_group + ".prem_post_ded = prem_post_ded")
        implied_rate_post_ded = prem_post_ded / eval("cov.jb_" + sub_group + ".tsi") if eval("cov.jb_" + sub_group + ".tsi") > 0 else None
        exec("cov.jb_" + sub_group + ".implied_rate_post_ded = implied_rate_post_ded")