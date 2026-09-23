import hx
import pandas as pd
import numpy as np
import math
from operator import itemgetter

def rate_cash_in_transit(hxd, df):
    cds = hxd.cds
    layer = cds.layers[0] 
    cov = cds.layers[0].coverages
    
    # Generate summaries by premise
    df["exp_band_1"] = df["tsi_band_1"] + df["tsi_band_2"]
    df["exp_band_2"] = df["tsi_band_3"] + df["tsi_band_4"]
    df["exp_band_3"] = df["tsi_band_5"]
    df["exp_band_4"] = df["tsi_band_6"] 
    df["exp_band_5"] = df["tsi_band_7"]
    df["exp_band_6"] = df["tsi_band_8"] + df["tsi_band_9"] + df["tsi_band_10"]

    # Read in rating tables
    table_rating_cit_premises = hx.params.table_rating_cit_premises

    prem_premises = 0.0

    for premise in ("General",):  # SA: Why not just use a list ["General"] instead of a tuple with a comma?
        df_summary = df[df["type"]==premise]
        df_summary = df_summary[["country", "tsi_cnv", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6"]].groupby("country", as_index=False).sum()
        df_summary = df_summary.rename(columns={"tsi_cnv": "tsi"})
        table_rates = table_rating_cit_premises[table_rating_cit_premises.type==premise][["country", "0_1m", "1_3m", "3_5m", "5_10m", "10_20m", "20m_plus"]]
        table_rates = table_rates.rename(columns={"0_1m": "rate_band_1", "1_3m": "rate_band_2", "3_5m": "rate_band_3", "5_10m": "rate_band_4", "10_20m": "rate_band_5", "20m_plus": "rate_band_6"})
        df_summary = df_summary.merge(table_rates, how="left", on="country")
        setattr(layer, "cit_" + premise.lower() + "_summary", df_summary.to_dict("records"))
        # Surely there is a better way of doing this weighted average summary
        # SA: you can make this much cleaner by doing this in a loop with getattr and setattr
        df_summary.rate_band_1 = (df_summary.rate_band_1 * df_summary.exp_band_1) / df_summary.exp_band_1.sum() if df_summary.exp_band_1.sum() > 0 else 0
        df_summary.rate_band_2 = (df_summary.rate_band_2 * df_summary.exp_band_2) / df_summary.exp_band_2.sum() if df_summary.exp_band_2.sum() > 0 else 0
        df_summary.rate_band_3 = (df_summary.rate_band_3 * df_summary.exp_band_3) / df_summary.exp_band_3.sum() if df_summary.exp_band_3.sum() > 0 else 0
        df_summary.rate_band_4 = (df_summary.rate_band_4 * df_summary.exp_band_4) / df_summary.exp_band_4.sum() if df_summary.exp_band_4.sum() > 0 else 0
        df_summary.rate_band_5 = (df_summary.rate_band_5 * df_summary.exp_band_5) / df_summary.exp_band_5.sum() if df_summary.exp_band_5.sum() > 0 else 0
        df_summary.rate_band_6 = (df_summary.rate_band_6 * df_summary.exp_band_6) / df_summary.exp_band_6.sum() if df_summary.exp_band_6.sum() > 0 else 0
        df_summary_subtotal = df_summary[["tsi", "exp_band_1", "exp_band_2", "exp_band_3", "exp_band_4", "exp_band_5", "exp_band_6", "rate_band_1", "rate_band_2", "rate_band_3", "rate_band_4", "rate_band_5", "rate_band_6"]].sum()
        setattr(layer, "cit_" + premise.lower() + "_summary_subtotal", df_summary_subtotal.to_dict())
        # SA: below is an unreadably long line, I'd split over multiple lines. You can use \ to split a line up in python:
        # 3 = 2 + \
        #       1
        # or do sum(
        #   prem_premises, 
        #   df_summary_subtotal.exp_band_1 * df_summary_subtotal.rate_band_1, 
        #   df_summary_subtotal.exp_band_2 * df_summary_subtotal.rate_band_2,
        #   ...
        # )
        prem_premises = prem_premises + df_summary_subtotal.exp_band_1 * df_summary_subtotal.rate_band_1 + df_summary_subtotal.exp_band_2 * df_summary_subtotal.rate_band_2 + df_summary_subtotal.exp_band_3 * df_summary_subtotal.rate_band_3 + df_summary_subtotal.exp_band_4 * df_summary_subtotal.rate_band_4 + df_summary_subtotal.exp_band_5 * df_summary_subtotal.rate_band_5 + df_summary_subtotal.exp_band_6 * df_summary_subtotal.rate_band_6
        
    cov.cit_premises.premium = prem_premises
    cov.cit_premises.tsi = df.tsi_cnv.sum()

    # CIT Specific Rating
    ## Populate defaults

    table_rating_cit_additional = hx.params.table_rating_cit_additional
    ex_rate = hx.params.table_input_currency[hx.params.table_input_currency.ccy == cds.currencies.source_currency].fx_rate.iloc[0] if cds.currencies.source_currency != None else 1
    
    prem_additional = 0.0
    tsi_additional = 0.0
    
    for i in range(len(table_rating_cit_additional)):
        # SA: exec and eval should only be used as a last resort! They're a potential security risk but most importantly are likely to cause bugs
        # use setattr and getattr instead, these can be chained together if required! Let me know if you'd like examples
        # This comment applies throughout
        # https://medium.com/@murungaephantus/why-you-should-not-use-eval-and-exec-in-python-77d19345128c#:~:text=The%20eval()%20and%20exec,be%20dangerous%20if%20used%20incorrectly.&text=The%20biggest%20security%20risk%20associated,used%20to%20execute%20malicious%20code.
        exec("cov.cit_additional.specific_" + str(i) + ".coverage = table_rating_cit_additional.coverage.iloc[" + str(i) + "]")  
        prem_wavg = 0.0
        tsi_wavg = 0.0
        for country in ["usa", "na_ex_usa", "sa", "uk", "europe", "asia", "oceania", "africa"]:
            tsi = eval("cov.cit_additional.specific_" + str(i) + "." + country) if eval("cov.cit_additional.specific_" + str(i) + "." + country) != None else 0.0 
            if i > 4:
                rate = eval("table_rating_cit_additional.rate.iloc[" + str(i) + "]")
            else:
                a = eval("table_rating_cit_additional.a.iloc[" + str(i) + "]")
                b = eval("table_rating_cit_additional.b.iloc[" + str(i) + "]")
                rate = a * math.exp(b * math.log(tsi / ex_rate)) if tsi != 0.0 else 0.0
            country_rel = eval("table_rating_cit_additional." + country + ".iloc[" + str(i) + "]")
            exec("cov.cit_additional.specific_" + str(i) + ".rate_" + country + " = rate * country_rel")
            prem_additional = prem_additional + tsi * rate * country_rel  # SA: It might be clearer to use the += operator: prem_additional += tsi * rate * country_rel
            tsi_additional = tsi_additional + tsi 
            prem_wavg = prem_wavg + tsi * rate * country_rel
            tsi_wavg = tsi_wavg + tsi
        exec("cov.cit_additional.specific_" + str(i) + ".rate_total = prem_wavg / tsi_wavg if tsi_wavg > 0.0 else 0.0")
        exec("cov.cit_additional.specific_" + str(i) + ".total = tsi_wavg")

    ## Additional Peril Premiums
    for cit_additional in cov.cit_additional.specific_custom:
        prem_wavg = 0.0
        tsi_wavg = 0.0
        for country in ["usa", "na_ex_usa", "sa", "uk", "europe", "asia", "oceania", "africa"]:
            tsi = eval("cit_additional." + country) if eval("cit_additional." + country) != None else 0.0 # Why is this not subscriptable using cit_additional["usa"]? cit_additional[country]
                                                                                                        # SA: because it's a hx object not a pandas df
            rate = eval("cit_additional.rate_" + country) if eval("cit_additional.rate_" + country) != None else 0.0
            prem_additional = prem_additional + tsi * rate
            tsi_additional = tsi_additional + tsi
            prem_wavg = prem_wavg + tsi * rate
            tsi_wavg = tsi_wavg + tsi
        cit_additional.rate_total = prem_wavg / tsi_wavg if tsi_wavg > 0.0 else 0.0
        cit_additional.total = tsi_wavg

    # Currency rate
    fx_rate = hx.params.table_input_currency[hx.params.table_input_currency["ccy"] == cds.currencies.source_currency]["fx_rate"].iloc[0]
    
    # total adjusted for fx rate
    cov.cit_additional.premium = prem_additional / fx_rate
    cov.cit_additional.tsi = tsi_additional / fx_rate

    # Populate exposure rate summary table
    table_exp_curves = hx.params.table_rating_exposure_curves
    for sub_group in ["premises", "additional"]:
        # if eval("cov.cit_" + sub_group + ".ded_perc") != None:
        #     ded_perc = eval("cov.cit_" + sub_group + ".ded_perc")
        # else:
        #     ded_perc = eval("cov.cit_" + sub_group + ".deductible") / eval("cov.cit_" + sub_group + ".tsi") if eval("cov.cit_" + sub_group + ".tsi") > 0 and eval("cov.cit_" + sub_group + ".deductible") != None else 0
        #IR edit:
        if eval("cov.cit_" + sub_group + ".deductible") != None:
            ded_perc = eval("cov.cit_" + sub_group + ".deductible") / eval("cov.cit_" + sub_group + ".tsi") if eval("cov.cit_" + sub_group + ".tsi") > 0 else 0
        else:
            ded_perc = eval("cov.cit_" + sub_group + ".ded_perc") if eval("cov.cit_" + sub_group + ".ded_perc") != None else 0

        credit = table_exp_curves[table_exp_curves.limded <= ded_perc]["cit" + sub_group].iloc[-1]
        exec("cov.cit_" + sub_group + ".credit = credit") # How do assign to a dynamic variable name with local scope?
        credit_applied = eval("cov.cit_" + sub_group + ".uw_adj_impact") if eval("cov.cit_" + sub_group + ".uw_adj_impact") != None else credit
        prem_post_ded = eval("cov.cit_" + sub_group + ".premium") * (1 - credit_applied)
        exec("cov.cit_" + sub_group + ".prem_post_ded = prem_post_ded")
        implied_rate_post_ded = prem_post_ded / eval("cov.cit_" + sub_group + ".tsi") if eval("cov.cit_" + sub_group + ".tsi") > 0 else None
        exec("cov.cit_" + sub_group + ".implied_rate_post_ded = implied_rate_post_ded")
        